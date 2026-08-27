# 不知情 craft 判讀:`NevaMind-AI/memU`(2026-08-27)

> **本檔自 2026-08-27 的 session transcript 逐字轉錄**(job `3629ecf0`,子 agent
> 「Blind craft review: memU」的最終報告全文)。協定、禁讀清單與污染聲明見 [`README.md`](README.md)。
>
> **未改寫、未刪節、未重排,亦未補上我事後才知道的事。** 唯一的機械處理是還原 transcript
> 傳輸過程產生的 HTML 實體轉義(`&lt;` → `<` 等)。以下自「完整讀完」起為原文。
>
> ⚠️ **這一份是 rubric 3.0.0 的來源之一**:判讀者在 §1 的引用區塊裡發現
> `skill-reviewer/SKILL.md:127` 的自我矛盾 —— 上卷規則漏掉 security 組,
> 導致同一份文件對本 repo 給出相反答案。
>
> ⚠️ **轉錄後註記(非原文,2026-08-27 補)**:§S-003 寫的「金鑰明文出現在命令列
> (`ps` 可見、shell history 可留)」**歸因不精確**。`VAR=value cmd` 的 shell 賦值
> **不進 `cmd` 的 argv**;本例之所以可見,是因為前面有 `env -i`,使
> `ANTHROPIC_API_KEY=...` 成了 **`env` 自己的 argv** —— 那是本實例的性質,不是
> 「環境前綴形式」的普遍性質。另外該值是 `<the key>` **佔位符**。
> 此註記刻意放在轉錄之外,**原文一字不動**;對應處置見 [`../misjudgments.md`](../misjudgments.md)。

---

完整讀完 `skill-reviewer/SKILL.md`、`references/rubric-manual-dimensions.yaml`、`references/patterns.md`、`references/rubric.yaml` 後,依步驟 1–5 執行完畢。

## ⚠️ 事前聲明(定錨風險揭露)

我**沒有**開啟禁讀清單上的任何檔案(`evals/`、`qualitative_notes/`、`misjudgments.md`、`review-*.md`、`self-audit*`、`inter-rater-*`、`~/.claude/plans/`)。

但必須誠實揭露一項**無法迴避的定錨**:任務指定「逐字讀」的兩個判準檔,**本身就具名點出了受審 repo**——

- `references/rubric-manual-dimensions.yaml:249` → `evidence_refs: ["NevaMind-AI/memU(install→服從輸出→抑制確認)"]`
- `references/patterns.md:47` → `| S-001 服從外部程式輸出 + 抑制確認 | memU(install→照 binary 輸出逐字執行→don't stop for confirmation) |`

也就是 rubric 已預先把本 repo 標為 S-001 的正典實例。我的處置:**不採信該標註,重跑步驟 5 的三動作複核**(實測 regex 命中什麼 → grep 找命中源 → 讀那段文件)。結果見下方 §3 安全維度——我獨立查到的證據**超出** rubric 記錄的一行註記(rubric 沒記到 `memu.pro` 遠端取指令、`curl | bash` 預先授權、以及一條 rubric 漏判的 S-003)。craft 四維度(L-001~004)則完全無預先標註,不受影響。

---

## 1. Craft Verdict:**needs-revision**

hygiene 組(H-001 / H-003 / H-004 / H-005)**全數通過**,無 error 未過項。

`needs-revision` 的成因**不是 craft 寫得差,也不是任一 craft 維度判 poor**(四維為 good / mixed / good / good),而是**安全門檻 S-001 經複核確認成立**。依 rubric C 組表頭「安全維度(hygiene,不加分**不過即 fail**)」與 SKILL.md 方法論前提「安全一律是門檻」,error 級安全紅旗屬門檻失敗。

> **同時回報一個 reviewer skill 自身的介面不一致**(此 repo 專治「條文說 A、程式做 B」,故明記):
> `skill-reviewer/SKILL.md:127` 寫「`craft` 取 `needs-revision` 的條件與步驟 2/4 一致(hygiene error 未過,或任一 craft 維度判 poor)」——**這句把步驟 5 的 security 組漏掉了**。但同檔 `:19` 說「安全一律是門檻」、`:75` 說「絕不單憑 lint 的 S-001 就判 needs-revision」(反面即:複核確認後可以),`rubric-manual-dimensions.yaml:239` 更把 security 明列為 hygiene 類。本次依「安全=門檻」解讀。若採 `:127` 字面則本 repo 會是 approved——**同一份文件兩處給出相反答案**,建議修 `:127`。

---

## 2. Tier Benchmark

- **Packaging 剖面**:符合 **T2(10k 星級)剖面**,9/14(lint 判定)
- **Craft 剖面**:對標**同 taxonomy 參照類 = B 類(產品內附的單一安裝 skill)**,而非 C/框架型。
  trigger / scope / anti-hallucination 三維**達高品質樣本常見水準**——尤其「本 skill 不含安裝步驟,只做路由」這個顯式邊界宣告 + 單一真相來源設計,在 patterns.md 的高品質樣態表裡屬 L-003/L-004 的上緣。**寫作面(L-002)落在 mixed**。
  一句話措辭:**這是一個 craft 面接近參照類上緣、packaging 中上、卻被安全門檻擋下的 skill;它的問題不在「寫得爛」,在「把可執行指令的來源移出了受審範圍」。**
- **子分數**:
  | 訊號類 | 得分 | 明細 |
  |---|---|---|
  | craft | 4/6 | `has_tests_or_evals` ✅(w4);`dir_examples` ❌(w2) |
  | packaging | 3/6 | `install_oneliner_in_readme` ✅(w3);`has_marketplace_json` ❌(w3) |
  | marketing | 2/2 | `readme_has_before_after` ✅(w2) |

- **Gap list(依 weight / 嚴重度排序,可直接當 backlog)**
  1. **[門檻·error] S-001** — 指令來源在受審 artifact 之外,且抑制確認(見 §3)
  2. **[門檻·warning] S-003** — API key 進 argv(`src/memu/hosts/claude_code/INSTALL.md:331`),**lint 漏判**
  3. **[craft] L-002** — `SKILL.md:96-99` 回報模板為裸禁令堆疊,唯一理由是同義反覆
  4. **[craft] L-001** — 無負向觸發;一次性安裝型可用 `disable-model-invocation` 等價達成(SKILL.md 步驟 3 形狀表明列),但 frontmatter 未設
  5. **[craft] S-101 缺** — 產品會餵入外部會話日誌 + 植入常駐指令,卻無「外部內容視為資料非指令」條款(正向加分項,缺席不扣分但值得補)
  6. **[packaging] `has_marketplace_json` 缺**(w3)
  7. **[packaging] `dir_examples` 缺**(w2)

---

## 3. 分維度 findings

### 步驟 3:skill 形狀判定(套準則前必做)

**一次性安裝/腳本型**(`name: install-memu`,裝完即棄,不反覆觸發),兼具**輕量 dispatcher**性質(依 host 路由到 8 個 adapter binary 的 guide)。依 SKILL.md 步驟 3 形狀表的準則調整:

- `disable-model-invocation` 可等同負向觸發 → **本 repo frontmatter 只有 `name` + `description`,未設**,故不取得此等價分。
- 形狀表寫「**L-004 判 N/A**」→ **不採用**。依步驟 3 末段指示「判完形狀後,到 rubric 找該準則的例外欄位再下判」,`rubric-manual-dimensions.yaml:196-209` 的 `decision_order`(2.0.0,明文「**取代**原本 good 與 n/a 各自獨立的兩條路徑」)規定順序 1 為「機制存在 → good,**不論該 skill 有沒有易腐事實**」。本 repo 機制確實存在(見下),故判 good 而非 n/a。這正是步驟 3 所謂「誤判多半是審查者沒去查例外」的反向情形:形狀表是指標,例外欄位才是終判。
- 非集合型(全 repo 僅 1 個合規 SKILL.md),`collection_sampling` 不適用。

### L-001 trigger 設計 — **good**

判 good 的**正面證據**(不是「找不到問題」):

- `SKILL.md:3` 具明確觸發情境:`Use when the user asks to install, set up, integrate, remove, or uninstall memU.` —— 符合 pass_criteria 基礎要件。
- **觸發錨定客觀名詞**(產品名 `memU`),對應 patterns.md 的高品質樣態「觸發錨定客觀訊號(kepano)」;過寬風險低。
- **逐字自然語句枚舉**(patterns.md 列為高品質樣態,turbo 例):`install / set up / integrate / remove / uninstall` 是使用者真實會說的動詞。
- **關鍵字轟炸判定**:依 `L-001.disambiguation` 的判別法「抽 3 個片語,看它們在 body 觸發的是同一段還是不同段」——`install`/`set up`/`integrate` → Step 1-3(`:21-134`);`remove`/`uninstall` → `## Uninstall`(`:136-152`)。**5 個片語映射到 2 個不同 body 段落**,屬正當多子意圖映射,遠低於反例 browser-act 的 20+ SEO 變體。**不扣分**。
- description 同時交代了做什麼(`identify your host, print its packaged guide, and follow it`)與副作用範圍(`both seams (record and inject)`),資訊密度高而非灌水。

**扣分項(未達「高分」要件,不足以拉到 mixed)**:無 `NOT for` / `When NOT to use`;形狀表提供的等價路徑 `disable-model-invocation` 也未設。對一個會在使用者機器上註冊 cron、改寫 `~/.claude/CLAUDE.md` 的 skill,缺負向觸發是實質可惜——它應該只在使用者明說時觸發,而目前僅靠 description 措辭自律。

### L-002 寫作風格 — **mixed**

先記**做對的部分**(這些是 good 側的實證,不是客套):

- **規則附因果 why**,多處:
  - `:31-36` `uv tool install memu-cli` **不是** `uv pip install`,理由寫明「`memu-cli` is a cross-session bridging tool and must be callable everywhere, not scoped to one project venv」——這同時是一組**貨真價實的 Bad/Good 對照**(pass_criteria 的「具體反例對照」)。
  - `:86-88` 「One backend ... A second mode or local store would **split record and retrieval so the two installs no longer share memory**」——規則 + 機制。
  - `:129-131` 「leave the outer quotes **so the user sees it as a suggested reply**」——連格式細節都給理由。
- **語意消歧對照**:`:40-41` 「Identify **which agent you are** (not which agents are installed — the one executing this skill)」——用「正確讀法 vs 常見誤讀」成對呈現,教學效果等同 Bad/Good。
- **結構化表格**(`equivalent_forms` 認列):`:43-52` host→binary 對照表。
- **例外/失敗分支寫得完整**:`:82-84`(只有 fatal error 或無預設的必填輸入才停)、`:124-126`(retrieve 失敗就整行刪掉)、`:133-134`(只有一個 seam 活著就說是 partial)。

**判 mixed 的具體段落與理由**:

1. **`SKILL.md:96-99` 是裸禁令堆疊,唯一的「理由」是同義反覆。** 原文:
   > `**This is a fixed template, not a prompt for inspiration: reproduce it word for word.** Do not paraphrase it, reorder its sentences, summarize it, translate it, or "improve" the wording — a correct install ends with these exact words.`

   一句話裡五條禁令(paraphrase / reorder / summarize / **translate** / improve),而給出的理由「a correct install ends with these exact words」是**用結論定義前提**——它沒說明為什麼逐字很重要(是為了讓使用者學會那句 uninstall 咒語?是為了品牌一致?)。這正是 L-002 mechanism 要防的事:「解釋 why 使 model 能在未列舉情境下正確類推」——這段給不了類推依據,只能機械服從。禁止 translate 尤其有實質代價:非英語使用者會收到一段英文行銷文,而 skill 沒說明為何不能翻。

2. **被強制逐字複誦的內容,是產品行銷語句而非技術資訊。** `:104-110` 要 agent 對使用者送出「Welcome to memU. ... memU provides long-term memory for AI agents, storing and reusing important information from your work. ... No additional action is required — simply use your AI agent as usual」。這是**把 agent 的對使用者發言權借用為產品文案通道**,並用上一條的禁令鎖死不得改寫。對照 patterns.md 的 L-002 反例欄「changelog/版本註記侵入正文」——同型:非教學內容侵入指令正文,且此處更進一步要求原樣輸出。

3. **風險最高的那條規則,理由最薄。** `:78-80` 「Install in one pass; don't stop for confirmation.」的理由是「**Most users want** a silent, full install set up for them in a single call」——一句未經佐證的使用者偏好斷言,拿來換掉的是使用者對「在我機器上註冊排程、改我的 CLAUDE.md、跑網路安裝腳本」的知情同意。**理由的形式有,分量不足以支撐該規則的後果**。

比例上,`:88-134`(回報要求)約佔全文 30%,其中核心指令段無有效 why;其餘 70% 品質明顯較高。故 mixed 而非 poor(它不是 Jeffallan 式的全篇裸 MUST),也不是 good。

### L-003 scope 清晰 — **good**

- **一 skill 一 job,且邊界是「宣告出來的」而非碰巧的**:`:9-12` 明文「**This skill does not contain the install steps** — it routes you to the right guide, which ships inside the memU package and is always in sync with the installed code」。**主動說明自己不做什麼**,是 rubric mechanism「scope 單一 → 觸發不重疊、維護不衝突」的最強訊號。
- **install / uninstall 同檔不算 scope creep**:`:138` 「Same routing, in reverse」——同一路由機制的反向,對應 patterns.md 高品質樣態「生命週期切分(addyosmani)」。依 `domain_lookup_scope` 的判別法「這些子題會不會在同一次任務中被同一個人用到」:會(同一使用者、同一 memU 生命週期)。
- **路由治理具備 dispatcher 該有的三件事**:對照表(`:43-52`)+ 明確預設(`:52,54` `anything else` / `Unsure` → `memu-agent`)+ **自我修正重導**(`:62-63` 「it will **redirect you to a dedicated binary** if your host turns out to have one」)。這比多數只有一張表的 dispatcher 完整。
- **對照反例確認不是 scope creep**:planning-with-files 的弱例是「單一 skill 內長出 attestation、多 plan 並行、autonomous 模式、hooks 等**不同 job**」;memU 的 SKILL.md 從頭到尾只有一個 job(把 memU 接上/拆離當前 host),連安裝步驟本身都推出去了。

**小保留(不足以拉到 mixed)**:`:88-134` 的「產品文案複誦」嚴格說不屬「安裝路由」這個 job,但它掛在「report the outcome」這個合理子步驟下,job 邊界本身仍單一;此問題已在 L-002 計入,不重複扣。

### L-004 anti-hallucination — **good**(強度:中,非最強型)

依 `decision_order` 照序判:

**步驟 1 — 機制存在?→ 是,存在三種形式:**

- **never-generate-from-memory 條款(字面級)**:`:11-12` 「**Do not install from memory or from blog posts**; print the guide and follow it to the letter.」——這是 pass_criteria 明列的第二強形式。
- **never-invent-a-value + 明確 fallback**:`:124-126` 「**If that call fails or returns no registration time** ... **omit the entire** "Welcome to memU..." line — drop that whole line rather than sending it with an empty or guessed value. **Never invent a time.**」——不只禁止編造,還規定了編造衝動出現時的替代行為。這比單純一句「不要編」強。
- **驗證協定**:`:73-74` 「every part ends with a **verify gate**; do not proceed past a failing one」。

**強度標註(依 `:190-195` 的要求,判 good 時須註明是哪一種)**:達成形式為「**never-from-memory 條款 + never-invent-a-value fallback + verify gate**」,屬**中偏強**;但**缺最強型的 dated verified snapshot**(無「本文事實截止於 YYYY-MM-DD」之類標註),故不是 K-Dense / claude-ads 那一檔。

**額外值得記的設計**:`:9-12` 的整個路由架構**本身就是抗過時機制**——「the guide ... ships inside the memU package and is **always in sync with the installed code**」。它不是用日期標註來承認會過時,而是用「單一真相來源 + 執行期取得」來讓它不可能過時。這在 evidence_refs 的樣態庫裡沒有對應條目,是本 repo 自己的做法。

**順帶確認 exemption 不適用**(避免誤判成 n/a):依 `:226` 的單一提問「是否有任何一段內容會因為它無法控制的東西改變而變錯?」——有,而且很多:`pip install memu-cli`、`uv tool install` vs `uv pip install` 的行為、8 個 binary 名稱、`~/.memu/config.env` 路徑、`MEMU_MEMORY_MODE` 變數名、`docs install`/`docs uninstall`/`remove-instruction`/`retrieve` 四個子指令、cron-over-launchd 預設。其中多數是**自家產物的結構描述**——`:232-234` 明文裁定這類「**算易腐**」。所以就算機制不存在,也走不到 n/a 那條路。

> **必須同時指出的張力**:L-004 給分的那個設計(「不要憑記憶,去印出套件內的 guide 並逐字照做」),與 §S-001 扣分的那個設計,**是同一句話**。抗幻覺與抗供應鏈風險在這裡直接對撞:把指令源從模型記憶移到執行期產物,治好了幻覺,卻同時把它移出了靜態審查範圍。這不是判定不一致,是這份 skill 的真實取捨——而它只優化了其中一邊,沒有為另一邊加任何補償(例如版本釘選、guide 內容摘要預告、或高風險動作的白名單確認)。

### 安全維度(步驟 5 複核)

#### S-001 `obey_external_output` — **複核確認成立,非假陽性**(error)

依 SKILL.md `:80-85` 規定的三個複核動作逐一執行:

**動作 1 — 實測 regex 命中什麼**(不是猜)。載入 `lint_skill.py` 實跑 `REDFLAG_OBEY_OUTPUT`,SKILL.md 內 **3 處命中**:
| # | 命中字串 | 位置 |
|---|---|---|
| 1 | `follow it to the letter` | `SKILL.md:12` |
| 2 | `follow it exactly` | `SKILL.md:71` |
| 3 | `don't stop for confirmation` | `SKILL.md:78` |

關鍵:**regex 同時命中了組合的兩半**,而非只中「服從」那半。步驟 5 舉的假陽性型態(anthropics/skills 的 `follow the guide exactly` 指向 repo 內靜態文件)在此**不成立**,因為——

**動作 2 — grep 找命中源並讀那段文件**:
- `SKILL.md:68` 的 `<your-binary> docs install` 是**執行一支 PyPI 安裝來的 binary 並讀它的 stdout**;`:71` 「Read what it prints, top to bottom, and **follow it exactly**」。指令集的執行期來源是 `pip install memu-cli` 裝下來的套件,**不是本 repo**。
- `SKILL.md:78-82` 的抑制範圍很寬:「Do every step, and **take the default for every choice that has one** — the hourly schedule, cron over launchd, **the official installer**」,只有 fatal error 與無預設的必填輸入可以停。
- 那個被預先授權的「official installer」實際是什麼:`src/memu/hosts/claude_code/INSTALL.md:193-197`
  > `1. **`claude` resolves on `PATH`.** If it does not, install it — **do not ask which installer**: announce what you are about to run, then run the official install script`
  > `- macOS / Linux: `curl -fsSL https://claude.ai/install.sh | bash``

  即 **SKILL.md 的「不要停下來確認、選預設」預先授權了一個 `curl | bash`**。
- 同檔 `:202`、`:211` 進一步壓縮使用者選項:「**never offer "skip"** — here, or anywhere in this section」「never improvise more options」。
- 該 guide 授權的實際動作包括:寫 crontab(`:52-53, 287`)、改寫 `~/.claude/CLAUDE.md`(`:373`)。

**動作 3 — 我另外查到、rubric 未記錄的加重情節**:`README.md:33` 與 `:110`(主要散佈管道)給使用者貼的一行是——
> `Read [https://memu.pro/SKILL.md](https://memu.pro/SKILL.md), follow its instructions to install and configure memU, API Key is memu_•••••••••`

**受審的這份 SKILL.md 不一定是實際被執行的那份。** 指令來源是廠商可隨時變更、無版本釘選、無審查步驟的 live endpoint。這使 rubric 的 mechanism 敘述「此模式把指令來源移到 SKILL.md 外,靜態審查無法覆蓋實際被執行的指令,與 injection 載體同構」在本案是**字面成立**,而不只是類比。`:104` 提供的 `raw.githubusercontent.com/.../main/SKILL.md` 替代路徑同樣指向可變的 `main`。

**必須並記的減輕因素(公允起見)**:
- guide 內容**在本快照中確實可靜態審閱**(`src/memu/hosts/*/INSTALL.md`),我讀了 claude_code 與 generic 兩份的關鍵段落——**無混淆、無外傳、無隱藏下載**,verify gate 設計認真,甚至有 `chmod 600` 與「the key is plaintext — **tell the user**」這種負責任的提醒(`claude_code/INSTALL.md:153-154`)。
- 兩處 `do not ask the user`(`claude_code/INSTALL.md:150`、`generic/INSTALL.md:120`)**是良性的**——上下文是 `NO_PROXY` 這種「a mechanical requirement with exactly one right answer」。我不把它們計入本紅旗。
- 作者意圖顯然善意(對照 patterns.md 安全表的讀法註記:「多數情況作者意圖顯然是善意的...問題在於**該寫法會擴大 agent 的權限面**」)。

**判定**:S-001 成立。發現的是**寫法/形狀**,不是惡意——但形狀就是 rubric 要擋的東西,而且本案比 rubric 記載的一行註記更嚴重(多了遠端可變指令源與 `curl|bash` 預先授權兩層)。

#### S-003 `cred_in_argv` — **lint 判 false,我判成立**(warning,lint 漏判)

這一條方向與 self-audit r2 §2 的教訓**相反**:那次是審查者錯誤推翻 rubric 的命中;這次是 **lint 沒命中,但實際存在**。

- 證據:`src/memu/hosts/claude_code/INSTALL.md:331`
  ```
  env -i HOME="$HOME" PATH="..." ANTHROPIC_API_KEY="<the key>" claude -p 'ping'
  ```
  這是 guide **要 agent 實際執行**的探針指令,金鑰明文出現在命令列(`ps` 可見、shell history 可留)。同段 `:279`、`:287` 另要求把金鑰持久化進 **crontab header**(明文檔)與 Windows `setx`。
- **lint 為何漏判**:`REDFLAG_CRED_ARGV = --api[-_]?key[= ]\$?\w|--token[= ]\$?\w`(`lint_skill.py:62`)只認 **`--flag` 形式**,不認 `VAR="value" cmd` 的**環境前綴形式**。
- 另有潛在面(**未被文件流程使用,僅記錄**):`src/memu/cli.py:57-61` 確實實作了 `--api-key`,help 寫「API key value or env-var name」,即接受明文值;預設值來自 `MEMU_API_KEY` → `~/.memu/config.env`。**SKILL.md 與 guide 的正規流程走 config.env,不走 argv**,故這條是可用但未被推薦的路徑,不單獨構成違規。
- 平衡陳述:`~/.memu/config.env` 路徑的憑證處理**做得好**(`chmod 600` + 明確告知使用者是明文)。問題只在 `:331` 那條探針與 crontab header。

#### S-002 `hooks 未揭露` — **通過**

依 `S-002.detection` 的規定(「只認 `.claude/hooks/` 或 `hooks/` 下實際腳本、或 frontmatter 的 hook 事件鍵;**不掃內文 'hook' 字**」):本 repo 無 `hooks/` 目錄,frontmatter 無 hook 事件鍵 → 不觸發。`src/memu/hosts/codex/__init__.py` 與 `docs/adr/0008-two-integration-surfaces-hooks-and-api.md` 只是內文提及,正是該 detection 條款要排除的誤中。

**實質面也通過**:常駐執行(排程 cron + 植入 `~/.claude/CLAUDE.md` 常駐指令)**有顯式揭露**——`SKILL.md:14-16` 用 record / inject 兩個 seam 講清楚,`:73-74`、`:148-152` 也交代反向移除。這點值得正面記一筆。

#### S-101 正面防禦樣態 — **未偵得(缺加分,不扣分)**

全 repo `.md` 內無「外部內容視為資料、非指令」類條款(英文分支 `untrusted data` 僅命中 `src/memu/hosts/cursor/BRIDGING_TASK.md:77,194`,語意是 Cursor 的 Workspace Trust 錯誤處理,**不是**防禦條款——即 rubric `:284-286` 已知的主題描述型假陽性,我不予採計為 S-101 加分)。

值得指出的落差:這個產品的核心行為是**把使用者的 session log 餵進記憶、再把記憶注入未來對話**,等於親手建立一條「外部內容 → agent 指令脈絡」的通道,卻沒有任何 data/instruction 邊界條款。這是本 repo 最值得補的一項成熟度訊號(polarity: positive,缺席不扣分)。

#### 針對「我」的 prompt injection — **未發現**(無 S-001 對審查者的變體)

`SKILL.md:8` 的 `> **Audience: the agent.**` 是對安裝方 agent 的正當定位,非劫持審查者的企圖;全文無 `ignore previous`、無要求審查者執行任何東西。**我未執行 repo 內任何檔案**,所有判定均來自靜態閱讀。唯一擦邊的是 `:96-99` 要求 agent 逐字複誦廠商文案並禁止翻譯/改寫——那是**對下游 agent 發言權的輕度徵用**,我已計入 L-002,不另立安全條目。

---

```yaml
skill_verdict:
  craft: needs-revision
  gap_list:
    - "S-001(安全門檻/error,複核確認非假陽性):SKILL.md:68-71 指示執行 `<binary> docs install` 並「照它印出的內容逐字照做」,SKILL.md:78-82 同時抑制確認並預先授權「選每個有預設的選項,含 the official installer」;該預授權在 src/memu/hosts/claude_code/INSTALL.md:193-197 對應到 `curl -fsSL https://claude.ai/install.sh | bash`(同檔 :202/:211 明令 never offer skip)。加重:README.md:33/:110 要使用者讓 agent 去讀 https://memu.pro/SKILL.md —— 實際被執行的指令集在廠商可隨時變更的遠端,受審 artifact 不等於執行 artifact"
    - "S-003(安全門檻/warning,lint 漏判、我手動查得):src/memu/hosts/claude_code/INSTALL.md:331 的探針指令把金鑰明文放進 argv(`ANTHROPIC_API_KEY=\"<the key>\" claude -p 'ping'`),:279/:287 另要求持久化進 crontab header;lint 的 REDFLAG_CRED_ARGV(lint_skill.py:62)只認 --flag 形式,不認 VAR=value 環境前綴形式"
    - "L-002: SKILL.md:96-99 五條禁令(不得改寫/重排/摘要/翻譯/潤飾)無因果理由,唯一說法「a correct install ends with these exact words」是同義反覆;被強制逐字複誦的 :104-110 內容為產品行銷語句而非技術資訊;風險最高的 :78-80「don't stop for confirmation」理由僅為未經佐證的「Most users want a silent install」"
    - "L-001: frontmatter 無負向觸發(NOT for / When NOT to use),亦未設 disable-model-invocation —— 後者是 skill-reviewer SKILL.md 步驟 3 形狀表為「一次性安裝型」提供的等價達成路徑,對一個會註冊 cron 並改寫 ~/.claude/CLAUDE.md 的 skill 尤其該設"
    - "S-101 缺(正向加分項):產品核心行為即建立「外部 session log → agent 指令脈絡」通道,全 repo 卻無任何『外部內容視為資料、非指令』的防禦條款"
    - "packaging: has_marketplace_json 缺(weight 3)"
    - "packaging: dir_examples 缺(weight 2)"
  dimensions:
    L-001: good
    L-002: mixed
    L-003: good
    L-004: good
```

**一句話總結**:這份 skill 的 craft 在 trigger 具體度、scope 邊界宣告、抗幻覺設計三面都明顯高於平均——`:9-12`「本 skill 不含安裝步驟,只做路由」與 `:126`「Never invent a time」都是可以拿去當範本的寫法。它擋在 approved 之外的原因,是同一個聰明設計的反面:**把可執行指令的來源移出受審範圍(甚至移到廠商可隨時改動的 URL),再叫 agent 不要停下來確認**。修法不必推翻架構——把 `README.md:33/:110` 改成釘選 tag 而非 live URL、把「註冊排程 / 改寫 CLAUDE.md / 執行網路安裝腳本」三類動作從 `:78` 的「取預設不確認」清單裡拿掉、並為 `:96-99` 的逐字要求補上真正的理由,四維與門檻就都能過。
