# self-audit round 2 — 擴大回測 18 個自家 skill(2026-08-17)

- 對象:`~/.claude/skills/` 全部 18 個未審 skill(round 1 已審 4 個,合計 22)
- 方法:`lint_skill.py` 全量 + 3 個平行 agent 做 craft 層(L-001~004)質化審查
- 目的:**累積 rubric 誤判樣本**——這是 round 1 §4 第 4 點所指「craft 是主判」的後續校準

---

## 1. lint 層結果(18/18)

| 指標 | 結果 |
|------|------|
| hygiene | **18/18 全 pass**(H-001 合規 SKILL.md 皆有) |
| packaging | 16 個 0/14、2 個 5/14(andrej-karpathy-perspective、huashu-nuwa) |
| knowledge_only 豁免 | 14 個觸發(H-004 判 N/A) |
| security flag | **僅 1 個**:`anysearch` 的 S-003 `cred_in_argv`(confidence: medium) |

packaging 全低再次印證 round 1 的結論(內部 skill 天然無 marketplace/一行安裝),**不重複記為新發現**。

## 2. ⭐ S-003 命中的完整經過(rubric 對、我錯)

`anysearch` 是 22 個自家 skill 中**唯一**觸發安全紅旗者,且是 `confidence: medium`——
正是我在 code-review C1 修正中「從被靜默丟棄救回來」的那一條。

**我的初判錯誤**:看到 README 有 `export ANYSEARCH_API_KEY=` / `.env` 就假設 regex 誤把環境變數
指派判成 argv,直接下結論「false positive」。

**查證推翻我自己**:
1. 用 6 個樣態實測 `REDFLAG_CRED_ARGV`——環境變數形式(`export X=`/`set X=`/`X=abc`)**全部正確不命中**,
   只有 `--api-key $KEY` / `--token $T` 這類真 argv 命中。regex 沒問題。
2. grep 找出真正的命中源:`anysearch_cli.ps1:502` 等處**實作了 `--api_key` 旗標**,
   且 `README.md:126` 明列優先序 **`--api_key` CLI flag > `.env` > 環境變數**——
   最高優先序就是最危險的那條路徑(憑證留在 shell history 與 process list)。
3. 獨立 agent 覆核同一結論,並補充緩解脈絡:實際範例指令都沒示範用 `--api_key`,
   使用引導只推薦 `.env`/環境變數,故 **`confidence: medium` 是恰當判定**(路徑存在但非預設)。

**這一則的價值**:
- **C1 修正被真實案例證明有效**——修正前這條會被靜默丟棄,22 個 skill 唯一的安全訊號會完全消失。
- **我犯了與 rubric 設計初衷相反的錯**:rubric 明訂安全紅旗要「LLM 複核」而非直接採信或直接推翻,
  我卻在沒查 regex 實際命中什麼的情況下就推翻它。**審查者的偷懶比 regex 的粗糙更危險。**

## 3. ⭐⭐ 六個 RUBRIC-MISMATCH(本輪核心產出)

三個 agent 獨立審查,回報 6 個誤判風險。**它們收斂到同一根因**:
patterns.md 的高品質樣態表是從「流程型/規則集型」skill 歸納的,套到其他 skill 形狀會字面誤判。

| # | skill | 準則 | 誤判風險 | 根因 |
|---|-------|------|---------|------|
| M1 | `grill-me`(11 行) | L-002 | 機械套用「解釋 why/Bad-Good/override」會判 poor | 它是**互動協定**不是規則集,沒有規則需要被解釋。扣分等於**獎勵灌水**發明不需要的 why 散文 |
| M2 | `zoom-out`(單句) | L-002 | 同上 | **canned-phrase 型**:本體就是一句觸發語,無內容可教 |
| M3 | `ga-methodology`(~25 觸發片語) | L-001 | 機械套「>20 變體 = 關鍵字轟炸」會判 poor | 每個片語對應**不同子意圖、不同回應**,是 turbo 式逐字枚舉而非同義詞灌水。**domain-lookup 型** skill 片語數天然多 |
| M4 | `improve-codebase-architecture` | L-002 | 缺 prose Bad/Good pair 可能被低估 | 它用**精確術語表 + 可證偽啟發式**(deletion test)達成同等清晰度。`ga-methodology` 也用表格+pseudocode 代替 prose 對照 |
| M5 | `asp`、`setup-matt-pocock-skills` | L-001 / L-003 | dispatcher 型 scope 天然廣;安裝腳本型無 Use when/dated snapshot | patterns.md **其實已有例外條款**(dispatcher 路由、`disable-model-invocation` 手動觸發),問題是**審查者是否記得查** |
| M6 | 全部 18 個 | L-004 | 18/18 皆無 anti-hallucination → 恐被讀成 18 個缺陷 | 純流程/方法論 skill **沒有會過時的外部事實**可宣稱。H-004 有 `exemption` 欄位,**L-004 沒有** |

## 4. rubric 修訂建議(round 2 產出,待裁決)

1. **L-004 補 exemption 條款**(對應 M6,最明確):比照 H-004 的寫法加
   `exemption: "skill 未宣稱任何外部/時效性事實(純流程、方法論、風格型)時判 N/A 而非缺項"`。
   證據:18/18 全缺席,若無此條款,任何內部 skill 集都會被系統性誤判。
2. **L-002 承認「可證偽啟發式/結構化表格」為 Bad/Good 的等價替代**(對應 M4)。
   現行 pass_criteria 只認「具體反例對照」,會低估用術語精確性或 deletion test 達成同等效果的寫法。
3. **L-002 補「skill 形狀」前置判斷**(對應 M1/M2):對 canned-phrase 型與互動協定型 skill,
   L-002 判 N/A;**明文寫出「不得因簡潔扣分」**——H-003 已有「長度非絕對」的 caveat,
   craft 維度需要同一條。
4. **L-001 區分「同義詞灌水」vs「多子意圖各自映射」**(對應 M3)。
   前者是 SEO 轟炸(browser-act 反例),後者是 domain-lookup skill 的正當設計。
5. **skill-reviewer SKILL.md 加一步「先判 skill 形狀再套準則」**(對應 M5——rubric 條款其實已存在,
   缺的是流程強制)。建議分類:process/rule 型、canned-phrase 型、domain-lookup 型、
   dispatcher/集合型、一次性安裝型。

## 5. rubric 未捕捉到的高品質模式(正面發現)

1. **跨 skill 的 reference 複用(DRY across skills)**:`improve-codebase-architecture` 以相對路徑
   引用 `../grill-with-docs/CONTEXT-FORMAT.md` 而非複製;`diagnose` 把逾越範圍的架構發現
   顯式交棒給 `/improve-codebase-architecture`。這是「個人 skill 庫像一套系統而非雜物堆」的
   成熟訊號,但 L-003 的證據庫只記錄了**集合型 repo 內**的 dispatcher,沒涵蓋
   **獨立 skill 之間**的交叉引用。建議列為 L-003 子樣態。
2. **anti-hallucination 三件套可模板化**:huashu-nuwa 生態系(母 skill + 16 子 skill)系統性內建
   「調研截止日 + 時效盲區顯性處理 + 誠實邊界」,是本次最一致的 L-004 高分群集——
   證明它不是個案巧合而是可複製機制。
3. **集合型應以子 skill 抽樣評分**:只讀 huashu-nuwa 的入口 SKILL.md 會低估其 craft,
   真正的品質訊號在 16 份子 SKILL.md 的一致模板。這其實正是 G2-Q4 `phase3b_sample` 的設計初衷,
   但 skill-reviewer 的 SKILL.md 未明文要求對集合型 skill 這樣做。

## 6. craft verdict 總表(18 個,全部 approved)

| 批次 | skill(t/s/sc/ah) |
|------|------------------|
| A | tdd g/g/g/n · diagnose g/g/g/n · grill-me g/m*/g/n · grill-with-docs g/g/g/n · write-a-skill m/m/g/n · improve-codebase-architecture g/g*/g/n |
| B | to-issues g/m/g/n · to-prd g/g/g/n · triage g/g/g/n · zoom-out g/m*/g/n · caveman g/g/g/n · ga-methodology g*/g*/g/n |
| C | asp g/g/m*/na · huashu-nuwa g/g/m/g · andrej-karpathy-perspective g/g/g/g · ai-stack-writeup m/m/g/m · anysearch p/m/g/m · setup-matt-pocock-skills g/g/g/na* |

`*` = 該項有 RUBRIC-MISMATCH,實際品質高於字面評分。

**兩個真實可改進處**(非 rubric 誤判):
- `anysearch`:trigger 過寬(5 大類幾乎涵蓋所有搜尋任務)+ S-003 argv 憑證路徑。
  本批唯一同時踩中 hygiene 安全與 craft 弱點者。
- `write-a-skill`:**它教別人寫 skill,自己卻沒示範負向觸發、override 節、anti-hallucination**——
  它的 Review Checklist 對這三者全部沉默。這是最值得優先修的一個(教材本身該是範例)。

## 7. 結論

- **22/22 自家 skill hygiene 全過、craft 全 approved**,rubric 沒有誤殺任何一個。
- 但 **6 個 RUBRIC-MISMATCH 顯示:rubric 的字面套用會誤判非流程型 skill**。
  這不是 rubric 錯,是它缺少「先判 skill 形狀」這一步——而這正是**只有擴大樣本才會浮現的問題**
  (round 1 的 4 個 skill 全是流程/知識型,形狀太一致,看不出來)。
- **最有價值的一則是我自己的誤判**(§2):我在沒查證的情況下推翻了 rubric 的安全告警,
  而它其實是對的。這印證了 skill-reviewer SKILL.md 的設計——安全紅旗要 LLM **複核**,
  而複核的意思是「去查」,不是「憑印象推翻」。
