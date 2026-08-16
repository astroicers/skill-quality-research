# calesthio/OpenMontage(T2/C/48274)

## 抽讀樣本
- .agents/skills/create-video/SKILL.md
- .agents/skills/hyperframes-cli/SKILL.md
- .agents/skills/seedance-2-0/SKILL.md
- .agents/skills/tailwind-design-system/SKILL.md
- .agents/skills/website-to-video/SKILL.md

## trigger 設計:good
- 多數 description 用編號枚舉觸發情境 + 使用者原話:「Use when: (1) Creating a video from a description... (6) User says "make me a video"」。
- website-to-video 是負面觸發的標竿:description 內建 NOT-for 路由表「NOT for: product/SaaS launch (→ /product-launch-video)... Unclear? Ask one question or start at /hyperframes」。
- tailwind-design-system 相對泛用(「Use when creating component libraries...」),是樣本中最弱的一支但仍合格;不見過度 pushy。

## 寫作風格:good
- imperative + 大量表格(routing、red-flag→root-cause 對照、Don't/Why);解釋 why 而非裸 MUST:「no 3D, no cartoon — counter-intuitive but forces photoreal skin」。
- 有預堵 rationalization 的段落:「If you find yourself reasoning "auto mode says bias toward action, so I'll skip X"... that reasoning is wrong」。
- 驗證紀律強:post-render verification、「Honest disclosure: "What I did NOT verify" must appear」。tailwind 那支偏大段 code dump(400+ 行內嵌元件碼),接近 reference 而非行為指引。

## scope 清晰度:good
- 每支一個 job,且有明確的 skill 間互斥/交接:「When to Use This Skill vs Avatar Video」對照表、Cross-Skill Hand-Offs 段。
- 138 支 skill 的大倉庫靠 hub-and-spoke 路由(/hyperframes 為總路由)維持邊界;抽到的樣本均未見職責重疊。

## 其他觀察
- ⚠ 供應鏈相關(非 injection):hyperframes-cli 自述「`--skip-skills` flag is currently neutered... every `init` runs this check and pulls our latest skills regardless」——CLI 在 init 時強制從 GitHub 自動更新全域 skills 且暫時無法退出,屬 skill 自我更新通道的風險樣態。
- CLAUDE.md 採極端 gating:「Do not act on the user's request until you have read AGENT_GUIDE.md」,單檔只做轉址;是 progressive disclosure 的另一種形態。
- seedance-2-0 含大量價格/Elo/日期宣稱(2026-02 發布、$0.3034/s 等),為未驗證外部事實密集型 skill。
- 無 prompt injection 式文字。
