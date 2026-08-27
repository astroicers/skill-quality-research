# 三次不知情 craft 判讀:原始輸出(2026-08-27)

這三份是 [`../review-craft-vs-packaging-2026-08-27.md`](../review-craft-vs-packaging-2026-08-27.md) §3.2
那張表的**原始證據**,也是 **rubric 3.0.0 上卷規則改寫**的直接來源。

> **為什麼要落檔**:此前只有摘要進版控,原始判讀活在 session transcript 裡。
> 兩輪獨立複審**都把「原始輸出未落檔」列為待補證據**——理由是 §3.2 的三列中
> 只有兩列能從 `evals.json` 交叉核對。現已補齊。

## 這批判讀在回答什麼

`craft verdict` 連續 **41 個對象全部 `approved`**,史上零次由 craft 觸發 `needs-revision`。
兩種解釋對應**完全不同的修法**:

- **選樣效應** —— 那 41 個都是有人選來裝的 skill,本來就不差 → 工具沒壞
- **門檻缺陷** —— `needs-revision` 只由 `poor` 觸發,而 `poor` 極罕見 → 判準等同關閉

所以從現有語料**刻意挑最弱的三個 repo**實測。

## 協定

**判讀者**:三個獨立 context,互不知道彼此存在,只拿到 repo 路徑 +
`skill-reviewer/SKILL.md`,照其步驟 1–5 執行。

**禁讀清單**(違反即作廢,派工單原文):

```
skill-reviewer/evals/            ← 尤其 evals.json,它含對這些 repo 的預期答案
research/qualitative_notes/
research/misjudgments.md、misjudgment-review-*.md
research/review-*.md、self-audit*.md
research/inter-rater-*
~/.claude/plans/
```

**派工單不含 `evals.json` 的預期值。** 理由:本專案已實測過 rubric 定錨會讓一致率
變成 **1.000**(見 [`../inter-rater-results.md`](../inter-rater-results.md) §「rubric 定錨」)。

**要求**:四個維度**每一條都要有值**,不得略過;判 `good` 也要附證據
——「找不到問題」和「查過而且它做對了」是兩件事。

## 結果

| repo | verdict | 來源 | L-001 | L-002 | L-003 | L-004 | 檔案 |
|---|---|---|---|---|---|---|---|
| `24kchengYe/human-skill-tree` | needs-revision | **hygiene** | mixed | good | mixed | mixed | [→](24kchengYe__human-skill-tree.md) |
| `NevaMind-AI/memU` | needs-revision | **security** | good | mixed | good | good | [→](NevaMind-AI__memU.md) |
| `Jeffallan/claude-skills` | **approved** | — | mixed | mixed | good | mixed | [→](Jeffallan__claude-skills.md) |

**12 個維度標記:7 mixed、5 good、`poor` 零個。**
craft 自己那條路徑(「任一維度判 `poor`」)在 **12 次機會裡一次都沒開火**;
兩個 `needs-revision` **都來自別的門檻**。

⇒ **41/41 不是選樣效應,是門檻設得讓 `mixed` 不用付任何代價。**

## 三位判讀者各自的定錨揭露(值得單獨讀)

派工單要求「若 rubric 內出現受審 repo 的名字,請明白記下你看到了什麼」。三位的處置:

| 判讀者 | 揭露內容 | 處置 |
|---|---|---|
| **memU** | `rubric-manual-dimensions.yaml:249` 與 `patterns.md:47` **直接把 memU 具名為 S-001 的正典實例** | **不採信標註**,重跑步驟 5 的三動作複核 → 查到**比 rubric 記載的更多**(遠端可變指令源、`curl\|bash` 預先授權、以及一條 lint 漏判的 S-003) |
| **Jeffallan** | `evidence_refs` 的「Jeffallan(裸 MUST 堆疊=弱例)」與 `patterns.md:21` | 對 L-002 改做**可複現計數**(逐條數 MUST 條目與附理由者)。**確認觀察為真但不跟隨標籤隱含的 `poor`** —— 因 2.1.0 的 `equivalent_forms` 認可結構化門檻表。**把分歧點寫下來供覆核** |
| **24kcheng** | 無預先標註 | 另主動揭露:harness 自動注入了受審 repo 的 `app/CLAUDE.md`,標明為抽樣清單外的證據 |

**其中一件事值得單獨記**:24kcheng 那位看到一段長得很像防禦條款的文字,
**主動不給 S-101 加分**,引的正是 rubric 2.2.0 才加的 `confidence_rationale`
(「以不可信輸入為主題的技術文件會整類命中」)。
**那是該段條文第一次被實地驗證影響了判定。**

## ⚠️ 污染聲明

判讀者未讀禁讀清單上的檔案,但**兩位揭露了無法迴避的定錨**(rubric 本身具名受審 repo)。
依 [`../../docs/llm-judge-contamination.md`](../../docs/llm-judge-contamination.md) §3,
**本輪判定不得充當 inter-rater 資料**,只作為使用驅動的判準校準證據。

## 保真度

三份都是**逐字轉錄**,不是重寫或摘要 —— 內文自 transcript 的 `<result>` 區塊整段取出,
**未改寫、未刪節、未重排**。唯一的機械處理是還原傳輸過程產生的 HTML 實體轉義
(`&lt;` → `<`、`&amp;` → `&`)。轉錄自 2026-08-27 的 session transcript(job `3629ecf0`)。

**未補上任何我事後才知道的事。** 唯一的例外是 memU 那份 §S-003 的一處事實歸因問題
(`VAR=value cmd` 不進 `cmd` 的 argv),它寫在**檔頭的「轉錄後註記」**裡、明確標為非原文,
**正文一字不動**;對應處置見 [`../misjudgments.md`](../misjudgments.md)。

## ⚠️ 本目錄在審查者禁讀清單上

這三份含具名 craft 證據與帶行號的完整推理鏈,而三個受審 repo 都在本專案語料內。
它是**比評級摘要更強的定錨形式** —— 不是別人的答案,是別人替你走完的整段推理。
已加入 [`../inter-rater-protocol.md`](../inter-rater-protocol.md) 的「必須隔離的東西」
與 [`../inter-rater/RATER-BRIEF-R2.md`](../inter-rater/RATER-BRIEF-R2.md) 的禁讀清單。
