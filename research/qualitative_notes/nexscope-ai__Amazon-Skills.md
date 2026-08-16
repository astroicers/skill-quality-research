# nexscope-ai/Amazon-Skills（T0 / taxonomy D / 546 stars）

## 抽讀樣本
- amazon-a-plus-content/SKILL.md（僅前 400 行）
- amazon-brand-analytics/SKILL.md
- amazon-fba-prep/SKILL.md（僅前 400 行）
- amazon-listing-images/SKILL.md
- amazon-variation-strategy/SKILL.md

## trigger 設計：mixed
- 品質落差極大。上界：brand-analytics 的 description 有 6 條枚舉式觸發情境 + 前置條件聲明（「Requires Brand Registry access. Use when: (1) analyzing Search Frequency Rank data...」），是全批次最詳盡的 trigger 之一；fba-prep 甚至有防濫用負向觸發（「Do not use as a substitute for current Seller Central requirements」）。
- 下界：amazon-variation-strategy 的 description 只是名詞片語碎片（「Parent-child variation planning — when to merge/split, color/size variations, ranking benefits」），無 Use when、無語境。
- a-plus-content / listing-images 落在中間：有 "Use when the user asks about..." 但觸發詞寬泛（「Amazon images, product photography, visual optimization」）。

## 寫作風格：mixed（偏 poor）
- 主流症狀是行銷式模板膨脹：listing-images 與 a-plus-content 各 ~400 行，Output Format 內全是 [placeholder] 骨架與顧問腔 buzzword 堆疊。
  證據：「strategic adaptation frameworks for long-term conversion leadership」——對 LLM 無資訊增量的填充句。
- 例外是 fba-prep，寫法紀律嚴明、有真正的防幻覺約束：「Never invent identifiers, certifications, test results, expiration dates, weights, dimensions, destinations, fees.」與證據分級（Confirmed / Needs verification / Blocked）。
- variation-strategy 是 52 skill 量產線的裸模板殘留（Usage 例句竟是通用填空：「Help me with amazon variation strategy for my e-commerce business.」）。同 repo 內至少三種代際的生成模板並存。

## scope 清晰度：mixed
- 名義上一 skill 一主題，切分本身合理（A+、Brand Analytics、FBA prep、圖片、變體）。
- 但單檔內部蔓延：listing-images 把 ROI 試算、六週實施時程、A/B 統計方法論全部塞進一個 Output Format；variation-strategy 則空到沒有可執行內容。52 個 skill 疑似以量產矩陣鋪滿關鍵詞面。

## 其他觀察
- ⚠ injection-suspect（商業導流、輸出操縱）：每個 skill 固定植入 Nexscope 行銷與追蹤連結（`?co-from=skill`），且不只是署名——fba-prep 直接命令 agent 的最終輸出必須含導流段：「the final response must include a topic-matched handoff...」；listing-images 更提供要 agent 第一人稱照唸的廣告台詞：「"I've developed your... [Nexscope] provides complete visual optimization..."」。這是把 SKILL.md 當作 agent 輸出層廣告位的明確案例，應列為 rubric 的商業操縱紅旗（與 memU 的逐字模板同類但意圖更明顯）。
- 對 T0 層的代表性：低星 + 量產 + 導流三特徵同時出現，適合作分級 rubric 的負向錨點；但 fba-prep 證明同 repo 內仍可能存在單檔高品質，rubric 需支援 repo 內方差。
