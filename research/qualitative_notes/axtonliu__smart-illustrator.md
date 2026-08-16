# axtonliu/smart-illustrator（T0 / B / 544★）

## 抽讀樣本
- SKILL.md（前 250 行；skill 位於 repo 根目錄，單 skill repo）

## trigger 設計：mixed
- description 有「觸發詞：配圖、插圖、PPT、slides、封面圖…」顯式列表，可路由；但整段是功能清單（三種模式 + 參數說明）而非「何時使用」的語境描述，無 Use when 句式、無排除條件。
- 觸發詞偏名詞堆疊，「PPT」「slides」這類寬泛詞容易誤觸發（用戶談論 PPT 內容≠要配圖）。

## 寫作風格：mixed
- 開篇「⛔ 強制規則（違反即失敗）」是 MUST 式高壓寫法，但值得注意：規則 1 用三行對照例子精準修補一個真實失效模式（把用戶給的檔案誤當 skill 配置），規則 2 給了 ❌/✅ 對照——MUST 有所指，不是空喊。
- 引擎選擇邏輯有解釋 why（「Mermaid 視覺表現力有限，能用 Excalidraw 就不用」）；命令模板具體可執行（HEREDOC + prompt-file）；語義色板/佈局規則是可查表的硬規格。整體實用但幾乎全是規則與參數表，缺敘事層。

## scope 清晰度：mixed
- 單一 skill 內裝三個 job：文章配圖、PPT 批量信息圖、封面圖，再疊三種引擎（Gemini/Excalidraw/Mermaid）與四平台尺寸。彼此相關（都是「為內容生成圖」）但按「一個 skill 一個 job-to-be-done」標準應拆分或至少分層——目前全靠 `--mode` 旗標分流，SKILL.md 一次載入全部細節。
- 有部分 progressive disclosure（styles/*.md、references/excalidraw-guide.md 按需讀取）。

## 其他觀察
- T0 樣本中結構完成度不差（styles/ 外置、config 優先級、降級路徑），差距主要在 trigger 語境化與 scope 收斂,而非粗製濫造。
- 命令硬編碼 `~/.claude/skills/smart-illustrator/` 安裝路徑，換位置即失效——與 text-to-cad 的 provenance/自定位做法成對比。
- 無 injection-suspect 內容。
