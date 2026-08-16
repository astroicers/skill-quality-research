# mvanhorn/last30days-skill（T2 / B / 58,344★）

## 抽讀樣本
- skills/last30days/SKILL.md（前 ~400 行；檔案自述 1400+ 行。註：本次讀取經工具壓縮，部分正文字句非逐字，引文僅取自未壓縮的 frontmatter 與可確認段落）
- 另參考 repo CLAUDE.md/AGENTS.md（自動載入）

## trigger 設計：mixed
- description 是能力描述而非「Use when」句式：「Research what people actually say about any topic in last 30 days…」；靠 argument-hint 與 slash command 補足。
- tags 極多（30+ 平台詞）偏 SEO 式觸發，觸發語境廣但不假。

## 寫作風格：poor→mixed（結構上 poor，內容誠實度高）
- 單檔 1400+ 行、11 條全大寫「LAW」、多層 self-check 與「MANDATORY」「STOP regenerate」堆疊，違反 progressive disclosure；skill 自己承認檔案長到模型讀不到尾（「file too long [to] reach before synthesis. Moved here in v3.0.8」）。
- 特殊優點：每條 LAW 附日期化 failure postmortem（如 2026-04-18 0/8 regression），是「用 why 支撐 MUST」的極端工程化版本——但整體是靠 shouting 維持 output contract。

## scope 清晰度：mixed
- 名義上一個 job（近 30 天輿情研究），實際塞入多個 job：research、library search、library feed、topic queue、discovery 三段協議、doctor 健檢，各有 fast path 分支，單一 SKILL.md 承載過多。

## 其他觀察
- ⚠ 值得注意（非典型 injection，屬 harness-override 設計）：LAW 1 明示覆蓋 WebSearch 工具自帶的「MUST include Sources:」要求（「Inside /last30days [this] mandate [is] SUPERSEDED」），並宣告 skill 模板優先於使用者全域記憶偏好（「skill template wins inside skill output」）。這是 skill 主動指示模型忽略 harness/使用者層指令的案例，對 rubric 的「權限層級尊重」維度是重要負面/爭議樣本。
- 開頭含 cache/path 檢測 bash 與 STEP 0 first-run wizard（裝 yt-dlp、抽瀏覽器 cookies）——高權限副作用寫在 skill 內，供應鏈面需標記（僅靜態記錄，未執行）。
