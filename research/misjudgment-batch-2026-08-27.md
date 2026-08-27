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
  **8 命中只保留 1,memU 的 4 個真陽性死掉 3** —— 而 memU 正是 rubric 對 S-001
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
| `follow it (to the letter\|exactly)` + `don't stop for confirmation`(**留**) | 5 | memU 3 處 + anthropics 1 處已知假陽性 |

repo 級判定變更:

| repo | 收窄前 | 收窄後 |
|---|---|---|
| `Jeffallan__claude-skills` | S-001 命中 | **無**(唯一命中是極性反轉的假陽性) |
| `NevaMind-AI__memU` | S-001 命中 | S-001 命中(不變) |
| `anthropics__skills` | S-001 命中 | S-001 命中(不變,已知假陽性,由步驟 5 攔) |

packaging 分數五個 repo **全部不變**(6/14、9/14、8/14、5/14、9/14)。

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
