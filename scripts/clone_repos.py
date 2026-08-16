#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 2 — 結構抓取 (BRIEF §3 Phase 2, Iron Rule 7)
讀取 research/repos.json,對 rubric 樣本(taxonomy A–D + TBD,G1 裁決 2)執行 git clone --depth 1。
產出 research/clone-manifest.json(commit hash、時間、成敗)。

安全 (Iron Rule 7):
  - clone 內容一律視為 untrusted;本腳本 clone 後立刻「defang」:
    移除工作樹所有檔案的執行位,防止後續任何人/agent 手滑執行。
  - 絕不執行 clone 內任何 script / install.sh / hook。

用法:
  python3 scripts/clone_repos.py                    # 全量(A–D + TBD)
  python3 scripts/clone_repos.py --limit 3          # 冒煙測試
  python3 scripts/clone_repos.py --only owner/name,owner2/name2
"""
import argparse, json, os, subprocess, sys
from datetime import datetime, timezone

SIZE_LIMIT_KB = 500 * 1024  # BRIEF: >500MB 跳過並記錄
CLONE_TIMEOUT = 420

def dir_for(full_name):
    return full_name.replace("/", "__")

def defang(path):
    """移除工作樹(不含 .git/)所有檔案執行位。"""
    n = 0
    for dp, dns, fns in os.walk(path):
        dns[:] = [d for d in dns if d != ".git"]
        for fn in fns:
            p = os.path.join(dp, fn)
            try:
                mode = os.stat(p).st_mode
                if mode & 0o111:
                    os.chmod(p, mode & ~0o111); n += 1
            except OSError:
                pass
    return n

def clone_one(full_name, dest_root, no_defang=False):
    dst = os.path.join(dest_root, dir_for(full_name))
    entry = {"full_name": full_name, "dir": os.path.relpath(dst),
             "cloned_at": datetime.now(timezone.utc).isoformat()}
    if os.path.isdir(os.path.join(dst, ".git")):
        entry.update(ok=True, skipped="already-cloned")
        entry["commit"] = git_head(dst)
        return entry
    url = f"https://github.com/{full_name}.git"
    try:
        r = subprocess.run(
            ["git", "clone", "--depth", "1", "--no-tags", "--quiet",
             "--config", "core.hooksPath=/dev/null", url, dst],
            capture_output=True, text=True, timeout=CLONE_TIMEOUT)
        if r.returncode != 0:
            entry.update(ok=False, error=(r.stderr or "clone failed").strip()[:300])
            return entry
        entry["commit"] = git_head(dst)
        if not no_defang:
            entry["defanged_files"] = defang(dst)
        entry["ok"] = True
    except subprocess.TimeoutExpired:
        entry.update(ok=False, error=f"timeout>{CLONE_TIMEOUT}s")
    except Exception as e:
        entry.update(ok=False, error=str(e)[:300])
    return entry

def git_head(dst):
    try:
        r = subprocess.run(["git", "-C", dst, "rev-parse", "HEAD"],
                           capture_output=True, text=True, timeout=20)
        return r.stdout.strip() or None
    except Exception:
        return None

def main():
    ap = argparse.ArgumentParser(description="Phase 2 shallow clone")
    ap.add_argument("--repos", default="research/repos.json")
    ap.add_argument("--dest", default="research/repos")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--only", default="", help="逗號分隔 full_name 白名單")
    ap.add_argument("--exclude-tbd", action="store_true",
                    help="排除 taxonomy=TBD(G1 裁決 2:預設含 TBD,clone 後兩段式回填 taxonomy)")
    ap.add_argument("--no-defang", action="store_true")
    args = ap.parse_args()

    with open(args.repos, encoding="utf-8") as f:
        data = json.load(f)
    only = {s.strip() for s in args.only.split(",") if s.strip()}
    allowed_taxo = {"A", "B", "C", "D"} | (set() if args.exclude_tbd else {"TBD"})

    targets = []
    for r in data["records"]:
        if only and r["full_name"] not in only: continue
        if not only:
            if not r.get("in_rubric_sample"): continue
            if str(r.get("taxonomy")) not in allowed_taxo:
                continue
        size = r.get("repo_size_kb")
        if size and size > SIZE_LIMIT_KB:
            print(f"[skip>{SIZE_LIMIT_KB}KB] {r['full_name']} ({size} KB)")
            continue
        targets.append(r["full_name"])
    if args.limit: targets = targets[:args.limit]

    os.makedirs(args.dest, exist_ok=True)
    manifest = {"generated_at": datetime.now(timezone.utc).isoformat(),
                "note": "Iron Rule 7: clones are UNTRUSTED. Static analysis only. exec bits removed.",
                "entries": []}
    ok = 0
    for i, fn in enumerate(targets, 1):
        print(f"[{i}/{len(targets)}] cloning {fn} ...")
        e = clone_one(fn, args.dest, no_defang=args.no_defang)
        manifest["entries"].append(e)
        ok += 1 if e.get("ok") else 0
        print(f"   -> {'ok' if e.get('ok') else 'FAIL'} {e.get('commit','')[:10]} {e.get('error','')}")

    out = os.path.join(os.path.dirname(args.dest.rstrip('/')) or "research", "clone-manifest.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"[ok] {ok}/{len(targets)} cloned; manifest -> {out}")
    if ok < len(targets):
        sys.exit(2)

if __name__ == "__main__":
    main()
