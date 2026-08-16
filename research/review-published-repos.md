# 品質檢測報告 — 三個已發布 skill repo(2026-08-17)

- 對象:`astroicers/visual-web-stack`、`astroicers/slidev-deck-stack`、`astroicers/talk-craft`
- 方法:`skill-reviewer` 完整流程(lint → 判 skill 形狀 → craft 四維度 → 安全複核),三個獨立 agent 平行審
- **與先前 self-audit 的差別**:這次審的是**已發布版**(有 `.claude-plugin`、`install.sh`、CI、LICENSE),
  packaging 面**如實採計、不宣告豁免**——內部版可以說「內部工具不採計 packaging」,發布版不行

---

## 一頁總結

| repo | Craft Verdict | craft 剖面 | packaging | 最該補的 |
|------|--------------|-----------|-----------|---------|
| talk-craft | **approved** | **T3** | 6/14 | 版本不一致(見下)+ evals |
| slidev-deck-stack | **approved** | 高星級剖面 | 6/14 | examples + build 迴歸測試 |
| visual-web-stack | **approved** | 高品質樣本剖面 | 6/14 | evals(code 片段無迴歸)+ examples |

**三者 craft 全部 approved,且 L-004(anti-hallucination)是本次最強項**——
`.fact-check.md` / `.asp-fact-check.md` 逐條主張標日期+來源連結+修正紀錄,
審查者評為「優於 rubric 原始 evidence_refs 樣本(K-Dense、claude-ads)」。

三個 repo 的 packaging 分數完全相同(6/14)、gap 完全相同——同一套打包模板,一致性好。

---

## 1. ⚠️ 立即可修的具體問題

### talk-craft:版本三處不一致(唯一的硬缺陷)

- `.claude-plugin/plugin.json` = **1.2.1**
- `marketplace.json` = **1.2.1**
- `CHANGELOG.md` 最新 = **[1.2.2] - 2026-07-05**

對已發布 repo 而言,marketplace 顯示的版本會與 changelog 宣稱的功能對不上。
**且 CI(`validate.yml`)沒有版本一致性檢查**——建議一併補,否則同類漂移會再犯。
(另兩個 repo 版本一致:slidev 1.1.1、visual-web-stack 1.0.2,三處對齊。)

### 三者共通:gap list 的真偽判定

審查者逐項判斷後(**不是照抄 lint**):

| gap | weight | 判定 |
|-----|--------|------|
| `has_tests_or_evals` | 4 | **真缺口**(三者皆是)。CI 只驗結構(JSON 合法、frontmatter、references 齊全),不驗**內容正確性**。visual-web-stack 的 `.asp-fact-check.md` #9/#13 顯示作者曾手動用 tsc 才抓到型別問題——這種漂移目前只能靠人工重跑 fact-check |
| `dir_examples` | 2 | talk-craft **非真缺口**(`references/worked-example.md` 已是端到端走查,只是不在 `examples/` 目錄形狀下——lint 的結構性假陰性);slidev / visual-web-stack 為**真缺口** |
| `readme_has_before_after` | 2 | **半真缺口**。三者的 `pitfalls.md` / `anti-patterns.md` 都有「症狀→原因→解法」表承擔同等教學功能,但不在 README、非視覺對照 |

**建議優先序**:補一份可跑的 `examples/`,同時當作 `has_tests_or_evals` 的迴歸靶標——
一份投入同時關掉兩個 gap(slidev 審查者的建議,我同意)。

---

## 2. ✅ 安全複核:S-003 三個全是誤報,已修 lint

lint 對三個 repo 都標了 `S-003 self_update`。**依 SKILL.md 步驟 5 紀律去查**(不憑印象推翻):

- 命中源是 README「## 更新」段的 `git pull && ./install.sh --force`
- 這是**給人看的手動更新說明**,不是 agent 自我更新
- 對照真陽性樣態(guizang-ppt-skill:SKILL.md 內指示每次啟動 `git fetch` 檢查上游)——性質完全不同

**三個獨立審查者也各自得出誤報結論**,與我一致。

**這實證了 final review 的 M4 預言(flag 疲勞)**:`REDFLAG_SELF_UPDATE` 匹配任何 `git pull`,
3/3 發布 repo 全中全誤報。**已修**:偵測範圍從「所有 .md」收窄為
**agent 指令面**(SKILL.md 全文 + hooks/),排除 README 與 install.sh(人為明示執行)。
修正後三個 repo 的 security flag 全清空。

`install.sh` 靜態審查(三者皆**只讀不執行**):純本地檔案操作、無 `curl|bash`、無 `eval`、
無網路呼叫、覆蓋前有互動確認、非互動環境要求顯式 `--force`、失敗路徑有明確訊息並非零退出。
**判定:無真實安全風險。**

---

## 3. craft 分維度亮點(三者共通的高分樣態)

- **L-001**:三者 Triggers 皆 20–40 詞,但抽樣驗證後**各自映射到不同 references 檔案/段落**——
  依新增的 `disambiguation` 條款判為「多子意圖映射」而非同義詞灌水,**不扣分**
- **L-002**:鐵則皆「規則 + 後果 why」而非裸 MUST。
  slidev 引文:「寫錯位置全域設定會靜默失效,不報錯也不生效,最難 debug」
- **L-003(三者最強項)**:跨 skill 邊界治理做到**欄位級契約**——
  talk-craft `templates.md §3` 定義 ghost-deck schema,並明講 slidev 端的消費規格在其
  `references/handoff.md`,「欄位字字對齊」。**這超出 rubric 現有 `sub_pattern_cross_skill` 的
  範例規格**(該條只記錄了相對路徑引用),是值得回饋 rubric 的更高階樣態
- **L-004**:如前述,三者的 fact-check 機制優於 rubric 原始標竿樣本

## 4. talk-craft 的自我一致性檢查(教材是否遵守自己教的)

talk-craft 教「標題下論點、不下主題標籤」(鐵則 3)。審查者檢查全 repo 約 50 個 section 標題:
**沒有任何一個是完整論點句**,全是主題標籤(「## 1. Assertion-Evidence」)。

**審查者的判定我同意:不構成 craft 降級**——鐵則 3 字面針對「投影片」,
技術參考文件用主題式標題是合理慣例(讀者要能掃描目錄)。
但作者值得知悉這個「教得比做得嚴」的落差,尤其 SKILL.md 本身沒有一句明示的 governing thought。

---

## 5. 本次檢測反饋到工具本身的三個修正

這次審查同時當成 skill-reviewer 的實戰校準,發現並修了三個 bug:

1. **S-003 誤報**(如上)——偵測範圍收窄到 agent 指令面
2. **`noncompliant_skills` 沒出現在 JSON 頂層**——H-005 的設計要 G5 取交集,少了它整合會壞。
   (是我寫回歸腳本時踩到才發現的,已加 selftest 斷言防再犯)
3. **naive parser 不認 YAML 隱式多行純量**(`description:` 後直接換行接縮排)——
   實例:`vercel-labs/agent-skills`。這讓 H-005 誤標 2 個 repo。
   與 round 1 修的 `description: |` 是同類 bug 的不同變體。
   **兩處 parser(lint 與 extract fallback)已同步對齊**,修正後 H-005 從 3/54 收斂到精確的 1/54。
