# obra/superpowers(T3/C/272628)

## 抽讀樣本
- skills/brainstorming/SKILL.md
- skills/receiving-code-review/SKILL.md
- skills/subagent-driven-development/SKILL.md
- skills/writing-plans/SKILL.md
- skills/writing-skills/SKILL.md

## trigger 設計:good
- 5/5 description 都是觸發條件導向,4/5 以 "Use when" 開頭且語境具體:「Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear」。
- 刻意不在 description 摘要 workflow——writing-skills 明文解釋原因:「a description summarizes the skill's workflow, an agent may follow the description instead of reading the full skill」。
- brainstorming 例外地非常 pushy:「You MUST use this before any creative work」;是有意設計(CLAUDE.md 稱其為 acceptance test 的 auto-trigger 錨點),屬「適度偏強」的上限案例。

## 寫作風格:good
- 全面 imperative + 大量解釋 why:「Why no thanks: Actions speak. Just fix it.」、「Why subagents: ...preserves your own context」。
- MUST/NEVER 密度高但幾乎每條都附 rationale、反例表(Red Flags / Common Mistakes)、好壞對照範例(❌/✅ yaml、對話示例),不是裸堆疊 MUST。
- 獨特手法:dot digraph 流程圖、rationalization table(預先堵住 agent 的自我開脫)、「your human partner」統一措辭。

## scope 清晰度:good
- 一 skill 一 job 邊界清楚:brainstorming=設計前對話、writing-plans=計畫文件、subagent-driven-development=執行、receiving-code-review=接收回饋。
- skill 間用 `REQUIRED SUB-SKILL: superpowers:xxx` 交叉引用而非重複內容;writing-skills 明文規範此模式並禁止 @-force-load。

## 其他觀察
- writing-skills 本身即一套 meta-rubric(TDD for skills、SDO、token 預算 <500 words——但該 repo 自己的 skills 多數超過此字數,言行不完全一致)。
- CLAUDE.md 是罕見的「防 AI slop PR」貢獻守則(94% PR 拒絕率、要求揭露 model/harness),對 taxonomy C 的 repo 治理成熟度是強信號。
- 無 injection-suspect;instructions 均為正常 skill 行為塑形內容。
