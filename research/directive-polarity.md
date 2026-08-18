# 指令極性與舉例:五條否證路徑,與一條不該變成判準的機制

> **這份文件回答什麼**:優質 skill 裡「正向/白名單」指令與「負向/黑名單」指令的比例是多少?
> 這個比例能不能當成判斷 skill 品質的變數?以及追問——**它是不是其實跟「有沒有舉例」是同一件事?**
>
> **為什麼值得寫下來**:答案是「不能當變數」,而否證它花了五條獨立路徑。
> 把否證過程留下,是為了讓下一個問同樣問題的人**不必重跑**。
> 這是本檔的主要價值,不是那個數字。

日期:2026-08-18 · rubric 影響:**無**(見 §9.5)· 修正紀錄見 §11

---

## 1. 結論(先講)

1. **沒有一個有意義的絕對比例。** 換一組同樣說得通的 marker,craft-good 的 pooled 比例
   在 **0.43 : 1 到 2.77 : 1** 之間擺動(**6.4×**,§3.2)。
   任何單一數字都是 marker 選擇的產物,不是語料的性質。
2. **但方向是穩健的,而且與直覺相反**:五組 marker 定義**全部**顯示
   craft-good 比 craft-mixed **更偏負向**(§3.2)。高工藝的 skill 禁令更密,不是更少。
3. **比例不能當判準。** craft-good 組內全距 **74×**;而且比例追蹤的是
   **skill 型態**(紀律型 vs 查表型),不是品質(§3.3)。
4. **極性與舉例不是兩個變數,是同一個結構的兩個側面。** 一個 `Bad: X / Good: Y`
   **同時是**一個舉例、也是一組負向配正向(§6)。
5. **失敗的根因不是量得不準,是「什麼算一條規則」這個單位不可 regex 化**(§5.1)。
   分母錯了,所有比率就都錯了。
6. **§7 的條件式(形式要對上失效型態)是好的寫作建議,但不是可用的審查判準。**
   10 repo × 5 位盲審的校準結果**反向**,預先登記的否證條件觸發(§9)。
7. **最終處置:rubric 不動,`rubric_version` 維持 2.1.0。**
   三位盲審獨立收斂到的機制(「禁令是否有害取決於有沒有附替代示範」)
   **已經是 L-002 的原文**,沒有東西需要補。

---

## 2. 語料與「優質」的操作型定義

| 項目 | 內容 |
|---|---|
| 語料 | `research/inter-rater/corpus/`(15 repos / **61** SKILL.md)+ `research/repos/`(5 repos / 156 SKILL.md) |
| ⚠️ 去重 | 那 61 檔中只有 **59 份唯一文件**——`blader` 與 `ayghri` 各有一組逐位元組重複。去重後所有結論方向不變 |
| 覆蓋率限制 | 全 80 repo 中**只有 19 個有本地全文**;`skill_details.json` **不含 body** |
| 「優質」定義 | `research/qualitative_notes/*.md` 的 **`寫作風格`** 欄,n=54 |
| ⚠️ 評級分佈 | 原始標籤:`good` 38、`mixed` 14、`mixed(偏 poor)` 1、`poor→mixed` 1。**沒有任何一份被評為單純 `poor`**;本文一律以 good(38)vs 非-good(16)理解 |
| **納入本文比較者** | 有本地全文**且**有 craft 評級 = **14 good / 4 mixed**(§3.1 完整列出,無其他門檻) |

⚠️ **統計效力的誠實聲明**:14 vs 4 撐不起任何檢定。
`inter-rater-results-round2.md` 已用數字證明此規模解析不出判準效果(每維度需 n≈404,用光母體差 7.6 倍)。
本文所有比較的定位是**存在證明與機制**,不是統計推論。文中不出現 p 值,也不應該有人從這裡推出門檻。

---

## 3. 比例

### 3.1 定版數字(marker set A,見 §10;納入規則:有全文+有評級,無門檻)

| craft | repo | pos | neg | ratio |
|---|---|---|---|---|
| good | `kepano__obsidian-skills` | 37 | 1 | **37.00** |
| good | `google__skills` | 192 | 58 | 3.31 |
| good | `shanraisshan__claude-code-best-practice` | 19 | 7 | 2.71 |
| good | `jnMetaCode__superpowers-zh` | 13 | 6 | 2.17 |
| good | `anthropics__skills` | 422 | 195 | 2.16 |
| good | `affaan-m__ECC` | 27 | 14 | 1.93 |
| good | `JimLiu__baoyu-skills` | 117 | 64 | 1.83 |
| good | `addyosmani__agent-skills` | 93 | 56 | 1.66 |
| good | `browser-act__skills` | 68 | 50 | 1.36 |
| good | `blader__humanizer` | 56 | 44 | 1.27 |
| good | `obra__superpowers` | 112 | 107 | 1.05 |
| good | `JuliusBrussee__caveman` | 27 | 45 | 0.60 |
| good | `RinDig__icm-architect` | 6 | 10 | 0.60 |
| good | `ayghri__i-have-adhd` | 15 | 30 | **0.50** |
| mixed | `Jeffallan__claude-skills` | 568 | 111 | 5.12 |
| mixed | `earthtojake__text-to-cad` | 82 | 22 | 3.73 |
| mixed | `NevaMind-AI__memU` | 6 | 6 | 1.00 |
| mixed | `axtonliu__smart-illustrator` | 1 | 3 | 0.33 |

| craft | n | pooled | 中位 | 全距 | 負向密度 |
|---|---|---|---|---|---|
| good | 14 | 1.75 : 1 | 1.74 : 1 | 0.50 – 37.0(**74×**) | 5.7 /1k字 |
| mixed | 4 | 4.63 : 1 | 2.36 : 1 | 0.33 – 5.12(15×) | 3.4 /1k字 |

### 3.2 ⚠️ 這些數字對 marker 選擇極度敏感(6.4×)

同一份語料、同一個納入規則,只換 POS marker 集合:

| marker set(POS 部分,NEG 固定) | good pooled | good 中位 | mixed pooled |
|---|---|---|---|
| A `always/must/should/prefer/required/ensure/use` | 1.75 | 1.74 | 4.72 |
| B 拿掉 `use` | 0.84 | 0.62 | 1.62 |
| C 只留 `always/must/required` | 0.58 | 0.43 | 1.42 |
| D 再加 `do/make/run` | 2.77 | 2.59 | 7.06 |
| E 只留 `always/must` | 0.43 | 0.31 | 1.35 |

→ **good pooled 擺動 0.43 – 2.77 = 6.4×。單一數字沒有意義。**
(此表的納入門檻為 `pos+neg ≥ 10`,故 mixed 欄與 §3.1 略異——axtonliu 被排除。
 這正是「未言明的門檻會改變數字」的實例,故一併揭露。)

→ **但方向穩健**:**5/5** 組定義下 mixed pooled 都高於 good pooled,
即 **craft-good 一致更偏負向**。這是本節唯一可靠的結論。

### 3.3 比例與 craft 正交 —— 三個端點案例

| repo | 比例 | craft | 質化筆記怎麼說 |
|---|---|---|---|
| `kepano__obsidian-skills` | **37 : 1(全語料最正向)** | good | 查表型 reference skill,「會標注具體 pitfall **而非堆 MUST**」 |
| `Jeffallan__claude-skills` | 5.12 : 1(**mixed 組最正向**) | **mixed** | 「MUST 清單多為**裸斷言、少講 why**」,證據 `MUST NOT DO: Mutate state directly / Use array index as key / Skip error boundaries in production`(無任何解釋) |
| `obra__superpowers` | 1.05 : 1(近乎對半) | good(標竿) | 「MUST/NEVER 密度高但**幾乎每條都附** rationale、反例表、好壞對照範例」 |

比例榜首(kepano)與近乎墊底(ayghri 0.50、obra 1.05)**都是 craft-good**;
mixed 組最正向的 Jeffallan(5.12)比八個 good repo 都更正向。
**比例追蹤的是 skill 型態(紀律型 vs 查表型),不是品質。**

---

## 4. 其他三個確定性代理指標,同樣不分層

全部依 craft 評級分組,**與 §3 同一納入規則(有全文+有評級,無門檻)**,中位數:

| # | 指標 | good (n=14) | mixed (n=4) | 判定 |
|---|---|---|---|---|
| 1 | 裸禁令率(禁令後 3 行內無替代/理由) | **65.8%**(0–100) | 41.7%(33–83) | good **反而更高**;全距重疊 |
| 2 | 舉例密度(**fenced code 塊**/1k字) | 4.0 | **5.8** | mixed **反而更多** |
| 3 | 規則級物證掛載率(規則鄰域有理由/例子/替代) | **17.9%**(0–54) | 45.4%(10–100) | good **反而更低**(且見 §5.1:此指標量錯單位) |

⚠️ **納入門檻會改變這些數字。** 早期草稿對指標 1、3 各自加了「禁令數 ≥5」「規則數 ≥10」的門檻,
得到 66.7% / 38.3% 等不同數值。本表一律**無門檻**,與 §3 一致。
一個獨立稽核用它自己的 regex 得到 60.5% / 18.9%——**方向全部相同,絕對值不同**。
這本身就是本文的結論之一。

⚠️ 關於指標 2 的一個重要更正:**並非「兩組 100% 都有例子」**。
以 fenced code block 計,good 組只有 **12/14(86%)**——
`blader` 與 `RinDig` **零個 code block**。而 `blader` 正是本文引為「舉例最豐富」的標竿。
這反而**強化** §5 的論點:它的例子是 `Before:` / `After:` 的引用區塊,不是 code fence。
**連「什麼算一個例子」都無法用單一 pattern 認定。**

### 4.1 換「單位」的敏感度(受控比較)

同語料(61 檔)、同 marker set A,只變動「一條指令」的認定單位:

| 單位 | pos | neg | ratio |
|---|---|---|---|
| marker 出現次數 | 860 | 507 | 1.70 : 1 |
| 指令行(bullet / 表格列 / 粗體規則 / 標題) | 348 | 260 | 1.34 : 1 |

→ 單位造成 **1.27×** 擺動。比 §3.2 的 marker 選擇(6.4×)小,但同向疊加。

---

## 5. ⚠️ regex 在最好的樣本上與人類判讀**相反**

| repo | 我的 regex | 分析師實際讀到 |
|---|---|---|
| `blader__humanizer` | 4.3% 掛載率 | 「每條都是『Words to watch + Problem(why)+ Before/After 實例』」 |
| `ayghri__i-have-adhd` | **0%** 掛載率 | 「10 條規則,**每條附 Bad/Good 對照例**」,證據 `Bad: "This will take some work." Good: "About 15 minutes if tests already cover this."` |
| `obra__superpowers` | 84% 判為裸禁令 | 「**幾乎每條都附** rationale、反例表、好壞對照範例,**不是裸堆疊 MUST**」 |

三例都是抽樣核對後**人工方向對、regex 錯**。

⚠️ **但質化筆記本身也不精確**:它說 blader 有「33 個 pattern」且「每條都是」三件套。
實測是 **35 個**編號 pattern,其中 `Problem:`(why)**33/35**、`Before:` **33/35**、
但 `Words to watch` 只有 **11/35**。
**「三件套無一例外」是錯的**;可辯護的說法是「33/35 附 why、33/35 附 Before/After 對照」。
(此不精確亦已進入 `rubric-manual-dimensions.yaml` 的 L-002 `evidence_refs`
 ——「blader/humanizer(33 pattern 皆附 why)」;已記入 `misjudgments.md` 待處理,本 PR 不動 rubric。)

### 5.1 根因:「什麼算一條規則」這個**單位**本身不可 regex 化

blader 的規則實際長這樣:

```
### 1. Inflated claims about importance and legacy
**Words to watch:** stands/serves as, is a testament, a pivotal role, …
**Problem:** AI writing often claims that ordinary details mark a major change…   ← why
**Before:** > The Statistical Institute of Catalonia was officially established in 1989, marking a pivotal moment…
**After:**  > The Statistical Institute of Catalonia was established in 1989, part of a wider decentralization…
```

**規則本體是一個編號標題,裡面一個祈使詞都沒有**(35 條中 34 條如此;唯一例外
`8. Avoiding is and are` 的 "Avoiding" 是描述被禁對象,不是祈使)。
我的 regex 只認「含 must / never / should / avoid 的行」,在此檔只找到 **24 行**
——與那 35 條 pattern **是兩個不同的母體**。**量錯了單位,不是量得不準。**

同一個抽象物件,語料裡至少三種互不相容的結構慣例:

| repo | 一條規則的載體 | 祈使詞? |
|---|---|---|
| `blader__humanizer` | 編號標題 + `Words to watch / Problem / Before / After` 欄位 | 無 |
| `obra__superpowers` | 粗體祈使句 + 鄰近 rationalization table | 有 |
| `Jeffallan__claude-skills` | `MUST DO:` / `MUST NOT DO:` 項目清單 | 有 |

→ 這解釋了 §3/§4 的指標為何**同時**失敗:
**你無法計數一個你無法可靠切分的東西。** 分母錯了,所有比率就都錯了。

---

## 6. 極性與舉例是同一結構

分析師給出 craft-good 的理由,五個 repo 各自獨立,卻用了幾乎相同的措辭:

| repo | craft | 分析師的用語 |
|---|---|---|
| `obra__superpowers` | good | 附 rationale、**反例表**、**好壞對照範例** |
| `ayghri__i-have-adhd` | good | 先給 5 條 why,再推 10 條規則,**每條附 Bad/Good 對照例** |
| `blader__humanizer` | good | Words to watch + **Problem(why)** + **Before/After 實例** |
| `kepano__obsidian-skills` | good | **CORRECT/WRONG 對照與原因** |
| `Jeffallan__claude-skills` | **mixed** | **裸斷言、少講 why** |

一個 `Bad: X / Good: Y` **同時是**:
- 一個具體舉例(「有舉例 AI 較不會出錯」的那個舉例);
- 一組負向指令配上正向替代(極性配對)。

它們不是相關的兩個變數,是**同一個物件的兩種數法**。這解釋了 §3/§4 為何兩邊都是雜訊
——分開計數是把同一性質透過兩個有損鏡頭各數一次。

**共同的潛在變數**:每條規則有沒有帶著「讀者照做所需之物」——理由、替代、或已完成的對照案例。
而這個性質**只有讀者看得見**,§5 已證明它不可 regex 化。

---

## 7. 一手來源:形式要對上失效型態(附對照實驗)

`research/inter-rater/corpus/obra__superpowers/skills/writing-skills/SKILL.md` L459–474
「Match the Form to the Failure」:

| 基線失效 | 該用的形式 | 不該用的形式 |
|---|---|---|
| 壓力下明知故犯(紀律型) | 禁令 + rationalization table + red flags | 軟性建議(prefer / consider) |
| 有照做但**輸出形狀**錯(冗長、埋沒結論、複述 spec) | **正向配方/契約**:直述輸出「是什麼」及其順序 | 禁令清單 |
| 漏掉必要元素 | **結構化**:模板裡的 REQUIRED 欄位/槽位 | 模板旁的散文提醒 |
| 行為該視條件而定 | 綁**可觀察述詞**的條件句 | 無條件規則 + 例外條款 |

其 head-to-head 措辭實驗(L470):在**形狀型**問題上,禁令組產生的非預期內容明顯多於配方組
(**fully separated distributions**),且「**trended** worse than even the no-guidance control」
(原文用了 trended 這個保留詞,本文照錄)。原文的告誡是
「micro-test your own case rather than assuming, but never reach for the prohibition by default」。

附帶兩條同源規則(L473–474):
- **不要加 nuance 子句**:「Don't X unless it matters」會重啟談判——
  在同組實驗中,替勝出的配方加上單一 nuance 子句,就把它從穩定降級為不穩定。
- **例外條款不會限縮作用域**:「此限制不適用於 code block」仍然會抑制 code block。

→ **這就是為什麼全域比例是錯的問法**:正確答案是條件式的,一個全域比例目標會摧毀這個條件。

### 7.1 一個**非 obra 血統**的獨立確證

`blader__humanizer`(craft-good,與 obra 無關聯)防守的正是典型的**形狀型失效**
——「文字讀起來像 AI」。而它採用的形式正是實驗處方的那一種:
**不是裸禁令清單,是欄位化的正向對照**(35 條 pattern 中 33 條附 `Problem`(why)、
33 條附 `Before`/`After` 逐字改寫)。它的比例是 1.27:1,負向密度 4.6/1k 字——都不極端。

同理 `kepano__obsidian-skills`(craft-good,37:1 近乎零負向)是查表型,
防的是**遺漏型**失效,用的是 schema 表與必填欄位——也就是「結構化槽位」那一列。

→ 兩個獨立作者,各自面對不同失效型態,各自選了對照表所預測的形式,且都被評為 craft-good。
這是 §7 條件式的**外部確證**,不依賴 obra 自己的說法。

---

## 8. ⚠️ 收緊 regex 會讓它從測品質變成測作者

61 檔語料中,**43 檔**帶硬禁令(`\bnever\b`/禁止/不得),**53 檔**帶任一禁令。
「配對替代構造」的普及率則**完全取決於你把 regex 收多緊**:

| 偵測定義 | 命中檔數 | 分佈 repo 數 | obra 系佔比 |
|---|---|---|---|
| **寬**:含任何對照標記(`❌` `✅` `<Bad>` `<Good>` `Instead` `Rather than`) | **41/61** | 15 | **7/41 = 17%** |
| **嚴**:緊鄰 `❌`→`✅` 配對,或 `<Bad>…<Good>` 區塊(≤500 字元) | **3/61** | 3 | **2/3 = 67%** |

寬定義下配對是**常見**性質(67% 檔案、全部 15 個 repo 都有),obra 系毫不突出。
嚴定義下樣本塌到 3 檔,其中 2 檔屬 obra 系——**看起來像血統偵測器**。

**但這不是語料的性質,是量測的假象。** 把 pattern 收緊到只剩 3 個命中時,
其中兩個屬於同一作者是抽樣噪音,不是訊號。這是 §5 那個發現的又一次現身:
**每一次「把 regex 收緊到夠具體」的嘗試,都會讓樣本塌陷並開始偵測作者身分而非品質。**

⚠️ 實務推論:任何用確定性 pattern 做「禁令是否配對」門檻的設計,
都會落在這條光譜上——寬則抓到所有人、嚴則抓到 obra。**兩端都不是品質判準。**

---

## 9. LLM 校準:預先登記的否證條件觸發 → **不改 rubric**

§5 證明確定性層不可信,所以 §7 那條件式必須由 LLM 判讀才有意義。這一節是那個校準。

### 9.1 協定(含實際執行與計畫的偏離)

10 個 repo,派 **5 位獨立審查者**,每人 2 個。
審查者**不知道** craft 評級、**不知道**假說方向、**被禁止**讀 `qualitative_notes/` 與 `rubric*.yaml`。
每人以字母序取**前 25 條**規則(反挑櫻桃),逐條標記失效型態、所用形式,
以及 `has_reason` / `has_example` / `has_replacement`。

⚠️ **兩處與計畫的偏離,如實記錄**:
1. 計畫預先登記「good/mixed **各半**」,實際執行為 **6 good / 4 mixed**
   ——第 5 位審查者拿到的是 `addyosmani`(good)+ `obra`(good),兩個都是 good。
2. 「前 25 條」對兩個 repo 不成立:`NevaMind` 全檔只有 **23** 條、
   `axtonliu` 只有 **15** 條(指示為「不足 25 則全取」,行為正確但 §9.1 原述不精確)。

**預先登記**(執行前寫定於計畫檔):排除 obra 系後,
若 good 組與 mixed 組的 form_mismatch 計數**目視重疊**(此 n 不容許 p 值),
則此訊號在本語料無鑑別力,**只留註記、不得進入裁決**。

### 9.2 結果

| repo | craft | n | 裸規則% | form_mismatch% | has_reason% | has_example% |
|---|---|---|---|---|---|---|
| `kepano__obsidian-skills` | good | 25 | 80 | 4 | 8 | 12 |
| `google__skills` | good | 25 | 32 | 0 | 24 | 48 |
| `blader__humanizer` | good | 25 | 24 | **60** | 60 | 60 |
| `ayghri__i-have-adhd` | good | 25 | 24 | 24 | 44 | 56 |
| `addyosmani__agent-skills` | good | 25 | 36 | 0 | 52 | 24 |
| `obra__superpowers` | good ⚠️ | 25 | 80 | 0 | 16 | 16 |
| `NevaMind-AI__memU` | mixed | 23 | 52 | 0 | 22 | 13 |
| `axtonliu__smart-illustrator` | mixed | 15 | 40 | 0 | 7 | 53 |
| `Jeffallan__claude-skills` | mixed | 25 | **96** | 12 | **0** | **0** |
| `earthtojake__text-to-cad` | mixed | 25 | 32 | 4 | 24 | 24 |

排除 obra 後的區間(good n=5 / mixed n=4):

| 指標 | good | mixed | 判定 |
|---|---|---|---|
| form_mismatch% | 0, 0, 4, 24, **60** | 0, 0, 4, 12 | **重疊,且 good 偏高(反向)** |
| 裸規則% | 24, 24, 32, 36, 80 | 32, 40, 52, 96 | 重疊 |
| has_reason% | 8, 24, 44, 52, 60 | 0, 7, 22, 24 | 重疊 |
| has_example% | 12, 24, 48, 56, 60 | 0, 13, 24, 53 | 重疊 |

**四個指標沒有一個分得開。否證條件觸發。**

另一個直接反證:**標竿 `obra` 的 `has_reason` 只有 16%,低於四個 mixed 中的兩個**
(NevaMind 22、earthtojake 24);裸規則率 80%,與 craft 最差的 `Jeffallan`(96%)同一量級。
若這些計數量的是工藝,標竿不該落在這個位置。

### 9.3 真正的產出:三位審查者獨立指認同一個機制

這比數字有價值,也是本節唯一值得保留的東西。

`shaping + prohibition` 這個機械配對規則,會在**最好的樣本上放假警報**:

> **blader 的審查者**:「15 條 pattern 在 (shaping+prohibition) 上全被標記為 form_mismatch
> ——但這其實是**假警報**:每一條都用 Before/After 示範了『該改成什麼樣』。」
>
> **ayghri 的審查者**:「被機械標記的 6 個 form_mismatch 幾乎都是這些字串禁令
> ——**但它們其實都附了範例與替代,是良性的**,只是配對觸發旗標。」
>
> **Jeffallan 的審查者**:「B 的 form_mismatch 低只是因為它的失效型別本就以 discipline 為主、
> 天然適配 prohibition/recipe,**而非因為它寫得更完整**。」

→ **禁令是否有害,不取決於它配的失效型態,取決於有沒有附上已完成的替代示範。**
→ 而「附 Bad/Good 對照例**或等價替代**」**正是 L-002 現行條文的原文**。

### 9.4 由審查者主動揭露的量測缺陷

依 `docs/llm-judge-contamination.md` 的作法,brief 裡留了主動揭露的空間,兩條都被用上了:

1. **循環性(已預期)** — obra 的審查者:「我是在用 obra 自家的分類法去評 obra 自家的 skill,
   `form_mismatch=0` 有一部分是**建構上必然**的、而非獨立證據。」
   它同時說明了自己的兩道防線,並指出「高 bare 數(20/25)就是我沒有一味替它擦脂抹粉的證據」。
2. **抽樣缺陷(未預期)** — 「嚴格字母序讓前 25 條全數來自 `brainstorming` 一檔,
   而 superpowers 招牌的 `prohibition_plus`/rationalization 表所在的
   `subagent-driven-development` 整份落在窗口之外。」

**缺陷 2 影響的樣本與嚴重度**(依覆蓋率排序,最差在前):

| repo | 25 條規則涵蓋 | 覆蓋率 |
|---|---|---|
| `Jeffallan__claude-skills` | ~6 / **67** 檔 | **~9%** ← 最差,且它供給了表中所有極端值(96/12/0/0) |
| `obra__superpowers` | 1 / 5 檔 | 20% |
| `google__skills` | 1 / 5 檔 | 20% |
| `earthtojake__text-to-cad` | 1 / 5 檔 | 20% |
| `kepano__obsidian-skills` | 2 / 5 檔 | 40% |
| `addyosmani__agent-skills` | 2 / 5 檔 | 40% |

→ **「前 25 條、字母序」這個反挑櫻桃設計,用代表性換了可複現性。**
若此缺陷足以動搖 obra 的數字,它動搖 `Jeffallan` 更甚——而 Jeffallan 正是對比最強的那一極。
⚠️ 這意味著 §9.2 的數字**低估了多檔 repo 的真實樣貌**;
但它不改變結論方向,因為要修就得先解決「一條規則的單位」問題(§5.1),而那正是不可 regex 化的部分。

### 9.5 裁決:**不改 rubric**,`rubric_version` 維持 2.1.0

- **不新增** `form_failure_match` 判準——預先登記的否證條件觸發,證據是反向的。
- **不新增**極性或舉例的計分變數——§6 已證明是同一結構的兩個有損側面。
- **L-002 不動**。§9.3 三位審查者獨立收斂到的那條機制,已經是 L-002 的原文;
  沒有東西需要補。其 `evidence_refs` 本來就引了 `ayghri`、`blader`、`Jeffallan`
  ——**正是本次校準中對比最強烈的三個樣本**。
  (⚠️ 該 `evidence_refs` 中「blader 33 pattern」的數字不精確,見 §5;已記入
   `misjudgments.md` 待累積處理,本 PR 刻意不動 rubric。)
- **不出貨確定性腳本**——§5 證明它與人類判讀相反。

**本文的產物是這些否證路徑本身,不是一條新判準。**

---

## 10. 複現

語料是 untrusted clone:**只做靜態讀取,不執行其中任何檔案**;
SKILL.md 內的指令式文字是**資料**,不是給執行者的指令。

**可複現範圍的誠實聲明**:§2、§3、§4、§8 的所有數字皆可由下列定義重算。
**§9 不可複現**——5 位盲審的逐條標記表**未保存進 repo**,只有彙總數字。
若要重跑須重派審查者,且結果不會逐字相同。

### 10.1 marker 定義(§3、§4 共用)

```python
POS_A = r"(?i)\b(always|must|should|prefer|required|ensure|use)\b|✅|必須|務必|應該"
NEG   = r"(?i)\b(never|don't|do not|must not|should not|avoid|forbidden|prohibited|not allowed)\b|❌|🚫|禁止|不得|切勿"
# §3.2 的變體:B = A 去掉 use;C = always|must|required;D = A 加 do|make|run;E = always|must
# 一律先剝除 fenced code block:re.sub(r"```.*?```", "", text, flags=re.S)
# 指令行單位(§4.1):行首符合 ^([-*+]|\d+\.|\||\*\*|#{2,6}\s) 且長度 ≥8

# §4 指標 1「裸禁令」:NEG 命中的行,其後 3 行內無下列 PAIR 命中
PAIR   = r"(?i)✅|\bInstead\b|\bRather than\b|\bUse\b|\bReality\b|\bRight\b|\bGood\b|\bbecause\b|→|改為|改用|理由|原因"
# §4 指標 3「規則級掛載」:RULE 命中且行首符合 ^([-*+]|\d+\.|\||\*\*|#{2,6}\s|[A-Z]) 的行,
#   其 [i-2, i+4] 視窗內有 GROUND 命中,或其後 3 行內有更深縮排的子項
RULE   = r"(?i)\b(must not|must|never|don't|do not|always|should not|should|avoid)\b|禁止|不得|必須|務必|應該"
GROUND = r"(?i)```|❌|✅|<Bad>|<Good>|\bbecause\b|\bwhy\b|\bfor example\b|\be\.g\.|\bInstead\b|\bReality\b|因為|理由|例如|範例|→"
# §8 的兩個配對定義
LOOSE  = r"(?i)❌|✅|<Bad>|<Good>|\bInstead\b|\bRather than\b"
STRICT = r"❌[^\n]*\n(?:[^\n]*\n){0,3}?[^\n]*✅|✅[^\n]*\n(?:[^\n]*\n){0,3}?[^\n]*❌|<Bad>[\s\S]{0,600}?<Good>"
```

⚠️ 這些 regex **本身就是本文否證的對象**(§5:它們與人類判讀相反)。
公開它們是為了讓數字可複現,**不是**建議任何人拿去當工具。

### 10.2 語料與納入規則

```bash
cd /home/ubuntu/skill-quality-research
# 語料範圍
find research/inter-rater/corpus research/repos -name SKILL.md | wc -l   # 217 = 61 + 156
# craft 評級原始標籤(注意有 : 與 ： 兩種冒號)
grep -hoE '^## 寫作風格[:：].*' research/qualitative_notes/*.md | sed 's/.*[:：] *//' | sort | uniq -c
```

納入規則:**repo 在上述兩棵樹之一有 SKILL.md,且 `qualitative_notes/` 有其 `寫作風格` 評級。無其他門檻。**
(§3.2 的變體表另加 `pos+neg ≥ 10`,已於該表註明——未言明的門檻會改變數字,這是實例。)

### 10.3 `observation-only` 的狀態

`pos_neg_ratio` 與 `neg_per_1k_words` **僅存在於本文件**,未註冊進
`rubric.yaml` 或 `aggregate_stats.py` 的 `feature_class`。
本文稱其為 observation-only 是**敘述性的,不是系統中的登記狀態**
——與 `fm_license_any`(有實際註冊)不同。若日後要讓此狀態具約束力,須實際登記。

---

## 11. 修正紀錄

本文件經一次獨立稽核(重算全部數字、不採信文中對自身 regex 的描述)。以下為被抓出並已修正者:

| # | 原本寫的 | 實際 | 處置 |
|---|---|---|---|
| 1 | 「配對構造 9/61,5/9 屬 obra 系 → 語料有血統混淆」 | 寬定義 41/61、obra 系 17% | 結論改為「**收緊 regex 會製造血統假象**」(§8) |
| 2 | 「`Jeffallan` 5.12:1 是**全語料最正向**」 | `kepano` 37:1 更高——**在同一張表裡自我矛盾** | 改為「mixed 組最正向」(§3.3) |
| 3 | 「blader **33** 條 pattern **無一例外**三件套」 | **35** 條;`Words to watch` 僅 **11/35** | 改為「33/35 附 why、33/35 附 Before/After」(§5、§7.1) |
| 4 | 「obra 低於四個 mixed 中的**三個**」 | **兩個** | 已改(§9.2) |
| 5 | 「定義敏感 **2.2×**」 | 該比較混淆了 marker set **與**檔案數(54 vs 61),非受控 | 拆為受控的**單位** 1.27×(§4.1)與 **marker set** 6.4×(§3.2) |
| 6 | 「兩組 **100%** 都有例子」 | 以 code block 計 good 僅 **86%**(blader、RinDig 為零) | 已改,並指出它**強化**了 §5(§4) |
| 7 | 「所有數字皆可由現有檔案重算」 | marker 集合從未公開;§9 審查者輸出未保存 | 公開全部 marker 定義,並聲明 §9 不可複現(§10) |
| 8 | §9.1「5 位審查者 good/mixed 各一」 | 實際 **6 good / 4 mixed**;兩個 repo 不足 25 條 | 如實記錄偏離(§9.1) |
| 9 | §9.4 缺陷清單漏列 `Jeffallan` | 其覆蓋率 ~9% 為最差,且供給所有極端值 | 補上完整覆蓋率表(§9.4) |
| 10 | 引 obra 實驗時漏掉 "trended" 保留詞 | 原文為 "**trended** worse" | 已照錄(§7) |
| 11 | 「61 檔」 | 含 2 組逐位元組重複,實為 **59 份唯一文件** | 已註明(§2) |
| 12 | 「poor 1」 | 無任何一份評為單純 `poor`,該標籤為 `poor→mixed` | 已註明(§2) |

**結論未因這些修正而改變**——所有群組層級的**方向**在 5 組 marker 定義下都複現,
§8 四個數字逐位複現,§7 一手來源逐行屬實,五段質化引文逐字屬實。
但**數字的精確度與可複現性有實質缺陷,已修**。
