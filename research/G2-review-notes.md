# G2 審查材料(Gate G2 — feature schema 與已知近似值)

- 審查對象:`extract_features.py` 的 61 欄 schema + README「已知近似值」清單
- 小批次證據:`research/feature_matrix.json`(5 rows:superpowers / ECC / karpathy-skills / anthropics-skills / ui-ux-pro-max)
- 形式:grill-with-docs 逐題裁決,決議即時落盤;全部定案後出 binary verdict
- 狀態:**審查進行中**

---

## 裁決紀錄

### Q1 ✅「合規 frontmatter」操作型定義(裁決 2 回填 stage-1 判準)

**問題**:BRIEF §6 邊界規則要求「含合規 frontmatter 的 SKILL.md」,但 `skill_spec_compliant`
實作為 `len(skills) > 0`(只數檔名)。反例:`anthropics/skills` 的 `template/SKILL.md`
(佔位模板)也被計入。空殼 SKILL.md 可讓 repo 通過 B/C/D 邊界。

**裁決**:合規 = frontmatter 同時有**非空 `name` 與非空 `description`**。
- 新增欄位 `skill_md_compliant_count`(保留 `skill_md_count` 原始計數)
- G1 裁決 2 的回填 stage-1 判準改綁 `skill_md_compliant_count ≥ 1`
- 不加長度門檻(門檻常數屬 G3 審查範圍,不在 G2 手拍)

### Q2 ✅ `open_issues` 缺欄(BRIEF §7 有列、pipeline 從未接線)

**問題**:BRIEF §7 工程品質列 `contributor_count, open_issues`,但 `base_record()` 丟棄了
`open_issues_count`,enrich-cache 與 feature_matrix 均無此欄;無任何下游腳本消費。

**裁決**:**回填 82 筆**——對 rubric 樣本逐筆 `gh api repos/{name}` 取 `open_issues_count`
寫回 repos.json,不重跑 search(零樣本擾動)。已知近似值追加第 8 條:
GitHub API 的 `open_issues_count` 為 **issues+PRs 合計**(API 怪癖),非純 issue 數。
`collect_repos.py` 的 `base_record()` 同步保留此欄,`extract_features.py` IDENTITY_KEYS 加入。

### Q3 ✅ `TRIGGER_RE` 三類實證假陰性,最小幅擴充

**證據**:小批次 943 skills 掃描——未中 595 筆中絕大多數為真陰性(description 確實無觸發情境),
但三類為結構性假陰性:(1)「should be used when」(官方推薦句式,≥2 例);
(2)「Activates for/when」(ECC 慣用);(3) 中文觸發語(小批次無中文樣本,但全量含多個中文 repo,
會被系統性判為無觸發 → 語言相關測量誤差 → 偽梯度風險)。

**裁決**:最小幅擴充,只加實證句式 + 保守中文觸發語
(`(should|can|may) be used when`/`used when`/`activates (for|when)`/`當使用者|當你|使用時機|何時使用|觸發`);
改完 selftest + 重跑小批次驗證無回歸。

### Q4 ✅ D 類「每 repo 抽樣 3–5 個 skill」口徑:3a 全量聚合、3b 確定性抽 ≤5

**問題**:ECC 單 repo 897 個 SKILL.md;BRIEF §6「抽樣 3–5」未指明管 3a 量化還是 3b 質化。

**裁決**:
- Phase 3a 聚合統計吃**全部** skill(deterministic、median 穩健、每 repo 終究一列,
  集合大小不影響 repo 層梯度權重)——「抽樣 3–5」不約束 3a
- extractor 新增 `phase3b_sample` 欄位:穩定規則(max-lines 1 + median-lines 1 + path sha1 排序取前 3,
  去重後 ≤5)確定性選出;**Phase 3b LLM 抽讀只准讀此名單**(可重現、防 cherry-pick,Iron Rule 3)
- BRIEF §6 D 類格加註此解釋

### Q5 ✅ `nonauthor_pr_count` org 膨脹:搭 Q2 便車新增 `owner_is_org`

**問題**:org repo 的 `-author:{org}` 只排除 org 帳號本身,員工 PR 全算非作者參與
(例:anthropics/skills = 1113)。org repo 在樣本中不少,工序 2 的 engagement 指標被系統性灌水。

**裁決**:Q2 回填的同一次 `gh api repos/{name}` 回應中取 `owner.type`,新增 `owner_is_org` 欄位
(零邊際成本)。工序 2 如何用它(分層/標旗/排除)屬 G3 分析層決策,G2 只確保欄位存在。
近似值 #3 同步註記此緩解。

### Q6 ✅ 其餘五個 regex proxy:全部凍結接受

**裁決**:`INSTALL_RE` / `BEFORE_AFTER_RE` / `METRIC_RE` / `MEDIA_RE` / `ci_validates_skills`
維持現狀,以文件化近似值身分接受。BEFORE_AFTER(裸 Before…After 800 字視窗)與
METRIC(badge 百分比誤中)的假陽性樣態補進 README 近似值 #1 細目。
理由:五者只餵 README 行銷面欄位,下游有 marketing-suspect 三道工序防線;
G2 資源集中在會污染 craft 梯度的項目(Q1/Q3/Q5)。
抽查洗清兩個疑點:superpowers `has_ci=False` 為真陰性(.github 無 workflows/)、
`hermes` claim 為真實支援(README §Hermes Agent)。

---

## 返工執行紀錄(六題裁決全部落地,2026-08-16)

| 變更 | 驗證 |
|------|------|
| `TRIGGER_RE` 擴充三類(Q3) | ui-ux-pro-max trig% 15.4→38.5(should-be-used-when 實證修復);anthropics 維持 66.7(真陰性未污染);selftest 新增中英斷言 |
| `skill_md_compliant_count` + `skill_spec_compliant` 改綁合規計數(Q1) | selftest:無 frontmatter 空殼不計入;小批次 5/5 無回歸。限制:佔位文字仍通過(README 近似值 #9,語意判讀留給 stage-2) |
| `phase3b_sample` 確定性抽讀名單(Q4) | selftest 確定性斷言;初版抽到 ECC 翻譯鏡像(docs/ja-JP、docs/tr),已加「skill 目錄名去重、同名取最短路徑」修正,重抽全部來自根部 skills/ |
| `backfill_repo_fields.py` 回填 open_issues + owner_is_org(Q2/Q5) | 82/82 成功、零失敗;`collect_repos.py` base_record 未來 run 直接保留兩欄 |
| README 近似值清單更新至 9 條(含 #7 過時數字修正) | — |
| BRIEF §6 兩處註記(合規定義、D 類 3–5 口徑) | — |

**Schema 定稿:61 → 65 欄**(+skill_md_compliant_count / open_issues / owner_is_org / phase3b_sample)。
小批次重跑通過;全量執行待 G2 verdict。

## G2 最終裁決

- [ ] **verdict:approved / rejected(附修改指示)**

**G2 verdict:approved(2026-08-16)**——schema 鎖定 65 欄,核准全量萃取與裁決 2 回填。
