# B2 真實使用首波:5 個未審已裝 skill × rubric 3.3.2(2026-09-02)

> 精進計畫第 5 步首波。lint 全過 hygiene、packaging 0/14(內部剖面,照例不採計)。
> verdict 皆 `craft_verdict_rollup()` 純函式;L-004 記序號。判讀者=rubric 維護者(污染照記)。

| skill | 形狀 | L-001 | L-002 | L-003 | L-004 | verdict |
|---|---|---|---|---|---|---|
| `asp`(138 行,v4 router) | dispatcher | **mixed** | good | good | **mixed(序3)** | **needs-revision** |
| `security-weekly-tw`(786) | domain 工作流 | good | good | good | mixed(序3) | approved-with-notes |
| `triage`(103) | process/rule | good | good | good | **good(序1)** | **approved** |
| `grill-me`(10) | 互動協定 | good | good | good | n/a(序4) | **approved** |
| `to-issues`(81) | process/rule | good | good | good | good(序1) | **approved** |

## 關鍵證據

- **asp L-001 mixed**:description 觸發詞含裸泛詞 `review`、`verify`、`qa`、`審查`、`驗證`、`安全`
  ——會收編非 ASP 情境的一般意圖(**friction 縫「意圖收編」首次真實開火**,對照:
  多子意圖映射本身正當,各詞確實路由不同子 skill)。L-004 序3:路由指向 repo 內檔案
  (同步真,「關於 repo 自身內容的宣稱」判法可用),但零 anti-hallucination 機制。
  gap:觸發詞去泛詞化(`asp review` 型前綴);v5 凍結宣告(ADR-017)是好的狀態陳述,續用
- **security-weekly-tw L-004 mixed(序3)**:MCP 工具/來源清單緊鄰枚舉自驗;
  但「專案路徑」表寫死 `~/projects/...` 絕對家目錄路徑(本地產物載重,跨機器即錯)
  ——記 findings:改相對於 repo 或環境變數
- **triage/to-issues L-004 good(序1)的機制範本**:「The mapping should have been
  provided to you — run `/setup-matt-pocock-skills` if not」——不憑記憶假設 label 字串、
  缺件走 setup;`triage` 另有 state-conflict flag-and-ask。**這正是 statement_test
  要的攔截力,值得收進 patterns.md 當正例**(下批處理時考慮)
- **grill-me**:10 行完整即合格(互動協定豁免;它有 3 條輕規則,不觸發「有規則集
  應照常判 L-002」的縫——判 good 非 N/A,兩讀同值)

## 縫活化紀錄

- 意圖收編(蓄積列 #6):**asp 真實開火**——首個非實驗室實例
- repo 路徑同步所指(蓄積列 #4):asp 判定顯示「關於 repo 自身內容」讀法可運作,
  但條文仍未明文(維持蓄積)

## 波間檢查

誤判佇列:本波**零新增**(兩處皆為既有蓄積列的活化);下波(4-5 個)照常。
