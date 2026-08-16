# OthmanAdi/planning-with-files（T2 / taxonomy C / 26,191 stars）

## 抽讀樣本
- skills/planning-with-files/SKILL.md（前 400 行）
- skills/planning-with-files-ar/SKILL.md（前 80 行）
- skills/planning-with-files-es/SKILL.md（前 80 行）
- skills/planning-with-files-zh/SKILL.md（前 80 行）
- skills/planning-with-files-zht/SKILL.md（前 80 行）

## trigger 設計：good
- 主檔 description 觸發條件具體且可操作化：「Use when asked to plan out, break down, or organize a multi-step project... or any work requiring 5+ tool calls」。
- 各語言版把觸發詞本地化成關鍵詞清單（zh：「觸發詞：任務規劃、專案計畫、制定計畫、分解任務...幫我規劃」），是多語 trigger 工程的少見範例。
- pushy 程度偏高但透明：除 description 外還用 UserPromptSubmit/PreToolUse hooks 主動注入 plan 內容，等於把觸發從語意層挪到機制層。

## 寫作風格：mixed
- 好的一面：imperative、講 why、有記憶模型比喻（「Context Window = RAM... Filesystem = Disk」）、決策矩陣（Read vs Write）、3-Strike 錯誤協議，甚至引研究佐證設計（「evidence (arxiv 2603.03258...) shows drift is real」）。
- 壞的一面：SKILL.md 長期堆積版本註記（v2.2.0 / v2.38.0 / v3.9.0 / v3.10.1 散落全文）、install-route 差異表、已知 bug workaround（引 claude-code issues #26251）——changelog 與 troubleshooting 侵入教學正文，讀者要先過濾歷史才能拿到當前規則。
- 4 個翻譯版內容忠實同步（連 hook 註解都保留英文原文），維護紀律好。

## scope 清晰度：mixed
- 核心 job 單一且清楚（file-based persistent planning），但單一 skill 內長出：多 plan 並行、attestation（SHA-256 防竄改）、autonomous/gated 模式、parallel-write guard、/plan-goal + /plan-loop 包裝、loop.md 模板——一個 skill 承載了一整個小產品的功能面。
- 18 個 SKILL.md 中至少 5 個是同一 skill 的語言複本（另推測含 IDE 變體，frontmatter 註解提到「the 11 IDE and language variants share one template」），skill_md_count 高度灌水，統計時需去重。

## 其他觀察
- ⚠ 安全觀察（非 injection 文字，屬機制面）：frontmatter 註冊 5 種 hook 事件，會在每次 prompt/工具呼叫時搜尋多個路徑並執行找到的第一個 shell script（「for c in "${PWF_SCRIPT_DIR}/inject-plan.sh" ... do [ -f "$c" ] && { SH="$c"; break; }」）。安裝此 skill = 授予 repo 內腳本常駐執行權，是 SKILL.md 格式中攻擊面最大的樣本；對 rubric 的啟示：hooks 欄位存在與否應是安全維度特徵。
- 對「防竄改」有罕見的誠實限制聲明：「Attestation does not cover this... it is a read-side gate that cannot stop the stale write」。
