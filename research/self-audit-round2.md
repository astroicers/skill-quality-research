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

## 4. rubric 修訂(round 2 產出,**5 條已全部落地 2026-08-17**)

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

---

## 8. 修訂落地紀錄(2026-08-17)

5 條建議全數實作,分兩批:

**批 1 — `rubric-manual-dimensions.yaml` 新增 6 個例外欄位**(對應 M1~M4、M6):

| 準則 | 新欄位 | 內容 |
|------|--------|------|
| L-001 | `disambiguation` | 「關鍵字轟炸」判準改為**語意是否重複**而非片語數量;附可操作判別法(抽 3 個片語看是否觸發同一段內容) |
| L-002 | `equivalent_forms` | 承認**可證偽啟發式**(deletion test)、**結構化表格/門檻表**、**精確術語表**為 Bad/Good 的等價替代 |
| L-002 | `exemption` | canned-phrase 型與互動協定型判 N/A;明文「**不得因簡潔扣分**——那等於獎勵灌水」 |
| L-003 | `sub_pattern_cross_skill` | 獨立 skill 間的交叉引用(相對路徑複用 reference、顯式交棒)亦計分 |
| L-003 | `collection_sampling` | 集合型須以子 skill 抽樣評分,不可只讀入口檔 |
| L-004 | `exemption` | 未宣稱外部/時效性事實者判 N/A;附證據(18/18 缺席)與判準 |

**批 2 — `skill-reviewer/SKILL.md` 流程強化**(對應 M5,並吸收 §2 的實錯教訓):

1. **新增「步驟 3:先判 skill 形狀」為套準則前的必做步驟**,含六型分類表
   (process/rule、canned-phrase、互動協定、domain-lookup、dispatcher/集合、一次性安裝)
   與各自的準則調整。明寫關鍵洞察:**誤判多半不是條款缺失,而是審查者沒去查例外欄位**。
   原步驟 3/4 順延為 4/5。
2. **步驟 5 加「複核 = 去查,不是憑印象推翻」**,把 §2 我自己的誤判寫成教訓與三步標準動作
   (實測 regex 命中什麼 → grep 找真正命中源 → 兩者做完才下判),
   並明訂「`confidence: medium` 的紅旗推翻它需要**最強**的證據,不是最弱的」。

**驗證**:YAML 解析通過、6 個欄位落在正確準則、SKILL.md 步驟編號 1–5 連續、lint selftest 綠
(含 drift-guard)。另派獨立 agent 用**修訂後**的 rubric 重審當初暴露誤判的 4 個 skill
(grill-me / zoom-out / ga-methodology / improve-codebase-architecture),驗證例外欄位確實接住誤判
——結果見 §9。

## 9. 修訂效果驗證(獨立 agent,用修訂後的 rubric 重審)

派一個未參與前述審查的 agent,嚴格照 skill-reviewer 新流程(含步驟 3 判形狀)重審當初
暴露誤判的 4 個 skill。**結論:例外欄位確實接住了誤判。**

| # | skill / 準則 | 無例外欄位會判 | 有例外欄位改判 | 依據 |
|---|-------------|--------------|--------------|------|
| 1 | ga-methodology / L-001 | poor(聯想 browser-act 20+ 轟炸) | **good** | `disambiguation` 的語意重複測試 |
| 2 | ga-methodology / L-002 | mixed/poor(無 prose Bad/Good) | **good** | `equivalent_forms` 認結構化門檻表 |
| 3 | grill-me / L-002 | poor(11 行、無 why、無 override) | **N/A** | `exemption` 互動協定型 |
| 4 | zoom-out / L-002 | poor(全文一句注入語) | **N/A** | `exemption` canned-phrase 型 |
| 5 | **全 4 個 / L-004** | 4/4 皆判缺項 | **4/4 N/A** | `exemption` 無外部事實宣稱 |

4 個 skill 最終 L-001/L-003 全 good、L-002 兩 good 兩 N/A、L-004 全 N/A——與 §6 的人工判定一致,
且**不再需要 `*` 標記「實際品質高於字面評分」**:字面評分本身已經正確。

### ⚠️ 驗證輪發現的殘餘缺口(已當場補上)

驗證者誠實回報:**`domain-lookup` 型缺 L-003 的 scope 例外**——shape 表只給了 dispatcher/集合型
「不因 scope 廣扣分」,ga-methodology 涵蓋 7+ 子題、字面上接近 planning-with-files 反例,
它判 good 是靠自行外推而非明文條款。

**已補 `domain_lookup_scope` 欄位**:判準改為「子題是否同屬一個 domain expertise」而非數量,
附可操作判別法(「這些子題會不會在同一次任務中被同一個人用到?」)與正反例對照
(ga-methodology 同一 domain 的不同切面 vs planning-with-files 不同 job 被塞進同一 skill)。

另一則觀察(未修,記錄):`improve-codebase-architecture` 依賴 `../grill-with-docs/*.md`,
單獨安裝會缺檔。`sub_pattern_cross_skill` 讓它在 L-003 加分(scope 治理成熟),
但「單獨抽出會壞掉」屬 packaging 完整性、非 craft——**兩者不衝突但 rubric 未明說分工**。
留待後續:若要修,應在 packaging/lint 層加「相對路徑跨 skill 依賴」檢查,而非改 craft 準則。

## 10. round 2 總結

- 22/22 自家 skill 全數通過(hygiene + craft),rubric 無誤殺
- 收集到 **6 條 RUBRIC-MISMATCH + 1 條驗證輪殘餘缺口**,全部已落地修正(7 個新例外欄位 + 流程步驟)
- 修訂經**獨立 agent 用修訂後 rubric 重審驗證**,誤判全數消除
- 最有價值的一則仍是 §2:**我自己在沒查證的情況下推翻了正確的安全告警**——
  這條教訓已寫進 skill-reviewer SKILL.md 步驟 5,成為流程的一部分
