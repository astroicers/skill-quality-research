# skill-quality-research

分析 97 個各星數階層 Agent Skills repo 的特徵梯度 → 推導證據導向的分級式品質 rubric →
封裝為可執行的 `skill-reviewer` skill。

**專案已完成**(Phase 0–6,三道 HITL gate 皆 approved)。所有產出仍是 **proposal**,供人工審查。

---

## 一句話結論

**在此樣本與時點,skill 的星數關聯的是「可安裝／可發現／可信任」的打包面,不是內容工藝。**
5 條可量測的差異化特徵全是 packaging/marketing 面;寫作工藝(觸發設計/風格/scope)量化上全落 noise。
因此 `skill-reviewer` 的核心價值在 **LLM 質化判讀**,自動化 lint 只能當 packaging 過濾器與安全門檻。

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
| `aggregate_stats.py` | 4 | — | tier 梯度、三分類、去混淆三道工序 |

### 測試

每支腳本自帶 `--selftest`(純函式與分類器斷言,零網路)。
`aggregate_stats.py --selftest` 用 40 個合成 repo 的固定夾具,驗證 differentiator /
hygiene / noise / marketing-suspect 是否被正確分類。
`lint_skill.py --selftest` 另含 **drift-guard**:硬編權重與 `references/rubric.yaml` 不一致即 fail。

---

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

## 統計限制(必讀)

- n=54(rubric 樣本),**不跑迴歸、不宣稱顯著**;differentiator 的 ρ(log★) 僅 0.19–0.32(弱)
- 所有 differentiator 對 `fork_star_ratio` 幾乎全負 → 差異化項**未被 fork 行為背書**
- hygiene 門檻多數來自官方規範三角驗證,非本樣本 prevalence(樣本以合規 SKILL.md 篩選)
- 已知偏斜:T0 領域偏 design-ui;C3 世代 n=3 過薄

## 目錄

```
research/BRIEF.md          ← spec(唯一權威)
research/                  ← 所有 phase 產出(disk-based handoff)
research/qualitative_notes/← 54 份質化筆記
research/repos/            ← untrusted clone(gitignored,~2.8G;clone_repos.py 可重建)
scripts/                   ← 6 支 pipeline 腳本
skill-reviewer/            ← D5 產出的 skill
docs/superpowers/          ← P3(掛入 ASP G5)的 spec / plan / 驗證 / SDD ledger
seeds/seed_repos.json      ← 2026-08-16 驗證的種子清單
```
