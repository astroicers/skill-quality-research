#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
G2 Q2/Q5 — 對 rubric 樣本回填 open_issues 與 owner_is_org(單次 gh api repos/{name})。

- 不重跑 search,零樣本擾動(G1 已核准的樣本不動)
- 可重入:已有兩欄位的 record 直接跳過
- 近似值註記:GitHub API 的 open_issues_count 為 issues+PRs 合計(README 近似值 #8)

用法:
  python3 scripts/backfill_repo_fields.py            # 全量(僅 in_rubric_sample)
  python3 scripts/backfill_repo_fields.py --limit 3  # 冒煙
"""
import argparse, json, subprocess, sys, time

INTERVAL = 0.8  # REST core 配額寬裕,禮貌間隔即可


def fetch(full_name):
    r = subprocess.run(
        ["gh", "api", f"repos/{full_name}", "--jq",
         '{open_issues: .open_issues_count, owner_type: .owner.type}'],
        capture_output=True, text=True, timeout=30)
    if r.returncode != 0:
        return None, (r.stderr or "").strip().splitlines()[:1]
    return json.loads(r.stdout), None


def main():
    ap = argparse.ArgumentParser(description="G2 Q2/Q5 backfill")
    ap.add_argument("--repos", default="research/repos.json")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    with open(args.repos, encoding="utf-8") as f:
        data = json.load(f)

    targets = [r for r in data["records"] if r.get("in_rubric_sample")
               and (r.get("open_issues") is None or r.get("owner_is_org") is None)]
    if args.limit:
        targets = targets[:args.limit]
    print(f"[backfill] 待補 {len(targets)} 筆")

    ok = failed = 0
    for i, rec in enumerate(targets, 1):
        info, err = fetch(rec["full_name"])
        if info is None:
            print(f"  [{i}/{len(targets)}] {rec['full_name']} FAILED {err}")
            failed += 1
        else:
            rec["open_issues"] = info["open_issues"]
            rec["owner_is_org"] = info["owner_type"] == "Organization"
            ok += 1
            if i % 20 == 0 or i == len(targets):
                print(f"  [{i}/{len(targets)}] ...{rec['full_name']}")
        time.sleep(INTERVAL)

    with open(args.repos, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[ok] 回填完成 ok={ok} failed={failed} → {args.repos}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
