# K-Dense-AI/scientific-agent-skills(T2/D/33629)

## 抽讀樣本
- skills/gtars/SKILL.md
- skills/imaging-data-commons/SKILL.md
- skills/neurokit2/SKILL.md
- skills/statistical-power/SKILL.md
- skills/tamarind/SKILL.md

## trigger 設計:good
五份全部有觸發語且語境極具體。statistical-power 是本批最佳範例:「Use whenever someone asks "how many subjects/samples/replicates do I need"…even when the request only mentions an effect size…without saying "power analysis" explicitly」,並在 description 內做跨 skill 消歧(「For laying out the study…use experimental-design」)。imaging-data-commons:「even when the user doesn't explicitly mention "IDC"」。neurokit2 用程式碼觸發(「Trigger when code imports neurokit2」)並加負向排除(「not for diagnosis or device validation」)。適度 pushy,不過度。

## 寫作風格:good
imperative + 幾乎每條禁令都附 why:post-hoc power「is circular: it is a deterministic function of the p-value」;下載參數順序陷阱「This is the most common source of broken IDC code」;tamarind 逐一標注 foot-gun(「a plain string value is treated as inline file content」)。有 dated verified snapshot(「Verified snapshot (2026-07-23)」)與 migration traps 段防 stale API 幻覺。gtars/neurokit2 的 supply-chain 與 data-contract 段落密度極高,對 LLM 消費者偏重,但每條均有機制理由,非空洞 MUST 堆疊。

## scope 清晰度:good
一 skill 一工具/方法域(gtars、IDC、NeuroKit2、power analysis、Tamarind 平台),並有顯式邊界宣告:neurokit2 的「Boundary」段(不得作為診斷/法規證據)、statistical-power 的 Related skills 路由。references/ 按需載入的 progressive disclosure 徹底(gtars 列明「These are the only six bundled references」)。

## 其他觀察
- 本 repo 展現「anti-hallucination 工程化」模式:固定版本快照+日期、stale API 名單、「fetch live sources, don't rely on a stale copy」,可作為 rubric 的高階特徵候選。
- neurokit2 有「Security note」教 agent 將掃描器 eval/exec 報告確認後記為 false positive——屬防禦性說明,非 injection。
- 無 injection-suspect 內容。
