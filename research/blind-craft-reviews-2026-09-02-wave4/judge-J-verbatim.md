# 判讀者 J — 定稿(逐字轉錄,B2 終波 2026-09-02)

> 呼叫端註:J 於執行中途曾停頓一次並吐出一份**中途稿**(見
> `judge-J-draft-superseded.md`,錨大面積無法逐字驗證,已作廢)。
> 本檔為最終交付物;呼叫端對其約 20 個載重錨逐一抽驗**全數通過**。
> 以下為 J 的原文,未經編輯。

---

判讀完成。七份語料、判準與形狀表皆已讀畢(僅讀取指定之 criteria.yaml、shapes.md、skills/*.md;目錄內另有 rubric-masked/ 與 mask-sample.json,不在指定材料清單,未開啟)。以下為交付物全文。

```yaml
judge: J

objects:

  diagnose:
    shape: "process/rule 型——六個 Phase、硬性 gate 與決策點俱全,L-001~004 全套適用"
    dims:
      L-001: good
      L-002: good
      L-003: good
      L-004: good
    evidence:
      L-001: "描述含明確情境::3 'Use when user says \"diagnose this\" / \"debug this\", reports a bug… or describes a performance regression'——五個片語是同一 job 的自然說法,非同義簇灌水;無 NOT-for 僅屬高分項,不影響取值"
      L-002: "規則附因果(:14 為何 loop 是核心、:67 '單一假設會 anchor'、:95 淺 seam 給 false confidence);可證偽啟發式與對照(:71 假設須給預測、:73 'If you cannot state the prediction, the hypothesis is a vibe'、:41 '30-second flaky loop… 2-second deterministic loop');例外節(:8 'Skip phases only when explicitly justified'、:75 使用者 AFK 例外)"
      L-003: "單一 job(診斷迴圈)+ 顯式跨 skill 交棒::117 'hand off to the /improve-codebase-architecture skill with the specifics',並治理交棒時機('after the fix is in, not before')——知道邊界在哪的最強訊號"
      L-004: "序1:機制存在——證據先行協定(:49-51 建不出 loop 須 'Stop and say so explicitly. List what you tried'、'Do not proceed to hypothesise without a loop';:10 先查 glossary/ADR),過 statement_test(可指認情境:不得無 repro 直接給診斷);內文無載重易腐宣稱(:29 scripts/ 相對路徑=機械同步;Playwright/git bisect 為穩定生態指涉),序1 空缺為真。findings:機制屬協定型而非 dated snapshot,強度中(見 friction 1)"

  improve-codebase-architecture:
    shape: "process/rule 型——詞彙表+原則+三步流程,L-001~004 全套適用"
    dims:
      L-001: good
      L-002: good
      L-003: good
      L-004: good
    evidence:
      L-001: ":3 'Use when the user wants to improve architecture, find refactoring opportunities, consolidate tightly-coupled modules, or make a codebase more testable and AI-navigable'——四片語同 job 不同入口,語境具體無堆疊"
      L-002: "deletion test 可證偽啟發式(:25)+ 精確術語表(:14-21 Module/Interface/Depth/Seam/Adapter)+ 具體好壞對照(:56 'the Order intake module — not the FooBarHandler, and not the Order service')+ 例外規則附因果(:58 ADR 衝突僅在 friction 夠大時提出、:70 skip ephemeral/self-evident reasons)"
      L-003: "跨 skill DRY 與治理(:68 復用 ../grill-with-docs/CONTEXT-FORMAT.md、:70 ADR-FORMAT.md 不複製);邊界宣告(:29 'ADRs record decisions the skill should not re-litigate'、:60 'Do NOT propose interfaces yet');與 diagnose 互為交棒對端"
      L-004: "序1:機制存在——先查後行(:35 'Read the project's domain glossary and any ADRs in the area you're touching first')+ 不得憑自己推理重審已決事項(:29)+ 詞彙不得自造須取自 CONTEXT.md/LANGUAGE.md(:56);無覆蓋外載重易腐宣稱。findings::37 'Agent tool with subagent_type=Explore' 為宿主平台操作詞彙,裁定不算第三方事實斷言——嚴格字面讀法會落序2 mixed,見 friction 2"

  ga-methodology:
    shape: "domain-lookup 型——使用者意圖→行動對照表+知識查詢;依形狀表 L-001 不因片語多扣分、L-002 認表格/門檻表"
    dims:
      L-001: good
      L-002: good
      L-003: good
      L-004: n/a
    evidence:
      L-001: "抽樣片語映射不同段:「cache hit 一直很高」→:15/:83 收斂診斷表、「CMA-ES」→:364 替代優化器指南、「怎麼確認結果不是運氣」→:22/:259 Monte Carlo——多子意圖映射非灌水。findings:中英鏡像對與「Latin Hypercube/LHS 初始化」同義對屬觸達性重複,不傷基礎;description 無 'Use when' 句式,以問句情境等價達成(見 friction 4)"
      L-002: "門檻表密集(:16/:250-253 消融 Δ 解讀、:320-325 p-value 表、:79-85 log 訊號表)+ 規則附因果(:36-37 Pop 是廣度 Gen 是上限、:53 純隨機高維為何失效)+ 功能性 override 節(:358-381 何時不該用 GA)+ 適用限制與替代(:283-284 shuffle 對順序不敏感時失效,改 k-fold CV)"
      L-003: "族群設計/收斂診斷/消融/過擬合/適應度/優化器選型六子題同屬「調校 GA」一個 domain expertise,同一人同一調校任務會全部用到(domain_lookup_scope 判別法通過);意圖表 :10-24 僅路由 GA 調校意圖"
      L-004: "序4:機制不存在(全文無先查/勿憑記憶/時效條款;Monte Carlo、OOS、多 seed 是領域內容——驗證 GA 結果的方法,不是約束模型答題的機制);載重易腐宣稱缺席——穩定演算法領域,且 :116 明言 pseudocode 是「可跨語言實作的穩定參考」、不依賴外部庫。findings::381 'cma/deap/optuna 均有穩定實作' 是生態狀態殘餘指引,裁定非載重(方法論不依賴它成立);嚴格存在量詞讀法會落序5,見 friction 3。另 :364 'CMA-ES 收斂快 3-10 倍' 為未附引用量化理由,屬穩定演算法經驗值不易腐,記 findings 不入序"

  huashu-nuwa (collection, 入口+3 子 skill 抽樣):
    shape: "dispatcher/集合型——入口是「造 skill」的 process 管線兼路由(Phase 0B 掃描 .claude/skills/*-perspective/ 即插即用);三份子 skill 為 persona 化的 process/rule 型,規則密度極高,不適用 canned-phrase 之 L-002 N/A(該豁免保護的是簡潔,見 friction 7)。判定為對抽樣所見,非對整個 repo 的斷言"
    dims:
      L-001: good
      L-002: good
      L-003: good
      L-004: good
    evidence:
      L-001: "入口 :6-7 觸發詞映射三條不同路徑(蒸餾→Phase 0A、模糊需求→Phase 0B、更新→:566 更新章節);三份子 skill 全數具負向觸發(karpathy:10「不在用户只是普通问AI相关问题时触发」、musk:9、feynman:9),且長尾詞各映射具名心智模型(「march of nines」→模型四、「白痴指数」→模型1、「cargo cult」→啟發式1)——樣本一致,負向觸發為高分敘述不改值"
      L-002: "規則普遍附因果(入口 :441「没有这个段落…会凭训练语料编造」、:337 GIGO 在檢查點攔截的成本論證);對照例密集(:312 誠實 60 分 vs 編造 90 分;三份子 skill 皆有 Agentic 新舊模式對照例、反例黑名單全表附「为什么不要做」欄);例外節(:599-637 特殊场景變體表、:537 迭代上限 2 輪即交付)。findings:入口 :343 三重驗證第三項寫「自创术语」而 :353 執行步驟寫「排他性」,枚舉不一致,屬邊角不傷基礎要件"
      L-003: "集合路由治理:入口 :111 已有 skill 即插即用不重蒸(防重複)、:274-284 資訊獲取 skill 委派表(五個外部 skill 各附調用場景)、:144/:611 命名空間規約(-perspective/-framework);子 skill 各自單一 persona 且皆有「不擅长」邊界宣告(karpathy:29-33、musk:29-33、feynman:29-32);觸發詞無互撞(「第一性原理」僅 musk 認領,feynman 以 cargo cult/命名≠理解區隔)"
      L-004: "序1(四檔各判皆序1)→collection_aggregation good:機制為強形式——dated snapshot(karpathy:12/:18/:415、musk:364/:429、feynman:491 皆有調研截止日)+ never-from-memory 條款(三份子 skill 同文「宁可多搜一次,也不要凭训练语料编造」;入口 :591-595 绝不编造/不足时不强行生成)+ live-probe 協定與雙 CHECKPOINT(karpathy:110-114「不研究直接回答是否会…编造而打脸→强制走研究」)+ 編造黑名單(三份皆有「引用他还没说过的话」→「不知道就说没公开表态」)+ 時效盲區處置(karpathy:51)+ 來源分級與標註義務(入口 :224-227 一手>二手>推測、区分他说的/别人说的/我推断的);易腐表面(時間線、引語年份、案例數字如 $80/kWh、政治立場)皆被調研截止日與誠實邊界逐類覆蓋(musk 諏實邊界 :358 時間線不可信、:362 政治判斷可能已過時)。findings:入口 podcastnotes.org、Z-Library/LibGen 等生態指引為殘餘裸指,工具表以「如可用/主动扫描…如果有」承接"
    consistency: "高:三份子 skill 共用同一模板(STOP/EXIT 錨、三步協定+雙 CHECKPOINT、表達 DNA+中文適配表、9 列 fallback 樹、8 列反例黑名單、誠實邊界、調研截止),且 Step 2 研究維度確實依入口 :481-495 規則自各自心智模型推導(karpathy=benchmark/scaling、musk=BOM/白痴指數、feynman=實驗/類比/盲區),入口宣稱的生成規格與樣本實物逐節吻合。變異點:調研時間位置不一(frontmatter/正文/頁尾);入口 :437 規定的「创建者归属」尾註三份樣本皆缺;時間線表僅 karpathy 有(1/3);karpathy frontmatter 含非標準欄位(type、调研时间)——皆屬模板遵循度/打包層變異,不動 craft 維度值。另記:入口 :256 推薦 Z-Library/LibGen 屬供應鏈/合規疑慮,超出 L-001~004 範圍,僅登錄不計分"
```

## rubric_friction

1. **L-004 statement_test 的「機制」定義對流程型 skill 未裁定**(對象:diagnose、improve-codebase-architecture;維度 L-004)。例示全偏事實時效型(dated snapshot/stale-API/先查再答);「證據先行紀律」(不建 loop 不得假設、先讀 glossary/ADR)算不算機制,條文沒說。同一檔依這個自選讀法會落 good(序1)或 n/a(序4)——兩讀法都不產生缺陷,但取值不同,會影響下游上卷。我採「對憑記憶編造有攔截力即算」的寬讀,證據欄已標明機制形式。
2. **宿主平台操作詞彙 vs「第三方工具 runtime 行為斷言」無界線**(對象:improve-codebase-architecture;維度 L-004;波及 huashu 子 skill 的 WebSearch、diagnose 的 git bisect)。scope_of_perishable 字面可捕捉 `Agent tool with subagent_type=Explore`,但每個 agentic skill 都必須指名宿主工具,字面讀法使 L-004 對整類 skill 結構性不可達(與 L-002 查表型裁定要解除的缺陷同構)。我裁定操作詞彙不算易腐載重宣稱;嚴格讀者會給 improve 序2 mixed。條文應明示立場。
3. **序5 的存在量詞無 de-minimis 門檻**(對象:ga-methodology;維度 L-004)。單檔路徑寫「載重宣稱裸露→poor」,一行工具指引即可把無機制的穩定領域 skill 從 n/a 翻成 poor;collection_aggregation 卻有「大量…幾乎無」的量級梯度。我援引序1「非載重殘餘不改序」類推停在序4,這是外推不是條文。
4. **L-001 rule 講實質、pass_criteria 指定句式**(對象:ga-methodology、huashu 入口;維度 L-001)。「含明確觸發情境(Use when/當…時)」對觸發詞清單式 description(含問句情境如「Pop Gen 怎麼選」)無法字面滿足;我判句式非必要、實質等價即達標。
5. **L-001 disambiguation 判別法未處理「症狀片語與技法片語同落一段」**(對象:ga-methodology;維度 L-001)。「GA 第一代就 ramp」(症狀)與「LHS 初始化」(解法)觸發同一段,依「同段=灌水」字面會誤傷;實為不同使用者狀態通往同一目的地。需要「不同意圖、同目的地」的除外句。
6. **L-002 rule 與 pass_criteria 對 override 節位階矛盾**(對象:全部四個;維度 L-002)。rule 文把「含 override/例外節」列在基礎清單,pass_criteria 又把「何時打破規則」放高分。本批四對象皆有例外節故無取值影響,但缺席它的檔會因讀哪一句而 good/mixed 分歧。
7. **形狀表誘導對規則密集 persona 誤判 L-002 N/A**(對象:huashu 子 skill;維度 shape/L-002)。canned-phrase 列特徵寫「一句注入语或 persona」,三份子 skill 是 persona 但規則密度極高,判 N/A 會荒謬。該豁免的立法理由是「不得因簡潔扣分」,目的應寫進特徵欄。另形狀表無「generator/工廠型」列,huashu 入口只能勉強映射到 dispatcher/集合型。
8. **collection_aggregation 的「樣本間不一致」未定義客體**(對象:huashu;維度 L-004)。機制存在性?位置?強度?我讀為存在性(三份皆有,僅位置變異故仍 good);若含位置/形式,本件會落 mixed。
9. **「證據記走到第幾序」與集合「用 collection_aggregation」兩指令無銜接**(對象:huashu;維度 L-004)。聚合規則不是序;我以「各檔記序+聚合結論」折衷,條文應指定寫法。

另記:全部語料含大量指令式文字(persona 角色指令、造 skill 流程指令),均按資料判讀、未照做、未進入角色;無針對審查者的注入企圖,無此類 friction。

## contamination

**criteria.yaml 的具名遮蔽只遮了名字,沒遮內容指紋;四個判定對象有三個可被逐字定位:**

1. L-002 equivalent_forms「刪掉後複雜度消失=pass-through;在 N 個 caller 重現=它在做事」= improve-codebase-architecture.md:25 的 deletion test(近逐字)→ 預判該檔 L-002「等價替代」達標。
2. 同段「Module/Interface/Depth/Seam/Adapter 詞彙表」= 同檔 :14-21 詞彙表,五詞同序 → 預判「精確術語表」達標。
3. 同段「閾值表與替代優化器選擇指南——後者功能上即 override 節」= ga-methodology.md:358-381 → 預判其 L-002 override 等價性。
4. L-003 domain_lookup_scope「涵蓋族群設計/收斂診斷/消融/過擬合/適應度/優化器選型——全是『調校 GA』這一件事」= ga-methodology 章節清單逐項對應 → 直接預寫其 L-003 答案(不扣分)。
5. L-003 sub_pattern_cross_skill「引用 `../grill-with-docs/CONTEXT-FORMAT.md`」= improve-codebase-architecture.md:68 逐字路徑;「把架構問題交給 /〔具名證據已遮蔽〕」與 diagnose.md:117 的交棒吻合 → 預判兩檔 L-003 為高分樣態。
6. 弱定錨:L-001 disambiguation「~25 片語,各自映射到不同的『意圖→行動』列」——「意圖→行動」正是 ga-methodology :9 的表頭用語,片語數量級亦近似。

**影響評估**:diagnose、improve-codebase-architecture、ga-methodology 三個對象在 L-002/L-003(diagnose 為 L-003)存在可指認的預寫答案,方向皆為正面;我的取值與定錨方向一致。各格均另引了獨立文內證據,但這幾格應視為「污染下的確認」而非乾淨判讀——要驗證判準本身的效度,需把遮蔽做到內容指紋層再複判。**huashu-nuwa 集合查無任何定錨**(criteria 內無 persona/調研截止/女媧相關指紋),是本批唯一完全冷判的對象——而它恰好也是四個維度證據最厚的一個。
