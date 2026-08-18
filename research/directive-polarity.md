# 指令極性:這個問題無法用確定性儀器回答

> **問題**:優質 skill 裡「正向/白名單」指令與「負向/黑名單」指令的比例是多少?
> 能不能當品質判準?以及:**它是不是跟「有沒有舉例」是同一件事?**
>
> **答案**:**量不出來。** 不是樣本不夠,是儀器本身有四個各自足以推翻結果的缺陷(§2)。
> 而唯一量得準的那個數字說:**任何確定性的「配對偵測器」實際上在偵測作者身分**(§3)。
>
> **本文的價值是這些否證路徑,不是任何一個比例數字。**

日期:2026-08-18 · rubric 影響:見 §6 · 本文經**四輪**獨立 review,修正紀錄見 §7

> ⚠️ **給後續量測的隔離提示**:本文 §3、§4 公開具名 repo 的資料。
> 已加入 `inter-rater-protocol.md`「必須隔離的東西」與 `research/inter-rater/RATER-BRIEF-R2.md` 禁讀清單。

---

## 1. 結論

1. **比例量不出來,而且原因是可指認的**:四個獨立缺陷,每一個都足以推翻結果(§2)。
   先前版本曾發布 `1.75 : 1` 等數字,**已全數撤回**。
2. **`❌/✅` 配對構造顯著集中於單一作者血統**(9/61 檔命中,5 屬 obra 系,P=0.0039;
   去重後 8/59、5 個,P=0.0022)→ **任何以此為門檻的確定性設計是血統偵測器**(§3)。
3. **LLM 版本也被否證**:預先登記的否證條件觸發,四個標記指標沒有一個分得開(§4)。
4. **「極性」與「舉例」不是兩個變數**:一個 `Bad: X / Good: Y` 同時是舉例與極性配對。
   兩者在確定性層一起失效,不是巧合。
5. **處置:不新增任何計分變數;rubric 僅作一處事實勘誤**(§6)。

---

## 2. 為什麼量不出來:四個獨立缺陷

先前版本(v1–v3)發布過 craft-good `1.75 : 1`、mixed `4.63 : 1` 等數字。
第四輪 review 找出四個缺陷,**每一個都獨立足以使那些數字失效**。全部已由本人對原始檔驗證。

### 缺陷 1:正向 marker 把禁令算成正向

`POS_A` 含 `\bmust\b`、`\bshould\b`、`\buse\b`,於是:

| 字串 | 被計為 |
|---|---|
| `You MUST NOT mutate state` | **正向** |
| `### MUST NOT DO` | **正向** |
| `should not skip` | **正向** |
| `don't use it` | **正向** |

`Jeffallan__claude-skills` 有 **66 個 `must not`**,其中 **64 個是 `### MUST NOT DO` 標題**
——全部計為正向。修正後該 repo 由 5.12:1 掉到 **4.52:1**,mixed pooled 由 4.63 掉到 **4.14**。
**一篇討論指令極性的文件,把 64 條禁令算成了背書。**

### 缺陷 2:語料被截斷,而且沿著比較的兩組不對稱

`research/inter-rater/corpus/PROVENANCE.md` 載明語料**只含 `craft_llm_todo` 列出的 SKILL.md**
(每 repo ≤5 份)。實測 15 個 repo 中 **10 個被截斷**:

| repo | 語料 | 上游實際 | 覆蓋率 |
|---|---|---|---|
| `affaan-m/ECC`(good) | 5 | **897** | **1%** |
| `google/skills`(good) | 5 | 111 | 5% |
| `browser-act/skills`(good) | 5 | 103 | 5% |
| `obra/superpowers`(good) | 5 | 14 | 36% |
| **`Jeffallan/claude-skills`(mixed)** | **67** | **67** | **100%** |

好組多為 1–36% 的抽樣,而 mixed 組的主導成員是**完整**的。
先前版本 §2 明文承諾「**無其他門檻**」——**那是假的**。
更糟的是,先前寫的警語「mixed 組實質上是一個 repo,Jeffallan 佔 83%」
**本身就是這個截斷造成的**,不是語料的性質。

### 缺陷 3:字數用 whitespace token,CJK 少算約 4.7 倍

所有「/1k 字」都是 `len(text.split())`。中文不用空格分詞,故
`jnMetaCode__superpowers-zh` 的 2,709 個 token 對應 **12,664 個 CJK 字元**。
於是「負向密度」部分在量**語言**而非極性:`obra` 9.40/1k 對上它自己的中文 fork 2.21/1k,
而兩者內容相關。

### 缺陷 4:五組 marker 變體只擾動分子

先前用五組 POS 變體宣稱穩健性,但 **NEG 固定不變**,而 NEG 本身有大洞:
`doesn't` 50、`cannot` 40、`can't` 29、`isn't` 27、`won't` 13、`shouldn't` 2
——約 161 次否定對一個 507 的分母**完全不可見(約 24%)**。
對稱地補齊 NEG 會使 good pooled 明顯下移而 mixed 幾乎不動:
**該擾動不是保守的,是朝著支持結論的方向不對稱。**

### 這四個缺陷不能靠補丁修

修 1 要重寫 marker;修 2 要重新 clone 未截斷語料(`affaan-m` 一家就 897 份);
修 3 要換 CJK-aware 分詞;修 4 要對稱重建 NEG。修完仍是 n=18 的存在證明。
**依 2026-08-18 裁定:比例表全數移除,不再嘗試。**

---

## 3. 唯一站得住的量測:`❌/✅` 是作者血統偵測器

此指標是**每檔的存在/不存在計數**——§2 的四個缺陷**一個都不適用**
(無正向 marker、無字數分母、無 NEG、不依賴檔內完整性)。四輪 review 逐位複現。

61 檔中含 `❌` 或 `✅` 者僅 **9 檔**;其中 **5 檔屬 obra 系**
(`obra__superpowers` 2 + 中文 fork `jnMetaCode__superpowers-zh` 3)。母體中 obra 系為 10/61。

| | N | obra 系母體 | 命中 | 其中 obra 系 | 隨機期望 | P(X≥k) |
|---|---|---|---|---|---|---|
| 全部 61 檔 | 61 | 10 | 9 | **5(56%)** | 1.48 | **0.0039** |
| 去重 59 份 | 59 | 10 | 8 | **5(62%)** | 1.36 | **0.0022** |

→ **任何以 `❌/✅` 配對為門檻的確定性設計,實質上在偵測「這是不是 obra 或它的 fork」。**
這是 `docs/llm-judge-contamination.md` §1 的判準自我定錨在**確定性特徵裡**復現
——比在 LLM judge 裡更危險,因為它看起來客觀。

⚠️ **放寬定義不能解決,只會稀釋**:加入 `Instead` / `Rather than` 後命中升到 41/61、
obra 系降到 17%。但那兩個是普通英文詞(單獨分別命中 31 與 22 檔),
放寬後的 41 檔中**有 31 檔(76%)完全不含 `❌`/`✅` 也不含 `<Bad>`/`<Good>`**。
**放寬後量到的不再是「配對構造」。**

⚠️ **適用範圍**:本節量的是 `❌/✅` 在 **SKILL.md** 上的分佈,且是**截斷後**的語料(缺陷 2)。
它**不**適用於 `R-005 readme_has_before_after` ——見 §7 修正 23,那條蘊含已自行否證。

---

## 4. LLM 校準:預先登記的否證條件觸發

> 依 `research/inter-rater-protocol.md`「報告措辭規定」,本節措辭為
> **same-model, independent-context reliability**,**不是** inter-rater reliability。

### 4.1 協定與全部偏離

10 個 repo、5 個獨立 context,每個 2 個。標記者不知 craft 評級、不知假說方向、
禁讀 `qualitative_notes/` 與 `rubric*.yaml`。以字母序取前 25 條規則,
標記失效型態、形式,及 `has_reason` / `has_example` / `has_replacement`。

⚠️ **六處偏離,如實記錄**:

1. 預先登記「good/mixed 各半」,實際 **6 good / 4 mixed**。
2. 自 18 個合格 repo **手選 10 個**,無成文規則;且預先登記指定「必含 obra、blader、
   ayghri、Jeffallan」——**即先前版本已引為範例的那幾個**。
3. 「前 25 條」對兩個 repo 不成立(`NevaMind` 23 條、`axtonliu` 15 條)。
4. **每個 repo 只有 1 個標記者**,跨 repo 比較混淆了標記者變異與 repo 變異。
5. **`has_replacement` 被收集但從未彙總**——而 §4.3 的機制陳述正建立在該屬性上。
   **結論所依賴的性質,從未被直接檢定。**
6. **「一條規則」的單位從未定義**,逐條標記表**未保存進 repo**,故**本節不可複現**。

**預先登記**:排除 obra 系後,若 good 與 mixed 的 form_mismatch 計數目視重疊,
則此訊號無鑑別力,**只留註記、不得進入裁決**。

### 4.2 結果

| repo | craft | n | 裸規則% | form_mismatch% | has_reason% | has_example% |
|---|---|---|---|---|---|---|
| `kepano__obsidian-skills` | good | 25 | 80 | 4 | 8 | 12 |
| `google__skills` | good | 25 | 32 | 0 | 24 | 48 |
| `blader__humanizer` | good | 25 | 24 | 60 | 60 | 60 |
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
| form_mismatch% | 0, 0, 4, 24, 60 | 0, 0, 4, 12 | **重疊** |
| 裸規則% | 24, 24, 32, 36, 80 | 32, 40, 52, 96 | **重疊** |
| has_reason% | 8, 24, 44, 52, 60 | 0, 7, 22, 24 | **重疊** |
| has_example% | 12, 24, 48, 56, 60 | 0, 13, 24, 53 | **重疊** |

**四個指標沒有一個分得開。否證條件觸發。**
依預先登記,此處**只陳述重疊,不從中讀出任何方向**
(先前版本曾寫「good 偏高/甚至反向」,那是預先登記明文禁止的事後方向解讀,已刪)。

### 4.3 三個 context 獨立指認的機制(觀察,非量測)

> **blader 的標記者**:被標記的「其實是**假警報**:每一條都用 Before/After 示範了該改成什麼樣」
> **ayghri 的標記者**:「**其實都附了範例與替代,是良性的**,只是配對觸發旗標」
> **Jeffallan 的標記者**:「form_mismatch 低只是因為它的失效型別本就以 discipline 為主,
> **而非因為它寫得更完整**」

→ 機制陳述:**禁令是否有害,不取決於它配的失效型態,取決於有沒有附上已完成的替代示範。**

⚠️ **此陳述未被本研究檢定**(偏離 5)。它是三個 context 的收斂觀察,不是量測結果。

### 4.4 標記者主動揭露的缺陷

1. **循環性(已預期)** — obra 的標記者:「我是在用 obra 自家的分類法評 obra 自家的 skill,
   `form_mismatch=0` 有一部分是**建構上必然**的。」
2. **抽樣缺陷** — 字母序讓 25 條集中在前一兩個檔案。與 §2 缺陷 2 疊加後,
   覆蓋率的分母本身不可比(對 `Jeffallan` 是 67 檔的 ~2%,對 `obra` 是**已截斷的** 5 檔中的 1 檔)。
   **本文未做敏感度分析。**

---

## 5. 一手來源(行號逐一核對屬實,但**其適用範圍比先前引述的窄**)

`research/inter-rater/corpus/obra__superpowers/skills/writing-skills/SKILL.md` L459–474
「Match the Form to the Failure」:

| 基線失效 | 該用 | 不該用 |
|---|---|---|
| 壓力下明知故犯(紀律型) | 禁令 + rationalization table + red flags | 軟性建議 |
| 有照做但**輸出形狀**錯 | **正向配方/契約** | 禁令清單 |
| 漏掉必要元素 | 模板裡的 **REQUIRED 槽位** | 散文提醒 |
| 行為視條件而定 | 綁**可觀察述詞**的條件句 | 無條件規則 + 例外條款 |

⚠️ **先前版本擴大了它的適用範圍,已更正。** L470 原文為:

> "In head-to-head wording tests **on dispatch-prompt guidance**, the prohibition arm produced
> clearly more of the unwanted content than the recipe arm (fully separated distributions),
> and trended worse than even the no-guidance control — **micro-test your own case rather than
> assuming, but never reach for the prohibition by default.**"

即該實驗的對象是 **dispatch-prompt guidance 這一種提示**,不是整個「形狀型失效」類別;
且作者明文要求**不要外推,自己 micro-test**。先前版本兩者都沒照錄。

→ 這是**寫作建議**,不是判準;而且是一份**無引用、無 n 的作者自陳**,
作者本人正是 §3 指認為語料主導混淆的那個血統。§4 顯示把它機械化為審查判準後結果不成立。

---

## 6. 裁決

- **不新增**任何計分變數(極性、舉例、form-failure match)。
- **不出貨**確定性腳本——§2 的四個缺陷與 §3 的血統集中使任何門檻都不可信。
- **L-002 的判準本體不動。** ⚠️ 但**不宣稱它已完整涵蓋** §4.3 的機制:
  其 `equivalent_forms` 明文承認「**精確術語表:以定義消除歧義,取代靠例子示範**」
  ——即無替代示範亦可計分,比該機制寬。差距真實,但本研究(偏離 5)無資格裁決。
- **一處事實勘誤已修**(非判準變更,`rubric_version` 2.1.0 → **2.1.1**):
  L-002 `evidence_refs` 的「blader/humanizer(33 pattern 皆附 why)」
  → 實測 **35** 條編號 pattern,`Problem:` 33/35、`Before:` 32/35、兩者兼具 31/35、
  `Words to watch` 僅 11/35、四欄位齊全僅 10/35。
  ⚠️ **此錯誤早在 `research/inter-rater/ratings-R3.json:118` 就被審查者記下**
  (「blader 的 **35** 個 pattern」),存在版控中無人回填;
  同一錯誤散落 7 處,其中 2 處隨 skill-reviewer 出貨。已一併更正。

---

## 7. 修正紀錄

本文經**四輪**獨立 review。v1–v3 的 22 條見 git 歷史
(`445fdb8` / `48d1cc3` / `20dfad8` / `4bb9139`);此處保留兩類:
**在修正動作中製造的錯誤**,以及**第四輪的結構性發現**。

### 在「修正」中製造的錯誤(最該記住的一類)

| # | 事件 |
|---|---|
| 1 | v1 稱「配對構造 9/61、5/9 屬 obra 系」。**v2 宣告它是錯的**,改為 41/61、17%。**v1 才是對的**——v2 用 `Instead`/`Rather than` 放寬,那是普通英文詞。**我在自我修正的動作裡推翻了一個正確的發現。** |
| 13 | v2 修好「Jeffallan 是最正向」(錯,是 kepano),**v3 卻在同一張表的另一端**寫下「ayghri 是最負向」——也錯,是 axtonliu。**鏡像重演。** |
| 15 | v3 引用 `inter-rater-protocol.md:173`,而**本 PR 自己對該檔的 +2 行編輯**把它推到 :175。 |
| 19 | v3 補的「視窗規則」**本身不能重現該節數字**——修 reproducibility gap 的補丁自己壞掉。 |
| 23 | v3 據 §3 的血統集中推論 `R-005 readme_has_before_after` 可能也在偵測血統,並記入 `misjudgments.md`。**經查不成立**:`feature_matrix.json`(**早就在版控裡**)顯示 80 repo 中 31 個為 True,obra 系 **1/2**,期望 0.775,**P=0.63,零集中**。我把一條 regex 在 SKILL.md 上的統計外推到另一條 regex 在 README 母體上,而否證所需的資料早就存在。 |

### 第四輪的結構性發現(導致本次大幅刪減)

| # | 發現 | 處置 |
|---|---|---|
| 24a | `POS_A` 把 `MUST NOT` / `should not` / `don't use` 計為正向;Jeffallan 64 個 `### MUST NOT DO` 標題全數被算成背書 | §2 缺陷 1;**比例表移除** |
| 24b | 語料每 repo ≤5 檔,15 個中 10 個被截斷(`affaan-m` 1%),而 mixed 主導成員完整 67/67;先前承諾「無其他門檻」為假 | §2 缺陷 2;**比例表移除** |
| 24c | 字數為 whitespace token,CJK 少算 ~4.7×,負向密度部分在量語言 | §2 缺陷 3;**比例表移除** |
| 24d | 五組 marker 變體只擾動分子,NEG 漏 `doesn't`/`cannot`/`can't`/`isn't`/`won't`(~24%),且不對稱 | §2 缺陷 4;**比例表移除** |
| 24e | 先前 §1 與判定欄讀出「good 偏高/反向」,而預先登記明文禁止事後方向解讀 | 已刪除方向語 |
| 24f | 先前把 obra 實驗的 "on dispatch-prompt guidance" 擴大為整個形狀型類別,並略去「micro-test your own case rather than assuming」 | §5 照錄原文與範圍 |
| 24g | 「33 pattern」錯誤散落 7 處(2 處出貨),且 `ratings-R3.json:118` 早已記錄正確值 35 | 全部更正,`rubric_version` → 2.1.1 |
| 24h | `misjudgments.md` 本身帶具名 craft 證據卻不在任何禁讀清單上,而 `CLAUDE.md` 指定它為專案唯一工作管道 | 已加入兩份禁讀清單 |

### 方法上的教訓

1. **引用二手數字而不回原始檔核對**(修正 1、3、4、11)。v3 起改為「每個數字必須直接量測」,
   第三、四輪確認該類錯誤已清零。
2. **單位混淆**(檔案 / repo / 區段 / token)。v3 出現四次,v4 又出現一次(缺陷 3 的 CJK)。
   **寫任何計數前,先寫下這個數字的單位是什麼。**
3. **外推前先查已有資料**(修正 23)。否證我那個 R-005 警示的資料早就在 `feature_matrix.json` 裡。
4. **修正動作本身需要被 review**(修正 1、13、15、19、23)。
   四輪裡有三輪的錯誤是在修正過程中產生的——這是本文最實在的一課。
5. **儀器要先驗證再量測。** 缺陷 1 是最基本的:一篇討論極性的文件,
   它的正向偵測器認不出 `MUST NOT`。四輪 review 才抓到,而一個
   `assert POS('MUST NOT') == 0` 的自我測試在第一分鐘就會抓到。

---

## 8. 複現

⚠️ **語料不在版控內**:`.gitignore` 排除 `research/repos/*` 與 `research/inter-rater/corpus/`
(`git ls-files` 各為 1 與 0 檔)。須先依 `research/clone-manifest*.json` 重建,
且重建拿到的是上游 HEAD 而非原快照。§4 的逐條標記表未保存,**該節不可複現**。

§3 是本文唯一完整可複現的量測:

```bash
# 命中檔數(需先重建語料)
grep -rlE '❌|✅' --include=SKILL.md research/inter-rater/corpus/ | wc -l      # 9
grep -rlE '❌|✅' --include=SKILL.md research/inter-rater/corpus/ \
  | grep -cE 'obra__superpowers|superpowers-zh'                                # 5
# 母體中 obra 系檔數
find research/inter-rater/corpus/obra__superpowers \
     research/inter-rater/corpus/jnMetaCode__superpowers-zh -name SKILL.md | wc -l  # 10
```

hypergeometric:`P(X≥5 | N=61, K=10, n=9) = 0.0039`;去重後 `N=59, n=8 → 0.0022`。
