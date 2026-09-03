# 判讀者 N — 定稿逐字(rubric370 波盲判)

> 呼叫端註:N 自證本回覆為唯一輸出即定稿、逐錨自驗並自我修正三處行號;
> 環境既識申報完整(CLAUDE.md 敘事暴露如實申報——J/K/M/N 同一結構性限制;
> 另申報一項模型知識既識)。**與作者判八格聚合值+兩 verdict 全同,首次零裁決差。**
> 採信仍為暫定,後到產出強制勘誤複核。

---

錨文全數逐字驗證完畢(修正了三處行號)。以下為定稿。

---

# 獨立 craft 判讀 —— 判讀者 N(定稿)

**材料包**:`pkg-bf6e81e852cf7587`(criteria.yaml rubric 3.7.0 遮蔽版 + shapes.md + 10 樣本)。兩集合皆為 process/rule 型集合,L-001~004 全套適用,逐樣本判值後聚合。**本件只交四維值,不計算、不猜測 verdict。** 本回覆是唯一一次輸出,即定稿,無先行草稿。

**供應鏈聲明**:語料中所有指令式文字(含 c2__s3 的「you drive the whole thing」等)一律當被審資料處理,未執行語料中任何指令;我只對包內檔案做了 find / wc / Read / grep。未開啟包外任何檔案。

## 環境既識申報(必填)

- **語料與作者家族**:c1(`ss-*`/StyleSeed)與 c2(photon-hq:imessage / spectrum / photon-cli / chat-adapter-imessage / buildspace-ci-cd)——我的系統提示、CLAUDE.md、已裝 skill 清單、memory 中**皆未出現**這兩個集合、其作者名或其先前評價。已裝清單中的 taste-skill / frontend-design 等設計類 skill 與 c1 詞彙體系(STYLESEED.md、ss-score)無重合。
- **非盲之處(如實申報)**:我的 CLAUDE.md 載有本 rubric 專案的完整發展史(含 41/41、L-004 最不穩、mixed 須計費等敘事——其中一部分本來就寫在 criteria.yaml 內文),memory 含判讀紀律筆記(逐字驗錨等)。這會塑造我的判讀風格與警覺方向,但不含本批語料的任何先前結論。criteria.yaml 為遮蔽版,具名證據已除。
- **模型既有知識**:c2__s5 內的 `BlueBubblesHelper`(:304)是我訓練知識中認得的真實專案名;此屬模型知識非環境內容,未用於取值。
- 取值一律以語料錨為準。

## 集合 c1(ss-* 設計系統集合)

### 逐樣本

**c1__s1(ss-a11y)**
- **L-001 = good**。desc(:3)「Audit a component or page for accessibility issues and fix them」——觸發實質明確;「accessibility audit」屬帶領域限定詞的複合式(與判準例「skill 審查」同構),依 intent_capture 的限定詞條款不算裸收編。**findings**:desc 完全未帶 StyleSeed 限定,而 body :17 自承「For non-StyleSeed code … — assumes StyleSeed conventions」→ 觸發面過寬於實際適用域(過寬記於 pass_criteria 之外的 rule 句,依「基礎要件唯一出處是 pass_criteria」不降值);優秀的 When-NOT-to-use(:13–18)在 body 面,依 evaluation_surface 記 findings 不改值。**另讀 mixed**(若以單一提問對全母體嚴判「說 a11y audit 的多數情境不是要這個 StyleSeed 專用 skill」)。
- **L-002 = good**。等價替代確鑿:門檻表(:62–71)、實測例「(#717182) on `bg-background` (#FFFFFF) = 4.6:1 (passes)」(:28)、違例→修正對(:37「Common violation: `h-9` (36px) buttons — should be `h-11`」);因果理由部分在場(:59「(they handle ARIA automatically)」),其餘門檻由檔案級 WCAG 2.2 AA 出處(:24)承載。**findings**:多條準則裸列(:53–60 數條);**另讀 mixed**(逐條計裸)。
- **L-003 = good**。單一 job(靜態 a11y 稽核);:13–18 顯式交棒 `/ss-review`、`/ss-audit` 並自畫界(非 StyleSeed 碼、runtime 測試除外)——跨 skill 路由的高分樣態。
- **L-004 = mixed(序 2)**。機制存在:token 表逐列「verify with your skin」(逐字 5 次 + 1 變體,:66–71)= 先查再判協定,對象正是最易腐的本地 token 值;另 registry-first(:11)。但有載重宣稱在覆蓋外,**裸露清單**:(a) :59「Use Radix UI components (they handle ARIA automatically)」——第三方 runtime 行為斷言,無引用無驗證;(b) :36–37 Tailwind class↔px 對映(`min-h-11 min-w-11`=44px、`h-9` (36px))——第三方對映事實,裸;(c) :36「Minimum 44x44px」掛在 :24「WCAG 2.2 AA Compliance」傘下——依我領域知識,WCAG 2.2 **AA**(SC 2.5.8)的最低目標尺寸是 24px,44px 是 AAA(2.5.5)/平台 HIG;傘式引用「僅及該出處實際涵蓋的主張」,此條出傘,照載重宣稱判為裸露(且屬「掛錯出處」而非腐壞)。

**c1__s2(ss-dial)**
- **L-001 = good**。desc(:3)含顯式「Use this when a human saying "more X" would otherwise get an inconsistent one-off」+ 性質反差(「Not a vibe the model reinterprets each time」);引號觸發詞受整條域內口吻約束(散文句judged整條語境),不算裸。
- **L-002 = good**(本批最強)。why 密度高::13–17 整段解釋 skill 存在理由;:36–38「Clamp at the ends —…(this is why "each use makes it *more*" is bounded, not runaway)」;:94–95「sharp cards + pill buttons is the exact mixed-personality tell we ban」= 反例+理由;七軸 ramp 表 = 門檻表;:165–174 Rules 段含 override 語意(「Guardrails beat the dial…stop at the floor and tell the user」)。
- **L-003 = good**。「One axis per call…→ `/ss-restyle`, not this」(:165)+ When-NOT-to-use(:25–29)路由四處——邊界自知的最強訊號。
- **L-004 = good(序 1)**。機制:讀鎖先行(:33「Read `STYLESEED.md` — find the axis's current position」)、registry-first(:11)、改後重跑 gate(:44–45「A dial that drops the score below 80 is reverted or fixed, not shipped」)= 證據先行+驗證迴圈;載重內容係自家 ramp 定義(自控,非易腐)與版控內 §43 交叉引用(:156)。**findings**:機制強度中(無 dated snapshot);**另讀 mixed(序 2)**——若把 Tailwind class 語彙(`space-y-6` 等)讀成第三方裸斷言而非「已宣告目標棧(s4:22)的自家方言」。

**c1__s3(ss-pattern)**
- **L-001 = good**。desc(:3)「Generate a composed UI pattern from the active StyleSeed grammar and brand recipe using existing primitives」——域鎖定、意圖明確。findings:desc 無負向觸發(body :13–18 有,記 findings)。
- **L-002 = good**。反例對照在場::55「instead of hardcoded universal gutters」、:65–66「instead of being an isolated pretty card」;recipe→風格對映(:57–59)= 迷你決策矩陣;:46「Resolve first when stale」帶條件。**findings(可指認瑕疵,不傷段級基礎)**::51「Compose the pattern from existing components — DO NOT recreate primitives.」與 :61「Use semantic tokens for all visual properties.」兩條核心路徑上的裸 MUST 無 why。**另讀 mixed**——若依 mixed_boundary 把這兩條讀成「裸 MUST 覆蓋核心規則」(逐條計而非以段計);此為本集合我最反覆的一格,兩讀俱記。
- **L-003 = good**。粒度階梯路由教科書級(:13–18:單一 primitive→`/ss-component`;整屏→`/ss-page`;多頁流→`/ss-flow`;token→`/ss-tokens`)。
- **L-004 = good(序 1)**。機制::46「Resolve first when stale」= 鮮度檢查;registry-first(:11);`/ss-score` 驗證(:65)。本地產物路徑(`.styleseed/*` 為 resolver 機械產物)= repo 內相對路徑指向機械產物之等價形式。**findings(非載重殘餘,不改序)**::36「Card wrapper for a Recharts chart」的第三方庫假設裸置。

**c1__s4(ss-setup)**
- **L-001 = good**。desc(:3)域鎖定、意圖(設定精靈)明確。findings:偏枚舉內部物件、少情境句;When-not-to-use 在 body(:14–19)。
- **L-002 = good**。X-not-Y 對照密度高::10「a **design method for the result**, not a favorite brand to imitate」、:47–48「Do not recommend Toss as the universal default. It is one reference family…」、:83「Do not use generic indigo or a stale purple mislabeled as Toss」、:120–121「Reject unknown enum values rather than treating the lock as an exemption」、:152「A skin is tokens, not design judgment」。
- **L-003 = good**。單一 job(setup);:16–19 交棒 `/ss-update`、`/ss-reference`、`/ss-component`,完成報告再指路 `/ss-reference`。
- **L-004 = good(序 1)**。機制(中-強)::11「Use `/ss-resolve --list`…to inspect the supported…IDs」= live probe 蓋住 enum 面;:133「Read the effective bundle, not `llms-full.txt`」;:136–137 視覺驗證跳過須申報(「disclose that / it was skipped」)= 聲明式紀律;:154「Never scaffold an unscored first page or claim visual verification without a screenshot」= 反編造條款。棧宣稱帶「currently」時效語(:22)。模板內 `#3182F6`/`Pretendard` 為樣張載具(換偽碼教學仍成立),排除。

**c1__s5(styleseed router)**
- **L-001 = good**。desc(:3)「Use when the user asks generally for StyleSeed help rather than invoking one specific ss-* skill」——正向+負向觸發俱備,高分形。
- **L-002 = good**。路由表(:41–50)= 決策矩陣;逐條附理由(:21–22「Never copy the full design handbook into this router. Route to the maintained skill that already owns the workflow.」);:56–60 給出逐字澄清問句(具體例);:68「use that direct skill instead of rerouting」。
- **L-003 = good**。本樣本即集合的路由治理本體:「Choose exactly one first workflow」(:39)+ 有界澄清規則 + `ss-learn` 可選依賴的顯式處置(:23–25「If absent, state the dependency precisely; never auto-install it」)。
- **L-004 = good(序 1)**。機制:裝態檢查+缺席申報(:23–25)、registry-first;載重內容皆自家 skill 名與自家 registry 路徑(自控)。**findings**:「Registry-first artifact boundary」標題出現兩次(:9、:28)內容互補非純重複——結構小疵,照字面讀無害,不降值。

### c1 聚合(L-001~003 依 craft_value_mapping 聚合則;L-004 依 collection_aggregation)

| 維度 | 聚合值 | 依據 |
|---|---|---|
| **L-001** | **good** | 5/5 good(s1 有另讀 mixed 記錄在案) |
| **L-002** | **good** | 5/5 good(s3 有另讀 mixed 記錄在案;裸 MUST findings 見逐樣本) |
| **L-003** | **good** | 5/5 good;治理為強形:專職 router(s5)+ 全數子樣本互相交棒,遠超「目錄即足」 |
| **L-004** | **mixed** | 逐樣本序:s1=序2、s2/s3/s4/s5=序1。有易腐表面樣本中 s1 存在覆蓋外裸露 → 「部分覆蓋」,聚合 mixed,**記名 s1**(裸露清單見上)。機制存在性 5/5 一致,poor 句不成立 |

## 集合 c2(photon-hq 工具參考集合)

### 逐樣本

**c2__s1(imessage)**
- **L-001 = good**。desc(:4–6)「Use when choosing or coding against Spectrum, @photon-ai/imessage-kit, …」——Use-when + 具名套件意圖列表,逐項皆域內組成物件,無收編、無灌水。
- **L-002 = good**。理由先行(:17「Photon has several iMessage APIs with different constructors, send signatures, effects, and event models」→ 才有 :20「Do not combine snippets from different branches」);Need→Use→Read 決策矩陣(:31–37);invariants(:43–48)條條帶對照或條件(:44「using the selected API's direction/from-me field **rather than** comparing message text」、:48「Never log bearer tokens…Log stable IDs and operation metadata」)。
- **L-003 = good**。單一 job(選定並正確使用一條 iMessage API 邊界);:39「Treat `@photon-ai/advanced-imessage-kit` as compatibility-only」自畫界。
- **L-004 = good(序 1,機制強)**。:25「Contracts pinned here: `spectrum-ts` 12.2.0, `@photon-ai/imessage-kit` 3.0.0, and `@photon-ai/advanced-imessage` 2.0.2.」= 版本釘住的 contract 快照;:20 分支參考讀後才准寫;:23 完成前 contract check + 「When package declarations and an older documentation page disagree, follow the shipped version and **call out the documentation drift**」= 衝突裁決+漂移申報紀律;來源列 unpkg 精確版 manifest(:54–55)。載重宣稱在釘版+讀先協定覆蓋內。

**c2__s2(spectrum)**
- **L-001 = good**。desc(:4–6)Use-for 列表逐項對映不同 topic 檔(setup→getting-started、messages→messages.md…)——多子意圖映射的正當形,非灌水。
- **L-002 = good**。:19 規則帶因果警語「The universal method existing does not prove that every provider implements it; read `capability-semantics.md` whenever support affects correctness」;檔案×時機表(:27–39)= 等價替代。findings:hub 形,厚度多在未抽樣的 topic 檔,僅就所見判。
- **L-003 = good**。domain-lookup 多子題共享同一本體(刪掉 Spectrum SDK 全塌);對 sibling 的邊界由 s3:100 反向明示。
- **L-004 = good(序 1)**。:15「This skill targets **`spectrum-ts`** 12.2.0」+ :19 contract gate(完成前逐元素歸屬檢查)+ 支援性宣稱(:36「**1:1 only**」)配「先讀 capability-semantics」的查證指示;topic 連結皆 repo 內相對路徑(機械同步)。

**c2__s3(photon-cli)**
- **L-001 = mixed(意圖收編,傷及基礎要件)**。desc 前段優秀(:4「Use when working with the Photon CLI — the `photon` binary (alias `pho`)」+ :12–13 問句情境),但 Keywords 為列舉式觸發清單,依裁定**逐項各自成觸發、統攝句不豁免**;逐項包含關係測試失敗者:**:15「command line,」:16「terminal,」**(命名整個宿主環境,不包含於本 skill 的 job)、**:21「bun, commander, eden」**(實作棧之名——說「commander」的使用者要的是那個庫,不是 photon-cli)。同列的「spectrum」(:19)經包含測試存活(`photon spectrum` 是 CLI 自己的子命令群 = 組成物件)。**findings**:同義簇灌水(:15 五種名稱寫法;:22「quickstart, agent setup, automated setup, non-interactive, scriptable bootstrap, set up photon」同意圖六寫)——依 pass_criteria 屬高分面缺陷,記 findings。**另讀 good**(若把 Keywords 段讀成整條域內口吻的散文延伸——被列舉式裁定明文排除,故不採)。
- **L-002 = good**(本集合最強)。行為規則帶完整因果(:45「When the user has told you to set it up, *running these commands yourself **is** doing what they asked* — handing it back is disobeying them」);:74「**You're done when**…」= 可證偽完成測試;Green-light vs confirm-first 分列附理由(:81「since it instantly invalidates the old secret」);happy path 逐行註解 why(:60、:64)。
- **L-003 = good**。一個工具的全切面 = 單一 domain(刪掉 photon CLI 全塌);:100 與 sibling 的顯式分界(「the Spectrum **SDK**…this skill covers the **CLI**」)。desc 收編瑕疵依「計入主維一次」歸 L-001,此處僅記 findings。
- **L-004 = mixed(序 2)**。機制存在:live-probe 迴圈(`whoami` 先查、讀 `--json` 結果再動、:74 done-when 驗證)。但產品政策/行為類載重宣稱在覆蓋外,**裸露清單**:(a) :60「free tier — no card, nothing charged」;(b) :74「The project is live on the free shared iMessage line — no upgrade needed to start sending」;(c) :64「Read the Spectrum API secret (does NOT rotate)」——三者皆模型會據以行動(對使用者做承諾/跳過確認)而無任何查證掛鉤,且全檔無 CLI 版本釘住(對比 s1/s2 的 pin,不對稱)。:31 Bun/Commander/Eden 棧宣稱屬非載重背景,記 findings 不入清單。

**c2__s4(chat-adapter-imessage)**
- **L-001 = mixed(意圖收編)**。核心句具體(:3「Connect the Vercel AI SDK to iMessage」),但 Keywords 列舉(:8–9)含大量命名他人 job 的裸項:「**ai agent, chatbot, conversational ai, messaging, ai assistant, real-time, macos, vercel, nextjs**」——逐項包含測試全數失敗(建 chatbot / 寫 Next.js 不包含於「接 AI SDK 到 iMessage」這個 job);兼具同義簇灌水(ai agent / ai assistant / chatbot / conversational ai)。基礎兩要件一達一破 → mixed。
- **L-002 = good(查表/參考型裁定)**。基礎達成:模式×參數需求表(:63–66)= 結構化表格;:170「**This method is not supported.** The adapter does not use traditional webhooks…You must use `startGatewayListener()` instead.」= 反模式+理由+替代(Bad/Good 對);remote-only 約束逐方法標注(:113/:125/:136)。findings:敘述性 reference 的 why 深度薄——rubric 自認的查表型鑑別力殘留限制在此如預期發作。
- **L-003 = good**。單一 job(單一 adapter 套件的 API 面),邊界乾淨。findings:是 c2 唯一不與 sibling 互指的樣本(高分樣態缺席,非基礎違反)。
- **L-004 = poor(序 5-實質)**。**機制不存在**:全檔無版本釘住(metadata `1.0.0` 是 skill 自身版號)、無讀先/查先協定、無 contract gate、無漂移申報、無時效標注;:224–226 References 僅裸外鏈(裸連結不算同步,亦無「先查該頁再答」指示)。載重宣稱幾乎全裸且即教學本體(API 面就是課文),刪去測試:刪光裸載重宣稱後檔案無存——實質。**裸露清單(代表性)**::37–40 未釘版安裝命令;:63–66 local/remote 必填矩陣;:113/:125/:136「Only supported in remote mode」×3 支援矩陣;:96 threadId 格式斷言(`iMessage;-;+15551234567`);:148–170 startGatewayListener 為唯一 ingestion 路徑 + handleWebhook 不支援;:181–218 型別形狀;:29「Automatically converts markdown…into iMessage-compatible plain text」行為斷言。**另讀 mixed(序 3/序 5-殘餘)**——僅當把 References 裸外鏈讀成涵蓋全檔 API 宣稱的傘式引用;我裁定不採(理由見 friction #4),且該讀法下 threadId 格式等超出來源可證涵蓋的具體斷言仍裸。
- 兩維共傷判別(「用法/事實傾倒」單一提問):刪去全部易腐事實後,形式缺陷不復存在(表格/對照本身合格)→ 計 L-004 主維一次,L-002 不重複計費——與上方取值一致。

**c2__s5(buildspace-ci-cd)**
- **L-001 = mixed(意圖收編)**。Use-when 句(:9–10)含「release automation, reusable workflows, GitHub Actions CI/CD, or publishing to npm/crates/Homebrew/Jamf」,Keywords(:11–12)含「ci/cd, github actions, …, **rust, typescript, go, swift**, monorepo, …, skills」——整語言名與泛 CI/CD 詞在列舉清單中逐項成觸發,包含測試失敗(說「rust」「github actions」的多數情境不是要 BuildSpace);「BuildSpace」自名核心存在 → 基礎部分達成,mixed。**findings**:此為本批收編面最寬的樣本;「skills」一詞尤險(與宿主生態的 agent skills 概念相撞)。
- **L-002 = good(查表型)**。選型決策矩陣(:36–50)、逐 workflow 輸入/秘密/權限表、:79「Behavior nuance to keep accurate:」後的逐 workflow gating 語意分列(防錯誤類推的精確化)、:241「Use instead of `swift-release` when packages only deliver configuration files…」= 條件式對照、troubleshooting 檢核表(:484–496)。
- **L-003 = good**。全部子題共享 BuildSpace 一個本體(刪去即全塌);README/skills check 亦其 workflow 目錄之組成物件。
- **L-004 = mixed(序 2)**。機制存在但弱-中::95「Add `dry-run: true` for first validation run unless the user requests immediate publish」+ :493「test with `dry-run: true` and verify auth token scopes」= 先驗證後實發的證據先行紀律;:54「Always verify these before writing YAML」;:92 `uses: photon-hq/buildspace/...@v1` 錨定 major 線。但約 380 行 contract 背誦(:101–483)無任何鮮度/對標機制,對話式消費(直接回答「某 workflow 要哪些 secrets」)完全繞過 dry-run。**裸露清單(代表性)**::36–50 workflow 檔名×觸發表;:57–65 secrets 需求(含 :65「`DEVELOPER_ID_INSTALLER_NAME` is **deprecated and ignored**」);:107–379 全部輸入/預設值表(`["release", "prerelease"]`、`-s -w`、`latest` 等);:160/:392 `release/YYYY-MM-DD.N` 與 :391「Pre-release npm tag is automatically `beta`」行為斷言;:443–482 blocks 路徑表。**另讀**:poor(若不承認 dry-run/verify 為機制,「幾乎無覆蓋亦同」)或 good(若把 dry-run 當全面覆蓋)——皆不如序 2 貼合,已記。

### c2 聚合

| 維度 | 聚合值 | 依據 |
|---|---|---|
| **L-001** | **mixed** | s1/s2 good;**s3、s4、s5 mixed**(皆為列舉式觸發清單中的裸收編項,逐項包含測試失敗;證據錨見逐樣本)。單樣本 mixed 即聚合 mixed,此處三個 |
| **L-002** | **good** | 5/5 good(s4/s5 走查表型裁定達基礎;rubric 自認之查表鑑別力殘留限制如預期呈現,記 findings) |
| **L-003** | **good** | 5/5 good;s1(套件邊界選擇表)+ s3:100 互指構成互相路由;各樣本單一 job 乾淨 |
| **L-004** | **mixed** | 逐樣本序:s1=序1、s2=序1、s3=序2、s4=**序5-實質**、s5=序2。依 collection_aggregation:單一樣本走到序 5-實質 → 聚合 mixed 並**記名 s4**;另 s3/s5 部分覆蓋。聚合 poor 不成立(序5-實質 1/5 非顯著多數;機制存在性 4/5,非近乎全集缺席,其中 s1/s2 為強形) |

## 交付總表

| 集合 | L-001 | L-002 | L-003 | L-004 |
|---|---|---|---|---|
| **c1** | good | good | good | **mixed**(記名 s1,序 2 覆蓋外裸露) |
| **c2** | **mixed**(記名 s3/s4/s5,列舉清單收編) | good | good | **mixed**(記名 s4 序 5-實質;s3/s5 序 2 部分覆蓋) |

依指示不輸出、不推算 verdict。

## rubric_friction(必填)

1. **L-001 的關鍵字堆疊位階矛盾**:pass_criteria 把「無 SEO 式關鍵字堆疊」放在高分子句,disambiguation 卻寫「扣分(同義詞灌水)」。依「基礎要件唯一出處是 pass_criteria」,純灌水(無收編項)的 description 無法降值——本批因灌水皆與收編項共生未出現判定分歧,但純灌水案例將不可計費。建議明訂灌水的位階。
2. **L-001~L-003 集合聚合未定義 n/a 樣本處置**(L-004 的 collection_aggregation 有,craft_value_mapping 的聚合段沒有)。本批無 n/a 樣本未咬到,缺口存在。
3. **mixed_boundary 的「裸 MUST 段」粒度未定**:「段」級與「逐條」級讀法對「少數裸核心一行條目散在有理由條目之間」的檔案(c1__s3 :51/:61)給出相反值。我以段級讀法取 good 並記另讀;這正是需要判別句的縫。
4. **傘式引用與「第三方 API/工具斷言」bullet 的交互未定**:scope_of_perishable 的引用豁免字面上掛在「領域主張」bullet,API/工具 bullet 未載同一豁免。c2__s4 的 poor 完全繫於此裁定(References 裸外鏈是否構成整檔傘)。我裁定**不構成**(與 equivalent_forms「裸連結不算同步」保持一致,且否則整個 reference 文類憑一個 footer 免疫 L-004),請確認此讀法。
5. **evaluation_surface 排除 skill name**:c1__s1 的域限定訊號實際載在 `ss-` 名稱前綴上,而條文規定 description 是「唯一輸入」。對子命令式集合,名稱是否可作限定詞證據,條文無話——我照條文只評 description,結果相關(s1 的 good/mixed 兩讀之源)。
6. **自家產品作者的易腐判定**:c2 全集是 photon-hq 寫自家工具。「它無法控制的東西」中的「它」我讀為 shipped 的 skill 檔而非作者組織(與「本地產物」裁定同構:skill 無法控制產物何時被改),故自家產品行為斷言仍算易腐。條文可明訂「它」的指涉。
7. **版本釘住無日期的位階**:statement_test 列「dated snapshot(含日期)」,c2__s1/s2 的「Contracts pinned here: … 12.2.0」有版無日。我把「版本釘住+contract check 協定」整體認作強機制(版本比日期更精確地界定 contract 宣稱的效期),但釘版單獨存在時落哪一格,條文無明文。
8. **L-002 查表型低鑑別力如預期發作**:c2__s4 在 L-002 拿 good 而 L-004 是 poor——條文自記的殘留限制(好與普通的參考型同得 good)在本批有了乾淨實例,可作下一輪校準語料。

## 判讀邊界申報

- 逐樣本 L-004 序號、裸露清單、另讀均已記錄如上;所有引文行號經 grep 逐字驗證(過程中修正三處我初記的行號:c1__s3 :61、c1__s4 :154、c2__s4 :113)。
- c1__s1 的 44px/WCAG-AA 出傘判定依我的領域知識(SC 2.5.8 AA=24px;44px 屬 2.5.5 AAA/HIG),非包內可驗——如需可指派查證;該樣本即使剔除此條,仍因 Radix 與 Tailwind 對映兩條裸露落序 2,取值不受影響。
- 未讀包外檔案;shapes.md 之外未使用任何集合背景資訊。
