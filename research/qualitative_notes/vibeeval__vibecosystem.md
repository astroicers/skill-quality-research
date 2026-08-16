# vibeeval/vibecosystem(T0 / C / 526★,341 個 SKILL.md)

## 抽讀樣本
- skills/fullstack-dev/SKILL.md
- skills/github-search/SKILL.md
- skills/math/measure-theory/integration-theory/SKILL.md
- skills/oauth-patterns/SKILL.md
- skills/plan-documentation/SKILL.md

## trigger 設計:mixed → poor
極度不一致。fullstack-dev 有結構化的「TRIGGER when / DO NOT TRIGGER when」清單(正例),但觸發面近乎無限寬(「building todo app, building CRUD app, building real-time app…」)。其餘多數缺觸發語:oauth-patterns 的 description 只是名詞串(「OIDC flows, PKCE implementation, token refresh strategies…」),github-search 只寫「Search GitHub code…via MCP」,integration-theory 是模板句「Use this skill when working on integration-theory problems」——341 個 skill 若多為此類,匹配區分度極低。

## 寫作風格:mixed
落差大到像不同作者/不同管線產物。好的一端:fullstack-dev 有 mandatory workflow、可勾選 checklist、三語言對照範例;plan-documentation 模板完整、規則簡明。壞的一端:integration-theory 出現去虛詞壓縮與 RAG 傾倒痕跡——內文混入教科書索引碎片與盜版來源標記(「[Measure, Integration Real Analysis (... (Z-Library)] Statue in Milan Maria Gaetana Agnesi…」),還有可疑的偽工具指令(「z3_solve.py prove "dominated_convergence"」——Z3 無法如此證明 DCT),典型未經人審的自動生成。oauth-patterns 則是純知識傾倒(整頁程式碼)而非 agent 程序,MUST/程序語言皆缺。

## scope 清晰度:mixed
單看各檔:plan-documentation、github-search、oauth-patterns 的 job 邊界尚可;fullstack-dev 一份塞 13 節+4 references,實為整本後端教科書而非單一 job。repo 層面是 341 個 skill 的百科式 grab-bag(從 OAuth 到測度論),與「skill=可觸發的工作能力」定位偏離,更像知識庫索引。

## 其他觀察
- 無 injection 式文字。
- ⚠ 品質風險(非 injection):integration-theory 內嵌 Z-Library 來源的教科書片段,有版權疑慮;且其「Tool Commands」引用的 runtime.harness 腳本能力宣稱(以 Z3 證明收斂定理)與現實不符,屬幻覺式工具描述。作為 T0 層樣本,「大量自動生成+無人工驗收」的特徵梯度非常明顯,適合當 rubric 低分錨點。
