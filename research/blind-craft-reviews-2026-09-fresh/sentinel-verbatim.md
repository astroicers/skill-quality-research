# 反匿名前哨(制度化首戰)— 定稿逐字

> 呼叫端註:前哨中途曾停頓吐出一份較淺的中途稿(LEAK 判定但實錘不同——
> 其 LEAK-1 為 L-003 條文兩讀,後在定稿重歸類為 friction/邊界案例;
> 該兩讀已由作者判讀與判讀者 K 獨立收斂,入 ledger)。以下為終局定稿,未經編輯。

---

攻擊完成。所有規劃的比對面都已掃過,以下是完整報告。

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
