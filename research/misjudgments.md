# 誤判記錄

> **一行一則,不要寫成報告。** 累積 5–10 條再一次處理。
>
> 為什麼是這個形式:本專案 15 節自審 + 兩輪一致性量測的**每一個發現**,
> 都來自「拿工具去用真實對象」或「獨立第三方指出來」,**零個來自更多分析**
> (完整歸類見 [`self-audit-round2.md`](self-audit-round2.md) §12–15)。
> 而 2026-08-18 的量測用數字證明了:再多量測也解析不出判準修訂的效果
> (每維度需 n≈404,用光母體差 7.6 倍,見 [`inter-rater-results-round2.md`](inter-rater-results-round2.md))。
>
> **所以這個檔案是這個專案往後唯一被證明會產出東西的管道。** 保持它輕。

## 格式

```
| 日期 | 對象 | 規則 | 它說什麼 | 我認為應該是什麼 |
```

「我認為應該是什麼」寫你的直覺就好,不用先查證 —— **查證是處理時才做的事**,
現在要的是不要讓那個瞬間的違和感消失。

## 處理紀律(累積後才做,不是每次)

1. **先去查,不要憑印象推翻。** 本專案記錄過至少五次「用間接訊號代替直接查證」
   而判錯的案例,其中一次是 rubric 對、我錯(§2),一次是連錯三輪(§15)。
2. **rubric 判對而你不喜歡結果,也是一種結論** —— §13 就是一例(自我指涉假陽性,
   查證後**刻意不修**,因為收窄會漏掉真陽性)。
3. 真的要改條文 → 遞增 `rubric_version`,並記得**理由段會污染下一輪量測**
   (見 [`../docs/llm-judge-contamination.md`](../docs/llm-judge-contamination.md) §3)。

---

## 待處理

| 日期 | 對象 | 規則 | 它說什麼 | 我認為應該是什麼 |
|------|------|------|----------|------------------|
| 2026-08-18 | `blader/humanizer` | L-002 `evidence_refs` | 「blader/humanizer(**33** pattern 皆附 why)」 | 實測 **35** 條編號 pattern,`Problem:`(why)33/35、`Before/After` 33/35、`Words to watch` 僅 **11/35**。可辯護版本:「35 pattern,33 附 why 與 Before/After」。源頭是 `qualitative_notes` 寫錯後被引進 rubric。見 [`directive-polarity.md`](directive-polarity.md) §4.2 |
| 2026-08-18 | `ayghri/i-have-adhd` | L-002 `evidence_refs` | 「why→rules→override→自檢」隱含每條規則都有對照 | 實測 10 條編號規則、僅 **8 對** `Bad:`/`Good:`。規則 9、10 無對照。同樣源自 `qualitative_notes` 未核原檔 |
| 2026-08-18 | 本 repo | R-005 `readme_has_before_after` | `lint_skill.py` L46–48 的 `BEFORE_AFTER_RE` 用 `❌.{0,500}?✅` 鄰近 regex 計分(weight 2,已接入 ASP G5) | `❌/✅` 在 61 檔語料只命中 9 檔,其中 **5 檔屬 obra 系**(P=0.0039)。此 regex 可能在偵測作者血統而非品質。**需要獨立評估**——不是說它一定錯,是說它從未被這樣檢驗過。見 [`directive-polarity.md`](directive-polarity.md) §5 |
| 2026-08-18 | 本 repo | L-002 `equivalent_forms` | 承認「**精確術語表:以定義消除歧義,取代靠例子示範**」為等價形式 | 三個獨立 context 收斂的機制是「禁令要附**已完成的替代示範**」,而術語表不提供示範。**L-002 比該機制寬。**⚠️ 但該機制本身未被檢定(`has_replacement` 收集了卻未彙總),所以**不知道該不該收窄**。要處理得先補那個量測 |

## 已處理

(處理後從上表移到這裡,附處置與 commit)

| 日期 | 對象 | 規則 | 處置 |
|------|------|------|------|
| 2026-08-17 | 本 repo | S-003 `cred_in_argv` | **查證後刻意不修** — 4 處命中全是 rubric 描述自己的樣態;收窄到 agent-facing 會漏掉 `anysearch` 那個真陽性(實作在 `.ps1` 而非 SKILL.md)。寧留假陽性不漏真陽性(§13) |
| 2026-08-18 | 一致性量測 | L-002 查表型 | 兩位審查者對同一條文讀出相反結論而**兩者都對** → 補裁定解除「good 在結構上不可達」,rubric 2.1.0(`40ea1c2`) |
| 2026-08-18 | 一致性量測 | L-004 `good` vs `n/a` | 三位獨立指認邏輯矛盾,兩位**各自發明相同的裁決規則** → 新增 `decision_order`,rubric 2.0.0(`9664857`) |
