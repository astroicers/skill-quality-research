# tt-a1i/archify(T2 / B / 13108★)

## 抽讀樣本
- archify/SKILL.md

## trigger 設計:good
description 有完整觸發語且枚舉具體場景:「Use when the user asks to visualize system architecture, infrastructure, cloud/security/network topology…or to convert/beautify Mermaid」,並描述輸入形態(plain-language 或貼上的 Mermaid)。範圍寬但均為真實能力,搭配 body 的 Type router 表分流五種圖型,pushy 程度合理。

## 寫作風格:mixed
Imperative 且紀律極強,verification 文化突出:「A non-zero exit can never be described as success」「Never counterfeit a pass with overflow: hidden, clipped content…」,並限制修復迴圈(兩輪無進展即誠實回報)。但可讀性受害於超長單段 invariant——desktop-viewer 一段近 300 詞塞入視窗尺寸、scrollWidth 斷言、修復順序等十餘條規則,無小標或列表切分;部分規則(Automatic Port Spread 的 16px/8px 幾何細節)放在主檔而非 references,與其自己宣示的 bounded reading path 相悖。

## scope 清晰度:good
一個 job:產出經驗證的自包含 HTML 圖表。用「Fast authoring path 只讀 schema+example、禁止先讀 renderer 原始碼」明確控制 agent 的探索邊界,references/*.md 按需載入,job-to-be-done 單一且交付物(validate→deliver→visual-check)定義清楚。

## 其他觀察
- 無 injection 疑慮。
- 「validate/deliver 雙命令 + SHA-256 receipt + 凍結 spec」的反造假設計(不准事後改已驗證檔案、不准宣稱未做過的 visual review)是本批次最強的 anti-hallucination 機制,建議進 rubric 的 verification 維度。
