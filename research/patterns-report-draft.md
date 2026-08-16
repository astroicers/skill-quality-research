# Patterns Report — DRAFT(Phase 4 自動生成,量化部分)

- generated_at: 2026-08-16T13:13:14.379195+00:00
- n = 54(rubric 樣本,tier 有效)
- 子樣本規模: {"class_BD": 40, "fame_F0": 22, "cohort_C1": 10, "cohort_C2": 38, "cohort_C3": 3}
- **統計誠實聲明**: n 過小,不做迴歸、不宣稱顯著性;下表為 prevalence 梯度 + Spearman 描述值 (BRIEF Phase 4)。

## 1. Hygiene 門檻特徵(各層皆備)
| feature | class | T0% | T1% | T2% | T3% | gap | ρ(log★) | F0復現 | mkt? | 強度 |
|---|---|---|---|---|---|---|---|---|---|---|
| skill_spec_compliant | hygiene | 100.0 | 100.0 | 100.0 | 100.0 | 0.0 | None | ✘ |  | strong |
| dir_scripts | hygiene | 71.4 | 87.5 | 84.8 | 83.3 | 11.9 | 0.002 | ✔ |  | strong |

## 2. Tier 梯度特徵(differentiator,依 gap 排序)
| feature | class | T0% | T1% | T2% | T3% | gap | ρ(log★) | F0復現 | mkt? | 強度 |
|---|---|---|---|---|---|---|---|---|---|---|
| has_marketplace_json | differentiator | 28.6 | 62.5 | 60.6 | 100.0 | 71.4 | 0.321 | ✔ | ⚠ | moderate |
| dir_examples | differentiator | 14.3 | 25.0 | 33.3 | 66.7 | 52.4 | 0.197 | ✔ |  | moderate |
| install_oneliner_in_readme | differentiator | 57.1 | 62.5 | 78.8 | 100.0 | 42.9 | 0.321 | ✔ |  | strong |
| has_tests_or_evals | differentiator | 28.6 | 50.0 | 69.7 | 66.7 | 38.1 | 0.213 | ✔ |  | strong |
| readme_has_before_after | differentiator | 28.6 | 50.0 | 45.5 | 66.7 | 38.1 | 0.192 | ✔ | ⚠ | moderate |

## 3. 反模式與 T0 特有現象
_TODO(Phase 3b 質化 + 人工):由 qualitative_notes 與 T0 層觀察填寫_

## 4. 官方規範 vs 社群實務落差
_TODO(LLM/人工):對照 anthropics/skills 與 skill-creator 撰寫_

## 5. 混淆因子分析
- fame / cohort / domain 分層方向見 gradient_analysis.json 的 robustness 欄位
- marketing-suspect 特徵(追星不追 engagement): ['has_marketplace_json', 'readme_has_before_after']
- 純度樣本(F0)未復現的 differentiator: 無

## 6. Rubric 權重與 tier 門檻推導依據
- 權重公式(G3 定稿): base = 1 + round(4 × min(gap,60)/60);weight = round(base × evidence 係數);non-craft(packaging/marketing)signal 上限 3;clamp 1..5(evidence: strong×1 / moderate×0.6 / weak×0.3)
- 判定常數: {"hygiene_min_prevalence": 70.0, "hygiene_max_range": 20.0, "diff_min_gap": 30.0, "min_tier_n": 3, "marketing_engagement_rho_max": 0.1}

## 附錄 A. Noise / 觀察記錄
| feature | class | T0% | T1% | T2% | T3% | gap | ρ(log★) | F0復現 | mkt? | 強度 |
|---|---|---|---|---|---|---|---|---|---|---|
| fm_license_any | observation-only | 28.6 | 37.5 | 42.4 | 83.3 | 54.7 | 0.206 | ✘ |  | weak |
| fm_allowed_tools_any | noise | 42.9 | 37.5 | 27.3 | 16.7 | -26.2 | -0.122 | ✘ |  | n/a |
| fm_metadata_any | noise | 42.9 | 50.0 | 45.5 | 33.3 | -9.6 | -0.062 | ✘ |  | n/a |
| desc_has_trigger_majority | noise | 71.4 | 50.0 | 60.6 | 50.0 | -21.4 | -0.131 | ✘ |  | n/a |
| dir_references | noise | 85.7 | 75.0 | 69.7 | 66.7 | -19.0 | -0.224 | ✘ |  | n/a |
| dir_assets | noise | 85.7 | 62.5 | 60.6 | 66.7 | -19.0 | -0.138 | ✘ |  | n/a |
| dir_evals | noise | 0.0 | 12.5 | 21.2 | 0.0 | 0.0 | 0.211 | ✔ |  | n/a |
| has_plugin_json | noise | 28.6 | 62.5 | 54.5 | 83.3 | 54.7 | 0.292 | ✔ |  | n/a |
| has_install_sh | noise | 42.9 | 12.5 | 18.2 | 16.7 | -26.2 | -0.078 | ✘ |  | n/a |
| has_ci | noise | 28.6 | 87.5 | 81.8 | 50.0 | 21.4 | 0.054 | ✔ |  | n/a |
| ci_validates_skills | noise | 28.6 | 75.0 | 63.6 | 33.3 | 4.7 | -0.04 | ✔ |  | n/a |
| has_changelog | noise | 14.3 | 25.0 | 42.4 | 16.7 | 2.4 | 0.083 | ✔ |  | n/a |
| has_version_tags | noise | 42.9 | 75.0 | 72.7 | 66.7 | 23.8 | 0.029 | ✔ |  | n/a |
| readme_has_metrics | noise | 42.9 | 37.5 | 69.7 | 50.0 | 7.1 | 0.126 | ✔ |  | n/a |
| readme_has_demo_media | noise | 14.3 | 12.5 | 30.3 | 16.7 | 2.4 | 0.079 | ✔ |  | n/a |

## 附錄 B. 層數不足未判定
無
