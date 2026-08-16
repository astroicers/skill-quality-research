# Patterns Report — DRAFT(Phase 4 自動生成,量化部分)

- generated_at: 2026-08-16T07:55:34.008172+00:00
- n = 3(rubric 樣本,tier 有效)
- 子樣本規模: {"class_BD": 1, "fame_F0": 0, "cohort_C1": 0, "cohort_C2": 0, "cohort_C3": 0}
- **統計誠實聲明**: n 過小,不做迴歸、不宣稱顯著性;下表為 prevalence 梯度 + Spearman 描述值 (BRIEF Phase 4)。

## 1. Hygiene 門檻特徵(各層皆備)
_(本批資料不足或無)_

## 2. Tier 梯度特徵(differentiator,依 gap 排序)
_(本批資料不足或無)_

## 3. 反模式與 T0 特有現象
_TODO(Phase 3b 質化 + 人工):由 qualitative_notes 與 T0 層觀察填寫_

## 4. 官方規範 vs 社群實務落差
_TODO(LLM/人工):對照 anthropics/skills 與 skill-creator 撰寫_

## 5. 混淆因子分析
- fame / cohort / domain 分層方向見 gradient_analysis.json 的 robustness 欄位
- marketing-suspect 特徵(追星不追 engagement): 無
- 純度樣本(F0)未復現的 differentiator: 無

## 6. Rubric 權重與 tier 門檻推導依據
- 權重公式(提案): weight = 1 + round(4 × min(gap,60)/60),clamp 1..5 → **G3 審查對象**
- 判定常數: {"hygiene_min_prevalence": 70.0, "hygiene_max_range": 20.0, "diff_min_gap": 30.0, "min_tier_n": 3, "marketing_engagement_rho_max": 0.1}

## 附錄 A. Noise / 觀察記錄
無

## 附錄 B. 層數不足未判定
| feature | class | T0% | T1% | T2% | T3% | gap | ρ(log★) | F0復現 | mkt? | 強度 |
|---|---|---|---|---|---|---|---|---|---|---|
| skill_spec_compliant | insufficient-tiers | None | None | 100.0 | 100.0 | None | None | ✘ |  | n/a |
| fm_license_any | insufficient-tiers | None | None | 0.0 | 100.0 | None | None | ✘ |  | n/a |
| fm_allowed_tools_any | insufficient-tiers | None | None | 0.0 | 0.0 | None | None | ✘ |  | n/a |
| fm_metadata_any | insufficient-tiers | None | None | 0.0 | 0.0 | None | None | ✘ |  | n/a |
| desc_has_trigger_majority | insufficient-tiers | None | None | 0.0 | 100.0 | None | None | ✘ |  | n/a |
| dir_scripts | insufficient-tiers | None | None | 100.0 | 50.0 | None | None | ✘ |  | n/a |
| dir_references | insufficient-tiers | None | None | 0.0 | 50.0 | None | None | ✘ |  | n/a |
| dir_assets | insufficient-tiers | None | None | 100.0 | 50.0 | None | None | ✘ |  | n/a |
| dir_examples | insufficient-tiers | None | None | 0.0 | 50.0 | None | None | ✘ |  | n/a |
| dir_evals | insufficient-tiers | None | None | 100.0 | 0.0 | None | None | ✘ |  | n/a |
| has_plugin_json | insufficient-tiers | None | None | 100.0 | 50.0 | None | None | ✘ |  | n/a |
| has_marketplace_json | insufficient-tiers | None | None | 100.0 | 100.0 | None | None | ✘ |  | n/a |
| has_install_sh | insufficient-tiers | None | None | 100.0 | 0.0 | None | None | ✘ |  | n/a |
| install_oneliner_in_readme | insufficient-tiers | None | None | 100.0 | 100.0 | None | None | ✘ |  | n/a |
| has_ci | insufficient-tiers | None | None | 100.0 | 0.0 | None | None | ✘ |  | n/a |
| ci_validates_skills | insufficient-tiers | None | None | 100.0 | 0.0 | None | None | ✘ |  | n/a |
| has_tests_or_evals | insufficient-tiers | None | None | 100.0 | 0.0 | None | None | ✘ |  | n/a |
| has_changelog | insufficient-tiers | None | None | 100.0 | 0.0 | None | None | ✘ |  | n/a |
| has_version_tags | insufficient-tiers | None | None | 100.0 | 0.0 | None | None | ✘ |  | n/a |
| readme_has_before_after | insufficient-tiers | None | None | 100.0 | 50.0 | None | None | ✘ |  | n/a |
| readme_has_metrics | insufficient-tiers | None | None | 100.0 | 0.0 | None | None | ✘ |  | n/a |
| readme_has_demo_media | insufficient-tiers | None | None | 0.0 | 0.0 | None | None | ✘ |  | n/a |
| skill_md_count | insufficient-tiers | None | None | 100.0 | 100.0 | None | None | ✘ |  | n/a |
| skill_md_max_lines | insufficient-tiers | None | None | 100.0 | 100.0 | None | None | ✘ |  | n/a |
| desc_len_median | insufficient-tiers | None | None | 100.0 | 100.0 | None | None | ✘ |  | n/a |
| multi_harness_count | insufficient-tiers | None | None | 100.0 | 100.0 | None | None | ✘ |  | n/a |
| readme_lines | insufficient-tiers | None | None | 100.0 | 100.0 | None | None | ✘ |  | n/a |
| pct_markdown_files | insufficient-tiers | None | None | 100.0 | 100.0 | None | None | ✘ |  | n/a |
