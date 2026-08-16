# jnMetaCode/superpowers-zh（T1 / taxonomy C / 7,686 stars）

## 抽讀樣本
- skills/brainstorming/SKILL.md
- skills/chinese-documentation/SKILL.md
- skills/receiving-code-review/SKILL.md
- skills/subagent-driven-development/SKILL.md
- skills/writing-skills/SKILL.md

## trigger 設計：mixed
- 繼承上游 obra/superpowers 的「description 只寫觸發條件、不寫流程」哲學，且 writing-skills 把理由講透：「描述總結了技能的工作流時，Claude 可能會跟隨描述而非閱讀完整的技能內容」——trigger 設計的 meta 認知是高水準。
- 但全數 description 已中文化：「当在当前会话中执行包含独立任务的实现计划时使用」(subagent-driven-development)。若使用者/宿主環境以英文運作，語意匹配召回可能劣化；這是翻譯 fork 特有的 trigger 風險。
- pushy 度兩極：brainstorming 極度 pushy（「在任何创造性工作之前必须使用此技能」+ 正文 <HARD-GATE>）；chinese-documentation 則反向明示「仅在用户显式 /chinese-documentation 时调用，不要根据上下文自动触发」。兩者各有道理，但整包一致性不足。

## 寫作風格：good
- 忠實保留上游的高規格寫法：rationalization 反駁表（「"记账本是额外开销" → 账本是能在压缩中存活下来的东西」）、dot 語法流程圖、紅綠對照範例、鐵律句式（「没有失败的测试就不写技能」）。
- 講 why 密度高：subagent-driven-development 解釋為何用子智能體（隔離上下文、保留協調者 context）、為何審查不可跳過（「没有审查的循环只是未经核实的空转」）。
- 譯文流暢、術語處理得當；chinese-documentation 本身就是排版規範，自我一致。

## scope 清晰度：good
- 一 skill 一流程 job（頭腦風暴→設計、收審查意見、子智能體執行計畫、寫 skill、中文排版），與上游相同的清晰切分；20 個 SKILL.md 無明顯湊數。
- chinese-documentation 是本 fork 新增的本地化 skill，與翻譯定位相符。

## 其他觀察
- 無 injection-suspect。CLAUDE.md 對貢獻者/agent 有強指令式門檻（「停下来。做任何事之前先读这一节」+ 要求回覆暗語「Strange things are afoot at the Circle K」以證明讀過），屬上游帶來的合規測試手法，指令對象是本 repo 的維護流程，非劫持外部任務。
- 對 rubric 的啟示：翻譯 fork 的品質幾乎完全繼承上游，「原創性/衍生性」與「描述語言 vs 觸發匹配」應是獨立於寫作品質的維度。
