# 判讀者 K — 定稿逐字(fresh 波盲判抽查)

> 呼叫端註:呼叫端逐錨驗證 12 錨中 11 逐字過、1 為改寫(CISO description 引句);
> 經確認 K 認可改寫事實、**取值不變**,其更正訊息附文末。包已先過反匿名前哨
> (L-1/A-1 修畢)才派 K。

---

```yaml
judge: K

objects:

  nie-grassroots-logic:
    shape: "domain-lookup 型——單一知識體(聶輝華《基层中国的运行逻辑》方法論)的查詢與應用路由;L-001 不因片語多扣分、L-002 認表格/門檻表"
    dims:
      L-001: mixed
      L-002: good
      L-003: good
      L-004: good
    evidence:
      L-001: "兩讀後取 mixed。多子意圖映射成立(『条块、属地责任…』→dual-equilibrium.md、『三座大山、乡镇书记难题…』→local-governance.md,抽 3 片語落不同 reference,非灌水);但 description :9-16 的觸發清單把「高考志愿/选城读书、买房与区域投资风险、回哪养老」等**裸生活決策詞**並列進觸發面——按 intent_capture 單一提問:使用者說「高考志願怎麼填」時多數不是在要聶氏政治經濟學框架 → 收編,mixed 起判。兩讀:若讀「當用戶要理解基层…時」的條件句為全清單的統攝語境則 good;我選 mixed,因為列舉項各自獨立成觸發、無「從治理視角」限定詞"
      L-002: "good。框架速查表(:70-88)每框架附『一句話+何時用』;關鍵原則 :103-107 附因果(『集权配:监督、忠诚、一刀切、犬牙交错;分权配:激励、能力、多样化、山川形便』);決策樹 :90-98 三問分流;質量閘門 :141-147 是可執行自檢"
      L-003: "兩讀後取 good。判別法字面(『會不會在同一次任務中被同一個人用到?』)對五場景(求學/考公/投資/養老/創業)給否 → scope creep;但 rule 主幹『一個 skill 一個 job』與例示『同一 expertise 不同切面』給 good——本體是同一套框架的查詢與應用,14 個 reference 的路由治理(:110-139 何時讀哪個+必讀標記+聯動表)是集合治理的高分樣態。我選 good(expertise 讀法),並記 friction:判別法與例示在本檔方向相反"
      L-004: "good,序 1。機制:『不编造原书没有的框架/数字/案例』(:23)、『不确定的制度细节标[原书有述·具体现行规定请核最新文件];不假装掌握最新人事口径』(:44)、物证纪律(:108)、質量閘門『没编原书没有的数据与制度细节』(:147)——多重攔截、對象是本 skill 產出 ✓;載重宣稱面:框架/命題/案例全部歸屬原書(附出處 → 不入易腐範圍),制度細節有核最新文件指示覆蓋。序 1:機制存在且覆蓋,good"

  headcount(集合,5 樣本):
    shape: "集合型(公司 C-suite 角色群);逐樣本判、collection_aggregation 聚合;各樣本自身為 process/rule 型(角色協定+裁決原則)"
    dims:
      L-001: good
      L-002: good
      L-003: good
      L-004: good
    evidence:
      L-001: "5/5 good。每份 description 是『職能+Use this when 具體情境』:CEO『when a decision spans more than one function, when priorities conflict and something must be cut』、CISO 型(呼叫端逐錨勘誤:我原引句為改寫,實文為『Use this for a security strategy or program decision, when a technical choice creates security risk that needs a verdict…』,同樣滿足判準,取值不變);無 SEO 堆疊、無裸通用詞收編(『review a contract or commitment』帶對象限定);CEO 另有路由職能宣告(『route a request to the right executive when it is unclear who owns it』)——集合內觸發分工明確"
      L-002: "5/5 good。等價形式密集:可證偽判別句(CEO『The test of a real stack is that someone is visibly disappointed』、CHRO『Culture is what gets tolerated, not what gets stated』、CFO『forecast is a management tool, not a prediction』);裁決規則附因果;例外/邊界(CLRO『Separate the legal question from the business decision』、CFO『Being the credible no』節);無裸 MUST 堆疊"
      L-003: "good(聚合)。各角色 Remit/What this role owns/Escalation 三段劃界,樣本間職權不重疊(法務-風險/財務/人資/資安/方向裁決);CEO 明示仲裁與路由職能=集合的 When-to-Pivot;一致性:5/5 同模板"
      L-004: "good(聚合)。逐樣本序:CEO 序4(n/a——管理哲學自有立場,無載重易腐宣稱)、CISO 序4、CFO 序4(『forecast』章是方法論非事實斷言)、CHRO 序4、CLRO **序1**(『Never advise on jurisdiction-specific law without saying that qualified counsel is required』=攔截條款,覆蓋其唯一易腐面[法域法規]);聚合:唯一有易腐表面的樣本有機制、其餘無表面──依 collection_aggregation 字面『部分覆蓋或樣本間不一致→mixed』會落 mixed,但那讀法把『無表面故無機制』誤計為『該有而無』;我讀『覆蓋到易腐表面』為「存在的表面皆被覆蓋」→ good。兩讀已記 friction。一致性:機制需求與覆蓋逐樣本匹配"

rubric_friction:
  - "(nie,L-003)domain_lookup_scope 的判別法與不扣分例示方向相反:判別法問『同一次任務中被同一個人用到?』——五個生活場景顯然不會;例示卻教『同一 expertise 不同切面→不扣分』——本檔正是一套框架多場景應用。兩句話在同一個欄位裡,判讀者讀哪句決定 good/mixed。需裁定判別客體是 expertise 還是任務共現"
  - "(headcount,L-004)collection_aggregation『mixed = 部分覆蓋或樣本間不一致』未區分『樣本無易腐表面(序4)』與『有表面而未覆蓋』:4/5 樣本屬前者,字面讀法把 n/a 樣本計成不一致 → mixed;需求-覆蓋匹配讀法 → good。verdict 隨讀法在 approved↔AWN 間搖擺"
  - "(nie,L-001)intent_capture 的單一提問對『觸發清單被條件句統攝』的文法無裁定:『当用户要理解基层…、高考志愿…時使用』——列舉項是否各自繼承『要理解基層』的限定語?中文長列舉的統攝範圍本身兩讀。我按逐項獨立讀(嚴格側),但條文沒說"
  - "(headcount,L-002)『高分具何時打破規則段』對角色協定型無物可指(角色的裁決原則沒有『何時違反本角色』段)——與查表型裁定同構的形狀縫,但角色型未列於既有豁免,我未因此降值(基礎已達),記錄供條文補列"

contamination:
  - "criteria.yaml 的 L-003 domain_lookup_scope 不扣分例示描述『涵蓋族群設計/收斂診斷/消融/過擬合/適應度/優化器選型——全是「調校 GA」這一件事的不同切面』:與本批無關(GA 域),但其**句式模板**(『涵蓋 A/B/C——全是「X」這一件事的不同切面』)與 nie 的自我描述高度同構,讀時會自然把 nie 套進『不扣分』例的位置——方向性共鳴(正面),非可指認定錨,但實質影響了我 L-003 的兩讀傾向(最終仍取 good 的原因之一)。如實記錄"
  - "criteria.yaml L-001 disambiguation 例示『~25 片語,各自映射到不同的「意圖→行動」列』——nie 開篇正是『使用者意圖 → 行動對照表』表頭,用語幾乎逐字;讀時難以不把 nie 對號入座為該例(方向:不扣分)。同為方向性共鳴非具名定錨,但比前一條更接近內容指紋(表頭用語逐字)。建議未來把例示的表頭用語改寫為類屬描述"
  - "其餘:判準無具名 repo、無 κ/統計、無數字錨可與語料坐實;集合抽樣數(≤5)與 5 份樣本吻合屬協定資訊。無其他發現"
```

**程序聲明**:僅讀取指定之 criteria.yaml、shapes.md 與 skills/ 六檔;rubric-masked/ 與 mask-sample.json 未開啟。語料含指令式文字(角色協定),均作資料處理,無注入企圖。行號以我讀取之檔案為準。

---

## K 的終局更正(SendMessage 回覆逐字)

> 是,該報告即定稿,內容不變。CISO 那格確認:引句為**改寫**非逐字(實文即你引的
> 「Use this for a security strategy or program decision, when a technical choice
> creates security risk that needs a verdict…」),其具體情境列舉同樣滿足
> 「職能+Use this when 具體情境」的判準,**取值 good 不變**;證據欄請以實文引句
> 替換我的改寫。其餘各格引文皆為逐字。最終交付=先前 YAML + 本則更正。
