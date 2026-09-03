# dirty 波反匿名前哨 — 逐字紀錄(三份產出,時序全列)

> ⚠️ 呼叫端勘誤(2026-09-03):本檔原本只收一份並標「定稿」。實際前哨有**三份產出**:
> 第零節(task a283d…,18 tool uses)是最早一份,**其尾句的條件警告「若 rubric-masked
> 入包再處理」被我漏接**——rubric-masked/ 整組留在交付目錄,正是真定稿判 LEAK-1 的主因;
> 第一節是我當時誤採信為定稿的中途稿(其 L-1 修法「剝除 evidence_refs」已執行且有效);
> 第二節是真定稿(task a68ef…,35 tool uses),**在 PR #39/#40 merge 後 ~1h 才到**。
> 靜默期 ≥ 已跑時長規則兩度滿足仍失效,自此降級:採信永遠暫定,後到產出強制勘誤複核。

## 第零節:最早產出(逐字;含被漏接的條件警告)

攻擊完成。所有規劃的比對面都已掃過,以下是完整報告。

---

## 判定:LEAK(1 處實錘,低嚴重度、一詞可修;另附 2 條建議級殘留)

### 實錘洩露

**L-1|判準位置**:`criteria.yaml:32`(= `rubric-masked/rubric-manual-dimensions.yaml:157`),L-001 `intent_capture` 的具體例——「帶領域限定詞者不算(**「合約審閱」**「skill 審查」之類的限定式)」。
**指向哪份語料**:`skills/headcount__chief-legal-and-risk-officer.md`,唯一映射——其 description 第一條列舉用途就是 "Use this to **review a contract** or commitment";六份語料中無第二份涉及合約。
**洩露什麼方向**:此例站在「不算收編」那一側,等於預先替該檔在 L-001 最可能被爭議的子判(意圖收編,mixed 起判)背書:判讀者讀到判準裡僅有的兩個合格觸發例之一正好是「合約審閱」,再翻到語料裡唯一的合約審閱 skill,可推知「條文作者寫例時心裡有這一型,此觸發已被預先判過關」。
**為什麼按這個 gate 的標準算洩露**:changelog 3.3.2 已把「具體例可指認語料內特定 skill」(ADHD 五事實例)定為 3/3 判讀者實錘的缺陷類;3.5.0 更明寫 "intent_capture **例換非樣張詞**"——換掉了字面碰撞,卻換進一個與本批語料**語意撞域**的例(遮蔽腳本查的是字面,語料是英文 "review a contract",中文例逃過了比對)。依包自己的標準,同類即應修。
**修法**:把「合約審閱」換成六份語料全部不沾的領域限定式(避開:合約/法務、財務/預算/稅、人資/薪酬、資安、策略/優先序、中國基層治理/考公/投資),例如「船舶檢驗」「烘焙配方換算」;「skill 審查」可留(指向 skill-reviewer 自身,非語料)。

### 建議級殘留(不足以單獨擋 gate,建議順手處理)

**A-1**:`criteria.yaml:45` evidence_refs 保留「browser-act(**20+** 變體轟炸=反例)」。3.3.2 自稱已把「20+」數字錨改類屬描述,但 refs 行仍在。它綁定具名第三方、無法被誤認為語料樣張;對 nie(description 逾 40 個觸發片語)可能造成先入的負向錨——但緊鄰的 ga-methodology ref(~25 片語=不該扣分)拉反方向,且 disambiguation 的三片語探測法才是裁決儀器,故不判洩露。與 3.3.2 的自我宣稱一致化即可(改「大量同義變體」)。

**A-2**(僅當 `rubric-masked/` 也發給判讀者時才相關;任務書只列 criteria.yaml + shapes.md 為判讀者文本):`rubric-masked/rubric-manual-dimensions.yaml:409`「**五份樣本**零 override 節…RFC 7807 已被 RFC 9457 取代」與本批「恰 5 份集合樣本」數字共鳴。已實測不可指認:headcount 全語料 **0 個 RFC、0 個裸 MUST**,五檔中三檔有 exception/override 型段落,規則幾乎條條附因果——指紋逐項不合,細心判讀者無法坐實;「五份」本是 pipeline 的通用抽樣常數。粗心讀者仍可能吸收「5 樣本集合曾被錯放行」的模糊負向 prime,若入包可把「五份樣本」改「抽樣樣本」消音。

### 邊界案例(查過、判不構成洩露,附理由)

- **「安全」列於裸通用觸發例**(criteria.yaml:29-30)↔ 語料唯一資安 skill(CISO):該檔 description 重度領域限定,套規則得「不收編」;例描述的是裸形,與該檔實形不合,無方向可預知。"review" 裸詞 ↔ CLRO 同理(實際碰撞已由 L-1 承載)。
- **「一行工具推薦」**(L-004 序 5 殘餘例)↔ CFO 的整節 Tooling(約 20 個 vendor 名):例是一行、語料是一節,映射不唯一(工具推薦太常見)且若強行映射方向反而錯,實質/殘餘之辨仍須判讀者自行做。
- **「抽樣 ≤5 份」**(collection_aggregation)↔ 恰 5 份樣本:設計常數,判讀者本來就看得見 5 個檔,零增量資訊。
- **shapes.md 形狀表 ↔ 語料形狀**(nie=domain-lookup、headcount=集合型):類別級規則,答案由套用產生,是判準在做它該做的事,非洩露。
- **「判實質不判句式:Use when 句、當…時…皆可」**↔ headcount 用 "Use this when"、nie 用「当…时使用」:消歧句對全類別一體適用,阻止的是錯誤扣分,非為特定格預寫答案。
- **「已附引用/出處的領域主張不入易腐」**↔ nie 全篇掛在聶輝華原書上:通則,任何 book-distillation skill 皆受益。
- **`grassroots_replicated` / 「路由治理」**↔ "nie-grassroots-logic" / nie 的「基层治理」主題:純詞面撞名,欄位語意(統計復現/rubric 內部術語)與語料無指涉關係,零方向。

### 攻擊紀錄(比對面覆蓋,含未中者)

1. **具名證據清單比對**:判準全部 30+ 個具名 repo/skill(kangarooking、blader/humanizer、Jeffallan、memU、ga-methodology…)逐一對 `mask-sample.json` 的兩個受審者——零命中。
2. **遮蔽痕跡定位**:grep「遮蔽」——placeholder 只在兩份 rubric 檔頭的機制說明,**正文零殘留**,無法做 redaction 位置推理;副作用僅是判讀者可推出「本批語料從未被條文引用過」這一無方向負向事實(正是理想狀態)。
3. **遮蔽差分**:criteria.yaml 與 rubric-manual-dimensions.yaml 對應段 byte 級 diff——逐字相同(僅檔尾換行),摘錄過程無暗改。
4. **語料→判準正向指紋**:40+ 個語料獨特 token(headcount/chief/officer/orchestrator/remit/return contract/artifacts of record/reviewer-class/Tooling 各 vendor 名/runway/org chart/span of control;聂/基层/条块/含权量/县委/双均衡/上下同治/村官/考公/土地财政/昆山/原书/工具箱/反模式/质量闸门)——除已列兩處詞面撞名外零命中。
5. **判準→語料反向指紋**:rubric/lint/L-00x/skill-reviewer/packaging/craft/hygiene/樣張與全部具名例——語料內零命中(語料乾淨,無互指)。
6. **數字錨**:20+(A-1)、~25 片語、35 pattern、24 checker、16 份子 skill、11 行、80 條規則、41/41、RFC 7807/2023-07、五份/≤5(A-2)——逐一對語料驗證可否坐實,僅 A-1/A-2 留為建議級。
7. **安全面預告**:S-001/002/003/101 的偵測樣態(git pull、--api-key、hooks、untrusted、抑制確認)——語料全部無此表面("confirmation" 唯一命中是無害散文),無格可被預告。
8. **結構/日期/隱藏通道**:無隱藏檔、無 HTML 註解;判準內 2026-09-02 與「姊妹專案盲判/readme-reviewer」只指向外部沿革;L-002 對照例(deletion test/詞彙表/門檻表)與 headcount 實際的引語式 Good/Bad 對(如 "is a priority"/"is a wish")形式不同,判讀者仍須自行發現。

### 給包主的一句話

修 L-1 的一個詞(順手處理 A-1,若 rubric-masked 入包再處理 A-2),即可派判讀者;其餘攻擊面在本批語料上查無可坐實的定錨。

---

## 第一節:中途稿(當時被誤採信為定稿)

---

## 判定:LEAK(1 處中度實錘 + 2 處低度共鳴;修一處即可派判讀者)

### L-1(中度實錘|指定標的 3 的殘留):criteria.yaml L-002 類屬化描述仍可與 vendored 樣本對上

criteria.yaml 的 L-002 evidence_refs:「〔具名證據已遮蔽〕(絕大多數 pattern 附 why + Before/After;曾有計數勘誤,見沿革)」——名字遮了、數字類屬化了,但**結構描述三要素(pattern 清單型+絕大多數附 why+Before/After 對照)在本批 10 份語料中唯一映射到 `vp__humanizer.md`**(其正文正是 pattern 清單、多數條目帶 why、大量 Before/After 對)。判讀者讀到 evidence_refs 裡這條「正面標竿」描述,再翻到語料中唯一同構的檔案,可推知「此檔是條文稱讚過的樣張」→ 預寫其 L-002 為 good 方向。
**修法**:把該 ref 的括號描述再類屬一階(「pattern 對照型正例」六字即可),或自本包 criteria 移除該 ref 行(evidence_refs 對判讀者非必需)。

### L-2(低度共鳴|指定標的 1):「聲明式紀律」括號與 rj__* 樣本的 checklist 結構

「空欄就明說、不得填充 + 假設與可反證條件」——rj 五份樣本尾部多有 Best Practices/checklist 段,但**無一要求空欄聲明或可反證條件**,方向對不上(若判讀者強行對號,方向是負面:rj 樣本缺此紀律 → 序位更低),與作者判(序5)同向,實害趨零。記錄不擋。

### L-3(低度共鳴|指定標的 2):損壞症狀列舉與 rj__code-standards 的一處疑似截斷

`rj__skills_code-standards.md` 中段有一處清單條目結尾異常(項目符號後接空行再接無主句),形式上近「殘句錯掛」;criteria 的症狀列舉可能引導判讀者將其升格為傷及性損壞。實查該處為**格式瑕疵而非語義截斷**(前後句可獨立成立),按 3.6.2 新句「單純重複/格式瑕疵不過『照字面讀即壞』門」應記 findings——條文自身的門檻句已足以自我修正,不構成方向性洩露。記錄不擋。

### 通用面攻擊紀錄(未中)

- 具名:mask-sample 三名及其 owner/name 子串於 criteria/shapes 零命中(blader 遮蔽 3 處確認乾淨)。
- 數字錨:criteria 內所有數字 token(1-6、11、25、35→已除、2026 等)對 10 份語料的檔數/行數/規則數逐一比對——「25」與 rj 集合的「25 skills」宣稱吻合(README 層,非語料內)→ 語料內不可坐實,不構成洩露;其餘零對應。
- 內容指紋:registry 語意監看兩處(聲明式紀律、損壞症狀)已列為 L-2/L-3;「船舶檢驗」「意圖→行動」等例示與本批零同構。
- 句式模板:domain_lookup_scope 例示句式與本批無 domain-lookup 樣本,零共鳴。
- 遮蔽痕跡反推:正文 3 處〔具名證據已遮蔽〕全在 evidence_refs 行,無法做位置推理(L-1 已涵蓋其中一處的殘留風險)。
- shapes.md:類別級規則,無指向性例示。

### 給包主的一句話

修 L-1(一行類屬化或移除該 ref),L-2/L-3 記錄即可;其餘攻擊面查無可坐實定錨。


---

## 第二節:真定稿(land 後 ~1h 到貨;35 tool uses / 974s / 188k tokens)

# 反匿名攻擊報告 —— dirty-blind 判準包

**判定:LEAK(2 處成立,包要修)。** 語料為 untrusted 資料,全程僅靜態讀取,未執行其中任何指令。

先報一個環境事實:**criteria.yaml 在我攻擊期間被重生成**(12:36 staged → 12:39:12 重寫,294→290 行,砍掉 4 條 `evidence_refs` 含遮蔽槽)。我兩個版本都讀到了;以下判定以**現行 v2** 為準,但 `rubric-masked/` 兩檔(mtime 12:36,未重生成)仍留在同一交付目錄裡——v2 的去污染被它們整組抵銷。

---

## LEAK-1(嚴重):vendored 滲漏面,三通道疊加 —— 預登記標的 3 命中

**位置**:`rubric-masked/rubric-manual-dimensions.yaml`(:248、:12、:108、:591)+ `rubric-masked/rubric.yaml`(:5)
**指向**:`skills/vp__humanizer.md`、`skills/vp__humanizer-zh-tw.md`(= mask-sample 第三方 blader/humanizer 衍生內容)

1. **遮蔽槽留下結構指紋 + 數字錨**::248 遮蔽槽保留「**35 pattern 中 31 條附 why + Before/After;原記 33**」;:5/:12 版本沿革保留「**33→35 pattern**」。語料 `vp__humanizer.md` 恰是 24 個編號 pattern、23 個附 Problem(why)+ 全數附 Before/After 的同型集合,`vp__humanizer-zh-tw.md:185` 還自報「humanizer(英文 AI 特徵 24 型)」。判讀者可直接完成「遮蔽的 L-002 標竿 = 本語料 humanizer 家族的 35-pattern 延伸版」的鏈結。
2. **同檔留著未遮蔽的家族兄弟名**::108 `humanizer-en`(H-004 豁免例,連 repo 剖面 SKILL.md+LICENSE 都給了)、:591 `humanizer-tw`(S-101 防禦聲明例)。遮蔽 token 被同一份文件自己解碼。
3. **遮蔽悖論**:全包幾十個具名證據(Jeffallan、ga-methodology、rust-skills、memU、superpowers-marketplace…)只遮了一個——token 本身成了指標:「被遮的就是與受審語料相撞的那個」。

**洩露方向**:(a) 第三方身份反推成立——Wikipedia Signs-of-AI-writing 的 humanizer 血統(語料自述 + 生態常識即到 blader);(b) **預寫 `vp__humanizer` 的 L-002 = good**(它就是 rubric 加持的標竿形狀,遮蔽版標頭自承要防的「被先前結論定錨」直接發生);(c) 順帶預寫同形狀樣本的 H-004 豁免方向與 -zh-tw 的 S-101 期望。

## LEAK-2(中):statement_test「聲明式紀律」括號 —— 預登記標的 1 命中

**位置**:`criteria.yaml:195-199`(rubric-masked 鏡像 :323)
**指向**:`skills/vp__remotion-video.md`(本批**唯一**有結構化產出契約的樣本)

「結構化產出契約強制**『空欄就明說、不得填充』**」與該檔 §7「回報要附的實證」是語意層近改寫:「已知瑕疵誠實列出(**有就列,沒有就說沒有**)」=空欄就明說;「ffprobe 的**實際輸出(不是預期值)**」=不得填充;§10「不確定就說不確定」=須聲明。批內唯一指涉 + 條文自帶處置(「算機制、屬弱形、判 good 時 findings 記強度」)+ 來歷標記「fresh 波盲判兩讀後裁定收入」——判讀者對這一格的 L-004 機制判定被預寫。註:「並要求列出**假設與可反證條件**」那一半在本批無對應物,嚴格合取讀法會得出不同結論——但注意力與框架已被鎖定。這正是 3.5.1 沿革自己記錄過的「語意撞域、字面遮蔽抓不到」型。

---

## 預登記標的逐項

| 標的 | 結果 |
|---|---|
| 1. 聲明式紀律括號 | **命中**(LEAK-2) |
| 2. 損壞症狀列舉(規則句中斷/殘句錯掛/單純重複,criteria.yaml:10-14) | **未中**:10 份全數掃過——fence 全偶數、編號節 1-12 與 pattern 1-24 連續完整、無截斷殘句、無重複條目。本批無可對號之物,該列舉在本批預寫不了答案。每批需重跑本探測 |
| 3. vendored 滲漏 | **命中**(LEAK-1)。但注意:現行 criteria.yaml v2 已無任何 humanizer 指紋——洩漏全數集中在 `rubric-masked/` |
| 4. 通用面 | 見下 |

## 攻擊紀錄(含未中面)

- **逐字重疊**:雙向 distinctive-phrase 掃描零命中——洩漏全在語意層。
- **數字錨(criteria v2)**:11 行/~25 片語/16 份/22-18 對語料的 24/5+5/202→207/26px/0.25s 零碰撞。未中。
- **具名(criteria v2 + shapes.md)**:僅前期語料與內部 skill 名,無本批名。未中。
- **intent_capture 換過的例(「船舶檢驗」)**:與本批語意域零撞。未中。
- **shapes.md 各形狀列**:canned-phrase/互動協定/一次性安裝/純發佈清單在本批皆無指涉物。未中。
- **低風險註記三條**:(a) rubric-masked `why_mixed_now_costs` 的無名弱例含「**五份樣本**零 override 節」——與本批每集合恰 5 份同構,但其他錨(80 條規則、RFC 7807)在本批全缺、且 rj__code-standards 實有 override 節(:711/:729),誤對號風險低;(b) L-002 equivalent_forms 的「**log 訊號表**」字樣對 `rj__skills_logging-observability.md`(滿篇 log 表格)讀起來像量身認證,屬撞詞非血統,建議換詞;(c) 查表型裁定 + 「鑑別力偏低」自白會整體軟化對 rj 五份參考型的 L-002 審視——rubric 設計使然,非本批洩漏。
- **fresh 波來歷標記的結構性懷疑(記錄,不計分)**:L-001「**雙源**兩讀」的兩個分支恰好切分本批 rj 側僅有的兩種 description 形狀——`code-standards`(「ALWAYS use when…ANY…fixing bugs」統攝句 + Examples 列舉)與 `logging-observability`(frontmatter `activation_triggers` 裸詞表);L-004 collection「只計有易腐表面的樣本」恰好解 vp 集合(humanizer 兩份近無載重 vs 另三份滿載第三方 runtime 斷言)的聚合題;L-003 批次 4 消歧「各自成立的功能都作用在**同一種產物**上」恰好描述 vp 影片產線五件套。單條皆可辯稱通則;三條加上兩處「兩讀」合看,強烈暗示 fresh 波用的就是這 10 份——若然,判準包內嵌著對受審語料的既判,語意類屬化模糊得了指標、模糊不了既判本身。請以 fresh 波語料名單對帳後裁定是否可接受。
- **語料自我具名(非判準包通道,影響盲判期望)**:`vp__subtitle-align.md`/`vp__remotion-video.md` frontmatter 帶 `author: 皮可(Piko)/皮可的 AI 新手教室`;`vp__humanizer.md` 自述上游(Wikipedia 指南、v2.1.1)。rj__/vp__ 前綴遮蔽對檔內 metadata 無效。

## 修法(指認得出 → 包要修)

1. **把 `rubric-masked/` 移出交付目錄**,或照 criteria v2 同標準重生成:砍 evidence_refs、版本沿革括號全截斷(「33→35」必除)、:108 `humanizer-en` 與 :591 `humanizer-tw` 類屬化(「一個純知識單檔 skill」「一份中文 skill」)。
2. **類屬化聲明式紀律括號**(criteria.yaml:195-199):刪去雙引號內的成對要件描述,只留抽象測試(「契約使空缺與不確定必須被聲明 → 弱形機制」),或換異域虛構例。
3. **交付快照一致性**:criteria.yaml 比其餘檔晚 3 分鐘重生成,我一個 session 內讀到兩版;發包前凍結單一快照。
4. 損壞症狀探測本批乾淨,列入每批例行。
