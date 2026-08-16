# browser-act/skills(T1 / D / 5334★,103 個 SKILL.md)

## 抽讀樣本
- solutions/ecommerce/1688-product-detail/SKILL.md
- solutions/ecommerce/etsy-shop-catalog/SKILL.md
- solutions/ecommerce/taobao-product-reviews/SKILL.md
- solutions/social-listening/xiaohongshu-auto-posting/SKILL.md
- solutions/social-listening/xiaohongshu-search-full/SKILL.md

## trigger 設計:mixed
形式上全有「Use when user mentions…」,但實作是關鍵字轟炸:1688 那份塞了 20+ 個變體(「1688 offer, 1688 detail, extract 1688 data, pull 1688 listings…」),etsy 份還加「Also applies to…any paginated bulk collection」,屬 recall 最大化的 SEO 式 stuffing——觸發面過寬、可能與同 repo 其他 102 個 skill 互相搶匹配。優點是雙語觸發詞(「采集淘宝商品评价」)確實對應真實用語。

## 寫作風格:good
全 repo 用同一嚴格模板(Objective / Prerequisites / Capability Components / Enum Parameters / Pagination / Success Criteria / Known Limitations / Execution Efficiency / Experience Notes),每個能力附完整 JSON 輸出例與 error handling,Success Criteria 是可判定的斷言(「result.error === false && result.count >= 1」)。禁令附 why:「eval hangs (~30 s timeout) when the callback causes a page redirect」。誠實標注採集失敗欄位(「[collection failed]」),Known Limitations 具體到 DataDome/lazy-load 行為。

## scope 清晰度:good
每 skill = 一個站點 × 一種頁面/操作(1688 詳情頁、Etsy 店鋪目錄、淘寶評論),邊界宣告明確(「this Skill covers detail pages only」)。xiaohongshu-auto-posting 是例外的多階段 workflow(選題→寫作→發布→追蹤),仍算單一 job 但顆粒度明顯大於其他份。

## 其他觀察
- 無 injection 式文字。但兩點值得記錄:(1)「Experience Notes」機制要求 agent 讀取並遵循工作目錄下的 memory 檔(browser-act-skill-forge-memories/*.md)來「調整策略順序」——這是一條未經驗證內容影響 agent 行為的間接通道,rubric 可列為供應鏈注意面;(2) 各 skill 反覆宣稱操作邊界=「使用者手動可及、等同代為複製貼上」,同時提供 stealth browser/反反爬指引,合規敘述與實際能力間存在張力。
