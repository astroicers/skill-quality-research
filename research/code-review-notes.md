# Code Review 覆核紀錄(2026-08-16,/code-review 分支審查 + receiving-code-review 覆核)

review 對象:`claude/claude-md-phase-0-31t3nk` vs main,聚焦 4 支 script 的統計/rubric 邏輯與 BRIEF 合規。
覆核紀律:逐條驗證技術正確性,不盲從。7 條全部成立(嚴重性有調整、F3 因果有修正)。

| # | finding | 覆核判定 | 處置 |
|---|---------|---------|------|
| F1 | lint 的 BEFORE_AFTER_RE 比 extract 校準版窄 → 低估 before_after、gap_list 錯報 | **真確**(嚴重性略高估:weight 2 + marketing_suspect) | ✅ 已修:lint 對齊 extract 寬版。⚠ 帶回 G2-Q6 標記的裸 Before…After 假陽性——見下方限制 |
| F2 | emit_report §6 印 pre-G3 舊 weight 公式,與實際計算矛盾 | **真確**(誤導 G3 審查者;手寫 patterns-report.md 已對) | ✅ 已修:emit_report §6 字串同步 G3 定稿公式 |
| F3 | apply_strata_caps 把非 rubric(E?/F)算進配額,稀釋樣本 | **部分真確**:Phase 1 執行 cap 時 F 類還是 TBD 候選(Phase 2 才回填 F),reviewer 因果錯置;實際 Phase 1 稀釋僅 E/E?(T0 約 4 位) | ⏸ 待裁:屬 Phase 1(G1 approved),修需重跑;記為已知限制,未來加 in_rubric_sample filter |
| F4 | extract parse_frontmatter naive fallback 不處理 block scalar,與 lint 分歧 | **真確但條件性**:環境有 PyYAML 6.0.3,實際走 yaml path,研究資料**未受影響** | ✅ 已修:fallback 加 block scalar(與 lint 對齊)+ 斷言;求無 PyYAML 可攜性 |
| F5 | lint 的 DIFFERENTIATOR weights/thresholds 硬編,與 rubric.yaml 脫鉤(drift risk) | **真確**(維護性,非當前錯) | ⏸ 待裁:加 drift-guard 或讓 lint 讀 rubric.yaml(增 yaml 依賴)——見待裁 |
| F6 | prevalence_by_tier median 用上中位,偶數 n 偏高 | **真確**(實質 bug;T1/T3 皆偶數 n) | ✅ 已修:改 statistics.median。實證:skill_md_max_lines T3 median 554→439.5 |
| F7 | gap_to_weight 對 packaging 設 cap 但 marketing 未設,marketing 可達 craft 頂 | **真確**(設計不對稱;當前唯一 marketing diff 已被 suspect,無實際觸發) | ✅ 已修:cap 擴至 packaging+marketing(符合 BRIEF §4 工序2) |

## 已修 5 條的驗證

- 全 3 支 selftest 綠(extract/aggregate/lint);新增 F4 fallback block-scalar 斷言。
- F6 重跑 aggregate:numeric-profile median 更正(T3 max_lines 554→439.5),differentiator 的 weight/prevalence 不受影響(用 prevalence 非 median),rubric.yaml 5 條不需重生。
- F7 對現有 differentiator 無數值影響(唯一 marketing signal readme_has_before_after 本就 weight 2 < 3),但語意對齊 spec。

## ⚠ F1 修正帶出的新限制(誠實記錄)

lint 對齊 extract 寬版後,`readme_has_before_after` 的偵測**含裸 `Before…After` 800 字視窗的假陽性**
(G2-Q6 已標記此假陽性樣態)。取捨:
- 對齊寬版 → 與 weight 校準一致(F1 修好),但帶回假陽性;
- 收窄兩者 → 消假陽性,但須重跑 Phase 3/4 重算 weight。
現選前者(一致優先);該特徵是 marketing signal + marketing_suspect + weight 2,影響極小。
**理想解(未來迭代)**:extract 與 lint 同步收窄 + 重算 weight。

## F3 / F5 裁決(2026-08-16,人工)

- **F3 → 記為已知限制 + 未來加 filter**(不重跑 Phase 1,不動 G1 approved 樣本)。
  `apply_strata_caps` docstring 已加精確 TODO(下輪重跑生效:cap 計數前濾掉 taxonomy in {E,E?},
  保留 TBD 候選;F 類不在此列因 Phase 1 時仍為 TBD)。
- **F5 → 加 drift-guard selftest**。lint runtime 維持零 yaml 依賴;selftest 以 naive 正則讀
  `references/rubric.yaml` 比對硬編 DIFFERENTIATORS weights,不一致即 fail。已雙向驗證
  (正常通過 + 注入 9≠4 能抓到)。

**7 條 findings 全部處置完畢**:F1/F2/F4/F6/F7 已修,F3 記錄+TODO,F5 drift-guard。
