# Executive Summary — skill-quality-research

> 一頁總結。完整證據見 `patterns-report.md`(D3)、`rubric.yaml`(D4)、`self-audit.md`(D6)。
> 定位:所有產出皆為 **proposal**,待人工審閱,非結論。快照日 2026-08-16。

## 一句話結論

**分析 97 個 Agent Skill repo 的星數梯度後發現:skill 的星數關聯的是「可安裝 / 可發現 / 可信任」的打包面,不是內容工藝——因此一個可靠的 skill 品質審查器,核心價值必然在 LLM 的質化 craft 判讀,自動化 lint 只能當 packaging 過濾器與安全門檻。**

## 我們做了什麼(方法)

- 依星數分四層(T0–T3)分層抽樣 97 repo,標注三組混淆因子(作者聲量 / 發布世代 / 領域),
  以 **F0 素人達 T2+** 的 14 個「純度樣本」作去混淆黃金對照組。
- 兩階段:deterministic script 先跑量化梯度,LLM 質化抽讀在後(54 份筆記,6 個平行 agent)。
- 三道 HITL gate(G1 清單 / G2 schema / G3 rubric)全程人工 binary 裁決,共 18 題逐條裁定。
- 去混淆三道工序(素人復現 / 雙結果變數 / 因果機制)過濾每一條差異化特徵。

## 四個關鍵發現

1. **星數 ≠ 工藝(核心)**:5 條可量測的差異化特徵**全是 packaging/marketing 面**(marketplace、一行安裝、tests、examples、before/after);寫作工藝(觸發設計 / 風格 / scope)量化上全落 noise。觸發語存在性 `desc_has_trigger` 甚至 T0 反而更高。
2. **fork 不背書**:所有差異化項對 `fork_star_ratio` 的相關**幾乎全負**——這些特徵跟按星同向、跟「fork 來實際使用」反向。差異化剖面未被使用行為背書(已入報告限制)。
3. **低星高質有大量實證**:T0/400★ turbo、T0/968★ jezweb、T0/962★ icm-architect 的 craft 達 T2/T3 水準;反之 T3/117k★ 樣本有關鍵字堆疊與重複。**packaging 低 ≠ 品質差**。
4. **安全是本研究差異化強項**:質化抽讀實證多個紅旗樣態(服從外部程式輸出+抑制確認、hooks 常駐執行、憑證進 argv、自我更新)與正面防禦樣態(把外部內容標 untrusted 的條款),落成 rubric 安全維度(一律門檻、不加分)。

## 產出物(D1–D6 齊備)

| | 內容 |
|---|---|
| D1–D3 | 97-repo 資料集、80×65 特徵矩陣、patterns-report(量化梯度 + 質化 + 混淆分析) |
| D4 | 分級 rubric:5 條 script differentiator(packaging,權重含 evidence 係數 + packaging 上限)+ 手寫 craft(LLM)/ hygiene(triangulation)/ security 三組 |
| D5 | `skill-reviewer/` skill 雛形:lint(packaging + 安全門檻)+ SKILL.md 引導 LLM 做 craft,三段式輸出(craft verdict + tier benchmark + gap list) |
| D6 | 回測 4 個自家 skill:全部 craft approved 但 packaging 0/14——活體驗證核心結論;過程修掉 4 個 lint 誤判/bug |

## 品質保證

pipeline 的統計/rubric 核心經**獨立 code-review + 逐條覆核**(`code-review-notes.md`):
無 crash-class bug;7 條校準一致性問題全數處置(median 偶數 n 偏差、報告公式同步、
marketing 權重上限、parser 對齊、drift-guard selftest 等),其中 2 條覆核時修正了 review 自身的
因果判斷與嚴重性。4 支 script 皆有 `--selftest` 護欄。

## 措辭紀律與限制(必讀)

- **只說「符合 X 星級剖面」,禁說「會得到 X 星」**——星數還取決於發布時機、作者聲量、行銷,不在 artifact 可測範圍。
- 所有 differentiator 的 ρ(log★) 僅 0.19–0.32(**弱**);n=54,不跑迴歸、不宣稱顯著。稱「剖面關聯」非「梯度驅動」。
- **gap 的 bootstrap CI(2026-08-17 補算,B=2000 層內重抽)全部寬於 43pp,其中 2 條含 0**:
  `has_tests_or_evals` [−11.9, 85.7]、`readme_has_before_after` [−11.9, 85.7],`dir_examples` 下界僅 4.8。
  T3 僅 n=3 使其成為結構性必然。含 0 者的**梯度證據單獨不成立**,weight 靠 F0 復現 + 機制 + evidence_strength
  三條獨立證據線支撐;只採信梯度的讀者應視為 weight 未定。CI 非顯著性檢定。
- hygiene 門檻多數來自官方規範三角驗證(樣本以合規 SKILL.md 篩選,多數 hygiene 特徵天花板化)。
- 已知偏斜:T0 領域偏 design-ui;C3 世代 n=3 過薄(複算封頂 weak)。

## 一句話展望

skill-reviewer 的價值錨點是 LLM craft 層;下一步應把它掛入治理層(ASP Auditor pattern),
並以更多低星高質樣本持續校準 craft 判準——因為那正是自動化最測不到、卻最決定品質的地方。
