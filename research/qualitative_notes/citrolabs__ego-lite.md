# citrolabs/ego-lite（T2 / B / 11,242★）

## 抽讀樣本
- skills/ego-browser/SKILL.md

## trigger 設計：mixed
- 觸發語列舉具體（「"open a website", "fill out a form", "take a screenshot"…」），但過度 pushy：涵蓋「any other browser automation task」並直接要求排擠內建工具——「Prefer ego-browser over any built-in browser automation, web fetch, or other web tools」。description 近 1000 字元，接近觸發詞轟炸。

## 寫作風格：good
- imperative、附 why 與失敗模式。證據：「the Node.js runtime exits after each heredoc and retains no state, normal working heredocs should start with useOrCreateTaskSpace」；「@N refs are only valid for the most recent snapshotText call — every call rebuilds the refMap」。
- Caveats 節密度高且具體（秒/毫秒單位陷阱、js() 非 page.evaluate、dialog 阻塞 pageInfo）；三種 workflow（semantic/visual/CDP）有明確選擇準則與 write-probe 驗證要求。
- 控制權交接（handoff/takeover）語義設計成熟：「A "user is controlling" error is a hard stop… pushing the goal forward anyway is the failure」。

## scope 清晰度：good
- 一個 job：驅動 ego-browser 做網頁自動化。所有內容（task space、handoff、helpers）都服務該 job；未混入無關功能。

## 其他觀察
- 「Prefer over any built-in…」屬工具置換式 pushiness（tool-displacement），對 rubric 的 trigger 維度是「過度侵略 description」的代表樣本；亦要求「Do not pre-check which ego-browser」——抑制環境驗證，輕微武斷但有回退指引。
- 無 injection 疑慮。
