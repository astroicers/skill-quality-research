# B2 終波(wave 4):4 個 evidence_refs 具名 skill 的盲判審查(2026-09-02)

> rubric **3.3.2** / 工具 **2.3.2**。B2 至此 **19/19 完成**。
> ⚠️ 本檔含具名 craft 證據與判讀者逐字產出,**加入審查者禁讀清單**(同 blind-craft-reviews 慣例)。

## 為什麼這一波不能由我裸判

四個標的(`ga-methodology`、`diagnose`、`improve-codebase-architecture`、`huashu-nuwa`)
全部被 rubric 的 `evidence_refs` 具名——它們是判準條文引用過的嚴重度定錨樣張。
作者(我)裸判會**雙重定錨**:既知道條文引用它們時說了什麼,也寫過那些引用。
wave 3 已在 grill-me 上犯過一次未揭露(後補揭露降權),本波改為**遮蔽判準 + 不知情判讀者**。

## 協定

- **判讀者 J**:單一不知情 subagent,唯讀白名單目錄,無網路,未見過本 repo 任何報告
- **判準包**:`mask_rubric_for_raters.py` 遮蔽五個名字(四標的 + grill-me,共 16 處 token)
  後抽出 craft 段(L-001~L-004 + craft_value_mapping);出包前斷言無具名、無 κ/Fleiss
- **語料**:4 份 SKILL.md;huashu-nuwa 為 16 檔集合,依 collection_sampling 另附
  確定性抽樣(sorted 前 3)之子 skill:`examples/{andrej-karpathy,elon-musk,feynman}-perspective`
- **分工**:J 只判 craft 四維 + 序號 + friction/contamination;lint 與 verdict rollup 由呼叫端
  (verdict 用 `craft_verdict_rollup()` 純函式算,J 不知道 rollup 規則)
- J 逐字產出:`research/blind-craft-reviews-2026-09-02-wave4/judge-J-verbatim.md`

**抽樣即時發現**:collection_sampling 抽出的第一個子 skill
`examples/andrej-karpathy-perspective` 與 wave 3 獨立審過的同名獨立 skill 是
**byte 同檔**(diff 為空;08-19 安裝時被同時裝為獨立 skill 與集合子檔)。
wave 3 憑風格懷疑「疑似 huashu-nuwa 血統」並揭露降權,本波證實了那個懷疑,
且 J 的盲判天然構成對同一檔的覆核(見 §交叉核對)。

## ⚠️ 插曲:中途稿事件(本波最重要的程序教訓)

J 執行約 8 分鐘時停頓一次,吐出一份**完整格式的中途稿**——四個對象、維度值、
行號引文、friction、contamination 俱全,**看起來就是交付物**。呼叫端照
「證據可指認」紀律逐錨驗證,結果:**四個對象的關鍵引文全部查無**——
diagnose/improve 是英文 skill,中途稿給的是不存在的中文『引文』;
ga-methodology 被引的『撰寫時快照』『PyGAD』『輪盤選擇』全不在檔內;
huashu 的『推演標記』條款不存在,且「子檔 1/3 有攔截」被 grep 直接否證(實為 3/3)。

約 8 分鐘後 J 交出**定稿**:錨大面積換新,呼叫端抽驗約 20 個載重錨**全數通過**
(含 karpathy:110-114 雙 CHECKPOINT、musk:358-364 誠實邊界、entry:343 vs :353
枚舉不一致這種細粒度引用)。兩份對照存證:
`judge-J-draft-superseded.md` / `judge-J-verbatim.md`。

**教訓三條**:
1. **判讀者輸出必須逐錨驗證後才可採信**——中途稿與定稿的維度值在 4 個對象上
   有 3 個不同(diagnose mixed→good、improve 2mixed+poor→4good、huashu mixed→good),
   誰先到手誰就會被寫進報告。與 `guards-need-an-adversary` 同構:
   **判讀不是證據,通過逐字驗證的判讀才是**。
2. 中途稿的錨是**似真編造**(語言都對不上卻有行號)——正是 rubric 在受審 skill 裡
   追殺的 anti-hallucination 失效型,發生在審查者自己身上。
3. 呼叫端因中途稿而把 4 個主檔全文讀過一遍、獨立重導了一次維度——
   結果與 J 定稿在 diagnose/huashu **逐維一致**,improve 差一維(見下)、
   ga 差一維(真分歧,見 §ga 分歧)。這次意外的雙盲交叉本身成了定稿可信度的佐證。

## 呼叫端半邊:deterministic lint(工具 2.3.2)

| skill | packaging | hygiene | security |
|---|---|---|---|
| ga-methodology | 0/14(內部工具形狀) | 0 err / 0 warn | 無紅旗 |
| diagnose | 0/14(內部工具形狀) | 0 err / 0 warn | 無紅旗 |
| improve-codebase-architecture | 0/14(內部工具形狀) | 0 err / 0 warn | 無紅旗 |
| huashu-nuwa | 5/14(T1 剖面) | 0 err / 0 warn | 無紅旗 |

四個標的 lint 面全潔淨;無 `confidence: medium` 紅旗需步驟 5 複核。
(huashu 入口 `:256` 推薦 Z-Library/LibGen 屬 J 另記的**合規疑慮**,非 lint 規則所轄,
如實轉錄於此;不入 craft 計分。)

## 盲判結果(J 定稿維度值 + 呼叫端 rollup)

| skill | shape(J) | L-001 | L-002 | L-003 | L-004(序) | verdict(rollup) |
|---|---|---|---|---|---|---|
| diagnose | process/rule | good | good | good | good(序1,協定型機制) | **approved** |
| improve-codebase-architecture | process/rule | good | good | good | good(序1) | **approved** |
| ga-methodology | domain-lookup | good | good | good | **n/a(序4,外推)** | **approved**(見分歧) |
| huashu-nuwa(集合 1+3) | dispatcher/集合 | good | good | good | good(序1,3/3 一致) | **approved** |

呼叫端獨立重導的差異:improve 的 L-001 我曾標 mixed——回查後那是**繼承中途稿前提**
(『高頻寬詞』),定稿讀法(四片語同 job 不同入口、語境具體)對照 `:3` 原文成立,採定稿。

**亮點證據**(逐錨已驗):
- **huashu-nuwa 是 L-004 的教科書級樣本**:生成器把「調研截止日 + never-from-memory +
  編造黑名單 + 雙 CHECKPOINT」**模板進產物**,三份抽樣子檔 3/3 帶全套
  (musk 誠實邊界甚至逐類覆蓋:時間線×2-3 倍、政治立場過時、管理風格兩極)。
  它也是本批**唯一完全冷判**的對象(criteria 無其內容指紋)——四個 good 全部乾淨。
- diagnose `:49` 「Stop and say so explicitly. List what you tried」+
  「Do not proceed to hypothesise without a loop」= never-from-memory 的流程型等價
  (J friction 1 如實記:這是寬讀,條文未裁定)。
- improve `:25` deletion test、`:35` 先讀 glossary/ADR、`:68` 跨 skill DRY 引用、
  與 diagnose `:117` 互為交棒對端——L-003 高分樣態成對出現。

## §ga 分歧:同一檔在條文兩讀下 approved ↔ needs-revision

唯一的真判斷分歧(非事實錯誤):ga-methodology 的 L-004。

- **J(盲判,採計)**:序4 n/a——機制不存在,但「穩定演算法領域」載重宣稱缺席;
  `:381` 『cma/deap/optuna 均有穩定實作』裁定為非載重殘餘,`:364` 『快 3-10 倍』
  裁定為穩定經驗值不易腐。J 自己標明「嚴格存在量詞讀法會落序5,這是外推不是條文」。
- **呼叫端替代讀法(記錄,不採計)**:序5 poor——`:381` 是第三方生態狀態斷言、
  `:364` 是未附引用的量化領域主張,兩者裸露且無任何機制;照字面
  「機制不存在 + 載重宣稱裸露 → poor」→ rollup **needs-revision**。
- **裁定**:verdict 隨盲判(**approved**)。理由:此分歧完全落在 ledger 既有的
  「序5 存在量詞無 de-minimis 門檻」縫內(friction 回歸 G-F1/H#1/I#3 三方收斂 +
  B2 真實 2 例),屬條文未決的裁量帶;裁量帶內**由不知情者定值、由具名者記錄分歧**,
  否則盲判協定形同虛設。已在 ledger 該列補記第 3 個真實活化例。
- 對作者的實際建議不受分歧影響:給 `:364`/`:381` 補引用或改「以官方 benchmark 為準」
  一行即可讓兩讀法收斂到同一側。

## 交叉核對:andrej-karpathy-perspective(wave 3 獨立判 vs 本波集合抽樣)

wave 3(作者判,已揭露血統懷疑並降權):L-004 good 序1 強,證據=
`调研时间: 2026-04-05` frontmatter + 调研截止邊界 + 時效盲區。
本波 J(盲判,不知 wave 3 存在):同檔判入集合 L-004 good 序1,證據=
`:12/:18/:415` 調研截止 + `:110-114` CHECKPOINT 強制走研究。
**兩位判讀者、兩種語境(獨立 skill vs 集合子檔)、同一份檔、同向同序**——
wave 3 那次「揭露降權後仍 approved」得到盲判覆核。

## ⭐ 污染發現:名字可遮,內容指紋遮不掉

J 的 contamination 節是本波最重的判準發現:**criteria 的具名遮蔽(`local/███`)擋住了
名字,但條文引用樣張時抄進去的內容片段本身就是指紋**——四個對象有三個被 J 逐字定位:

| criteria 內的片段 | 指向 | 後果 |
|---|---|---|
| L-002 equivalent_forms 的 deletion test 描述(近逐字) | improve `:25` | 預寫其 L-002 答案 |
| 同段「Module/Interface/Depth/Seam/Adapter」五詞同序 | improve `:14-21` | 同上 |
| 同段「閾值表與替代優化器選擇指南=override 節」 | ga `:358-381` | 預寫其 L-002 答案 |
| L-003 domain_lookup_scope 的六子題清單 | ga 章節逐項 | 直接預寫其 L-003 答案 |
| L-003 sub_pattern_cross_skill 的逐字路徑 | improve `:68` / diagnose `:117` | 預寫兩檔 L-003 |

**影響**:diagnose/improve/ga 的 L-002、L-003 格是「**污染下的確認**」——J 各格另引了
獨立文內證據、方向皆與定錨一致,但不能當乾淨判讀;**huashu-nuwa 四維全冷判**。
這與 friction 回歸抓到的 ADHD 內容指紋(3.3.2 已修)同型,但**結構上更難修**:
那次是舉例可換掉,這次的指紋就是 evidence_refs 樣張被抄進條文當教材的本體。
已入 ledger 待處理(遮蔽工具需做到內容指紋層,屬設計題不屬反射修補)。

**盲判協定的邊界由此明確**:對 evidence_refs 具名樣張,遮名字只解決一半;
本波的 L-002/L-003 結論仍站得住(有獨立證據 + 三態同向),但下次再審樣張級對象,
判讀包必須先過內容指紋檢查。

## friction / contamination 處置

J 定稿 9 條 friction:4 條併入 ledger 既有列補記活化
(序5 de-minimis→既有列 +ga;probe 對象→既有列 +diagnose/improve 證據先行之問;
rule/pass_criteria 位階→既有列 +L-001 句式例;形狀表鍵→既有列 +persona/generator 例),
4 條新縫入 ledger(宿主平台詞彙 vs 第三方斷言;L-001 判別法症狀/技法同段誤傷;
L-002 override 位階矛盾;collection_aggregation 合成客體+序號寫法),
1 條(J#4 句式)併入位階列。內容指紋污染另立一列。
中途稿的 5 條 friction **全數作廢**(建立在編造的檔案內容上)。

## B2 收官(19/19)

| verdict | skills |
|---|---|
| approved | triage, grill-me†, to-issues(w1);to-prd, zoom-out, humanizer-en(w2);archify, andrej-karpathy-perspective†, grill-with-docs(w3);**diagnose‡, improve-codebase-architecture‡, ga-methodology‡◊, huashu-nuwa‡**(w4 盲判) |
| approved-with-notes | security-weekly-tw(w1), ai-stack-writeup(w3) |
| needs-revision | asp(w1), write-a-skill(w2), caveman(w2), anysearch(w3) |

† = 具名定錨已揭露降權;‡ = 遮蔽盲判(其中 diagnose/improve/ga 的 L-002/L-003 為
污染下的確認,huashu 全冷判);◊ = verdict 在條文兩讀下不穩定(見 §ga 分歧)。

**B2 總結**:19 個 skill,13 approved(內 2 帶降權揭露、3 帶污染標記)、
2 approved-with-notes、4 needs-revision。四個 NR 各有可指認的真實缺陷
(asp/anysearch 的意圖收編觸發、write-a-skill 的 500-vs-100 行內部矛盾、
caveman 的 ~75% 裸數字);其中意圖收編 ×2 與序5 邊界案(ga 分歧)同時活化了
ledger 既有縫——**真實使用把 friction 回歸預測的縫逐一踩實,且 19 例中
未出現縫外的新失效型**。縫的修訂已蓄積至批次門檻,見 misjudgments.md。
