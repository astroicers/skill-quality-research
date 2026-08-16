# jezweb/claude-skills（T0 / D / 968★）

## 抽讀樣本
- plugins/dev-tools/skills/ux-audit/SKILL.md
- plugins/frontend/skills/react-native/SKILL.md
- plugins/integrations/skills/elevenlabs-agents/SKILL.md
- plugins/integrations/skills/google-apps-script/SKILL.md
- plugins/writing/skills/resume-cover-letter/SKILL.md

## trigger 設計：good
- 一律「Use when/whenever」+ 引號觸發語清單。證據：「Use whenever the user mentions ElevenLabs, building a voice agent, an AI phone system…」；google-apps-script 連錯誤情境都當觸發（「troubleshooting deprecated @11labs packages, webhook errors」）。
- ux-audit 的 description 極長（塞入 verdict 規則、hard gates 摘要），資訊量高但逼近 1024 字元上限，是「description 當 spec 用」的邊界案例。

## 寫作風格：good
- Problem/Fix 表格 + 解釋 why：「Functions ending with _ are private… This is a silent failure — the call simply doesn't work with no error」；「The difference is 70x」（batch 讀寫）。
- 有版本漂移意識：「Model lineups and pricing rot fast — check the live list… don't hardcode a model id you haven't verified this session」——罕見的抗過期寫法。
- ux-audit 用可驗證機制取代口號：Interaction Manifest、audit-the-audit 時間戳合理性檢查（「median gap < 0.5s = Incomplete (didn't actually interact)」）、獨立 sub-agent self-critique——直接對抗 LLM「假裝做完」失敗模式。

## scope 清晰度：good
- 一 skill 一 job，plugin 分類清楚；ux-audit 龐大但仍是單一 job（互動式稽核），關鍵路徑 inline、選讀材料在 references/。

## 其他觀察
- CLAUDE.md 明文推翻 500 行上限教條（「a working skill that's 800 lines beats a broken skill that's 300 lines with critical content in references the agent never reads」），並附實測失敗案例——與 anthropics/vercel 的 progressive-disclosure 教義直接衝突，是 rubric「SKILL.md 長度」門檻常數的重要反方證據。
- T0 星數但工程品質達 T2+ 水準，支持「星數≠品質」的分層假說。無 injection 疑慮。
