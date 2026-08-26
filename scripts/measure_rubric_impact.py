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

⚠️ `~/.claude/skills` 是本機、可變、未進版控的目錄。缺席時本腳本**跳過該根並明說**,
不會假裝量過——這正是它要防的那種說謊。
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "skill-reviewer", "scripts"))
import lint_skill as L  # noqa: E402

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
    """重算一個目標的三種判定 + 生產面文本。只讀檔,不執行任何受審檔案。"""
    n_total = n_md = n_prose = n_code = 0
    dir_scripts = False
    prod_chunks = []
    for dp, dirs, fs in os.walk(path, followlinks=followlinks):
        dirs[:] = [d for d in dirs if d not in L.SKIP_DIRS]
        rel = os.path.relpath(dp, path).replace(os.sep, "/")
        if re.search(r"(^|/)scripts(/|$)", "" if rel == "." else rel):
            dir_scripts = True
        for f in fs:
            n_total += 1
            ext = os.path.splitext(f)[1].lower()
            if ext in (".md", ".markdown"):
                n_md += 1
            if ext in L.PROSE_EXT or (ext == "" and f.upper() in L.PROSE_NAMES):
                n_prose += 1
            if ext in L.CODE_EXT:
                n_code += 1
            # 生產偵測面:與 lint_skill.analyze 的 all_text 同一組副檔名
            if f.lower().endswith((".md", ".yml", ".yaml", ".sh")):
                prod_chunks.append(L.read_text(os.path.join(dp, f)))
    if n_total == 0:
        return None
    n = max(n_total, 1)
    return {
        "files": n_total,
        "pct_md": round(100 * n_md / n, 1),
        "pct_prose": round(100 * n_prose / n, 1),
        "code": n_code,
        "dir_scripts": dir_scripts,
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

    ko_diff, ko_diff_nothresh, s101_new = [], [], []
    for t in targets:
        args = (t["pct_prose"], t["pct_md"], t["code"], t["dir_scripts"])
        cur, leg, noth = ko_current(*args), ko_legacy(*args), ko_no_threshold(*args)
        if cur != leg:
            ko_diff.append({**{k: t[k] for k in ("root", "name", "pct_md", "pct_prose", "code")},
                            "legacy": leg, "current": cur})
        if noth != leg:
            ko_diff_nothresh.append({"root": t["root"], "name": t["name"],
                                     "pct_prose": t["pct_prose"], "legacy": leg, "no_threshold": noth})
        # S-101:量**生產面**(F-5),不是只量 SKILL.md
        if L.DEFENSE_UNTRUSTED.search(t["prod_text"]):
            s101_new.append({"root": t["root"], "name": t["name"]})

    return {
        "corpus_roots": [{"label": l, "path": p, "followlinks": f} for l, p, f in CORPUS_ROOTS],
        "skipped_roots": skipped,
        "n_targets": len(targets),
        "n_by_root": {l: sum(1 for t in targets if t["root"] == l) for l, _, _ in CORPUS_ROOTS},
        "knowledge_only_changed": ko_diff,
        "no_threshold_variant_changed": ko_diff_nothresh,
        "s101_hits_production_surface": s101_new,
    }


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
    print("[selftest] measure_rubric_impact: all assertions passed ✔")


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
        print(f"    {d['root']}:{d['name']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
