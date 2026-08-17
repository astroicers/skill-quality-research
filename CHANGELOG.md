# CHANGELOG

版本語意:`plugin.json` / `marketplace.json` 追的是 **skill-reviewer 工具**的版本;
`rubric_version`(見兩份 rubric 檔頭)追的是**判準本身**的版本。兩者刻意分開——
工具可以修 bug 而判準不動,判準也可以在工具不變的情況下調整。

---

## [1.0.3] — 2026-08-17

工具行為未變、rubric 判準未變(`rubric_version` 維持 1.1.0)。
本版揭露並備妥量測本研究**最大的未量測缺口**,另修一個會造成資料遺失的 footgun。

### Added

- **`research/inter-rater-protocol.md`** — craft 判定的審查者間一致性量測協定。
  本工具的主判在 craft(`L-001`..`L-004`),那是 LLM 判斷,而整個專案
  **從未量過兩個獨立審查者會不會給同樣結論**。連帶影響:54 份質化筆記是單一審查者的判斷;
  round 2 的 7 個例外欄位可能是修正、也可能是對單一審查者偏好的過度擬合,目前無法區分。
- **`research/inter-rater-sample.json`** — 15 個 repo 的樣本**已預先登記**:
  從 54 個 rubric 樣本各層依 `sha1(full_name)` 排序確定性抽出(T0:2/T1:2/T2:9/T3:2),
  與 `phase3b_sample` 同一道反 cherry-pick 紀律。
- **`scripts/agreement.py`** — 零依賴一致性計分:成對一致率、Cohen's κ(含線性加權,
  craft verdict 是有序尺度)、Fleiss' κ、分維度計分。selftest **對照文獻公認值**驗證
  (Fleiss 1971 十受試者例 κ=0.210、手算 Cohen κ=0.400),不是自己算的答案自己驗。
  判讀規則先寫死:不設 kappa 通過門檻、必須併看成對一致率、真正的產出是分歧本身。
- README 統計限制新增此缺口;`CLAUDE.md` 未竟事項表同步。

### Fixed

- **`clone_repos.py` 的 manifest 會靜默覆蓋研究快照紀錄**。輸出路徑原本寫死
  `research/clone-manifest.json`,**不論 `--dest` 指到哪**。重 clone 任何子集到別的目錄,
  都會蓋掉 54 repo 分析基於哪些 commit 的唯一紀錄(`research/repos/` 本身 gitignored)。
  改為跟著 `--dest` 走,預設 dest 維持原檔名以相容既有 pipeline;新增 `--manifest` 可覆寫。
- **`clone_repos.py` 原本完全沒有 `--selftest`**,也不在 CI 內——上面那個 bug 就是改它時
  才發現沒人測過它。已補 selftest(斷言不同 dest 產生不同 manifest)並掛進 CI 的
  Linux 與 Windows 兩個 job。

---

## [1.0.2] — 2026-08-17

rubric 判準未變(`rubric_version` 維持 1.1.0)。本版是 **Windows 可攜性**修正。

### Fixed

- **相對路徑未正規化,Windows 上多項判定靜默失效**。`os.path.relpath` 用 `os.sep`,
  但下游全部以 `/` 比對。實際後果:
  - `(^|/)scripts(/|$)` 這類 regex 全部比不到 → `dir_scripts` / `dir_examples` /
    `dir_references` / `has_tests_or_evals` 誤判 false → **packaging 分數系統性偏低**
  - `.github/workflows/` 前綴比對失效 → `has_ci` 誤判
  - `noncompliant_skills` 變成 `bad\SKILL.md`,而 G5 傳入的 `changed_files` 來自 git
    一律是 `/` → 交集永遠為空 → **H-005 change-scoped 靜默失效**(不會報錯,只是不再擋)

  修法:`rel` 在源頭正規化為 `/`(`lint_skill.py` 與 `extract_features.py` 兩處)。
  POSIX 上 `os.sep` 就是 `/`,此改動在 Linux/macOS 是 no-op,零行為風險。
- **Windows 重導向輸出時 `UnicodeEncodeError`**。工具訊息含中文,Windows 預設走 locale
  編碼(cp950/cp1252)。`lint_skill.py` 啟動時自行 `sys.stdout.reconfigure(encoding="utf-8")`
  ——出貨工具必須自己站得住,不能要求使用者先設 `PYTHONUTF8=1`。

### Added

- **CI `windows-latest` job**。既有的「模擬 Windows」selftest 只換掉 `os.path.relpath`
  與 `os.sep`,`os.path.basename` 仍是 posixpath 版——它能逼出 regex 與前綴比對的問題,
  但**不能代表真 Windows**。所以真 runner 是必要的,不是錦上添花。
  其中一步刻意設 `PYTHONUTF8=0`,驗證出貨工具在沒有環境變數協助時也能跑。
- **兩支 selftest 各加「模擬 Windows 分隔符」區塊**,斷言的是
  **「平台不得改變判定」**(POSIX 結果 == 模擬 Windows 結果),
  而不是某個特徵一定為 True。已反向驗證:拿掉正規化,兩支 selftest 都會失敗。
- README 新增 Windows 安裝與已知限制段落(`install.sh` 仍是 POSIX-only)。

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
