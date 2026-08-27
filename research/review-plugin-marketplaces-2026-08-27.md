# packaging 半邊第一次被拉滿:8 個 plugin marketplace(2026-08-27)

- **對象**:`~/.claude/plugins/marketplaces/` 全部 8 個 repo
- **rubric**:2.2.0 / 工具 1.3.0
- **為什麼是這批**:`skill-reviewer` 的 6 條 script differentiator 有 5 條是 packaging 面,
  來自 Phase 1–4 的星數梯度分析、由 G3(最高風險 gate)核准。
  既有審查裡它**開過火但從未拉開**——最高只到 6/14,tier 從未超過 T2。
  plugin marketplace 是能把它拉滿的母體(8 個全有 `marketplace.json`)。

> 🔧 **本節初版寫錯,已更正(2026-08-27,PR #9 開出後自查)**。初版寫
> 「**每一次真實審查裡它們都沒開過火**…packaging 一律 **0/14**,一律宣告「不採計」」——
> **三處皆偽**,而且這正是本 repo 存在的理由要抓的那種句子:
>
> | 初版宣稱 | 實際 |
> |---|---|
> | 一律 0/14 | round 2 有 **2 個 5/14**;08-26 那輪有 **1 個 4/14**;3 個發布 repo **全為 6/14** |
> | 一律宣告「不採計」 | 發布 repo 那輪明寫「packaging 面**如實採計、不宣告豁免**——內部版可以說不採計,發布版不行」 |
> | 5 條從未開過火 | **4 條開過**:`install_oneliner_in_readme`、`has_marketplace_json`、`dir_examples`、`has_tests_or_evals` |
>
> **可辯護的版本(見 §1 的修訂表)**:唯一真的從未開過火的是 `readme_has_before_after`
> ——而它在本批**第一次開火就是假陽性**(§2-B)。那是比初版更強也更真的說法。
>
> 我在寫下那句話之前沒有回查 `self-audit-round2.md:14`、
> `review-installed-skills-2026-08-26.md:31-32`、`review-published-repos.md:12-22`
> ——**三份紀錄都在版控裡,一次 grep 就會推翻它。**

> ⚠️ **污染聲明**:同 [`review-installed-skills-2026-08-26.md`](review-installed-skills-2026-08-26.md)
> ——判讀者已讀過 rubric 全文與 `misjudgments.md`,本輪判定不得充當 inter-rater 資料。

---

## 1. packaging 第一次跑出分佈

| repo | packaging | tier 剖面 | 結構 |
|------|-----------|-----------|------|
| `rust-skills` | **14/14** | T3 | 自含(`source: ./`) |
| `claude-plugins-official` | 12/14 | T3 | **聚合器**(289 plugins,`./external_plugins/*`) |
| `context-mode` | 12/14 | T3 | 自含 |
| `claude-code-warp` | 10/14 | T2 | 自含 |
| `mattpocock` | 8/14 | T2 | 自含 |
| `taste-skill` | 8/14 | T2 | 自含 |
| `superpowers-marketplace` | 6/14 | T1 | **純指標**(4 檔、0 SKILL.md、10 plugins 全 `source: url`) |
| `visual-web-stack` | 3/14 | 低於 T1 | 自含 |

**先講不可比的那兩個。** `superpowers-marketplace` 是純發佈清單,設計上就沒有 skill;
`claude-plugins-official` 是 289 個 plugin 的聚合器(31 份 SKILL.md,大多數 plugin 非 skill 型)。
把它們與自含型 repo 並排比分數是錯的——**這一點必須先確認再解讀,否則排序本身就是假的。**

可比的自含型有 6 個,分佈 3–14/14,tier 橫跨 T1 到 T3。

### 與既有語料的精確對照(取代初版那句錯的「一律 0/14」)

| differentiator | 權重 | 本批之前開過火? | 實據 |
|---|---|---|---|
| `install_oneliner_in_readme` | 3 | ✅ | `andrej-karpathy-perspective`、`huashu-nuwa`(各 5/14)、3 個發布 repo(6/14) |
| `has_marketplace_json` | 3 | ✅ | 3 個發布 repo(6/14 = install 3 + marketplace 3) |
| `dir_examples` | 2 | ✅ | `andrej-karpathy-perspective`、`huashu-nuwa` |
| `has_tests_or_evals` | 4 | ✅ | `turnstile-spin`(4/14) |
| **`readme_has_before_after`** | 2 | ❌ **從未** | 本批第一次開火 —— **而且是假陽性**(§2-B) |

所以本批真正新的是三件事,不是「第一次開火」:

1. **第一次拉到滿檔**:既有語料最高 6/14,本批到 14/14;tier 第一次出現 **T3**
2. **第一次跨 tier 分佈**:T1 → T3 都有,benchmark 的鑑別力第一次可觀察
3. **`readme_has_before_after` 第一次開火,而它是假陽性** —— 一條權重 2、
   `marketing_suspect: true`、`gap_ci95` 含 0 的規則,**在史上第一次命中時就是誤判**

### 但頂端那個分數有 2 分是誤判

見 §2-B:`rust-skills` 的 `readme_has_before_after` 命中的是**功能支援矩陣**而非 before/after 示範。
扣掉後是 12/14,與 `claude-plugins-official`、`context-mode` 同分。
**「唯一滿分」這個觀察不成立。**

### 與 craft 的關係:一個乾淨的對照

`visual-web-stack` packaging **3/14、低於 T1 剖面**,而它的 craft 在
[`review-published-repos.md`](review-published-repos.md) 已判 **approved**。

以前這個對照永遠是「0/14 vs approved」,而 0 可以用「結構上不可能有 packaging」解釋掉。
**現在是 3/14 vs approved——非零、可比,而結論不變:packaging 剖面低不代表 craft 差。**
這是專案核心結論(星數關聯打包面非內容工藝)第一次拿到**非退化**的佐證。

---

## 2. 三個新發現(全部已查證,已記入 `misjudgments.md`)

### A. H-001 對「純指標型 marketplace」判 error,而那是最硬的門檻

`superpowers-marketplace` 共 4 個檔:`README.md`、`LICENSE`、
`.claude-plugin/marketplace.json`、`.claude/settings.local.json`。
10 個 plugin 全部 `source: url` —— **它是發佈清單,設計上不含任何 skill**。

lint 的判定:

```
H-001 pass=False severity=error | 合規 SKILL.md 數=0
craft_llm_todo = []
```

依 `SKILL.md` 步驟 2,hygiene error 未過 → **craft verdict 直接 needs-revision,不必往下**。
於是工具對一個**正在正確履行其職責**的 repo 輸出「需要修正」。

**這不是措辭問題,是缺一個判別。** 輸出無法區分兩件事:
- 「這不是一個 skill repo」
- 「這是一個壞掉的 skill repo」

兩者的處置完全不同,而現在它們塌成同一個 verdict。
下游後果具體:ASP `pipeline.md` 對 hygiene error 是 `issues.append(...)` → **擋 gate**
(安全紅旗才降 YELLOW_FLAG,hygiene error 不降)。

⚠️ **對照**:H-004 有 `knowledge_only` 豁免、L-002 有兩型豁免、L-004 有 exemption——
**只有 H-001 沒有形狀豁免,而它是唯一的 auto-fail。**

### B. R-005 `readme_has_before_after` 誤中功能比較表

`BEFORE_AFTER_RE` 的 `✅.{0,500}?❌|❌.{0,500}?✅` 分支會命中支援矩陣。實查三例:

| repo | 命中位置 | 命中內容 | 判定 |
|---|---|---|---|
| `rust-skills` | `README.md:143` | `✅ \| ✅ \| ✅ \| ⏎ \| Auto meta-cognition trigger \| ✅ \| ✅ \| ❌` | **假陽性**(功能支援矩陣) |
| `mattpocock` | `README.md:109` | `BEFORE**: "There's a problem when a lesson…` | 真陽性 |
| `context-mode` | `README.md:45` | `Before: 47 × Read() = 700 KB. After…` | 真陽性,且是**理想形式**(帶量化) |

`Before…After` 分支運作正常;出問題的是 `✅/❌` 那一支。

這與 [`directive-polarity.md`](directive-polarity.md) 的結論**同源但不同機制**:
該檔證明 `❌/✅` 配對在 **SKILL.md** 上顯著集中於單一作者血統(P=0.0039),
故確定性配對門檻實為血統偵測器。這裡是**同一個 regex 分支在 README 上的另一種失效**
——不是血統,是**表格**。兩者合起來:`✅/❌` 這個訊號在兩種語料上各有各的失效方式。

R-005 權重 2,`marketing_suspect: true`,`gap_ci95` **含 0**(rubric.yaml 已標)。
本輪等於給那條 CI 含 0 的註記再添一個具體理由。

### C. S-003 `self_update` 的 agent-facing 收窄含 `hooks/`,而 hooks 是程式碼

`claude-plugins-official` 標了 4 個 security flag。依步驟 5 逐一複核:

| flag | 命中源 | 複核 |
|---|---|---|
| S-001 `obey_external_output` | `plugins/frontend-design/skills/frontend-design/SKILL.md:31`「Where the brief pins down a visual direction, **follow it exactly** — the brief's own words always win」 | **假陽性**。指的是遵循**使用者的設計 brief**,不是服從外部工具輸出。**rubric 已明文預告過這一型**(「S-001 的 regex 會誤中正當文件的『follow the guide exactly』」) |
| S-003 `self_update` | `plugins/security-guidance/hooks/security_reminder_hook.py:838,845` | **假陽性,且成因是新的**——見下 |
| S-002 `registers_hooks` | 該 repo 確有 hooks | 真陽性(事實陳述,非缺陷) |
| S-101 | 正向防禦樣態 | 正向標記 |

**S-003 這一則的成因值得記**。命中的原文是:

> `_PUSH_RANGE_RE` is not push-specific — `git fetch` and `git pull` print range lines…

那是一個**解析 git 輸出的安全 hook**,在註解裡**說明 git 指令會印什麼**。
它不是「skill 每次啟動自我更新」。

而它之所以沒被既有收窄擋掉,是因為 `self_update` 的 agent-facing 定義是
**`SKILL.md` 全文 + `hooks/`**。那次收窄(final review M4)是為了排除
README 的「## 更新 → git pull」這種**給人看的散文**,校準時想的是散文。
**沒有人想過 `hooks/` 裡放的是程式碼——而程式碼裡談論 git 指令是完全正當的。**

⚠️ 兩個假陽性都被 `confidence: low-static-needs-llm` 正確標記,
步驟 5 的複核流程如設計運作。**工具沒壞,是收窄的校準面漏了一種內容型態。**

---

## 3. hygiene 其餘

- `taste-skill` H-003 warning:SKILL.md 過長且無 `references/` 拆分
- 8 個 repo 的 `noncompliant_skills` **全為 0**——H-005 逐檔合規全過
- 除 `superpowers-marketplace` 外,無 hygiene error

## 4. 對本專案的意義

1. **packaging 半邊第一次被拉滿,而 `readme_has_before_after` 史上第一次開火就是假陽性。**
   ⚠️ 初版在此寫「第一次被行使…每一次審查都是 0/14」——**已更正,見檔首**。
   既有語料它開過火但從未超過 6/14;真正從未開過的只有 R-005 那一條。
   **一條從未命中過的規則,也是一條從未被檢驗過的規則** —— 而它一命中就錯。
2. **「低 packaging ≠ 低 craft」拿到非退化佐證**:`visual-web-stack` 3/14 vs craft approved。
   以前的 0/14 可以用「結構上不可能」解釋掉,3/14 不行。
3. **三個新發現全部來自「拿工具去用一個沒用過的母體」**,零個來自更多分析——
   與 `self-audit-round2.md` §12–15 的歸類一致,再添一批樣本。
4. **形狀盲點又出現一次**(H-001 對純指標型)。這是 rubric 第 N 次在**沒見過的形狀**上失準:
   round 2 有 6 次(patterns.md 套錯形狀)、2026-08-26 有 1 次(`.txt`/LICENSE)、本輪 1 次。
   共同結構是**判準隱含了一個「典型 repo 長什麼樣」的假設,而母體一換就露餡**。
