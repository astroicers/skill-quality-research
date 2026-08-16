# kangarooking/cangjie-skill(T1/B/8054)

## 抽讀樣本
- SKILL.md(根目錄單體 skill,全文 169 行)

## trigger 設計:good
- description 枚舉中英使用者原話(「拆书」「蒸馏一本书」「turn a book or video into skills」)並附 NOT-for 邊界:「NOT for simple summarization, book reviews, or role-playing as the author (that is nuwa-skill's job)」——正負觸發 + 指路兄弟 skill。
- 甚至把「description 必須明確 trigger 條件,不能只是『一个关于 X 的 skill』」寫進自己的品質紅線(meta 級自覺)。

## 寫作風格:good
- imperative 五階段流水線,關鍵步驟解釋 why:「用户轻确认……阶段 2–4 是最耗时的部分,这一步确认能避免大量返工」、「不凭记忆拆书——没文本就停下来问」。
- 有硬性品質紅線(「违反则阻止输出」)、斷點續跑機制(PIPELINE_STATE.md)、降級方案(不支援並行時串行)。範例具體(「帮我拆《穷查理宝典》」)。

## scope 清晰度:good
- 一個 job:長內容→原子 skills。✅/❌ 邊界表明確;與 nuwa-skill(蒸餾人)/darwin-skill(進化 skill)的生態分工寫成專節,輸出格式對接 darwin。
- 方法論細節外移 methodology/、extractors/、templates/,主檔保持路由層。

## 其他觀察
- 內建對產出 skill 的壓力測試要求(應調用/誘餌/邊界模糊 prompt,含跨 skill 混淆測試)——與 obra/superpowers 的 TDD-for-skills 理念相同,出現在 T1 層值得注意。
- 無 CLAUDE.md;無 injection-suspect。
