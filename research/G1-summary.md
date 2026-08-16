# G1 Review Summary(Gate G1 — 人工審查用)

- 產生時間:2026-08-16T11:20:38.670291+00:00  mode:api
- 總 repo 數:97;rubric 樣本(A–D):82
- tier 分布:{'T0': 18, 'T1': 12, 'T2': 59, 'T3': 8}
- cohort 分布:{'C0': 13, 'C1': 20, 'C2': 59, 'C3': 5}(切點為提案值,請對照 created_at 分布確認)
- fame 分布:{'F0': 37, 'F1': 27, 'F2': 18, None: 15}
- taxonomy 分布:{'A': 1, 'B': 5, 'C': 8, 'D': 8, 'E': 6, 'E?': 5, 'F': 4, 'TBD': 60}
- domain 分布:{'TBD': 25, 'code-quality': 1, 'design-ui': 20, 'dev-workflow': 12, 'media-gen': 2, 'memory-context': 5, 'meta-tooling': 14, 'research-analysis': 6, 'science': 3, 'security': 3, 'writing-content': 6}
- 純度樣本(F0 且 T2+):19 個 → ['Egonex-AI/Understand-Anything', 'nanocoai/nanoclaw', 'topoteretes/cognee', 'OthmanAdi/planning-with-files', 'titanwings/colleague-skill', 'ayghri/i-have-adhd', 'mksglu/context-mode', 'teng-lin/notebooklm-py', 'muratcankoylan/Agent-Skills-for-Context-Engineering', 'eigent-ai/eigent', 'wanshuiyin/Auto-claude-code-research-in-sleep', 'NevaMind-AI/memU', 'earthtojake/text-to-cad', 'tt-a1i/archify', 'Orchestra-Research/AI-Research-SKILLs', 'citrolabs/ego-lite', 'nidhinjs/prompt-master', 'Jeffallan/claude-skills', 'aden-hive/hive']

## 資料完整度(BRIEF §4 去混淆三道工序的前提)

| 欄位 | 落地率 | 抓取失敗原因 |
|------|--------|--------------|
| `author_followers` | 82/82 (100.0%) | — |
| `prior_fame_proxy` | 81/82 (98.8%) | not-searchable×1 |
| `author_fame_tier` | 82/82 (100.0%) | — |
| `contributor_count` | 82/82 (100.0%) | — |
| `nonauthor_pr_count` | 82/82 (100.0%) | — |
| `fork_star_ratio` | 82/82 (100.0%) | — |

- ✅ **工序1_素人復現** — 需要 author_fame_tier;覆蓋率 100.0%;純度樣本 19 個
- ✅ **工序2_雙結果變數** — 需要 fork_star_ratio + contributor_count + nonauthor_pr_count;覆蓋率 100.0%
- ✅ **工序3_機制陳述** — 需要 LLM 判讀,無資料依賴

## 待人工定案(TBD / 啟發式標籤)
- Shubhamsaboo/awesome-llm-apps
- mvanhorn/last30days-skill
- CherryHQ/cherry-studio
- calesthio/OpenMontage
- kepano/obsidian-skills
- github/awesome-copilot
- blader/humanizer
- nanocoai/nanoclaw
- googleworkspace/cli
- vercel-labs/agent-skills
- topoteretes/cognee
- vercel-labs/skills
- phuryn/pm-skills
- agentskills/agentskills
- op7418/guizang-ppt-skill
- titanwings/colleague-skill
- alibaba/open-code-review
- mksglu/context-mode
- KKKKhazix/khazix-skills
- teng-lin/notebooklm-py
- liyupi/ai-guide
- google/skills
- muratcankoylan/Agent-Skills-for-Context-Engineering
- kubesphere/kubesphere
- larksuite/cli
- microsoft/SkillOpt
- alibaba/zvec
- eigent-ai/eigent
- NVIDIA/SkillSpector
- travisvn/awesome-claude-skills
- NevaMind-AI/memU
- earthtojake/text-to-cad
- tt-a1i/archify
- Orchestra-Research/AI-Research-SKILLs
- citrolabs/ego-lite
- nidhinjs/prompt-master
- Jeffallan/claude-skills
- AgriciDaniel/claude-obsidian
- aden-hive/hive
- BehiSecc/awesome-claude-skills
- nicobailon/visual-explainer
- nexu-io/html-anything
- xixu-me/xget
- AgriciDaniel/claude-ads
- google-labs-code/stitch-skills
- kangarooking/cangjie-skill
- jnMetaCode/superpowers-zh
- rohitg00/awesome-claude-design
- jezweb/claude-skills
- RinDig/icm-architect
- bawadou/claude-engineer
- jiweiyeah/Skills-Manager
- simonw/claude-skills
- hoangsonww/Claude-Code-Agent-Monitor
- Shanyin-ai/shanyin-screenwriting-master
- nexscope-ai/Amazon-Skills
- axtonliu/smart-illustrator
- Austin1serb/Anthropic-Leaked-Source-Code
- 24kchengYe/human-skill-tree
- vibeeval/vibecosystem
- tobihagemann/turbo
- reticlehq/reticle
- tamdogood/builder-essential-skills
- crabbuild/compass
- yschimke/compose-ai-tools

## 抽樣方法記錄
```json
{
  "queries": [
    "topic:claude-skills",
    "topic:claude-code-skills",
    "topic:agent-skills",
    "topic:claude-code-plugins",
    "\"claude skills\" in:name,description",
    "\"agent skills\" in:name,description"
  ],
  "pages": 2,
  "range_samples": [
    {
      "tier": "T1",
      "query": "topic:claude-skills stars:1000..9999",
      "n_target": 12,
      "picked": [],
      "method": "interleave(stars-sorted, updated-sorted), dedup, deterministic"
    },
    {
      "tier": "T0",
      "query": "topic:claude-skills stars:100..999",
      "n_target": 10,
      "picked": [
        "nexscope-ai/Amazon-Skills",
        "yschimke/compose-ai-tools",
        "axtonliu/smart-illustrator",
        "reticlehq/reticle",
        "Austin1serb/Anthropic-Leaked-Source-Code",
        "tamdogood/builder-essential-skills",
        "24kchengYe/human-skill-tree",
        "tobihagemann/turbo",
        "vibeeval/vibecosystem",
        "crabbuild/compass"
      ],
      "method": "interleave(stars-sorted, updated-sorted), dedup, deterministic"
    }
  ],
  "search_interval_sec": 3.0,
  "strata_caps": {
    "applied": true,
    "brief_ref": "BRIEF §3 Phase 1(G1 修訂):T3 全收 / T2 全收 / T1 抽 10–12 / T0 抽 15–20",
    "caps": {
      "T3": "全收",
      "T2": "全收",
      "T1": 12,
      "T0": 18
    },
    "priority": "seed > range-sample > main-query(stars desc)",
    "kept_per_tier": {
      "T0": 18,
      "T1": 12,
      "T2": 59,
      "T3": 8
    },
    "dropped_per_tier": {
      "T0": 168,
      "T1": 168
    },
    "dropped_names": {
      "T0": [
        "23blocks-OS/ai-maestro",
        "A-cat-with-carrots/OnlyShot",
        "AKCodez/higgsfield-claude-skills",
        "Abhi24384/Anthropic-Mythos-Desktop-Studio",
        "Abhinavbwj/Claude-skills-for-Computational-Designers",
        "AlpacaLabsLLC/skills-for-architects",
        "Ar9av/PaperOrchestra",
        "Arindam200/cc-lens",
        "Bhanunamikaze/Agentic-SEO-Skill",
        "BrianRWagner/ai-marketing-claude-code-skills",
        "BrownFineSecurity/iothackbot",
        "Cassette-Editor/oh-my-cassette",
        "CesiumGS/cesiumjs-skills",
        "ComPDFKit/compdf-skills",
        "Fokkyp/claude-skills",
        "Frappucc1no/recall-loom",
        "Gabberflast/academic-pptx-skill",
        "GenielabsOpenSource/spine-animation-ai",
        "Houseofmvps/ultraship",
        "ItsssssJack/power-design",
        "JasonColapietro/suede-creator-skills",
        "JayantDevkar/claude-code-karma",
        "JuneYaooo/social-account-doctor",
        "JuneYaooo/xhs-writer-skill",
        "K-Dense-AI/claude-skills-mcp",
        "LeastBit/Claude_skills_zh-CN",
        "LukasNiessen/terrashark",
        "MIKOTOKAWAII25/local-ai-code-assistant",
        "Microck/ordinary-claude-skills",
        "Mrjie7205/serenity-bottleneck-hunter",
        "NTCoding/claude-skillz",
        "NikiforovAll/claude-code-rules",
        "Nyrok/flompt",
        "OneWave-AI/claude-skills",
        "Sushegaad/Claude-Skills-Governance-Risk-and-Compliance",
        "SynaLinks/synalinks-skills",
        "ToluVictor/canvas-apps-tools",
        "UiPath/coder_eval",
        "VikashLoomba/copilot-mcp",
        "Vitorlindo201/Themata-Claude-Scribe",
        "XiaoMaColtAI/math-modeling-skill",
        "YANZHANLIN/ielts-claude-skills",
        "aapersh/strategy-skills-for-claude",
        "aeonfun/soul.md",
        "ahmedasmar/devops-claude-skills",
        "ailabs-393/ai-labs-claude-skills",
        "aldegad/sprite-gen",
        "alirezarezvani/claude-code-skill-factory",
        "alonw0/web-asset-generator",
        "anombyte93/prd-taskmaster",
        "aofp/yume",
        "arbiterForge/codeArbiter",
        "arvindrk/extract-design-system",
        "athola/claude-night-market",
        "avibebuilder/claude-prime",
        "avidevelops/claude-architect-exam-prep",
        "baidu-netdisk/bdpan-storage",
        "bchao1/paper-finder",
        "billy-enrizky/openbrowser-ai",
        "bitjaru/styleseed",
        "bitwize-music-studio/claude-ai-music-skills",
        "borghei/Claude-Skills",
        "boshu2/agentops",
        "cclank/lanshu-awesome-ai-video-kit",
        "chengzhongwei/Prompt-sensei",
        "chenxiachan/xhs-claude-skills",
        "chrisvoncsefalvay/claude-d3js-skill",
        "chujianyun/skills",
        "claude-office-skills/skills",
        "codejunkie99/graph-engineering",
        "coffeefuelbump/csv-data-summarizer-claude-skill",
        "coleam00/second-brain-skills",
        "coreyhaines31/makerskills",
        "damionrashford/RivalSearchMCP",
        "decebals/claude-code-java",
        "dinglebear-ai/unraid",
        "dongshuyan/compass-skills",
        "evanca/flutter-ai-rules",
        "ferdinandobons/startup-skill",
        "fleurytian/awesome-claude-skills",
        "gamedev-skills/awesome-gamedev-agent-skills",
        "gbessoni/seobuild-onpage",
        "gcpdev/llm-council-skill",
        "ginuim/skill-base",
        "giuseppe-trisciuoglio/developer-kit",
        "glebis/claude-skills",
        "haddock-development/claude-reflect-system",
        "haowjy/creative-writing-skills",
        "honnibal/claude-skills",
        "hqhq1025/skill-optimizer",
        "hypnguyen1209/offensive-claude",
        "iKora128/stop-ai-slop-jp",
        "iamzhihuix/happy-claude-skills",
        "indranilbanerjee/digital-marketing-pro",
        "inhouseseo/superseo-skills",
        "instavm/coderunner",
        "instavm/open-skills",
        "intercom/2x-skills",
        "jabrena/plinth",
        "jamditis/claude-skills-journalism",
        "jeecgboot/skills",
        "jherrodthomas/robotics-skills-suite",
        "jwangkun/claude-for-financial-services-cn",
        "kangarooking/x-skills",
        "karanb192/awesome-claude-skills",
        "karanb192/itr-wala",
        "kazukinagata/shinkoku",
        "keskinonur/claude-code-ios-dev-guide",
        "khendzel/skills-janitor",
        "laolaoshiren/claude-code-skills-zh",
        "lazypay/Archscribe",
        "leemysw/feishu-docx",
        "levnikolaevich/claude-code-skills",
        "lingxling/awesome-skills-cn",
        "majiayu000/claude-skill-registry",
        "majiayu000/spellbook",
        "malob/nix-config",
        "marketingjuliancongdanh79-pixel/skill-generator",
        "memvid/claude-brain",
        "mhattingpete/claude-skills-marketplace",
        "microsoft/power-platform-skills",
        "mliu98/awesome-human-distillation",
        "molly554/replycueai_public",
        "mrtooher/fable-mode",
        "mxyhi/ok-skills",
        "nWave-ai/nWave",
        "nexscope-ai/eCommerce-Skills",
        "nimrodfisher/data-analytics-skills",
        "nuwa-skills/awesome-nuwa",
        "ognjengt/founder-skills",
        "oliver-kriska/claude-elixir-phoenix",
        "ombulabs/claude-code_rails-upgrade-skill",
        "op7418/Video-Wrapper-Skills",
        "opslane/opslane",
        "palkan/skills",
        "posit-dev/skills",
        "proficientlyjobs/proficiently-claude-skills",
        "rampstackco/claude-skills",
        "rediumvex/ai-video-generator-claude",
        "rokpiy/auto-commenter",
        "sanshao85/claude-skills-guide",
        "seb1n/awesome-ai-agent-skills",
        "secondsky/claude-skills",
        "serejaris/personal-corp-os",
        "sergebulaev/linkedin-skills",
        "seyedehsanhadi/sloptrim",
        "shanraisshan/claude-code-hooks",
        "slimeglitch/gryffin-calorai-ventus",
        "smallnest/goskills",
        "spences10/svelte-claude-skills",
        "spontaneousai/job-hunt-copilot",
        "staruhub/ClaudeSkills",
        "syahiidkamil/Software-Engineer-AI-Agent-Atlas",
        "tamtom/play-console-cli",
        "thoughtbot/rails-audit-thoughtbot",
        "tripleyak/SkillForge",
        "tzachbon/smart-ralph",
        "wanghuan9/skilldock",
        "wanshuiyin/Anti-Autoresearch",
        "worldwonderer/novel-to-game",
        "wrsmith108/linear-claude-skill",
        "y49/tlive",
        "yanliudesign/offer-toolkit-skill",
        "zarazhangrui/youtube-to-ebook",
        "zhaihao118/Micro-Drama-Skills",
        "zippoxer/subtask",
        "zouchenzhen/thesis-defense-pptx-skill",
        "zscole/adversarial-spec"
      ],
      "T1": [
        "0x0funky/agent-sprite-forge",
        "0xNyk/awesome-hermes-agent",
        "Agents365-ai/drawio-skill",
        "AminBlg/SimpleEnglish",
        "Ar9av/obsidian-wiki",
        "Astro-Han/karpathy-llm-wiki",
        "AvdLee/Swift-Concurrency-Agent-Skill",
        "AvdLee/SwiftUI-Agent-Skill",
        "BayramAnnakov/claude-reflect",
        "DenisSergeevitch/agents-best-practices",
        "Devin-AXIS/iPolloWork",
        "Eronred/aso-skills",
        "Forward-Future/loopy",
        "FrancyJGLisboa/agent-skill-creator",
        "GuDaStudio/skills",
        "JimLiu/baoyu-design",
        "JuneYaooo/gpt-image2-ppt-skills",
        "JuneYaooo/nihaisha-nishi-tcm",
        "KKKKhazix/human-writing",
        "Kaelio/ktx",
        "KhazP/vibe-coding-prompt-template",
        "Klotzkette/claude-fuer-deutsches-recht",
        "Leutenegger/book-to-skill",
        "MARKTECHPOST-AI-MEDIA-INC/AI-Agents-Projects-Tutorials",
        "MengTo/Skills",
        "NVIDIA/skills",
        "NarratorAI-Studio/narrator-ai-cli-skill",
        "Natively-AI-assistant/natively-cluely-ai-assistant",
        "OpenRaiser/NanoResearch",
        "OpenSenseNova/SenseNova-Skills",
        "Owl-Listener/designer-skills",
        "Paramchoudhary/ResumeSkills",
        "Prat011/awesome-llm-skills",
        "RKiding/Awesome-finance-skills",
        "Sahir619/fable-method",
        "SamurAIGPT/Generative-Media-Skills",
        "SawyerHood/dev-browser",
        "SnailSploit/Claude-Red",
        "ThinkInAIXYZ/deepchat",
        "Vincentwei1021/video-shotcraft",
        "Weizhena/Deep-Research-skills",
        "WenyuChiou/awesome-agentic-ai-zh",
        "WordPress/agent-skills",
        "a5c-ai/babysitter",
        "aaron-he-zhu/aaron-marketing-skills",
        "abubakarsiddik31/claude-skills-collection",
        "activeloopai/hivemind",
        "addyosmani/web-quality-skills",
        "ageerle/ruoyi-ai",
        "agiwhitelist/auteur",
        "aipoch/medical-research-skills",
        "aiwithremy/claude-skills-llm-council",
        "alookai/alook",
        "amElnagdy/delegate-skills",
        "anbeime/skill",
        "antfu/skills",
        "antonbabenko/terraform-skill",
        "apify/agent-skills",
        "bergside/awesome-design-skills",
        "bevibing/tutor-skills",
        "breaking-brake/cc-wf-studio",
        "browserbase/skills",
        "browserwing/browserwing",
        "brycewang-stanford/Auto-Empirical-Research-Skills",
        "chuspeeism/dashi-ppt-skill",
        "ciembor/agent-rules-books",
        "cisco-ai-defense/skill-scanner",
        "cloudflare/security-audit-skill",
        "codeaashu/claude-code",
        "composio-community/awesome-claude-plugins",
        "conorluddy/ios-simulator-skill",
        "datopian/portaljs",
        "davepoon/buildwithclaude",
        "davidondrej/skills",
        "deanpeters/Product-Manager-Skills",
        "dgreenheck/webgpu-claude-skill",
        "dotnet/skills",
        "elementalsouls/Claude-BugHunter",
        "elementalsouls/Claude-OSINT",
        "eugeniughelbur/obsidian-second-brain",
        "evalstate/fast-agent",
        "expo/skills",
        "fcakyon/claude-codex-settings",
        "feiskyer/claude-code-settings",
        "foryourhealth111-pixel/Vibe-Skills",
        "geekjourneyx/md2wechat-skill",
        "glincker/thesvg",
        "glitternetwork/pinme",
        "gooseworks-ai/goose-skills",
        "gosom/google-maps-scraper",
        "gotalab/cc-sdd",
        "heilcheng/awesome-agent-skills",
        "hesamsheikh/octogent",
        "heshengtao/super-agent-party",
        "himself65/finance-skills",
        "htmlstreamofficial/preline",
        "huangjia2019/claude-code-engineering",
        "huangserva/skill-prompt-generator",
        "iamzhihuix/skills-manage",
        "iflytek/skillhub",
        "ikaijua/Awesome-AITools",
        "inkeep/open-knowledge",
        "internet-court/internet-court-skill",
        "isjiamu/gzh-design-skill",
        "itsmostafa/aws-agent-skills",
        "jacob-bd/gemini-notebook-mcp-cli",
        "jakubkrehel/make-interfaces-feel-better",
        "jakubkrehel/skills",
        "jangviktor-web/nihaixia",
        "jeremylongshore/claude-code-plugins-plus-skills",
        "jherrodthomas/automotive-skills-suite",
        "jihe520/MathModelAgent",
        "joeseesun/qiaomu-anything-to-notebooklm",
        "kevinluosl/deepbot",
        "lackeyjb/playwright-skill",
        "lessweb/deepcode-cli",
        "libukai/awesome-agent-skills",
        "liustack/modlens",
        "maxritter/pilot-shell",
        "memodb-io/Acontext",
        "metalbear-co/mirrord",
        "mex-memory/mex",
        "microsoft/skill-recorder",
        "microsoft/skills",
        "minsight-ai-info/AI-Search-Hub",
        "mohitagw15856/pm-claude-skills",
        "mrgoonie/claudekit-skills",
        "muxuuu/serenity-skill",
        "ningzimu/codex-ppt-skill",
        "nowork-studio/notfair-plugin",
        "open-gitagent/opengap",
        "parcadei/Continuous-Claude-v3",
        "pedrohcgs/claude-code-my-workflow",
        "plannotator/effective-html",
        "quemsah/awesome-claude-plugins",
        "refly-ai/refly",
        "remotion-dev/skills",
        "rohitg00/pro-workflow",
        "romainsimon/paperasse",
        "rpamis/comet",
        "samber/cc-skills-golang",
        "skalesapp/skales",
        "snyk/agent-scan",
        "softaworks/agent-toolkit",
        "specstoryai/getspecstory",
        "supabase/agent-skills",
        "taishi-i/awesome-ChatGPT-repositories",
        "tech-leads-club/agent-skills",
        "timescale/pg-aiguide",
        "tinyplex/tinybase",
        "trailofbits/skills",
        "twostraws/Swift-Agent-Skills",
        "twostraws/SwiftUI-Agent-Skill",
        "u14app/neo-chat",
        "vuejs-ai/skills",
        "wesammustafa/Claude-Code-Everything-You-Need-to-Know",
        "wondelai/skills",
        "worldwonderer/oh-story-claudecode",
        "wuyoscar/GPT-Image2-Skill",
        "xingkongliang/skills-manager",
        "xixu-me/awesome-persona-distill-skills",
        "xu-xiang/everything-claude-code-zh",
        "yaojingang/yao-meta-skill",
        "yetone/native-feel-skill",
        "yzfly/douyin-mcp-server",
        "zanwei/design-dna",
        "zebbern/claude-code-guide",
        "zenbu-labs/terminal-browser"
      ]
    }
  }
}
```

## G1 檢查清單(BRIEF §3)
- [ ] 清單完整性(重要 repo 未遺漏;superpowers 現址已確認)
- [ ] taxonomy 分類正確(尤其 E/F 排除是否合理)
- [ ] 純度標籤 domain / fame / cohort 標注正確
- [ ] 四層抽樣分布合理(T0/T1 不可全是同類同域)
- [ ] verdict:approved / rejected(附修改指示)
