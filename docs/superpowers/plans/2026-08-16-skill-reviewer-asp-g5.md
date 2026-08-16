# skill-reviewer 掛入 ASP Pipeline G5 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 讓 ASP 的 G5 HARDEN gate 在變更觸及 SKILL.md 時自動跑 skill-reviewer——hygiene error 擋 gate,安全紅旗與 craft 判讀降 YELLOW_FLAG 交人複核。

**Architecture:** 不新增腳本、不新增 profile。在 `~/.claude/asp/profiles/pipeline.md` 的 `evaluate_G5` pseudocode 加一段條件子句(貼合既有 `qa_agent.independent_verify()` + `EXECUTE("make lint")` 的混用形狀),並在 `~/.claude/asp/config/rule-registry.yaml` 登記兩條規則。skill-reviewer 以 symlink 全域安裝。

**Tech Stack:** Markdown pseudocode(ASP profile 慣例)、扁平 YAML(rule-registry,awk/grep 可解析不依賴 yq)、Python 3 stdlib(既有 lint_skill.py)、POSIX symlink。

**Spec:** `docs/superpowers/specs/2026-08-16-skill-reviewer-asp-g5-design.md`

## Global Constraints

- **授權範圍嚴格限三項**:`~/.claude/asp/profiles/pipeline.md`、`~/.claude/asp/config/rule-registry.yaml`、建立 symlink。不得動其他 ASP 檔案(spec §10)。
- **rule-registry.yaml 文法**:扁平兩~五行一組,awk/grep 可解析,**不依賴 yq**(檔頭第 7 行明訂)。
- **改動全域框架前備份**:兩個 ASP 檔在首次修改前各存一份 `.bak`,任何 task 失敗即可還原。
- **不擋 gate 的錯誤處理**:skill-reviewer 缺席/執行失敗/JSON 非法 → YELLOW_FLAG,絕不 GATE_FAIL(spec §5)。
- **symlink 路徑**:`~/.claude/skills/skill-reviewer` → `/home/ubuntu/skill-quality-research/skill-reviewer`。
- 本 plan 修改的是使用者全域框架,**每個 task 的 commit 只 commit 本 repo 的檔案**(ASP 檔不在任何 git repo 內,以 `.bak` + 驗證指令代替版本控制)。

---

### Task 1: 全域安裝 skill-reviewer(symlink)

**Files:**
- Create: `~/.claude/skills/skill-reviewer`(symlink → `/home/ubuntu/skill-quality-research/skill-reviewer`)
- Test: 手動驗證指令(無測試框架,ASP 層以指令驗證)

**Interfaces:**
- Consumes: 本 repo 既有的 `skill-quality-research/skill-reviewer/`(SKILL.md、scripts/lint_skill.py、references/、evals/)
- Produces: 全域路徑 `~/.claude/skills/skill-reviewer/scripts/lint_skill.py` 可執行——Task 2 的 pseudocode 引用此路徑

- [ ] **Step 1: 確認目標不存在(避免覆蓋既有檔案)**

```bash
command ls -la /home/ubuntu/.claude/skills/skill-reviewer 2>&1 | head -3
```

Expected: `No such file or directory`。若已存在且非 symlink,**停止並回報**——不得覆蓋使用者既有檔案。

- [ ] **Step 2: 建立 symlink**

```bash
command ln -s /home/ubuntu/skill-quality-research/skill-reviewer /home/ubuntu/.claude/skills/skill-reviewer
```

- [ ] **Step 3: 驗證 symlink 指向正確且 lint 可透過全域路徑執行**

```bash
command readlink /home/ubuntu/.claude/skills/skill-reviewer
python3 /home/ubuntu/.claude/skills/skill-reviewer/scripts/lint_skill.py --selftest
```

Expected: readlink 印出 `/home/ubuntu/skill-quality-research/skill-reviewer`;selftest 印出 `[selftest] lint_skill: all assertions passed ✔`

- [ ] **Step 4: 驗證斷鏈情境的降級行為(spec §5 過渡期安全)**

```bash
python3 /home/ubuntu/.claude/skills/skill-reviewer/scripts/lint_skill.py /nonexistent-repo-xyz 2>&1; echo "exit=$?"
```

Expected: 印出 usage 訊息、`exit=2`(非 0)。這證明呼叫端能以非零 exit code 偵測失敗並降級為 YELLOW_FLAG,而非誤判為「檢查通過」。

- [ ] **Step 5: 記錄安裝結果到本 repo**

```bash
cd /home/ubuntu/skill-quality-research
command printf '%s\n' "# P3 安裝紀錄" "" "- 2026-08-16 skill-reviewer 全域安裝(symlink)" "  \`~/.claude/skills/skill-reviewer\` → \`~/skill-quality-research/skill-reviewer\`" "- 驗證:全域路徑 selftest 通過;缺席情境 exit=2 可被偵測" > docs/superpowers/P3-install-log.md
git add docs/superpowers/P3-install-log.md
git commit -m "P3 Task 1: skill-reviewer 全域 symlink 安裝 + 驗證紀錄"
```

---

### Task 2: pipeline.md 的 evaluate_G5 加入 skill 子句

**Files:**
- Modify: `/home/ubuntu/.claude/asp/profiles/pipeline.md`(插入點:第 323 行後、第 325 行 `IF issues:` 前)
- Create: `/home/ubuntu/.claude/asp/profiles/pipeline.md.bak`(修改前備份)
- Test: 手動驗證(pseudocode 無執行環境,以結構檢查代替)

**Interfaces:**
- Consumes: Task 1 建立的 `~/.claude/skills/skill-reviewer/scripts/lint_skill.py`;其 `--json` 輸出的欄位 `hygiene[]`(含 `id`/`severity`/`pass`/`detail`)、`security[]`(含 `id`/`flag`/`confidence`)、`tier_benchmark_packaging`、`gap_list`
- Produces: `evaluate_G5` 內的 skill 子句——Task 3 的 rule-registry 兩條規則對應此子句的兩個判定點(hygiene→gate-log、craft→manual)

- [ ] **Step 1: 備份原檔並記錄 checksum**

```bash
command cp /home/ubuntu/.claude/asp/profiles/pipeline.md /home/ubuntu/.claude/asp/profiles/pipeline.md.bak
command sha256sum /home/ubuntu/.claude/asp/profiles/pipeline.md
```

記下 checksum,Step 5 用來確認只改了預期範圍。

- [ ] **Step 2: 確認插入點內容未偏移**

```bash
command sed -n '321,326p' /home/ubuntu/.claude/asp/profiles/pipeline.md
```

Expected 完全等於:
```
    ELSE:
      IF NOT spec.rollback_plan.tested:
        checks.append("⚠️ Rollback Plan 未經測試（建議但不強制）")

  IF issues:
    RETURN GATE_FAIL(issues)
```

若不符,**停止並回報**——檔案已被他處修改,插入點需重新定位。

- [ ] **Step 3: 插入 skill 子句**

用 Edit 工具,將這段(第 323–325 行區間):

```
        checks.append("⚠️ Rollback Plan 未經測試（建議但不強制）")

  IF issues:
```

替換為:

```
        checks.append("⚠️ Rollback Plan 未經測試（建議但不強制）")

  // P3: skill-reviewer（僅當變更觸及 SKILL.md；skill-quality-research）
  IF artifacts.changed_files MATCHES "**/SKILL.md":
    lint = EXECUTE("python3 ~/.claude/skills/skill-reviewer/scripts/lint_skill.py {repo_root} --json")

    IF lint.exit_code != 0 OR NOT is_valid_json(lint.stdout):
      YELLOW_FLAG("skill-reviewer 未安裝或執行失敗，跳過 skill 檢查（不擋 gate）")
    ELSE:
      // 擋 gate：只有 hygiene error 級（確定性判定，無假陽性疑慮）
      FOR h IN lint.hygiene WHERE h.severity == "error" AND h.pass == false:
        issues.append("Skill hygiene 未過：{h.id} {h.detail}")

      // 不擋：安全紅旗有已知假陽性（S-001 誤中正當文件），降 YELLOW_FLAG 交人複核
      FOR s IN lint.security WHERE s.confidence == "low-static-needs-llm":
        YELLOW_FLAG("Skill 安全紅旗待複核：{s.id}/{s.flag}")

      // craft：比照 qa_agent，由 LLM 層判讀；判斷不是事實，不擋 gate
      skill_verdict = skill_reviewer.review(artifacts.changed_skills)
      IF skill_verdict.craft == "needs-revision":
        YELLOW_FLAG("Skill craft 待修：{skill_verdict.gap_list}")

      checks.append("Skill packaging 剖面：{lint.tier_benchmark_packaging}（僅 packaging 面，非總評）")

  IF issues:
```

- [ ] **Step 4: 驗證插入正確且結構完整**

```bash
command grep -n "P3: skill-reviewer" -A 3 /home/ubuntu/.claude/asp/profiles/pipeline.md
command grep -c "FUNCTION evaluate_G" /home/ubuntu/.claude/asp/profiles/pipeline.md
```

Expected: 第一個指令印出插入的子句起始(行號約 325);第二個仍印出 `6`(G1–G6 六個函式都在,未破壞結構)。

- [ ] **Step 5: 驗證只動了 evaluate_G5 範圍**

```bash
command diff /home/ubuntu/.claude/asp/profiles/pipeline.md.bak /home/ubuntu/.claude/asp/profiles/pipeline.md | command head -30
```

Expected: 只有新增行(`>` 開頭),無刪除行(`<` 開頭),且全部落在 G5 區段。若見到刪除行,執行 `command cp /home/ubuntu/.claude/asp/profiles/pipeline.md.bak /home/ubuntu/.claude/asp/profiles/pipeline.md` 還原後回報。

- [ ] **Step 6: Commit(本 repo 的 plan 進度)**

```bash
cd /home/ubuntu/skill-quality-research
command printf '%s\n' "" "- 2026-08-16 Task 2: pipeline.md evaluate_G5 加入 skill 子句(備份 pipeline.md.bak)" >> docs/superpowers/P3-install-log.md
git add docs/superpowers/P3-install-log.md
git commit -m "P3 Task 2: ASP pipeline.md evaluate_G5 加入 skill-reviewer 子句"
```

---

### Task 3: rule-registry.yaml 登記兩條規則

**Files:**
- Modify: `/home/ubuntu/.claude/asp/config/rule-registry.yaml`(插入點:第 76 行 `GATE-G6` 區塊後、第 78 行註解前)
- Create: `/home/ubuntu/.claude/asp/config/rule-registry.yaml.bak`
- Test: 以 grep 驗證可解析性(檔頭第 7 行明訂「awk/grep 可解析,不依賴 yq」)

**Interfaces:**
- Consumes: Task 2 建立的 G5 skill 子句(兩個判定點)
- Produces: `GATE-G5-SKILL-HYGIENE`(observed_by: gate-log)與 `GATE-G5-SKILL-CRAFT`(observed_by: manual)兩個 rule_id——供 `rule-stats.sh` 統計與 `tests/test_rule_registry.sh` 防漂移

- [ ] **Step 1: 備份並確認插入點**

```bash
command cp /home/ubuntu/.claude/asp/config/rule-registry.yaml /home/ubuntu/.claude/asp/config/rule-registry.yaml.bak
command sed -n '72,78p' /home/ubuntu/.claude/asp/config/rule-registry.yaml
```

Expected 完全等於:
```
  - id: GATE-G6
    enabled_since: "2026-06-11"   # v5 起 gate-log 全面記錄（F-9 累積期保護）
    desc: "Ship Gate"
    source: "asp-gate.md"
    observed_by: gate-log

  # ── 靜態 deny patterns（denied-commands.json 逐條；方案 A：不可觀測）──
```

若不符,**停止並回報**。

- [ ] **Step 2: 插入兩條規則**

用 Edit 工具,將:

```
    desc: "Ship Gate"
    source: "asp-gate.md"
    observed_by: gate-log

  # ── 靜態 deny patterns
```

替換為:

```
    desc: "Ship Gate"
    source: "asp-gate.md"
    observed_by: gate-log

  # ── G5 skill 品質檢查（P3：skill-quality-research，見 pipeline.md evaluate_G5）──
  - id: GATE-G5-SKILL-HYGIENE
    enabled_since: "2026-08-16"
    desc: "Skill hygiene 門檻（H-001 合規 SKILL.md 等 error 級；擋 gate）"
    source: "skill-reviewer/references/rubric-manual-dimensions.yaml"
    observed_by: gate-log
  - id: GATE-G5-SKILL-CRAFT
    enabled_since: "2026-08-16"
    desc: "Skill craft 質化判讀（LLM 層，YELLOW_FLAG 不擋 gate）"
    source: "skill-reviewer/SKILL.md"
    observed_by: manual

  # ── 靜態 deny patterns
```

- [ ] **Step 3: 驗證 grep 可解析(檔案自身的文法要求)**

```bash
command grep -A 4 "id: GATE-G5-SKILL-HYGIENE" /home/ubuntu/.claude/asp/config/rule-registry.yaml
command grep -c "^  - id: " /home/ubuntu/.claude/asp/config/rule-registry.yaml
```

Expected: 第一個印出完整五行(id/enabled_since/desc/source/observed_by);第二個的數字比備份檔多 2。

- [ ] **Step 4: 驗證 observed_by 取值在合法詞彙內**

```bash
command grep "observed_by:" /home/ubuntu/.claude/asp/config/rule-registry.yaml | command grep -v "session-audit\|gate-log\|manual\|none" || echo "✓ 全部 observed_by 皆為合法詞彙"
```

Expected: `✓ 全部 observed_by 皆為合法詞彙`

- [ ] **Step 5: 驗證只新增未刪除**

```bash
command diff /home/ubuntu/.claude/asp/config/rule-registry.yaml.bak /home/ubuntu/.claude/asp/config/rule-registry.yaml
```

Expected: 只有 `>` 開頭的新增行。若有 `<` 刪除行,執行 `command cp /home/ubuntu/.claude/asp/config/rule-registry.yaml.bak /home/ubuntu/.claude/asp/config/rule-registry.yaml` 還原後回報。

- [ ] **Step 6: Commit**

```bash
cd /home/ubuntu/skill-quality-research
command printf '%s\n' "- 2026-08-16 Task 3: rule-registry.yaml 登記 GATE-G5-SKILL-HYGIENE / -CRAFT" >> docs/superpowers/P3-install-log.md
git add docs/superpowers/P3-install-log.md
git commit -m "P3 Task 3: rule-registry 登記兩條 G5 skill 規則"
```

---

### Task 4: 用 evals 驗證擋/不擋分界

**Files:**
- Create: `docs/superpowers/P3-verification.md`(驗證結果紀錄)
- Test: 用既有 `skill-reviewer/evals/evals.json` 的 5 個案例 + 既有 clone

**Interfaces:**
- Consumes: Task 1 的全域 lint、Task 2 的擋/不擋規則(hygiene error 擋、security low-static 不擋)
- Produces: 驗證證據——確認 spec §6 的預期行為與實際 lint 輸出一致

- [ ] **Step 1: 驗證「hygiene error 應擋」的案例**

```bash
python3 /home/ubuntu/.claude/skills/skill-reviewer/scripts/lint_skill.py \
  /home/ubuntu/skill-quality-research/research/repos/24kchengYe__human-skill-tree --json \
  | python3 -c "import json,sys; d=json.load(sys.stdin); e=[h for h in d['hygiene'] if h['severity']=='error' and h['pass'] is False]; print('擋 gate:', bool(e), e)"
```

Expected: `擋 gate: True [{'id': 'H-001', ...}]`(68 個 SKILL.md 全無 frontmatter)

- [ ] **Step 2: 驗證「安全假陽性不應擋」的案例**

```bash
python3 /home/ubuntu/.claude/skills/skill-reviewer/scripts/lint_skill.py \
  /home/ubuntu/skill-quality-research/research/repos/anthropics__skills --json \
  | python3 -c "import json,sys; d=json.load(sys.stdin); e=[h for h in d['hygiene'] if h['severity']=='error' and h['pass'] is False]; s=[x['id'] for x in d['security']]; print('擋 gate:', bool(e), '| YELLOW_FLAG:', s)"
```

Expected: `擋 gate: False | YELLOW_FLAG: ['S-001', ...]`——官方 repo 不被假陽性擋下,只發 flag。

- [ ] **Step 3: 驗證「craft 佳但 packaging 低」不被擋**

```bash
python3 /home/ubuntu/.claude/skills/skill-reviewer/scripts/lint_skill.py \
  /home/ubuntu/skill-quality-research/research/repos/ayghri__i-have-adhd --json \
  | python3 -c "import json,sys; d=json.load(sys.stdin); e=[h for h in d['hygiene'] if h['severity']=='error' and h['pass'] is False]; print('擋 gate:', bool(e), '| packaging:', d['packaging_score'], '/', d['packaging_max'])"
```

Expected: `擋 gate: False | packaging: 7 / 14`——packaging 低不擋 gate。

- [ ] **Step 4: 驗證「未觸及 SKILL.md 時零影響」(回歸保護)**

這是 pseudocode 層的條件判斷,以人工核對代替執行:讀 Task 2 插入的子句,確認整段包在
`IF artifacts.changed_files MATCHES "**/SKILL.md":` 之內。

```bash
command sed -n '/P3: skill-reviewer/,/^  IF issues:/p' /home/ubuntu/.claude/asp/profiles/pipeline.md | command head -5
```

Expected: 第 2 行即為 `IF artifacts.changed_files MATCHES "**/SKILL.md":`,確認無任何邏輯落在條件之外。

- [ ] **Step 5: 記錄驗證結果**

把 Step 1–4 的實際輸出寫入 `docs/superpowers/P3-verification.md`,格式:

```markdown
# P3 驗證結果(2026-08-16)

| 案例 | 預期 | 實際 | 判定 |
|------|------|------|------|
| 24kchengYe/human-skill-tree | hygiene error 擋 | (貼實際輸出) | ✅/❌ |
| anthropics/skills | 假陽性不擋、只 flag | (貼實際輸出) | ✅/❌ |
| ayghri/i-have-adhd | packaging 低不擋 | (貼實際輸出) | ✅/❌ |
| 未觸及 SKILL.md | 整段跳過 | (貼 sed 輸出) | ✅/❌ |
```

任一項為 ❌ 即停止並回報,不繼續。

- [ ] **Step 6: Commit**

```bash
cd /home/ubuntu/skill-quality-research
git add docs/superpowers/P3-verification.md docs/superpowers/P3-install-log.md
git commit -m "P3 Task 4: evals 驗證擋/不擋分界(4 案例全通過)"
```

---

### Task 5: 更新專案文件並收尾

**Files:**
- Modify: `CLAUDE.md`(目前狀態段)
- Modify: `research/BRIEF.md`(§3 Phase 6 的 P3 展望標記為已實作)
- Test: 無(文件變更)

**Interfaces:**
- Consumes: Task 1–4 的完成狀態
- Produces: 專案文件與實際狀態一致

- [ ] **Step 1: 更新 CLAUDE.md 目前狀態**

用 Edit 工具在 CLAUDE.md 的「目前狀態」段末尾加入:

```markdown
- **P3 ✅ 完成(2026-08-16)**:skill-reviewer 已掛入 ASP Pipeline G5——
  `~/.claude/asp/profiles/pipeline.md` 的 `evaluate_G5` 加 skill 子句(hygiene error 擋、
  安全紅旗與 craft 降 YELLOW_FLAG),`rule-registry.yaml` 登記兩條規則;
  skill-reviewer 以 symlink 全域安裝。spec/plan/驗證見 `docs/superpowers/`
```

- [ ] **Step 2: 更新 BRIEF.md 的 P3 展望**

用 Edit 工具,將 BRIEF.md §3 Phase 6 的這行:

```
- P3 展望(本階段不做):將 skill-reviewer 掛入 ASP 治理層,作為 Auditor pattern 的一個檢查器。
```

替換為:

```
- P3 展望(原標「本階段不做」;**經人工授權於 2026-08-16 實作完成**):skill-reviewer 已掛入
  ASP 治理層 G5 HARDEN gate 作為檢查器。設計見 `docs/superpowers/specs/2026-08-16-skill-reviewer-asp-g5-design.md`。
```

- [ ] **Step 3: 驗證兩份文件已更新**

```bash
cd /home/ubuntu/skill-quality-research
command grep -c "P3 ✅ 完成" CLAUDE.md
command grep -c "經人工授權於 2026-08-16 實作完成" research/BRIEF.md
```

Expected: 兩個指令都印出 `1`

- [ ] **Step 4: 全 selftest 回歸(確認 P3 未破壞既有產物)**

```bash
cd /home/ubuntu/skill-quality-research
python3 scripts/collect_repos.py --selftest && \
python3 scripts/extract_features.py --selftest && \
python3 scripts/aggregate_stats.py --selftest >/dev/null && \
python3 skill-reviewer/scripts/lint_skill.py --selftest && echo "✓ 全 4 支 selftest 綠"
```

Expected: `✓ 全 4 支 selftest 綠`

- [ ] **Step 5: Commit**

```bash
cd /home/ubuntu/skill-quality-research
git add CLAUDE.md research/BRIEF.md
git commit -m "P3 Task 5: 專案文件同步(CLAUDE.md 狀態 + BRIEF P3 標記完成)"
```

- [ ] **Step 6: 列出變更等待人工確認後才 push(ASP 鐵則)**

```bash
cd /home/ubuntu/skill-quality-research
git log origin/claude/claude-md-phase-0-31t3nk..HEAD --oneline
git status --short
```

**停止並向使用者報告**:列出上述變更、ASP 兩檔的改動摘要與 `.bak` 位置,等待人工確認後才 `git push`。不得自行 push。

---

## 附錄:還原程序(任一 task 失敗時)

```bash
# 還原 ASP 兩檔
command cp /home/ubuntu/.claude/asp/profiles/pipeline.md.bak /home/ubuntu/.claude/asp/profiles/pipeline.md
command cp /home/ubuntu/.claude/asp/config/rule-registry.yaml.bak /home/ubuntu/.claude/asp/config/rule-registry.yaml
# 移除 symlink（只移除連結，不影響 repo 內容）
command rm /home/ubuntu/.claude/skills/skill-reviewer
# 驗證還原
command diff /home/ubuntu/.claude/asp/profiles/pipeline.md.bak /home/ubuntu/.claude/asp/profiles/pipeline.md && echo "✓ pipeline.md 已還原"
```
