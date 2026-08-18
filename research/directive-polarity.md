# 指令極性與舉例:五條否證路徑,與一條不該變成判準的機制

> **這份文件回答什麼**:優質 skill 裡「正向/白名單」指令與「負向/黑名單」指令的比例是多少?
> 這個比例能不能當成判斷 skill 品質的變數?以及追問——**它是不是其實跟「有沒有舉例」是同一件事?**
>
> **為什麼值得寫下來**:答案是「不能當變數」,而否證它花了四條獨立路徑。
> 把否證過程留下,是為了讓下一個問同樣問題的人**不必重跑**。
> 這是本檔的主要價值,不是那個數字。

日期:2026-08-18 · rubric 影響:見 §9

---

## 1. 結論(先講)

1. **若一定要一個數字**:craft 評級為 good 的 skill,正向:負向 ≈ **1.75 : 1**(中位 1.74),
   負向密度約 5.7 個/1k 字。粗略是「正向 2 : 負向 1」。
2. **但這個數字不能拿來判品質。** craft-good 組內部全距 **74×**(0.50:1 ↔ 37:1);
   全語料**最正向**的 repo(5.12:1)評級是 mixed,而標竿 `obra/superpowers`(1.05:1)
   幾乎對半。比例追蹤的是 **skill 型態**(紀律型 vs 查表型),不是品質。
3. **極性與舉例不是兩個變數,是同一個結構的兩個側面。** 一個 `Bad: X / Good: Y`
   **同時是**一個舉例、也是一組負向配正向。分開計數等於把同一性質用兩個有損鏡頭各數一次。
4. **四個確定性代理指標全部不分層**,且在最好的樣本上 **regex 與人類判讀相反**(§5)。
5. **條件式判準(§7)是好的寫作建議,但不是可用的審查判準。**
   10 個 repo × 5 位盲審的校準顯示,把「形式↔失效型態」做成機械配對規則後,
   結果**反向**:craft-good 的 `blader` 拿到 60% 不匹配,craft-mixed 的 `Jeffallan` 只有 12%
   (§9)。三位審查者**獨立**診斷出同一個原因——禁令是否有害,
   **不取決於它配的失效型態,取決於有沒有附上已完成的替代示範**。
6. **最終處置:rubric 不動,`rubric_version` 維持 2.1.0。**
   §9.3 收斂到的那條機制已經是 L-002 的原文(「附 Bad/Good 對照例或等價替代」),
   沒有東西需要補。**本文的產物是否證路徑,不是新判準。**

---

## 2. 語料與「優質」的操作型定義

| 項目 | 內容 |
|---|---|
| 語料 | `research/inter-rater/corpus/`(15 repos / 61 SKILL.md)+ `research/repos/`(5 repos / 156 SKILL.md) |
| 覆蓋率限制 | 全 80 repo 中**只有 ~19 個有本地全文**;`skill_details.json` **不含 body**(只有 path/name/lines/desc_len/description_head) |
| 「優質」定義 | `research/qualitative_notes/*.md` 的 **`寫作風格`** 欄(good 38 / mixed 15 / poor 1,n=54)。**刻意不用星數**——本專案已證實星數關聯 packaging 非 craft |
| 可用於比較者 | 有本地全文**且**有 craft 評級:**14 good / 4 mixed** |

⚠️ **統計效力的誠實聲明**:14 vs 4 撐不起任何檢定。
`inter-rater-results-round2.md` 已用數字證明此規模解析不出判準效果(每維度需 n≈404,用光母體差 7.6 倍)。
本文所有比較的定位是**存在證明與機制**,不是統計推論。文中不出現 p 值,也不應該有人從這裡推出門檻。

---

## 3. 若一定要一個數字

| craft | repos | pooled | 中位 | 全距 | 負向密度 |
|---|---|---|---|---|---|
| good | 14 | **1.75 : 1** | 1.74 : 1 | **0.50 – 37.0** | 5.7 /1k字 |
| mixed | 4 | 4.63 : 1 | 2.36 : 1 | 0.33 – 5.12 | 3.4 /1k字 |

方向上高工藝反而**負向更密**(5.7 vs 3.4),與「正向提示較好」的直覺相反。但 n=4,不可據此下結論。

---

## 4. 四個確定性代理指標,全部不分層

全部依 craft 評級分組(中位數),非星數分層:

| # | 指標 | good | mixed | 判定 |
|---|---|---|---|---|
| 1 | 正負比例 | 1.74 : 1 | 2.36 : 1 | 全距 0.50–37 vs 0.33–5.12,完全重疊 |
| 2 | 裸禁令率(禁令後 3 行內無替代/理由) | **66.7%** | 47.4% | good **反而更高**;全距 39–100% vs 36–83%,重疊 |
| 3 | **舉例密度**(code 塊/1k字) | 4.0 | **5.8** | mixed **反而更多**;兩組 **100%** 都有例子 |
| 4 | **規則級物證掛載率**(規則鄰域有理由/例子/替代) | 38.3% | 33.9% | 全距 0–70.8% vs 15.9–51.9%,重疊 |

四個指標中有兩個(#2、#3)方向與假說**相反**,另兩個全距重疊。
在 §5.1 揭露「單位切錯」之後,這正是一個壞量測該有的樣子——
不是訊號微弱,是分母根本不對。

另有一條**定義敏感度**問題:同一份語料,換個合理定義比例就差 **2.2×**——

| 操作型定義 | pos : neg |
|---|---|
| 詞彙 marker 計數 | 1.43 : 1 |
| 指令行計數(僅 bullet / 表格列 / 粗體規則) | 0.64 : 1 |

一個「變數」的值會因為「怎麼算才叫一條指令」這種可辯護的重新定義而跨越決策邊界,
它就不是量測,是旋鈕——等於交給每個後續審查者一個**不改動 skill 就能移動分數**的手段。

### 三個端點案例(比例與 craft 正交)

| repo | 比例 | craft | 質化筆記怎麼說 |
|---|---|---|---|
| `Jeffallan__claude-skills` | **5.12 : 1**(全語料最正向) | **mixed** | 「MUST 清單多為**裸斷言、少講 why**」,證據 `MUST NOT DO: Mutate state directly / Use array index as key / Skip error boundaries in production`(無任何解釋) |
| `kepano__obsidian-skills` | **37 : 1**(近乎零負向) | good | 查表型 reference skill,「會標注具體 pitfall **而非堆 MUST**」 |
| `obra__superpowers` | **1.05 : 1**(近乎對半) | good(標竿) | 「MUST/NEVER 密度高但**幾乎每條都附** rationale、反例表、好壞對照範例」 |

**最正向的是 mixed,最對半的是標竿。**

---

## 5. ⚠️ regex 在最好的樣本上與人類判讀**相反**

這是本文最重要的方法論發現,也是為什麼確定性層不值得出貨。

| repo | 我的 regex | 分析師實際讀到 |
|---|---|---|
| `blader__humanizer` | 4.3% 掛載率 | 「33 個 pattern **每條都是**『Words to watch + Problem(why)+ Before/After 實例』三件套」 |
| `ayghri__i-have-adhd` | **0%** 掛載率 | 「10 條規則,**每條附 Bad/Good 對照例**」,證據 `Bad: "This will take some work." Good: "About 15 minutes if tests already cover this."` |
| `obra__superpowers` | 84% 判為裸禁令 | 「**幾乎每條都附** rationale、反例表、好壞對照範例,**不是裸堆疊 MUST**」 |

三例都是抽樣核對後**人工對、regex 錯**。

### 5.1 根因:「什麼算一條規則」這個**單位**本身不可 regex 化

追查 `blader` 那個 4.3% 找到了根因,它比「配對偵測不準」更根本。
blader 的規則實際長這樣:

```
### 1. Inflated claims about importance and legacy
**Words to watch:** stands/serves as, is a testament, a pivotal role, …
**Problem:** AI writing often claims that ordinary details mark a major change…   ← why
**Before:** > The Statistical Institute of Catalonia was officially established in 1989, marking a pivotal moment…
**After:**  > The Statistical Institute of Catalonia was established in 1989, part of a wider decentralization…
```

**規則本體是一個編號標題,裡面一個祈使詞都沒有。**
我的 regex 只認「含 must / never / should / avoid 的行」,
所以它根本沒在量 blader 的 33 條 pattern——量的是散落各處的另一批句子,
而那批句子確實較少附例。**量錯了單位,不是量得不準。**

同一個抽象物件,語料裡至少三種互不相容的結構慣例:

| repo | 一條規則的載體 | 祈使詞? |
|---|---|---|
| `blader__humanizer` | 編號標題 + `Words to watch / Problem / Before / After` 四段模板 | 無 |
| `obra__superpowers` | 粗體祈使句 + 鄰近 rationalization table | 有 |
| `Jeffallan__claude-skills` | `MUST DO:` / `MUST NOT DO:` 項目清單 | 有 |

→ 這解釋了 §4 四個指標為何**同時**失敗:
**你無法計數一個你無法可靠切分的東西。** 分母錯了,四個比率就都錯了。

---

## 6. 極性與舉例是同一結構

分析師給出 craft-good 的理由,五個 repo 各自獨立,卻用了幾乎相同的三件套措辭:

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

它們不是相關的兩個變數,是**同一個物件的兩種數法**。這解釋了 §4 為何兩邊都是雜訊
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

其 head-to-head 措辭實驗:在**形狀型**問題上,禁令組產生的非預期內容明顯多於配方組
(**分佈完全分離**),且比**無指引對照組更差**。原文的告誡是
「micro-test your own case rather than assuming, but never reach for the prohibition by default」。

附帶兩條同源規則:
- **不要加 nuance 子句**:「Don't X unless it matters」會重啟談判——
  在同組實驗中,替勝出的配方加上單一 nuance 子句,就把它從穩定降級為不穩定。
- **例外條款不會限縮作用域**:「此限制不適用於 code block」仍然會抑制 code block。
  真要豁免,得重構到規則構不到它。

→ **這就是為什麼全域比例是錯的問法**:正確答案是條件式的,一個全域比例目標會摧毀這個條件。

### 7.1 一個**非 obra 血統**的獨立確證

`blader__humanizer`(craft-good,與 obra 無關聯)防守的正是典型的**形狀型失效**
——「文字讀起來像 AI」。而它採用的形式正是 obra 實驗處方的那一種:
**不是禁令清單,是四段正向模板**(`Words to watch / Problem / Before / After`),
33 條 pattern 無一例外。它的正負比例是 1.27:1,負向密度 4.6/1k 字——都不極端。

同理 `kepano__obsidian-skills`(craft-good,37:1 近乎零負向)是查表型,
防的是**遺漏型**失效,用的是 schema 表與必填欄位——也就是「結構化槽位」那一列。

→ 兩個獨立作者,各自面對不同失效型態,各自選了對照表所預測的形式,且都被評為 craft-good。
這是 §7 條件式的**外部確證**,不依賴 obra 自己的說法。

---

## 8. ⚠️ 收緊 regex 會讓它從測品質變成測作者

61 檔語料中,**43 檔**帶硬禁令(never/禁止/不得),53 檔帶任一禁令。
「配對替代構造」的普及率則**完全取決於你把 regex 收多緊**:

| 偵測定義 | 命中檔數 | 分佈 repo 數 | obra 系佔比 |
|---|---|---|---|
| **寬**:含任何對照標記(`❌` `✅` `<Bad>` `<Good>` `Instead` `Rather than`) | **41/61** | 15 | **7/41 = 17%** |
| **嚴**:緊鄰 `❌`→`✅` 配對,或 `<Bad>…<Good>` 區塊 | **3/61** | 3 | **2/3 = 67%** |

寬定義下配對是**常見**性質(67% 檔案、全部 15 個 repo 都有),obra 系毫不突出。
嚴定義下樣本塌到 3 檔,其中 2 檔屬 obra 系——**看起來像血統偵測器**。

**但這不是語料的性質,是量測的假象。** 把 pattern 收緊到只剩 3 個命中時,
其中兩個屬於同一作者是抽樣噪音,不是訊號。這是 §5 那個發現的又一次現身:
**每一次「把 regex 收緊到夠具體」的嘗試,都會讓樣本塌陷並開始偵測作者身分而非品質。**

⚠️ 實務推論(這才是要記住的):任何用確定性 pattern 做「禁令是否配對」門檻的設計,
都會落在這條光譜上——寬則抓到所有人、嚴則抓到 obra。**兩端都不是品質判準。**
若硬要出貨這種門檻,它會以 `docs/llm-judge-contamination.md` §1 的判準自我定錨形式復現,
而且**比在 LLM judge 裡更危險,因為它看起來客觀**。

> **紀錄一次修正**:本節初稿寫成「配對構造只出現在 9/61 檔,5/9 屬 obra 系」,
> 據此宣稱語料存在血統混淆。該數字來自一個未經我複驗的嚴定義量測,**是錯的**;
> 實測寬定義為 41/61、obra 系 17%。結論因此從「語料有血統混淆」
> 修正為「收緊 regex 會製造血統假象」——後者才是站得住的陳述。

---

## 9. LLM 校準:預先登記的否證條件觸發 → **不改 rubric**

§5 證明確定性層不可信,所以 §7 那條件式必須由 LLM 判讀才有意義。這一節是那個校準。

### 9.1 協定

10 個 repo(有本地全文且有 craft 評級者),派 **5 位獨立審查者**,每人 2 個(good/mixed 各一)。
審查者**不知道** craft 評級、**不知道**假說方向、**被禁止**讀 `qualitative_notes/` 與 `rubric*.yaml`。
每人以字母序取前 25 條規則(反挑櫻桃),逐條標記失效型態、所用形式,
以及 `has_reason` / `has_example` / `has_replacement` 三個獨立屬性。

**預先登記**(執行前寫定,見本專案計畫檔):排除 obra 系後,
若 good 組與 mixed 組的 form_mismatch 計數**目視重疊**(此 n 不容許 p 值),
則此訊號在本語料無鑑別力,**只留註記、不得進入裁決**。

### 9.2 結果

| repo | craft | 裸規則% | form_mismatch% | has_reason% | has_example% |
|---|---|---|---|---|---|
| `kepano__obsidian-skills` | good | 80 | 4 | 8 | 12 |
| `google__skills` | good | 32 | 0 | 24 | 48 |
| `blader__humanizer` | good | 24 | **60** | 60 | 60 |
| `ayghri__i-have-adhd` | good | 24 | 24 | 44 | 56 |
| `addyosmani__agent-skills` | good | 36 | 0 | 52 | 24 |
| `obra__superpowers` | good ⚠️ | 80 | 0 | 16 | 16 |
| `NevaMind-AI__memU` | mixed | 52 | 0 | 22 | 13 |
| `axtonliu__smart-illustrator` | mixed | 40 | 0 | 7 | 53 |
| `Jeffallan__claude-skills` | mixed | **96** | 12 | **0** | **0** |
| `earthtojake__text-to-cad` | mixed | 32 | 4 | 24 | 24 |

排除 obra 後的區間(good n=5 / mixed n=4):

| 指標 | good | mixed | 判定 |
|---|---|---|---|
| form_mismatch% | 0, 0, 4, 24, **60** | 0, 0, 4, 12 | **重疊,且 good 偏高(反向)** |
| 裸規則% | 24, 24, 32, 36, 80 | 32, 40, 52, 96 | 重疊 |
| has_reason% | 8, 24, 44, 52, 60 | 0, 7, 22, 24 | 重疊 |
| has_example% | 12, 24, 48, 56, 60 | 0, 13, 24, 53 | 重疊 |

**四個指標沒有一個分得開。否證條件觸發。**

還有一個更直接的反證:**標竿 `obra` 的 `has_reason` 只有 16%,低於四個 mixed 中的三個**;
裸規則率 80%,與 craft 最差的 `Jeffallan`(96%)同一量級。
若這些計數量的是工藝,標竿不該落在這個位置。

### 9.3 真正的產出:三位審查者獨立指認同一個機制

這比數字有價值,也是本節唯一值得保留的東西。

`shaping + prohibition` 這個機械配對規則,會在**最好的樣本上放假警報**:

> **blader 的審查者**:「15 條 pattern 在 (shaping+prohibition) 上全被標記為 form_mismatch
> ——但這其實是**假警報**:每一條都用 Before/After 示範了『該改成什麼樣』,
> 把裸禁令補成了帶範例的可執行指令。」
>
> **ayghri 的審查者**:「被機械標記的 6 個 form_mismatch 幾乎都是這些字串禁令
> ——**但它們其實都附了範例與替代,是良性的**,只是配對觸發旗標。」
>
> **Jeffallan 的審查者**:「B 的 form_mismatch 低只是因為它的失效型別本就以 discipline 為主、
> 天然適配 prohibition/recipe,**而非因為它寫得更完整**。」

→ **禁令是否有害,不取決於它配的失效型態,取決於有沒有附上已完成的替代示範。**
→ 而「附 Bad/Good 對照例**或等價替代**」**正是 L-002 現行條文的原文**。

### 9.4 兩個由審查者主動揭露的量測缺陷

依 `docs/llm-judge-contamination.md` 的作法,brief 裡留了主動揭露的空間,兩條都被用上了:

1. **循環性(已預期)** — obra 的審查者:「我是在用 obra 自家的分類法去評 obra 自家的 skill,
   `form_mismatch=0` 有一部分是**建構上必然**的、而非獨立證據。」
   它同時說明了自己的兩道防線,並指出「高 bare 數(20/25)就是我沒有一味替它擦脂抹粉的證據」。
2. **抽樣缺陷(未預期)** — 「嚴格字母序讓前 25 條全數來自 `brainstorming` 一檔,
   而 superpowers 招牌的 `prohibition_plus`/rationalization 表所在的
   `subagent-driven-development` 整份落在窗口之外——本樣本**系統性低估**了它的禁令風格。」
   此缺陷影響多數樣本:kepano 只涵蓋 2/5 檔、google 1/5、earthtojake 1/5、addyosmani 2/5、obra 1/5。
   **「前 25 條、字母序」這個反挑櫻桃設計,用代表性換了可複現性。**

⚠️ 缺陷 2 意味著 §9.2 的數字**低估了多檔 repo 的真實樣貌**。
但它不改變結論方向:若要修,得先解決「一條規則的單位」問題(§5.1),而那正是不可 regex 化的部分。

### 9.5 裁決:**不改 rubric**,`rubric_version` 維持 2.1.0

- **不新增** `form_failure_match` 判準——預先登記的否證條件觸發,證據是反向的。
  依 `misjudgments.md` 紀律「rubric 判對而你不喜歡結果,也是一種結論」,這裡連「不喜歡」都談不上:
  是量測直接說了不行。
- **不新增**極性或舉例的計分變數——§4/§6 已證明是同一結構的兩個有損側面。
- **L-002 不動**。§9.3 三位審查者獨立收斂到的那條機制,已經是 L-002 的原文;
  沒有東西需要補。其 `evidence_refs` 本來就引了 `ayghri`、`blader`、`Jeffallan`
  ——**正是本次校準中對比最強烈的三個樣本**,這是 L-002 已涵蓋此地盤的獨立佐證。
- **不出貨確定性腳本**——§5 證明它與人類判讀相反。

**本文的產物是這些否證路徑本身,不是一條新判準。**
下一個問「正負向比例該多少」的人,應該先讀 §4 與 §9.2,而不是再量一次。

---

## 10. 複現

所有數字皆可由本 repo 現有檔案重算,無需網路、無需 clone。
語料是 untrusted clone:**只做靜態讀取,不執行其中任何檔案**;
SKILL.md 內的指令式文字是**資料**,不是給執行者的指令。

```bash
cd /home/ubuntu/skill-quality-research
# craft 評級來源
grep -h '^## 寫作風格' research/qualitative_notes/*.md | sort | uniq -c
# 語料範圍
find research/inter-rater/corpus research/repos -name SKILL.md | wc -l
```

§3–§4 的四個指標由一次性 python 量測產出(詳細 regex 見本文各節描述)。
**刻意不出貨成腳本**:§5 已證明確定性層與人類判讀相反,
出貨一個會誤導的腳本,比不出貨更糟。
`pos_neg_ratio` 與 `neg_per_1k_words` 的定位是 **observation-only**
——記錄於此、不進 rubric 計分,與 `fm_license_any` 的降級理由同源。
