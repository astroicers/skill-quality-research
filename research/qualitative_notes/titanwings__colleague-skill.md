# titanwings/colleague-skill(T2/B/22680)

## 抽讀樣本
- SKILL.md(根目錄單體 skill,讀前 400 行)

## trigger 設計:mixed
- frontmatter description 是「這是什麼」的雙語陳述(「Unified meta-skill engine for distilling colleague... characters」),無 Use when、無觸發語——對自動載入不利。
- 觸發語其實寫在 body 的「触发条件」段(「/dot-skill」「帮我创建一个 skill」「我想蒸馏一个人」),位置錯了:agent 未載入 body 前看不到。

## 寫作風格:mixed
- 程序性寫作紮實:工具對照表、逐步命令、失敗排查(「bot 未添加到群聊」「token 過期」)、多宿主相容規則並解釋原因(禁止猜測 cd 路徑)。
- 但全文中英雙份導致冗長;更重要的是指令中含高自主副作用動作:教 agent「自己写 Python 脚本」直呼飛書 API,並「向对方的 open_id 发一条消息('你好')」以取得 chat_id——skill 主動指示對真人發訊息。

## scope 清晰度:mixed
- 名義上一個 job(把人蒸餾成 skill),但單檔捆綁三個 character family + 五種採集通道 + 完整 OAuth 教學 + 版本管理,單一 SKILL.md 承載過多;progressive disclosure 依賴 prompts/ 與 tools/ 但主檔仍超載。

## 其他觀察
- ⚠ 隱私/倫理樣態(非 injection):skill 的核心流程是在目標同事不知情下採集其私聊訊息、文件、郵件(.eml/.mbox)以建立人格模擬,並指示以發訊息方式探取會話 ID。屬 rubric 應標記的「高風險資料採集型 skill」。
- 對照組價值:與 kangarooking/cangjie-skill 同為「蒸餾」meta-skill,但 trigger 放置與 scope 紀律明顯較弱。
- 無 prompt injection 式文字。
