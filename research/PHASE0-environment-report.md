# Phase 0 — 環境初始化報告 + Phase 1 阻斷分析

- 執行時間:2026-08-16(UTC)
- 執行環境:Claude Code on the web(remote container),**非本機 CLI**
- spec:`research/BRIEF.md` v1.2.1
- 結論:**Phase 0 全項通過;Phase 1 在本環境無法依 spec 執行,需人工裁決**

---

## 1. Phase 0 驗收(BRIEF §3 Phase 0)

| 檢查項 | 結果 | 證據 |
|--------|------|------|
| `git` | ✅ | 2.43.0 |
| `python3` | ✅ | 3.11.15 |
| `jq` | ✅ | jq-1.7 |
| `gh` CLI | ❌ 未安裝 | 但腳本走 `urllib`,不依賴 `gh`(僅 `get_token()` 有 `gh auth token` fallback) |
| 認證 | ✅ | `GITHUB_TOKEN` 存在;`/rate_limit` 回 core 15000/hr、search 30/min |
| 目錄 `research/` `research/repos/` `scripts/` | ✅ 已建立 | — |
| BRIEF 快照 | ✅ 已存在 | `research/BRIEF.md` v1.2.1 |
| `collect_repos.py --selftest` | ✅ 全綠 | all assertions passed |
| `extract_features.py --selftest` | ✅ 全綠 | all assertions passed |
| `aggregate_stats.py --selftest` | ✅ 全綠 | 分類器在 40 個合成 repo 夾具上全部判對 |

補充(Phase 2 預檢,BRIEF 未要求但先行排除風險):`git ls-remote` 對任意第三方公開 repo 可用。

---

## 2. 環境能力邊界(實測)

remote container 的出站流量走 agent proxy,GitHub 存取被**依 session repo 範圍**限縮。

| 路徑 | 狀態 | 備註 |
|------|------|------|
| `git clone` / `ls-remote` 任意公開 repo | ✅ 匿名可讀 | proxy 直接服務匿名 git read |
| `raw.githubusercontent.com` | ✅ 200 | 任意公開 repo 檔案可取 |
| `api.github.com/rate_limit`、`/user` | ✅ 200 | 帳號層級端點 |
| `api.github.com/repos/{任意 repo}` | ❌ 403 | `GitHub access to this repository is not enabled for this session` |
| `api.github.com/repos/astroicers/skill-quality-research` | ❌ 403 | `An org admin must connect the Claude GitHub App` |
| `api.github.com/search/*` | ❌ 403 | `sessions are bound to their configured repositories` |
| `api.github.com/users/*` | ❌ 403 | 同上(非 repo-scoped 路徑) |
| `github.com` HTML、`codeload.github.com` | ❌ 403 | — |

兩項關鍵確認:

1. **與憑證無關,是路徑政策**:去掉 `Authorization` header 後回應完全相同的 403。
   → 使用者自備 PAT **也無法**解除,proxy 在路徑層攔截。
2. **`add_repo` 不解決此問題**:對 `anthropics/skills` 呼叫 `add_repo(access:"read")` 回覆
   「read access is already available… **GitHub API tools do not cover unattached repositories**」。
   僅 `access:"push"` 會附掛憑證——對 40 個第三方 repo 掛 push 憑證不正當,且跨 owner 多半遭拒。

---

## 3. Phase 1 阻斷分析

### 3.1 無法執行的部分

BRIEF §3 Phase 1 的**發現(discovery)機制全滅**:六組 `topic:` / `in:name,description` 查詢與
T1/T0 的 `stars:1000..9999` / `stars:100..999` 區間抽樣,全部依賴 `/search/repositories`。

連帶後果:**T0 層(100–1k 星)完全無樣本**——種子清單最低是 `obra/superpowers-marketplace` 1,209 星。
而 BRIEF §4 把 hygiene 門檻定義為「缺什麼會掉出 1k 級」,該定義**只能由 T0 層對照得出**。
沒有 T0,hygiene 與 differentiator 的三分類失去下界。

### 3.2 BRIEF §7 Feature Schema 逐欄可得性

| 欄位 | 本環境 | 說明 |
|------|--------|------|
| `stars` / `forks` / `fork_star_ratio` | ❌ | 僅 32 個種子有 2026-08-16 快照值 |
| `created_at` / `pushed_at` / `launch_cohort` / `days_since_creation` / `stars_per_month` | ❌ | 可用 full clone 首次 commit 日期做**近似**(非 spec 定義) |
| `topics` / `repo_size_kb` | ❌ | 無替代路徑 |
| `license` | ⚠️ | 可從 clone 內 LICENSE 檔判讀(非 SPDX API 值) |
| `author_followers` / `prior_fame_proxy` / `author_fame_tier` | ❌ | `/users/*` 全封,**無任何替代路徑** |
| `contributor_count` | ⚠️ | full clone `git shortlog -sn` 可得 committer 數(≠ GitHub contributors) |
| `nonauthor_pr_count` | ❌ | `/search/issues` 全封 |
| `has_version_tags` | ✅ | `git ls-remote --tags` 可用 |
| **skill 結構全段**(`skill_md_count`、frontmatter、description 系列、`dir_*`) | ✅ | 純靜態解析 |
| **打包與安裝全段**(`has_plugin_json`、`has_marketplace_json`、`has_install_sh`、`install_oneliner_in_readme`、`multi_harness_claims`) | ✅ | 純靜態解析 |
| **工程品質**(`has_ci`、`ci_validates_skills`、`has_tests_or_evals`、`has_changelog`) | ✅ | 純靜態解析 |
| **README 行銷面全段** | ✅ | 純靜態解析 |

### 3.3 對 BRIEF v1.2「去混淆三道工序」的衝擊(§4)

| 工序 | 需要的資料 | 本環境 |
|------|-----------|--------|
| 1. 素人復現(F0 素人達 T2+) | `author_fame_tier` ← followers / prior_fame | ❌ **無法執行** |
| 2. 雙結果變數(engagement 梯度) | `fork_star_ratio`、`contributor_count`、`nonauthor_pr_count` | ❌ **無法執行** |
| 3. 機制陳述 | LLM 判讀,無資料依賴 | ✅ 可執行 |

三道工序是 v1.2 為攔截「偽差異化因子」(BRIEF §9-9)而設的強制關卡,**缺一即降級**。
本環境只剩第 3 道 → 任何 differentiator 的 `evidence_strength` 上限只能是 `weak`,
且 `grassroots_replicated` 與 `marketing-suspect` 兩個 rubric 欄位無從填寫。

### 3.4 判定

Phase 1 若在本環境以 `--offline` 種子模式執行,產出的 `repos.json` 會是:
32 repos、tier 僅 T1–T3(T0 = 0)、`launch_cohort` 全 null、`author_fame_tier` 全 null、
純度樣本 0 個、engagement 欄位全 null。

此即 repo 內既有冒煙快照 `research/G1-summary.md` 的狀態,BRIEF §3 的 G1 驗收清單中
「純度標籤 domain / fame / cohort 標注正確」與「四層抽樣分布合理」**兩項確定無法通過**。

依 Iron Rule 2(AI proposes, human reviews)與 Iron Rule 1(不確定就停下來問),
**停在此處等待人工裁決**,不自行降級 spec 後續跑。

---

## 4. 已完成的 G1 前置工作(不依賴上述裁決)

### 4.1 種子存活驗證(32/32)

以 `git ls-remote --heads` 逐一驗證,**32 個種子 repo 全部存活**,無 404、無失聯。

### 4.2 `obra/superpowers` 追址結案 ✅

BRIEF §5 標注「原址 API 已 404,Phase 1 需追查現址」。實測結果:

- `git ls-remote https://github.com/obra/superpowers.git` → **成功**,回傳大量 branch refs
  (含 `codex/bump-superpowers-evals-*`、`agentic-end-to-end-testing` 等活躍分支)
- `raw.githubusercontent.com/obra/superpowers/main/README.md` → **200,12,137 bytes**,
  內容為 Superpowers 本體(`# Superpowers … a complete software development methodology
  for your coding agents, built on top of a set of composable skills`)
- **無改名重導**,`obra/superpowers` 即現址

→ **G1 檢查清單「superpowers 現址已確認」該項可勾選。**
原 404 應為製定 BRIEF 時未認證 API 撞 60 req/hr 上限所致(BRIEF §9-4 已記錄該次撞牆),
而非 repo 消失。BRIEF §5 的 `~116,000*` 星數註記仍待有 API 的環境覆核。

---

## 5. 可選路徑(待人工裁決)

| 選項 | 做法 | 代價 |
|------|------|------|
| **A. 本機跑 Phase 1** | 在有 `gh auth` 的本機 CLI 跑 `collect_repos.py`,把 `research/repos.json` commit 進 repo,再回 remote session 續跑 Phase 2+ | 需切換環境一次;**spec 完整性 100% 保留**(建議) |
| **B. 種子降級模式** | `--offline` 產 32-repo `repos.json`,接受 T0 缺層、去混淆工序 1&2 失效 | rubric 所有 differentiator 封頂 `weak`;hygiene 門檻無下界可推 |
| **C. git 側補值** | Phase 2 改 full clone,以首次 commit 日期近似 `created_at`、`git shortlog` 近似 contributor | 補得到 cohort 近似值;`stars`/`followers`/PR 數仍無解,且偏離 spec 定義 |
| **D. 自備 PAT** | — | **已實測排除**:403 與憑證無關,proxy 在路徑層攔截 |

無論選哪條,§4 的種子存活驗證與 superpowers 結案都已成立,不需重跑。
