#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_evals.py — skill-reviewer 的行為迴歸測試

與 `lint_skill.py --selftest` 的分工:
  - selftest 測「純函式與單一判定」(regex、parser、單條 rule)
  - 本檔測「**對整個 repo 的端到端行為契約**」——擋/不擋分界、change-scoped、exclude

兩組案例:
  1. fixtures/(已提交,CI 一定跑)——合成的最小 repo,涵蓋核心行為契約
  2. evals.json 的真實 repo(在 research/repos/,gitignored)——存在才跑,缺席則跳過並提示

用法:
  python3 skill-reviewer/evals/run_evals.py           # 兩組都跑(真實 repo 缺席則 skip)
  python3 skill-reviewer/evals/run_evals.py --ci      # 只跑 fixtures,缺席不算失敗
"""
import json
import re, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LINT = os.path.join(os.path.dirname(HERE), "scripts", "lint_skill.py")
REPO_ROOT = os.path.dirname(os.path.dirname(HERE))


def lint(repo, *extra):
    r = subprocess.run([sys.executable, LINT, repo, "--json", *extra],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise AssertionError(f"lint 執行失敗 rc={r.returncode}: {r.stderr[:200]}")
    return json.loads(r.stdout)


def hyg(d, rule_id):
    return next(h for h in d["hygiene"] if h["id"] == rule_id)


def blocks(d):
    """gate 會不會被擋 = 有沒有 error 級且未過的 hygiene"""
    return any(h["severity"] == "error" and h["pass"] is False for h in d["hygiene"])


# ── fixture 契約:每條都是「行為」而非「數字」,不會因 rubric 微調而脆斷 ──
def fixture_cases():
    fx = lambda n: os.path.join(HERE, "fixtures", n)

    def c_good():
        d = lint(fx("good-skill"))
        assert not blocks(d), "合格 skill 不該擋 gate"
        assert hyg(d, "H-001")["pass"] is True
        assert hyg(d, "H-005")["pass"] is True
        assert d["packaging_score"] > 0, "有 marketplace/一行安裝/before-after,分數不該是 0"

    def c_blind_spot():
        """H-001 的 repo 級盲點:一好一壞時 H-001 仍 pass,必須靠 H-005 抓到"""
        d = lint(fx("broken-frontmatter"))
        assert hyg(d, "H-001")["pass"] is True, "H-001 是 repo 級,有 1 個合規就 pass(這正是盲點)"
        assert hyg(d, "H-005")["pass"] is False, "H-005 必須抓到那個壞檔"
        assert d["noncompliant_skills"] == ["skills/b/SKILL.md"], d["noncompliant_skills"]
        assert not blocks(d), "repo-wide 情境下既有壞檔只是 warning,不該擋"

    def c_change_scoped():
        """change-scoped:改壞了才擋;沒碰到就不擋(不因別人的爛攤子阻斷你)"""
        base = fx("broken-frontmatter")
        hit = lint(base, "--changed-files", "skills/b/SKILL.md")
        assert hyg(hit, "H-005")["severity"] == "error" and blocks(hit), "本次改壞 → 必須擋"
        miss = lint(base, "--changed-files", "skills/a/SKILL.md")
        assert hyg(miss, "H-005")["severity"] == "warning" and not blocks(miss), "沒碰到壞檔 → 不該擋"

    def c_security_not_blocking():
        """安全紅旗是刻意不擋的(ADR-033 D1);若哪天變成擋,這條會 fail 提醒你那是設計變更"""
        d = lint(fx("security-obey-output"))
        assert any(s["id"] == "S-001" for s in d["security"]), "S-001 應被偵測到"
        assert not blocks(d), "安全紅旗刻意不擋 gate——改成擋屬設計變更,需先改 ADR-033"

    def c_exclude():
        """vendored 目錄不該被算成自己的"""
        base = fx("good-skill")
        n_all = len(lint(base)["craft_llm_todo"])
        n_ex = len(lint(base, "--exclude", "skills")["craft_llm_todo"])
        assert n_all == 1 and n_ex == 0, f"--exclude 未生效:抽樣 {n_all} → {n_ex}(應為 1 → 0)"

    return [("合格 skill 不擋", c_good),
            ("H-001 盲點由 H-005 補上", c_blind_spot),
            ("change-scoped 只擋改壞的", c_change_scoped),
            ("安全紅旗刻意不擋", c_security_not_blocking),
            ("--exclude 排除 vendored", c_exclude),
            ("craft verdict 取值域不漂移", c_verdict_domain),
            ("上卷規則與 evals 一致", c_rollup_matches_rubric),
            ("security 欄位語意(複核≠命中)", c_security_semantics),
            ("security 標註與 lint 實測對帳", c_security_field_matches_lint)]


# ── evals.json 的 security 欄位語意 ────────────────────────────────────────────
# 舊版是 `sec = bool(c["expected"].get("security"))` —— 把「**lint 命中**」直接等同
# 「**經複核確認成立**」。而 SKILL.md:19/:75 與 rubric 的上卷規則第 2 條三處都明禁這個等同
# (「絕不單憑 lint 的 S-001 就判 needs-revision」)。後果不是措辭問題:一個 lint 有紅旗
# 但複核判假陽性的 repo **無法作為 evals 案例存在**,它會被強制算成 needs-revision——
# 而 misjudgments.md 已記多起這種假陽性(anthropics 的 `follow the guide exactly`、
# Jeffallan 的極性反轉、cloudflare 的 `--token`)。
#
# 新 schema:security 是**物件陣列**,`review` 必填。
#   {"id": "S-001", "flag": "obey_external_output", "review": "confirmed"|"false-positive",
#    "source": "為什麼這樣判(行號/理由)"}
# `review` 刻意必填而非有預設 —— CHANGELOG 1.3.1 修過同型的 `bool(None)` 靜默預設。
SECURITY_REVIEW_VALUES = ("confirmed", "false-positive")


def _lint_module():
    """import lint_skill,sys.path 只動一次。

    (2026-08-27 複審 F8:原本兩個函式各自 `sys.path.insert(0, ...)`,每次呼叫都插一筆
     —— 實測跑一輪 fixture 後 sys.path 由 11 長到 31,20 筆重複。行程內、無磁碟殘留,
     但那是「沒人負責收」的副作用,本 repo 的驗收會逐項清點它。)
    """
    _p = os.path.join(HERE, "..", "scripts")
    if _p not in sys.path:
        sys.path.insert(0, _p)
    import lint_skill as L
    return L


def security_confirmed(expected):
    """evals.json 的 security 欄位 → rollup 的 `security_error_confirmed`。

    只有**經複核確認成立**且**severity 為 error** 的紅旗才會翻 verdict。
    severity 不在 evals.json 裡自己再編一次,而是查 `lint_skill.SECURITY_SEVERITY`
    (ADR-031:同一意義兩處編碼會 drift)。
    """
    L = _lint_module()
    out = False
    for e in expected.get("security") or []:
        assert isinstance(e, dict), \
            f"security 必須是物件陣列(舊的字串陣列語意含混,已淘汰):{e!r}"
        for k in ("id", "flag", "review"):
            assert e.get(k), f"security 條目缺必填欄位 `{k}`:{e}"
        assert e["review"] in SECURITY_REVIEW_VALUES, \
            f"review 取值域外:{e['review']}(僅 {SECURITY_REVIEW_VALUES})"
        assert e["flag"] in L.SECURITY_SEVERITY, \
            f"未知 flag `{e['flag']}` —— 與 lint_skill.SECURITY_RULES 不同步"
        if e["review"] == "confirmed" and L.SECURITY_SEVERITY[e["flag"]] == "error":
            out = True
    return out


def case_verdict(expected):
    """一個 evals case 的 expected → 上卷規則算出的 craft verdict。

    抽成函式是為了讓 fixture 能行使**同一條路徑**。否則
    `sec = security_confirmed(...)` 這個呼叫點退回 `bool(...)` 不會被任何斷言接到
    ——真實 case 裡沒有「有 craft_dimensions 且 security 為假陽性」的組合,
    兩種寫法在現有語料上答案相同(實測)。守衛不能只在資料剛好行使到時才有效。
    """
    L = _lint_module()
    return L.craft_verdict_rollup(
        expected["craft_dimensions"],
        hygiene_error=str(expected.get("hygiene", "")).startswith("FAIL"),
        security_error_confirmed=security_confirmed(expected))


def absence_note(n_checked, n_absent):
    """對帳結果的自述:跳過任何一筆就必須說出來,回傳 None 代表「全部都對帳了」。

    ⚠️ 條件是 `if n_absent`,**不是** `if n_absent and not n_checked`(2026-08-27 複審 F2)。
    舊條件讓「**部分**缺席」落進沉默:只要有一個 repo 在場,另一個缺席 repo 的標註
    就一次都沒對帳,而該 case 照樣印 ✓。那與 CHANGELOG 1.3.1「selftest 不得靜默降級」
    直接抵觸,也正是本函式所屬的斷言自己要修的失效型(用 skip 換一個「已驗證」的錯覺)。

    抽成純函式的理由與 `case_verdict()` 同:**這條分支在本機永遠走不到**
    (`research/repos/` 五個 repo 都在,`n_absent` 恆為 0),在 CI 上又永遠只走全缺席那一格。
    「部分缺席」是真實會發生(clone 到一半、只留 evals 需要的子集)卻**兩種環境都測不到**的狀態,
    只有純函式斷言接得住。寫法對齊 lint_skill 的 `drift-guard 比對 N/M 條`。
    """
    if not n_absent:
        return None
    return (f"已對帳 {n_checked} 筆、未對帳 {n_absent} 筆(real repo 缺席;"
            f"schema 與語意仍由 fixture 覆蓋)")


def c_security_semantics():
    """`security` 欄位的行為契約,全部由 **committed fixture** 驅動(不依賴 gitignored repo)。

    ⚠️ 為什麼一定要有 fixture:`research/repos/` 是 gitignored,任何只跑在真實 repo 上的
    新斷言在 CI 上會 skip —— 那等於用 skip 換一個「已驗證」的錯覺。
    ADR-033:162 那個「已驗證 ✅」就是這樣壞掉的(它斷言的 `blocks()` 只看 hygiene error,
    對任何沒有 hygiene error 的 repo 恆為真,即使 S-001 完全不再被偵測到照樣綠)。
    """
    fxp = os.path.join(HERE, "fixtures", "security-obey-output")
    d = lint(fxp)
    flags = {s.get("flag") for s in d["security"]}
    assert "obey_external_output" in flags, f"fixture 應命中 S-001,實得 {flags}"

    # 契約 1:同一份 lint 輸出,`review` 不同 → verdict 不同。這正是舊 schema 表達不了的事。
    conf = security_confirmed({"security": [
        {"id": "S-001", "flag": "obey_external_output", "review": "confirmed",
         "source": "fixture:SKILL.md"}]})
    fp = security_confirmed({"security": [
        {"id": "S-001", "flag": "obey_external_output", "review": "false-positive",
         "source": "fixture:SKILL.md"}]})
    assert conf is True and fp is False, (conf, fp)

    # 契約 2:warning 級紅旗即使複核確認成立也**不翻 verdict**(上卷規則第 2 條只認 error)
    warn = security_confirmed({"security": [
        {"id": "S-003", "flag": "cred_in_argv", "review": "confirmed", "source": "x"}]})
    assert warn is False, "warning 級紅旗不得翻 verdict —— 上卷規則第 2 條只認 error"

    # 契約 3:**端到端** —— 全 good 維度 + 一個複核為假陽性的 error 級紅旗 → 仍是 approved。
    # 這是舊 schema 表達不了的那個 case,現有真實語料裡剛好沒有(anthropics 有假陽性但沒標
    # craft_dimensions),所以在此用合成 expected 行使同一條路徑。
    approved_dims = {"L-001": "good", "L-002": "good", "L-003": "good", "L-004": "good"}
    assert case_verdict({"craft_dimensions": approved_dims, "security": [
        {"id": "S-001", "flag": "obey_external_output", "review": "false-positive",
         "source": "合成"}]}) == "approved", \
        "複核為假陽性的紅旗不得翻 verdict —— 呼叫點是否退回 bool(security)?"
    assert case_verdict({"craft_dimensions": approved_dims, "security": [
        {"id": "S-001", "flag": "obey_external_output", "review": "confirmed",
         "source": "合成"}]}) == "needs-revision", \
        "複核確認成立的 error 級紅旗必須翻 verdict(上卷規則第 2 條)"

    # 契約 4:對帳結果的自述 —— **部分缺席不得靜默**(2026-08-27 複審 F2)。
    # 這三格在本機與 CI 都走不到「部分缺席」,只有純函式斷言接得住。
    assert absence_note(2, 0) is None, "全部對帳完不該多印東西"
    for _c, _a in ((0, 2), (1, 1), (5, 1)):
        _n = absence_note(_c, _a)
        assert _n and f"已對帳 {_c} 筆" in _n and f"未對帳 {_a} 筆" in _n, \
            f"跳過 {_a} 筆卻沒說出來(或數字不對):{_n!r}"
    assert absence_note(1, 1), \
        "**部分**缺席必須出聲——條件若退回 `n_absent and not n_checked`,這一格會靜默"

    # 契約 5:缺 `review` 必須炸,不得靜默當成 False(bool(None) 型的靜默預設)
    for bad in ({"security": [{"id": "S-001", "flag": "obey_external_output"}]},
                {"security": [{"id": "S-001", "flag": "obey_external_output", "review": "maybe"}]},
                {"security": ["S-001 obey_external_output"]},
                {"security": [{"id": "S-001", "flag": "no_such_flag", "review": "confirmed"}]}):
        try:
            security_confirmed(bad)
        except AssertionError:
            continue
        raise AssertionError(f"應該拒絕卻放行了:{bad}")


def c_security_field_matches_lint():
    """凡 evals.json 的 case 標了 `security`,lint 必須真的在該 repo 命中該 flag。

    這條同時把 ADR-033:162 那個空過的「已驗證 ✅」補實 —— 那一列宣稱
    「已知假陽性不擋 → anthropics/skills 的 S-001 → eval 案例實跑」,而它斷言的
    `blocks(d) is False` 對任何沒有 hygiene error 的 repo 恆為真。
    真實 repo 缺席時本條 skip(缺席資訊由 real_repo_cases 統一回報),
    **但 schema 與語意由上一條的 fixture 全程覆蓋**。
    """
    spec = json.load(open(os.path.join(HERE, "evals.json"), encoding="utf-8"))
    n_checked = n_absent = 0
    for c in spec["cases"]:
        ents = c["expected"].get("security") or []
        if not ents:
            continue
        security_confirmed(c["expected"])          # schema 先過(缺欄即炸)
        repo = os.path.join(REPO_ROOT, c["repo"])
        if not os.path.isdir(repo):
            n_absent += len(ents); continue
        got = {s.get("flag") for s in lint(repo)["security"]}
        for e in ents:
            assert e["flag"] in got, (
                f"{c['repo']}: evals 標了 {e['id']}/{e['flag']} 但 lint 沒命中(實得 {got})"
                " —— 標註與偵測脫節,這正是『證據說謊』")
            n_checked += 1
    return absence_note(n_checked, n_absent)


# craft verdict 的取值域與上卷規則,canonical 在
# references/rubric-manual-dimensions.yaml 的 craft_verdict_rollup。
# 可執行鏡像在 scripts/lint_skill.py 的 craft_verdict_rollup(),由下方兩條守衛釘住三者不漂移。
CRAFT_VERDICT_VALUES = ("approved", "approved-with-notes", "needs-revision")

_ROLLUP_KEY = "craft_verdict_rollup:"


def _rubric_block():
    """取出 rubric 的 craft_verdict_rollup 區塊(從該鍵到下一個頂層鍵)。

    ⚠️ **必須夾範圍**(2026-08-27 獨立複審 high 1):前一版用**全檔 substring** 比對,
    而三個取值字串在條文散文裡到處都是,於是突變模擬顯示——
    刪掉整行 `values:`、把 `needs-revision` 改名、加入第 4 個值,**三種都照樣通過**。
    當時我只測過「整個區塊改名」(那確實會擋),就宣稱做過負向驗證。
    """
    path = os.path.join(HERE, "..", "references", "rubric-manual-dimensions.yaml")
    txt = open(path, encoding="utf-8").read()
    assert _ROLLUP_KEY in txt, f"rubric 缺 {_ROLLUP_KEY} —— 取值域無 canonical 來源"
    body = txt.split(_ROLLUP_KEY, 1)[1]
    # 下一個頂層鍵 = 行首非空白的 `xxx:`;沒有就到檔尾
    m = re.search(r"^(?=\S)[A-Za-z_][\w-]*:", body, re.M)
    # ⚠️ 找不到邊界時**不得**默默延伸到檔尾——那會讓本守衛退化回「全檔比對」,
    # 也就是 high 1 當初失效的狀態(實測:下一個頂層鍵寫成 `"security":` 時
    # 夾範圍由 2615 → 7445 chars 且無任何訊號,該狀態下可構造出守衛放行)。
    # 與 CHANGELOG 1.3.1「selftest 不得靜默降級」同一主題。
    assert m, ("找不到 craft_verdict_rollup 的下一個頂層鍵 —— 夾範圍失效,"
               "守衛會退化成全檔比對(那正是 high 1 的失效模式)")
    return body[:m.start()]


def c_verdict_domain():
    """三處取值域必須**集合相等**:rubric 的 values / lint 的常數 / evals.json 的實際值。

    來歷:`evals.json` 長期寫著 `approved-with-notes`,而 SKILL.md 說「取值域僅此兩個」
    ——條文與 evals 對不上且無任何東西會轉紅。這條是那個缺口的守衛。
    """
    block = _rubric_block()
    m = re.search(r"^\s*values:\s*\[([^\]]*)\]", block, re.M)
    assert m, "rubric 的 craft_verdict_rollup 缺 values: [...] —— 取值域無來源"
    rubric_vals = {v.strip() for v in m.group(1).split(",") if v.strip()}
    # **集合相等**,不是逐個 `in`。逐個 in 會被子字串吃掉
    # ('approved' in 'approved-with-notes' == True),那圈永遠不可能獨立失敗。
    assert rubric_vals == set(CRAFT_VERDICT_VALUES), \
        f"取值域漂移:rubric={sorted(rubric_vals)} vs 程式={sorted(CRAFT_VERDICT_VALUES)}"
    spec = json.load(open(os.path.join(HERE, "evals.json"), encoding="utf-8"))
    bad = [(c["repo"], c["expected"].get("craft_verdict"))
           for c in spec["cases"]
           if c["expected"].get("craft_verdict") not in CRAFT_VERDICT_VALUES]
    assert not bad, f"evals.json 的 craft_verdict 落在取值域外:{bad}"


def c_rollup_matches_rubric():
    """evals.json 標了 craft_dimensions 的 case,其 craft_verdict 必須等於純函式算出來的。

    ⚠️ 這是本 PR 主行為(`≥2 mixed → needs-revision`)**唯一**的可執行覆蓋。
    在此之前 `craft_dimensions` 沒有任何程式讀取,而 CHANGELOG 標 major
    「同樣的輸入會得到不同的 verdict」——沒有一條斷言鎖住那個 verdict(複審 high 2)。
    """
    L = _lint_module()
    spec = json.load(open(os.path.join(HERE, "evals.json"), encoding="utf-8"))
    n = 0
    for c in spec["cases"]:
        dims = c["expected"].get("craft_dimensions")
        if not dims:
            continue
        n += 1
        want = c["expected"]["craft_verdict"]
        # ⚠️ 用 startswith 不是 ==:`evals.json` 的實際值帶診斷後綴
        # (`"FAIL(H-001:68 個 SKILL.md 全無 frontmatter…)"`),`== "FAIL"` 對唯一有值的
        # case 恆為 False —— 那是一條死映射,會擋下正確條目(獨立複審實測)。
        got = case_verdict(c["expected"])
        assert got == want, f"{c['repo']}: 上卷算出 {got} 但 evals 標 {want}(dims={dims})"
    # ⚠️ 下限 >=2 而非 >=1:實測顯示 >=1 允許本 PR **唯一**行使
    # 「≥2 mixed → needs-revision」的那個 case 被無聲刪除而守衛仍 PASS
    # (三態守衛接不到,因為 needs-revision 由其他 case 的 craft_verdict 就覆蓋了,
    #  而那些 case 從未與維度對帳)。
    assert n >= 2, f"標了 craft_dimensions 的 case 只有 {n} 個 —— 上卷規則覆蓋不足"
    # `craft_only_verdict`:門檻(hygiene/security)蓋掉維度時,craft 本身的值。
    # 它讓「門檻優先於維度」這件事可被斷言,而不只是條文裡的一句話。
    for c in spec["cases"]:
        dims = c["expected"].get("craft_dimensions")
        only = c["expected"].get("craft_only_verdict")
        if not (dims and only):
            continue
        got = L.craft_verdict_rollup(dims)          # 不帶門檻
        assert got == only, f"{c['repo']}: craft-only 算出 {got} 但 evals 標 {only}"
        assert only != c["expected"]["craft_verdict"], \
            f"{c['repo']}: craft_only_verdict 與 craft_verdict 相同,這個欄位就沒有意義"
    # 取值域三態各至少要被行使一次(含 craft_only_verdict)。
    # 否則會出現「合法化了一個值卻沒有任何案例長那樣」——複審實測過:
    # Jeffallan 由 approved-with-notes 改判 needs-revision 後,第三態一個 case 都不剩。
    seen = {c["expected"].get("craft_verdict") for c in spec["cases"]}
    seen |= {c["expected"].get("craft_only_verdict") for c in spec["cases"]}
    missing = set(CRAFT_VERDICT_VALUES) - seen
    assert not missing, f"取值域有值零覆蓋:{sorted(missing)} —— 合法化了卻沒有案例行使它"


def real_repo_cases():
    """evals.json 的真實 repo(gitignored)。只斷言穩定的行為,不鎖具體分數。"""
    spec = json.load(open(os.path.join(HERE, "evals.json"), encoding="utf-8"))
    expect_block = {"24kchengYe__human-skill-tree": True}     # 其餘皆不該擋
    out = []
    for case in spec["cases"]:
        repo = os.path.join(REPO_ROOT, case["repo"])
        name = case["name"][:38]
        if not os.path.isdir(repo):
            out.append((name, None)); continue
        key = os.path.basename(repo)
        def check(repo=repo, key=key):
            d = lint(repo)
            want = expect_block.get(key, False)
            assert blocks(d) is want, f"{key}: 擋={blocks(d)} 但預期={want}"
        out.append((name, check))
    return out


def main():
    ci = "--ci" in sys.argv
    failed = skipped = 0

    print("── fixtures(行為契約,CI 必跑)──")
    for name, fn in fixture_cases():
        try:
            # case 回傳非 None 時是「這條打了折」的自述,印在**它自己的 ✓ 之後**。
            # (2026-08-27 複審 F7:原本 case 內直接 print,揭露行落在自己的 ✓ 之前,
            #  視覺上掛到上一條去了 —— 揭露的位置錯了等於沒揭露。)
            note = fn()
            print(f"  ✓ {name}" + (f" — ⚠️ {note}" if note else ""))
        except (AssertionError, ValueError) as e:
            print(f"  ✗ {name}: {e}"); failed += 1

    print("── 真實 repo(research/repos/,gitignored)──")
    for name, fn in real_repo_cases():
        if fn is None:
            print(f"  ○ {name} — clone 不存在,跳過"); skipped += 1; continue
        try:
            fn(); print(f"  ✓ {name}")
        except (AssertionError, ValueError) as e:
            print(f"  ✗ {name}: {e}"); failed += 1

    print()
    if skipped and not ci:
        print(f"提示:{skipped} 個真實 repo 案例被跳過。重建:python3 scripts/clone_repos.py")
        print("     (重建拿到的是上游 HEAD,非原快照——見 research/repos/README.md)")
    if failed:
        print(f"❌ {failed} 個案例失敗"); return 1
    print(f"✅ 全部通過(跳過 {skipped} 個)"); return 0


if __name__ == "__main__":
    sys.exit(main())
