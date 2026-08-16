# wanshuiyin/Auto-claude-code-research-in-sleep(T2/C/14742)

## 抽讀樣本
- skills/auto-review-loop/SKILL.md
- skills/comm-lit-review/SKILL.md
- skills/dse-loop/SKILL.md
- skills/mermaid-diagram/SKILL.md
- skills/paper-slides/SKILL.md

## trigger 設計:mixed
- 3/5 觸發語優秀:comm-lit-review「Use when the task is about communications, wireless...」+ fallback 邊界;dse-loop/paper-slides 枚舉使用者原話含中文(「做PPT」「sweep parameters」)。
- 2/5 偏弱:mermaid-diagram 的 description 只講功能無 Use when;auto-review-loop 的 description 在講 backend 機制(Copilot/Codex 路由)而非觸發語境。
- 獨特正面樣態:反誤觸發防護——「Do not wrap this skill in /loop, /schedule」並解釋為何(timer 重入會重置 reviewer 記憶、零新訊號全 token 成本)。

## 寫作風格:mixed
- 工程紀律極強:Constants 表、狀態持久化(compact recovery)、append-only 審計日誌、fail-closed 規則,多處解釋 why(「Why this exists: REVIEW_STATE.json is overwritten each round...」)。
- 但 auto-review-loop 協定密度過載(400+ 行的 backend 路由、evidence/nonce/acquittal 機制),且把版本修正殘留寫進正文:「Earlier wording here used `or`... that was an internal inconsistency; the `AND` form is authoritative」——changelog 混入行為指令。
- 出現疑似虛構模型名(`gpt-5.6-sol`、`gpt-5.5`)作硬編碼常數,知識過期風險高。
- dse-loop 有清楚的 Safety Rules 前置(NEVER sudo / rm -rf / git push)——防禦性寫作的好範例。

## scope 清晰度:good
- 每支 skill 一個 job:文獻回顧/DSE 迴圈/圖表生成/投影片生成/審稿迴圈,互不重疊;共用協定抽到 shared-references/(output versioning、reviewer routing、external-cadence)。
- auto-review-loop 單一 job 但單檔承載五種 reviewer backend 的完整協定,是「job 單一、實作超載」的樣態。

## 其他觀察
- 反 sycophancy 審稿設計:「Start from the assumption that the work is broken... Trust nothing the author tells you」+ 跨模型家族強制(executor 與 reviewer 必須不同家族,fail closed)。
- auto-review-loop 的 SCOPE LIMITS 明文將「malicious local user」排除出威脅模型並禁止 reviewer 提出 hash/digest 防護——屬「skill 限縮安全審查範圍」的可記錄樣態(有解釋理由,非惡意)。
- 無 injection-suspect。
