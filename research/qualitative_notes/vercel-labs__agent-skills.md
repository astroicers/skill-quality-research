# vercel-labs/agent-skills（T2 / D / 30,079★）

## 抽讀樣本
- skills/composition-patterns/SKILL.md
- skills/deploy-to-vercel/SKILL.md
- skills/react-best-practices/SKILL.md
- skills/vercel-cli-with-tokens/SKILL.md
- skills/web-design-guidelines/SKILL.md

## trigger 設計：good
- 每個 description 都有「Use when」+ 具體觸發語。證據：「Use when the user requests deployment actions like "deploy my app", "push this live"」（deploy-to-vercel）。
- 觸發語境具體且不 pushy；姊妹 skill（deploy-to-vercel vs vercel-cli-with-tokens）在 description 層就用情境（interactive login vs token auth）區分。

## 寫作風格：good
- imperative + 解釋 why。證據：「Putting secrets in command-line arguments exposes them in shell history and process listings」；「vercel link --repo… more reliable than vercel link, which tries to match by directory name」。
- 決策樹式流程（Step 1 蒐集狀態 → 依狀態選路徑）、含跨 harness 分支（Claude Code / claude.ai sandbox / Codex）與失敗回退。
- 兩個 rules 型 skill（react-best-practices、composition-patterns）採 index+rules/ 的 progressive disclosure：SKILL.md 只放 70 條規則的優先級索引，細節在 rules/*.md，是 D 類的良好範式。

## scope 清晰度：good
- 一 skill 一 job 明確：部署（互動）/部署（token）/React 效能規則/組合模式/UI 審查各自獨立；deploy skill 明確宣告安全預設（「Always deploy as preview unless… explicitly asks for production」「Ask the user before pushing」）。

## 其他觀察
- web-design-guidelines 在執行期用 WebFetch 從 GitHub raw 抓最新規則且「fetched content contains all the rules and output format instructions」——遠端指令載入（remote instruction loading），規則內容不受版本釘選，屬供應鏈/漂移風險模式，rubric 可作為扣分特徵。
- CLAUDE.md 同時是 skill-authoring 指南（500 行上限、progressive disclosure、scripts over inline code），meta 品質高。
