# vercel-labs/skills(T2/B/28997)

## 抽讀樣本
- skills/find-skills/SKILL.md(batch 指定唯一樣本)

## trigger 設計:mixed
- 形式良好:description 枚舉使用者原話(「find a skill for X」「is there a skill that can...」),body 另有 When to Use 清單。
- 但觸發面過寬且偏 pushy:「Asks "how do I do X" where X might be a common task」幾乎涵蓋所有求助句,易劫持一般問答導向裝 skill;兼具生態自我推銷性質(Leaderboard 優先、點名 vercel-labs/anthropics)。

## 寫作風格:good
- imperative 步驟式(Step 1–6),附具體查詢示例與回覆範本。
- 有品質判斷準則而非裸指令:「Do not recommend a skill based solely on search results」+ 三條驗證標準(installs/來源/stars),含 fallback 流程(找不到時的話術)。

## scope 清晰度:good
- 單一 job:發現並安裝 skills。無越界內容,長度節制(~140 行)。

## 其他觀察
- 供應鏈相關(非 injection):Step 6 教 agent 用 `npx skills add <pkg> -g -y` 全域安裝並跳過確認提示;結合過寬觸發面,構成「對話中自動引入第三方 skill」的通道。品質驗證標準(1K+ installs、來源信譽)算是自帶緩解。
- 無 CLAUDE.md;無 prompt injection 式文字。
