# 第三次誤判批次(2026-09-02,15 條)→ rubric 3.4.0 / 工具 2.3.3

蓄積來源:friction 回歸三方收斂 10 條(2026-09-02)+ B2 終波盲判 5 條(同日)。
觸發:達批次門檻上緣(15 條)且 B2 收官——縫已被真實使用踩實
(序 5 一次 verdict 翻面、意圖收編 2 真實例、statement_test 兩讀在盲判中實際出現)。

**處置分佈:15 條全數處置——12 條全動手、3 條部分動手**(不修半邊 3 處:
形狀表 generator 列、材料互用合成義務、同作者類推,皆單源/n=1 無實證;
移待測半邊 1 處:全自動指紋遮蔽)。
⚠️ 初版寫「13 動手、2.5 不修、2 個第二半移待測」——半列被重複計入不同分母、
待測半邊實為 1 處不是 2,加總 >15;**獨立複審 MEDIUM-2 抓出**,已改為逐列可加總的帳。
commit 訊息沿用了錯帳,無法改,以本檔為準。
lint_skill.py 零改動;工具版本 2.3.3 因 SKILL.md 形狀表與 mask 工具同車。

## 逐條處置

| # | 縫 | 處置 | 落點 |
|---|---|------|------|
| 1 | L-004 序 5 無比例感 + rule「高階加分項」自相矛盾(3 真實例,ga 一次 verdict 翻面) | ✅ 序 5 依「**刪去全部裸露載重宣稱,教學價值是否實質受損**」分支 poor/mixed,兩支必列裸露清單;rule 改「機制與載重宣稱的覆蓋」,pass_criteria 明寫「加分項指機制,非整維可有可無」 | decision_order 序 5、rule、pass_criteria |
| 2 | statement_test 原則句與「來源標註=弱形式」互斥(RinDig good↔n/a) | ✅ 來源標註**除名**於機制;效果改由 scope_of_perishable 承接(**已附引用主張不入易腐範圍**——引用把驗證責任交給來源);pass_criteria 強弱梯刪尾項 | statement_test、scope_of_perishable、pass_criteria |
| 3 | 機制/probe 對象未定(google 兩級擺幅;wave4 +2:證據先行紀律算不算) | ✅ 補**對象判別**單一提問(G-F11 三方收斂句:「宣稱失效時,機制會不會讓模型在行動前發現或聲明?」);「**證據先行紀律**」入算列(流程型 never-from-memory 等價)——批准 wave4 盲判 J 的寬讀,它與呼叫端獨立重導同向 | statement_test |
| 4 | equivalent_forms 相對路徑未限權威源(手抄快照可騙序 3) | ✅ 補「**標的須是權威源或機械產物**」;手抄快照的正確形式是 dated snapshot 歸序 2 | equivalent_forms |
| 5 | L-001 評估面(desc vs body)兩讀 | ✅ 新增 `evaluation_surface`:**只評 frontmatter description**(觸發抉擇唯一輸入);body 段記 findings | L-001 |
| 6 | 意圖收編無測試(asp/anysearch 2 真實例)+「非過寬」三段位階不一 + 跨維雙計無裁決 + wave4 句式問題 | ✅ 新增 `intent_capture` 判別(單一提問:「使用者說出該詞時,多數情境是不是在要這個 skill?」);craft_value_mapping 補「**基礎要件唯一出處=pass_criteria**」與「跨維瑕疵計主維一次」;pass_criteria 改「判實質不判句式」 | L-001、craft_value_mapping |
| 7 | 形狀表「一次性安裝」指南/腳本無判別 | ✅ 特徵欄補「skill **自身**裝完即棄;**教人安裝某物的指南不屬此列**」 | SKILL.md 形狀表 |
| 8 | 形狀表互動協定型以主題為鍵(ayghri 被抹 L-002;wave4 +2 persona 同病) | ✅ 兩列列鍵改「**無規則可解釋**」;⚠️ **generator/工廠型列刻意不加**——n=1(huashu),且 dispatcher+collection_sampling 路徑經盲判實測可行,增列是無實證的新判準 | SKILL.md 形狀表 |
| 9 | L-002 裸 MUST 劑量-反應線缺(三位各自發明門檻) | ✅ 新增 `mixed_boundary`:**位置判別**(裸段覆蓋核心規則=mixed;邊角=findings)——沿用 craft_value_mapping 已驗證的位置規則,不發明比例常數 | L-002 |
| 10 | 單源利刃 4 條(I#11 合取洞 / I#2 材料互用 / G-F5 序 3 部分覆蓋 / G-F14 同作者類推) | ✅(a)(c)動手:序 3 擴「**全面時效標注**」+ 部分覆蓋分流句(帶標注不再摔序 5);🚫(b)(d)**刻意不修**:單源、無第二實例,寫進去是無實證判準(L-002 exemption ⚠️ 政策) | decision_order 序 3;(b)(d) 不動 |
| 11 | scope_of_perishable 字面捕捉宿主平台詞彙(整類 agentic skill 結構性不可達) | ✅ 不算清單補**宿主平台操作詞彙**——批准 J 的裁定;同 L-002 查表型裁定的病,同一解法 | scope_of_perishable |
| 12 | L-001 判別法誤傷「症狀/解法同段」 | ✅ 補除外句:「同段測試只殺同義異寫,不殺異意同歸」 | disambiguation |
| 13 | L-002 rule 與 pass_criteria 對 override 位階矛盾(預防性) | ✅ override 出 rule 基礎清單,pass_criteria 明標「高分項非基礎」——騎在 #6 的位階統一上 | L-002 rule/pass_criteria |
| 14 | collection_aggregation 不一致客體 + 序號寫法無銜接 | ✅ 客體=**機制存在性**(位置/形式變異記 findings);寫法=逐樣本記序+聚合結論一行——**批准 J 實地發明並可行的慣例**,非憑空新設 | collection_aggregation |
| 15 | 內容指紋污染(名字可遮、指紋遮不掉;3/4 對象被盲判者定位) | ✅ 部分動手:**registry 9 條**入 rubric 檔尾 + mask 工具三件(產包剝除/命中警告/quote 漂移守衛,selftest 已在 CI);🔬 **全自動指紋遮蔽移待測**(把指紋段換 fallback 文字是否不損判讀語意,無語料可驗) | fingerprints registry、mask_rubric_for_raters.py |

## 負向驗證(實測輸出)

1. **指紋漂移守衛**:單獨改條文側的 quote(registry 不動)→ selftest
   `AssertionError: 指紋漂移(條文改寫後 registry 未同步):['improve-codebase-architecture: quote 已不存在於條文(刪掉後複雜度消失=pass-through…)']` ✅ 轉紅
2. **命中警告真跑**:wave4 樣本(4 標的 + grill-me)→ **9 條 ⚠️ 警告**
   (= registry 中 4 標的的全部條目;grill-me 無 registry 條目,正確無警告);
   輸出包 `grep -c "fp-registry|fingerprints:"` = **0**(剝除成功)
3. ⚠️ **首發突變無效自查**:第一次突變用 `sed` 全檔替換,同時改到條文與 registry
   **兩側**(同字串)→ 守衛看到的仍是一致狀態,**綠燈**;且當時誤用 `git checkout --`
   還原,把鏡像副本退回 HEAD(3.3.2、無 registry),連帶讓真跑測試在無 registry 的
   檔上空轉(0 警告)。兩者都不是守衛失效,是**測試自己壞掉**——改為全形引號錨定的
   單側突變 + `cp` 自正本還原後重做,才得到上面兩條有效輸出。
   與 3.2.0 收尾「兩個突變仍綠而那不是守衛失效,是突變無效」完全同型,故如實記。

## 勘誤:wave4 報告「huashu-nuwa 唯一全冷判」不成立

編 registry 盤點指紋時發現 **criteria 判讀包內本來就有 huashu 的兩處指紋**:
L-004 evidence_refs 的「調研截止日+時效盲區+誠實邊界三件套」敘述、
L-003 collection_sampling 的「16 份子 skill」——**兩處都在 J 讀過的包裡,
而 J 的污染稽核明寫『huashu 集合查無任何定錨』**。污染稽核者自己漏抓 2 處,
正是「指紋偵測不能靠人」的第二個證據(第一個是 3.3.2 前三位判讀者只在
撞上時才發現 ADHD 指紋)。wave4 報告已同批修正;huashu 的 L-003/L-004 應與
另三個對象同等標「污染下的確認」(其 L-004 判定仍站得住——呼叫端獨立驗了
~10 個檔內錨,但「冷判」宣稱撤回)。方向註記:兩處指紋皆正向,與 J 取值同向。

## 條文兩讀收斂驗算(ga-methodology)

3.4.0 後重走 ga 的 L-004:`:364`「快 3-10 倍」與 `:381`「均有穩定實作」仍是
無機制下的裸露載重宣稱(宿主詞彙除外條款不覆蓋它們——cma/deap/optuna 是第三方庫
不是宿主工具)→ 進序 5 分支判別:「刪去這兩處,skill 教學價值是否實質受損?」
否(全文 381 行的方法論不依賴它們)→ **mixed,列裸露清單**。
與 J 的 n/a 和呼叫端舊讀法的 poor 相比,新條文把兩讀(approved↔needs-revision)
收斂為單讀:dims good/good/good/mixed → rollup **approved-with-notes**。
⚠️ 依「判定用判定時之版本」原則,wave4 的 approved **不追溯改判**;此驗算只證明
縫已閉合,並供 skill 作者參考(補兩行引用即可回 good/序 1…實為序 4 n/a)。

## 這一批最值得記的一課

**污染稽核也是判讀,判讀就會漏。** J 在同一份包上抓到 6 處指紋、漏掉 2 處
(而且漏掉的恰是它判得最好的對象的);我首發的突變測試自己無效還亮綠燈。
兩件事同構:**偵測動作本身不構成證據,能轉紅的機械守衛才是**——所以指紋進
registry 由 selftest 釘住,而不是進「下次記得檢查」的散文。

## 獨立複審(land 前,唯讀 reviewer)

判定 **NEEDS_WORK(2 MEDIUM / 4 LOW)**;六個驗收標的中可追溯性、污染紀律、
一致性、判準內在一致四項過(「單純來源標註」三處說法同向、序 3/序 5 邊界無新縫、
CHANGELOG 逐項對 diff 無虛報)。反面發現與處置:

- **MEDIUM-1(已修)**:`fp_warnings()` 名字集合漏 owner 位——skill 名寫在
  owner 位的樣本會漏警告。已補三寫法比對 + selftest 負向 case;
  「quote 檢查逐檔自治」半邊**明文豁免**(registry 治理它所在檔,是設計,已註記於程式)
- **MEDIUM-2(已修)**:15 條帳不可加總(半列重複計入分母、待測半邊 1 誤記 2)——
  三份文件改為「12 全動手 + 3 部分動手」的逐列可加總寫法;
  **commit 訊息的錯帳無法改,以本檔為準**。這正是本 repo 追殺的
  「散文數字對不上實表」形態,由複審在 land 前攔下
- LOW-1(記錄):遮蔽包的 rubric.yaml 版本註解攜帶 3.4.0 條目名,輕微時間定錨,
  非具名非統計不違紀律;LOW-3/LOW-4(記錄):「主張/出處」用詞同義、
  序 5「教學價值」屬判讀裁量帶(兩支強制裸露清單使比例可覆核),
  下輪 friction 若收到兩讀分歧再錨定
