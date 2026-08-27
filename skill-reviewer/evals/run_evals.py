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
            ("上卷規則與 evals 一致", c_rollup_matches_rubric)]


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
    return body[:m.start()] if m else body


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
    sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
    import lint_skill as L
    spec = json.load(open(os.path.join(HERE, "evals.json"), encoding="utf-8"))
    n = 0
    for c in spec["cases"]:
        dims = c["expected"].get("craft_dimensions")
        if not dims:
            continue
        n += 1
        want = c["expected"]["craft_verdict"]
        hyg = c["expected"].get("hygiene") == "FAIL"
        sec = bool(c["expected"].get("security"))
        got = L.craft_verdict_rollup(dims, hygiene_error=hyg, security_error_confirmed=sec)
        assert got == want, f"{c['repo']}: 上卷算出 {got} 但 evals 標 {want}(dims={dims})"
    assert n >= 1, "沒有任何 case 標了 craft_dimensions —— 上卷規則零覆蓋"
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
            fn(); print(f"  ✓ {name}")
        except AssertionError as e:
            print(f"  ✗ {name}: {e}"); failed += 1

    print("── 真實 repo(research/repos/,gitignored)──")
    for name, fn in real_repo_cases():
        if fn is None:
            print(f"  ○ {name} — clone 不存在,跳過"); skipped += 1; continue
        try:
            fn(); print(f"  ✓ {name}")
        except AssertionError as e:
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
