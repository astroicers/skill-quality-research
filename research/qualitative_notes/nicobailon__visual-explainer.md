# nicobailon/visual-explainer(T1 / B / 9498★)

## 抽讀樣本
- plugins/visual-explainer/SKILL.md

## trigger 設計:good
description 用「Use for diagrams, architecture overviews, diff or plan reviews, project recaps, comparison tables, slide decks…」列舉觸發場景,body 再補量化門檻(「If a table would have 4+ rows or 3+ columns, render it as HTML」)。觸發面偏寬(「any visual explanation」)但與能力相符;quick mode / slides 皆設為 opt-in,避免過度搶戲。

## 寫作風格:good
以 invariant 清單 + routing 表組織,imperative 簡潔,關鍵禁令附因:「Never define page-level .node; Mermaid uses it internally」「15+ elements…use the hybrid overview + cards pattern」。反 generic 美學規則給到 hex 級具體度(禁 #8b5cf6 等 Tailwind 預設紫)。Final checklist 可逐項驗證。MUST 密度適中,少數段落(PPTX 匯出)句子偏長。

## scope 清晰度:good
一個 job:產自包含 HTML 視覺說明頁。以「Reference routing」表實作 progressive disclosure(只讀當前輸出需要的 template/reference),slide/quick/PPTX 等模式邊界與 fallback 條件都明確(「If it is not a fit…fall back to the normal full HTML workflow」)。

## 其他觀察
- 無 injection 疑慮。
- 同時支援多 harness(Pi 工具、MCP、Glimpse viewer)並各自定義 render 行為,是「跨 runtime 相容宣告」的中型範例;T1 層出現此成熟度值得在梯度分析中標記。
