# Jeffallan/claude-skills（T2 / taxonomy D / 11,030 stars）

## 抽讀樣本
- skills/cli-developer/SKILL.md
- skills/laravel-specialist/SKILL.md
- skills/prompt-engineer/SKILL.md
- skills/react-expert/SKILL.md
- skills/vue-expert/SKILL.md

## trigger 設計：good
- 全部遵循 repo 自訂標準「[Brief capability statement]. Use when [triggering conditions]」，且 CLAUDE.md 明文論證了「Description Trap」：description 含流程步驟會讓 agent 抄捷徑不讀正文——這是對 trigger 設計有 meta 認知的 repo。
- 觸發條件落到具體技術訊號：「Use when building React 18+ applications in .jsx or .tsx files, Next.js App Router projects」。
- 另備 metadata.triggers 關鍵詞欄輔助檢索。瑕疵：react-expert 的 description 以 Use when 開頭、能力陳述在後，與自家格式順序相反，執行紀律未達 100%。

## 寫作風格：mixed
- 高度模板化：每檔固定 persona 開場（「Senior React specialist with deep expertise...」）+ Core Workflow(5 步) + Reference 路由表 + MUST DO / MUST NOT DO + Output Templates。一致性極好，但 MUST 清單多為裸斷言、少講 why。
  證據：「MUST NOT DO: Mutate state directly / Use array index as key / Skip error boundaries in production」（無任何解釋）
- 部分條目有補救：cli-developer 的 MUST NOT 附三語言 TTY 偵測代碼；workflow 步驟嵌入驗證命令與失敗迴路（「run php artisan test before considering any step complete」）。
- 範例代碼真實可跑（Pest 測試、React 19 useActionState），品質中上；整體是「工整但偏 checklist 堆疊」的風格。

## scope 清晰度：good
- 一 skill 一技術棧角色（CLI / Laravel / prompt / React / Vue），progressive disclosure 明確（SKILL.md ~100 行 + references/ 100-600 行分層），CLAUDE.md 給出量化目標「50% token reduction through selective loading」。
- 67 個 skill 的大集合，但抽樣未見互相重疊；related-skills 欄位有交叉引用治理。

## 其他觀察
- 無 injection-suspect。
- 每檔尾部強制 SEO backlink（「Every SKILL.md MUST end with a single canonical Documentation link」），CLAUDE.md 坦承目的是「render as a real <a href> on aggregators for SEO backlinks」——skill 檔案被兼作行銷載體的輕度案例，可作 rubric 的「商業訊號」弱特徵。
- 明文致謝並引用 obra/superpowers 的方法論，屬有 attribution 的衍生集合。
