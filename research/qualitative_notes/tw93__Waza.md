# tw93/Waza（T1 / D / 6853★）

## 抽讀樣本
- skills/check/SKILL.md（前 200 行）
- skills/hunt/SKILL.md（前 200 行）
- skills/learn/SKILL.md（前 120 行）
- skills/think/SKILL.md（前 120 行）
- skills/ui/SKILL.md（前 120 行）

## trigger 設計：good
- 三層觸發設計：description 含「Use when users ask in any language for…」+「Not for …」排除句；自訂 `when_to_use` 欄位列中英雙語觸發短語（「排查, 报错, used to work, broke after update」）；再加 `dispatch_intent` 供路由。是本批對「觸發」投資最重的 repo。
- 注意 `when_to_use`/`dispatch_intent` 是非標準 frontmatter 欄位，依賴自家 RESOLVER.md 路由——可移植性略受限，但設計意圖明確。

## 寫作風格：good
- Outcome Contract 開篇（outcome/done when/evidence/output/authorization），先定義「做完長什麼樣」再給流程——與常見的步驟堆疊相反。大量事故蒸餾出的 Gotchas 表（What happened → Rule），例：「Build passed but UI still looked wrong → Move up the Runtime Evidence Ladder」。規則附 why：「A patch applied to a symptom creates a new bug somewhere else」。
- MUST 密度高（Hard Rules / Hard Stops）但每條可證偽、帶觸發條件與證據要求（HIGH finding 需三件證據），非空喊。模式化 progressive disclosure（Mode Picker → 按需載 references/mode-*.md）。單檔仍偏長（check 200+ 行）。

## scope 清晰度：good
- 8 個 skill 硬上限、RESOLVER 路由表、每個 skill 的 description 自帶 Not-for 邊界。check 覆蓋 review+triage+release+audit 偏寬，但用 mode 檔外置化解；skill 間互相 handoff（hunt→ui、learn→read/write）有明文分界。

## 其他觀察
- CLAUDE.md 本身是一份 skill 設計方法論（no-op test、「give the model the target, not the path」、leading words 壓縮技巧），對本專案 rubric 推導有直接參考價值。
- skill_md_count=16 是 skills/ 與生成的 plugins/waza/ 鏡像重複計數，實際 8 個 skill。
- 無 injection-suspect 內容。
