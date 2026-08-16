# anthropics/skills(T3 / A / 169634★)

## 抽讀樣本
- skills/canvas-design/SKILL.md
- skills/claude-api/SKILL.md
- skills/frontend-design/SKILL.md
- skills/internal-comms/SKILL.md
- skills/theme-factory/SKILL.md

## trigger 設計:mixed
同 repo 內落差極大。claude-api 是全批次最工程化的 trigger:description 內建 TRIGGER/SKIP 雙向規則與先決 grep(「SKIP only when another provider is being worked on」),適度 pushy 且有明確退場條件。canvas-design 與 internal-comms 有標準觸發語(「You should use this skill when the user asks to create a poster」/「use this skill whenever asked to write some sort of internal communications」)。但 frontend-design 與 theme-factory 的 description 純描述性、無任何 Use when 觸發語(「Guidance for distinctive, intentional visual design…」),依賴平台自動載入語境。

## 寫作風格:good
主體是 imperative + 解釋 why 的混合,少見無理由的 MUST 堆疊。frontend-design 品質最高:給校準知識而非禁令(「AI-generated design right now clusters around three looks…they are defaults rather than choices」)。claude-api 用表格解釋 API drift 的「stale prior → current」理由。缺點:canvas-design 靠形容詞轟炸與重複催眠(「repeat phrases like "meticulously crafted"」),且 theme-factory 有明顯 typo(「color themes themes」「has been creating」),顯示官方 repo 內品質不均。

## scope 清晰度:good
每個 skill 一個 job:canvas-design=靜態視覺藝術、theme-factory=套主題、internal-comms=內部溝通文件(router 式分派到 examples/*.md)。claude-api 域廣(API 參考+migrate+prompt-audit 子命令)但仍是「寫 Claude API 程式」單一 job,並用 {lang}/ 與 shared/ 檔案做 progressive disclosure。

## 其他觀察
- canvas-design 有一段偽造使用者發言的操縱式 prompt:「The user ALREADY said "It isn't perfect enough…"」——不是針對分析者的 injection,但屬於值得 rubric 關注的 manipulation pattern(以假對話歷史提高輸出品質)。
- internal-comms 以第一人稱「help me write」撰寫,是個人化 skill 範本;與其他 skill 的第三人稱體例不一致。
