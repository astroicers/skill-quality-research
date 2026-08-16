# Taxonomy 回填 stage-2 提案(G1 裁決 2 之 LLM/人工覆核段)

- stage-1(deterministic,`backfill_taxonomy.py`)已定案:**14 筆 B**(1 個合規 SKILL.md)
- 本檔為 stage-2 LLM 判讀提案,**待人工核可後才寫入 repos.json**
- 判定測試(F vs C/D):「刪掉 skills 後 repo 還是不是產品?刪掉軟體後 skills 能不能獨立成立?」
  服務方向:code 服務 skills → C/D;skills 服務 code → F

## C 類(框架/方法論:多 skill 組成工作流)— 6 筆

| repo | 理由 |
|------|------|
| calesthio/OpenMontage | 12 條 production pipeline 由 138 個 skill 組成 agentic 影片工作流,skills 即產品 |
| AgriciDaniel/claude-obsidian | 16 skills 組成「第二大腦」單一工作流(ingest→link→file) |
| AgriciDaniel/claude-ads | 跨 12 平台的 paid-media 作業方法論,ads-math/attribution 等為同一工作流組件 |
| jnMetaCode/superpowers-zh | superpowers(C 類框架)完整漢化 + 6 原創,繼承框架性質 |
| vibeeval/vibecosystem | 138 agents + 295 skills 組成 dev process swarm,code(148)遠少於 skill(341) |
| tobihagemann/turbo | 自述「composable dev process packaged as modular skills」,教科書 C |

## D 類(集合:獨立 skill library)— 13 筆

| repo | 理由 |
|------|------|
| kepano/obsidian-skills | 5 個獨立 Obsidian 格式 skill,零 code |
| vercel-labs/agent-skills | 官方 skill 集合,各自獨立(react/vercel/writing) |
| phuryn/pm-skills | 68 個獨立 PM skill,code 僅 3 檔 |
| KKKKhazix/khazix-skills | 6 個獨立 skill 合集 |
| google/skills | 111 個按產品分類的獨立 skill |
| muratcankoylan/Agent-Skills-for-Context-Engineering | 主題式知識 skill 庫,非工作流 |
| earthtojake/text-to-cad | 自述 library;code 內嵌於各 skill 目錄服務該 skill(方向:code 服務 skill) |
| Orchestra-Research/AI-Research-SKILLs | 98 個研究 skill,編號目錄僅為分類 |
| Jeffallan/claude-skills | 66 個獨立全端 skill |
| google-labs-code/stitch-skills | skill library(MCP server 在別的 repo) |
| jezweb/claude-skills | plugins/* 獨立 skill 包 |
| nexscope-ai/Amazon-Skills | 52 個獨立賣家 skill |
| tamdogood/builder-essential-skills | 個人日常 skill 集 |

## F 類(工具/harness:主體是軟體)— 16 筆 → `in_rubric_sample=false`

| repo | 理由(code 檔數) |
|------|------|
| CherryHQ/cherry-studio | AI 桌面應用(4172),skills 是產品內建資源 |
| nanocoai/nanoclaw | OpenClaw 替代品容器產品(491),skills 是 add-integration 入口 |
| googleworkspace/cli | 官方 CLI 產品,skills 教 agent 用 CLI(刪 skills 產品仍在) |
| topoteretes/cognee | AI memory 平台(2328),skills 是使用入口 |
| alibaba/open-code-review | code review 工具(372),2 skill 為入口 |
| mksglu/context-mode | context 優化工具(423),ctx-* skills 是指令面 |
| kubesphere/kubesphere | 容器平台(10316),skills 為平台管理面 |
| larksuite/cli | 官方 CLI 產品(2364),同 googleworkspace |
| microsoft/SkillOpt | 優化器研究工具(230),skills 是 plugin 入口 |
| eigent-ai/eigent | 桌面應用(759),example-skills 為示例附件 |
| NVIDIA/SkillSpector | 安全掃描工具,SKILL.md 全是**測試 fixtures** |
| aden-hive/hive | multi-agent harness(1208) |
| nexu-io/html-anything | HTML 編輯器應用,skills 是產品內模板 |
| hoangsonww/Claude-Code-Agent-Monitor | 監控 dashboard 應用(278),skills 是自家開發用 |
| reticlehq/reticle | runtime 感知工具(1217),skills 包裝產品 |
| crabbuild/compass | Rust 知識圖譜引擎(882),僅 2 skill |

## 排除候補定案 — 10 筆 → `in_rubric_sample=false`

| repo | 判定 | 理由 |
|------|------|------|
| agentskills/agentskills | E | Agent Skills 開放規格文件本身,無實體 skill(仍為 §10 參考基準) |
| liyupi/ai-guide | E | 資源大全/教程(90.6% md),目錄類 |
| alibaba/zvec | F | 向量資料庫,description 含關鍵詞誤入樣本 |
| xixu-me/xget | F | 加速引擎,誤入樣本 |
| bawadou/claude-engineer | F | CLI 框架,無 SKILL.md |
| jiweiyeah/Skills-Manager | F | skill 管理桌面應用(managing ≠ being skills) |
| simonw/claude-skills | E | /mnt/skills 內容的指向性 dump(clone 僅 2 檔) |
| Shanyin-ai/shanyin-screenwriting-master | E | README 型 prompt 說明,無 SKILL.md/CLAUDE.md 載體,非 v1.2.1 例外 |
| Austin1serb/Anthropic-Leaked-Source-Code | F | 洩漏源碼 dump(1350 code),非 skill repo |
| 24kchengYe/human-skill-tree | E? | 68 個 SKILL.md **全部無 frontmatter**(標題式 Markdown);CLAUDE.md 非行為框架,不落 v1.2.1 例外。**必須進 patterns-report §3 反模式**:T0 層「有 SKILL.md 之形、無規格之實」的典型標本 |

## 人工項 — 1 筆

| repo | 處置 |
|------|------|
| yschimke/compose-ai-tools | 1.5GB 超限未 clone,無靜態證據;維持 TBD + `no-clone` 註記,不進特徵矩陣(BRIEF 規定跳過並記錄) |

## 套用後樣本剖面(提案)

- rubric 樣本:82 → **56**(−16 F、−10 排除;compose-ai-tools 無特徵列,實際可分析 55)
- taxonomy 全定案:A:1 / B:19(5+14) / C:14(8+6) / D:21(8+13) / E+E?+F:41 / TBD:1(no-clone)
- **注意**:T2 層將因 F 類產品 repo 大量出列而顯著縮小——熱潮期高星「skill repo」有相當比例
  實為帶 `.claude/skills/` 的軟體產品,此現象本身是 patterns-report §4/§5 的素材
