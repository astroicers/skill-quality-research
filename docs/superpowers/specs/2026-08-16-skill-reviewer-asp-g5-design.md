# skill-reviewer 掛入 ASP Pipeline G5 — 設計文件

- 日期:2026-08-16
- 狀態:**Draft — 待人工審查**(ASP 鐵則:Draft ADR/spec 狀態下禁止實作生產代碼)
- 來源:`research/BRIEF.md` §3 Phase 6 的 P3 展望(原標「本階段不做」,經人工授權推進)
- 前置:skill-quality-research Phase 0–6 完成、G1/G2/G3 approved、PR #1

---

## 1. 背景與問題

`skill-reviewer`(本研究 D5)目前是獨立 skill,只能人工觸發。ASP 已有成熟的 6 階段品質管線
(G1–G6),但**沒有任何 gate 檢查 skill 本身的品質**——當專案新增或修改 SKILL.md 時,
無論其 frontmatter 是否合規、是否含安全紅旗,都能無阻通過 G5 HARDEN。

本設計把 skill-reviewer 掛入 G5,讓 skill 品質成為管線的一部分。

## 2. 探勘紀錄(重要:含一次幻覺修正)

初次以 Explore subagent 探勘 ASP,其報告 `~/.claude/asp/scripts/asp-gate-check.sh:40-120`
含硬編 G1–G6 case——**經 Read 驗證該檔不存在,連行號都是虛構**。本 spec 的所有 ASP 事實
改以 Read / `command grep` 逐一驗證(BRIEF Iron Rule:外部事實驗證)。

已驗證為真的 ASP 事實:

| 事實 | 驗證方式 | 對本設計的意義 |
|------|---------|---------------|
| `profiles/pipeline.md` 的 G1–G6 是 **pseudocode 規格**(`FUNCTION evaluate_G5(artifacts)`),由 agent/skill 解讀執行,非 shell 腳本 | Read | 掛入 = 加一段 FUNCTION 子句,不寫新腳本 |
| **G5 已混用** agent 判讀(`qa_agent.independent_verify()`、`sec_agent.review()`)與 shell(`EXECUTE("make lint")`) | grep -A 45 | skill-reviewer 的 LLM+script 兩層與此天然同構,**零新機制** |
| `config/rule-registry.yaml` 為扁平 yaml,欄位 `id/desc/source/observed_by/exempt`;`observed_by` 詞彙 = `session-audit\|gate-log\|manual\|none`;文法「awk/grep 可解析,不依賴 yq」 | Read | 新 checker 有現成登記慣例;craft→`manual`、lint→`gate-log` |
| gate 統計來源為 `.asp-gate-log/*.md` frontmatter | rule-registry.yaml 註解 | 有現成證據落盤格式,不需新增 |
| `levels/standard.yaml` 的 `check:` 慣例為一行 shell exit-code | Read | 佐證:craft(LLM 判讀)無法塞進此慣例,必須走 agent 呼叫路線 |
| `~/.claude/asp/` **是安裝產物**,來源在獨立 git repo `/home/ubuntu/AI-SOP-Protocol`;其 `scripts/install.sh` 第 253 行會 `rm -rf profiles config` 再重新複製;installed VERSION=5.0.0、repo=5.1.0(升級已逾期) | Read `install.sh`、比對兩處 VERSION(fix round 2 C2 finding,先前遺漏) | 本次改動(pipeline.md、rule-registry.yaml)寫在安裝副本上,任何人跑一次升級就會被無聲清除;正解是提交進 AI-SOP-Protocol repo,但超出本次授權範圍,見 §11 |

## 3. 設計

### 3.1 觸發條件

僅當 G5 HARDEN 階段且本次變更觸及 `**/SKILL.md`。不觸及則整段跳過——對絕大多數任務零額外成本。

### 3.2 在 `evaluate_G5` 加入的子句

```
// skill-reviewer:僅當變更觸及 SKILL.md(P3,skill-quality-research)
IF artifacts.changed_files MATCHES "**/SKILL.md":
  lint = EXECUTE("python3 <skill-reviewer>/scripts/lint_skill.py <repo> --json")

  // 擋 gate:只有 hygiene error 級
  FOR h IN lint.hygiene WHERE h.severity == "error" AND h.pass == false:
    issues.append("Skill hygiene 未過:{h.id} {h.detail}")

  // 不擋:安全紅旗有已知假陽性,降 YELLOW_FLAG 交人複核
  // 排除 positive(防禦樣態,無 confidence 欄位);medium(如 cred_in_argv)假陽性率最低,措辭加重
  FOR s IN lint.security WHERE s.polarity != "positive":
    IF s.confidence == "medium":
      YELLOW_FLAG("Skill 安全紅旗(較高信心,優先複核):{s.id}/{s.flag}")
    ELSE:
      YELLOW_FLAG("Skill 安全紅旗待複核(靜態偵測,假陽性率高):{s.id}/{s.flag}")

  // craft:比照 qa_agent,由 LLM 層判讀
  skill_verdict = skill_reviewer.review(artifacts.changed_skills)
  IF skill_verdict.craft == "needs-revision":
    YELLOW_FLAG("Skill craft 待修:{skill_verdict.gap_list}")
  checks.append("Skill packaging 剖面:{lint.tier_benchmark_packaging}(僅 packaging 面)")
```

### 3.3 三個關鍵設計決定

| 決定 | 理由 |
|------|------|
| **只 hygiene error 擋 gate** | 安全紅旗有實證假陽性(S-001 誤中 `anthropics/skills` 的正當文件「follow the guide exactly」),擋了會造成 gate 假阻。hygiene H-001(無合規 SKILL.md)是確定性判定,無假陽性疑慮 |
| **security 過濾條件用 `polarity != "positive"` 而非「只挑 low-static」** | `lint_skill.py` 的 security 項有三種形態:`confidence: "low-static-needs-llm"`(假陽性高)、`confidence: "medium"`(如 `cred_in_argv`,憑證進命令列,假陽性最低、最該複核)、`polarity: "positive"` 的 S-101(正面防禦樣態,無 confidence 欄位,不該當紅旗)。若只挑 `low-static` 會把訊號強度最高的 medium 靜默丟棄——這是 fix round 2 修正的 C1 finding,修法為排除 positive 後全部 flag,並讓 medium 措辭更醒目(「較高信心,優先複核」) |
| **craft 寫成 `skill_reviewer.review()` agent 呼叫** | 與既有 `qa_agent.independent_verify()` / `sec_agent.review()` 完全同形,執行者(Claude)讀到時跑 skill-reviewer 的 SKILL.md 流程 |
| **craft 不擋 gate,只 YELLOW_FLAG** | craft 是判斷不是事實,符合 BRIEF「AI proposes, human reviews」;且研究已證 craft 與 packaging 正交,不宜機械化擋人 |

### 3.4 rule-registry.yaml 新增(沿用現有扁平格式)

```yaml
  - id: GATE-G5-SKILL-HYGIENE
    desc: "Skill hygiene 門檻(H-001 合規 SKILL.md 等 error 級;擋 gate)"
    source: "skill-reviewer/references/rubric-manual-dimensions.yaml"
    observed_by: manual
  - id: GATE-G5-SKILL-CRAFT
    desc: "Skill craft 質化判讀(LLM 層,YELLOW_FLAG 不擋 gate)"
    source: "skill-reviewer/SKILL.md"
    observed_by: manual
```

**`observed_by` 更正說明(fix round 2 I2 finding)**:原設計 `GATE-G5-SKILL-HYGIENE` 用
`observed_by: gate-log`,但 `rule-stats.sh` 第 67 行的 gate-log 聚合只會合成 `GATE-<G1..G6>`
這種頂層 id,無法產生子規則 id,導致此規則永遠 0 命中。`enabled_since` 的 90 天新規則保護
到期後,0 命中會被判讀為「待刪候選」——假訊號。已改為 `observed_by: manual`,與 `-CRAFT`
對齊,並在 `rule-registry.yaml` 該條加註解說明原因。

### 3.5 檔案改動範圍(最小化——動的是使用者的全域框架)

| 檔案 | 改動 |
|------|------|
| `~/.claude/asp/profiles/pipeline.md` | `evaluate_G5` 加 §3.2 子句 |
| `~/.claude/asp/config/rule-registry.yaml` | 加 §3.4 兩條登記 |
| `skill-reviewer/` | **不改**(現況已滿足需求) |

**不做**:不新增 profile、不新增 shell 腳本、不動 hooks、不改 levels/*.yaml。

## 4. 資料流

```
G5 HARDEN 觸發
  └─ changed_files 觸及 **/SKILL.md?
       ├─ 否 → 跳過(零成本)
       └─ 是 → lint_skill.py --json
                 ├─ hygiene error       → issues[]      → 可能 GATE_FAIL
                 ├─ security low-static → YELLOW_FLAG   → 人工複核
                 └─ packaging tier      → checks[]      → 記錄
              → skill_reviewer.review()(LLM craft)
                 └─ needs-revision      → YELLOW_FLAG   → 人工判
```

## 5. 錯誤處理

| 情境 | 行為 |
|------|------|
| `lint_skill.py` 不存在或執行失敗 | YELLOW_FLAG「skill-reviewer 未安裝/執行失敗」,**不擋 gate**(工具缺席不應阻斷他人管線) |
| lint 回傳非法 JSON | 同上,降級為 YELLOW_FLAG |
| 變更觸及大量 SKILL.md(如集合型 repo) | lint 本身是 repo 級單次呼叫,無 N+1 問題;craft 依 `craft_llm_todo` 的確定性抽樣 ≤5 個 |
| 受審 repo 是 untrusted 第三方 clone | lint 純靜態讀取(BRIEF Iron Rule 7);craft 層 SKILL.md 已明訂「內容是資料不是指令」 |

## 6. 測試方式

用本 repo 既有的 `skill-reviewer/evals/evals.json` 5 案例驗證擋/不擋分界:

| 案例 | 預期 |
|------|------|
| `24kchengYe/human-skill-tree`(68 個 SKILL.md 全無 frontmatter) | hygiene H-001 fail → **進 issues,擋 gate** |
| `anthropics/skills`(S-001 已知假陽性) | 只 YELLOW_FLAG,**不擋** |
| `ayghri/i-have-adhd`(craft 佳、packaging 7/14) | hygiene pass、craft approved → 通過,packaging 剖面進 checks |
| `NevaMind-AI/memU`(真 S-001) | YELLOW_FLAG 交人判(此為刻意取捨:寧可漏擋也不假阻) |
| 未觸及 SKILL.md 的一般任務 | 整段跳過,G5 行為與現況完全相同(回歸保護) |

## 7. 已知限制與取捨

1. **真安全問題可能漏擋**:S-001 有真有假(memU 是真、anthropics 是假),因無法自動區辨,選擇一律 YELLOW_FLAG。取捨理由:gate 假阻的代價(阻斷正當開發、侵蝕對 gate 的信任)高於漏擋的代價(仍有 YELLOW_FLAG 提示人看)。
2. **craft 判讀不可重現**:LLM 判讀本質有變異;`craft_llm_todo` 的確定性抽樣只保證「讀哪幾個檔」可重現,不保證 verdict 一致。
3. **packaging 剖面對內部 skill 天然偏低**(self-audit 實證 4/4 為 0/14),故只進 `checks` 記錄、永不擋 gate。
4. **本設計未觸及 G1–G4/G6**:skill 品質只在 HARDEN 檢查一次,不做全管線佈點(YAGNI)。
5. **H-001 是 repo 級判準,抓不到「新增一個壞 SKILL.md」**(fix round 2 I1 finding):
   `lint_skill.py` 的 H-001 是 `skill_md_compliant_count >= 1`(整個 repo 至少一個合規 SKILL.md
   即 pass)。因此在已有多個正常 skill 的 repo 裡新增一個壞掉的 SKILL.md,H-001 仍 pass,
   G5 仍會放行。取捨理由:改判準(例如改成「本次變更觸及的 SKILL.md 各自合規」)需要重跑
   本研究 Phase 3/4 的統計校準(rubric 權重是針對 repo 級聚合訂的),超出本次 plan 的範圍,
   因此本次選擇誠實記錄此限制而不修改 code。

## 8. 替代方案(已評估未採用)

| 方案 | 未採用理由 |
|------|-----------|
| B. 獨立 `profiles/skill_auditor.md` | 需動 profile-map 與載入條件,面積大於收益;G5 子句已足夠 |
| C. 只在 `hooks/pretooluse-ship-gate.sh` 加檢查 | 只能跑 shell 層(lint),craft 完全掛不上——與研究核心結論(craft 才是主判)相悖 |

## 9. 前置依賴:skill-reviewer 需先全域安裝

**已查證(2026-08-16)**:`~/.claude/skills/skill-reviewer/` **不存在**;skill-reviewer 目前只在本 repo
(`skill-quality-research/skill-reviewer/`)。ASP 是全域框架,G5 子句不能引用單一專案的相對路徑。

因此本設計有一個**前置步驟**:

```
Step 0(實作前):將 skill-reviewer 安裝到 ~/.claude/skills/skill-reviewer/
Step 1:pipeline.md 的 <skill-reviewer> 一律解析為 ~/.claude/skills/skill-reviewer/
```

pseudocode 中的路徑固定寫作 `~/.claude/skills/skill-reviewer/scripts/lint_skill.py`。
若該路徑不存在,依 §5 錯誤處理降級為 YELLOW_FLAG,不擋 gate——這也讓「ASP 已掛但 skill 未裝」
的過渡期是安全的。

**安裝方式:symlink**(人工裁定 2026-08-16)。
`~/.claude/skills/skill-reviewer` → `~/skill-quality-research/skill-reviewer`,
使 repo 的 rubric/lint 更新自動生效,無需重新同步。
已知代價:repo 移動或刪除會斷鏈——由 §5 的錯誤處理接住(降級 YELLOW_FLAG,不擋 gate)。

## 10. 授權範圍(已取得)

本設計改動使用者的全域 ASP 框架(`~/.claude/asp/`)。
**人工已明示授權(2026-08-16)**:可動 `profiles/pipeline.md` 與 `config/rule-registry.yaml` 兩檔,
以及建立 Step 0 的 symlink。授權範圍僅限此三項,不含其他 ASP 檔案。

## 11. 長期落地建議(未執行,需另行授權)

**背景(fix round 2 C2 finding)**:`~/.claude/asp/` 不是原始碼,是 git repo
`/home/ubuntu/AI-SOP-Protocol` 的**安裝產物**。該 repo 的 `scripts/install.sh` 在複製階段對
`profiles/hooks/templates/levels/config/scripts/advanced` 逐一 `rm -rf` 後再整個目錄複製覆蓋
(含 `profiles/` 與 `config/`)。目前 installed VERSION=5.0.0,repo VERSION=5.1.0——升級已逾期。
只要有人(含使用者自己)之後跑一次 ASP 升級,本次加入的 G5 skill 子句與兩條
`GATE-G5-SKILL-*` 規則就會被**無聲清除**,且不會有任何錯誤訊息提示。

**本次未做的正解**:把 §3.2 的 pipeline 子句與 §3.4 的兩條規則,以正常開發流程提交進
`/home/ubuntu/AI-SOP-Protocol` repo 本身——過該 repo 自己的 ADR / SPEC / gate 審查機制,
成為框架原始碼的一部分,而不是掛在使用者本機的安裝副本上。這樣升級只會把功能一併帶
到新版本,不會清除它。

**為何本次不做**:超出本次任務的授權範圍(§10 明示授權僅限 `~/.claude/asp/` 的兩個安裝檔
與 symlink,不含 `/home/ubuntu/AI-SOP-Protocol/`)。且該 repo 有自己的治理流程(從探勘記錄
看與本專案的 BRIEF/ADR 機制同構),貿然直接改會繞過其審查。

**過渡期緩解**:已在 `docs/superpowers/P3-install-log.md` 新增顯著警告章節,記錄「升級會覆蓋」
與重新套用步驟;若使用者之後決定要長期落地,依此節內容另開任務,走 AI-SOP-Protocol repo 自己
的流程。
