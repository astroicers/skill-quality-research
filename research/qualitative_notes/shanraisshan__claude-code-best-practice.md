# shanraisshan/claude-code-best-practice(T2/C/64553)

## 抽讀樣本
- .claude/skills/agent-browser/SKILL.md
- .claude/skills/presentation/vibe-to-agentic-framework/SKILL.md
- .claude/skills/weather-fetcher/SKILL.md
- .claude/skills/weather-svg-creator/SKILL.md
- agent-teams/.claude/skills/time-fetcher/SKILL.md

## trigger 設計:mixed
agent-browser 是教科書級:「Use when the user needs to interact with websites…Triggers include requests to "open a website", "fill out a form"…」——觸發語+具體語境+使用者語句列舉俱全。但其餘樣本無觸發語:weather-fetcher/time-fetcher 標 `user-invocable: false`(刻意作為 agent 預載 skill,description 只寫「Instructions for fetching…」,屬合理設計而非疏忽);vibe-to-agentic-framework 的 description 純描述概念,無 Use when。

## 寫作風格:good
一致 imperative、指令可直接複製執行、每個 pattern 附完整範例。會解釋 why:Ref Lifecycle 段講清 refs 何時失效及原因;presentation framework skill 逐段解釋「Why Low level / Why TodoApp」的教學設計理由。weather 雙 skill 極簡但規則明確(「Use the exact temperature value provided — do not re-fetch」)。MUST 使用克制且都有上下文。

## scope 清晰度:good
每個 skill 恰好一個 job:瀏覽器自動化 CLI、抓 Dubai 溫度、產 SVG 卡片、簡報概念框架、抓 Dubai 時間。weather 系統刻意拆成 fetcher(agent 預載)+ svg-creator(Skill tool 呼叫)兩個 skill 示範 Command→Agent→Skill 分層,是 single-responsibility 的示範性案例。progressive disclosure 落實(references/ 與 templates/ 分層,SKILL.md 只留核心)。

## 其他觀察
- 本 repo 定位是 best-practice 參考庫,weather/time skills 是 pedagogical 玩具而非生產用途,評估時應視為「示範刻意極簡」。
- CLAUDE.md 品質高(<200 行自我要求、rules 的 paths lazy-load 說明),與 skill 內容相互一致。
- 無 injection-suspect 內容。
