# RinDig/icm-architect(T0/B/962)

## 抽讀樣本
- SKILL.md(根目錄單體 skill,全文 111 行)

## trigger 設計:good
- description 枚舉 6 種具體使用情境 + 使用者原話:「says "make this an ICM", "ICM this", "map this repo", "audit this folder", "what would a change hit"」。語境具體、不過度 pushy。

## 寫作風格:good
- imperative + 罕見地重視 why:library/catalog 隱喻解釋整套設計、十條 invariants 各附理由(「Renaming folders reorders the pipeline — that is the point」)。
- 有 Guardrails 與誠實的適用邊界:「Know where ICM loses. Real-time multi-agent collaboration... genuinely need framework code」;anti-patterns 來自實際觀察(「seen in the wild」)。
- 驗證機制內建(walk test:cold agent 兩次讀內能定位;token check 2k–8k)。

## scope 清晰度:good
- 一個 job(把流程/知識設計成 ICM workspace),Build/Restructure 兩模式切分清楚,六種 form 用「Reach for it when」表路由;深度內容外移 references/ 與 assets/templates/。
- 「If the whole job fits in one saved prompt, say so and don't build a workspace at all」——主動反過度使用自身。

## 其他觀察
- T0(962 stars)但品質達 T2/T3 樣本水準,是「星數≠品質」的反例樣本,對 rubric 校準有價值。
- 引用來源標註(arXiv:2603.16021, MIT-licensed)。
- 有 1 份 CLAUDE.md(未在樣本內)。無 injection-suspect。
