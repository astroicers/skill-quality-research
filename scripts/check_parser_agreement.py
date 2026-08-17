#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""三方 frontmatter parser 一致性守門。

本專案有三條 frontmatter 解析路徑,任兩條分歧都會讓「同一個 repo 得到不同分數」:

  1. `extract_features.parse_frontmatter` 走 PyYAML(`yaml.safe_load`)——**有裝 PyYAML 時**
  2. `extract_features.parse_frontmatter` 的 naive fallback ——**沒裝 PyYAML 時**
  3. `lint_skill.parse_fm` ——出貨用的 skill-reviewer,刻意**不依賴 PyYAML**(必須可獨立跑)

為什麼這件事非守不可:PyYAML 是 try/except 的選用依賴,所以**同一份 SKILL.md 在有/沒有
PyYAML 的機器上會走不同 parser**。研究期間本機裝了 PyYAML 6.0.3,已發布的所有數字都來自路徑 1;
路徑 2 從未在真實語料上驗證過。2026-08-17 首次實測 161 份真實 SKILL.md,發現 3 份分歧
(naive 未解 YAML 雙引號內的 `\\"` 轉義,`desc_len` 差 6 字元),修好後降為 0。
（該分歧對 rubric 規則本身零影響——name/description 非空與 trigger regex 都不受反斜線影響——
 只動到 `desc_len_median` 這個 numeric-profile 觀察值。但 fallback 的 bug 就是 bug。）

因為 skill-reviewer 必須可獨立出貨,`_unquote_scalar` 在兩處各有一份複本;
複本一定會漂移,**除非有測試盯著**——這支腳本就是那個測試。

用法:
  python3 scripts/check_parser_agreement.py                     # 掃預設語料
  python3 scripts/check_parser_agreement.py --corpus some/dir   # 指定語料
  python3 scripts/check_parser_agreement.py --require 20        # 語料不足 20 份就失敗
"""
import argparse
import pathlib
import re
import sys

# 預設語料:已提交的 fixtures + 本 repo 自己的 skill + (若存在)未進版控的第三方 clone
DEFAULT_CORPUS = [
    "skill-reviewer",                 # 自己的 SKILL.md 與 evals fixtures(已進版控,CI 拿得到)
    "research/repos",                 # untrusted clone(gitignored;CI 沒有 → 自動略過)
]
COMPARED_KEYS = ("name", "description")


def load_parsers(root):
    """把三條路徑取出來。研究腳本與出貨腳本刻意不互相 import,這裡只在測試中並存。"""
    sys.path.insert(0, str(root / "scripts"))
    sys.path.insert(0, str(root / "skill-reviewer" / "scripts"))
    import extract_features as ef
    import lint_skill as ls

    def via_pyyaml(text):
        if not ef.HAVE_YAML:
            return None                      # 沒裝 PyYAML → 這條路徑不存在,不是失敗
        return ef.parse_frontmatter(text)[0]

    def via_naive(text):
        saved = ef.HAVE_YAML
        ef.HAVE_YAML = False                 # 強制走 fallback,即使本機裝了 PyYAML
        try:
            return ef.parse_frontmatter(text)[0]
        finally:
            ef.HAVE_YAML = saved

    def via_lint(text):
        return ls.parse_fm(text)[0]

    return ef.HAVE_YAML, {"pyyaml": via_pyyaml, "extract-naive": via_naive, "lint_skill": via_lint}


def norm(d, key):
    """比較用的正規化:只收斂空白(換行/縮排在 YAML 多行純量上本就不該有意義)。"""
    if d is None:
        return "<n/a>"
    v = d.get(key)
    return None if v is None else re.sub(r"\s+", " ", str(v)).strip()



def _diff_window(vals, span=34):
    """只印**第一處差異附近**的片段——印前 70 字元通常整段相同,看不出差在哪。"""
    items = list(vals.items())
    ref = items[0][1] or ""
    i = next((k for k in range(max(len(v or "") for _, v in items))
              if len({(v or "")[k:k + 1] for _, v in items}) > 1), None)
    if i is None:                                  # 只差在長度(某條路徑提早截斷)
        return " | ".join(f"{n}=len {len(v or '')}" for n, v in items) + "  (前綴相同,長度不同)"
    lo = max(0, i - span // 2)
    return (f"首處差異在 offset {i}(共長 {len(ref)}):"
            + " | ".join(f"{n}=…{(v or '')[lo:i + span]!r}…" for n, v in items))


def main():
    ap = argparse.ArgumentParser(description="三方 frontmatter parser 一致性檢查")
    ap.add_argument("--root", default=".", help="repo 根目錄")
    ap.add_argument("--corpus", action="append", help="語料目錄(可重複;預設見 DEFAULT_CORPUS)")
    ap.add_argument("--require", type=int, default=3,
                    help="語料下限;低於此值視為檢查未實際執行而失敗(預設 3)")
    args = ap.parse_args()
    root = pathlib.Path(args.root).resolve()

    have_yaml, parsers = load_parsers(root)
    dirs = [root / d for d in (args.corpus or DEFAULT_CORPUS)]
    files, skipped = [], []
    for d in dirs:
        if d.is_dir():
            files += sorted(d.rglob("SKILL.md"))
        else:
            skipped.append(d)
    files = sorted(set(files))

    if len(files) < args.require:
        print(f"❌ 語料只有 {len(files)} 份 SKILL.md(< --require {args.require}),"
              f"檢查沒有實際執行", file=sys.stderr)
        if skipped:
            print(f"   缺席目錄: {[str(p.relative_to(root)) for p in skipped]}", file=sys.stderr)
        return 1

    # 無 PyYAML 的機器上「pyyaml 路徑」不存在,必須從比較集合移除,
    # 否則它的 None 會被 norm() 變成 "<n/a>" 而與另兩條全部報成分歧。
    if not have_yaml:
        parsers.pop("pyyaml")
    names = list(parsers)
    disagreements, errors = [], []
    for f in files:
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError as e:                          # 讀不到就是讀不到,不靜默跳過
            errors.append(f"{f}: 讀取失敗 {e}")
            continue
        parsed = {}
        for name, fn in parsers.items():
            try:
                parsed[name] = fn(text)
            except Exception as e:                    # noqa: BLE001 — 任一 parser 拋出都是缺陷
                errors.append(f"{f}: {name} 拋出 {type(e).__name__}: {e}")
                parsed[name] = None
        if any(v is None for v in parsed.values()):
            continue                                  # 某條路徑拋出,前一步已記錄為錯誤
        for key in COMPARED_KEYS:
            vals = {n: norm(parsed[n], key) for n in names}
            if len(set(vals.values())) > 1:
                rel = f.relative_to(root)
                disagreements.append(f"{rel} [{key}] {_diff_window(vals)}")

    print(f"語料 {len(files)} 份 SKILL.md;比對路徑 {names}"
          f"{'' if have_yaml else '(本機無 PyYAML → 只比兩條 naive 路徑)'}")
    if skipped:
        print(f"略過缺席目錄: {[str(p.relative_to(root)) for p in skipped]}")

    if errors:
        print(f"\n❌ {len(errors)} 個解析錯誤:", *errors[:20], sep="\n  ")
    if disagreements:
        print(f"\n❌ {len(disagreements)} 處分歧(同一份 SKILL.md 在不同 parser 下不同):",
              *disagreements[:20], sep="\n  ")
    if errors or disagreements:
        print("\n→ 三條路徑必須一致,否則「有沒有裝 PyYAML」會改變評分結果。"
              "\n  修法:讓 extract_features 的 naive fallback 與 lint_skill.parse_fm 同步"
              "(兩者各有一份 _unquote_scalar 複本,常是漂移來源)。")
        return 1

    print(f"✅ {len(names)} 條 parser 路徑在 {len(files)} 份真實 SKILL.md 上完全一致"
          f"({len(COMPARED_KEYS)} 個欄位 × {len(files)} 份 × {len(names)} 路徑)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
