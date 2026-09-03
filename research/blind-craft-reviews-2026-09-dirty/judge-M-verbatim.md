# 判讀者 M — 逐字紀錄(中途稿 + 真定稿)

> ⚠️ 呼叫端勘誤(2026-09-03):**下方第一節是中途稿**——原註「無中途稿誤採」是錯的,
> 我正是採它裁決並 land 了 PR #39;真定稿(第二節)在 merge 後才到,13 tool uses、
> 帶逐行錨,其 nano L-002 good 的五組錨經逐字驗實 → viper verdict 勘誤 NR→AWN
> (§定稿勘誤,`review-dirty-wave-2026-09.md`)。原註全文保留如下當紀錄:
> 原註:終局三規則全程套用(前哨先行修包、靜默期 ≥ 已跑時長、無中途稿誤採)。
> 錨驗:語料引文抽驗全過;**friction #1 的「消費者載入該樣本即受害」句經 grep
> 在包內不存在**(F7 已刪的舊句)——判讀者編造錨第 2 例,該條 friction 的
> 「兩句互指」半邊作廢;其真問題(Expert-in desc 樣本層取值)由呼叫端依位置規則
> 裁定(desc=該樣本核心觸發面 → mixed)。M 的 vp L-002 聚合 mixed 依 3.6.2 實文
> 為規則正確,呼叫端採納並修正作者判(viper AWN→NR)。
> **←這一步就是後來被定稿推翻的那一步**(中途稿的「用法傾倒 why≈0」被定稿實錨否證)。

---

```yaml
judge: M
material_boundary: >-
  只讀 dirty-blind/ 內 criteria.yaml、shapes.md、skills/ 十份;rubric-masked/ 與
  mask-sample.json 未開啟;未上網。
supply_chain: >-
  十份語料均按資料處理;無指向審查者的注入。rj 樣本內大量指令式教學內容照資料判讀。

objects:

  rj__collection(5 樣本):
    shape: "集合型(主題式技術指南庫);各樣本自身為查表/參考型長文(pattern+config 傾倒)"
    per_sample:
      javascript-testing-patterns: {L-001: good, L-002: poor, L-003: good, L-004: "序5-實質 → poor"}
      code-standards:              {L-001: mixed, L-002: poor, L-003: good, L-004: "序5-實質 → poor"}
      python-testing-patterns:     {L-001: good, L-002: poor, L-003: good, L-004: "序5-實質 → poor"}
      logging-observability:       {L-001: good, L-002: poor, L-003: good, L-004: "序5-實質 → poor"}
      python-performance-optimization: {L-001: good, L-002: poor, L-003: good, L-004: "序5-實質 → poor"}
    dims: {L-001: good, L-002: poor, L-003: good, L-004: poor}
    evidence:
      L-001: "4/5 desc 具體 Use when(js-testing :3『Use when writing JavaScript/TypeScript tests, setting up test infrastructure…』);code-standards :3『Expert in code design standards including SOLID principles…』無觸發情境 → 該樣本 mixed(傷及其觸發面);聚合兩讀後取 good 帶 findings。⚠️ 此格我在 good/mixed 兩讀間最不確定"
      L-002: "5/5 同質:近千行 config/pattern 傾倒,因果詞近零(js-testing 948 行掃得 1 處 because;code-standards 970 行 0 處);無 Bad/Good、無 override;結構化表格要件也缺 → 樣本 poor;聚合『全同 → 該值』→ poor"
      L-003: "各樣本單一主題、邊界乾淨;集合層 25 skills 僅目錄羅列——路由治理弱形 → good 帶 findings"
      L-004: "5/5 同型:Jest/Vitest/pytest/cProfile 等第三方斷言貫穿、零機制零時效;逐樣本序 5-實質 → poor;聚合 poor 句全集成立 → poor"

  vp__collection(5 樣本):
    shape: "集合型(在地化 curation:vendored 上游 + 自製強化層與工具);樣本多為 process/rule 型"
    per_sample:
      humanizer:        {L-001: good, L-002: good, L-003: good, L-004: "序1(版本釘+附出處) → good"}
      humanizer-zh-tw:  {L-001: good, L-002: good, L-003: good, L-004: "序1(audit loop 機制) → good"}
      remotion-video:   {L-001: good, L-002: good, L-003: good, L-004: "序1(秒數一律由 SRT 推導=證據先行) → good"}
      subtitle-align:   {L-001: good, L-002: good, L-003: good, L-004: "序1(ASR 只取時間,文字用你給的=反編造設計) → good"}
      nano-banana-pro:  {L-001: good, L-002: mixed, L-003: good, L-004: "序5-實質 → poor"}
    dims: {L-001: good, L-002: mixed, L-003: good, L-004: mixed}
    evidence:
      L-001: "5/5 具體(remotion :3 域錨清楚;nano 綁定特定工具);無收編 → good"
      L-002: "4/5 強(remotion 🔴鐵則+『會被退回的常見原因』;zh-tw audit loop;subtitle-align 附 why);nano-banana 為用法傾倒、why 近零 → 樣本 mixed;聚合:單樣本 mixed、瑕疵屬該樣本核心 → 聚合 mixed"
      L-003: "顯式疊層路由(zh-tw :6『疊在 humanizer 之上』)=高分樣態 → good"
      L-004: "4 樣本序 1;nano-banana 序 5-實質 → 樣本 poor;聚合:單一序5樣本 → poor 邊界句 → mixed、findings 記名"

rubric_friction:
  - "(rj,L-001)集合聚合『單樣本 mixed』的聚合層適用兩讀——我最終取 good,但另讀取 mixed。此格值搖擺"
  - "(rj,L-003)『集合/框架型具路由治理』是基礎還是高分?僅目錄清單時 good↔mixed 兩讀"
  - "(vp,L-002)nano 的用法傾倒同時計了 L-002 mixed 與 L-004 poor——跨維主維規則寫『計主維一次』,但『用法傾倒』主維是 L-002 還是 L-004 無裁定,我兩維都計了"
  - "(通用)criteria 無 evidence_refs(似被剝除)——不影響判讀,反而乾淨"

contamination:
  - "具名/數字:零;逐一比對 10 份語料檔數/行數/規則數無對應"
  - "『聲明式紀律』括號與 rj checklist 不同構;損壞症狀列舉與 rj__code-standards 一處格式異常近似,但按條文門檻自判為格式瑕疵——條文門檻句自我修正了可能的誤導"
  - "vendored 樣本在 criteria 中無可指認稱讚描述——無預寫方向。整體:無可指認定錨"
```

**程序聲明**:一次交付定稿;行號以我讀取之檔案為準;無中途稿。


---

## 第二節:真定稿(land 後到貨;13 tool uses / 848s / 166k tokens;逐行錨版)

讀畢 criteria、shapes 與十份語料。以下為一次交付的定稿。

```yaml
judge: M

collections:

  rj:
    shape: "process/rule 型集合——五份獨立的規則/模式語料庫子 skill(設計原則、JS/Python 測試、logging、Python 效能),帶 domain-lookup 色彩,L-001~004 全套適用、以子 skill 抽樣評分"
    samples:
      - id: rj__skills_code-standards
        dims: {L-001: mixed, L-002: good, L-003: good, L-004: "n/a(序4)"}
        evidence:
          L-001: "L3『**ALWAYS use when designing ANY classes/modules, implementing features, fixing bugs, refactoring code, or writing functions.**』——列舉項『fix bug』『implement feature』是另一個 job 的名字、僅因可被設計視角詮釋而收入(單一提問:使用者說 fix bug 時多數不是在要設計準則 skill)→ 收編,mixed 起判;兩讀:多數列舉皆收編可讀 poor,但域內自有觸發(『apply SOLID』『is this too complex』『avoid over-engineering』)存在=基礎部分達成 → 選 mixed"
          L-002: "why 具備(L737『Duplication is better than wrong abstraction』、L149『Adding push notification requires modifying this method』);全篇 ❌/✅ 對照(L34-49 BaseEntity);高分 override 節亦在(L721『### ❌ Don't Over-Apply When:』)"
          L-003: "L21『For naming conventions..., see `naming-conventions` skill』顯式交棒;全檔共享『程式設計原則』單一本體;findings:desc 收編兼傷職責面,依主維規則計入 L-001 一次"
          L-004: "序4:教學內容為穩定方法論,無載重宣稱——bcrypt/Stripe 字面屬樣張(L67、L632 範例註解);猶豫:L962『Code is read 10x more than written』未附引用,判修辭性量化非載重(另讀=序5-殘餘→mixed),選序4 n/a"
      - id: rj__skills_javascript-testing-patterns
        dims: {L-001: good, L-002: mixed, L-003: good, L-004: "poor(序5-實質)"}
        evidence:
          L-001: "L3『Use when writing JavaScript/TypeScript tests, setting up test infrastructure, or implementing TDD/BDD workflows』——域限定觸發,無收編;findings:desc 宣稱 end-to-end testing 而 body 無 E2E 章(觸發面對 e2e 需求會空轉)"
          L-002: "核心規則面(L949-963 Best Practices 15 條)多為裸/近裸清單(『Follow AAA Pattern』『One assertion per test』),全檔零 Bad/Good 對照、純正例模板不屬 equivalent_forms 三型;部分項帶目的子句(L953『Mock external dependencies: Keep tests isolated』)=基礎部分達成 → mixed"
          L-003: "全檔同屬 JS/TS 測試單一 domain(單元/整合/mock/元件/fixtures 共享本體);findings:desc 與 When-to-Use 宣稱 e2e、CI/CD 而內容缺席"
          L-004: "無機制(Resources L1022-25 為裸連結,無『先查再答』指示);裸露清單:jest.config L27-52(ts-jest preset、coverageThreshold)、vitest config L57-73(provider:'v8')、renderHook 自 @testing-library/react L815、faker API L873-883、supertest/pg 用法 L491-706;刪去框架 API 面即教學本體盡毀 → 序5-實質 poor"
      - id: rj__skills_logging-observability
        dims: {L-001: good, L-002: good, L-003: good, L-004: "poor(序5-實質)"}
        evidence:
          L-001: "desc L3 主題式但判實質可推觸發語境;非標準 frontmatter 欄 `activation_triggers`(L4-14)非 description、載入器不消費,比照 body when-to-use 記 findings 不改值——另讀:若該欄被消費,裸項『debugging』『monitoring』逐項成收編 → mixed;選 good(評估客體=description,『debugging patterns』子句依整條域內語境判不裸)"
          L-002: "L205-219『# BAD - logging credentials / # GOOD ...』對照;L40『Don't log everything - unnecessary noise obscures real issues』(why);L27-33 log level 表、L460-468 工具表=結構化表格等價形式"
          L-003: "logs/traces/metrics 同一 observability 本體;findings:§7 之 Conditional Breakpoints(L384-393)與 Remote Debugging(L395-408)屬互動式除錯 job、刪掉 observability 本體不塌——但僅兩小節邊角,不傷主職責;L878『Combine with: development-philosophy..., security-first-design...』跨 skill 路由"
          L-004: "無機制;裸露清單:§8 工具表 L460-468(含『Stackdriver | GCP native』已改名、『CloudLogging | Azure native』錯置=已實際腐壞)、§10 五語言函式庫清單 L523-657(含『slog - Standard library (Go 1.21+)』)、Jaeger thrift exporter L539/L756(OTel 已棄用路線)、prometheus_client L475-487、debugpy L400-408;猶豫兩讀:核心規範(§1-4)刪後仍存 → 殘餘?但殘餘例示量級是『一行工具推薦』,此處為兩整節+跨例 API 面 → 取實質,poor"
      - id: rj__skills_python-performance-optimization
        dims: {L-001: good, L-002: good, L-003: good, L-004: "mixed(序2)"}
        evidence:
          L-001: "L3『Use when debugging slow Python code, optimizing bottlenecks, or improving application performance』——『slow Python code』域限定;寬尾子句受整條 Python 效能語境約束不算裸"
          L-002: "通篇 slow/fast 對照且附可跑 benchmark=可證偽(L224-244、L282-307、L618-647);L826『Profile before optimizing - Measure to find real bottlenecks』(why);findings:L246-249『Even faster...map』對 lambda 情形存疑(準確性邊角瑕疵,不傷基礎要件)"
          L-003: "profiling→模式→DB→記憶體→benchmark 全屬『Python 調速』單一 expertise,刪本體全塌"
          L-004: "機制存在=證據先行紀律(L826『Profile before optimizing』、L869『[ ] Benchmarked before and after optimization』,各 pattern 內嵌 timeit 探針=效能宣稱帶驗證);覆蓋外裸露清單:py-spy CLI 旗標 L204-213、kernprof L143、pip 套件名 L130/L173/L809、pytest-benchmark 旗標 L821、Resources 之 PyPy/Cython 一行定性 L855-856 → 序2 mixed;附註:機制為弱形(證據先行),另讀否定機制則裸露屬殘餘 → 仍 mixed,兩讀收斂"
      - id: rj__skills_python-testing-patterns
        dims: {L-001: good, L-002: mixed, L-003: good, L-004: "poor(序5-實質)"}
        evidence:
          L-001: "L3『Use when writing Python tests, setting up test suites, or implementing testing best practices』——pytest 具名,整條域內口吻,寬尾子句不算裸"
          L-002: "有一節真對照(L638-664『# Good test names / # Bad test names』附理由『Not descriptive』『Too vague』),但核心規則面(L898-907 十條、各 pattern)多為裸清單與純正例 → 基礎部分達成 mixed(比 js 版多一節對照,仍不及格線之上)"
          L-003: "全檔 Python 測試單一 domain;CI/CD 章(L804-839)屬測試基建、同本體"
          L-004: "無機制;裸露清單:`sqlalchemy.ext.declarative.declarative_base` L735(SQLAlchemy 2.0 已遷移=已腐)、async fixture 未用 pytest_asyncio 形式 L399-404、GH Actions `actions/checkout@v3`/`setup-python@v4`/`codecov-action@v3` L819-836(舊 major)、pytest/pytest-cov 旗標 L712-727、hypothesis API L575-614;框架 API 面即教學本體 → 序5-實質 poor"
    aggregate:
      L-001: mixed   # 單樣本 mixed(code-standards 意圖收編)→ 聚合 mixed;樣本層位置規則已濾,聚合層不重判
      L-002: mixed   # 兩樣本 mixed(js-testing、py-testing:核心規則面裸清單、無對照/等價形式)→ 聚合 mixed
      L-003: good    # 五樣本全同 good;抽樣內見跨 skill 路由(code-standards→naming-conventions、logging→Combine with 三鄰)
      L-004: poor    # 有易腐表面的 4 樣本中 3 個走到序5-實質、僅 1 個具弱機制:「大量時效性宣稱而幾乎無機制」的 poor 句對抽樣所見成立(非「單一樣本序5-實質」情形,不受 mixed 地板拘束);逐樣本序=4/5實/5實/2/5實

  vp:
    shape: "process/rule 型集合——工具包裝/產線型與改寫規則型子 skill 混合,樣本間有互見路由(zh-tw→humanizer 分層、subtitle-align→tts-dialogue 交棒、字幕句級/頁級與影片產線分工)"
    samples:
      - id: vp__humanizer-zh-tw
        dims: {L-001: good, L-002: good, L-003: good, L-004: "mixed(序2)"}
        evidence:
          L-001: "desc L10-11『當要寫/改繁中台灣文案、旁白、逐字稿、貼文,或覺得稿子有中文 AI 味、翻譯腔、書面腔、用語不道地時使用』——情境+症狀雙入口皆域限定;症狀片語同歸一段屬『異意同歸』非灌水"
          L-002: "❌/✅ 對照(L94-101)、Before/After 全例+『改了什麼』註記(L165-171);why 到位(L44『AI 訓練語料大量簡體,繁中輸出常滲大陸詞』、L107『堆了假』);可證偽啟發式(L62 阿姨測試、L154 默唸測試);override 節(L127『若稿子是真人講的,這節不適用』、L187 專業向放寬)"
          L-003: "L23『先跑 `humanizer` 清英文毛病 → 再跑這份...兩者互補、不重複』——跨 skill 分層路由;鎖語氣與 TTS 節皆同一 job(去 AI 味)的守則,刪本體即塌"
          L-004: "機制存在=保真/不誇大紀律(L31『只講做得到、查得證的,不為戲劇效果膨脹數字/後果/因果』、L34『事實、數字、步驟一字不能跑』——弱形、對象為本 skill 產出,強度記此);覆蓋外裸露清單:TTS 行為斷言(L124『TTS 唸出來會卡字、變怪、出雜音』、L126『破折號、刪節號少用——TTS 處理不穩』=直接驅動改寫行為的第三方 runtime 斷言,無任何探針)、L185『humanizer(英文 AI 特徵 24 型)』手抄鄰檔結構數字、L44 訓練語料主張 → 序2 mixed(另讀否定機制:裸露屬殘餘 → 仍 mixed,收斂)"
      - id: vp__nano-banana-pro
        dims: {L-001: good, L-002: good, L-003: good, L-004: "mixed(序5-殘餘)"}
        evidence:
          L-001: "desc L3『Use for image create/modify requests incl. edits』——該觸發詞多數情境正是在要此 skill(它就是影像生成的執行者),任務包含於自身 job → 非收編"
          L-002: "L28『Goal: fast iteration without burning time on 4K until the prompt is correct』、L24『...so images are saved where the user is working』(why);解析度映射表 L45-49、Common failures 症狀→解法表 L66-69=結構化等價形式;findings:L118『Do not read the image back』無 why(邊角)"
          L-003: "單一 job(以隨附腳本生成/編修圖),邊界乾淨無 creep"
          L-004: "機制不成立——Preflight(L61-64 `command -v uv`、`test -n $GEMINI_API_KEY`)屬『只探測使用者環境』型,statement_test 明文不算;Common failures 表為事後判讀非事前攔截;裸露清單:L39『The Gemini 3 Pro Image API supports three resolutions (uppercase K required)』、L41-43 ~1024/2048/4096px、模型名 Gemini 3 Pro Image、quota/403 行為 L69;自家腳本行為(路徑、錯誤字串、key 順序)與 skill 同包受控,不入易腐;刪去 API 事實後工作流(draft→iterate→final、檔名、模板)教學價值仍立 → 殘餘,mixed;猶豫:安裝路徑 ~/.claude/skills/... 判宿主平台詞彙豁免(另讀=環境路徑斷言),不影響取值"
      - id: vp__humanizer
        dims: {L-001: good, L-002: good, L-003: good, L-004: "n/a(序4)"}
        evidence:
          L-001: "desc L5-6『Use when editing or reviewing text to make it sound more natural and human-written』——目的子句限定寬動詞;模式列舉逐項映射不同章節(§1/§4/§10/§13...)=多子意圖非灌水;findings:未標語種(語言路由靠 zh-tw 檔單向承擔)"
          L-002: "24 型每型 Words to watch+Problem(why)+Before/After 對照(如 L104『AI chatbots tack present participle phrases onto sentences to add fake depth』+L107/L110);L38『Sterile, voiceless writing is just as obvious as slop』(why)"
          L-003: "『去 AI 痕跡+注入人聲』同屬『讓文字像人寫』一個 job、共享同一本體;findings:對 zh-tw 無回指路由(單向)"
          L-004: "序4 n/a:域主張整批附出處(L22/L435『based on Wikipedia's Signs of AI writing page, maintained by WikiProject AI Cleanup』+L437 直接引文)——依 scope_of_perishable『已附引用的領域主張』不入易腐範圍,扣除後無在scope載重宣稱;另讀:傘式引用不及逐條,模型行為斷言(L212『AI has repetition-penalty code』、L161『post-2023』)殘餘裸露 → 序5-殘餘 mixed;選 n/a(引用條款未要求逐條掛注形式),猶豫記此"
      - id: vp__remotion-video
        dims: {L-001: good, L-002: good, L-003: good, L-004: "good(序1)"}
        evidence:
          L-001: "desc L3『把逐字稿＋配音＋實錄素材做成成品影片(Remotion)。含時間軸鐵則、抽幀自審、播放相容轉檔。』——輸入/輸出/工具俱名,判實質觸發語境清楚(無 Use-when 句式不扣)"
          L-002: "規則|為什麼雙欄表(L30-35、L77-82);實錯敘事作因果(L59『曾經有一版手打秒數...全片畫面與旁白錯開,整支重做』、L94);❌/✅(L109『絕不要 width:100% 硬撐——人臉會變形』、L163『只給 -pix_fmt yuv420p 沒有用』);L231-239 症狀|真正原因|解法 表"
          L-003: "單一產線 job,各節皆其工序;去識別化/長任務皆本產線環節;L134-136 句級/頁級 SRT 與字幕工具分工互見"
          L-004: "序1 good:機制=強形多重——L33『配音實長用 ffprobe 讀出來/不准手打秒數』與 L245『秒數從 SRT 來,不從腦袋來』(never-from-memory)、L169-174 驗證命令+判讀『要看到 yuv420p / tv / bt709 / bt709』(live probe+判讀表)、L200-207『只跑 ffprobe 不算自審』『回報要附 ffprobe 的實際輸出(不是預期值)』(證據先行交付)、L247『不確定就說不確定』;載重第三方行為斷言(L151 yuvj420p 預設、L82 OffthreadVideo 跳閃)皆落在交付前探針/抽幀自審覆蓋內;findings(非載重殘餘裸露,不改序):L133『約 9 成觀眾不開 CC』未附引用量化——模型據以行動的是『燒字幕』規則而非該數字;另讀視其為覆蓋外載重 → 序2 mixed,選序1"
      - id: vp__subtitle-align
        dims: {L-001: good, L-002: good, L-003: good, L-004: "good(序1)"}
        evidence:
          L-001: "desc L3『把配音對齊成零錯字的 SRT(faster-whisper 強制對齊)。ASR 只取時間,文字用你給的。』——job、方法、與常見誤解的切割一句寫清"
          L-002: "L26『所以就算 whisper 聽錯字,字幕內容也不會錯——它只借時間』(why);L74-78 ✅/❌ 用途表附後果(『會把前一句尾音帶進下一句』);L101-105 驗收標準表+L108 診斷指引"
          L-003: "單一 job;L80『雙人對話用 `tts-dialogue`』顯式交棒、L114-119 句級/頁級與影片產線分工=跨 skill scope 治理"
          L-004: "序1 good:機制=驗收探針+判讀表(L96-105:cue 數=行數、末 cue 不超過 ffprobe 時長、首句&lt;1s、抽查中段)覆蓋本 skill 核心宣稱『時間準、零錯字』;findings(殘餘裸露記名):L70『尾音會超出 cue 結尾約 0.25 秒』(第三方行為量化,其支撐之禁令本身保守安全)、L44 模型名 medium/large-v3 現行性、L117『約 9 成觀眾不開 CC』;另讀視為覆蓋外載重 → 序2 mixed,選序1(與 remotion 同一判別:模型行動於規則、非於數字)"
    aggregate:
      L-001: good    # 五樣本全同 good
      L-002: good    # 五樣本全同 good(對照/等價形式與 why 皆在,裸規則僅邊角)
      L-003: good    # 五樣本全同 good;集合內互見路由成立(zh-tw→humanizer 分層、subtitle-align→tts-dialogue)
      L-004: mixed   # 有易腐表面的 4 樣本(humanizer 序4 不計入不一致)中 2 個存在覆蓋外/殘餘裸露(zh-tw 序2、nano 序5-殘餘)=「部分覆蓋」;且機制存在性樣本間不一致(nano 無機制、餘皆有);poor 句不成立;逐樣本序=2/5殘/4/1/1
```

## rubric_friction

1. **L-001 的評估面遇到非標準 frontmatter 欄位無規可循**:`rj__skills_logging-observability` 的 `activation_triggers`(L4-14)既非 description 也非 body。我依 evaluation_surface 的理路(評模型實際消費的觸發輸入)比照 body when-to-use 處理(記 findings 不改值),但若某載入器消費該欄,裸項「debugging」「monitoring」逐項即成收編——同一檔在兩種宿主下取值相反。條文宜明訂非 description 的 frontmatter 觸發欄怎麼算。
2. **L-004 序5 的實質/殘餘是二分,中間形態無處落**:logging 的裸露(兩整節約 15-20%、核心規範仍存)遠超殘餘例示的「一行工具推薦」量級,卻也不是「教學本體盡毀」;二分逼我落實質→poor。js/py-testing 那種全檔 API 面的 poor 與 logging 的 poor 在檔內是兩種嚴重度,取值看不出來。
3. **「載重宣稱」與「順帶量化形容」的界線在序1 情境下缺判別法**:「約 9 成觀眾不開 CC」「尾音超出約 0.25 秒」這類支撐規則的量化,判載重(→序2 mixed)或殘餘修辭(→序1 findings)直接翻轉有強機制樣本的取值。我採「模型行動於規則抑或於該數字」為判別;條文只在序5 內提及「順帶的量化形容」,序1 的「非載重殘餘」無對應判別句。
4. **傘式引用是否滿足「已附引用」未定**:vp__humanizer 以整檔兩處聲明出處覆蓋 24 型全部域主張,無逐條掛注。我接受傘式(序4 n/a),但另讀(逐條才算)會落序5-殘餘 mixed。
5. **集合聚合的 poor 邊界**:「單一樣本走到序5-實質 → 聚合 mixed」與開頭 poor 句之間,幾個樣本才夠「大量…幾乎無機制」沒有寫。rj 是 4 個有表面樣本中 3 個序5-實質,我判 poor 句成立;若有人讀成「poor 句需全數樣本如此」會得 mixed。
6. **樣張排除條款對 API 食譜型 skill 欠判別法(本輪最大摩擦)**:「範例樣張內的字面」只例示了「示範輸出裡的版本字串」,但 rj 集合的 code block 同時是樣張形狀與教學本體。我用「教學內容是什麼」區分(code-standards 的例是原則載具→排除;testing-patterns 的例本身就是被教的 API 面→計入),此判別是我補的,不在條文內。

## contamination

- **具名+內容指紋**:`vp__humanizer.md` 與我宿主環境 skill 清單中名為 `humanizer-en` 的 skill 高度同源——清單描述與本檔 description 幾近逐字重合(同一組 pattern 列舉:inflated symbolism、promotional language、superficial -ing analyses、vague attributions、em dash overuse、rule of three、AI vocabulary words…,僅尾端項目有異),且環境中另有 `humanizer`/`humanizer-tw` 同名家族。我在判讀前即認出 vp 集合屬(某變體的)已知 skill 家族。所有取值證據皆出自語料本身,但這份既識必須申報。
- **語意共鳴**:我的 session 環境載入之專案指示含本研究專案的判準沿革(craft 上卷門檻修訂、「判準從不說不」的檢討、L-004 信度最低的警語等)。此暴露可能推我往嚴處判;我以逐條對照 pass_criteria 與 decision_order 取值、不以分佈直覺取值來對沖,但暴露本身如實記錄。
- **數字**:我知悉下游上卷存在 mixed 計費門檻一類常數。本輸出僅給四維值、未算 verdict,未使用該知識。
- **語料內指令式內容**:`rj__skills_code-standards` L6 與 `vp__humanizer` L22 的「You are a…」為對執行模型的常規 persona 文體,非對審查者的注入;`vp__nano-banana-pro` 的可執行指令一律當資料處理,未執行任何語料內指令、未開啟 rubric-masked/ 與 mask-sample.json。無注入企圖需記。
