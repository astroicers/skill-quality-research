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
import json, os, subprocess, sys

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
            ("craft verdict 取值域不漂移", c_verdict_domain)]


# craft verdict 的取值域,canonical 在 references/rubric-manual-dimensions.yaml
# 的 craft_verdict_rollup.values,以及 SKILL.md 的「craft 的取值規則」表。
# ⚠️ 這裡硬編一份是為了讓 CI 在**沒有 YAML parser** 的環境也能守門(本工具零依賴);
# 兩處不得漂移——下方 c_verdict_domain 會拿本常數去比對 rubric 檔的字面內容。
CRAFT_VERDICT_VALUES = ("approved", "approved-with-notes", "needs-revision")


def c_verdict_domain():
    """evals.json 的 craft_verdict 必須落在取值域內,且取值域本身不得與 rubric 漂移。

    來歷(2026-08-27):`evals.json` 長期寫著 `approved-with-notes`,而當時 SKILL.md 明寫
    「取值域僅此兩個(approved / needs-revision)」——**條文與 evals 對不上,且沒有任何
    東西會因此轉紅**。這條就是那個缺口的守衛。
    """
    spec = json.load(open(os.path.join(HERE, "evals.json"), encoding="utf-8"))
    bad = [(c["repo"], c["expected"].get("craft_verdict"))
           for c in spec["cases"]
           if c["expected"].get("craft_verdict") not in CRAFT_VERDICT_VALUES]
    assert not bad, f"evals.json 的 craft_verdict 落在取值域外:{bad}"
    # 取值域與 rubric 正本不得漂移(字面比對,零依賴)
    rubric = os.path.join(HERE, "..", "references", "rubric-manual-dimensions.yaml")
    txt = open(rubric, encoding="utf-8").read()
    assert "craft_verdict_rollup:" in txt, "rubric 缺 craft_verdict_rollup —— 取值域無 canonical 來源"
    for v in CRAFT_VERDICT_VALUES:
        assert v in txt, f"取值 {v!r} 不在 rubric 的 craft_verdict_rollup 內 —— 兩處已漂移"


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
