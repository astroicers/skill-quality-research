# blader/humanizer(T2 / B / 35886★)

## 抽讀樣本
- SKILL.md(單一 skill repo)

## trigger 設計:good
description 含標準觸發語且語境具體:「Use when editing or reviewing text to make it sound more natural and human-written」,並列舉可偵測的 pattern 名單讓模型能從任務語意匹配。不過度 pushy——沒有把「所有寫作任務」都攬進來,而是限定在編修/審稿情境。

## 寫作風格:good
全批次最佳寫作範本之一。33 個 pattern 每條都是「Words to watch + Problem(why)+ Before/After 實例」三件套,例:「LLMs substitute elaborate constructions for simple copulas」配上 Gallery 825 改寫例。更難得的是有整節 false-positive 防護(「A single em dash means nothing; …plus a "Conclusion" section is a confession」)與「Signs of human writing (preserve these)」,教判斷而非只下禁令。Invocation Modes(pasted/file/embedded)把輸出契約講清楚。

## scope 清晰度:good
一個 job:移除 AI 寫作痕跡。邊界處理細緻——明確排除 quotations/code/frontmatter,且規定 writing sample 優先於 skill 自身規則(「Matching the author beats scrubbing the tell」),避免 skill 越權改壞作者聲音。

## 其他觀察
- 無 injection 疑慮。
- frontmatter 帶 version metadata(2.9.1)與 MIT license,單檔 skill 也維持工程化版本管理,可作 rubric 的 metadata 特徵參照。
