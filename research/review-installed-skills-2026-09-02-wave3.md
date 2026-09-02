# B2 第三波:5 個未審已裝 skill × rubric 3.3.2(2026-09-02)

> lint 全過 hygiene;verdict 皆純函式;L-004 記序號。判讀者=rubric 維護者(污染照記)。

| skill | 形狀 | L-001 | L-002 | L-003 | L-004 | verdict |
|---|---|---|---|---|---|---|
| `ai-stack-writeup`(49) | process/rule | good | good | good | mixed(序2) | **approved-with-notes** |
| `andrej-karpathy-perspective`(501) | persona/domain | good | good | good | **good(序1 強)** | **approved** ⚠️見揭露 |
| `anysearch`(186,vendor) | domain 工具 | **mixed** | good | good | mixed(序2) | **needs-revision** |
| `archify`(121) | process 工具 | good | good | good | **good(序1 強)** | **approved** |
| `grill-with-docs`(88) | process/rule | good | good | good | good(序1) | **approved** |

## 關鍵證據

- **karpathy 序1 強形式**:frontmatter `调研时间: 2026-04-05` + 「调研截止」邊界 +
  **時效盲區處理段**(`:51`:截止日後的事以角色身份說「還沒了解到」)+ 引句附年份
  ——「調研截止日+時效盲區+誠實邊界」三件套齊。負向觸發也在
  (「不在用戶只是普通問 AI 時觸發」)。
  ⚠️ **揭露**:evidence_refs 具名稱道的 huashu-nuwa 生態系正是以此三件套聞名,
  本 skill 疑似同一作者族系——我對它的 good 可能與該正向定錨同構;
  取值有文本逐字支撐,但**降權使用、不引為判準有效性證據**
- **archify 序1 強形式**:`validate/deliver` 機械驗證協定(9 checks、receipt 判讀、
  「non-zero exit can never be described as success」、兩輪無改善即停損如實報)+
  brands **查詢命令取代憑記憶**。工具型 skill 做對 L-004 的活範本——
  它證明序 5 的工具文類困境**不是結構性宿命**,是可以寫出來的
- **anysearch L-001 mixed**:Trigger 段「information retrieval / fact-checking /
  web browsing」+「This skill is the **recommended** search tool」——收編幾乎一切
  查資訊意圖並自我推薦蓋過 harness 內建(**意圖收編縫第 2 個真實例**,與 asp 同判法);
  vertical 域映射本身正當。L-004 序2:`doc` 命令是「介面未知先查」的弱機制,
  但 15 域清單與旗標面在覆蓋外裸露
- **anysearch S-003 cred_in_argv 複核成立**(medium):`:87` 明文以 `--api_key`
  CLI flag 為第一優先憑證路徑(argv 暴露);`:104` auto-registered key 回寫**有**
  要求使用者確認(紀律對)。warning 級不翻 verdict,如實記
- **ai-stack-writeup 序2**:機制在(「抽 3 條聲明回原始素材交叉核對」+ 去識別化
  grep 自檢),但「新 skill 需開新 session」的 harness 行為斷言在覆蓋外裸露。
  與 caveman(無機制→序5)對照:**序 1/2/5 梯度在真實語料上成立**
- **grill-with-docs 序1**:repo 結構描述以假設語態+「exploration 先看」承載,
  ADR 三條件測試是可證偽判別法

## 縫活化紀錄

- **意圖收編**(蓄積列):anysearch 第 2 個真實例(vendor 自薦型)
- **probe 對象**(蓄積列):anysearch 的 python --version 偵測=環境探測,照 I 分界不計機制
  ——分界可用但仍是自選,維持蓄積

## 波間檢查

誤判佇列:零新增列(兩處活化已補記於列內)。B2 累計 **15/19**;
剩 4 個全是 evidence_refs 具名者(ga-methodology/diagnose/improve-codebase-architecture/
huashu-nuwa)——**終波需先產遮蔽判讀包或派不知情判讀者**,作者裸判會雙重定錨。
