# wshobson/agents（T2 / D / 38844★）

## 抽讀樣本
- plugins/accessibility-compliance/skills/screen-reader-testing/SKILL.md（前 400 行）
- plugins/backend-development/skills/temporal-python-testing/SKILL.md（全文）
- plugins/business-analytics/skills/data-storytelling/SKILL.md（全文）
- plugins/dotnet-contribution/skills/dotnet-backend-patterns/SKILL.md（前 150 行）
- plugins/observability-monitoring/skills/prometheus-configuration/SKILL.md（全文）

## trigger 設計：good
- 180 個 skill 的 description 一律以「Use when …」收尾且語境尚可：「Use when implementing Temporal workflow tests or debugging test failures」。模板化但一致、可路由。
- 缺點：觸發語是量產模板句，區分度靠主題名詞，無「not for」排除語。

## 寫作風格：mixed
- 本質是知識庫/教科書式 reference，不是 agent 工作流指令：Core Concepts、表格、checklist、程式碼範例。dotnet-backend-patterns 的 ✅/❌ 對照範例品質高；temporal 有明確的 progressive disclosure 指引（何時載入哪個 resources/*.md），且引用官方 docs 來源。
- 但深度極不均：prometheus-configuration 與 data-storytelling 是 60-70 行的殼，主體一句「Detailed pattern documentation lives in references/details.md」帶過；screen-reader-testing 是快捷鍵/checklist 傾倒。少數未溯源數字（螢幕閱讀器市占 %）。無 MUST 堆疊，也幾乎不解釋 why——因為它根本不指揮 agent 行為。

## scope 清晰度：good
- 每個 skill 單一主題、單一 job；靠 plugin 分組 + Related Skills 交叉引用。倉庫層級是 91-plugin 超市（taxonomy D），但單 skill 邊界乾淨。

## 其他觀察
- 工廠化產物：同一骨架（frontmatter → When to Use → Core Concepts → Best Practices）批量生成 180 份，品質梯度主要體現在「殼 vs 有肉」的比例。CLAUDE.md 反而是全 repo 最講究的檔案（多 harness 生成管線、150 行上限自律）。
- 無 injection-suspect 內容。
