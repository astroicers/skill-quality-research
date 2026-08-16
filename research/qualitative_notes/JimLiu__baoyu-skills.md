# JimLiu/baoyu-skills(T2 / D / 25039★)

## 抽讀樣本
- .claude/skills/release-skills/SKILL.md
- skills/baoyu-cover-image/SKILL.md
- skills/baoyu-danger-x-to-markdown/SKILL.md
- skills/baoyu-diagram/SKILL.md
- skills/baoyu-post-to-weibo/SKILL.md

## trigger 設計:good
五份全部有明確、雙語化的觸發語,且列舉具體 utterance 而非抽象領域:「Use when user says "release", "发布", "new version"…」「Use when user asks to "post to Weibo", "发微博"…」。baoyu-diagram 的 description 最長,除觸發語還定義輸出契約(「Output is always a standalone .svg file」)。pushy 程度適中——關鍵字多但都是真實同義觸發詞,非 SEO 堆疊。

## 寫作風格:good
Imperative 工作流(Step 0–5、Progress Checklist)、大量表格、輸出範例具體。禁令幾乎都附 why:「Never kill all Chrome processes…The user may have regular Chrome windows open」;x-to-markdown 的 consent flow 把風險逐條列給使用者。扣分點:⛔/⚠️/CRITICAL/BLOCKING 標記密度偏高,cover-image 的 backend 解析規則(Codex/Cursor/fallback 五層)閱讀負擔大。

## scope 清晰度:good
每 skill 一個 job(發版/封面圖/推文轉檔/SVG 圖表/發微博),並用 references/ 子檔做 progressive disclosure(auto-selection、prompt-template 等按需載入)。repo 以 CLAUDE.md 明文規定「skill 自包含、不得外連 repo 級文件」,故 User Input Tools 等 boilerplate 在每份 SKILL.md 刻意重複——是有意識的架構取捨而非失控複製。

## 其他觀察
- 無 injection 疑慮;x-to-markdown 明示使用逆向工程 X API 並強制 consent 檔,風險揭露做得規範。
- EXTEND.md 三層偏好檔(project/XDG/home)+ 首次設定 BLOCKING gate,是本批次最成熟的「skill 個人化設定」機制,可作 rubric 特徵。
