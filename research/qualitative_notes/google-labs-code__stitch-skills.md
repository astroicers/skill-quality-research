# google-labs-code/stitch-skills（T1 / D / 8,060★）

## 抽讀樣本
- plugins/stitch-build/skills/react-native/SKILL.md（讀取經工具壓縮，引文取可確認段落）
- plugins/stitch-build/skills/remotion/SKILL.md
- plugins/stitch-design/skills/manage-design-system/SKILL.md
- plugins/stitch-design/skills/upload-to-stitch/SKILL.md
- plugins/stitch-utilities/skills/taste-design/SKILL.md

## trigger 設計：mixed
- 多數 description 是能力陳述，無「Use when」句式（remotion：「Generate walkthrough videos from Stitch projects…」）。
- upload-to-stitch 有「ALWAYS use this skill when… particularly when direct MCP tool calls fail or truncate」——語境具體但 ALWAYS 偏 pushy。品質在同 repo 內不一致。

## 寫作風格：mixed
- react-native 走 GATE/MANDATORY/PROHIBITED 重規訓風（「CRITICAL: Every step in skill MANDATORY. Do NOT skip」+ 每 phase 的 ❌ anti-pattern 清單），部分有 why（AI fetch 對 GCS 網域會失敗所以必須用 script），但 MUST 密度高。
- remotion 反而是人類教程口吻（「Recommended: Familiarity with Remotion's video capabilities」），偏文件而非 agent 指令，兩者風格割裂。
- 亮點：design 系 skill 有制度化 HITL checkpoint（「Before uploading, you MUST pause and ask the user for confirmation」）與精準 API 陷阱說明（selectedScreenInstances 不能帶 x/y/width/height 否則 invalid argument）。

## scope 清晰度：good
- plugin 分層（build/design/utilities）+ 一 skill 一 job（轉 RN、產影片、管理 design system、上傳資產、產 DESIGN.md），互相引用時明確指名所在 plugin。

## 其他觀察
- ⚠ 安全面（非 injection）：upload-to-stitch 指示 agent 讀取各 harness 的 MCP 設定檔（`~/.claude.json`、`~/.gemini/settings.json`）萃取 API key，並以 `--api-key <API_KEY>` 命令列參數傳遞——憑證出現在 argv/shell history，與 vercel-labs 明文禁止的模式相反，可作 rubric 安全維度的對照組。
- taste-design 全篇 BANNED 清單（No Inter、no purple neon、no fake metrics），偏 opinionated 設計律法；「no fabricated data」條款本身是好的反幻覺規則。
