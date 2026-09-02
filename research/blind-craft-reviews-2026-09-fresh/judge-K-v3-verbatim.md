# 判讀者 K — 第三次產出(逐字;與已確認「定稿」的 v1 實質分歧)

> 呼叫端註:時序——v1(完整判讀)→ 呼叫端催收 → v2(確認「定稿,內容不變」)→
> **v3(本檔:agent 恢復後整個重判,較 v1 深一層)**。v3 的四組載重錨經逐字驗證
> **全部屬實**(CISO Never 清單撕斷+重複、CFO Tooling 裸廠商斷言、法規時限句、
> CE anti-padding),其中兩處 v1 與作者判讀皆未讀到。勘誤與裁決見
> `../review-fresh-wave-2026-09.md` 勘誤節。教訓:**催收確認過的「定稿」仍非終局**。

---

All materials read: criteria.yaml, shapes.md, and the six corpus files. `rubric-masked/` and `mask-sample.json` were not opened. Judging now, per procedure.

```yaml
judge: K
material_boundary: >-
  只讀 fresh-blind/ 內 criteria.yaml、shapes.md、skills/ 六份;rubric-masked/ 與
  mask-sample.json 未開啟;未上網;未讀目錄外任何檔案。
supply_chain: >-
  六份語料內無指向審查者的指令注入。nie 檔的「调用本 skill 时必须做的」等指令是給
  載入該 skill 的執行模型的正常內容,視為資料,未照做。

objects:

  # ========== 對象 1:headcount__*(同一集合 repo 的 5 份抽樣) ==========
  - id: headcount__collection
    scope_note: 一切判定是對「抽樣所見」(5 份 chief)的判定,不是對整個 repo 的斷言。
    shape: >-
      集合型(dispatcher/集合)——五樣本以 namespace 互引(finance:/people:/security:/legal-risk:),
      chief-executive 明示路由職能(「route a request to the right executive」);各樣本自身為
      規則密集 persona,依 shapes.md canned-phrase 列的括號排除(「規則密集的 persona/mode skill
      不落此列」),照 process/rule 全套判。
    samples: [chief-executive, chief-financial-officer, chief-human-resources-officer,
              chief-information-security-officer, chief-legal-and-risk-officer]
    consistency_line: >-
      五樣本骨架高度一致(description 意圖列表 → Why this role exists → Remit → 原則節皆附 why →
      What this role owns → Escalation → Never → Return contract);變異點:CISO 的 Return contract
      缺「If any section is empty, say so rather than padding it」條款、其 Never 列表有編輯損壞、
      無 Works with 節;CFO 獨有 Tooling 節(抽樣中唯一實質易腐面);CE 獨任升級端點。

    dims:
      L-001:
        value: good
        evidence: >-
          五份 description 皆為情境化意圖列表且帶領域限定詞——CE:3「Use this when a decision spans
          more than one function」;CFO:3「build or challenge a budget…assess unit economics or
          runway」;CHRO:3「diagnose why a team is underperforming for non-technical reasons」
          (自帶負向限定);CISO:3「a security strategy or program decision…risk that needs a
          verdict」;CLRO:3「review a contract or commitment, assess regulatory or privacy
          exposure」。無裸通用詞觸發;抽 3 片語各對應不同 body 節(CFO:budget→forecast 節、
          controls→controls 節、runway→cash 節),非同義簇灌水。
        aggregation: 五樣本皆 good、無樣本間不一致 → good。
        two_readings:
          - where: chief-executive description 的「when a plan needs pressure-testing before commitment」
            reading_A: 子句放整條 description 語境讀(全句組織級口吻、前後皆跨職能決策情境)→ 非收編。
            reading_B: 子句孤立讀是裸的通用意圖(泛「幫我壓測計畫」多數情境不是在要 CEO persona)→ 收編、mixed 起判。
            chosen: A
            why: evaluation_surface 說評的是 description 這個「模型做觸發抉擇時的唯一輸入」——輸入單位是整條而非孤立子句;intent_capture 的判別對象是「裸通用動詞/名詞」,此為受語境約束的情境子句。
        findings_no_value_change:
          - 五份皆無 NOT-for 負向觸發(高分項缺席,依 craft_value_mapping 不影響取值)。
          - CISO「deciding whether to accept or block a risk」與 CLRO「decide whether a risk should be accepted, mitigated, or refused」觸發面有重疊;由 CE 的路由子句與雙方 Escalation 節仲裁,記觸發面 finding(主維歸 L-001)。

      L-002:
        value: mixed
        evidence: >-
          四份基礎全達且厚:CE:44-46 對照例「"We are not pursuing enterprise until the mid-market
          motion repeats" is a priority. "Enterprise is a lower priority" is a wish.」+ 62-67 例外節
          (何時打破:reviewer-class finding、recurring conflict);CFO:78-80「"Not at this
          conversion rate" is a negotiation…"it's not in the budget" is a wall they will route
          around」;CHRO:57-59「defensible when explained out loud survives that; one built from
          individual negotiations does not」;CLRO:46-54 兩段式回答規則+why(「keeps the function
          consulted early」)。CISO 好例亦在(53-55「"This is not secure" leaves the team
          guessing…"this ships when the credential is rotated…" is a task someone can finish
          today」),但其 Never 列表(113-122)有結構損壞:115「Treat a passed audit as evidence of
          security. Audits test whether controls exist as documented,」句子中斷,殘句「which is a
          different question from whether they work.」擱淺在 120 行、掛在無關條目「Do not fix another
          team's finding…」之下;且 117「Do not block without stating exactly what unblocks it」與
          121「Block without saying what would unblock…」同一規則重複兩見。
        aggregation: >-
          移植 L-004 聚合邏輯:基礎達成的樣本間不一致(4 份乾淨 good、1 份約束清單內有傷及
          「規則附因果理由」的損壞)→ mixed。單一樣本驅動,其餘四份 why 密度與對照例水準一致地高。
        two_readings:
          - where: chief-information-security-officer 的 Never 列表損壞
            reading_A: 各規則的 why 與對照例在 body 節完整存在,清單損壞屬排版/編輯事故 → 記 findings、樣本仍 good。
            reading_B: Never 清單是 persona skill 執行者最直接消費的核心約束面;一條規則的因果子句在原位被撕斷、殘句錯掛他條、另一條重複——是落在核心規則區、傷及「規則附因果理由」呈現的可指認瑕疵 → 樣本 mixed。
            chosen: B
            why: mixed_boundary 的位置原則(核心規則/讀者最常走的路徑 → 傷及基礎;邊角 → findings)——約束清單非邊角;此非 nitpick 級措辭問題,是兩個條目「照字面讀即壞」。
        findings_no_value_change:
          - CISO Never 列表極性混排(前三條裸動詞承 Never、後三條 Do not)——外觀問題。
          - 各樣本 Never 條目皆為 body 已解釋規則的摘要,非裸 MUST 堆疊(CE:131-136 六條皆可回溯至對應節)。

      L-003:
        value: good
        evidence: >-
          每樣本單一 job(一個高管職能)+ 顯式 Remit/Owns/Escalation 邊界,且互相路由:CE:127
          「Nothing — this is the escalation endpoint」+ 131「delegate to the responsible chief」;
          CFO:65-66「See `finance:internal-controls-and-audit` for the design and
          `security:access-and-identity` for the system permissions」+ 92 雙向升級條件;CHRO:68-69
          「See `people:compensation-and-leveling`…and `people:performance-management`…」;CISO:
          88-89「See `security:incident-response` for the mechanics and
          `legal-risk:privacy-and-data-protection` for the obligations themselves」;CLRO:67
          「See `legal-risk:enterprise-risk` for the register itself」。集合型「路由治理」的
          pass_criteria(dispatcher 或互相路由)兩者兼備:CE 是 dispatcher,五份的
          Escalation/See-X-for-Y 是 When-to-Pivot 等價形式。
        aggregation: 五樣本皆 good、無不一致 → good。L-003 依集合型例外不因 scope 廣扣分(未觸發——各樣本 scope 本就單一)。
        findings_no_value_change:
          - namespace 引用標的(子 skill)在抽樣之外,可解析性在本材料邊界內不可驗;判的是如寫之設計。

      L-004:
        value: mixed
        evidence: 見逐樣本序;聚合理由見 aggregation。
        per_sample_decision_order:
          chief-executive:
            order: 1
            value: good
            evidence: >-
              機制:Return contract 的聲明紀律——153「If any section is empty, say so rather than
              padding it」+ 必填「Assumptions — what must hold for this to be right」「What would
              change my mind — the specific evidence that would reverse this」(148-151),對本 skill
              自身產出有攔截力;內文掃無載重宣稱(全篇為管理方法論/結構邏輯,無外部可過期事實),
              序 1 的「內文無載重宣稱時此條件空缺為真」成立。強弱註記:弱檔形式(聲明紀律),
              非 dated snapshot。
          chief-financial-officer:
            order: 2
            value: mixed
            bare_list:
              - "96-100 Tooling 節:廠商×市場分層斷言(「QuickBooks or Xero at small scale, NetSuite, Sage Intacct, or Dynamics 365 in the middle, SAP or Oracle at the top」及 planning/close/payments/cap-table 四層清單)——未附時效、未入機制覆蓋,讀者會據以選型,屬日期敏感市場資料。"
              - "60-61 次要:「The most common real-world loss is not sophisticated fraud. It is a convincing email asking for a payment redirection」——未附引用的經驗頻率斷言(其後的結構機理「succeeds when one person can both authorize and pay」不易腐)。"
            note: 機制同 CE(聲明紀律,119-128),但 Tooling 斷言在覆蓋外裸露 → 序 2。
          chief-human-resources-officer:
            order: 1
            value: good
            evidence: >-
              機制同 CE(112-121,含 121 anti-padding 條款);內文刻意停在結構層(「through pay
              transparency law」「disclosure obligations」皆無具名法規/門檻/日期),掃無具體載重
              宣稱 → 序 1 空缺為真。
          chief-information-security-officer:
            order: "5(殘餘性裸露)"
            value: mixed
            bare_list:
              - "79「Several regimes require notice within days, and some sectors far faster」——未附引用的法規時限斷言。"
              - "110「breach notification in particular runs on statutory clocks measured in hours」——同類,更具體。"
            note: >-
              序 1/2 不成立:其 Return contract(124-131)缺 anti-padding 條款,「Likelihood, with the
              reasoning rather than a number alone」薄於 statement_test 最低構成,判無機制。
              序 3 未採計:88-89 把 obligations 本體委給 `legal-risk:privacy-and-data-protection`
              而不複製,是正確的不抄寫設計,但標的是姊妹 prose skill,非 equivalent_forms 要求的
              「權威源或機械產物」。序 4 不成立(載重宣稱存在)→ 序 5;刪去兩處時限斷言,
              教學價值大體存續(僅一節失去動機錨)→ 殘餘分支 → mixed。
              讀法穩健性:即使採計 return contract 為機制(→序 2)或採計委託為同步形式(→序 3,
              細則取兩側較低者),取值皆為 mixed;讀法只動序號、不動值。
          chief-legal-and-risk-officer:
            order: 1
            value: good
            evidence: >-
              機制雙重:101「Never advise on jurisdiction-specific law without saying that qualified
              counsel is required」——乾淨的「不得直答、須聲明」條款,對象是本 skill 自身的法律
              主張(不依賴 return contract 讀法即成立);另有 Return contract 聲明紀律(121)。
              內文法理主張停在管轄中性的結構層(84-91 privilege 節),管轄敏感處由 101 條款覆蓋
              → 序 1。
        aggregation: >-
          依 collection_aggregation:機制存在性樣本間不一致(4 份有聲明式機制,CISO 無——其
          contract 整條缺 anti-padding 行,屬存在性差異而非位置/形式變異)+ 2/5 樣本有覆蓋外或
          殘餘裸露(CFO、CISO)→「部分覆蓋或樣本間不一致」→ mixed。
        two_readings:
          - where: 全集合——Return contract 是否過 statement_test
            reading_A: 「If any section is empty, say so rather than padding it」+ 強制 Assumptions/「What would change my mind」= 對自身產出的「須聲明、不得編造填格」攔截,屬證據先行/聲明紀律家族的弱形 → 是機制。
            reading_B: 例示的機制皆為「先查/先建證據再答」;return contract 只結構化輸出的誠實度,不攔截段內事實編造 → 非機制;則 CE/CHRO 落序 4(n/a)、CFO 落序 5(仍 mixed)、CLRO 憑 101 行獨立仍序 1(good)。
            chosen: A
            why: statement_test 自書最低構成是「對憑記憶編造有攔截力」且明示接納流程型等價形式;anti-padding 條款創造可指認的「不得直答、須聲明」情境,不落排除清單(它是可執行指令,非泛泛免責語)。兩讀之下聚合值皆 mixed(不一致性兩讀皆在),僅個別樣本在 good/n-a 間移動。

  # ========== 對象 2:nie-grassroots-logic(獨立判) ==========
  - id: nie-grassroots-logic
    shape: >-
      domain-lookup 型(知識查詢表、多子意圖:框架速查表 70-88、「何時讀哪個 reference」對照表
      114-129),附流程元素(決策樹、質量閘門);依 shapes.md 適用 L-001 片語例外與 L-002 表格認列。
      非集合型:routing 標的是同一 skill 的 references/,不是子 skill。
    dims:
      L-001:
        value: good
        evidence: >-
          description(3-16)為長情境列表。灌水判別法實測抽 3 片語:考公选岗→
          `power-and-positions.md`+life-decisions §2(118、136);土地财政→
          `development-dilemmas.md`(81、122);谁适合当村支书→`village-fit.md`(119)——三片語
          三目的地,屬多子意圖映射非同義簇;結尾具名/術語觸發(聂辉华、含权量)精確。
        two_readings:
          - where: 「高考志愿/选城读书」「买房与区域投资风险」「回哪养老」等生活意圖片語
            reading_A: 複合限定(选城/区域投资风险/回哪)+ 整條 description 濃厚的政經域錨定,泛生活求助不會被多數劫持;且個人抉擇是該 skill 明載的實際 job(life-decisions.md 五場景)→ 非收編。
            reading_B: 「高考志愿」單看是裸生活意圖,多數說這詞的使用者不是在要治理分析 → 收編、mixed 起判。
            chosen: A
            why: intent_capture 的單一提問以「該 skill 的實際 job」為準——城市/區位選擇正是其聲明並有專章承載的 job;判別單位取整條 description(觸發輸入)。片語騎在邊界上,記 finding。
        findings_no_value_change:
          - 無 NOT-for 負向觸發(高分項缺席,不影響取值)。
          - description 長達 14 行,密度極高;本次逐類抽測未見同義異寫,但維護時最易從此處開始灌水。
      L-002:
        value: good
        evidence: >-
          規則附因果與 do/don't 對照皆在:106「集权/分权要素不要混搭。集权配:监督、忠诚、一刀切、
          犬牙交错;分权配:激励、能力、多样化、山川形便」(參數化配對);107「十八大前后规律不同。
          勿用唯 GDP 锦标赛一套讲今天;要用政绩→问责、激励→监督」(反例+替代);33「别把县委书记
          简单画成「土皇帝」或「包青天」」(雙向反例);框架速查表每列「一句話」機制+「何时用」
          (equivalent_forms 認結構化表格);141-147 質量閘門是可證偽自檢清單。依查表型裁定,
          override 節缺席不擋 good;基礎(因果理由+等價替代)達成。
        findings_no_value_change:
          - 表列單元極簡(如「亲近(服务)+ 清白(可预期);不完全契约」),受查表型裁定保護;值得記的是它反而具備條文殘留限制段所期望的鑑別特徵——逐條目「何时用」欄。
      L-003:
        value: good
        evidence: >-
          單一 domain expertise(「用聂辉华原書框架分析基層中國」)的多切面;domain_lookup_scope
          判別法:解釋現象與個人抉擇會在同一任務鏈被同一人用到(五場景聯動表 133-139 明示
          场景→框架 reference 串接,如投资→`development-dilemmas.md`+`business-environment.md`),
          且決策樹 92-98 顯式分流「用户要解释还是要选?」——非 planning-with-files 式異 job 堆疊。
          內部路由治理:三层地图(48-52)+「何时读哪个 reference」14 檔映射表(114-129)+ INDEX.md
          總圖,dispatcher 級。
        findings_no_value_change:
          - 14 個 references/ 檔與 INDEX.md 不在本語料內,路由標的存在性不可驗;判的是如寫之設計。
      L-004:
        order: 1
        value: good
        evidence: >-
          序 1:機制存在且載重宣稱皆在覆蓋內。機制三重——44「**不确定的制度细节**标
          「[原书有述·具体现行规定请核最新文件]」;不假装掌握最新人事口径」(標注+改查協定);
          23「不编造原书没有的框架/数字/案例」與 108「**物证纪律。**框架名、命题、案例来自原书;
          数字与人事以原书/用户补充为准」(never-from-memory 條款);147 自檢閘門「没编原书没有的
          数据与制度细节」。覆蓋:領域主張全篇歸屬原書(scope_of_perishable:已附出處的主張
          不入易腐範圍),制度時效性由 44 行協定接住;references/ 相對路徑隨版控同步。
          強弱註記:中檔形式(never-from-memory+標注協定+自檢閘門),無 dated snapshot
          (無調研截止日)——記敘述強度,不動取值。
```

## rubric_friction

1. **集合聚合規則只存在於 L-004**(對象:headcount;維度:L-001/L-002/L-003)。任務與 shapes.md 都要求集合「四維合出一組值」,但 criteria 只在 L-004 寫了 collection_aggregation;其餘三維無聚合條文,我被迫移植 L-004 的「存在性不一致→mixed/形式變異→findings」邏輯。這直接決定了 L-002 聚合是 mixed 還是 good(4 好 1 壞的樣態在無條文下兩讀皆通)。

2. **「傷及基礎要件」對結構性文本損壞無裁定**(headcount/CISO;L-002)。mixed_boundary 只規範裸 MUST 劑量;「Never 清單內句子被撕斷+條目重複」究竟算 craft_value_mapping 的「排版——記 findings 不降值」還是「傷及『規則附因果理由』——降 mixed」,條文無判別法,我自選了位置原則的延伸讀法(約束清單=核心消費面)。此格是本次判讀最可能與他人分歧之處。

3. **statement_test 對「聲明式紀律」正反清單皆未列**(headcount;L-004)。「If any section is empty, say so rather than padding it」+強制 Assumptions/falsifier 欄,既不在「算」的例示(全是先查/先建證據型),也不在「不算」的例示(非泛泛免責、非來源標註)。此讀法翻轉 CE/CHRO 於序 1(good)與序 4(n/a)之間——取值實際換值域,不只換敘述。

4. **intent_capture 的判別單位不明**(headcount/CE、nie;L-001)。條文針對「裸通用動詞/名詞」,對「寬情境子句」(CE 的 pressure-testing 子句、nie 的「高考志愿/选城读书」)未說應孤立判還是放整條 description 語境判;兩讀給出不同值,我選整條語境判。

5. **equivalent_forms「指向單一事實源」未涵蓋集合內姊妹 skill**(headcount/CISO;L-004)。「See `legal-risk:privacy-and-data-protection` for the obligations themselves」是教科書級的「不抄寫、指向擁有者」設計,但標的卡在「權威源或機械產物」定義外(姊妹檔是 prose),序 3 採計與否無條文支撐;附帶地,部分覆蓋+部分裸露時「證據記走到第幾序」該記單序還是複合序,亦無記法規範(我記主走序+註明)。

6. **輕微**:L-001 pass_criteria 把「無 SEO 式關鍵字堆疊」語法上掛在高分子句內(「高分再具負向觸發且無…」),而 disambiguation 又把同義詞灌水寫成扣分項——堆疊究竟是基礎瑕疵還是高分阻斷項,極性有張力。本語料未觸發(兩對象皆無灌水),未影響取值。

## contamination

- **具名定錨:無**。criteria/shapes 的 20 餘個具名 evidence_refs(kangarooking、ga-methodology、blader/humanizer、planning-with-files…)無一是本語料;全文無 headcount、chief-*、聂辉华、基层 等字樣。
- **數字定錨:無**。條文內數字(~25 片語、11 行、35 pattern 等)皆繫於他 repo,與本語料無對應。
- **內容指紋:無直接指紋**。條文舉例(CLI 安裝路徑、index.html 的 CSS class、船舶檢驗)均不指向六份檔案。
- **語意共鳴(候選,材料邊界內不可證實)三處**:
  1. decision_order 自註「2026-09-02 依姊妹專案盲判驗證擴為五序」——與本次盲判**同日**;而新增序 1 的「內文無載重宣稱時此條件空缺為真——主動寫反編造條款是真實的 craft」所描述的組態(無易腐內容+自帶反編造條款),與 headcount 樣本(return contract 的 anti-padding 條款)逐點吻合,本次 3/5 樣本恰好走進這一支。
  2. 序 5 殘餘分支的舉例「一行工具推薦」與 CFO 唯一的裸露面(Tooling 節,廠商推薦)同型——若「姊妹專案」語料含本批或其同族檔案,則這兩處分支形同為本語料量身。
  3. scope_of_perishable 自註「2026-09-02 自 readme-reviewer 已驗證結構回灌」——同日修訂痕跡;標的名稱非本語料,列此僅供溯源。

---

判讀完成。交付摘要:兩對象、materials 全部限定在指定目錄內讀取,禁讀項未開啟。headcount 集合(5 樣本):L-001 good、L-002 mixed(單樣本驅動——CISO Never 清單編輯損壞)、L-003 good(全樣本互路由,集合型路由治理雙形式兼備)、L-004 mixed(逐樣本序 1/2/1/5/1;機制存在性 4:1 不一致+兩樣本裸露)。nie-grassroots-logic:四維全 good(L-004 走到序 1,never-from-memory+標注協定+自檢閘門)。四處關鍵格附了兩讀與選讀理由;friction 六條(最重的是集合聚合規則僅 L-004 有、statement_test 對聲明式紀律無裁定);contamination 無具名/數字定錨,但有三處與同日條文修訂的語意共鳴候選,已如實列出。
