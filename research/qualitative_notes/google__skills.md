# google/skills(T2/D/18375)

## 抽讀樣本
- skills/cloud/agent-platform-inference/SKILL.md
- skills/cloud/cloud-logging-query-generation/SKILL.md
- skills/cloud/gke-inference/SKILL.md
- skills/cloud/gke-multitenancy/SKILL.md
- skills/cloud/google-cloud-waf-performance-optimization/SKILL.md

## trigger 設計:good
五份全部 Use when + 負向排除,格式高度一致(官方模板):gke-inference「Use when deploying GKE inference servers…Don't use for generic batch jobs (use gke-batch-hpc instead)」;gke-multitenancy「Don't use for single-tenant…(use gke-basics instead)」;agent-platform-inference 甚至把觸發語境細到錯誤碼(「troubleshoot 429 Resource Exhausted (DSQ), 400…, or 404」)。負向排除都指名替代 skill,是本批最工整的觸發設計。

## 寫作風格:good
imperative,強調 why 與精確操作。agent-platform-inference 的 region 探測段是亮點:「Do not rely on Google Search or training-corpus knowledge for availability claims — regional availability changes frequently and grounded text can be stale」,並逐一定義 200/404/其他狀態碼的處置。cloud-logging 對 placeholder 陷阱解釋透徹(「a placeholder acts as an explicit filter that causes logs to be missed…MUST omit the entire filter line」)。有 MUST/CRITICAL 但都掛具體後果。gke-inference 的加速器選型表、troubleshooting 表資訊密度高且可操作。

## scope 清晰度:good
一 skill 一雲端任務域,且以「MCP Tools / CLI-only」開頭聲明可用工具面,邊界明確。skill 間互相指名交接(gke-multitenancy → gke-platform-security / gke-workload-security;agent-platform-inference → agent-platform-deploy),形成清晰的官方 skill 網而非重複。progressive disclosure 徹底:cloud-logging 把 20+ 服務 schema 拆到 references/query_*.md 並要求「you MUST read the specific service file before generating」。

## 其他觀察
- agent-platform-inference 內建「Safety & Confirmation Tiers」:即使唯讀 inference 也要求 interactive Yes/No 確認並禁止同回合執行——展示成本/配額防護的 HITL 模式,可作 rubric 的安全機制候選。
- 官方 repo,模板化程度高;略有重複粘貼瑕疵(agent-platform-inference 有一段 TIP 文字重複兩次),但不影響判讀。
- 無 injection-suspect 內容。
