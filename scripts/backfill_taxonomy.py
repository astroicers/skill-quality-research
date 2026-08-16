#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
G1 裁決 2 — taxonomy 兩段式回填的 stage-1(deterministic)。

規則(BRIEF §6 + G2 Q1):
  - skill_md_compliant_count ≥ 1 且 skill_md_count == 1 → B(單一 skill)
  - skill_md_compliant_count ≥ 1 且 skill_md_count ≥ 2 → 保留 TBD,列入 cd_pending(C/D 細分交 stage-2 LLM/人工)
  - skill_md_compliant_count == 0                      → 列入 exclusion_candidates(stage-2 覆核 v1.2.1 CLAUDE.md-only 例外)
  - 不在 feature_matrix(clone 被跳過)                  → 列入 manual(無靜態證據,人工判)

只有 B 會直接寫回 repos.json(加 taxonomy_note);其餘輸出清單供 stage-2。
"""
import json, sys

def main():
    with open("research/repos.json", encoding="utf-8") as f:
        data = json.load(f)
    with open("research/feature_matrix.json", encoding="utf-8") as f:
        matrix = {r["full_name"]: r for r in json.load(f)["rows"]}

    applied_b, cd_pending, exclusion_candidates, manual = [], [], [], []
    for rec in data["records"]:
        if not rec.get("in_rubric_sample") or rec.get("taxonomy") != "TBD":
            continue
        m = matrix.get(rec["full_name"])
        if m is None:
            manual.append(rec["full_name"]); continue
        compliant, total = m["skill_md_compliant_count"], m["skill_md_count"]
        if compliant >= 1 and total == 1:
            rec["taxonomy"] = "B"
            rec["taxonomy_note"] = "backfill-stage1: 1 compliant SKILL.md"
            applied_b.append(rec["full_name"])
        elif compliant >= 1:
            cd_pending.append((rec["full_name"], total, compliant))
        else:
            exclusion_candidates.append((rec["full_name"], total, m["claude_md_count"]))

    with open("research/repos.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[stage-1] B 定案 {len(applied_b)} 筆:")
    for n in applied_b: print("   B:", n)
    print(f"[stage-2 待辦] C/D 細分 {len(cd_pending)} 筆:")
    for n, t, c in cd_pending: print(f"   CD: {n} (skill_md={t}, compliant={c})")
    print(f"[stage-2 待辦] 排除候補 {len(exclusion_candidates)} 筆(0 合規 SKILL.md):")
    for n, t, cl in exclusion_candidates: print(f"   EX?: {n} (skill_md={t}, claude_md={cl})")
    print(f"[人工] 無 clone 證據 {len(manual)} 筆:")
    for n in manual: print("   MANUAL:", n)

if __name__ == "__main__":
    sys.exit(main())
