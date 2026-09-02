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

前兩次批次處理:2026-08-26(原七條)、**2026-08-27(第二次,11 條全數結案)**。
第二次的查證與處置全文見
[`misjudgment-batch-2026-08-27.md`](misjudgment-batch-2026-08-27.md)。

> ⚠️ **上一版導言的一句話是錯的,兩半都錯**,留在此處當紀錄:
> 它寫「`REDFLAG_OBEY_OUTPUT` 與 `REDFLAG_CRED_ARGV` 與 S-101 中文分支同一缺陷型,
> **可沿用同一修法**(三條件共現)」。
> (a) **兩條不同型**:前者是極性反轉(假陽性),後者是形式未涵蓋(假陰性)。
> (b) **修法不能沿用**:實測把三條件共現移植到 S-001,**7 命中只保留 1**,
> memU 的 4 個真陽性死掉 3(`python3 scripts/measure_obey_port.py` 可重跑) —— `_SOFT_NL` 在英文 markdown 條列上會併出數百字元的
> 「一句」,任何 `not`/`never` 都變成消音海綿。該機制在 CJK 短句剛好,英文長段落過度消音。
> 且**代價不對稱**:S-101 是正向標記不進 gate,S-001 是 error 會翻 verdict。
> 「兩個缺陷長得像」不蘊含「修法可以共用」——這是本次最值得記的一課。

**目前 10 條(蓄積中,friction 回歸 2026-09-02 三方收斂;依計畫「蓄積不即修」,
污染兩條已即修 3.3.2)。** 收斂矩陣與逐字紀錄:`research/friction-regression-2026-09-02/`。
原 4 條於 2026-08-27 結案(見「已處理」)。

| 日期 | 對象 | 規則 | 它說什麼 | 我認為應該是什麼 |
|------|------|------|----------|------------------|
| 2026-09-02 | friction×3(G-F1/H#1/I#3) | L-004 序 5 + rule 欄 | rule 寫「高階加分項」,序 5 把缺席變 gate | **自相矛盾且無比例感**:8 份 4 poor 全同構(工具包裝型整文類結構性落 poor);序 3 機械同步出口對 CLI 型結構性不可用;41 行乾淨 wrapper 與 960 行零溯源大全同格。readme 側修過的二元病以新形式回來。⚠️ **B2 真實使用 +2 例**(2026-09-02 wave2:caveman 49 行單一 ~75% 裸數字落 poor;write-a-skill 同型)——實驗室 4 + 真實 2 |
| 2026-09-02 | friction×3(H#2/G-F3/I 行為) | statement_test | 原則句要「攔截力」,清單收「單純來源標註=弱形式」 | **互斥**:裸引註不創造任何「須先查」情境——RinDig 憑一行 arXiv 在 good↔n/a 兩端,兩讀皆忠於條文 |
| 2026-09-02 | friction×3(H#3/G-F11/I#1) | 機制/probe 的對象 | 「live probe + 判讀表」列為機制 | **未定探測對象**:對使用者環境的前置探測 vs 對 skill 自身宣稱的鮮度查證——google 差兩級、shanraisshan 差 poor/mixed 全懸在判讀者自訂線;序 1/2 的「在覆蓋內」也無判別式(G-F11 提議:「該宣稱失效時,機制會不會在行動前讓模型發現或聲明?」) |
| 2026-09-02 | friction×2(G-F4/I#4) | equivalent_forms「repo 內相對路徑」 | 隨版控天然同步 | **未要求同步標的是權威事實源**——手抄外部 CLI 文件進 references/ 再相對引用,字面即過序 3;照此讀法任何有 references/ 的 skill 都到不了序 5,而同步的是文對文非文對事實 |
| 2026-09-02 | friction×3(H#4/G-F10/I#7) | L-001 評估面 | rule 寫「description 觸發語境」 | **body 的 when-to-use 段算不算沒說**——affaan 型(desc 零觸發、body 有清單)在 poor↔mixed 兩讀;一句「只評 frontmatter description,body 段記 findings」即可消歧 |
| 2026-09-02 | friction×3(H#11/G-F8,F9/I#9,#6) | L-001「適度 pushy」+ 基礎要件出處 | 只有同義簇抽 3 測試 | **意圖收編無測試**(裸 `push` 劫持使用者更小的顯式意圖);「非過寬」在 rule/pass_criteria/disambiguation 三段位階不一,「傷及基礎要件」無唯一出處;同一瑕疵跨維(L-001/L-003)可不可雙計無裁決 |
| 2026-09-02 | friction×2(G-F7/I#5) | 形狀表「一次性安裝/腳本型」 | 特徵=「裝完即棄」 | **安裝『指南』與安裝『腳本』無判別式**——google 型歸該列則 L-004 直接 N/A,成片裸斷言豁免;需判別句(自身裝完即棄+disable-model-invocation vs 教人安裝某物) |
| 2026-09-02 | friction×2(H#6/I#12) | 形狀表「互動協定型」 | 以主題(互動節奏)為鍵 | **有完整規則集的 mode skill 被抹 L-002**——ayghri 帶全批最強的 Bad/Good+override 卻字面落 N/A 列;該列鍵應是「無規則可解釋」而非主題;disable-model-invocation 的持續模式型在 L-001 也無著墨 |
| 2026-09-02 | friction×3(H#7/G-F12/I#10) | L-002 連言比例 | 「附因果 + 反例/等價」 | **MUST 堆疊的劑量-反應線缺**:同檔一半優秀 why 一半裸 MUST 檢查表時,mixed 從哪開始無指引;三位各自發明門檻 |
| 2026-09-02 | friction 單源利刃(I#11/I#2/G-F5/G-F14) | L-004 結構 | 序 1 合取、scope 分工 | (a) **全時效標注但無機制 → 序 5**(合取結構洞:帶標注是覆蓋的替代卻仍要機制);(b) **L-002 的 why 層與 L-004 載重互為材料**(五事實既是 L-002 冠冕又是 L-004 死因,補一行引用即跳序 1——合成義務沒寫);(c) 序 3 無部分覆蓋語言;(d) 同作者異 repo 工具靠類推 |

> ⚠️ **紀律偏離說明(2026-09-02)**:rubric 3.3.0(L-004 回灌)未走誤判批次——
> 它不是誤判,是**姊妹專案 readme-reviewer 兩輪盲判驗證過的結構缺口**
> (獨立第三方證據,查證已完成;先例:2026-08-27 收尾清空「門檻擋的是反射性修補,
> 不是已查證的收尾」)。全文 `research/backport-2026-09-02.md`。

⚠️ 後兩條是**未達 5–10 門檻就處理的**,理由記在這裡以免下次被當成先例:
使用者明確要求收尾清空,而兩條在批次處理期間**查證已經做完**、修法已定,
留著只是佔一個「待辦」的位子而不是一個「待查」的位子。
**門檻擋的是反射性修補,不是已查證的收尾。**

| 日期 | 對象 | 規則 | 它說什麼 | 我認為應該是什麼 |
|------|------|------|----------|------------------|

## 待測(新增 2 條,friction 回歸)

| 日期 | 對象 | 卡在哪 | 解除條件 |
|------|------|--------|---------|
| 2026-09-02 | L-003 | **8/8 good 零鑑別**(H#12/I#13,與 L-002 查表型鑑別力低同型)——不是誤判,是判準對這批太易滿足 | 需要含真實 scope creep 的語料;真實使用中出現 L-003 非 good 案例時回看 |
| 2026-09-02 | collection_sampling 協定 | 單檔語料讓抽樣/聚合規則**不可執行且不可見**(三方皆指)——判定對檔誠實、對 repo 未定義 | 下輪語料附「取自集合 repo」標記與檔數;或恢復多檔抽樣 |

## 待測(儀器目前做不到,**不佔處理額度**)

| 日期 | 對象 | 規則 | 卡在哪 | 解除條件 |
|------|------|------|--------|---------|
| 2026-08-18 | 本 repo | L-002 `equivalent_forms` | 條文承認「精確術語表」為等價形式,但三個獨立 context 收斂的機制是「禁令要附**已完成的替代示範**」,而術語表不提供示範 → **條文比機制寬**。是否該收窄,取決於 `has_replacement` 的彙總 | **不可復現。** 該屬性只在 [`directive-polarity.md`](directive-polarity.md) §4.1 的 LLM 標記協定收過,而同節偏離 5 記「收集但從未彙總」、偏離 6 記「逐條標記表**未保存進 repo**,故本節不可複現」;`feature_matrix.json`(80×65)無此欄。重做需 10 repo × 25 規則重新標記,**正是 2026-08-18 明令停止的路線**。依 L-002 `exemption` 自身的 ⚠️ 政策(「先修已證實的、把未證實的標為待測」)維持現狀 |
| 2026-08-26 | 本 repo | S-101 中文偵測的精確度 | 以「不可信輸入」為主題的**技術文件**會整類命中(獨立複審構造 13 句良性句、10 句命中):「使用者輸入不得直接執行,必須先跳脫」「注入的參數不可被當作指令碼執行」——談 XSS/SQL 防護,不是 skill 對自己設立的防禦條款。根因:CTX 詞表收了 `注入/不可信/使用者輸入`,而那正是**這類文件必然出現的詞**。與英文分支的 `accepts untrusted data` **完全同型** | **刻意不再追,已改標低信心。** 三輪複審的軌跡是「拒絕清單 → 三條件共現 → CTX 詞表 + 反轉排除」,**每輪都用更複雜的機制換來一組新形狀的破口,而每個破口都是複審者隨手構造十來句就找到的**——同 [`directive-polarity.md`](directive-polarity.md) 的標準決定:**這個問題無法用確定性儀器回答**。2.2.0 起 S-101 帶 `confidence: low-static-needs-llm`,走 SKILL.md 步驟 5 的 LLM 複核。解除條件:**有足量中文語料可量假陽性率時再談收窄**;在那之前把它當低信心訊號用,不當事實用 |
| 2026-08-26 | 本 repo | `REDFLAG_OBEY_OUTPUT` 的 CJK 覆蓋 | 該紅旗只認英文句法,中文的同語意表述漏判 | **需先有中文語料驗假陽性率。** 中文的「請完全依照上述步驟」在正當文件裡極常見(`humanizer/SKILL.md:23` 本身就是正當用法),補 CJK 樣態會製造假陽性,與 rubric 對 S-001「假陽性高、絕不單憑 lint 判定」的告誡相衝。目前 CJK 語料僅 13 份,不足以校準。**2.2.0 只補了正向的 S-101**(不進 gate,過度命中無安全風險) |
| 2026-08-27 | 本 repo | H-002 後半「非官方 template 佔位語」 | 條文要求偵測「description 是抄官方 template 沒改的佔位文字」,而程式從未實作 | **實作它會擊中官方 baseline。** 實測精確比對官方 template 字串 → 命中 `anthropics/skills`(T3、18/18 全合規)—— 它附了一份**給人抄的 template**,而那是正當內容。與 `superpowers-marketplace` 的 H-001 誤判**同型**(工具分不出「這是壞的」與「這是範本」)。3.1.0 已把 H-002 降 `info` 並註明未實作。**解除條件:有足量 template 衍生語料可量假陽性率。** 前半(description 非空)已由 H-001/H-005 涵蓋,不另設 id(ADR-031) |
| 2026-08-27 | 本 repo | `REDFLAG_CRED_ARGV` 的 `VAR=value cmd` 形式 | 環境前綴形式的憑證傳遞不命中(memU `INSTALL.md:331`) | **補樣式的精確度是 8–15%,不值得。** 天真版 `\w*(API_KEY\|TOKEN)\w*=` 全語料 111 命中 / 61 檔(`export FOO_API_KEY=xxx` 這種正當設定整批掃進來);收窄版 13 命中中最多 1–2 真。而 `SKILL.md:84` 把 `cred_in_argv` 的 `medium` 當成「假陽性率最低、推翻它需要最強證據」在用,**整套複核紀律建立在那個標籤上**,補進去會直接摧毀它的語意。3.1.0 改以 `lint_skill.CRED_KNOWN_UNCOVERED` 常數收該實例並由 selftest 斷言「目前不命中」——缺口變成可見、可轉紅。**解除條件:有辦法在不犧牲 `medium` 語意的前提下辨識該形式**(例如先判斷該行是不是要被執行的指令) |

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

### 收尾清空(2026-08-27,2 條)

兩條都是**同一型**:判準把責任壓在一個它自己沒定義 / 沒存放的東西上。
落地版本 rubric **3.2.0** / 工具 **2.2.0**,PR #15。

| 日期 | 對象 | 規則 | 處置 |
|------|------|------|------|
| 2026-08-27 | 本 repo | S-001/S-002/S-003 的 `confidence` | **已修:入條文 + drift-guard。** `medium` / `low-static-needs-llm` 原本**只存在於 `lint_skill.SECURITY_RULES`**,兩份 rubric 一個字都沒有 —— 而 `SKILL.md:82/:91` 的整套複核紀律(「low 不得單獨判死」「推翻 medium 需要最強證據」)就掛在那兩個詞上。⇒ 新增 `confidence_values` 定義段(**值不是形容詞,是對複核者的舉證責任分配**)+ **逐 flag** 的 `confidence` 欄。**逐 flag 是必要的**:S-003 底下 `cred_in_argv`(比對命令字面,medium)與 `self_update`(要判給人看還是給 agent 跑,low)信心不同,單一欄位會把這個差別抹掉,而那個差別正是複核紀律的依據。新增 `parse_rubric_security_confidence()` + drift-guard(逐 flag 比對 + 值域雙向相等)|
| 2026-08-27 | 本 repo | `run_evals.py` 的 `expect_block` | **已修:移進 `evals.json`。** 「哪個 repo 該擋」原本硬編在 `real_repo_cases()` 裡、其餘一律預設 False。與 `security` 欄位是同一個 schema 缺口的第二面:**新增一個「該擋」的 case 必須同時改兩個檔,而只改 `evals.json` 不會有任何東西轉紅** —— 那個 case 會被靜默當成「不該擋」。⇒ `expect_block` **必填無預設**、`expect_block_reason` 一併必填(布林說不出「因為 H-001 error」還是「因為根本沒 hygiene error」),新增 `c_expect_block_schema` 並斷言**擋/不擋兩側都至少各有一個 case** |

### ASP 跨 repo(2026-08-27)

兩條都是**登記時就寫明「跨 repo 需另開 PR」**的項目,當日即結案
(`AI-SOP-Protocol` PR #116,merge commit `5895b58`)。**零行為變更,只讓證據停止說謊。**

| 日期 | 對象 | 規則 | 處置 |
|------|------|------|------|
| 2026-08-27 | ASP `ADR-033:86` | 「hygiene error…無假陽性疑慮」 | **已更正。** 那是 hygiene error 被授權為唯一 auto-fail 的**理由**,已被 `superpowers-marketplace` 否證(純發佈清單 repo 拿到 H-001 error)。ADR 內加「事實更正 1」區塊:表的「擋」不變,**變的是那個授權理由不再成立**;日後要擴充 auto-fail 範圍不能再引用這一句。⚠️ 同時把我自己記錯的一處寫進去:**gate 曝險實測為零**(`pipeline.md` 的守衛是 `changed_files MATCHES "**/SKILL.md"`,`skill_md_count == 0` 的 repo 不可能觸發),真正的傷害是輸出說錯話 |
| 2026-08-27 | ASP `ADR-033:162` / `:259` | 「已知假陽性不擋 → eval 案例實跑 → 已驗證 ✅」 | **已更正。** 那個 ✅ 是**空過的**:eval 斷言 `blocks(d) is False`,而 `blocks()` 只看 hygiene,對任何沒有 hygiene error 的 repo 恆為真 —— 即使 S-001 完全不再被偵測到照樣綠。ADR 內加「事實更正 2」區塊並附 `blocks()` 原始碼。**結論(已知假陽性不擋)仍成立**,改的是「憑什麼說已驗證」;本 repo 側的 `c_security_field_matches_lint` 已讓它真的可轉紅 |

### 第二次批次(2026-08-27,11 條)

處置分佈:**7 條動手、4 條刻意不修**;另 2 條的第二半移入「待測」、4 條新登記。
查證與突變驗證全文見 [`misjudgment-batch-2026-08-27.md`](misjudgment-batch-2026-08-27.md)。

| 日期 | 對象 | 規則 | 處置 |
|------|------|------|------|
| 2026-08-27 | 本 repo | `evals.json` 無法表達「複核為假陽性」 | **已修(最優先)。** `security` 改為物件陣列 `{id, flag, review, source}`,`review` **必填**(避免 `bool(None)` 型的靜默預設,CHANGELOG 1.3.1 才修過同型)。新增兩條斷言:(a) 同一份 lint 輸出、`review` 不同 → verdict 不同;(b) **凡標了 `security`,lint 必須真的在該 repo 命中該 flag**。severity 查 `lint_skill.SECURITY_RULES`,不在 evals 再編一次(ADR-031)。**新增 fixture 驅動**——`research/repos/` 是 gitignored,只跑在真實 repo 上的斷言在 CI 會 skip,那等於用 skip 換一個「已驗證」的錯覺。5 個突變全數轉紅 |
| 2026-08-27 | 本 repo | H-002 未實作 | **已修:`severity: error → info`、`check_type: script → llm`,並加 `implementation_status` 註明未實作**(rubric 3.1.0)。降級是讓條文停止說謊,不是放寬——它從來沒有生效過。後半移入「待測」(實作會擊中 `anthropics/skills`)。同步修 `lint_skill.py` 那行說謊的註解(`# H-001/002/003/004 hygiene 門檻`)|
| 2026-08-27 | 本 repo | differentiator 條數 5 vs 6 | **已修 4 處**(`research/rubric.yaml:10` + 出貨副本 + `CLAUDE.md` + `review-plugin-marketplaces-2026-08-27.md`),句末加降級來歷註。是**過期敘述不是錯字**:`fm_license_any` 依 G3-Q1 降 observation-only,而定稿檔搬的是裁決**前**的原句。⚠️ **`G3-review-notes.md:15` 刻意不動** —— 那是裁決前的獨立覆核紀錄,當時為真,改它等於竄改稽核軌跡 |
| 2026-08-27 | 本 repo | `signal_type: craft` 名實不符 | **只改 `dir_examples` craft → packaging**(weight 2 未觸 cap 3,**總分 `/14` 與 verdict 零變更**;⚠️ 但**子分數的分子與分母都會動** —— 凡 `dir_examples` 命中的 repo,2 分由 craft 搬到 packaging,`anthropics__skills` 的 craft script 子分數由 2/6 掉到 0/4。我先寫「分數零變更」、補記時又只說「分母變了」,兩次都低估,由獨立複審 F4 指出),並給 R-001/R-004/R-005 加 `measurement_note` 說明實際量法。這讓 `README.md:154`「5 條有 4 條是 packaging/marketing」第一次真的成立。**順帶修一個更嚴重的**:drift-guard 原本 `for feat, w, _sig in ...` **刻意丟棄 signal**,於是 signal 漂移完全無守衛——已納入比對。❌ **不改 `has_tests_or_evals`**:weight 4→3 會讓 51/80 repo 的分數改變、84 處硬寫的 `/14`(18 個檔案)全部過期,與「5 vs 6」完全同型的缺陷,代價與收益不成比例 |
| 2026-08-27 | `superpowers-marketplace` | H-001 對純發佈清單 repo | **已修,但不改 H-001。** 依紀律 2,條文說「存在 ≥1 個合規 SKILL.md」而該 repo 確實沒有——**條文為真**,缺的是 SKILL.md **步驟 3 形狀表少一列**。已加「純發佈清單型」列 + 修步驟 2 的「不必往下」(否則執行者根本走不到步驟 3)+ H-001 加 `scope_note`。⚠️ **我記錄的「下游後果:擋 gate」不成立**:`pipeline.md:327` 的守衛是 `changed_files MATCHES "**/SKILL.md"`,一個 `skill_md_count == 0` 的 repo 不可能觸發。真正的傷害是**輸出說錯話**,不是擋 gate |
| 2026-08-27 | 本 repo | `REDFLAG_OBEY_OUTPUT` 極性盲區 | **已修:刪掉 `without\s+(?:stopping\s+for\s+)?confirmation` 那一支。** 實測(現存 5 repo / 804 檔)該支 **2 命中、0 真陽性**,而它想抓的語意已由 `don'?t\s+stop\s+for\s+confirmation` 覆蓋(memU `SKILL.md:78` 正是靠那支)——**降假陽性而不降召回**。新增 `OBEY_KNOWN_UNCOVERED` 常數 + 兩條召回斷言。實測結果:`Jeffallan` 的 S-001 消失(唯一命中是假陽性),memU 保留。❌ 不移植三條件共現(理由見本檔導言的勘誤段)|
| 2026-08-27 | 本 repo | `REDFLAG_CRED_ARGV` 環境前綴形式 | **不補樣式,改加 `CRED_KNOWN_UNCOVERED` 常數**(比照既有的 `DEFENSE_KNOWN_UNCOVERED`),selftest 斷言「目前不命中」。缺口變成可見、可轉紅,而不用付假陽性的帳。⚠️ **我的原記錄有兩處事實錯誤**:(1)「金鑰明文進 argv、`ps` 可見」——`VAR=value cmd` 的 shell 賦值**不進 `cmd` 的 argv**,本例可見是因為前面有 `env -i`,使它成了 **`env` 自己的 argv**;照原描述去抓 `VAR=value cmd` 抓的是錯的形狀。(2) 值是 `<the key>` **佔位符**。第二半移入「待測」|
| 2026-08-27 | `Jeffallan` | R-004 `has_tests_or_evals` | 🚫 **查證後刻意不修 —— rubric 判對、我錯(本專案第三次)。** 實查 `validate-skills.py` 的 24 個 checker class(`YamlChecker`/`NameFormatChecker`/`SectionOrderChecker`/`LineCountChecker`…)**全部是格式/結構/交叉引用檢查,沒有一個測 skill 行為**;它自己的 docstring 寫「Validates skill **structure**」。決定性先例:`review-published-repos.md:44` —— 同一批審查者、同一天、同一張表,對「有 CI 但只驗結構不驗內容」明確判**真缺口**,對 `dir_examples` 判假陰性,**他們早就把這兩種情況分開了**。我那一列自己也預感到了(「放寬會讓『有任何驗證腳本』都算數」)。已改為在 R-004 的 `measurement_note` 與 SKILL.md 的「gap_list 不是照抄 lint」段落把這條讀法寫進條文 |
| 2026-08-27 | `addyosmani` | S-101 英文分支 | 🚫 **查證後刻意不修 —— 我描述的後果不存在。** `_defense_untrusted` 是 **repo 級布林**,addyosmani 已靠 `test-driven-development/SKILL.md:339` 的**真陽性**判 True,收窄英文分支**不改變它的任何判定**。且實測 29 repo 有真陽性損失(`claude-plugins-official` 的 5 處防禦條款因跨句被誤殺),`DEFENSE_CALIB_POS` 唯一的英文 POS 句也會讓 selftest 轉紅。rubric 的 `confidence_rationale` 早已替這件事結案(明寫英文的 `accepts untrusted data` 與中文那個破口「完全同型」)——**它是「待測」段 2026-08-26 S-101 那列的一個實例,不是新問題** |
| 2026-08-27 | `rust-skills` | R-005 `✅/❌` 分支 | 🚫 **不修 regex、不降級,只補 `measurement_note`。** ⚠️ **我原本寫「血統裁定可能意味著該降級」,那是第二次犯同一個已具名記錄的錯**:`directive-polarity.md:114-115` 白紙黑字排除了這個外推(「本節量的是 `❌/✅` 在 **SKILL.md** 上的分佈…**不**適用於 R-005」),而 §7 的**修正 23** 就是這一條——上次我據血統集中推論 R-005 也在偵測血統,查 `feature_matrix.json`(早就在版控裡)80 repo 31 True、obra 系 1/2、**P=0.63 零集中**,已自行否證。另兩處要更正:`❌→✅` 與 `✅→❌` **兩支都中同一張表,只修一支無效**;`NevaMind-AI__memU` 是**第二個**假陽性實例。降級會動 `maxscore=14`,讓所有歷史 packaging 分數不可比,而 tier 門檻是照 14 分校準的 |
| 2026-08-27 | `claude-plugins-official` | S-003 `self_update` 命中 hooks 內的註解 | 🚫 **查證後刻意不修。** 它已由 `confidence: low-static-needs-llm` 正確標記、步驟 5 如設計攔下,**工具沒壞,是收窄的校準面漏了一種內容型態**(校準時想的是散文,沒人想過 `hooks/` 裡放的是程式碼,而程式碼裡談論 git 指令完全正當)。剝除註解要對每種語言各寫一套,換到的是一個 **warning 級**訊號的精確度。已把該形狀寫進 rubric S-003 的 `known_false_positives`,讓步驟 5 的複核者查得到 |
