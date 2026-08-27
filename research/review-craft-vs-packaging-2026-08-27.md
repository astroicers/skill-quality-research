# craft 那一半:盤點、實測、以及一個從來不說「不」的判準(2026-08-27)

**起因**:使用者反映專案的對外第一句(「高星 repo 的共同點是好裝,不是寫得好」)
讓人以為**這個工具只做安裝檢查、不管寫得好不好**,並要求查證「我們是不是真的沒在審 craft」。

三份獨立盤點(對外文字 / 工具機制 / 已做審查)+ 三次不知情實測。

> ⚠️ **污染聲明**:三份盤點的判讀者已讀過 rubric 全文;三次實測的判讀者**未讀** rubric 以外的評價性檔案
> (禁讀清單見 §3.1),但其中兩位揭露了無法迴避的定錨(rubric 本身具名受審 repo)。
> 本輪判定**不得**充當 inter-rater 資料。

---

## 1. 答案分三層,而且彼此矛盾

| 層 | 結論 |
|---|---|
| **呈現面** | 使用者是對的,而且是結構性的 |
| **條文面** | 完全相反 —— craft 遠比 packaging 厚 |
| **執行面** | craft 零機器背書,而且**判準從來不說「不」** |

### 1.1 呈現面:craft 在對外文字裡近乎隱形

README 375 行:談 craft 約 **50 行(13%)**、談 packaging/CI 約 **165 行(44%)**。
而那 50 行**有 26 行(L333–358)在講 craft 判定有多不可靠** —— 正面主張 craft 的篇幅只剩 **約 24 行(6.4%)**。

- **14 個標題無一含「craft」或「工藝」**。唯一含「工藝」的粗體行是圖表小標
  「**工藝面 —— 沒有梯度**」,語意是負向的
- **能複製貼上的東西全是 packaging**:quickstart 給了 lint 的程式碼區塊,craft 路徑是純散文
- **標語出現 5 次,只有 1 次立刻澄清**。`CHANGELOG.md:502`、`plugin.json`、`marketplace.json`
  三處,標語都是該段落的**最後一句、後面什麼都沒有**;plugin description 的最後一個詞是 `not craft`
- **`marketplace.json` 頂層 description**(清單頁最可能顯示的一行)**`craft` 與 `packaging`
  兩個字都沒有**,只有「evidence-based」+「97-repo star-gradient study」——純研究定位、零工具定位
- **GitHub `about` 欄位是空的**。使用者以為的「about」其實是 README 標語
- 「craft 才是核心價值」這句話**逐字搜遍所有對外文字都找不到**。最接近的完整句在
  `research/EXECUTIVE-SUMMARY.md:8` 與 `CLAUDE.md:30`,兩者都不是第一觸點。
  README 裡最接近的是 L170,而它是 **bash 程式碼區塊裡的註解** —— 不會進 TOC、側欄或搜尋摘要

唯一把這件事寫進**標題**的地方是 `skill-reviewer/SKILL.md:62`
(「步驟 4:質化審 craft(這是你的核心工作,lint 做不到)」)——**只有 agent 載入時才讀得到**。

### 1.2 條文面:craft 比 packaging 厚 4.5 倍

| | 條數 | 平均非空白字元 | 進分數? |
|---|---|---|---|
| script differentiator(packaging 面) | 5 | **325** | ✅ 唯一有數字的一組,合計 14 分 |
| craft_llm(L-001~004) | 4 | **1458** | ❌ 無 weight、無 severity |

而且厚在會改變判定的地方:`decision_order`、`equivalent_forms`、`exemption`、
`disambiguation`、`domain_lookup_scope`、形狀分類前置步驟。

- **54 份質化筆記中 craft 佔實質論述 70%;`packaging` 出現 0 次、`marketplace` 出現 0 次**
- rubric 修訂史:**craft 改過 4 次**(1.1.0 的 7 個例外欄位、2.0.0 L-004、2.1.0 L-002、2.1.1 勘誤),
  而 **packaging 的 R-001~R-005 自 2026-08-16 定稿起一個字都沒改過**

### 1.3 執行面:craft 零機器背書

- **不計分**(無 weight/severity)、**不進 CI**、**evals 從未斷言**
  (`evals.json` 的 `craft_verdict` 全是給人讀的散文,`run_evals.py` 只斷言 hygiene error)
- **`skill_verdict` 全 repo 無任何程式解析**
- gate 端 craft **只降黃旗、不擋**
- 信度量過兩輪後**正式宣告不可行**(每維度需 n≈404,母體 54,差 7.6 倍)

---

## 2. 最刺的一條:41/41 全部 approved

跨 5 輪實際審查,**41 個對象、約 152 個維度標記,craft verdict 41/41 全是 `approved`**。

史上唯一一次 `needs-revision` 來自 **hygiene 不是 craft**,且該則後來被判為工具缺陷
([`misjudgments.md`](misjudgments.md) 的 H-001 那條)。

craft 判讀**推翻過確定性層 6 次以上,方向一律是「往上救」**(把 lint 的假陰性判回 good),
**沒有一次往下**。而「packaging 高但 craft 判 needs-revision」——**零例,且結構上不可能**:
packaging 唯一跑出高分的那一輪(08-27 marketplace)根本沒做 craft 判讀。

### 成因是門檻,不是判讀敷衍

舊規則(`SKILL.md:127`):`needs-revision` iff **hygiene error 未過,或任一維度判 poor**。

而 `poor` 極為罕見。54 份質化筆記的維度評級(以 `^## <維度>[:：]` 逐檔解析,54/54 全解析):

| 每份的 mixed 個數(3 維度) | 份數 |
|---|---|
| 0 | 30 |
| 1 | 14 |
| 2 | 6 |
| 3 | 4 |

(上表為**寬鬆解析**;嚴格解析為 `{0:30, 1:14, 2:8, 3:2}`,見下方敏感度表。)

⚠️ **這個數字我錯過兩次,兩次都是計數方法**:
1. regex 字元類放了兩個**半形**冒號而半數檔案用**全形**`：`,只解析到 27/54,連 `poor` 名單都認錯
2. 修好之後,**逐維 mixed 數用嚴格解析、百分比用寬鬆解析**——同一份文件混用兩套
   (由獨立複審指出)

**解析規則與敏感度(2026-08-27 獨立複審指出後補)**:54 份筆記中有 **3 格是複合標籤**
——`mvanhorn__last30days-skill.md` L-002「poor→mixed(結構上 poor,內容誠實度高)」、
`nexscope-ai__Amazon-Skills.md` L-002「mixed(偏 poor)」、`vibeeval__vibecosystem.md` L-001「mixed → poor」。
兩種處置給出不同數字:

| 解析 | poor% | **≥2 mixed** | ≥3 mixed | 逐維 mixed |
|---|---|---|---|---|
| 嚴格(複合格丟棄) | 1.9% | **20.4%** | 5.6% | 15 / 14 / 7 |
| 寬鬆(取第一個 token) | 3.7% | **20.4%** | 11.1% | 16 / 15 / 7 |

⚠️ **本次採用的門檻不受這個選擇影響**——`≥2 mixed` 在兩套解析下都是 **20.4%**。
受影響的是 `poor%`(1.9 vs 3.7)與 `≥3 mixed`(5.6 vs 11.1)。
先前的敘述**混用了兩套**(逐維 mixed 數用嚴格、百分比用寬鬆),已統一為上表並在此揭露。

---

## 3. 實測:craft 判讀會不會說「不」

41/41 有兩種解釋——**選樣效應**(那 41 個都是有人選來裝的 skill)或**門檻缺陷**。
這兩者對應的修法完全不同,所以先實測。

### 3.1 方法

從現有語料**刻意挑最弱的三個 repo**(其中兩個 `evals.json` 明確預期 `needs-revision`),
各派一個**不知情的獨立 context**,照 `SKILL.md` 步驟 1–5 完整跑一次,產出四維度逐條判定。

**禁讀清單**(違反即作廢):`evals/`、`qualitative_notes/`、`misjudgments*`、`review-*`、
`self-audit*`、`inter-rater-*`、`~/.claude/plans/`。派工單**不含 evals 的預期值** ——
本專案已實測過 rubric 定錨會讓一致率變成 1.000([`inter-rater-results.md:30-36`](inter-rater-results.md))。

### 3.2 結果

| repo | verdict | 來源 | L-001 | L-002 | L-003 | L-004 | 原始判讀 |
|---|---|---|---|---|---|---|---|
| `24kchengYe__human-skill-tree` | needs-revision | **hygiene** | mixed | good | mixed | mixed | [→](blind-craft-reviews-2026-08-27/24kchengYe__human-skill-tree.md) |
| `NevaMind-AI__memU` | needs-revision | **security** | good | mixed | good | good | [→](blind-craft-reviews-2026-08-27/NevaMind-AI__memU.md) |
| `Jeffallan__claude-skills` | **approved** | — | mixed | mixed | good | mixed | [→](blind-craft-reviews-2026-08-27/Jeffallan__claude-skills.md) |

> **三份完整判讀已逐字轉錄進版控**(2026-08-27):
> [`blind-craft-reviews-2026-08-27/`](blind-craft-reviews-2026-08-27/)。
> 此前只有本表進版控,原始輸出活在 session transcript 裡,兩輪複審都把它列為待補證據。
> ⚠️ 該目錄含具名 craft 證據,**已加入 `inter-rater-protocol.md` 與 `RATER-BRIEF-R2.md`
> 兩份禁讀清單**。

**12 個維度標記:7 mixed、5 good、`poor` 零個。**
craft 自己那條路徑(「任一維度判 poor」)**在 12 次機會裡一次都沒開火**;
兩個 needs-revision **都來自別的門檻**。

**`Jeffallan` 判 `approved` 時帶著**:80 條 MUST DO/MUST NOT DO 僅約 8 條附因果理由
(`cloud-architect/SKILL.md:66-84` 十六條全裸,其中「Use overly complex architectures」不可證偽)、
五份樣本零 override 節、零 anti-hallucination 機制、兩個 skill 觸發面重疊且路由圖恰在該格斷裂、
且 `api-designer` 全篇以 **RFC 7807** 為現行標準——**該 RFC 已於 2023-07 被 RFC 9457 取代**,
全篇無任何時效標注。判讀者自己加了警告:「**approved 不等於優秀:四維中三維 mixed**」。

**⇒ 41/41 不是選樣效應,是門檻設得讓 `mixed` 不用付任何代價。**
而 `mixed` 正是審查者用來標示「這裡有問題」的那一格。

### 3.3 三位判讀者的誠實揭露(值得單獨記)

- **memU 那位**發現 `rubric-manual-dimensions.yaml:249` 與 `patterns.md:47`
  **直接把 memU 具名為 S-001 的正典實例**,主動揭露這是無法迴避的定錨,並**不採信標註、
  重跑步驟 5 的三動作複核** —— 結果查到比 rubric 記載的更多(見 §4)
- **Jeffallan 那位**同樣發現 rubric 具名該 repo(`evidence_refs` 的「裸 MUST 堆疊=弱例」),
  對 L-002 改做可複現計數,**確認觀察為真但不跟隨標籤隱含的 `poor`** ——
  因為 2.1.0 的 `equivalent_forms` 認可結構化門檻表,而五份樣本全部具備。
  它把分歧點寫下來供覆核:「若我只照標籤走,這裡會判 poor,verdict 會翻成 needs-revision」
- **human-skill-tree 那位**看到一段長得很像防禦條款的文字,**主動不給 S-101 加分**,
  引的正是 rubric 2.2.0 才加的 `confidence_rationale`(「以不可信輸入為主題的技術文件會整類命中」)
  —— **那段條文第一次被實地驗證影響了判定**

---

## 4. 實測順帶撈到的四個缺陷

| # | 缺陷 | 出處 |
|---|---|---|
| a | **`SKILL.md:127` 的上卷規則漏掉 security** —— 照字面讀,一個經複核確認的 S-001 會得到 `approved`,而同檔「方法論前提」明寫「安全一律是門檻」。**同一份文件兩處給出相反答案**,且那是 gate 端會消費的那條 | memU 實測 |
| b | **`REDFLAG_OBEY_OUTPUT` 有極性盲區** —— `without confirmation` 命中了「**DO NOT PROCEED** without confirmation」與「**MUST NOT DO**: … without confirmation」,兩處極性都相反。**與 2.2.0 修過的 S-101 中文分支同一缺陷型,只是發生在紅旗側** | Jeffallan 實測 |
| c | **`REDFLAG_CRED_ARGV` 漏 `VAR=value cmd` 環境前綴形式** —— `ANTHROPIC_API_KEY="<key>" claude -p 'ping'`(`memU/src/memu/hosts/claude_code/INSTALL.md:331`)不會命中,只認 `--flag` | memU 實測 |
| d | **`has_tests_or_evals` 對「有驗證但不叫 tests/」的 repo 假陰性** —— Jeffallan 有 77KB 的 `validate-skills.py` + 三個 CI workflow + pre-commit,但無 `tests/` 目錄。與已知的 `dir_examples` 同型 | Jeffallan 實測 |

另外三個來自盤點:**H-002 條文有程式沒有**、**differentiator 條數 5 vs 6 漂移**、
**`signal_type: craft` 名實不符**(`has_tests_or_evals`/`dir_examples` 實作是目錄存在性,
而 `rubric.yaml:10` 自己寫「無一是寫作工藝」)。全部入 [`misjudgments.md`](misjudgments.md)。

---

## 5. 已知限制:哪些數字不可機械重建

本報告有兩組數字**無法從 repo 內以程序重建**。列在這裡不是為了留白給下一個人補,
而是因為**明記做不到,比讓它看起來像漏做要好** —— 這個 repo 已有兩次
(κ 路線、指令極性)靠宣告不可行換到正確結論的先例。

| 數字 | 出處 | 為什麼不可機械重建 | 為什麼不補 |
|---|---|---|---|
| **41 個對象、約 152 個維度標記、41/41 `approved`** | §2 開頭 | 這 41 筆散在 **4 份格式不統一的歷史 review 報告**裡:有的用 `skill_verdict` YAML 區塊,有的用散文段落,有的只有一張總表。沒有共同的可解析欄位 | 要補就得**回頭改 4 份歷史報告的格式**,而那等於重寫已完成的稽核紀錄。且這些數字的**用途**(證明「craft 判準從來不說不」)已由 §3 的三次不知情實測**獨立確認** —— 12 個維度標記、craft 路徑 0/12 開火。用途達成了,重建的邊際價值接近零 |
| **README 375 行中 craft 約 50 行、packaging/CI 約 165 行、其中 26 行在講 craft 不可靠** | §1.1 | 是**人工逐行歸類**。一行屬於 craft 還是 packaging,經常取決於它在論證裡的角色而非關鍵字 —— 例如統計限制段講的是 craft 的**可信度**,算 craft 篇幅還是算警語篇幅,是判斷不是規則 | 硬做成腳本會製造**假的精確感**:一個 `grep -c` 出來的比例看起來可複現,實際上只是把判斷藏進了 regex。與其給一個假裝客觀的數字,不如明說它是人工盤點 |

**共同的處置**:兩組數字在原文中都已標為約數(「約 152 個」「約 50 行」),
本節補上它們**為何**只能是約數。若未來要重建,正確的做法是先統一
`skill_verdict` 的落檔格式**再往前跑**,而不是回頭改歷史。

---

## 6. 處置

### 已做

- **rubric 3.0.0:上卷規則改寫**(補 security 門檻 + `mixed` 開始計費 + 三態),
  規則移入 rubric 正本為 canonical;`run_evals.py` 新增取值域守衛(含兩個負向驗證)
- **對外定位全面改寫**:README hero/標題/quickstart、兩份 JSON、GitHub about、SKILL.md frontmatter

### 刻意不做

- **不刪、不弱化星數梯度結論**。它有 97 個 repo 的資料支撐,而且
  `README.md` 的統計限制段是這個 repo 最誠實的部分之一
- **不為了讓 craft「看起來有在做事」而發明分數**。craft 不計分是刻意設計
  (`rubric.yaml:10-11` 有論證);修的是**上卷門檻**,不是硬塞 weight
- **不改 ASP `pipeline.md`**:`approved-with-notes` 在 gate 上不會產生訊號
  (那裡只認 `needs-revision`)。要讓它發聲得改 ASP 安裝副本,而升級會覆蓋。**已記為已知限制。**

## 7. 對本專案的意義

1. **「使用者的一個直覺」比三輪自審更有效**。這一整條線的起點是一句
   「我們的 about 讓人覺得只在乎安裝檢查」——而它撈出了 41/41 這個結構性缺陷。
   與 [`self-audit-round2.md`](self-audit-round2.md) §12–15 的歸類一致:發現來自
   **拿工具去用**或**外部指出**,零個來自更多分析。
2. **條文寫得厚 ≠ 判準會作用**。craft 的條文是 packaging 的 4.5 倍厚、修訂 4 次 vs 0 次,
   但因為上卷門檻設在 4% 的事件上,**整半邊等於沒有輸出**。
   厚度是投入的證據,不是效果的證據。
3. **rubric 2.2.0 的 `confidence_rationale` 第一次被實地驗證**——一位不知情判讀者
   讀了它、據以不給 S-101 加分。條文影響判定這件事,終於有了一個可指認的實例。
