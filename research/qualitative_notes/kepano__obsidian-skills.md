# kepano/obsidian-skills（T2 / taxonomy D / 46,344 stars）

## 抽讀樣本
- skills/defuddle/SKILL.md
- skills/json-canvas/SKILL.md
- skills/obsidian-bases/SKILL.md（僅前 400 行）
- skills/obsidian-cli/SKILL.md
- skills/obsidian-markdown/SKILL.md

## trigger 設計：good
- 觸發條件錨定在可客觀判定的訊號上：副檔名（.canvas / .base / .md）、使用者提及的名詞（wikilinks, callouts, Bases）。
  證據：「Use when working with .canvas files, creating visual canvases, mind maps, flowcharts」(json-canvas)
- defuddle 有罕見的高品質負向觸發：「Do NOT use for URLs ending in .md — those are already markdown, use WebFetch directly」。
- 適度 pushy：defuddle 主張「Use instead of WebFetch」並給出理由（省 token、去雜訊），是有依據的搶位而非濫觸發。

## 寫作風格：good
- 精煉的 reference 型寫法：表格化 schema、必填欄位、最少廢話；defuddle 全檔僅 42 行。
- 會標注具體 pitfall 而非堆 MUST。
  證據：「Use \n for line breaks in JSON strings. Do not use the literal \\n -- Obsidian renders that as the characters \ and n」
- obsidian-bases 對 Duration 型別的錯誤模式給了 CORRECT/WRONG 對照與原因（「Duration does NOT support .round() directly」）。
- 每檔含 Validation/Verify 步驟與官方 spec 連結，progressive disclosure 用 references/ 子檔（EXAMPLES.md、FUNCTIONS_REFERENCE.md）。

## scope 清晰度：good
- 一 skill 一格式/工具：網頁抽取、Canvas 格式、Bases 格式、CLI、Obsidian Markdown 語法。5 個 skill 零重疊，是小而純的官方配套 repo 典型。
- obsidian-cli 同時涵蓋 vault 操作與 plugin 開發除錯，稍寬，但仍是「用 CLI 操作 Obsidian」單一 job。

## 其他觀察
- 無 injection-suspect。
- 供應鏈面：defuddle 引導 `npm install -g defuddle`、obsidian-cli 含 `obsidian eval code=...`（在 app 內執行 JS）——皆為工具本身的正當文件，但屬於會擴大 agent 行為面的內容。
- 本 repo 是「官方廠商 + 少量高聚焦 skill」的品質上界樣本，適合作 rubric 的正向錨點。
