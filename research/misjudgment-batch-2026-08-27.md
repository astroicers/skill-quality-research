# 第二次誤判批次處理:11 條(2026-08-27)

> 第一次批次見 [`misjudgment-review-2026-08-26.md`](misjudgment-review-2026-08-26.md)(7 條)。
> 帳本在 [`misjudgments.md`](misjudgments.md);本檔是查證過程與**負向驗證的實測輸出**。
>
> 落地版本:`rubric_version` 3.0.0 → **3.1.0**、plugin **2.0.0 → 2.1.0**。

## 這一批最值得記的一課

**「兩個缺陷長得像」不蘊含「修法可以共用」。**

上一版 `misjudgments.md` 的導言寫:`REDFLAG_OBEY_OUTPUT` 與 `REDFLAG_CRED_ARGV`
「與 2.2.0 修過的 S-101 中文分支同一缺陷型,**可沿用同一修法**(三條件共現)」。
**兩半都錯**:

- **不同型**。前者是**極性反轉**(regex 命中了語意相反的句子 → 假陽性);
  後者是**形式未涵蓋**(regex 認不出另一種寫法 → 假陰性)。
- **修法不能沿用**,而且理由不只是「不同型」。實測把三條件共現移植到 S-001:
  **7 命中只保留 1,memU 的 4 個真陽性死掉 3** —— 而 memU 正是 rubric 對 S-001
  的 `evidence_refs` 錨定案例。成因:`_SOFT_NL` 把單一換行併成空白,
  在英文 markdown 的條列上會併出**數百字元的「一句」**,任何 `not`/`never`
  都變成消音海綿。**該機制在 CJK 短句剛好,在英文長段落過度消音。**
- 還有一層**代價不對稱**,S-101 自己的 `confidence_rationale` 就寫著:
  「標低信心的代價可接受:它是正向標記、不進 gate,誤判只稀釋一個加分」。
  三條件共現敢收那麼緊,**前提就是過度消音只損失一個加分**。
  而 S-001 是 `severity: error`、會經 `security_error_confirmed` 翻 `needs-revision`。
  **同一機制在不同極性的規則上,代價完全不對稱。**

## 處置總表

| # | 條目 | 處置 |
|---|---|---|
| 1 | evals `security` 語意 | ✏️ 修(最優先)——結構化欄位 + 兩條新斷言 + fixture |
| 2 | H-002 未實作 | ✏️ `error → info`、`script → llm`、註明未實作;後半移「待測」 |
| 3 | differentiator 5 vs 6 | ✏️ 改 4 處 + 來歷註;`G3-review-notes.md` 不動 |
| 4 | `signal_type: craft` | ✏️ 只改 `dir_examples` + 三條 `measurement_note` + drift-guard 納入 signal |
| 5 | H-001 對純發佈清單 repo | ✏️ 改步驟 3 形狀表 + 步驟 2 + `scope_note`;**不改 H-001** |
| 6 | `REDFLAG_OBEY_OUTPUT` 極性 | ✏️ 刪 `without confirmation` 一支 + `OBEY_KNOWN_UNCOVERED` |
| 7 | `REDFLAG_CRED_ARGV` 形式 | ✏️ 加 `CRED_KNOWN_UNCOVERED`;**不補樣式** |
| 8 | R-004 對 `Jeffallan` | 🚫 **rubric 判對、我錯(第三次)** |
| 9 | S-101 英文分支 | 🚫 描述的後果不存在 |
| 10 | R-005 `✅/❌` | 🚫 不修 regex、不降級,只補註 |
| 11 | `self_update` 命中 hooks 註解 | 🚫 工具沒壞,是校準面漏了一種內容型態 |

**7 動、4 不動。** 另:2 條的第二半移入「待測」、4 條新登記。

---

## 三次「我錯了」

這一批查證推翻了我自己記錄裡的**六處事實**。列在這裡不是自責,是因為
它們都屬同一個型態——**用間接訊號代替直接查證**,而本專案已記錄過至少五次。

### (a) R-004:rubric 判對、我錯(**本專案第三次**)

我把它記成「假陰性」,理由是「該 repo 有 77KB 的驗證器 + 三個 CI workflow」。

實查 `validate-skills.py` 的 **24 個 checker class**:`YamlChecker`、`NameFormatChecker`、
`SectionOrderChecker`、`LineCountChecker`、`CrossReferenceChecker`……
**全部是格式/結構/交叉引用檢查,沒有一個測 skill 行為。**
它自己的 docstring 寫著「Validates skill **structure**, YAML frontmatter, and count consistency」。

R-004 的 mechanism 是「可驗證性使**改動不退化**」。一個格式檢查器不會因為
skill 的觸發設計壞掉而轉紅——**機制沒有達成**。

**決定性先例**:[`review-published-repos.md:44`](review-published-repos.md) ——
同一批審查者、同一天、同一張表,對「有 CI 但**只驗結構不驗內容**」明確判**真缺口**,
而對 `dir_examples`(範例寫在內文)判假陰性。**他們早就把這兩種情況分開了。**

我那一列自己也預感到了(「⚠️ 修之前先確認:放寬會讓『有任何驗證腳本』都算數」)
—— 查證顯示預感正確,而且證據比預感強。

順帶記一個沒人提過的觀察:R-004 的 `tier_prevalence` 是
`{T0: 28.6, T1: 50.0, T2: 69.7, T3: 66.7}` —— **T2 > T3,梯度在頂端反轉**。
已在條文加註。

### (b) R-005:第二次犯同一個已具名記錄的錯

我的計畫原本寫「血統裁定可能意味著該降級 R-005」。

[`directive-polarity.md:114-115`](directive-polarity.md) **白紙黑字排除了這個外推**:
「本節量的是 `❌/✅` 在 **SKILL.md** 上的分佈…**不**適用於 R-005」。
而同檔 §7「在**修正**中製造的錯誤」的**修正 23 就是這一條** —— 上次我據血統集中
推論 R-005 也在偵測血統,經查 `feature_matrix.json`(**早就在版控裡**)
80 repo 31 True、obra 系 1/2、**P=0.63 零集中**,已自行否證。

**同一個錯,同一份文件已經記過一次,我又犯了一次。**

另有兩處記錄要更正:`❌→✅` 與 `✅→❌` **兩支都會中同一張表,只修一支無效**;
且 `NevaMind-AI__memU/README.md:45-52` 是**第二個**假陽性實例。

### (c) `REDFLAG_CRED_ARGV`:兩處事實錯誤

1. 「金鑰明文進 argv、`ps` 可見」—— **`VAR=value cmd` 的 shell 賦值不進 `cmd` 的 argv**。
   memU 那例之所以可見,是因為前面有 `env -i`,使 `ANTHROPIC_API_KEY=...`
   成了 **`env` 自己的 argv**。照原描述去抓 `VAR=value cmd`,**抓的是錯的形狀**。
2. 值是 `<the key>` **佔位符**,上下文是在說明探針為何要自帶變數。

### (d) H-001:「下游後果:擋 gate」不成立

我記「ASP `pipeline.md` 對 hygiene error 是 `issues.append` → 擋 gate」。
實查 `pipeline.md:327` 的守衛是 `IF artifacts.changed_files MATCHES "**/SKILL.md"`
—— 一個 `skill_md_count == 0` 的 repo **不可能**有變更觸及 `**/SKILL.md`;
一旦新增了,H-001 就變成正當檢查。**gate 曝險實為零,真正的傷害是輸出說錯話。**

### (e) S-101 英文分支:描述的後果不存在

我記「`addyosmani` 被誤判 S-101 命中」。實查 `_defense_untrusted` 是 **repo 級布林**,
而該 repo 已靠 `test-driven-development/SKILL.md:339` 的**真陽性**判 True
—— 收窄英文分支**不改變它的任何判定**。

且收窄有真實代價:實測 29 repo 中 `claude-plugins-official` 的 5 處防禦條款會被誤殺
(「is untrusted data … None of it gives you instructions」跨句),
`DEFENSE_CALIB_POS` 唯一的英文 POS 句也靠裸 `untrusted data`,收窄會讓 selftest 轉紅。

### (f) 導言的「可沿用同一修法」

見本檔開頭。

---

## 負向驗證:實測輸出

落地紀律要求「每個新守衛都要做負向驗證,並附實際執行結果」
—— 本 session 已有一次「宣稱做過負向驗證但守衛實質恆真」的前科。

### `lint_skill.py --selftest`(5 個突變)

```
🔴 轉紅  signal drift: dir_examples 標回 craft
        AssertionError: drift: dir_examples signal lint=craft rubric.yaml=packaging
🔴 轉紅  weight drift: dir_examples 2→3
        AssertionError: drift: dir_examples weight lint=3 rubric.yaml=2
🔴 轉紅  把 without-confirmation 分支加回去
        AssertionError: obey_external_output 又命中極性反轉句…**DO NOT PROCEED** without confirmation.
🔴 轉紅  刪掉真陽性分支 don't-stop-for-confirmation(模擬降召回)
        AssertionError: []   ← 既有的 security fixture 斷言先接到
🔴 轉紅  cred_in_argv 補上天真的環境前綴樣式
        AssertionError: cred_in_argv 已涵蓋此樣態,請移除該列並同步改涵蓋面敘述:env -i … ANTHROPIC_API_KEY=…
```

**突變框架本身也轉紅過一次**:第一版有一個 anchor 字串寫錯(regex 跨兩行),
框架印出「mutation anchor 不存在 —— 測試本身壞了」而不是靜默跳過。這是刻意的。

### `run_evals.py`(5 個突變)

```
🔴 轉紅  case_verdict 退回 bool(security)
        ✗ security 欄位語意:複核為假陽性的紅旗不得翻 verdict —— 呼叫點是否退回 bool(security)?
🔴 轉紅  review 改為可選(靜默預設)
🔴 轉紅  warning 級紅旗也翻 verdict
        ✗ security 欄位語意:warning 級紅旗不得翻 verdict —— 上卷規則第 2 條只認 error
🔴 轉紅  memU 的 review 改標 false-positive
        ✗ 上卷規則與 evals 一致:上卷算出 approved-with-notes 但 evals 標 needs-revision
🔴 轉紅  anthropics 的 flag 改成 lint 沒命中的
        ✗ security 標註與 lint 實測對帳:evals 標了 S-001/cred_in_argv 但 lint 沒命中
          (實得 {'obey_external_output'}) —— 標註與偵測脫節,這正是『證據說謊』
```

**第一個突變是這次最重要的一條。** 起初 `sec = security_confirmed(...)` 寫在
`c_rollup_matches_rubric` 的迴圈裡,而**把它改回 `bool(...)` 不會被任何斷言接到**
—— 因為現有真實語料裡沒有「有 `craft_dimensions` 且 security 為假陽性」的組合
(`anthropics` 有假陽性但沒標維度),兩種寫法答案相同。
⇒ 抽出 `case_verdict()`,讓 fixture 用合成 `expected` 行使**同一條路徑**。
**守衛不能只在資料剛好行使到時才有效。**

### CI 條件下的實測(只有版控內的檔案)

`research/repos/` 是 gitignored。用 `git ls-files` 複製出一份只含版控內容的樹再跑:

```
✓ security 欄位語意(複核≠命中)
    (real repo 全部缺席,2 個 security 標註未對帳;schema 與語意仍由 fixture 覆蓋)
✓ security 標註與 lint 實測對帳
✅ 全部通過(跳過 5 個)
```

**它明說了「2 個標註未對帳」而不是印一個乾淨的勾。** ADR-033:162 那個
「已驗證 ✅」就是因為缺這句話而空過了。

### `REDFLAG_OBEY_OUTPUT` 收窄的行為變更(全語料實測)

現存 5 repo、804 個 `.md/.yml/.yaml/.sh`:

| 分支 | 命中 | 真陽性 |
|---|---|---|
| `without\s+(?:stopping\s+for\s+)?confirmation`(**刪**) | 2 | **0** |
| `follow it (to the letter\|exactly)` + `don't stop for confirmation`(**留**) | 5 | memU **4 處**(`SKILL.md:12/:71/:78` + `INSTALL-LATEST.md:118`)+ anthropics 1 處已知假陽性 |

repo 級判定變更:

| repo | 收窄前 | 收窄後 |
|---|---|---|
| `Jeffallan__claude-skills` | S-001 命中 | **無**(唯一命中是極性反轉的假陽性) |
| `NevaMind-AI__memU` | S-001 命中 | S-001 命中(不變) |
| `anthropics__skills` | S-001 命中 | S-001 命中(不變,已知假陽性,由步驟 5 攔) |

packaging 分數五個 repo **全部不變**(6/14、9/14、8/14、5/14、9/14)。

---

## 獨立複審(`/asp:review-work`)在這批上又找到 9 條

`policies/reality-checker.md` 的 role prompt、預設 `NEEDS_WORK`、≥3 正面證據且 0 反面才 PASS。
第一輪回報 **NEEDS_WORK(15 正面 / 9 反面)**。它逐字複現了本檔引用的突變輸出、
獨立重跑了 804 / 2 / 0 三個數字,然後在**我自己點名的兩個高風險守衛上各找到一個真的洞**。

⚠️ **工具白名單偏差**:本 harness 給不出精確的 `Read/Grep/Glob`。判讀者**無 Edit/Write**
(機械保證),但有 Bash;派工單限定唯讀命令與記憶體內突變,判讀者收尾自證
`git status --short` 為空。這個偏差如實記在這裡。

### 兩個真的洞

**F1 —— drift-guard 可被塊內註解完全遮蔽,真 drift 空過(medium)**

我在同一批裡才剛把 signal 納入 drift-guard,而那條 naive regex
`feature:\s*(\S+)[\s\S]*?signal_type:\s*(\S+)[\s\S]*?weight:\s*(\d+)` **讀的是註解不是值**。
複審者構造:把 `dir_examples` 的 signal 真的改成 `craft`、weight 真的改成 `9`,
同時在塊內留一行 `# 原為 signal_type: packaging 、 weight: 2 ,現調整` → **守衛 GREEN**。
我自己複現了一次:守衛解析到 `('packaging','2')`,YAML 真值是 `('craft','9')`。

**最尖銳的一點是它的攻擊面就是本 repo 的文體** —— `rubric.yaml` 的 R-001 勘誤註解
(我這一批加的)就正好長在 `feature:` 與 `signal_type:` 之間。

⇒ 改寫成 `parse_rubric_differentiators()`:先剝整行註解,再以 `- id:` 切塊、
塊內各自抓欄、欄位錨在行首 4 空格。順帶消掉複審者另外指出的兩個副作用
(少一個 `signal_type` 會報錯 rule 名、合法 YAML 重排會誤報一片)。
加一條 F1 回歸夾具,**含 anchor 失效時的自我斷言**。

**F2 —— `c_security_field_matches_lint` 的「部分缺席」是靜默的(medium)**

條件寫成 `if n_absent and not n_checked`,於是只要有一個 repo 在場,
另一個缺席 repo 的標註就一次都沒對帳、而該 case 照樣印 `✓`。
**那正是這條斷言自己要修的失效型**(用 skip 換一個「已驗證」的錯覺)。

⇒ 改成 `if n_absent:`,訊息帶 `已對帳 N 筆、未對帳 M 筆`,對齊
`drift-guard 比對 N/M 條` 的寫法。三種狀態實測:

```
全缺席   ✓ security 標註與 lint 實測對帳 — ⚠️ 已對帳 0 筆、未對帳 2 筆(…)
部分缺席 ✓ security 標註與 lint 實測對帳 — ⚠️ 已對帳 1 筆、未對帳 1 筆(…)   ← 舊碼在這裡全靜默
全在場   ✓ security 標註與 lint 實測對帳
```

### 三條敘述精度(在別的 repo 可略,在這裡不行)

- **F3**:CHANGELOG 寫「唯一改變 lint 輸出的是 `REDFLAG_OBEY_OUTPUT`」—— **假的**。
  `differentiators[].signal` 的 `dir_examples` 也是**機器可讀輸出欄位**的變更。已改成兩處。
- **F4**:「分數與判定零變更」與補記的「只有分母變了」**兩次都低估**。實測:凡
  `dir_examples` 命中的 repo,2 分由 craft **搬到** packaging ——
  `anthropics__skills` 的 craft script 子分數 `2/6 → 0/4`,**分子也動**。
  總分 `/14` 確實不變。已補上五個 repo 的逐列對照表。
- **F5**:本檔 §「留下的分支」寫 memU「3 處」—— 實為 **4 處**
  (`SKILL.md:12/:71/:78` + `INSTALL-LATEST.md:118`),而且 3+1=4 與同列的計數欄 5 自相矛盾。已改。

### 四條低嚴重度

- **F6**:`craft_verdict_rollup` **不驗維度鍵**,`{}` 落在最寬鬆值 `approved`、未知鍵照算。
  它是 SKILL.md 指示 LLM 產出四維後餵進來的公開介面,漏產或打錯鍵會**靜默拿到 approved**
  —— **那正是 3.0.0 要修的形狀,不能在自己的實作裡重演**。已加鍵的守衛 + 三條負向 case。
- **F7**:揭露行印在自己的 `✓` **之前**,視覺上掛到上一條去了。已改為由 `main()`
  接在該 case 自己的 `✓` 後面印。
- **F8**:`sys.path` 每次呼叫都 insert,跑一輪 fixture 由 11 長到 31。已提為 `_lint_module()`。
- **F9**:commit 標題「commit 說明附實際輸出」比內容強半步(逐條輸出在本檔)。已知,不改寫歷史 commit。

### 待補證據 2:「8 命中只保留 1」不可重建 → 已改成可重跑的腳本

複審者實測舊 regex 只有 **7** 命中、不是 8,並**正確地把它記成「待補證據」而非 finding**
(移植版的實作不在 repo 內,無從得知那個 8 在數什麼)。

而那個數字是「刻意不移植」這個決定的**全部依據**,四處引用、只活在一次性腳本裡。
⇒ 新增 [`scripts/measure_obey_port.py`](../scripts/measure_obey_port.py),把移植版實作出來、
掛進 CI selftest。**結論不變,數字更正為 7**:

```
語料:research/repos(804 個 .md/.yml/.yaml/.sh 檔)
舊 regex(收窄前)全語料 : 7 命中
移植三條件共現後       : 1 命中
   Jeffallan__claude-skills           2 → 0
   NevaMind-AI__memU                  4 → 1
   anthropics__skills                 1 → 0
被消音的最長「一句」   : 884 字元(anthropics__skills/skills/frontend-design/SKILL.md)
```

「memU 4 個真陽性死掉 3」那一半**完全成立**。`--selftest` 的第 3 條斷言是一段
452 字元的併句 fixture —— **那是「為什麼不移植」的可執行版本**,不再是散文裡的數字。

### 修完之後的負向驗證(含兩個「仍綠但不是守衛失效」)

```
🔴 F1: 整支解析器還原成舊的跨塊 naive regex → 解析器又讀到註解而非真值了
🔴 F2: 條件退回 `and not n_checked`        → 跳過 1 筆卻沒說出來(或數字不對):None
🔴 F2: 已對帳/未對帳兩個數字對調            → 跳過 2 筆卻沒說出來(或數字不對):'已對帳 2 筆…'
🔴 F6: 拿掉空 dict 的守衛                  → 空 dict 不得回 approved
🔴 F6: 拿掉未知鍵的守衛                    → 打錯的鍵不得照算
```

⚠️ **另有兩個突變仍綠,而那不是守衛失效,是突變無效** —— 如實記下,不當成通過:

| 突變 | 仍綠的原因 |
|---|---|
| 只把 `clean = "\n".join(非註解行)` 換回 `clean = txt` | 註解行是 `    # 原為 signal_type: …`,而欄位錨是 `^ {4}signal_type:` —— **行首錨自己就擋得住**,沒有重現 F1 |
| 只把 `feature` 的錨放寬成 `re.search(r"feature:\s*(\S+)", blk)` | 一個塊內只有一個 `feature:`,放寬它不改變任何結果 |

**兩層防護各自獨立有效**(剝註解 + 切塊/行首錨),所以要重現 F1 必須把**整支解析器**
還原 —— 那個突變確實轉紅。第一次跑出「🟢 仍綠」時我沒有直接記成守衛失效,
而是先去看突變到底改了什麼:**這一步本身就是本 repo 反覆記錄的那個教訓**
(猜 regex 命中什麼而沒去實測)。

### 這一輪的元教訓

**我在同一批裡剛補的守衛(drift-guard 納入 signal),自己就有一個更深的洞。**
補守衛的動作本身不構成證據;**只有讓別人來打它才算**。
而 F1 的攻擊面恰好是本 repo 用來記錄變更來歷的文體 —— 這種東西自己是找不到的。

---

## 刻意不做的事

- **不改 `has_tests_or_evals` 的 weight。** 實測 tier band 0/80 翻面(比預期安全),
  但 weight 4→3、滿分 14→13 會讓 **51/80 repo 的印出分數改變**,並使
  **84 處硬寫的 `/14`(18 個檔案)全部過期** —— 與「5 vs 6」完全同型的缺陷,
  代價與收益不成比例。
- **不動 `G3-review-notes.md:15`。** 那是裁決前的獨立覆核紀錄,當時為真;
  改它等於竄改稽核軌跡。
- **不動 `scripts/aggregate_stats.py` 的 `SIGNAL_TYPE` 與 `rubric-draft.yaml`。**
  同理:那是 Phase 4 的產生器與其凍結產出,canonical 是 `research/rubric.yaml`(ADR-031)。
  改產生器會讓已提交的 draft 靜默過期。
- **不開 ASP 側的 PR。** ADR-033 的兩處事實更正(`:86` 的「無假陽性疑慮」已被否證、
  `:162`/`:259` 的「已驗證 ✅」是空過斷言)在 `AI-SOP-Protocol`,**跨 repo**,
  已登記待處理,需另行授權。
