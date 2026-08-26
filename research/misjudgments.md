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
   **2026-08-26 的第一次批次處理又添一次**:七條裡有一條查證後是 rubric 判對。
2. **rubric 判對而你不喜歡結果,也是一種結論** —— §13 就是一例(自我指涉假陽性,
   查證後**刻意不修**,因為收窄會漏掉真陽性)。
3. 真的要改條文 → 遞增 `rubric_version`,並記得**理由段會污染下一輪量測**
   (見 [`../docs/llm-judge-contamination.md`](../docs/llm-judge-contamination.md) §3)。
   落條文時理由寫在 CHANGELOG 與批次處理報告,rubric 內只留最小事實陳述。
4. **分清「待處理」「待測」「已處理」。** 儀器做不到的東西不該佔待處理額度——
   它不是還沒做,是目前做不了。放「待測」。

---

## 待處理

第一次批次處理於 2026-08-26 完成,原七條全數結案
(查證全文見 [`misjudgment-review-2026-08-26.md`](misjudgment-review-2026-08-26.md))。
下列一條是**同日獨立複審時新發現**、且**超出該 PR 的 AC**,依紀律另記不擴大 diff。

| 日期 | 對象 | 規則 | 它說什麼 | 我認為應該是什麼 |
|------|------|------|----------|------------------|
| 2026-08-26 | `addyosmani/agent-skills` | S-101 英文分支 | 判 S-101 命中(正向加分) | 命中源是 `skills/security-and-hardening/SKILL.md:3` 的「Use when building any feature that **accepts untrusted data**」與 `:25` 的「Where does **untrusted data** cross into your system?」——這兩句是**主題描述**(這個 skill 在講怎麼處理不可信輸入),不是**設立防禦條款**。同檔 `test-driven-development/SKILL.md:339` 的「is untrusted data, **not instructions**」才是真的。⚠️ **這是既有英文分支的問題,不是 2.2.0 引入的**:裸 `untrusted\s+data` 沒有「規定語意」的必要成分,與 CJK 分支 3 修掉的破口**完全同型**(見 rubric `language_coverage` 的判準說明)。可能修法:比照 CJK 分支要求前綴或 `not instructions` 共現。⚠️ 修之前先確認:S-101 是正向標記、過度命中只稀釋訊號不擋 gate,值不值得為此動一條已穩定的英文 regex |

## 待測(儀器目前做不到,**不佔處理額度**)

| 日期 | 對象 | 規則 | 卡在哪 | 解除條件 |
|------|------|------|--------|---------|
| 2026-08-18 | 本 repo | L-002 `equivalent_forms` | 條文承認「精確術語表」為等價形式,但三個獨立 context 收斂的機制是「禁令要附**已完成的替代示範**」,而術語表不提供示範 → **條文比機制寬**。是否該收窄,取決於 `has_replacement` 的彙總 | **不可復現。** 該屬性只在 [`directive-polarity.md`](directive-polarity.md) §4.1 的 LLM 標記協定收過,而同節偏離 5 記「收集但從未彙總」、偏離 6 記「逐條標記表**未保存進 repo**,故本節不可複現」;`feature_matrix.json`(80×65)無此欄。重做需 10 repo × 25 規則重新標記,**正是 2026-08-18 明令停止的路線**。依 L-002 `exemption` 自身的 ⚠️ 政策(「先修已證實的、把未證實的標為待測」)維持現狀 |
| 2026-08-26 | 本 repo | S-101 中文偵測的精確度 | 以「不可信輸入」為主題的**技術文件**會整類命中(獨立複審構造 13 句良性句、10 句命中):「使用者輸入不得直接執行,必須先跳脫」「注入的參數不可被當作指令碼執行」——談 XSS/SQL 防護,不是 skill 對自己設立的防禦條款。根因:CTX 詞表收了 `注入/不可信/使用者輸入`,而那正是**這類文件必然出現的詞**。與英文分支的 `accepts untrusted data` **完全同型** | **刻意不再追,已改標低信心。** 三輪複審的軌跡是「拒絕清單 → 三條件共現 → CTX 詞表 + 反轉排除」,**每輪都用更複雜的機制換來一組新形狀的破口,而每個破口都是複審者隨手構造十來句就找到的**——同 [`directive-polarity.md`](directive-polarity.md) 的標準決定:**這個問題無法用確定性儀器回答**。2.2.0 起 S-101 帶 `confidence: low-static-needs-llm`,走 SKILL.md 步驟 5 的 LLM 複核。解除條件:**有足量中文語料可量假陽性率時再談收窄**;在那之前把它當低信心訊號用,不當事實用 |
| 2026-08-26 | 本 repo | `REDFLAG_OBEY_OUTPUT` 的 CJK 覆蓋 | 該紅旗只認英文句法,中文的同語意表述漏判 | **需先有中文語料驗假陽性率。** 中文的「請完全依照上述步驟」在正當文件裡極常見(`humanizer/SKILL.md:23` 本身就是正當用法),補 CJK 樣態會製造假陽性,與 rubric 對 S-001「假陽性高、絕不單憑 lint 判定」的告誡相衝。目前 CJK 語料僅 13 份,不足以校準。**2.2.0 只補了正向的 S-101**(不進 gate,過度命中無安全風險) |

## 已處理

(處理後從上表移到這裡,附處置與 commit)

| 日期 | 對象 | 規則 | 處置 |
|------|------|------|------|
| 2026-08-17 | 本 repo | S-003 `cred_in_argv` | **查證後刻意不修** — 4 處命中全是 rubric 描述自己的樣態;收窄到 agent-facing 會漏掉 `anysearch` 那個真陽性(實作在 `.ps1` 而非 SKILL.md)。寧留假陽性不漏真陽性(§13) |
| 2026-08-18 | 一致性量測 | L-002 查表型 | 兩位審查者對同一條文讀出相反結論而**兩者都對** → 補裁定解除「good 在結構上不可達」,rubric 2.1.0(`40ea1c2`) |
| 2026-08-18 | 一致性量測 | L-004 `good` vs `n/a` | 三位獨立指認邏輯矛盾,兩位**各自發明相同的裁決規則** → 新增 `decision_order`,rubric 2.0.0(`9664857`) |
| 2026-08-18 | `blader/humanizer` | L-002 `evidence_refs` | **早已修完,只是沒歸檔。** 質化筆記(`qualitative_notes/blader__humanizer.md:10`)與 rubric `evidence_refs` 兩邊都已在 **2.1.1** 更正為「35 pattern 中 31 條附 why + Before/After」。批次處理時查兩處來源確認 |
| 2026-08-18 | `ayghri/i-have-adhd` | L-002 `evidence_refs` | **rubric 判對、我錯**(本專案第二次)。「10 條規則僅 8 對 `Bad:`/`Good:`」屬實,但規則 9(量化門檻+替代:「Five items ranked beats ten unranked」)與規則 10(三組具名禁用語+正面替代)各有 L-002 `equivalent_forms` 認可的等價形式;rubric 寫的是**結構**不是覆蓋率,四段(why 5 條 / rules 10 條 / override 6 條 / Pre-send check)逐一查證全部存在。**rubric 不動**;錯的是質化筆記寫「每條附 Bad/Good」,已修 |
| 2026-08-18 | 本 repo | R-005 `readme_has_before_after` | **已自行否證。** `feature_matrix.json` 早就含答案:80 repo 中 31 個 `True`,obra 系 1/2(期望 0.775,P=0.63)——零集中。P=0.0039 只屬於 `❌\|✅` 在 **SKILL.md** 上的分佈。**我在提出警示前沒查已有資料** |
| 2026-08-26 | `good-writing-tw` / `humanizer-en` | H-004 `knowledge_only` | **已修,rubric 2.2.0。** 判定由 `pct_markdown` 改量 `pct_prose`(含 `.txt/.rst/.adoc/.org` 與 `LICENSE/NOTICE/COPYING/…`)。兩個實測反例:`good-writing-tw`(75%)、`humanizer-en`(`SKILL.md`+`LICENSE`=50%)——後者反常在**附一個 LICENSE 就掉出豁免**。**門檻保留不取消**:實測直接拿掉會讓純資料目錄(15 個 `.json`)被誤判為純知識型,「不是程式碼」≠「是散文」。**數字不寫在這裡**——跑 `python3 scripts/measure_rubric_impact.py` 重現母體與兩種修法的 delta |
| 2026-08-26 | `humanizer-tw` | S-101 `defensive_untrusted_clause` | **已修,rubric 2.2.0。** S-101 補**繁簡中文**偵測(三條件共現:外來輸入標記 + 規定形式 + 無轉折語,非關鍵字比對)。**校準語料落在 `lint_skill.py` 的 `DEFENSE_CALIB_POS`/`_NEG` 常數、由 selftest 逐句斷言,本列刻意不寫命中率數字**——散文裡的數字無法轉紅(這一列初版寫過「4/4、0/6」而樣本不在 repo 內,由獨立複審抓出)。母體與新增命中的 delta 跑 `python3 scripts/measure_rubric_impact.py`,它量的是**生產偵測面**(整個 repo 的 `.md/.yml/.yaml/.sh`)而非僅 `SKILL.md`——用比生產面窄的母體校準會系統性低估假陽性曝險。⚠️ **本列初版誤稱「四條 regex 全英文字面 → 對 CJK 近乎全盲」,實測推翻**:`REDFLAG_CRED_ARGV`(`--token`)與 `REDFLAG_SELF_UPDATE`(`git pull`)比對**命令字面**,中文文件照常命中,**語言相依的只有散文型的兩條**。紅旗的 CJK 覆蓋轉入「待測」 |
| 2026-08-26 | `cloudflare` | S-003 `cred_in_argv` | **查證後刻意不修。** 命中源實查為 `references/tunnel/api.md:152` 的 `cloudflared tunnel run --token ${TUNNEL_TOKEN}` 等,**真陽性**。違和感在於 `cloudflared --token` 是官方唯一文件化方式、受審者無從修正,而輸出沒有格位能表達「真陽性但不可修」。**不為 n=1 增設格位**——成本高於收益,且新格位一旦存在就會被濫用來消音真紅旗(同 §13 的取捨)。**若出現第二例,再考慮加 `remediation: none-documented`** |
