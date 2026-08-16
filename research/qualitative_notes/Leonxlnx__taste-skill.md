# Leonxlnx/taste-skill(T2 / B / 76977★)

## 抽讀樣本
- skills/brutalist-skill/SKILL.md
- skills/gpt-tasteskill/SKILL.md
- skills/imagegen-frontend-mobile/SKILL.md
- skills/stitch-skill/SKILL.md
- skills/taste-skill-v1/SKILL.md

## trigger 設計:poor
五個樣本的 description 全數缺乏 Use when / trigger 語式,多為風格形容詞堆疊(「Elite UX/UI & Advanced GSAP Motion Engineer. Enforces Python-driven true randomization…」)或適用場景的名詞片語(「For data-heavy dashboards, portfolios, or editorial sites」)。taste-skill-v1 的 description 甚至只講版本相容性(「preserved for projects depending on its exact behavior」),完全不含觸發語境。imagegen-frontend-mobile 有寫「This skill is for / not for」清單,但放在 body 而非 description。

## 寫作風格:mixed
高度 opinionated、規則密集,部分有 bias-correction 的 why(「LLMs have statistical biases toward specific UI cliché patterns」),範例具體到 class 名與 hex 值,這是優點。但缺點顯著:(1) ALL-CAPS 禁令堆疊(「BANNED FOREVER」「strictly BANNED」「catastrophic failure」)遠多於解釋;(2) brutalist-skill 整份做了去虛詞壓縮,連 description 都不成句(「interfaces fusing Swiss typographic print military terminal aesthetics」),犧牲可讀性;(3) gpt-tasteskill 要求模擬 Python RNG 的儀式性步驟,屬 cargo-cult prompt 技巧。

## scope 清晰度:good
每個 skill 對應一種明確 deliverable(brutalist UI / GSAP landing page / mobile 截圖生成 / Stitch DESIGN.md / v1 相容包),且 imagegen 類明確宣告「generates images only. It does not write code」。repo 層面各 skill 間有審美規則大量重複(Inter ban、#000000 ban、min-h-[100dvh] 等在 3+ 份出現),維護面有 drift 風險,但單 skill 的 job 邊界清楚。

## 其他觀察
- 無 injection 疑慮。
- 「dial 設定檔」模式(DESIGN_VARIANCE: 8 等 1–10 刻度)在多份 skill 重複出現,是此 repo 的特色機制,對 rubric 的「參數化風格控制」是一個可觀察特徵。
