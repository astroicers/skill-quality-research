# muratcankoylan/Agent-Skills-for-Context-Engineering（T2 / D / 17,744★）

## 抽讀樣本
- examples/interleaved-thinking/generated_skills/comprehensive-research-agent/SKILL.md（機器生成範例）
- skills/advanced-evaluation/SKILL.md
- skills/context-optimization/SKILL.md
- skills/memory-systems/SKILL.md
- skills/self-improvement-loops/SKILL.md

## trigger 設計：good
- 統一「This skill should be used for: …」列舉式 description（第三人稱，符合注入 system prompt 的慣例），語境具體。
- 每個 skill 的 When to Activate 都含正向觸發 + 「Do not activate」路由到相鄰 skill：「Route file-backed scratchpads to filesystem-context, handoff summaries to context-compression…」（memory-systems）——負向邊界是全 corpus 制度化的（CLAUDE.md rule 8 強制）。

## 寫作風格：good
- 解釋 why 多於 MUST：「Constraints stated in prompt text get evolved away. Enforce budgets… in the runtime」（self-improvement-loops）。
- 結構標準化（Core Concepts / Gotchas / Integration / References），Gotchas 節是高訊號經驗失敗模式；數字宣稱帶 `claim-*` provenance ID 回鏈 claims/index.jsonl——罕見的可稽核性設計。
- 弱點：偏知識文獻而非可操作程序（比較像教材章節），部分閾值（50-70% 壓縮、<5% 品質降級）精確得可疑但至少集中管理。生成範例 skill（comprehensive-research-agent）明顯較弱：泛用清單 + self-report 分數 metadata。

## scope 清晰度：good
- 一 skill 一概念域且互相顯式劃界（Integration 節逐一聲明「This skill owns X, adjacent skills own Y」），是 taxonomy D 中 scope 治理最嚴謹的樣本之一。

## 其他觀察
- CLAUDE.md 定義完整 CI gate（frontmatter 驗證、skill_health --strict、activation-case 回歸 fixtures）——skill 品質被當測試對象，可作 rubric「工程化程度」上錨。
- 無 injection 疑慮。
