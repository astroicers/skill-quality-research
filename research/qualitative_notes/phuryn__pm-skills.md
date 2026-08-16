# phuryn/pm-skills（T2 / D / 25300★）

## 抽讀樣本
- pm-execution/skills/summarize-meeting/SKILL.md（全文）
- pm-product-discovery/skills/analyze-feature-requests/SKILL.md（全文）
- pm-product-discovery/skills/brainstorm-experiments-new/SKILL.md（全文）
- pm-toolkit/skills/grammar-check/SKILL.md（前 150 行）
- pm-toolkit/skills/privacy-policy/SKILL.md（前 150 行）

## trigger 設計：good
- 每條 description 都是「做什麼 + Use when + 3 個具體場景」：「Use when reviewing customer feature requests, triaging a backlog, or making prioritization decisions」。具體、不過分 pushy、彼此區分度夠。
- CLAUDE.md 明文規定 description 要含 trigger phrases——觸發設計是有意識的治理項目。

## 寫作風格：good
- Imperative 編號步驟 + persona 開場（「You are an experienced product manager」）+ 現成輸出模板（meeting summary 表格、error report 格式）。有領域依據並註明出處（Dan Olsen Opportunity Score、Alberto Savoia《The Right It》），不是空泛 MUST。
- privacy-policy 的 [⚠️ LEGAL REVIEW REQUIRED] 標記與免責聲明是負責任的設計。範例品質好（grammar-check 每類錯誤都有 error→fix 對照）。
- 小瑕疵：CLAUDE.md 說「Skills need no placeholders」，但 grammar-check/privacy-policy 用了 `$OBJECTIVE`/`$TEXT` 等自訂 placeholder，treaty 與實作有輕微漂移；summarize-meeting 在正文引用 `$ARGUMENTS`。

## scope 清晰度：good
- 一個 skill 一個 job（會議紀要 / 需求分析 / 實驗設計 / 校對 / 隱私政策），無混裝。9 個 plugin 按 PM 職能分域，且規定禁止跨 plugin 硬引用——邊界治理明確。

## 其他觀察
- Further Reading 全部指向作者自家 Product Compass 內容，但 CLAUDE.md 強制中性語氣、禁 CTA，行銷動機被制度化約束。
- 有 validator + CI 一致性測試（計數、版本同步），treaty 級治理在 D 類合集中少見。
- 無 injection-suspect 內容。
