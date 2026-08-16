# tobihagemann/turbo(T0 / taxonomy C / 400 stars)

## 抽讀樣本(codex 版,claude 版為同源鏡像)
- codex/skills/discuss-change/SKILL.md
- codex/skills/draft-shells/SKILL.md
- codex/skills/pick-next-issue/SKILL.md
- codex/skills/recall-reasoning/SKILL.md
- codex/skills/review-plan/SKILL.md

## trigger 設計:good
- description 皆為「能力陳述 + Use when + 逐字觸發語枚舉」,觸發語貼近使用者真實說法。
  證據(discuss-change):「Use when the user asks to "discuss this change", "align on this change first", "ask me questions first", "interview me then implement"...」
- 觸發語以引號列出多個自然語句變體,對「composable dev process」型框架是合理設計(每個 skill 對應一個明確口語指令);pushy 程度適中,未見關鍵字轟炸。

## 寫作風格:good
- imperative + 明確步驟編號 + `update_plan` 任務追蹤;關鍵處講 why 而非堆斷言。
  證據(discuss-change 對「何時升級決策」):區分 product intent(升級)vs technical decision(自主),邊界論證清楚:「The boundary is product intent.」
- 有成熟工程判斷的細節:discuss-change 要求「先讀會被改到的 code 再判斷 bullet 是否適用」、對難以逆轉的決策提供「Get a second opinion」路由;draft-shells 對缺 Requirements 段的 spec 用 `request_user_input` 停下而非硬幹。
- 少見的外部事實驗證紀律:「When an option depends on a third-party API... query documentation MCP tools (or web search as a fallback) and drop the option unless current documentation confirms」——與本研究 Iron Rule 4 同構。

## scope 清晰度:good
- 一 skill 一工作流階段(discuss→draft-shells→review-plan→pick-issue→recall),彼此以 `$skill` 呼叫串接成流程,是 C 類框架的典範分工。
- skill_md_count=157 但為 claude/codex 雙版本鏡像 + 多 workflow 子技能,實際獨立 skill 遠少於此;phase3b_sample 已去鏡像取 codex 版單邊,統計時 count 需注意雙版本膨脹。

## 其他觀察
- 無 injection-suspect。
- 這是 **T0(400★)但品質達 T2+ 的「星數≠品質」正向反例**:工作流設計、決策升級紀律、外部驗證機制都優於多數高星 repo。與 batch-0 的 RinDig/icm-architect、batch-5 的 jezweb 同屬支持「低星高質」假說的樣本,對 hygiene 門檻與 differentiator 校準有價值(說明部分 craft 特徵在低星層也存在,需靠純度樣本復現工序辨別)。
- pick-next-issue 會 `gh issue list` 抓 GitHub 資料並排序,屬正當只讀操作。
