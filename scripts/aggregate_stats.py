#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 4 — tier 梯度分析與 rubric 草稿 (BRIEF §3 Phase 4, §6.5, §8)
讀取: research/feature_matrix.json
輸出: research/gradient_analysis.json
      research/rubric-draft.yaml        (script 可判定規則;LLM 維度由 Phase 3b/人工補)
      research/patterns-report-draft.md (量化表格已填;質化章節留 TODO 給 LLM/人工)

實作 BRIEF 的機制:
  - 特徵三分類: hygiene / differentiator / noise(門檻常數皆為 G3 審查對象,見 THRESHOLDS)
  - 去混淆三道工序: (1) F0 純度樣本復現 (2) 雙結果變數 engagement (3) 機制陳述
    → 機制陳述由 MECHANISM 表提供草稿;缺機制的特徵自動降為觀察記錄
  - 分層穩健性: B/D 類、F0 層、各 cohort 內複算方向
  - 統計誠實: 不跑迴歸;Spearman 手刻;每張表印 n;n<3 的層不參與判定

用法:
  python3 scripts/aggregate_stats.py
  python3 scripts/aggregate_stats.py --selftest   # 合成 40 repo 固定夾具,驗證分類器正確性
"""
import argparse, json, math, os, random, statistics, sys
from datetime import datetime, timezone

TIERS = ["T0", "T1", "T2", "T3"]

# ---- G3 審查對象:所有判定常數 ----
THRESHOLDS = {
    "hygiene_min_prevalence": 70.0,   # 各層皆 ≥70%
    "hygiene_max_range": 20.0,        # 且平坦(層間差 ≤20pp)
    "diff_min_gap": 30.0,             # T_top − T_bottom ≥ 30pp
    "min_tier_n": 3,                  # 層內 n<3 不參與判定
    "marketing_engagement_rho_max": 0.10,  # 星梯度成立但 engagement rho 低 → marketing-suspect
}

# 進入梯度分析的布林特徵(§7 schema 對應)
BOOL_FEATURES = [
    "skill_spec_compliant", "fm_license_any", "fm_allowed_tools_any", "fm_metadata_any",
    "desc_has_trigger_majority",
    "dir_scripts", "dir_references", "dir_assets", "dir_examples", "dir_evals",
    "has_plugin_json", "has_marketplace_json", "has_install_sh", "install_oneliner_in_readme",
    "has_ci", "ci_validates_skills", "has_tests_or_evals", "has_changelog", "has_version_tags",
    "readme_has_before_after", "readme_has_metrics", "readme_has_demo_media",
]
NUM_FEATURES = ["skill_md_count", "skill_md_max_lines", "desc_len_median",
                "multi_harness_count", "readme_lines", "pct_markdown_files"]

# signal_type 對應 (BRIEF §8);security 維度一律 hygiene(§8 例外),此處先標 signal 供 rubric 用
SIGNAL_TYPE = {
    "skill_spec_compliant": "craft", "fm_license_any": "craft", "fm_allowed_tools_any": "craft",
    "fm_metadata_any": "craft", "desc_has_trigger_majority": "craft",
    "dir_scripts": "craft", "dir_references": "craft", "dir_assets": "craft",
    "dir_examples": "craft", "dir_evals": "craft",
    "has_ci": "craft", "ci_validates_skills": "craft", "has_tests_or_evals": "craft",
    "has_changelog": "craft", "has_version_tags": "craft",
    "has_plugin_json": "packaging", "has_marketplace_json": "packaging",
    "has_install_sh": "packaging", "install_oneliner_in_readme": "packaging",
    "multi_harness_count": "packaging",
    "readme_has_before_after": "marketing", "readme_has_metrics": "marketing",
    "readme_has_demo_media": "marketing", "readme_lines": "marketing",
}
DIMENSION = {
    "skill_spec_compliant": "spec_compliance", "fm_license_any": "spec_compliance",
    "fm_allowed_tools_any": "spec_compliance", "fm_metadata_any": "spec_compliance",
    "desc_has_trigger_majority": "trigger_design",
    "dir_scripts": "deterministic_offloading", "dir_references": "progressive_disclosure",
    "dir_assets": "progressive_disclosure", "dir_examples": "docs_installability",
    "dir_evals": "tests_evals",
    "has_plugin_json": "docs_installability", "has_marketplace_json": "docs_installability",
    "has_install_sh": "docs_installability", "install_oneliner_in_readme": "docs_installability",
    "has_ci": "tests_evals", "ci_validates_skills": "tests_evals",
    "has_tests_or_evals": "tests_evals", "has_changelog": "docs_installability",
    "has_version_tags": "docs_installability",
    "readme_has_before_after": "docs_installability", "readme_has_metrics": "docs_installability",
    "readme_has_demo_media": "docs_installability",
}
# 機制陳述草稿(工序 3;缺席者自動降級為觀察)
MECHANISM = {
    "skill_spec_compliant": "走官方 SKILL.md 規格 → harness 能被動載入 metadata,觸發與相容性可預期",
    "desc_has_trigger_majority": "description 是唯一常駐 context 的觸發機制,含觸發語境直接提高命中率",
    "dir_scripts": "重複/可驗證操作下放 deterministic script,降低 LLM 誤差與 token 成本",
    "dir_references": "progressive disclosure:細節按需載入,SKILL.md 保持精簡可讀",
    "dir_evals": "有 evals 才能迭代驗證 skill 行為,品質可回歸測試",
    "has_tests_or_evals": "同上:可驗證性使改動不退化",
    "has_ci": "CI 讓貢獻與變更有守門,協作品質穩定",
    "ci_validates_skills": "CI 直接驗 skill 結構/frontmatter,壞 skill 進不了 main",
    "has_plugin_json": "plugin 打包使 skill 可被 marketplace 發現與一鍵安裝",
    "has_marketplace_json": "marketplace 清單降低多 skill 安裝摩擦",
    "has_install_sh": "一鍵安裝腳本降低採用門檻",
    "install_oneliner_in_readme": "README 首屏一行安裝,採用摩擦最小化",
    "multi_harness_count": "跨 harness 相容擴大可用人群(Claude Code/Codex/Cursor...)",
    "readme_has_before_after": "before/after 對比讓價值 3 秒內可感知(採用面)",
    "readme_has_metrics": "量化主張(省 65% token)給出可傳播的價值錨點(採用面)",
    "readme_has_demo_media": "demo 媒體降低理解成本(採用面)",
    "fm_license_any": "授權明確才可被企業/marketplace 合法採用",
    "has_version_tags": "版本標記使安裝可鎖定、變更可追溯",
    "has_changelog": "變更紀錄降低升級風險",
    "fm_allowed_tools_any": "宣告工具面縮小攻擊面與意外行為(安全/可預期性)",
    "fm_metadata_any": "額外 metadata 支援目錄/registry 生態整合",
    "dir_assets": "輸出用資產(模板/字型)內建,產出即專業",
    "dir_examples": "範例降低首次使用的理解成本",
}


# ---------------- 統計工具(零依賴) ----------------
def spearman(xs, ys):
    pairs = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None]
    n = len(pairs)
    if n < 4: return None
    def ranks(vs):
        order = sorted(range(len(vs)), key=lambda i: vs[i])
        r = [0.0] * len(vs); i = 0
        while i < len(vs):
            j = i
            while j + 1 < len(vs) and vs[order[j + 1]] == vs[order[i]]: j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1): r[order[k]] = avg
            i = j + 1
        return r
    rx, ry = ranks([p[0] for p in pairs]), ranks([p[1] for p in pairs])
    mx, my = sum(rx) / n, sum(ry) / n
    cov = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    vx = math.sqrt(sum((a - mx) ** 2 for a in rx)); vy = math.sqrt(sum((b - my) ** 2 for b in ry))
    return round(cov / (vx * vy), 3) if vx and vy else None

def feat_value(row, feat):
    v = row.get(feat)
    if v is None: return None
    if isinstance(v, bool): return 1.0 if v else 0.0
    try: return float(v)
    except (TypeError, ValueError): return None

def prevalence_by_tier(rows, feat):
    out = {}
    for t in TIERS:
        vals = [feat_value(r, feat) for r in rows if r.get("star_tier") == t]
        vals = [v for v in vals if v is not None]
        out[t] = {"n": len(vals),
                  "prevalence": round(100 * sum(1 for v in vals if v >= 0.5) / len(vals), 1) if vals else None,
                  "median": round(sorted(vals)[len(vals) // 2], 1) if vals else None}
    return out

def classify(prev, min_n):
    """回傳 (feature_class, gap, usable_tiers)。BRIEF Phase 4 三分類。"""
    usable = [t for t in TIERS if prev[t]["n"] >= min_n and prev[t]["prevalence"] is not None]
    if len(usable) < 3:
        return "insufficient-tiers", None, usable
    ps = [prev[t]["prevalence"] for t in usable]
    gap = ps[-1] - ps[0]
    monotonic = all(ps[i + 1] >= ps[i] - 5 for i in range(len(ps) - 1))  # 容忍 5pp 抽樣噪音
    strictly_up = ps[-1] > ps[0]
    if min(ps) >= THRESHOLDS["hygiene_min_prevalence"] and (max(ps) - min(ps)) <= THRESHOLDS["hygiene_max_range"]:
        return "hygiene", round(gap, 1), usable
    if monotonic and strictly_up and gap >= THRESHOLDS["diff_min_gap"]:
        return "differentiator", round(gap, 1), usable
    return "noise", round(gap, 1), usable

def gap_to_weight(gap, evidence="strong", signal_type="craft"):
    """G3-Q2 定稿公式:base = 1 + round(4*min(gap,60)/60),再乘 evidence 係數,
    packaging signal 設上限 3(packaging 是可安裝性、非工藝,不得與 craft 同權)。clamp 1..5。"""
    if gap is None: return None
    base = 1 + round(4 * min(gap, 60.0) / 60.0)
    ev_factor = {"strong": 1.0, "moderate": 0.6, "weak": 0.3}.get(evidence, 1.0)
    w = max(1, round(base * ev_factor))
    if signal_type == "packaging":
        w = min(w, 3)
    return max(1, min(5, w))

def direction_in_subset(rows, feat, min_n=2):
    """子樣本內 top-bottom 可用層方向;+1/-1/0/None。穩健性與純度復現用。"""
    prev = prevalence_by_tier(rows, feat)
    usable = [t for t in TIERS if prev[t]["n"] >= min_n and prev[t]["prevalence"] is not None]
    if len(usable) < 2: return None, prev
    d = prev[usable[-1]]["prevalence"] - prev[usable[0]]["prevalence"]
    return (1 if d > 5 else -1 if d < -5 else 0), prev


# ---------------- 主分析 ----------------
def analyze(rows):
    rows = [r for r in rows if r.get("in_rubric_sample") and r.get("star_tier") in TIERS]
    n = len(rows)
    log_stars = [math.log10(max(r.get("stars") or 1, 1)) for r in rows]
    fsr = [r.get("fork_star_ratio") for r in rows]
    contrib = [r.get("contributor_count") for r in rows]
    subsets = {
        "class_BD": [r for r in rows if str(r.get("taxonomy")) in ("B", "D")],
        "fame_F0": [r for r in rows if r.get("author_fame_tier") == "F0"],
    }
    for c in ("C1", "C2", "C3"):
        subsets[f"cohort_{c}"] = [r for r in rows if r.get("launch_cohort") == c]

    results = []
    for feat in BOOL_FEATURES + NUM_FEATURES:
        vals = [feat_value(r, feat) for r in rows]
        prev = prevalence_by_tier(rows, feat)
        fclass, gap, usable = classify(prev, THRESHOLDS["min_tier_n"])
        if feat in NUM_FEATURES:
            # G3 前修正:數值特徵的 prevalence(>=0.5 即真)恆為 ~100%,套 prevalence 三分類會
            # 誤產 hygiene 規則;改標 numeric-profile,只報 tier_median 剖面,不進 rubric rules
            fclass = "numeric-profile"
        rho_stars = spearman(vals, log_stars)
        rho_fsr = spearman(vals, fsr)
        rho_contrib = spearman(vals, contrib)

        # 工序 1: 純度樣本復現(F0 內同向)
        g_dir, _ = direction_in_subset(subsets["fame_F0"], feat)
        grassroots = (g_dir == 1)
        # 工序 2: 雙結果變數(G3-Q5 收緊:median 而非 max,且 fork_star_ratio 必須不顯著為負)
        eng_rhos = [x for x in (rho_fsr, rho_contrib) if x is not None]
        med_eng = statistics.median(eng_rhos) if eng_rhos else None
        fsr_negative = (rho_fsr is not None and rho_fsr < -THRESHOLDS["marketing_engagement_rho_max"])
        marketing_suspect = (fclass == "differentiator" and med_eng is not None
                             and (med_eng < THRESHOLDS["marketing_engagement_rho_max"] or fsr_negative))
        # 工序 3: 機制陳述
        mechanism = MECHANISM.get(feat)
        # 分層穩健性
        robust = {}
        for name, sub in subsets.items():
            d, _ = direction_in_subset(sub, feat)
            robust[name] = {"n": len(sub), "direction": d}
        robust_dirs = [v["direction"] for v in robust.values() if v["direction"] is not None]
        robust_pass = bool(robust_dirs) and all(d >= 0 for d in robust_dirs) and any(d == 1 for d in robust_dirs)

        if fclass == "differentiator":
            checks = [grassroots, not marketing_suspect, robust_pass, mechanism is not None]
            strength = "strong" if all(checks) else ("moderate" if sum(checks) >= 3 else "weak")
            if not grassroots: strength = "weak"                     # BRIEF 工序 1: 未復現上限 weak
            if mechanism is None: fclass, strength = "observation-only", "n/a"  # 工序 3
            # G3-Q1: weak 且同時未過 grassroots 復現與 robustness → 證據不足,降為觀察記錄
            elif strength == "weak" and not grassroots and not robust_pass:
                fclass = "observation-only"
        elif fclass == "hygiene":
            strength = "strong" if all(prev[t]["n"] >= THRESHOLDS["min_tier_n"] for t in usable) else "moderate"
        else:
            strength = "n/a"

        results.append({
            "feature": feat, "signal_type": SIGNAL_TYPE.get(feat, "craft"),
            "dimension": DIMENSION.get(feat, "misc"),
            "feature_class": fclass, "gap_pp": gap,
            "tier_prevalence": {t: prev[t]["prevalence"] for t in TIERS},
            "tier_median": {t: prev[t]["median"] for t in TIERS},
            "tier_n": {t: prev[t]["n"] for t in TIERS},
            "spearman_log_stars": rho_stars,
            "spearman_fork_star_ratio": rho_fsr, "spearman_contributors": rho_contrib,
            "grassroots_replicated": grassroots, "marketing_suspect": marketing_suspect,
            "robustness": robust, "robustness_pass": robust_pass,
            "mechanism": mechanism, "evidence_strength": strength,
            "weight_proposal": gap_to_weight(gap, strength, SIGNAL_TYPE.get(feat, "craft")) if fclass == "differentiator" else None,
            # 樣本經 taxonomy 回填以「合規 SKILL.md」篩選,此特徵 100% 為選樣循環,非市場證據
            "selection_artifact": feat == "skill_spec_compliant",
        })
    return {"n": n, "thresholds": THRESHOLDS, "results": results,
            "subset_sizes": {k: len(v) for k, v in subsets.items()}}


# ---------------- 輸出 ----------------
def emit_rubric_yaml(analysis, path):
    lines = ["# rubric-draft.yaml — Phase 4 自動草稿(僅 script 可判定規則;LLM 維度見 BRIEF §8 之 2/7/8)",
             "# 所有 weight/門檻由梯度分析推導,公式與常數為 G3 審查對象",
             f"# generated_at: {datetime.now(timezone.utc).isoformat()}",
             f"# n: {analysis['n']}  thresholds: {json.dumps(analysis['thresholds'])}", "rules:"]
    i = 0
    for r in sorted(analysis["results"], key=lambda x: (x["feature_class"] != "hygiene",
                                                        -(x["gap_pp"] or 0))):
        if r["feature_class"] not in ("hygiene", "differentiator"): continue
        i += 1
        tp = r["tier_prevalence"]
        lines += [
            f"  - id: R-{i:03d}",
            f"    feature: {r['feature']}",
            f"    dimension: {r['dimension']}",
            f"    check_type: script",
            f"    feature_class: {r['feature_class']}",
            f"    signal_type: {r['signal_type']}",
            f"    grassroots_replicated: {str(r['grassroots_replicated']).lower()}",
            f"    marketing_suspect: {str(r['marketing_suspect']).lower()}",
            f"    tier_prevalence: {{T0: {tp['T0']}, T1: {tp['T1']}, T2: {tp['T2']}, T3: {tp['T3']}}}",
            f"    weight: {r['weight_proposal'] if r['weight_proposal'] is not None else 'null  # hygiene: 門檻不計分,不過即 fail'}",
            f"    evidence_strength: {r['evidence_strength']}",
            f"    mechanism: \"{(r['mechanism'] or '').replace(chr(34), chr(39))}\"",
        ]
        if r.get("selection_artifact"):
            lines.append("    selection_artifact: true  # 樣本以合規 SKILL.md 篩選;100% prevalence 為循環,規則本身仍成立但不可當市場證據")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

def emit_report(analysis, path):
    res = analysis["results"]
    def table(items, cols):
        head = "| feature | class | " + " | ".join(cols) + " |"
        sep = "|" + "---|" * (len(cols) + 2)
        body = []
        for r in items:
            tp = r["tier_prevalence"]
            row = [r["feature"], r["feature_class"],
                   *(str(tp[t]) for t in TIERS),
                   str(r["gap_pp"]), str(r["spearman_log_stars"]),
                   "✔" if r["grassroots_replicated"] else "✘",
                   "⚠" if r["marketing_suspect"] else "",
                   r["evidence_strength"]]
            body.append("| " + " | ".join(row) + " |")
        return "\n".join([head, sep] + body)
    cols = ["T0%", "T1%", "T2%", "T3%", "gap", "ρ(log★)", "F0復現", "mkt?", "強度"]
    hyg = [r for r in res if r["feature_class"] == "hygiene"]
    dif = sorted([r for r in res if r["feature_class"] == "differentiator"], key=lambda x: -(x["gap_pp"] or 0))
    noi = [r for r in res if r["feature_class"] in ("noise", "observation-only")]
    ins = [r for r in res if r["feature_class"] == "insufficient-tiers"]
    md = f"""# Patterns Report — DRAFT(Phase 4 自動生成,量化部分)

- generated_at: {datetime.now(timezone.utc).isoformat()}
- n = {analysis['n']}(rubric 樣本,tier 有效)
- 子樣本規模: {json.dumps(analysis['subset_sizes'], ensure_ascii=False)}
- **統計誠實聲明**: n 過小,不做迴歸、不宣稱顯著性;下表為 prevalence 梯度 + Spearman 描述值 (BRIEF Phase 4)。

## 1. Hygiene 門檻特徵(各層皆備)
{table(hyg, cols) if hyg else '_(本批資料不足或無)_'}

## 2. Tier 梯度特徵(differentiator,依 gap 排序)
{table(dif, cols) if dif else '_(本批資料不足或無)_'}

## 3. 反模式與 T0 特有現象
_TODO(Phase 3b 質化 + 人工):由 qualitative_notes 與 T0 層觀察填寫_

## 4. 官方規範 vs 社群實務落差
_TODO(LLM/人工):對照 anthropics/skills 與 skill-creator 撰寫_

## 5. 混淆因子分析
- fame / cohort / domain 分層方向見 gradient_analysis.json 的 robustness 欄位
- marketing-suspect 特徵(追星不追 engagement): {[r['feature'] for r in res if r['marketing_suspect']] or '無'}
- 純度樣本(F0)未復現的 differentiator: {[r['feature'] for r in dif if not r['grassroots_replicated']] or '無'}

## 6. Rubric 權重與 tier 門檻推導依據
- 權重公式(提案): weight = 1 + round(4 × min(gap,60)/60),clamp 1..5 → **G3 審查對象**
- 判定常數: {json.dumps(analysis['thresholds'])}

## 附錄 A. Noise / 觀察記錄
{table(noi, cols) if noi else '無'}

## 附錄 B. 層數不足未判定
{table(ins, cols) if ins else '無'}
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)


# ---------------- selftest: 合成夾具驗證分類器 ----------------
def selftest():
    """確定性夾具(無隨機):每層 12 repo,特徵按精確計數植入,斷言分類器行為可重現。"""
    rows = []
    stars_base = {"T0": 100, "T1": 3000, "T2": 30000, "T3": 150000}
    contrib_base = {"T0": 3, "T1": 10, "T2": 25, "T3": 60}   # engagement 隨 tier 增長(真實結構)
    g_count = {"T0": 2, "T1": 5, "T2": 8, "T3": 12}          # differentiator: 16.7→100%, gap 83pp
    m_count = {"T0": 1, "T1": 2, "T2": 4, "T3": 6}           # marketing: 8.3→50%, gap 42pp
    N = 12
    for tier in TIERS:
        for i in range(N):
            g = i < g_count[tier]                 # 前段植入 craft 特徵
            m = i >= N - m_count[tier]            # 尾段植入 marketing 特徵(高層與 g 部分重疊)
            cb = contrib_base[tier]
            # 語意(=BRIEF 工序 2 的世界觀): craft 帶動 engagement;marketing repo 星照漲、engagement 塌陷
            contrib = 2 if m else cb * (2 if g else 1) + (i % 3)
            fsr = 0.001 if m else round(0.03 + (0.02 if g else 0.0) + 0.001 * (i % 5), 4)
            rows.append({
                "full_name": f"x/{tier}-{i}", "in_rubric_sample": True, "star_tier": tier,
                "stars": stars_base[tier] + i * 7,
                "taxonomy": ["B", "C", "D"][i % 3],
                "author_fame_tier": ["F0", "F0", "F1", "F2"][i % 4],   # F0 = 每層一半
                "launch_cohort": ["C1", "C2", "C3"][i % 3],
                "fork_star_ratio": fsr,
                "contributor_count": contrib,
                "dir_evals": g,                                # 植入 differentiator(craft)
                "skill_spec_compliant": i != N - 1,            # 植入 hygiene(各層 91.7%,平坦)
                "readme_has_metrics": m,                       # 植入 marketing-suspect
                "desc_has_trigger_majority": i % 2 == 0,       # 植入 noise(各層 50%,平坦)
            })
    analysis = analyze(rows)
    by = {r["feature"]: r for r in analysis["results"]}
    assert by["dir_evals"]["feature_class"] == "differentiator", by["dir_evals"]
    assert by["dir_evals"]["weight_proposal"] == 5, by["dir_evals"]["weight_proposal"]
    assert by["dir_evals"]["marketing_suspect"] is False, by["dir_evals"]
    assert by["dir_evals"]["grassroots_replicated"] is True
    assert by["dir_evals"]["evidence_strength"] == "strong", by["dir_evals"]["evidence_strength"]
    assert by["skill_spec_compliant"]["feature_class"] == "hygiene", by["skill_spec_compliant"]
    assert by["desc_has_trigger_majority"]["feature_class"] == "noise", by["desc_has_trigger_majority"]
    assert by["readme_has_metrics"]["feature_class"] == "differentiator", by["readme_has_metrics"]
    assert by["readme_has_metrics"]["marketing_suspect"] is True, by["readme_has_metrics"]
    print("[selftest] aggregate_stats: 分類器在確定性夾具上全部判對 ✔")
    print(f"  dir_evals            → differentiator gap={by['dir_evals']['gap_pp']}pp "
          f"weight={by['dir_evals']['weight_proposal']} strength={by['dir_evals']['evidence_strength']} "
          f"ρ(contrib)={by['dir_evals']['spearman_contributors']}")
    print(f"  readme_has_metrics   → differentiator 但 marketing_suspect=True "
          f"ρ(contrib)={by['readme_has_metrics']['spearman_contributors']}(星梯度成立、engagement 塌陷 → 隔離)")
    print(f"  skill_spec_compliant → hygiene;desc_has_trigger_majority → noise")


def main():
    ap = argparse.ArgumentParser(description="Phase 4 梯度分析")
    ap.add_argument("--matrix", default="research/feature_matrix.json")
    ap.add_argument("--out", default="research")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest: return selftest()

    with open(args.matrix, encoding="utf-8") as f:
        rows = json.load(f)["rows"]
    analysis = analyze(rows)
    os.makedirs(args.out, exist_ok=True)
    with open(os.path.join(args.out, "gradient_analysis.json"), "w", encoding="utf-8") as f:
        json.dump({"generated_at": datetime.now(timezone.utc).isoformat(), **analysis},
                  f, ensure_ascii=False, indent=2)
    emit_rubric_yaml(analysis, os.path.join(args.out, "rubric-draft.yaml"))
    emit_report(analysis, os.path.join(args.out, "patterns-report-draft.md"))
    n_tiers = len({r.get("star_tier") for r in rows if r.get("star_tier")})
    print(f"[ok] gradient_analysis.json / rubric-draft.yaml / patterns-report-draft.md 已輸出 (n={analysis['n']}, tiers={n_tiers})")
    if n_tiers < 3:
        print("[note] 有效 tier <3:分類多為 insufficient-tiers,屬預期(完整判定需 Phase 1 全量四層資料)")
    print("[G3] 請人工逐條審查 rubric-draft.yaml(權重公式、門檻常數、機制陳述)後才得進 Phase 5")

if __name__ == "__main__":
    main()
