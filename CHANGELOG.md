# CHANGELOG

版本語意:`plugin.json` / `marketplace.json` 追的是 **skill-reviewer 工具**的版本;
`rubric_version`(見兩份 rubric 檔頭)追的是**判準本身**的版本。兩者刻意分開——
工具可以修 bug 而判準不動,判準也可以在工具不變的情況下調整。

---

## [1.0.1] — 2026-08-17

rubric 判準未變(`rubric_version` 1.0.0 → 1.1.0 只加標註,規則與權重原封不動)。
本版全部是**可重現性**與**不確定性揭露**的修正。

### Fixed

- **frontmatter naive fallback 不還原 YAML 雙引號轉義**(`\"`)。
  影響:PyYAML 是選用依賴,所以有裝/沒裝的機器會得到不同的 `desc_len`。
  在 161 份真實 SKILL.md 上實測分歧 3 份(`anthropics/skills` 的 pptx / xlsx /
  slack-gif-creator),修後 0 份。**對 rubric 規則零影響**——只動到 `desc_len_median`
  這個 numeric-profile 觀察值。修正在 `extract_features.py` 與 `lint_skill.py` 兩處
  (skill-reviewer 必須可獨立出貨,不得 import 研究腳本,因此接受複本 + 測試把關)。

### Added

- **`scripts/check_parser_agreement.py`** — 三條 frontmatter parser 路徑(PyYAML /
  extract naive fallback / `lint_skill.parse_fm`)逐檔比對 `name` 與 `description`,
  任一分歧即 fail。上面那個 bug 就是它抓到的。
- **`scripts/check_stdlib_only.py`** — 零依賴 allowlist 守門。選用依賴(目前只有 PyYAML)
  必須被 `try/except` 包住,否則視為硬依賴而 fail;first-party 模組自動識別。
- **`skill-reviewer/evals/fixtures/yaml-escapes/`** — 把上述 bug 固化成 CI 拿得到的回歸夾具。
  原始語料是 gitignored 的第三方 clone,CI 看不到,所以那 161 份不能當夾具。
- **`aggregate_stats.py` 的 `bootstrap_gap_ci()`** — 對 `T_top − T_bottom` 的 prevalence
  差做層內 bootstrap 百分位 CI(B=2000,固定種子可重現)。**不是顯著性檢定。**
  結果寫進 `gradient_analysis.json`、`patterns-report.md`、`rubric.yaml` 標註。
- **CI Python 版本矩陣** 3.9 / 3.10 / 3.11 / 3.12 / 3.13(`fail-fast: false`),
  並且**先在無 PyYAML 環境跑一遍、再裝上 PyYAML 跑第二遍**。
- **`feature_matrix.json` 的 `frontmatter_parser` / `python` 欄位** — 讓輸出自我描述是哪條
  路徑產生的。既有檔案已回填 `pyyaml-6.0.3`,並在 `frontmatter_parser_note` 明示為回填。
- **`rubric_version`** 欄位(兩份 rubric),CI 斷言存在且同步。

### Disclosed(判準未變,但揭露了原本沒說清楚的不確定性)

- **5 條 differentiator 中有 2 條的 gap 95% CI 含 0**:`has_tests_or_evals` [−11.9, 85.7]、
  `readme_has_before_after` [−11.9, 85.7];`dir_examples` 下界僅 4.8。T3 層只有 n=3,
  CI 寬到 90pp 以上是結構性必然。**weight 保留原值**,因為每條另有 F0 草根復現、機制陳述、
  evidence_strength 三條獨立證據線;只採信梯度證據的讀者應視為 weight 未定。
- **判定門檻的預先登記時序**寫進 README 並可用 `git show` 自行驗證:
  `THRESHOLDS` 與 BRIEF 的去混淆三道工序比真實資料早 **2h43m** 進 git。

---

## [1.0.0] — 2026-08-16

初版。Phase 0–6 完成,三道 HITL gate(G1 / G2 / G3)皆 approved。

- 97 個 repo 分層抽樣、54 個進 rubric 樣本的特徵梯度分析
- 分級式 rubric:script 可判定 5 條 differentiator + 手寫 hygiene / craft_llm / security 維度
- `skill-reviewer` skill(deterministic lint + LLM craft 判讀兩層)
- 核心結論:**星數關聯的是「好裝」,不是「寫得好」**
