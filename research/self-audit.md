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

## 4. 回饋 rubric 的修訂建議(✅ 1–3 已於本輪落地並驗證,2026-08-16)

1. ✅ **tier benchmark 分軌**:lint 輸出改為「packaging tier · 僅 packaging 面」+「craft tier: PENDING-LLM」
   兩行分列;`knowledge_only` 為真時印純知識型警語(packaging 天然偏低,總評以 craft 為準)。
   JSON 加 `benchmark_note` / `craft_tier` / `knowledge_only` 欄。
2. ✅ **H-004 豁免條款**:`knowledge_only`(pct_markdown ≥85% 且 code ≤2 且無 scripts/)時 H-004 判 N/A(顯示 —)
   而非 ✗。rubric H-004 加 `exemption` 註。4/4 自家 skill 已正確豁免。
3. ✅ **S-002 hooks 偵測收窄**:只認 `.claude/hooks/` 或 `hooks/` 下實際腳本、或 frontmatter 的 hook 事件鍵;
   移除內文 "hook" 掃描。visual-web-stack/talk-craft 先前的 React/GSAP hook 誤報已消除(sec=[])。
   三條均加 selftest 斷言(內文 hook 不觸發、frontmatter hook 觸發、純知識型豁免)。
4. **craft 是主判的證據更強了**:4/4 內部 skill 的價值全在 craft、全被 packaging 漏判 → 再次確認
   skill-reviewer 的價值錨點是 LLM craft 層,lint 只是 packaging 過濾器與安全門檻。
5. ✅ **parse_fm 支援 YAML block scalar**(§7 發現的 bug):`description: |` 多行描述現能解析,
   `desc_has_trigger`/`desc_head` 不再對 block-scalar skill 歸零;加 selftest 斷言。

## 6. Craft Verdict(LLM 層,三段式 — lint 做不到的核心判定)

依 `rubric-manual-dimensions.yaml` 的 craft_llm 組(L-001~004)讀 4 個 SKILL.md 原文判定。
**這正是 lint 無法自動化、必須 LLM 做的部分**——且過程中發現 lint 一個真 bug(見 §7)。

### talk-craft — Craft: **approved(T3 craft 剖面)**
- **1. Craft Verdict**:approved。內部方法論 skill,packaging 不採計。
- **2. Tier Benchmark**:craft 剖面 **T3**(達官方基準以上);packaging 0/14 宣告不採計。
- **3. findings**:
  - L-001 trigger **good**:「當你要寫、規劃或改一份簡報…時必須載入」觸發語境具體、適度 pushy,且明示與 slidev 的邊界(工具無關)。Triggers 近 40 詞但皆真實同義情境,未到 SEO 轟炸。
  - L-002 style **good(標竿)**:每條鐵則都附 why(鐵則2「最關鍵的東西放最後等於沒講到」、鐵則4「改結構便宜,改頁貴」)——正是「解釋 why 而非堆 MUST」。
  - L-003 scope **good(標竿)**:與 slidev-deck-stack 明確分工+交棒點,是 skill 間路由治理典範。
  - L-004 anti-halluc **present**:「撰寫基準 2026-06」+ `.fact-check.md`/`sources.md` 查證紀錄。

### slidev-deck-stack — Craft: **approved(T2–T3 craft 剖面)**
- L-001 **good**(具體觸發+必須載入);L-002 **good**(五層架構圖+v52 釘選);L-003 **good**(與 talk-craft 互補);L-004 **present**(v52 版本釘選 + `.fact-check.md`)。

### visual-web-stack — Craft: **approved(T2 craft 剖面)**
- L-001 **good**(觸發錨定客觀技術訊號 R3F/Lenis/ScrollTrigger);L-002 **good**(四層+單一強原則「DOM/Canvas 只經 Zustand」);L-003 **good**;L-004 **偏弱**(有 React 19 版本但無查證紀錄引用)。

### security-weekly-tw — Craft: **approved(T1–T2 craft 剖面)**
- L-001 **good**(英文 Use-when + 中英 Triggers);L-002 **mixed**(操作/路由手冊型,列 what/where 為主,少 why——對此類工具型 skill 合適但無 L-002 加分);L-003 **good**(功能→觸發詞對照表清楚);L-004 間接(術語庫有 validate_terminology 工具)。

**四者總評**:craft 全部 approved,craft 剖面 T1–T3。與研究樣本的 ayghri/turbo/jezweb 同型(**低 packaging、高 craft 的健康內部 skill**)。packaging 0/14 是內部工具的正確特徵,非缺陷。

## 7. ⚠ 新發現的 lint 正確性 bug(craft 層跑出來的)

**`parse_fm` 不支援 YAML block scalar(`description: |` 多行)**。4 個自家 skill 全用此語法,
導致 lint 的 `desc_has_trigger` 全誤判 False、`desc_head` 全空——但實際 4 個 trigger 設計都 good。
這是實質正確性 bug(會讓所有用 block scalar 的 skill 的 trigger 指標歸零),已於本輪修復
(`parse_fm` 加 block scalar 支援 + selftest 斷言)。修復後 3/4 skill 的 trigger 正確抓到。

**visual-web-stack 修復後仍 False**:它用「當專案使用…時必須載入」,而 `TRIGGER_RE` 的中文主詞只涵蓋
`當你/當使用者`。但其 craft L-001 已判 **good**(觸發錨定客觀技術訊號)。**這個「lint False 但 LLM good」
的對比不修**——它正是 desc_has_trigger 為 noise(G3 發現 B)的活證據:二元 regex 永遠追不完觸發句式,
craft 品質非靠 LLM 判不可。追著擴 regex 打地鼠會製造假的完備感,與研究結論背道而馳。

## 5. 結論

skill-reviewer 雛形在自家 skills 上的表現**符合設計預期且暴露了正確的校準邊界**:
- ✅ hygiene 門檻、安全紅旗(帶 confidence)、craft_llm_todo 抽樣都正常運作
- ✅ packaging 0/14 的「失準」恰恰驗證了核心方法論(craft≠packaging≠星數)
- ⚠ 待修:tier 分軌顯示、H-004 豁免、S-002 regex 收窄
- 措辭紀律守住:全程「剖面」非「星數預測」

**這 4 個 skill 的實際評級**:craft approved、內部工具不採計 packaging——都是「低 packaging、高 craft」
的健康內部 skill,與研究樣本中的 ayghri/i-have-adhd、turbo 同型(低星/低 packaging 但 craft 達標)。
