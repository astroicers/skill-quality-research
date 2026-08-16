# self-audit.md — 用 skill-reviewer 回測自家 skills(Phase 6, D6)

- 日期:2026-08-16
- 對象:talk-craft、slidev-deck-stack、visual-web-stack、security-weekly-tw
- 方法:`lint_skill.py`(packaging + hygiene + security)+ 本 LLM 對 SKILL.md 的 craft 判讀
- 目的:校準 rubric,記錄 false positive/negative → 回饋修訂

## 1. lint 結果(全部 4 個)

| skill | hygiene | packaging | H-004 dir_scripts | craft(LLM 判) |
|-------|---------|-----------|-------------------|----------------|
| talk-craft | pass | **0/14** | ✗ | 高:description 具 Triggers 段、imperative、scope 單一(簡報論證) |
| slidev-deck-stack | pass | **0/14** | ✗ | 高:觸發情境具體(Slidev 專屬)、references/ 分層 |
| visual-web-stack | pass | **0/14** | ✗ | 高:觸發錨定技術棧訊號(R3F/Lenis)、scope 清楚 |
| security-weekly-tw | pass | **0/14** | ✗ | 高:Triggers 中英雙列、job 明確(週報/術語) |

## 2. ⚠ 關鍵 false negative:packaging benchmark 對「個人內部 skill」系統性失準

**4 個 skill 全部 packaging 0/14 → lint 標「低於 T1 剖面」,但它們都是成熟、精心設計的高質工具。**

原因:自家 skills 是 SKILL.md/references 型**個人工具**,天然沒有 marketplace.json、一行安裝、
before/after README、demo media——因為它們**不對外發布行銷**。5 條 packaging differentiator
(全來自「對外發布的高星 repo」樣本)對內部 skill 全數不適用。

這不是 rubric 錯,而是**精確印證了整個研究的核心結論**(G3 發現 A):
> 星數關聯的是 packaging/可發現性,不是 craft。內部 skill 沒有 packaging 訊號,不代表 craft 差。

**修正機制早已內建**:SKILL.md 三段式輸出明訂「受審 skill 可宣告『內部工具,不採計 marketing/packaging 子分數』」。
→ 對這 4 個 skill,正確判定是:**craft verdict = approved;packaging 不採計;tier benchmark 只報 craft 剖面**。

## 3. 其他誤判記錄

| 項目 | 類型 | 判定 |
|------|------|------|
| H-004 dir_scripts ✗(全 4 個) | 疑似 false positive | talk-craft/slidev 等是**純知識/方法論型** skill,本就不需 scripts/。H-004 是 info 級不影響門檻,但應在 rubric 註明「純參考型 skill 豁免 deterministic offloading」 |
| S-002 registers_hooks(talk-craft、visual-web-stack)| false positive | regex 誤中 references 內文提到的 "hook"(如 React hooks、GSAP hook),非真的註冊 harness hook。confidence 已標 low-static-needs-llm,LLM 複核應駁回 |

## 4. 回饋 rubric 的修訂建議(→ 下一輪迭代)

1. **tier benchmark 分軌**:packaging 剖面與 craft 剖面**必須分開報**,且對宣告「內部工具」者
   tier 只由 craft 剖面決定。現行 lint 的 `tier_benchmark_packaging` 單獨看會誤導,SKILL.md 已要求
   LLM 分列子分數,但建議 lint 輸出層就把「packaging tier」明確標為「僅 packaging 面,非總評」。
2. **H-004 豁免條款**:純知識/參考型 skill(無確定性操作)豁免 dir_scripts,避免 info 級雜訊。
3. **S-002 hooks 偵測**:縮小 regex,只認 frontmatter 的 hook 註冊或 `.claude/hooks/`,不掃內文 "hook" 字。
4. **craft 是主判的證據更強了**:4/4 內部 skill 的價值全在 craft、全被 packaging 漏判 → 再次確認
   skill-reviewer 的價值錨點是 LLM craft 層,lint 只是 packaging 過濾器與安全門檻。

## 5. 結論

skill-reviewer 雛形在自家 skills 上的表現**符合設計預期且暴露了正確的校準邊界**:
- ✅ hygiene 門檻、安全紅旗(帶 confidence)、craft_llm_todo 抽樣都正常運作
- ✅ packaging 0/14 的「失準」恰恰驗證了核心方法論(craft≠packaging≠星數)
- ⚠ 待修:tier 分軌顯示、H-004 豁免、S-002 regex 收窄
- 措辭紀律守住:全程「剖面」非「星數預測」

**這 4 個 skill 的實際評級**:craft approved、內部工具不採計 packaging——都是「低 packaging、高 craft」
的健康內部 skill,與研究樣本中的 ayghri/i-have-adhd、turbo 同型(低星/低 packaging 但 craft 達標)。
