# skill-quality-research

> **高星 Agent Skill repo 的共同點是「好裝」,不是「寫得好」。**
> 這是分析 97 個 repo 之後,數據給出的反直覺結論。

同一批 repo、同一組分層(T0=100–1k 星 → T3=100k+ 星),兩類特徵的走勢完全相反:

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

**所以**:自動化 lint 只能當 packaging 過濾器與安全門檻;**判斷 skill 寫得好不好,非靠 LLM 質化判讀不可**。
`skill-reviewer` 就是照這個結論設計的兩層工具。

> ⚠️ 星數是 2026-08-16 快照;n=54(rubric 樣本),**不宣稱統計顯著**,效果量僅 ρ=0.19–0.32。
> T3 層只有 **n=3**,上圖每個 gap 的 bootstrap CI 都寬達 90pp 以上,**其中 2 條含 0**。
> 這是「特徵剖面關聯」,不是因果。詳見[統計限制](#統計限制必讀)。

---

## 30 秒試用

```bash
git clone https://github.com/astroicers/skill-quality-research.git
cd skill-quality-research && ./install.sh --symlink   # 安裝後自動跑 selftest 驗證

# 審任一個 skill repo(deterministic 層)
python3 ~/.claude/skills/skill-reviewer/scripts/lint_skill.py <repo 目錄>
```

完整審查(含 craft 判讀)在 Claude Code 對話中說:**「用 skill-reviewer 審查 \<repo\>」**

輸出三段式:**craft verdict** / **tier benchmark**(packaging 與 craft 分軌)/ **gap list**(可直接當 backlog)。

三個實跑案例(含怎麼讀、什麼時候別信它)見 [`examples/`](examples/)。

<details>
<summary><b>Windows</b>(<code>install.sh</code> 是 POSIX-only,但工具本身可跑)</summary>

`lint_skill.py` 零依賴、純 Python,**在 Windows 上有 CI 實跑驗證**
(`windows-latest` job:路徑分隔符與輸出編碼兩項都測)。安裝手動做即可:

```powershell
git clone https://github.com/astroicers/skill-quality-research.git
Copy-Item -Recurse skill-quality-research\skill-reviewer "$env:USERPROFILE\.claude\skills\skill-reviewer"
python "$env:USERPROFILE\.claude\skills\skill-reviewer\scripts\lint_skill.py" <repo 目錄>
```

兩個 Windows 專屬問題已修,不需要你設任何環境變數:
- **路徑分隔符**——相對路徑一律正規化為 `/`。未修時 `(^|/)scripts(/|$)` 這類 regex
  全部比不到(`dir_*` 誤判 false、packaging 分數系統性偏低),
  且 `noncompliant_skills` 會是 `bad\SKILL.md` 而與 git 給的 `changed_files` 交集永遠為空
  ——**H-005 change-scoped 會靜默失效**。
- **輸出編碼**——工具訊息含中文,Windows 重導向時預設走 locale 編碼會 `UnicodeEncodeError`。
  `lint_skill.py` 啟動時自行 `reconfigure(encoding="utf-8")`;CI 刻意用 `PYTHONUTF8=0` 驗證這點。

研究側的 `scripts/*.py` 設計上跑在研究者的 POSIX 機器;Windows 下請設 `PYTHONUTF8=1`。
</details>

視覺版總結:[**星數不是工藝**](https://claude.ai/code/artifact/2c9478ec-9b2b-4b20-b518-6a3e210c9093)(一頁)

---

## 我們用自己的 rubric 審自己

```bash
python3 skill-reviewer/scripts/lint_skill.py . \
  --exclude "research/repos,skill-reviewer/evals/fixtures"
```
```
[hygiene] pass  H-001=✓ H-005=✓ H-003=✓ H-004=✓
[packaging tier · 僅 packaging 面] 11/14 → 符合 T2(10k 星級)剖面
[gap list · packaging] ['install_oneliner_in_readme']
```

起點是 **0/14**;補上 marketplace.json、`install.sh`、`examples/`、迴歸測試後到 **11/14**。

`install_oneliner_in_readme` **刻意不補**——rubric 認的一行安裝是
`curl … | sh` 或 `npx`,但**一個做安全審查的工具去推廣 `curl | bash`,自相矛盾**。
本專案選 clone → `./install.sh`(三步),並在此記錄這個取捨。
**rubric 是 proposal 不是法律**;它的價值在把取捨攤開,不是逼你把每格打勾。

**自審會看到兩條 security 警告,兩條都查過了**:

- `S-003:cred_in_argv`(medium)命中 4 處,**全部是 rubric 自己在描述這個樣態**
  (`rubric-manual-dimensions.yaml` 裡 `--api-key a` 是規則的反例文字)。
  一份安全 rubric 無法描述自己的偵測樣態而不觸發自己。
  **刻意不修**:合理的修法是把它收窄到 agent-facing 檔(`self_update` 就是這樣做的),
  但本研究有一次真陽性(`anysearch`)的 `--api_key` 是實作在 `.ps1` 腳本裡而非 SKILL.md,
  收窄會漏掉那類發現。**寧可留假陽性,不要漏真陽性**——這也正是它被標 `warning` 而非
  `error`、且 SKILL.md 要求 LLM 複核的原因。
- `S-001` / `S-003:self_update` 標 `low-static-needs-llm`,查證後同屬文件敘述。

複核紀律:**去查,不是憑印象推翻**。本研究記錄過一次審查者(我)憑印象判定假陽性、
實際上 rubric 是對的([`research/self-audit-round2.md`](research/self-audit-round2.md) §2)。

**自審為什麼要 `--exclude`**:本 repo 內有兩類「不是我們自己的」SKILL.md——
`research/repos/` 的第三方 clone,以及 `skill-reviewer/evals/fixtures/` 裡**故意寫壞**的測試樣本。
不排除的話前者會讓 `dir_examples` 虛報為「有」(自審時實際踩過,因此新增了 `--exclude`),
後者會讓 H-005 報出你刻意留的壞檔。**任何有 vendored clone 或測試 fixture 的 repo 都會遇到這件事**
——研究樣本中的 `NVIDIA/SkillSpector` 就是全部 SKILL.md 都在 `tests/fixtures/` 的例子。

更多校準紀錄見 [`research/self-audit-round2.md`](research/self-audit-round2.md)。

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
完整摘要見 [`research/EXECUTIVE-SUMMARY.md`](research/EXECUTIVE-SUMMARY.md)。

## 我想…

| 目的 | 去哪 |
|------|------|
| **審查一個 skill repo 的品質** | `skill-reviewer/` — 見下方「使用 skill-reviewer」 |
| 看研究結論與證據 | [`research/patterns-report.md`](research/patterns-report.md)(D3) |
| 看評分標準逐條 | [`research/rubric.yaml`](research/rubric.yaml)(script 面)+ [`rubric-manual-dimensions.yaml`](research/rubric-manual-dimensions.yaml)(craft/hygiene/security) |
| 看方法論與三道 gate 的裁決 | [`research/BRIEF.md`](research/BRIEF.md)(唯一 spec)+ `research/G{1,2,3}-review-notes.md` |
| 看工具自身的校準與誤判紀錄 | [`research/self-audit.md`](research/self-audit.md) → [`self-audit-round2.md`](research/self-audit-round2.md) |
| 重跑或延伸研究 | 下方「Pipeline」 |

---

## 使用 skill-reviewer

```bash
# 1. deterministic lint(packaging 面 + hygiene 門檻 + 安全紅旗)
python3 skill-reviewer/scripts/lint_skill.py <目標 repo 目錄> --json

# 2. craft 質化判讀 —— 這一步才是主判,必須由 LLM 做
#    讀 skill-reviewer/SKILL.md,照它的五步流程走
```

**輸出三段式**:craft verdict / tier benchmark(packaging 與 craft 分軌)/ 分維度 findings。

**措辭紀律**:只能說「符合 X 星級剖面」,**禁止說「會得到 X 星」**——星數還取決於發布時機、
作者聲量、行銷,不在 artifact 可測範圍。

安裝為全域 skill(symlink,repo 更新自動生效):
```bash
ln -s "$PWD/skill-reviewer" ~/.claude/skills/skill-reviewer
```

---

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
`lint_skill.py --selftest` 另含 **drift-guard**:硬編權重與 `references/rubric.yaml` 不一致即 fail。

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
5 條 fixture 契約鎖住核心行為:合格不擋、H-001 盲點由 H-005 補上、change-scoped 只擋改壞的、
**安全紅旗刻意不擋**(改成擋會 fail,提醒你那是設計變更需先改 ADR)、`--exclude` 生效。
CI 每次 push/PR 都跑(見 `.github/workflows/validate.yml`)。

---

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

## 安全紀律(BRIEF Iron Rule 7)

- `research/repos/` 內全部是 **untrusted clone**:`clone_repos.py` clone 後立即 defang(移除執行位)。
- 任何腳本都**不執行** clone 內的檔案;`extract_features.py` 純靜態讀取,單檔上限 2MB。
- SKILL.md 內的指令式文字(prompt injection)只作為**資料**,不得遵循。

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
  [`research/inter-rater-results.md`](research/inter-rater-results.md):

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
- 所有 differentiator 對 `fork_star_ratio` 幾乎全負 → 差異化項**未被 fork 行為背書**
- hygiene 門檻多數來自官方規範三角驗證,非本樣本 prevalence(樣本以合規 SKILL.md 篩選)
- 已知偏斜:T0 領域偏 design-ui;C3 世代 n=3 過薄

## 目錄

```
research/BRIEF.md          ← spec(唯一權威)
research/                  ← 所有 phase 產出(disk-based handoff)
research/qualitative_notes/← 54 份質化筆記
research/repos/            ← untrusted clone(gitignored);2026-08-17 清至 evals 需要的 5 個
                              (105M),其餘 75 個已刪 — 見 research/repos/README.md
scripts/                   ← 6 支 pipeline 腳本
skill-reviewer/            ← D5 產出的 skill
docs/superpowers/          ← P3(掛入 ASP G5)的 spec / plan / 驗證 / SDD ledger
seeds/seed_repos.json      ← 2026-08-16 驗證的種子清單
```
