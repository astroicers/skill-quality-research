#!/usr/bin/env python3
"""量測 rubric 判準改動對現有語料的影響,並把母體與方法寫死成可重跑的東西。

**為什麼存在**(2026-08-26 獨立複審 F-5 / F-6):
rubric 2.2.0 的兩條改動各自附了數字(「更正 2、回歸 0」「校準 N/N」),但當時
母體只寫在散文裡、量測只活在一次性腳本中,repo 內沒有可重跑的東西。複審指出兩件事:

  F-6 母體不可**重**現 —— 「38 已安裝 skill + 5 repo 快照 + 16 corpus」沒說是哪三個根目錄,
      也沒說 `os.walk` 跟不跟隨 symlink(不跟隨時 SKILL.md 數 38、跟隨時 58,
      而「只新增 2 個命中」**只在跟隨時成立**)。
  F-5 S-101 的校準母體是 SKILL.md,但**生產偵測面是整個 repo 的 `.md/.yml/.yaml/.sh`**
      (`lint_skill.analyze` 的 `all_text`)。用比生產面窄的母體校準會系統性低估假陽性曝險。

本腳本把兩者都釘住:母體 = 三個具名根目錄,S-101 一律量**生產面**。

用法:
    python3 scripts/measure_rubric_impact.py              # 印報告
    python3 scripts/measure_rubric_impact.py --json       # 機器可讀
    python3 scripts/measure_rubric_impact.py --selftest   # 純函式斷言(CI 用)

⚠️ **完整量測只能在具備本機語料的環境跑。** 三個母體根在 CI 上**全部不可得**:
`~/.claude/skills` 是本機路徑;`research/inter-rater/corpus/` 追蹤 0 檔(gitignored);
`research/repos/` 只追蹤一個 README。所以 `measure.txt` 這份證據永遠只有作者機器能產生,
複審者要驗證得自己重跑。缺席時本腳本**跳過該根並明說**,不會假裝量過。

**CI 上跑的是 `--selftest`**,而它兩組斷言都自建 fixture、不依賴上述任何一個根——
所以 CI 綠代表「判定函式與特徵抽取正確」,**不代表 59 目標量測跑過**。這兩件事不要混。
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "skill-reviewer", "scripts"))
import lint_skill as L  # noqa: E402

# 2.1.1 的 S-101 偵測(純英文字面)。留一份在此當**基準線**,
# 好讓「2.2.0 新增了幾個命中」成為可重跑的 delta 而不是散文裡的宣稱。
DEFENSE_UNTRUSTED_LEGACY = re.compile(
    r"(?is)(untrusted\s+data|as\s+data,?\s+not\s+instructions|"
    r"never\s+follow\s+(?:instructions|embedded)|treat\s+external\s+content\s+as\s+data)")

# ── 母體:三個具名根目錄。不是「38 + 5 + 16」這種只有作者知道的數字 ────────────
REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
CORPUS_ROOTS = [
    ("installed-skills", os.path.expanduser("~/.claude/skills"), True),   # 含 symlink → 跟隨
    ("repo-snapshots",   os.path.join(REPO, "research", "repos"), False),
    ("inter-rater",      os.path.join(REPO, "research", "inter-rater", "corpus"), False),
]

# ── 被比較的兩種 knowledge_only 判定 ──────────────────────────────────────────
def ko_current(pct_prose, pct_md, n_code, dir_scripts):
    """現行(rubric 2.2.0):量散文,門檻保留。"""
    return pct_prose >= 85.0 and n_code <= 2 and not dir_scripts

def ko_legacy(pct_prose, pct_md, n_code, dir_scripts):
    """2.1.1:量 .md,門檻保留。"""
    return pct_md >= 85.0 and n_code <= 2 and not dir_scripts

def ko_no_threshold(pct_prose, pct_md, n_code, dir_scripts):
    """被否決的替代修法:直接拿掉門檻。留在這裡是為了讓「它會回歸」可以被重跑驗證。"""
    return n_code <= 2 and not dir_scripts


def scan_dir(path, followlinks):
    """取一個目標的特徵 + 生產面文本。只讀檔,不執行任何受審檔案。

    ⚠️ **特徵一律取自 `lint_skill.analyze`,本檔不自行重算**(ADR-031:同一意義兩處編碼會 drift)。
    獨立複審第二輪 finding 6 指出前一版重寫了一份抽取邏輯,並實測出三處會分歧的地方
    (`.markdown` 是否計入 `n_md`、`Scripts/` 的大小寫、空的 `scripts/` 目錄)——
    在當時 59 個目標上碰不到,但基準線 `ko_legacy` 正是拿 `pct_markdown` 算的,一旦碰到就錯。
    現在唯一的判定來源是 `lint_skill`,本檔只負責:母體定義、`followlinks`、生產面文本。
    """
    m = L.analyze(path)
    if m["_n_files_total"] == 0:
        return None
    prod_chunks = []
    for dp, dirs, fs in os.walk(path, followlinks=followlinks):
        dirs[:] = [d for d in dirs if d not in L.SKIP_DIRS]
        for f in fs:
            # 生產偵測面:與 lint_skill.analyze 的 all_text 同一組副檔名
            if f.lower().endswith((".md", ".yml", ".yaml", ".sh")):
                prod_chunks.append(L.read_text(os.path.join(dp, f)))
    return {
        "files": m["_n_files_total"],
        "pct_md": m["pct_markdown"],
        "pct_prose": m["pct_prose"],
        "code": m["code_file_count"],
        "dir_scripts": m["dir_scripts"],
        "lint_knowledge_only": m["knowledge_only"],   # 用來斷言本檔的 ko_current 與它等價
        "prod_text": "\n".join(prod_chunks)[:2_000_000],
    }


def measure():
    targets, skipped = [], []
    for label, root, follow in CORPUS_ROOTS:
        if not os.path.isdir(root):
            skipped.append({"root": label, "path": root, "reason": "不存在"})
            continue
        for d in sorted(os.listdir(root)):
            p = os.path.join(root, d)
            if not os.path.isdir(p):
                continue
            m = scan_dir(p, follow)
            if m:
                targets.append({"root": label, "name": d, **m})

    ko_diff, ko_diff_nothresh, s101_hits, s101_added = [], [], [], []
    for t in targets:
        args = (t["pct_prose"], t["pct_md"], t["code"], t["dir_scripts"])
        cur, leg, noth = ko_current(*args), ko_legacy(*args), ko_no_threshold(*args)
        if cur != leg:
            ko_diff.append({**{k: t[k] for k in ("root", "name", "pct_md", "pct_prose", "code")},
                            "legacy": leg, "current": cur})
        if noth != leg:
            ko_diff_nothresh.append({"root": t["root"], "name": t["name"],
                                     "pct_prose": t["pct_prose"], "legacy": leg, "no_threshold": noth})
        # S-101:量**生產面**(F-5),不是只量 SKILL.md。
        # 同時對 legacy(2.1.1 的純英文 regex)取基準線 —— 沒有它就重現不了
        # 「2.2.0 新增 N 個命中」這句宣稱(複審 finding 8:變數名宣稱有基準線但實際沒有)。
        now = L.defense_untrusted_hit(t["prod_text"])
        was = bool(DEFENSE_UNTRUSTED_LEGACY.search(t["prod_text"]))
        if now:
            s101_hits.append({"root": t["root"], "name": t["name"], "in_legacy": was})
        if now and not was:
            s101_added.append({"root": t["root"], "name": t["name"]})

    return {
        "corpus_roots": [{"label": l, "path": p, "followlinks": f} for l, p, f in CORPUS_ROOTS],
        "skipped_roots": skipped,
        "n_targets": len(targets),
        "n_by_root": {l: sum(1 for t in targets if t["root"] == l) for l, _, _ in CORPUS_ROOTS},
        "knowledge_only_changed": ko_diff,
        "no_threshold_variant_changed": ko_diff_nothresh,
        "s101_hits_production_surface": s101_hits,
        "s101_added_by_2_2_0": s101_added,
    }


def _selftest_extraction():
    """特徵抽取與判定等價性的斷言 —— **自建 fixture,不依賴任何語料**。

    來歷(兩輪複審,同一個缺陷換了兩次位置):
      第二輪 finding 7:前一版的 selftest 11 條全部落在三個純判定函式上,
        而 F-5/F-6 要修的其實是母體定義、symlink 處理、特徵抽取 —— 那一半零斷言。
      第三輪 finding 2:補上的那一半**在 CI 上一條都不跑**,而 docstring 寫著
        「用已進版控的 `research/inter-rater/corpus`…CI 上也跑得到」——**那句話是假的**。
        `research/inter-rater/corpus/` 被 `.gitignore:14` 排除,`git ls-files` = 0;
        守衛因此在 CI 上必定成立,整組靜默跳過,而 `selftest()` 結尾照樣印
        「all assertions passed ✔」。skip 訊息還把原因誤診成「淺 checkout?」。
        **同一份 `validate.yml:128` 早就寫過 `research/repos/` 是 gitignored 拿不到,
        同一個知識沒有套用到這裡。**

    所以現在**一個外部路徑都不依賴**:fixture 用 `tempfile` 當場建。
    這樣它在 CI、在作者機器、在淺 checkout 上跑的是同一組東西。
    """
    import tempfile

    # ① 純資料目錄:散文 0% —— 「不是程式碼 ≠ 是散文」的固化樣本,
    #    也是「取消門檻」那個被否決修法的回歸來源
    with tempfile.TemporaryDirectory() as td:
        d = os.path.join(td, "pure-data"); os.makedirs(d)
        for i in range(15):
            open(os.path.join(d, f"r{i}.json"), "w").write("{}")
        m = scan_dir(d, False)
        assert m["pct_prose"] == 0.0, ("純資料目錄應為 0% 散文", m["pct_prose"])
        assert m["code"] == 0, m["code"]
        assert ko_current(m["pct_prose"], m["pct_md"], m["code"], m["dir_scripts"]) is False
        assert ko_no_threshold(m["pct_prose"], m["pct_md"], m["code"], m["dir_scripts"]) is True, \
            "前提:取消門檻的修法確實會讓純資料目錄翻 True"

    # ② 散文非 .md:`.txt` + `LICENSE` —— 2.2.0 的兩個實測反例形態
    with tempfile.TemporaryDirectory() as td:
        d = os.path.join(td, "prose"); os.makedirs(os.path.join(d, "docs"))
        open(os.path.join(d, "SKILL.md"), "w").write("---\nname: s\ndescription: Use when X.\n---\nb\n")
        open(os.path.join(d, "docs", "source.txt"), "w").write("prose")
        open(os.path.join(d, "LICENSE"), "w").write("MIT")
        m = scan_dir(d, False)
        assert m["pct_md"] < 85.0 and m["pct_prose"] == 100.0, (m["pct_md"], m["pct_prose"])
        assert ko_legacy(m["pct_prose"], m["pct_md"], m["code"], m["dir_scripts"]) is False, \
            "前提:舊規則在此形態上確實會 False"
        assert ko_current(m["pct_prose"], m["pct_md"], m["code"], m["dir_scripts"]) is True

    # ③ **ko_current 必須與 lint_skill 的 knowledge_only 等值**(ADR-031 的機械守衛)。
    #    含 `.markdown`、`Scripts/`(大寫)、空 `scripts/` —— 正是複審實測出兩份實作
    #    會分歧的三個地方。現在 scan_dir 直接取 lint 的特徵,這組驗的是它沒有再分岔。
    cases = [
        ("md-only",     [("SKILL.md", "x")], []),
        ("markdown-ext",[("SKILL.md", "x"), ("a.markdown", "x")], []),
        ("upper-script",[("SKILL.md", "x")], ["Scripts"]),
        ("empty-script",[("SKILL.md", "x")], ["scripts"]),
        ("with-code",   [("SKILL.md", "x"), ("a.py", "x"), ("b.py", "x"), ("c.py", "x")], []),
        ("mixed",       [("SKILL.md", "x"), ("d.json", "{}"), ("NOTICE", "x")], []),
    ]
    for name, files, dirs in cases:
        with tempfile.TemporaryDirectory() as td:
            d = os.path.join(td, name); os.makedirs(d)
            for sub in dirs:
                os.makedirs(os.path.join(d, sub))
            for fn, body in files:
                open(os.path.join(d, fn), "w").write(body)
            m = scan_dir(d, False)
            assert m is not None, name
            assert ko_current(m["pct_prose"], m["pct_md"], m["code"], m["dir_scripts"]) \
                == m["lint_knowledge_only"], f"判定與 lint_skill 分歧:{name}"

    # ④ 空目錄不得讓抽取炸掉,也不得被算成目標
    with tempfile.TemporaryDirectory() as td:
        assert scan_dir(td, False) is None, "空目錄應回 None"


def selftest():
    """純函式斷言 —— 不依賴本機語料,CI 可跑。"""
    # ko_current 只在「散文足量 + 無可執行內容」時為真
    assert ko_current(100.0, 50.0, 0, False) is True
    assert ko_current(85.0, 0.0, 0, False) is True, "門檻是 >= 不是 >"
    assert ko_current(84.9, 100.0, 0, False) is False
    assert ko_current(100.0, 100.0, 3, False) is False, "code>2 不得豁免"
    assert ko_current(100.0, 100.0, 0, True) is False, "有 scripts/ 不得豁免"
    # legacy 在兩個實測反例上確實會失敗(這是本次改動的前提)
    assert ko_legacy(100.0, 75.0, 0, False) is False, "前提:good-writing-tw 形態舊規則判 False"
    assert ko_legacy(100.0, 50.0, 0, False) is False, "前提:humanizer-en 形態舊規則判 False"
    assert ko_current(100.0, 75.0, 0, False) is True
    assert ko_current(100.0, 50.0, 0, False) is True
    # 被否決的修法在純資料目錄上確實會回歸
    assert ko_no_threshold(0.0, 0.0, 0, False) is True, "前提:取消門檻會讓純資料目錄翻 True"
    assert ko_current(0.0, 0.0, 0, False) is False, "現行修法不得讓純資料目錄豁免"
    _selftest_extraction()
    # 輸出要說**跑了什麼**。原本只印「all assertions passed ✔」,
    # 而抽取那一組曾經依賴 gitignored 語料、在 CI 上整組靜默跳過——
    # 「全部通過」與「所有*可用的*通過」當時分不出來。現在兩組都自建 fixture,
    # 但輸出仍須點名,否則下一組環境相依的斷言會重演同一件事。
    print("[selftest] measure_rubric_impact: 全部通過 ✔"
          "(純判定函式 + 特徵抽取/與 lint_skill 等值比對;兩組皆自建 fixture,"
          "無外部語料依賴,故 CI 與本機跑的是同一組)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest()
        return 0
    r = measure()
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0
    print("母體(三個具名根目錄):")
    for c in r["corpus_roots"]:
        n = r["n_by_root"].get(c["label"], 0)
        print(f"  {c['label']:18s} n={n:3d}  followlinks={c['followlinks']}  {c['path']}")
    for s in r["skipped_roots"]:
        print(f"  ⚠️ 跳過 {s['root']}({s['reason']}):{s['path']} —— 本次未量到這一根")
    print(f"  合計 n={r['n_targets']}\n")
    print(f"knowledge_only 2.1.1 → 2.2.0 判定改變:{len(r['knowledge_only_changed'])}")
    for d in r["knowledge_only_changed"]:
        print(f"    {d['root']}:{d['name']:26s} md={d['pct_md']:5.1f}% prose={d['pct_prose']:5.1f}% "
              f"code={d['code']}  {d['legacy']} → {d['current']}")
    print(f"\n被否決的『取消門檻』修法判定改變:{len(r['no_threshold_variant_changed'])}"
          f"  ← 多出來的就是它的回歸")
    for d in r["no_threshold_variant_changed"]:
        print(f"    {d['root']}:{d['name']:26s} prose={d['pct_prose']:5.1f}%  "
              f"{d['legacy']} → {d['no_threshold']}")
    print(f"\nS-101 命中(**生產偵測面** all_text,非僅 SKILL.md):{len(r['s101_hits_production_surface'])}")
    for d in r["s101_hits_production_surface"]:
        print(f"    {d['root']}:{d['name']:26s} {'(2.1.1 即已命中)' if d['in_legacy'] else '← 2.2.0 新增'}")
    print(f"  其中 2.2.0 新增:{len(r['s101_added_by_2_2_0'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
