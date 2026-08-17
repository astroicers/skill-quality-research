#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""驗證「零依賴」聲明:所有 import 必須在明列的 stdlib allowlist 內。

為什麼用 allowlist 而不是 `sys.stdlib_module_names`:
後者是 **Python 3.10+** 才有的 API,而本檢查要在 3.9 上跑(見 .github/workflows/validate.yml
的 python matrix)。allowlist 同時比 stdlib 檢查更嚴——它把依賴面**釘住**,
新增任何 import(即使是 stdlib)都必須有人明確加進來,不會悄悄擴大。

若手上的 Python 有 `sys.stdlib_module_names`,額外交叉檢查 allowlist 自己沒寫錯
(避免有人把第三方套件名加進 allowlist 就放行)。

用法: python3 scripts/check_stdlib_only.py
"""
import argparse
import ast
import pathlib
import sys

# 本專案允許的 import(全部 stdlib)。新增前請確認:真的必要嗎?
ALLOWED = {
    "argparse", "ast", "collections", "csv", "datetime", "hashlib", "io", "json",
    "math", "os", "pathlib", "random", "re", "statistics", "subprocess",
    "sys", "tempfile", "time", "urllib",
}

# 選用第三方依賴:允許 import,但**必須**被 try/except 包住且有 fallback,
# 否則「零依賴」聲明失效。PyYAML 是唯一一個(extract_features 的 frontmatter 快路徑);
# 兩條路徑的一致性由 scripts/check_parser_agreement.py 守。
OPTIONAL_GUARDED = {"yaml"}

TARGET_GLOBS = ("scripts/*.py", "skill-reviewer/scripts/*.py", "skill-reviewer/evals/*.py")


def imported_modules(path):
    """回傳 [(lineno, module, guarded)];相對 import(level>0)不算外部依賴。

    guarded = 該 import 是否位於 try 區塊內(選用依賴的判準)。
    """
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    guarded_lines = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Try):
            for sub in node.body:
                for inner in ast.walk(sub):
                    if isinstance(inner, (ast.Import, ast.ImportFrom)):
                        guarded_lines.add(inner.lineno)
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            out += [(node.lineno, a.name.split(".")[0]) for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.level == 0:
            out.append((node.lineno, (node.module or "").split(".")[0]))
    return [(ln, m, ln in guarded_lines) for ln, m in out if m]


def main():
    ap = argparse.ArgumentParser(description="驗證零依賴聲明(allowlist 制)")
    ap.add_argument("--root", default=".", help="repo 根目錄")
    args = ap.parse_args()
    root = pathlib.Path(args.root)

    files = sorted(p for g in TARGET_GLOBS for p in root.glob(g))
    if not files:
        print(f"❌ 在 {root} 底下找不到任何目標檔案,檢查沒有實際執行", file=sys.stderr)
        return 1

    # first-party:本 repo 自己的模組(檔名即模組名)。check_parser_agreement.py 會 import
    # extract_features / lint_skill 來做三方比對,那不是外部依賴。
    first_party = {f.stem for f in files}

    violations = []
    used, optional_used, fp_used = set(), set(), set()
    for f in files:
        for lineno, mod, guarded in imported_modules(f):
            if mod in first_party:
                fp_used.add(mod)
                continue
            if mod in OPTIONAL_GUARDED:
                optional_used.add(mod)
                if not guarded:                       # 沒被 try 包住 → 變成硬依賴
                    violations.append(
                        f"{f}:{lineno} import {mod} 未被 try/except 包住 —— 選用依賴變硬依賴")
                continue
            used.add(mod)
            if mod not in ALLOWED:
                violations.append(f"{f}:{lineno} import {mod}")

    # 交叉檢查:allowlist 本身不得混入非 stdlib(僅 3.10+ 可查)
    stdlib = getattr(sys, "stdlib_module_names", None)
    if stdlib:
        fake = sorted(m for m in ALLOWED if m not in stdlib)
        if fake:
            violations.append(f"allowlist 混入非 stdlib 模組: {fake}")
    if root.joinpath("requirements.txt").exists():
        violations.append("出現 requirements.txt —— 零依賴聲明失效")

    if violations:
        print("❌ 零依賴檢查失敗:", *violations, sep="\n  ")
        return 1

    unused = sorted(ALLOWED - used)
    print(f"✅ 零依賴檢查通過:{len(files)} 檔、{len(used)} 個 import 全在 allowlist 內"
          f"{'(stdlib 交叉檢查亦通過)' if stdlib else '(此版本無 stdlib_module_names,略過交叉檢查)'}")
    if optional_used:
        print(f"   選用依賴(皆已 try/except 包住,有 fallback):{sorted(optional_used)}"
              f" —— 路徑一致性見 scripts/check_parser_agreement.py")
    if fp_used:
        print(f"   first-party 互相 import:{sorted(fp_used)}")
    if unused:
        print(f"   註:allowlist 有 {len(unused)} 個未被用到,可考慮收斂 → {unused}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
