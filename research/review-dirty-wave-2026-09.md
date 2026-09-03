# dirty 波審查報告(2026-09-03,熟成輪 2 Track B)

> rubric **3.6.2** / 工具 **2.3.9**。語料:`clone-manifest-dirty-wave.json`
> (7 髒標的反向選樣 + 7 篇安全主題中文文件);預登記 `dirty-wave-preregistration.md`
> 先 commit 後審。⚠️ 含具名 craft 證據,加入審查者禁讀清單。盲判另檔逐字。

## 總表(作者判;集合一律逐樣本 + 聚合)

| repo | SKILL× | L-001 | L-002 | L-003 | L-004 | verdict |
|---|---|---|---|---|---|---|
| agenticluke/claude-skill-benchmark-methodology-plus | 1 | good(NOT-for+管線觸發) | good(1-5 anchor+加減分表) | good | good(**序1 強**:Proven/Corroborated/Asserted/Inferred 四級 + evidence cutoff 紀律) | **approved** |
| viper0355/claude-skills-pack | 8(抽5) | good 5/5 | **mixed**(盲判修正:nano 用法傾倒 why≈0 → 樣本 mixed,3.6.2 實文聚合不再重判 → mixed;作者初判 good 屬鬆) | good(humanizer→zh-tw 顯式疊層路由) | **mixed**(4 序1 + nano-banana-pro **序5-實質→樣本 poor**;F8 句:單一序5樣本→聚合 mixed 記名) | **needs-revision**(盲判修正 AWN→NR) |
| rjgladish/claude-skills-pack | 25(抽5) | mixed(校正:Expert-in 樣本 desc=其核心觸發面 → 樣本 mixed → 聚合 mixed;作者初判 good+findings 屬鬆) | **poor**(5 樣本同產生器、~千行 config 傾倒、因果詞≈0;**集合「全同→該值」首個 poor**) | good | **poor**(**collection poor 句首開火**:大量工具斷言幾乎無機制,全集成立) | **needs-revision** |
| belentani7/claude-skills-pack | 9(抽5) | mixed(2/5 樣本「Expert in」零觸發情境) | mixed(gsap/token 零因果 vs writing-skills 有結構——任一 poor 封頂) | good | mixed(gsap 序5-實質 + token-optimizer desc 裸「60-90%」序5-殘餘;F8 記名) | **needs-revision** |
| wensia/ai-skills | 22(抽5) | good | good(zodiac 強調/避免對照;why 薄記 findings) | good | mixed(feishu/craft wrapper 樣本序5-實質 2-3 個;F8 記名) | **approved-with-notes** |
| MHDN55/claude-skills-pack(ECC 288 聚合) | 288(抽5) | good(When-to-Activate 齊) | **poor**(948 行級傾倒、因果≈1/千行,同質) | **mixed**(**L-003 首批非 good**:288 檔僅目錄分區、零路由/dispatcher——集合治理基礎未達) | **poor**(collection poor 句成立) | **needs-revision** |
| markschwandt/claude-skills-package | 332(抽5) | good | **poor**(894 行 4 因果詞) | **mixed**(同上,marketplace 打包有、路由無) | mixed(「proven」類無出處宣稱,F8 記名) | **needs-revision** |

**最終 1 approved / 1 AWN / 5 NR**(盲判裁決後;作者初判為 1/2/4——兩處作者判偏鬆被盲判與規則實文修正,均在 land 前)。 verdict 皆 `craft_verdict_rollup()`;
S-003(viper/nano-banana `--api-key` 第一優先+「use if user provided key in chat」)
複核**成立**(medium 級,與 anysearch 同類,warning 不翻 verdict);
S-002 registers_hooks ×2(兩巨獸)未逐一複核,記 findings 待有需要再查。

## 受測 rung(預登記 §2)——兩個零里程 rung 都拿到首里程

| rung | 開火 | 判讀 |
|---|---|---|
| **序 5 實質/殘餘分支** | **6+ 次**:nano-banana(實質→樣本 poor)、gsap(實質)、token-optimizer(殘餘:裸 60-90%)、rjgladish/MHDN55 多樣本(實質)、wensia wrapper 群 | **全數單讀**;「刪去後教學價值受損」判別在 wrapper 型(受損)與順帶宣稱(不受損)上給出可分辨答案 |
| 序 3 取低合成 | **0 次**(仍無「部分機械同步+部分裸露」案例) | **兩輪未釣到,依計畫停損:記「該失效型在真實生態罕見」,不再專門加碼**;自然使用中出現再收 |
| 集合聚合 L-001~L-003(3.6.2 首戰) | 多次:L-002「全同→該值」出首個 poor(rjgladish);「任一 poor 封頂」(belentani);單樣本傷及性(belentani L-001) | 單讀 ✓ |
| #2 表面限定 + F8 poor 邊界句 | **雙側開火**:單一序5樣本→聚合 mixed 記名(viper/wensia);大量幾乎無→聚合 poor(rjgladish/MHDN55) | 單讀 ✓,邊界句把兩側分得開 |
| intent_capture 包含關係判別 | 數次(全部組成物件側;無新收編案) | 單讀 |
| 塌掉測試消歧句 | 集合層不適用居多;未遇中間型 | LOW-3 觀察項未觸發 |

**L-003 零鑑別待測:解除證據到貨**——兩個巨獸聚合包給出首批非 good
(288/332 檔零路由=集合治理基礎未達,mixed 單讀)。該待測列可於下批結案。

## B4:S-101 假陽性量測(對抗性語料)

- 語料:7 篇注入/XSS/CSRF/上傳教學(LyleMi 筆記,rst;正是待測列害怕的 FP 面)
- 句級命中 **1**:`SECDOC__LyleMi_cmdi.md:104`「尽量不要执行外部的应用程序或命令」
  → 人工標 **FP**(對開發者的通用建議,非 skill 自我防禦條款)——**首個實錘 FP**
- 兩波合計 TP 1 / FP 1 / n=2,**遠低於 30 門檻 → 續停**;但方向數據有價值:
  待測列當年以構造句推出「整類命中」,**真實教學語料 7 篇僅 1 中**——
  2.2.0 三條件共現對真語料的抵抗力遠好於構造句攻擊所示。活化補記入待測列

## 誤判/friction(→ ledger)

1. **集合治理的 poor 門檻無錨**(MHDN55/markschwandt):L-003 mixed vs poor——
   「零路由但有目錄分區」算部分達成(mixed)或未達成(poor)?我取 mixed
   (目錄=弱治理形),嚴讀可 poor。**單源兩讀,值搖擺**,入 ledger
2. **vendored 滲漏類**(組包時實錘):語料含第三方衍生內容(viper vendor 了
   評語樣張級的第三方 skill),遮蔽清單只遮受審者名,**evidence_refs 正當具名的
   第三方與 vendored 副本對上=定錨**(其計數還可對檔數出)。本輪以「第三方名
   入遮蔽清單+數字類屬化」手工處理;規則化入 ledger
3. 協定偏離自查:belentani 的 token-optimizer 初判時未全文讀(違反本輪預登記
   「集合樣本一律全文讀」),補讀後**發現 desc 裸 60-90% 宣稱**、樣本序改
   殘餘→NR 不變——偏離被自查抓回,但證明該協定條款是必要的

## F4:誤判率讀數(預登記指標,方向訊號非量測)

| 輪 | 對象 | 新 ledger 列 | 率 |
|---|---|---|---|
| 2026-08-26 | 16 | 5 | 0.31 |
| B2 四波 | 19 | 5 | 0.26 |
| fresh 波(勘誤後) | 12 | 6 | 0.50 |
| **dirty 波** | **7** | **3** | **0.43** |

confound 照預登記;兩個抽查輪(0.50/0.43)穩定高於純作者輪——
再次印證「量測被抽查深度支配」;縫的絕對量在遞減(6→3)且本輪三條全是
**聚合/包裝協定層**,核心四維判準零新縫。

## 停損與里程結論

- 前 4 個髒標的:1 approved + 1 AWN + 2 NR → 餌到貨,不縮輪 ✓
- **序 5 分支:兩輪合計里程充足,判別穩定——該 rung 熟成**
- **序 3:兩輪零開火,依預登記停損記「罕見」,不再專門加碼**
- 3.6.2 新條文(集合聚合/F8/包含關係)首戰全單讀——**批次 4 的六刀在髒語料上站住了**

## 盲判抽查

抽選(開火最多前 2;MHDN55 依預登記血統迴避):**rjgladish** 與 **viper**。
前哨指定攻擊:2 處預登記語意標的 + vendored 滲漏面。逐字:`blind-craft-reviews-2026-09-dirty/`。

### 前哨:LEAK 1 中度 + 2 低度共鳴

- **L-1 實錘(vendored 滲漏類第 2 確認)**:L-002 evidence_refs 的類屬化描述
  (「pattern 清單+絕大多數附 why+Before/After」三要素)在 10 份語料**唯一映射**到
  vendored 的上游樣本——遮名+數字類屬仍擋不住結構描述。
  **修法採更徹底選項:判讀包整批剝除 evidence_refs(4 行)**,整類消滅——
  refs 是作者材料,判讀者不需要;M 判讀時自證「不影響判讀,反而乾淨」
- L-2/L-3:兩處預登記語意標的與本批**方向對不上或被 3.6.2 門檻句自我修正**
  ——語意監看標的首輪實測,防線設計有效
- 組包自查另先抓到一層:遮蔽清單原只有受審者名,vendored 上游名(evidence_refs
  正當具名)需**另行加入遮蔽清單**——已規則化入 ledger

### 判讀者 M vs 作者(終局三規則全程套用,零程序事故)

| 集合 | 作者初判 | M | 裁決後 |
|---|---|---|---|
| rjgladish | good/poor/good/poor | good†/poor/good/poor | **mixed**/poor/good/poor → NR(verdict 同) |
| viper | good/good/good/mixed | good/**mixed**/good/mixed | good/**mixed**/good/mixed → **NR**(AWN→NR) |

† M 的 rj L-001 good 出自一條**編造錨**(引「消費者載入該樣本即受害」——F7 已刪
的舊句,包內不存在;判讀者編造錨第 2 例,grep 即證)。拿掉編造錨後,
M 自己的樣本判(code-standards mixed)+ 3.6.2 實文聚合 → mixed;
作者初判 good+findings 同屬鬆。**兩位判讀者的鬆各被對方的實錨修正**——
L-002/L-004 兩維雙方全同;差異全在 L-001 聚合一格,且裁決後單讀。

### B5 讀數:兩個熟成判據

- **判準半邊:verdict-swinging 兩讀 = 0**——所有分歧均為值級且 verdict 經裁決
  收斂單一結果;3.6.2 六刀 + 3.6.1 判別句在髒語料上站住(F8 雙側、集合聚合、
  包含關係、序 5 分支全部單讀)✓
- **operator 半邊:B3 全程零程序事故**——前哨先行、包修先於派工、靜默期 ≥
  已跑時長、無中途稿誤採、判讀者編造錨被 grep 攔下、盲判修正在 land 前吸收 ✓

### friction / 誤判(→ ledger 3 列)

1. **集合路由治理的位階與 poor 門檻**(雙源:作者 + M friction #2;
   兩巨獸 mixed vs rj 的 good-帶-findings——「僅目錄清單」落點無錨)
2. **跨維雙計「用法傾倒」主維無裁定**(M friction #3;與舊單源利刃「材料互用」
   同族 → 升雙源):nano 同一事實計 L-002 mixed 又計 L-004 poor,
   跨維主維規則對此形無指引
3. **vendored 滲漏類規則化**(組包實錘 + 前哨 L-1):判讀包**常規剝除
   evidence_refs** + 語料含第三方衍生內容時上游名入遮蔽清單——入包裝協定
