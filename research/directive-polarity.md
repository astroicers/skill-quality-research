# 指令極性:為什麼這個比例不能當品質判準

> **問題**:優質 skill 裡「正向/白名單」指令與「負向/黑名單」指令的比例是多少?
> 能不能當成判斷品質的變數?以及:**它是不是跟「有沒有舉例」是同一件事?**
>
> **答案**:沒有有意義的絕對比例;不能當變數;而「舉例」與「極性」在**確定性量測上同樣失效**。
>
> **本文的價值是否證路徑,不是那個數字。** 寫下來是為了讓下一個問同樣問題的人不必重跑。

日期:2026-08-18 · rubric 影響:**無**(§8)· 本文經兩輪獨立 review,修正紀錄見 §10

> ⚠️ **給後續量測的隔離提示**:本文 §3、§6 公開了具名 repo 的 craft 評級。
> 若要再派審查者做一致性量測,**本檔須加入禁讀清單**
> (見 `inter-rater-protocol.md` §「必須隔離的東西」、`research/inter-rater/RATER-BRIEF-R2.md`)。

---

## 1. 結論

1. **沒有有意義的絕對比例。** 換一組同樣說得通的 marker,craft-good 的 pooled 比例
   在 **0.43 : 1 – 2.77 : 1** 之間擺動(**6.4×**,§3.2)。任何單一數字都是 marker 選擇的產物。
2. **但方向穩健,且與直覺相反**:五組 marker 定義**全部**顯示 craft-good 比 craft-mixed
   **更偏負向**。高工藝的 skill 禁令更密,不是更少。
3. **比例不能當判準**:craft-good 組內全距 **74×**,且榜首(37:1)與近墊底(0.50:1)都是 good。
   它追蹤的是 **skill 型態**(紀律型 vs 查表型),不是品質。
4. **「有沒有舉例」在確定性量測上同樣失效**,而且方向也反(§4)。
   `Bad: X / Good: Y` **同時是**一個舉例與一組極性配對——兩者不是獨立變數。
5. **`❌/✅` 配對構造在本語料中顯著集中於單一作者血統**(9/61 檔命中,5 個屬 obra 系,
   P=0.0039;去重後 8/59、5 個,P=0.0022)。任何以此為門檻的確定性設計,
   **實質上是血統偵測器**(§5)。
6. **LLM 盲審校準:預先登記的否證條件觸發**,四個指標沒有一個分得開,
   `form_mismatch` 甚至反向(§6)。
7. **處置:rubric 不動,`rubric_version` 維持 2.1.0**(§8)。

---

## 2. 語料、定義與效力

| 項目 | 內容 |
|---|---|
| 語料 | `research/inter-rater/corpus/`(15 repos / **61** SKILL.md,去重後 **59** 份唯一文件)+ `research/repos/`(5 repos / 156 SKILL.md) |
| 覆蓋率 | 全 80 repo 中只有 **19** 個有本地全文;`skill_details.json` **不含 body** |
| 「優質」定義 | `research/qualitative_notes/*.md` 的 `寫作風格` 欄,n=54。原始標籤:`good` 38、`mixed` 14、`mixed(偏 poor)` 1、`poor→mixed` 1(**無任何一份為單純 `poor`**) |
| 納入比較者 | 有本地全文**且**有 craft 評級 = **14 good / 4 mixed**,**無其他門檻** |

### ⚠️ 可複現性的誠實聲明(重要)

**本文多數數字在新 clone 上無法重算。** `.gitignore` 排除了
`research/repos/*` 與 `research/inter-rater/corpus/`(`git ls-files` 各為 1 與 0 檔),
語料**不在版控內**。§9 公開了全部 marker 定義,
但**執行它們需要先依 `research/clone-manifest*.json` 重建語料**。
§6 的逐條審查者標記表**未保存進 repo**,只有彙總數字——**該節不可複現**。

### ⚠️ 統計效力

14 vs 4 撐不起任何檢定。且 **mixed 組實質上是一個 repo**:
剝除 code block 後,該組共 41,738 字,其中 `Jeffallan` 佔 **34,747 字(83%)**,
另三者(`earthtojake` 5,320 / `NevaMind` 1,011 / `axtonliu` 660)合計不足 7,000 字。
「mixed pooled 4.63:1」基本上是 Jeffallan 自己的數字戴著組別的帽子。
good 組亦有對稱問題:`obra__superpowers` 與其中文 fork `jnMetaCode__superpowers-zh`
被當作兩個獨立點,而 §5 正是在排除這個血統。

**本文所有比較的定位是存在證明與機制,不是統計推論。** 文中不出現 p 值於分組比較
(§5 的 hypergeometric 是對「集中度」而非「分組差異」)。

---

## 3. 比例

### 3.1 定版數字(marker set A,見 §9;無門檻)

| craft | repo | pos | neg | ratio |
|---|---|---|---|---|
| good | `kepano__obsidian-skills` | 37 | 1 | **37.00** |
| good | `google__skills` | 192 | 58 | 3.31 |
| good | `shanraisshan__claude-code-best-practice` | 19 | 7 | 2.71 |
| good | `jnMetaCode__superpowers-zh` ⚠️obra系 | 13 | 6 | 2.17 |
| good | `anthropics__skills` | 422 | 195 | 2.16 |
| good | `affaan-m__ECC` | 27 | 14 | 1.93 |
| good | `JimLiu__baoyu-skills` | 117 | 64 | 1.83 |
| good | `addyosmani__agent-skills` | 93 | 56 | 1.66 |
| good | `browser-act__skills` | 68 | 50 | 1.36 |
| good | `blader__humanizer` | 56 | 44 | 1.27 |
| good | `obra__superpowers` ⚠️obra系 | 112 | 107 | 1.05 |
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
| mixed | 4 | 4.63 : 1 | 2.36 : 1 | 0.33 – 5.12 | 3.4 /1k字 |

⚠️ 74× 的上端由 `kepano` 的 **neg=1** 撐起(近零分母);
mixed 的 pooled 由 `Jeffallan` 主導(見 §2)。兩端都脆弱。

### 3.2 對 marker 選擇極度敏感(6.4×)

同語料、同納入規則,只換 POS marker 集合(NEG 固定):

| POS marker set | good pooled | good 中位 | mixed pooled |
|---|---|---|---|
| A `always/must/should/prefer/required/ensure/use` | 1.75 | 1.74 | 4.72 |
| B A 去掉 `use` | 0.84 | 0.62 | 1.62 |
| C 只 `always/must/required` | 0.58 | 0.43 | 1.42 |
| D A 加 `do/make/run` | 2.77 | 2.59 | 7.06 |
| E 只 `always/must` | 0.43 | 0.31 | 1.35 |

→ good pooled 擺動 **6.4×**。**單一數字沒有意義。**
(本表另加 `pos+neg ≥ 10` 門檻,故 mixed 欄與 §3.1 略異——`axtonliu` 被排除。
 未言明的門檻會改變數字,這是實例,故一併揭露。)

→ **但 5/5 組定義下 mixed pooled 都高於 good pooled。方向是本節唯一可靠的結論。**

### 3.3 比例與 craft 正交

| repo | 比例 | craft |
|---|---|---|
| `kepano__obsidian-skills` | **37 : 1(全語料最正向)** | good(查表型) |
| `Jeffallan__claude-skills` | 5.12 : 1(**mixed 組最正向**) | **mixed** |
| `obra__superpowers` | 1.05 : 1(近乎對半) | good |
| `ayghri__i-have-adhd` | 0.50 : 1(全語料最負向) | good |

**最正向與最負向都是 good。** 比例追蹤 skill 型態,不是品質。

---

## 4. 其他三個確定性指標,同樣不分層(且方向也反)

與 §3 同一納入規則,無門檻,中位數:

| # | 指標 | good (n=14) | mixed (n=4) | 判定 |
|---|---|---|---|---|
| 1 | 裸禁令率(禁令後 3 行內無替代/理由) | **65.8%**(0–100) | 41.7%(33–83) | good **更高**,全距重疊 |
| 2 | **舉例密度**(fenced code 塊/1k字) | 4.0 | **5.8** | mixed **更多** |
| 3 | 規則級物證掛載率 | **17.9%**(0–54) | 45.4%(10–100) | good **更低**,全距重疊 |

三個指標**方向全部與假說相反**,且全距皆重疊。

⚠️ **納入門檻會改變絕對值**:早期草稿對指標 1、3 各自加了門檻,得到 66.7% / 38.3%;
一個獨立稽核用它自己的 regex 得到 60.5% / 18.9%。**方向三者一致,絕對值三者不同。**

⚠️ **「有例子」本身也無法用單一 pattern 認定**:以 fenced code block 計,
good 組只有 **12/14(86%)**——`blader` 與 `RinDig` 為零。
而 `blader` 的例子是 `Before:` / `After:` 引用區塊,不是 code fence。

### 4.1 「單位」也造成擺動(受控比較)

同語料(61 檔)、同 marker set A,只變「一條指令」的認定單位:

| 單位 | pos | neg | ratio |
|---|---|---|---|
| marker 出現次數 | 860 | 507 | 1.70 : 1 |
| 指令行 | 348 | 260 | 1.34 : 1 |

→ **1.27×**。與 §3.2 的 marker 選擇(6.4×)同向疊加。

### 4.2 為什麼單位是根本問題

`blader__humanizer` 的規則載體是**編號標題 + 欄位**,標題裡沒有祈使詞:

```
### 1. Inflated claims about importance and legacy
**Words to watch:** stands/serves as, is a testament, a pivotal role, …
**Problem:** AI writing often claims that ordinary details mark a major change…
**Before:** > …officially established in 1989, marking a pivotal moment…
**After:**  > …established in 1989, part of a wider decentralization…
```

實測(直接對原檔):**35** 條編號 pattern;其中 `Problem:` 33、`Before:` 33、
但 `Words to watch` 僅 **11**。而「含 must/never/should/avoid 的行」在此檔只有 **24** 行
——**與那 35 條是兩個不同的母體**。

同一抽象物件,語料裡至少三種互不相容的載體:blader 的欄位化編號標題、
`obra` 的粗體祈使句、`Jeffallan` 的 `MUST DO:` / `MUST NOT DO:` 清單。

→ **你無法計數一個你無法可靠切分的東西。分母不穩,§3/§4 的比率就都不穩。**

---

## 5. ⚠️ `❌/✅` 配對是作者血統偵測器,不是品質偵測器

61 檔中,含 `❌` 或 `✅` 者僅 **9 檔**;其中 **5 檔屬 obra 系**
(`obra__superpowers` 2 + 中文 fork `jnMetaCode__superpowers-zh` 3)。
母體中 obra 系為 10/61,隨機期望命中 1.48 個。

| | N | obra 系母體 | 命中 | 其中 obra 系 | 隨機期望 | P(X≥k) |
|---|---|---|---|---|---|---|
| 全部 61 檔 | 61 | 10 | 9 | **5(56%)** | 1.48 | **0.0039** |
| 去重 59 份 | 59 | 10 | 8 | **5(62%)** | 1.36 | **0.0022** |

→ **任何以 `❌/✅` 配對為門檻的確定性設計,實質上在偵測「這是不是 obra 或它的 fork」。**
這是 `docs/llm-judge-contamination.md` §1 的判準自我定錨在**確定性特徵裡**復現
——比在 LLM judge 裡更危險,因為它看起來客觀。

⚠️ **放寬定義不能解決,只會稀釋**:把 `Instead` / `Rather than` 納入後命中升到 41/61、
obra 系降到 17%——但那兩個是普通英文詞,單獨就分別命中 31 檔與 22 檔,
命中的 41 檔中有 12 檔**只**match 到這兩個詞。放寬後量到的不再是「配對構造」。

⚠️ **本結論對現有系統的蘊含,本文不作裁決但必須指出**:
`skill-reviewer/scripts/lint_skill.py` 的 `BEFORE_AFTER_RE`(L46–48)是
`❌.{0,500}?✅` / `Before.{0,800}?After` 鄰近 regex,支撐已計分的
`R-005 readme_has_before_after`(weight 2),且 skill-reviewer 已接入 ASP Pipeline G5。
本節的推論適用於它。**這需要獨立評估,不在本文範圍**,已記入 `misjudgments.md`。

---

## 6. LLM 校準:預先登記的否證條件觸發

### 6.1 協定(含所有偏離)

> 依 `research/inter-rater-protocol.md`:173 的規定,本節措辭為
> **same-model, independent-context reliability**,**不是** inter-rater reliability。
> 所有「審查者」皆為同一模型的獨立 context,非跨模型亦非人類。

10 個 repo,5 個獨立 context,每個 2 個 repo。
標記者**不知** craft 評級、**不知**假說方向、**被禁**讀 `qualitative_notes/` 與 `rubric*.yaml`。
以字母序取前 25 條規則,逐條標記失效型態、形式,及
`has_reason` / `has_example` / `has_replacement`。

⚠️ **五處偏離,如實記錄**:

1. 預先登記為「good/mixed 各半」,實際 **6 good / 4 mixed**(第 5 個 context 拿到兩個 good)。
2. 樣本自 18 個合格 repo 中**手選 10 個**:4 個 mixed 全取,14 個 good 只取 6,無成文規則;
   且預先登記指定「必含 obra、blader、ayghri、Jeffallan」——**即本文先前已引為範例的那幾個**。
3. 「前 25 條」對兩個 repo 不成立:`NevaMind` 僅 23 條、`axtonliu` 僅 15 條
   (指示為「不足則全取」,行為正確但百分比的分母因此不同)。
4. **每個 repo 只有 1 個標記者**,故跨 repo 比較混淆了標記者變異與 repo 變異。
5. **`has_replacement` 被收集但從未彙總報告**——而 §6.3 的結論正是建立在該屬性上。
   它只間接進入 `bare_rules` 的定義。**結論所依賴的性質,從未被直接檢定。**

**預先登記**:排除 obra 系後,若 good 與 mixed 的 form_mismatch 計數目視重疊,
則此訊號在本語料無鑑別力,**只留註記、不得進入裁決**。

### 6.2 結果

| repo | craft | n | 裸規則% | form_mismatch% | has_reason% | has_example% |
|---|---|---|---|---|---|---|
| `kepano__obsidian-skills` | good | 25 | 80 | 4 | 8 | 12 |
| `google__skills` | good | 25 | 32 | 0 | 24 | 48 |
| `blader__humanizer` | good | 25 | 24 | **60** | 60 | 60 |
| `ayghri__i-have-adhd` | good | 25 | 24 | 24 | 44 | 56 |
| `addyosmani__agent-skills` | good | 25 | 36 | 0 | 52 | 24 |
| `obra__superpowers` | good ⚠️循環 | 25 | 80 | 0 | 16 | 16 |
| `NevaMind-AI__memU` | mixed | 23 | 52 | 0 | 22 | 13 |
| `axtonliu__smart-illustrator` | mixed | 15 | 40 | 0 | 7 | 53 |
| `Jeffallan__claude-skills` | mixed | 25 | 96 | 12 | 0 | 0 |
| `earthtojake__text-to-cad` | mixed | 25 | 32 | 4 | 24 | 24 |

排除 obra 系後(good n=5 / mixed n=4):

| 指標 | good | mixed | 判定 |
|---|---|---|---|
| form_mismatch% | 0, 0, 4, 24, **60** | 0, 0, 4, 12 | **重疊,且 good 偏高** |
| 裸規則% | 24, 24, 32, 36, 80 | 32, 40, 52, 96 | 重疊 |
| has_reason% | 8, 24, 44, 52, 60 | 0, 7, 22, 24 | 重疊 |
| has_example% | 12, 24, 48, 56, 60 | 0, 13, 24, 53 | 重疊 |

**四個指標沒有一個分得開。否證條件觸發。**
(依預先登記,此處**只陳述重疊**,不從中讀出方向。)

### 6.3 三個 context 獨立指認同一個機制

> **blader 的標記者**:15 條被標為 form_mismatch「其實是**假警報**:
> 每一條都用 Before/After 示範了『該改成什麼樣』。」
>
> **ayghri 的標記者**:「被機械標記的 6 個…**其實都附了範例與替代,是良性的**。」
>
> **Jeffallan 的標記者**:「B 的 form_mismatch 低只是因為它的失效型別本就以 discipline 為主、
> 天然適配 prohibition,**而非因為它寫得更完整**。」

→ 機制陳述:**禁令是否有害,不取決於它配的失效型態,取決於有沒有附上已完成的替代示範。**

⚠️ 此陳述**未被本研究檢定**——見 §6.1 偏離 5,`has_replacement` 從未彙總。
它是三個 context 的**收斂觀察**,不是量測結果。

### 6.4 標記者主動揭露的缺陷

1. **循環性(已預期)** — obra 的標記者:「我是在用 obra 自家的分類法評 obra 自家的 skill,
   `form_mismatch=0` 有一部分是**建構上必然**的。」
2. **抽樣缺陷(未預期)** — 字母序讓 25 條全落在單一檔案。覆蓋率:

| repo | 涵蓋 | 覆蓋率 |
|---|---|---|
| `Jeffallan__claude-skills` | ~1–2 / **67** 檔 | **~2%** ← 最差,且供給表中所有極端值 |
| `obra` / `google` / `earthtojake` | 1 / 5 | 20% |
| `kepano` / `addyosmani` | 2 / 5 | 40% |

→ **反挑櫻桃的設計,用代表性換了可複現性。** 影響 10 個樣本中的 6 個。
此偏誤**不對稱**:被列出的多為 good,而漏列的 `Jeffallan` 供給了所有 mixed 極端值。
**本文未做敏感度分析。**

---

## 7. 一手來源(逐行核對屬實)

`research/inter-rater/corpus/obra__superpowers/skills/writing-skills/SKILL.md` L459–474
「Match the Form to the Failure」:

| 基線失效 | 該用 | 不該用 |
|---|---|---|
| 壓力下明知故犯(紀律型) | 禁令 + rationalization table + red flags | 軟性建議 |
| 有照做但**輸出形狀**錯 | **正向配方/契約**:直述輸出「是什麼」及順序 | 禁令清單 |
| 漏掉必要元素 | 模板裡的 **REQUIRED 槽位** | 散文提醒 |
| 行為視條件而定 | 綁**可觀察述詞**的條件句 | 無條件規則 + 例外條款 |

L470 的 head-to-head 措辭實驗:形狀型問題上,禁令組產生的非預期內容多於配方組
(**fully separated distributions**),且「**trended** worse than even the no-guidance control」
(原文的保留詞 trended 照錄)。

L473–474 附帶兩條:**不要加 nuance 子句**(替勝出配方加一個 nuance 子句即從穩定降為不穩定);
**例外條款不會限縮作用域**。

→ **這是好的寫作建議,且是本文唯一有對照實驗支撐的內容。**
但 §6 顯示:把它機械化為審查判準後結果反向。**建議 ≠ 判準。**

---

## 8. 裁決:不改 rubric

- **不新增** `form_failure_match` 判準——預先登記的否證條件觸發(§6.2)。
- **不新增**極性或舉例的計分變數——兩者在確定性層同樣失效且方向皆反(§3、§4)。
- **不出貨**確定性腳本——§4.2 的分母問題與 §5 的血統集中使任何門檻都不可信。
- **L-002 不動。** ⚠️ 但**不宣稱 L-002 已完整涵蓋**:
  其 `equivalent_forms` 明文承認「**精確術語表:以定義消除歧義,取代靠例子示範**」
  ——即**無替代示範亦可計分**,比 §6.3 的機制陳述**寬**。
  兩者的差距是真實的,但 §6.1 偏離 5 意味著本研究**沒有資格**斷言該差距該怎麼補。
  已記入 `misjudgments.md` 待累積處理。
- `rubric_version` 維持 **2.1.0**。

---

## 9. marker 定義(複現用)

⚠️ 執行前須先依 `research/clone-manifest*.json` 重建語料(§2)。
⚠️ 這些 regex **本身就是本文否證的對象**。公開是為了可複現,**不是**建議拿去當工具。

```python
POS_A  = r"(?i)\b(always|must|should|prefer|required|ensure|use)\b|✅|必須|務必|應該"
NEG    = r"(?i)\b(never|don't|do not|must not|should not|avoid|forbidden|prohibited|not allowed)\b|❌|🚫|禁止|不得|切勿"
# §3.2 變體:B = A 去 use;C = always|must|required;D = A 加 do|make|run;E = always|must
# 一律先剝 fenced code:re.sub(r"```.*?```", "", text, flags=re.S)
# 指令行單位(§4.1):行首 ^([-*+]|\d+\.|\||\*\*|#{2,6}\s) 且長度 ≥8
PAIR   = r"(?i)✅|\bInstead\b|\bRather than\b|\bUse\b|\bReality\b|\bRight\b|\bGood\b|\bbecause\b|→|改為|改用|理由|原因"
RULE   = r"(?i)\b(must not|must|never|don't|do not|always|should not|should|avoid)\b|禁止|不得|必須|務必|應該"
GROUND = r"(?i)```|❌|✅|<Bad>|<Good>|\bbecause\b|\bwhy\b|\bfor example\b|\be\.g\.|\bInstead\b|\bReality\b|因為|理由|例如|範例|→"
# §5:僅 r"❌|✅"。納入規則:有本地全文 + 有 craft 評級,無其他門檻(§3.2 表另加 pos+neg≥10,已註明)
```

`pos_neg_ratio` / `neg_per_1k_words` **僅存在於本文件**,未註冊進 `rubric.yaml`
或 `aggregate_stats.py` 的 `feature_class`——稱其 observation-only 是**敘述性的**,
不是系統中的登記狀態。

---

## 10. 修正紀錄

本文經**兩輪獨立 review**(重算全部數字 + 交叉檢查內部一致性)。第一版與第二版的錯誤:

| # | 曾經寫的 | 實際 | 處置 |
|---|---|---|---|
| 1 | v1:「配對構造 9/61、5/9 屬 obra 系」→ **v2 宣告此數字「是錯的」,改為 41/61、17%** | **v1 是對的**。`❌/✅` 單獨算就是 9/61、5 個 obra 系(P=0.0039)。v2 用 `Instead`/`Rather than` 放寬,那是普通英文詞(單獨命中 31 / 22 檔),稀釋了真訊號 | **撤回 v2 的撤回**,恢復並強化原結論(§5) |
| 2 | 「`Jeffallan` 5.12:1 是全語料最正向」 | `kepano` 37:1 更高,**同一張表裡自我矛盾** | 已改(§3.3) |
| 3 | 「blader 33 條 pattern 無一例外三件套」 | **35** 條,`Words to watch` 僅 11 | 改為只陳述直接實測值(§4.2) |
| 4 | 「ayghri 10 條規則每條附 Bad/Good」 | 10 條規則、**8 對** | **整段刪除**(二手引用,未核原檔) |
| 5 | 「定義敏感 2.2×」 | 混淆了 marker set 與檔案數(54 vs 61),非受控 | 拆為單位 1.27×(§4.1)與 marker 6.4×(§3.2) |
| 6 | 「兩組 100% 都有例子」 | good 僅 86% | 已改(§4) |
| 7 | 「所有數字皆可由現有檔案重算」 | **語料在 `.gitignore` 內**,新 clone 上指令回傳 0 | 已改為明確的不可複現聲明(§2) |
| 8 | §6.1 協定描述 | 五處偏離未揭露,含 **`has_replacement` 收了沒報** | 全部列出(§6.1) |
| 9 | 「三位審查者獨立」 | 違反 `inter-rater-protocol.md`:173 的強制措辭 | 改為 same-model, independent-context(§6.1) |
| 10 | 「正是 L-002 原文,沒東西需要補」 | L-002 的 `equivalent_forms` 明文承認無替代示範的形式,**比機制寬** | 改為指出差距、但聲明本研究無資格裁決(§8) |
| 11 | §5/§6/§7.1 的三組質化引用與「非 obra 血統獨立確證」 | 建立在未核對的二手引用上;§7.1 更被 §6.3 的盲審資料反證 | **整段刪除** |
| 12 | 缺陷清單漏列 `Jeffallan`;稱「影響多數樣本」 | 其覆蓋率 ~2% 最差;實為 6/10 | 已補完整表(§6.4) |

**方法上的教訓(這是本文最該被記住的一條)**:
第 1、3、4、11 條全部出自同一個壞習慣——**引用 `qualitative_notes` 的數字而不回原始檔核對**。
第 1 條更糟:我在「自我修正」的動作裡**推翻了一個正確的發現**。
本次改寫的規則是:**每個寫進本文的數字,都必須是本人對原始檔的直接量測。**
所有做不到這一點的段落已刪除,而非改寫。
