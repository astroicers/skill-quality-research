# alirezarezvani/claude-skills(T2/D/24496)

## 抽讀樣本
- .gemini/skills/c-level-agents/SKILL.md
- .gemini/skills/cmo-advisor/SKILL.md
- .gemini/skills/pricing-strategist/SKILL.md
- .gemini/skills/security-pen-testing/SKILL.md
- .gemini/skills/terraform-patterns/SKILL.md

## trigger 設計:good
四份具體、一份(c-level-agents)偏弱。pricing-strategist 最佳:「Use when designing or revisiting product pricing…selecting a pricing model…running Van Westendorp PSM…」+ 明確負向排除(「not deal-by-deal discounting, not brand positioning」)。cmo-advisor、terraform-patterns、security-pen-testing 皆有 Use when + 觸發語句列舉。c-level-agents 的 description 偏功能清單(「13 cs-* agents…21 /cs:* commands」),Use when 較泛。

## 寫作風格:good
imperative + 決策導向,幾乎每個 skill 都有 Anti-patterns 段解釋「為何不要」而非只列 MUST:pricing 的「Recommending a specific number…final price is a human commercial decision」、cmo 的「'companies with 50-1000 employees' is not an ICP」。canon citation 掛在每條 forcing question(「Canon: Ramanujam 2016, Mistake #1」),範例品質高。security-pen-testing 的攻擊 payload 屬合法範疇內容,並前置「written authorization is mandatory」與 CFAA 警示。

## scope 清晰度:good
每 skill 一決策域並顯式互相消歧:pricing-strategist 的「Distinct from」段逐一切開 deal-desk/cmo-advisor/cro-advisor/sales-engineer;security-pen-testing 有四路 skill 對照表(offensive vs defensive vs governance vs CI gate)。c-level-agents 是刻意的 orchestrator(包裝 13 個既有 skill),邊界清楚。這是本批 scope 消衷做得最系統化的 repo(362 skills 規模下仍維持自我區分)。

## 其他觀察
- CLAUDE.md 極端龐大(數千行,幾乎全是版本 changelog),對「repo 治理文件」是反模式;但單 skill 本身簡潔,符合其自訂的「keep each self-contained」原則。
- 展現工程化品質基建:write-a-skill 6-item checklist、`scripts/audit_skills.py` 全庫掃描、description validator——這些是可作 rubric 高階特徵的「後設治理」訊號。
- 無 injection-suspect;security-pen-testing 的 payload/攻擊字串均為被分析的安全教學內容,已加授權門檻。
