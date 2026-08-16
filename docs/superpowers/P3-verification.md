# P3 驗證結果(2026-08-16,2026-08-17 fix round 1 更新)

驗證對象:Task 1(全域 symlink)、Task 2(`pipeline.md` `evaluate_G5` 的 skill 子句)、
Task 3(rule-registry 兩條規則)所建立的「擋 gate / 不擋 gate」分界。

> **Fix round 1 更正**:Step 3 原判定 ❌ 為誤判根因。經 controller 查證,packaging 9/14 才是
> 正確值——差異來自 code-review F1 修正擴寬了 `BEFORE_AFTER_RE`(對齊 `extract_features.py`
> 的校準版正則),使該 README 既有的 `## Before` / `## After` 章節正確被偵測到,故 +2 分。
> 原引用的 7/14 是 F1 修正前的陳舊基準。`skill-reviewer/evals/evals.json` 與 plan 的
> Task 4 Step 3 Expected 已由 controller 同步更正為 9/14。判定關鍵始終是 `擋 gate: False`,
> 現已對照更正後的 expected 全部相符。詳見下方 Step 3 區塊與 `task-4-report.md` 的
> "Fix round 1" 章節。

## 結果總表

| 案例 | 預期 | 實際 | 判定 |
|------|------|------|------|
| 24kchengYe/human-skill-tree | hygiene error 擋 | `擋 gate: True [{'id': 'H-001', 'pass': False, 'detail': '合規 SKILL.md 數=0', 'severity': 'error'}]` | ✅ |
| anthropics/skills | 假陽性不擋、只 flag | `擋 gate: False \| YELLOW_FLAG: ['S-001', 'S-003']` | ✅ |
| ayghri/i-have-adhd | packaging 低不擋(更正後 expected:`擋 gate: False \| packaging: 9 / 14`) | `擋 gate: False \| packaging: 9 / 14` | ✅ |
| 未觸及 SKILL.md | 整段跳過 | 見下方 sed 輸出 | ✅ |

> 註:case 3 的 9/14 為 F1 修正後的正確值,原 7/14 為陳舊基準(F1 修正前);判定關鍵是
> `擋 gate: False`,此結論自始至終未變。

## 逐項證據

### Step 1 — hygiene error 應擋(24kchengYe/human-skill-tree)

指令:

```bash
python3 /home/ubuntu/.claude/skills/skill-reviewer/scripts/lint_skill.py \
  /home/ubuntu/skill-quality-research/research/repos/24kchengYe__human-skill-tree --json \
  | python3 -c "import json,sys; d=json.load(sys.stdin); e=[h for h in d['hygiene'] if h['severity']=='error' and h['pass'] is False]; print('擋 gate:', bool(e), e)"
```

實際輸出:

```
擋 gate: True [{'id': 'H-001', 'pass': False, 'detail': '合規 SKILL.md 數=0', 'severity': 'error'}]
```

與 brief 預期完全一致。判定:✅

### Step 2 — 安全假陽性不應擋(anthropics/skills)

指令:

```bash
python3 /home/ubuntu/.claude/skills/skill-reviewer/scripts/lint_skill.py \
  /home/ubuntu/skill-quality-research/research/repos/anthropics__skills --json \
  | python3 -c "import json,sys; d=json.load(sys.stdin); e=[h for h in d['hygiene'] if h['severity']=='error' and h['pass'] is False]; s=[x['id'] for x in d['security']]; print('擋 gate:', bool(e), '| YELLOW_FLAG:', s)"
```

實際輸出:

```
擋 gate: False | YELLOW_FLAG: ['S-001', 'S-003']
```

brief 預期為 `擋 gate: False | YELLOW_FLAG: ['S-001', ...]`(以 `...` 容許額外 flag)。實際除
`S-001` 外還多了 `S-003`,但兩者皆屬 `security` 清單、皆非 hygiene error,不影響「不擋 gate」的核心
判定。判定:✅

### Step 3 — craft 佳但 packaging 低不應擋(ayghri/i-have-adhd)

指令:

```bash
python3 /home/ubuntu/.claude/skills/skill-reviewer/scripts/lint_skill.py \
  /home/ubuntu/skill-quality-research/research/repos/ayghri__i-have-adhd --json \
  | python3 -c "import json,sys; d=json.load(sys.stdin); e=[h for h in d['hygiene'] if h['severity']=='error' and h['pass'] is False]; print('擋 gate:', bool(e), '| packaging:', d['packaging_score'], '/', d['packaging_max'])"
```

實際輸出:

```
擋 gate: False | packaging: 9 / 14
```

更正後 expected 輸出(controller 已同步更正 `evals.json` 與 plan 的 Task 4 Step 3):
`擋 gate: False | packaging: 9 / 14`。實際輸出與更正後 expected **完全一致**。

**根因(controller 裁決,已查證確認)**:差異並非上游 repo README 內容漂移,而是
**code-review F1 修正擴寬了 `BEFORE_AFTER_RE`**(對齊 `extract_features.py` 的校準版正則),
使該 README 既有的 `## Before` / `## After` 章節(第 37、45 行)正確被偵測到,
`readme_has_before_after` 由(F1 修正前的)未偵測狀態轉為 `true`,+2 分權重。查證方式:

- `skill-reviewer/scripts/lint_skill.py` 的 changelog 註記明確記載
  `F1 lint BEFORE_AFTER_RE 對齊 extract 校準版(帶回假陽性,記為限制)`。
- `skill-reviewer/evals/evals.json` 現已由 controller 更正為
  `"packaging_tier": "T1 剖面(9/14;缺一行安裝與 examples。註:code-review F1 修正擴寬
  BEFORE_AFTER_RE 對齊校準版後,README 的 '## Before/## After' 正確被偵測,由 7/14 更正為
  9/14)"`。
- gap_list 現只剩 `install_oneliner_in_readme`(3 分)、`dir_examples`(2 分)兩項未達標,
  缺分合計 5 分,14 − 5 = 9,與實際輸出自洽。

核心語意判定(packaging 偏低、craft 佳但不擋 gate)自始至終成立:9/14(64%)明顯低於滿分,
`擋 gate: False`。原 fix round 0 判定為 ❌ 是因逐字比對到「陳舊的 7/14 基準」而非「F1 修正後
的正確值 9/14」,現已更正。

判定:✅(對照更正後 expected 完全相符)

### Step 4 — 未觸及 SKILL.md 時零影響(回歸保護)

指令:

```bash
/usr/bin/sed -n '/P3: skill-reviewer/,/^  IF issues:/p' /home/ubuntu/.claude/asp/profiles/pipeline.md | /usr/bin/head -5
```

實際輸出:

```
  // P3: skill-reviewer(僅當變更觸及 SKILL.md;skill-quality-research)
  IF artifacts.changed_files MATCHES "**/SKILL.md":
    lint = EXECUTE("python3 ~/.claude/skills/skill-reviewer/scripts/lint_skill.py {repo_root} --json")

    IF lint.exit_code != 0 OR NOT is_valid_json(lint.stdout):
```

第 2 行即為 `IF artifacts.changed_files MATCHES "**/SKILL.md":`,與 brief 預期完全一致,確認
所有邏輯皆包在該條件之內。判定:✅

## 結論與後續建議(fix round 1 更新)

四案例(Step 1–4)**全部通過**。Step 3 原判定 ❌ 的根因已由 controller 查證並更正:非上游
repo 內容漂移,而是 code-review F1 修正擴寬 `BEFORE_AFTER_RE` 對齊 `extract_features.py`
校準版,使 README 既有的 Before/After 章節正確被偵測,9/14 才是 F1 修正後的正確值,
7/14 是 F1 修正前的陳舊基準。controller 已同步更正 `skill-reviewer/evals/evals.json`
與 plan 的 Task 4 Step 3 Expected。判定關鍵「packaging 低不擋 gate」(`擋 gate: False`)
自始至終成立,現四案例對照更正後 expected 全部 ✅。

依 task-4-brief 規範,本 task 判定由 BLOCKED 轉為 **通過**,執行 Step 6 commit(commit
message 依 fix round 1 指示更正為反映「4 案例通過;case 3 基準由 7/14 更正為 9/14」)。
