# 研究:97 個 Agent Skill repo 的星數梯度

> 這一頁是 `README.md` 搬出來的完整研究內容 —— 星數梯度、方法論、統計限制、
> pipeline、自審紀錄。README 只留「這是什麼 / 怎麼裝 / 怎麼用 / 能信到什麼程度」。
>
> **與 [`research/EXECUTIVE-SUMMARY.md`](../research/EXECUTIVE-SUMMARY.md) 的分工**:
> 那份是 BRIEF 定義的**交付物**(D1–D6 的一頁總結,對照 spec 驗收用);
> 本頁是**給讀者的敘述**,同一批事實的不同用途。數字若有出入,以
> [`research/rubric.yaml`](../research/rubric.yaml) 與
> [`research/feature_matrix.json`](../research/feature_matrix.json) 為準。

## 兩類特徵的星數走勢完全相反

同一批 repo、同一組分層(T0=100–1k 星 → T3=100k+ 星):

**打包面 —— 沿星數單調爬升**

```
marketplace.json          一行安裝說明
T0  ██████··············  28.6%      T0  ███████████·········  57.1%
T1  ████████████········  62.5%      T1  ████████████········  62.5%
T2  ████████████········  60.6%      T2  ████████████████····  78.8%
T3  ████████████████████ 100.0%      T3  ████████████████████ 100.0%
```

**工藝面 —— 沒有梯度,最低星那層甚至最高**

```
description 有觸發語        references/ 分層(progressive disclosure)
T0  ██████████████······  71.4%      T0  █████████████████···  85.7%
T1  ██████████··········  50.0%      T1  ███████████████·····  75.0%
T2  ████████████········  60.6%      T2  ██████████████······  69.7%
T3  ██████████··········  50.0%      T3  █████████████·······  66.7%
```

左邊那兩條能被 regex 數出來,右邊那兩條不能——**而右邊才是你真正想知道的**。
這就是為什麼 `skill-reviewer` 的 lint 只負責 packaging 與安全門檻,
**craft 判讀交給 LLM,而且它是主判**。

**⚠️ 這四條在分析裡的實際身分,以及上圖沒有畫的東西**(星數為 2026-08-16 快照):

| 圖上的特徵 | 分類 | T3−T0 gap | bootstrap 95% CI |
|---|---|---|---|
| `has_marketplace_json` | differentiator | +71.4pp | `[42.9, 100.0]` — 寬 57.1pp,**不含 0** |
| `install_oneliner_in_readme` | differentiator | +42.9pp | `[14.3, 85.7]` — 寬 71.4pp,**不含 0** |
| `desc_has_trigger_majority` | **noise** | **−21.4pp**(ρ −0.131) | **未計算**(CI 只算給 differentiator)|
| `dir_references` | **noise** | **−19.0pp**(ρ −0.224) | **未計算** |

**上圖畫的是 5 條 differentiator 裡 CI 最窄的兩條** —— 這件事得自己說出來。
最弱的兩條(`has_tests_or_evals`、`readme_has_before_after`,CI 皆 **[−11.9, 85.7]**、
**含 0**)**不在圖上**;`dir_examples` 的 CI 寬 95.2pp 也不在。
**含 0 的意思是「就梯度這一條證據而言,與沒有梯度無法區分」**——
逐條見[統計限制](#統計限制必讀)。

## 我們用自己的 rubric 審自己

```bash
python3 skill-reviewer/scripts/lint_skill.py . \
  --exclude "research/repos,skill-reviewer/evals/fixtures"
```
```
[hygiene] pass  H-001=✓ H-005=✓ H-003=✓ H-004=✓
[packaging tier · 僅 packaging 面] 12/14 → 符合 T3(頂層)剖面
[craft tier] PENDING-LLM(讀 craft_llm_todo 後由 SKILL.md 層填)
[gap list · packaging] ['readme_has_before_after']
[security] S-001:obey_external_output(low-static-needs-llm); S-003:cred_in_argv(medium); S-003:self_update(low-static-needs-llm); S-101:defensive_untrusted_clause(low-static-needs-llm)
```

起點是 **0/14**;補上 marketplace.json、`install.sh`、`examples/`、迴歸測試後到 11/14,
2026-08-27 的 README 重整後到 **12/14**。那次分數變動有**兩個獨立成因**,
兩個都值得記,因為它們的方向相反:

### ⚠️ 「刻意不補一行安裝」那條取捨,理由本來就不成立

原文寫:「rubric 認的一行安裝是 `curl … | sh` 或 `npx`,但**一個做安全審查的工具
去推廣 `curl | bash`,自相矛盾**」。

**那句話只涵蓋了 `INSTALL_RE` 六個分支裡的兩個。** 實測整條 regex:

```
✅ '/plugin marketplace add astroicers/skill-quality-research' → 命中
✅ '/plugin install skill-reviewer@skill-reviewer'             → 命中
```

`/plugin\s+(?:install|marketplace)` **一直都在名單上**,而 `.claude-plugin/marketplace.json`
與 `plugin.json` 我們**兩個檔案都早就有了** —— 缺的只是 README 沒寫。
Claude 原生安裝路徑既滿足這條規則,又**完全不必推廣 `curl | bash`**。

**這是自我更正,不是默默補格子。** 原本的取捨是真誠的,但**論證範圍小於它自己引用的規則**
——與本專案記錄過的其他誤判同型:主張的範圍超出(或這次是**小於**)證據的範圍。

### ⚠️ 而 `readme_has_before_after` 那 2 分,本來就是假陽性

舊的 11/14 裡有 2 分來自它。唯一命中點是舊 README 的字面字串 `before-after`,
出現在「已知近似值」**列舉偵測器名稱**的那一行
(`regex 啟發式(trigger / install / before-after / metric / …)`)
—— **不是 before/after 示範**,與 `cred_in_argv` 命中我們自己的 rubric 同型。

那一段這次搬到本頁,README 的命中因此歸零,該項轉為 `gap_list` 的唯一缺項。
**所以「11/14 → 12/14」不是淨賺 1 分,是 `+3(真實補上)−2(假陽性消失)`。**

⇒ 現在的 12/14 比舊的 11/14 **更誠實而不是更高分**。
剩下那 2 分 **刻意不補**:before/after 對照要有真的對照才寫,
為了補格子去湊一個,正是這份 rubric 在 `marketing_suspect: true` 標註裡警告的事。
**rubric 是 proposal 不是法律**;它的價值在把取捨攤開,不是逼你把每格打勾。

**自審會看到三條 security 紅旗,三條都查過了**(另有一條 `S-101` 是
**正向防禦樣態、`polarity: positive`,不是紅旗**——把它算進紅旗數是本研究記錄過的
一次自我更正,見 [`research/misjudgments.md`](../research/misjudgments.md) 2026-08-26 那批):

- `S-003:cred_in_argv`(medium)命中 **11 處,全部是本專案的文件在描述這個樣態**——
  兩份 rubric 副本各 1 處(`--api-key a` 是規則的反例文字)、
  `self-audit-round2.md` 5 處、`review-installed-skills-2026-08-26.md` 2 處、
  `misjudgment-review-2026-08-26.md` 1 處,以及**這份 README 的這一段本身** 1 處。
  一份安全 rubric 無法描述自己的偵測樣態而不觸發自己;連談論它的報告也會
  ——**這個數字會隨文件增加而長,不代表偵測變嚴**。
  **刻意不修**:合理的修法是把它收窄到 agent-facing 檔(`self_update` 就是這樣做的),
  但本研究有一次真陽性(`anysearch`)的 `--api_key` 是實作在 `.ps1` 腳本裡而非 SKILL.md,
  收窄會漏掉那類發現。**寧可留假陽性,不要漏真陽性**——這也正是它被標 `warning` 而非
  `error`、且 SKILL.md 要求 LLM 複核的原因。
- `S-001` / `S-003:self_update` 標 `low-static-needs-llm`,查證後同屬文件敘述。

> `confidence` 的兩個值(`medium` / `low-static-needs-llm`)**不是形容詞,是對複核者的
> 舉證責任分配**——完整語意見 `rubric-manual-dimensions.yaml` 的 `confidence_values`
> (3.2.0 起入條文;在此之前它們只存在於 lint 的程式碼裡,而整套複核紀律就掛在那兩個詞上)。

複核紀律:**去查,不是憑印象推翻**。本研究記錄過一次審查者(我)憑印象判定假陽性、
實際上 rubric 是對的([`research/self-audit-round2.md`](../research/self-audit-round2.md) §2)。

**自審為什麼要 `--exclude`**:本 repo 內有兩類「不是我們自己的」SKILL.md——
`research/repos/` 的第三方 clone,以及 `skill-reviewer/evals/fixtures/` 裡**故意寫壞**的測試樣本。
不排除的話前者會讓 `dir_examples` 虛報為「有」(自審時實際踩過,因此新增了 `--exclude`),
後者會讓 H-005 報出你刻意留的壞檔。**任何有 vendored clone 或測試 fixture 的 repo 都會遇到這件事**
——研究樣本中的 `NVIDIA/SkillSpector` 就是全部 SKILL.md 都在 `tests/fixtures/` 的例子。

更多校準紀錄見 [`research/self-audit-round2.md`](../research/self-audit-round2.md)。

## 判定門檻在看到資料之前就寫進 git 了

分析門檻能不能相信,取決於它是**先定好**的、還是看完資料回頭湊出來的。
這件事不必相信我們的說法——git 可以驗:

```bash
git show 453316e:scripts/aggregate_stats.py | grep -A4 'THRESHOLDS = {'
git show 453316e:research/repos.json      | head -3        # mode: offline-seeds-only
```

| 時間(+08:00) | commit | 內容 | 當時的資料 |
|---|---|---|---|
| 08-16 **16:12** | `453316e` | BRIEF 全文(含去混淆三道工序)+ `THRESHOLDS` 四個常數<br>`hygiene_min_prevalence: 70.0` / `hygiene_max_range: 20.0` / `diff_min_gap: 30.0` / `min_tier_n: 3` | `repos.json` = `mode: offline-seeds-only`,**32 筆種子,零真實資料** |
| 08-16 **18:56** | `80f734f` | Phase 1 全量收集 | 真實資料首次進 repo |
| 08-16 **20:41** | `d0550cd` | 最終 `rubric.yaml` | — |

**門檻與分類規則比真實資料早 2 小時 43 分進 git。** 所以「哪些特徵算 hygiene、哪些算
differentiator」不是挑出來的——規則先寫死,資料進來後照跑,結果就是結果。

這也是為什麼我們留下了**對自己不利**的產出:5 條 differentiator 有 4 條是 packaging/marketing 面,
`desc_has_trigger_majority`(最直覺該是好工藝的指標)判成 noise 且 T0 最高,
兩條 differentiator 的 bootstrap CI 含 0。若門檻是事後訂的,這些都可以被調掉。

---

**專案狀態**:Phase 0–6 完成,三道 HITL gate 皆 approved。所有產出仍是 **proposal**,供人工審查。
完整摘要見 [`research/EXECUTIVE-SUMMARY.md`](../research/EXECUTIVE-SUMMARY.md)。

## 交付物

| ID | 檔案 | 內容 |
|----|------|------|
| D1 | `research/repos.json` | 97 repos + tier/domain/fame/cohort 標籤 |
| D2 | `research/feature_matrix.{csv,json}` | 80 repos × 65 欄特徵矩陣 |
| D3 | `research/patterns-report.md` | 量化梯度 + 質化模式 + 混淆因子分析 |
| D4 | `research/rubric.yaml` + `rubric-manual-dimensions.yaml` | 分級 rubric(script differentiator + craft/hygiene/security) |
| D5 | `skill-reviewer/` | skill 雛形(SKILL.md + lint + references + evals + plugin) |
| D6 | `research/self-audit.md`(+ round 2) | 回測 22 個自家 skill 的校準報告 |
| — | `research/EXECUTIVE-SUMMARY.md` | 一頁總結 |
| — | `research/qualitative_notes/` | 54 份 LLM 質化抽讀筆記 |

**`*-draft` 檔是腳本自動產出的中間件**(`aggregate_stats.py` 每次執行都會重寫):
`patterns-report-draft.md` / `rubric-draft.yaml`。無 `-draft` 者才是經人工審定的交付物。

---

## Pipeline(重跑或延伸用)

```
Phase 0  環境        gh auth login (或 export GITHUB_TOKEN)
                     python3 scripts/{collect_repos,extract_features,aggregate_stats}.py --selftest
Phase 1  收集   →G1  python3 scripts/collect_repos.py
Phase 2  clone       python3 scripts/clone_repos.py
Phase 3a 特徵   →G2  python3 scripts/extract_features.py --limit 5   # 小批次鎖 schema
                     python3 scripts/extract_features.py             # 全量
Phase 3b 質化        LLM 抽讀(依 feature_matrix 的 phase3b_sample 確定性名單)
Phase 4  合成   →G3  python3 scripts/aggregate_stats.py
Phase 5  封裝        skill-reviewer/
Phase 6  回測        research/self-audit*.md
```

**Phase 1 需要 GitHub API**(claude.ai/code 的 remote 容器封鎖 `/search/*`,詳見
`research/PHASE0-environment-report.md` §2);Phase 2 起兩種環境皆可。

### 各腳本職責

| 腳本 | Phase | API 面 | 檔案系統面 |
|------|-------|--------|-----------|
| `collect_repos.py` | 1 | 搜尋、tier/cohort/fame、prior_fame、engagement | — |
| `backfill_repo_fields.py` | 1 補 | `open_issues` / `owner_is_org` | — |
| `clone_repos.py` | 2 | — | shallow clone + **defang**(移除執行位) |
| `extract_features.py` | 3a | 僅 `git ls-remote --tags`(`--offline` 可關) | 全靜態解析 |
| `backfill_taxonomy.py` | 2 後 | — | 兩段式回填 taxonomy(stage-1 script) |
| `aggregate_stats.py` | 4 | — | tier 梯度、三分類、去混淆三道工序、gap bootstrap CI |
| `check_stdlib_only.py` | 守門 | — | 零依賴 allowlist(選用依賴須被 try 包住) |
| `check_parser_agreement.py` | 守門 | — | 三條 frontmatter parser 路徑等價性 |

### 測試

每支腳本自帶 `--selftest`(純函式與分類器斷言,零網路)。
`aggregate_stats.py --selftest` 用 40 個合成 repo 的固定夾具,驗證 differentiator /
hygiene / noise / marketing-suspect 是否被正確分類,並斷言 bootstrap CI 可重現(固定種子)。
`lint_skill.py --selftest` 另含 **drift-guard**:硬編的 differentiator **weight 與 signal**
與 `references/rubric.yaml` 不一致即 fail,security 的 **confidence 逐 flag** 與
`rubric-manual-dimensions.yaml` 不一致亦 fail(值域雙向相等:用了沒定義的值、
或定義了沒人用的值,都轉紅)。

**兩道環境守門**(2026-08-17 新增,起因見下方「已知近似值」):
```bash
python3 scripts/check_stdlib_only.py        # 零依賴聲明:allowlist + 選用依賴須有 try/fallback
python3 scripts/check_parser_agreement.py   # 三條 parser 路徑讀同一份 SKILL.md 必須同結果
```
CI 的 `python` job 在 **3.9 / 3.10 / 3.11 / 3.12 / 3.13** 五個版本上各跑一次
(`fail-fast: false`),並且**先在沒有 PyYAML 的環境跑一遍、再裝上 PyYAML 跑第二遍**——
「零依賴」與「兩條 parser 路徑等價」都是實測出來的,不是宣稱的。

**行為迴歸**(與 selftest 分工:selftest 測純函式,這個測端到端契約):
```bash
python3 skill-reviewer/evals/run_evals.py        # fixtures + 真實 repo
python3 skill-reviewer/evals/run_evals.py --ci   # 只跑已提交的 fixtures
```
10 條 fixture 契約鎖住核心行為。前五條是端到端的擋/不擋分界:合格不擋、
H-001 盲點由 H-005 補上、change-scoped 只擋改壞的、**安全紅旗刻意不擋**
(改成擋會 fail,提醒你那是設計變更需先改 ADR)、`--exclude` 生效。
後五條鎖住**判準與案例檔不得脫節**:craft verdict 取值域三處一致、上卷規則與 `evals.json` 逐案對帳、
`security` 欄位語意(**lint 命中 ≠ 複核確認成立**)、`security` 標註必須對應真實的 lint 命中、
`expect_block` 每個 case 必填且程式端無預設。
CI 每次 push/PR 都跑(見 `.github/workflows/validate.yml`)。

---

## 已知近似值

所有 deterministic proxy 皆非 ground truth,逐條記錄於 `research/G2-review-notes.md` 與
`research/code-review-notes.md`。重點:

- regex 啟發式(trigger / install / before-after / metric / media / ci-validates)
- `open_issues` 為 GitHub API 的 issues+PRs 合計
- `nonauthor_pr_count` 對 org repo 偏高(已補 `owner_is_org` 供分層)
- 分類門檻常數集中於 `aggregate_stats.py` 的 `THRESHOLDS`
- **PyYAML 是選用依賴,所以「有裝/沒裝」曾經會得到不同數字**——2026-08-17 發現並修掉:

  `extract_features.py` 的 frontmatter 解析有 PyYAML 快路徑與 naive fallback 兩條;
  研究期間本機裝了 PyYAML 6.0.3,**所有已發布數字都產自快路徑,fallback 從未在真實語料上驗證**。
  補測 161 份真實 SKILL.md 後找到 3 份分歧(`anthropics/skills` 的 pptx / xlsx /
  slack-gif-creator):fallback 沒有還原雙引號內的 `\"` 轉義,`desc_len` 差 6 字元。
  **對 rubric 規則零影響**(name/description 非空與 trigger regex 都不受反斜線影響),
  只動到 `desc_len_median` 這個 numeric-profile 觀察值。已修,分歧 3 → 0。

  三項後續:`feature_matrix.json` 新增 `frontmatter_parser` 欄位讓輸出自我描述
  (既有檔案已回填並標示為回填);`scripts/check_parser_agreement.py` 成為永久守門;
  `skill-reviewer/evals/fixtures/yaml-escapes/` 把該 bug 固化為 CI 拿得到的回歸夾具。

## 統計限制(必讀)

- n=54(rubric 樣本),**不跑迴歸、不宣稱顯著**;differentiator 的 ρ(log★) 僅 0.19–0.32(弱)
- **gap 的 bootstrap CI 極寬,2 條 differentiator 的 CI 含 0**(2026-08-17 補算,B=2000 層內重抽):

  | feature | gap | 95% CI |
  |---|---|---|
  | has_marketplace_json | 71.4pp | [42.9, 100.0] |
  | dir_examples | 52.4pp | [4.8, 100.0] |
  | install_oneliner_in_readme | 42.9pp | [14.3, 85.7] |
  | **has_tests_or_evals** | 38.1pp | **[−11.9, 85.7]** ⚠ |
  | **readme_has_before_after** | 38.1pp | **[−11.9, 85.7]** ⚠ |

  T3 只有 **n=3**,CI 寬到 90pp 以上是結構性必然。含 0 的意思是「就梯度這一條證據而言,
  與沒有梯度無法區分」。weight 保留原值是因為另有 F0 草根復現、機制陳述、evidence_strength
  三條獨立證據線;**只採信梯度證據的讀者應把這兩條視為 weight 未定**。
  CI **不是**顯著性檢定,不得因不含 0 而宣稱顯著。
- **craft 判定的一致性已量測一次(2026-08-17)**,結果與行動見
  [`research/inter-rater-results.md`](../research/inter-rater-results.md):

  | 維度 | Fleiss κ | 成對一致率 |
  |---|---|---|
  | L-001 觸發設計 | 0.862 | 0.952 |
  | L-003 scope 邊界 | 0.754 | 0.905 |
  | L-002 規則附 why | 0.597 | 0.846 |
  | **L-004 anti-hallucination** | **0.400** | **0.595** |
  | 整體 | 0.628 | 0.824 |

  ⚠️ **這是上界不是 inter-rater**:三位審查者是**同一個模型**在獨立 context 跑。
  一致性低 → 判準確實有歧義(硬結論);一致性高 → 只代表沒排除問題,換人只會更低。
  n=55 格很小,κ 在此規模不穩定;報告不設通過門檻。
  **L-004 獨佔 14 個分歧中的 8 個**,三位獨立指出同樣的邏輯矛盾(`good` 與 `n/a` 兩條路徑
  對「無易腐事實但有反編造條款」的 skill 同時成立)→ 已改寫條文,`rubric_version` 升 **2.0.0**。
  執行中還發現一個協定缺陷:**rubric 的 `evidence_refs` 具名了 6 個樣本 repo**,
  那 5 格的一致性是 **1.000**(零分歧)——主數字已排除它們。

  **第二輪(2026-08-18)推翻了「用這個方法驗證 rubric 修訂」的可行性**
  ([`inter-rater-results-round2.md`](../research/inter-rater-results-round2.md)):
  同基準比對下,**兩個條文完全沒改的維度變動幅度大於我改過的兩個**
  (L-003 −0.319、L-001 −0.213 vs L-002 −0.068、L-004 +0.091)。
  **在 n≈14 的規模,輪間變異吞掉了 rubric 修訂的效果。** 整體數字倒是穩:
  PA 0.824 → 0.806、κ 0.628 → 0.539。**要引用就引用整體 PA,不要引用分維度 κ。**
  唯一跨輪重現的:L-004 的成對一致率兩輪都墊底。
- 所有 differentiator 對 `fork_star_ratio` 幾乎全負 → 差異化項**未被 fork 行為背書**
- hygiene 門檻多數來自官方規範三角驗證,非本樣本 prevalence(樣本以合規 SKILL.md 篩選)
- 已知偏斜:T0 領域偏 design-ui;C3 世代 n=3 過薄

## 關於研究中具名的第三方 repo

本研究分析 97 個公開 repo,報告與 54 份質化筆記中會具名引用它們作為樣態實例。
四點說明:

1. **全部是公開原始碼的靜態閱讀**——從未執行任何 clone 內的檔案(Iron Rule 7)
2. **不是漏洞揭露,不宣稱任何作者有惡意**。標為 `injection-suspect` 意思是
   「這段文字在結構上與 injection 載體同構」,多數情況作者意圖顯然善意
3. **樣態是發現,repo 只是可查證的證據**——換成任何有相同寫法的 repo,結論相同
4. **快照為 2026-08-16/17**,repo 內容會變;每則觀察對應 `clone-manifest.json` 的 commit

若你是被引用的 repo 作者、認為我們讀錯了,請開 issue——本研究自己就記錄過
7 次 rubric 誤判與 1 次審查者誤判。

## 目錄

```
research/BRIEF.md          ← spec(唯一權威)
research/                  ← 所有 phase 產出(disk-based handoff)
research/qualitative_notes/← 54 份質化筆記
research/repos/            ← untrusted clone(gitignored);2026-08-17 清至 evals 需要的 5 個
                              (105M),其餘 75 個已刪 — 見 research/repos/README.md
scripts/                   ← 13 支:pipeline(collect/clone/extract/aggregate)+ 量測 + 守門
skill-reviewer/            ← D5 產出的 skill
docs/superpowers/          ← P3(掛入 ASP G5)的 spec / plan / 驗證 / SDD ledger
seeds/seed_repos.json      ← 2026-08-16 驗證的種子清單
```
