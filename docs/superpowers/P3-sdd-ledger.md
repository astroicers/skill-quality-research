# SDD ledger — plan: docs/superpowers/plans/2026-08-16-skill-reviewer-asp-g5.md

Spec: docs/superpowers/specs/2026-08-16-skill-reviewer-asp-g5-design.md (已讀,binding authority)
Branch: claude/claude-md-phase-0-31t3nk @ 2866f02
Workspace: .superpowers/sdd/2026-08-16-skill-reviewer-asp-g5/

## Pre-flight 衝突掃描

### 跨任務:共用檔案 / interface 配對

| Task 對 | 共用 | 產出 vs 消費 | 發現 |
|---------|------|-------------|------|
| T1 → T2 | `~/.claude/skills/skill-reviewer/scripts/lint_skill.py` | T1 產出全域可執行路徑;T2 pseudocode 引用 `~/.claude/skills/skill-reviewer/scripts/lint_skill.py` | ✅ 路徑字面一致 |
| T1 → T4 | 同上 | T4 Step 1-3 用全域路徑跑 lint | ✅ 一致 |
| T2 → T3 | 概念耦合(非檔案) | T2 產出兩個判定點;T3 登記 GATE-G5-SKILL-HYGIENE(gate-log)/-CRAFT(manual) | ✅ 對應正確:hygiene 走 gate-log、craft 走 manual |
| T2 → T4 | `pipeline.md` | T2 寫入子句;T4 Step 4 用 sed 讀回驗證條件包覆 | ✅ T4 的 sed pattern `/P3: skill-reviewer/,/^  IF issues:/p` 與 T2 插入的註解字串 `// P3: skill-reviewer` 相符 |
| T2 → T5 | 無檔案共用 | T5 只改本 repo 文件 | ✅ 無衝突 |
| T1..T4 → T5 | `docs/superpowers/P3-install-log.md` | T1 建立(`>`覆寫)、T2/T3 追加(`>>`)、T4 commit | ✅ 順序正確:T1 先建再由後續追加 |
| T3 → T4 | 無 | T4 未驗證 rule-registry | ⚠️ 見下方 finding-1 |

### 各任務:自身一致性

| Task | 自身檢查 | 發現 |
|------|---------|------|
| T1 | 建立 symlink → 驗證 readlink/selftest → 驗證斷鏈 exit code → commit log 檔 | ✅ 自洽 |
| T2 | 備份 → 驗插入點 → Edit → 驗結構 → diff 確認只增不刪 → commit | ✅ 自洽;插入點 L321-326 已於 plan 撰寫時實測 |
| T3 | 備份 → 驗插入點 → Edit → grep 可解析 → observed_by 詞彙 → diff → commit | ✅ 自洽;插入點 L72-78 已實測 |
| T4 | 4 個驗證案例,各有明確 expected | ✅ 自洽;三個 repo 路徑均存在於 research/repos/ |
| T5 | 改 2 文件 → grep 驗證 → 全 selftest → commit → 停下等人工 push | ✅ 自洽;符合 ASP 鐵則 |

### Findings 與裁決

**finding-1(輕微,不阻斷)**:T4 驗證涵蓋 T1/T2 的行為,但**未驗證 T3 的 rule-registry 登記**。
plan 的 T3 Step 3-5 自身已含 grep 可解析性與 observed_by 詞彙驗證,涵蓋充分。
**Ruling**:不加 task。T3 的內建驗證已足夠,額外的 T4 案例只是重複 — 代價:若 rule-registry
被其他程序改壞,要到下次 `rule-stats.sh` 執行才會發現(可接受,非本 plan 引入的風險)。

**finding-2(需注意)**:本 plan 修改的 `~/.claude/asp/` **不在任何 git repo 內**,
因此 `review-package` 產生的 diff 只會涵蓋本 repo 的檔案(log/文件),看不到 ASP 兩檔的實際改動。
**Ruling**:task reviewer 的 review package 需額外附上 ASP 檔的 `diff .bak` 輸出作為證據,
由我(controller)在 dispatch 時以檔案形式提供 — 代價:若我漏附,reviewer 會對 T2/T3 的核心
改動盲審(我會在 T2/T3 的 review dispatch 明確處理)。

**finding-3**:plan Global Constraints 要求「每個 task 的 commit 只 commit 本 repo 的檔案」,
與 SDD 的「commits <base7>..<head7>」記錄慣例相容 — ✅ 無衝突。

掃描結論:無阻斷性衝突,3 條 finding 已裁決。開始執行 Task 1。

## 執行紀錄
Task 1: complete (commits 2866f02..0f363e2, review clean)
Task 1: minor (deferred): brief Step 4 寫 /nonexistent-repo-xyz、實測用 /nonexistent-xyz — 行為相同,僅字面差異
Task 1: minor (deferred): report 日期 header 2026-08-17 vs log/commit 2026-08-16 — 純表面
Task 2: BASE=0f363e2
Task 2: DONE_WITH_CONCERNS — implementer 回報 `command diff` 仍被 rtk 攔截、輸出誤似含刪除行;已用 /usr/bin/diff 交叉驗證為純新增
Task 2: Ruling: 採納此環境發現 — ASP 檔驗證一律改用 /usr/bin/diff 絕對路徑。我已獨立複驗 324a325,346、0 刪除行、6 個 gate 函式完整。代價:若 rtk 行為再變,驗證指令需再調整
Task 2: complete (commits 0f363e2..5063d25, review clean; ASP diff 324a325,346 純新增)
Task 2: minor (deferred): checks.append 字串多「,非總評」— brief 已含,無害澄清
Task 3: BASE=5063d25
Task 3: Ruling: implementer 發現既有 rule 用 observed_by: pretooluse-ship-gate(不在我 spec 記錄的 4 詞彙內)。已複驗其存在於 .bak L208 = 既有狀態,非本 task 引入。裁決:我的 spec 詞彙清單不完整(漏記 rule-registry 實際允許的擴充值),非檔案有誤;本 task 新增的兩條用 gate-log/manual 皆合法,不需改。代價:若未來有人以我 spec 的 4 詞彙做校驗會誤報既有規則
Task 3: complete (commits 5063d25..e450fbc, review clean; ASP diff 77a78,89 純新增, id 46→48)
Task 3: minor (deferred): desc 全形/半形標點與 spec §3.4 原文不完全逐字(源自 brief,語意相同)
Task 4: BASE=e450fbc
Task 4: BLOCKED — case 3 實際 9/14 vs 預期 7/14(implementer 誠實停止,未提交假通過的 commit message)
Task 4: Ruling: 根因非 repo drift(implementer 推測),而是**我的 code-review F1 修正**擴寬 BEFORE_AFTER_RE 對齊校準版正則,使 ayghri README 的 '## Before/## After' 正確被偵測(+2)。7/14 是 F1 修正前的陳舊值,存在於 evals.json / self-audit.md / plan 預期值三處。裁決:9/14 才是正確值,修正三處陳舊基準而非改 code。代價:若日後再收窄該正則,這些值需再更新
Task 4: fix round 1/5 (1 addressed, 0 open — case3 基準 7/14→9/14; commits e450fbc..697ff7f)
Task 4: fix round 1 re-review: ADDRESSED,根因裁決經 re-reviewer 獨立覆核同意,無新破壞
Task 4: complete (commits e450fbc..253721a, review clean, 4/4 案例 ✅)
Task 5: BASE=253721a
Task 5: complete (commits 253721a..eae555f, review clean)
FINAL REVIEW: 2 Critical / 3 Important / 5 Minor
Final: Ruling C1 — 確認為真(已複驗 lint_skill.py:163-171)。cred_in_argv(confidence=medium,憑證外洩,最高訊號)被 == 'low-static-needs-llm' 過濾器靜默丟棄;S-101 無 confidence 鍵。修:改為排除 polarity==positive 後全部 YELLOW_FLAG。代價:flag 量略增(可接受,總比漏掉憑證檢查好)
Final: Ruling C2 — 確認為真且嚴重(已複驗:AI-SOP-Protocol/.asp 為 git 來源,installed 5.0.0 vs repo 5.1.0,install.sh:253 rm -rf profiles config)。我的 spec §2 查了 pipeline.md 內容卻沒查其來源,是實質盲點。修:P3-install-log 明記升級會覆蓋 + 提供重新套用指令。**不自行改 AI-SOP-Protocol repo**(超出使用者授權的三項範圍,需另行請示)
Final: Ruling I1 — 確認為真。H-001 是 repo 級(compliant_count>=1),新增一個壞 SKILL.md 不會被擋。修:記入 spec §7 已知限制(改判準需重跑 Phase 3/4 校準,超出本 plan 範圍)
Final: Ruling I2 — 確認為真(rule-stats.sh:67 只合成 GATE-G1..G6)。GATE-G5-SKILL-HYGIENE 的 observed_by: gate-log 恆零命中,90 天後變假訊號。修:改為 manual
Final: Ruling I3 — 確認為真。spec §6 列 5 案例,plan Task 4 只做 4 個,漏掉 memU(唯一驗證『真安全問題刻意不擋』)。修:補跑此案例
FINAL fix wave: commit 1241827 (5/5 findings ADDRESSED, re-review 確認無新破壞)
SDD 完成:5 tasks + 1 final fix wave,全部 review clean
