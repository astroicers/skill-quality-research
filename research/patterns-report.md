# Patterns Report(D3)— skill-quality-research Phase 4 合成報告

- n = 54(rubric 樣本;A:1/B:19/C:13/D:21;T3:6/T2:33/T1:8/T0:7);純度樣本 F0×14
- 子樣本:class_BD=40、fame_F0=22、cohort_C1=10/C2=38/C3=3
- 量化來源 `gradient_analysis.json`;質化來源 54 份 `qualitative_notes/`
- **統計誠實聲明**:n 過小,不做迴歸、不宣稱顯著;下為 prevalence 梯度 + Spearman 描述值。
  所有 differentiator 的 ρ(log★) 僅 0.19–0.32(**弱**),一律稱「符合 X 星級剖面」,非「梯度驅動/會得 X 星」。

---

## 1. Hygiene 門檻特徵(各層皆備)

| feature | T0% | T1% | T2% | T3% | 說明 |
|---|---|---|---|---|---|
| skill_spec_compliant | 100 | 100 | 100 | 100 | **selection artifact**:樣本本以合規 SKILL.md 篩選,100% 是循環,不可當市場證據 |
| dir_scripts | 71.4 | 87.5 | 84.8 | 83.3 | 唯一由本樣本存活的真 hygiene(各層皆高、平坦) |

⚠ hygiene 分類幾乎崩塌(見 §6)。最終 rubric 的 hygiene 門檻改由 **triangulation**(官方 spec + anthropics/skills)補強,見 `rubric-manual-dimensions.yaml` H-001~004。

## 2. Tier 梯度特徵(differentiator)

| feature | signal | T0 | T1 | T2 | T3 | gap | **gap 95%CI** | ρ(log★) | weight | 強度 | 註 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| has_tests_or_evals | craft | 28.6 | 50 | 69.7 | 66.7 | 38 | **[−11.9, 85.7]** | 0.213 | 4 | strong | 唯一 craft 面 strong;**CI 含 0** |
| install_oneliner_in_readme | packaging | 57.1 | 62.5 | 78.8 | 100 | 43 | [14.3, 85.7] | 0.321 | 3 | strong | packaging 上限 3 |
| has_marketplace_json | packaging | 28.6 | 62.5 | 60.6 | 100 | 71 | [42.9, 100.0] | 0.321 | 3 | moderate | ⚠ marketing-suspect |
| dir_examples | craft | 14.3 | 25 | 33.3 | 66.7 | 52 | [4.8, 100.0] | 0.197 | 2 | moderate | 下界貼近 0 |
| readme_has_before_after | marketing | 28.6 | 50 | 45.5 | 66.7 | 38 | **[−11.9, 85.7]** | 0.192 | 2 | moderate | ⚠ marketing-suspect;**CI 含 0** |

**gap 95%CI 怎麼讀(2026-08-17 補算)**:層內 bootstrap 重抽 B=2000、固定種子的百分位區間,
**不是**顯著性檢定,不得因「CI 不含 0」宣稱顯著。它回答的是「若重抽同樣大小的樣本,這個 gap 大概落在哪」。
T3 只有 **n=3**,所以 CI 寬到 90pp 以上是結構性的必然,不是計算錯誤。

三件事因此必須說清楚:

1. **5 條裡有 2 條的 CI 含 0**(`has_tests_or_evals`、`readme_has_before_after`)——就梯度這一條證據而言,
   它們與「根本沒有梯度」無法區分。`dir_examples` 下界 4.8pp 也僅一步之遙。
2. **weight 仍保留原值**,因為 weight 不是只由梯度推出的:每條都另有 F0 草根復現、機制陳述、
   evidence_strength 三條獨立證據線,梯度是其中一條而非全部。**若讀者只採信梯度證據,
   應把這兩條視為 weight 未定**——這個判讀權我們交還給讀者,不替他決定。
3. 這反而**強化**了本研究的核心結論方向:星數是弱訊號。連「packaging 比 craft 更能解釋星數」
   這個結論,其證據強度也遠低於一張沒有 CI 的表格看起來的樣子。

**核心觀察(最重要)**:5 條 differentiator 中 4 條是 packaging/marketing 面,唯一的 craft 面(has_tests_or_evals)也偏工程而非寫作。**寫作工藝(trigger/style/scope)量化上全落 noise**——見 §3。這強力印證:**在此樣本與時點,skill 星數關聯的是「可安裝/可發現/可信任」,不是內容工藝。**

## 3. 反模式與 T0 特有現象(質化)

> **具名 repo 的讀法**:以下樣態附具名實例是為了可查證。全部來自公開原始碼的靜態閱讀
> (2026-08-16 快照),**樣態是發現、repo 只是證據**;不是漏洞揭露,不宣稱作者有惡意。
> 詳見 [`qualitative_notes/README.md`](qualitative_notes/README.md)。

- **有 SKILL.md 之形、無規格之實**:24kchengYe/human-skill-tree(T0)68 個 SKILL.md 全無 frontmatter,標題式 Markdown。已 H-001 擋下。此為 T0 層典型反模式。
- **觸發語存在但品質崩壞**:高星 repo 常「有觸發語但關鍵字轟炸」——browser-act 20+ SEO 式變體、Jeffallan SKILL.md 尾強制 SEO backlink。二元 `desc_has_trigger` 抓不到這種劣化。
- **skill_md_count 灌水**:planning-with-files / turbo 用語言/IDE 鏡像複製、vibeeval 341 skills grab-bag 品質極不一。統計需去鏡像(已由 phase3b_sample 目錄去重處理)。
- **機械 token 壓縮傷害**:karpathy-skills、addyosmani ci-cd 檔文法詞脫落、可讀性受損——「過度壓縮」是可觀測負面特徵。
- **裸 MUST 堆疊**:Jeffallan、Leonxlnx/taste 以 ALL-CAPS 禁令取代解釋 why。
- **單一 skill 長成小產品**:planning-with-files 一個 skill 內含多 plan/attestation/模式/hooks,scope 膨脹。

## 4. 官方規範 vs 社群實務落差

- **官方(anthropics/skills)**:description 三人稱能力陳述 + 觸發條件;但同 repo 內落差大(claude-api 觸發設計最工程化,frontend-design/theme-factory 無觸發語、template 是佔位)。→ 連官方都非每個 skill 都寫觸發語,「有無 Use when」不宜當硬門檻。
- **社群優於官方之處**:blader/humanizer(35 pattern 中 31 條附 why+before/after;2026-08-18 勘誤)、ayghri(why→rules→override→自檢)、addyosmani(生命週期切分+防重複規則+error-as-untrusted-data)——寫作紀律超越官方基準。
- **CLAUDE.md-only 現象(v1.2.1)**:karpathy-skills(202k★)零 SKILL.md 純 CLAUDE.md;jezweb CLAUDE.md 主張「800 行勝過 300」反對官方 <500 建議。→ 規格合規是 hygiene 但非工藝上界;長度非絕對(H-003 列 warning 非 error)。
- **anti-hallucination 是社群自發的高階模式**:K-Dense、Orchestra、claude-ads、google 內建 dated snapshot / never-from-memory,官方 spec 未強制。

## 5. 混淆因子分析(去混淆三道工序)

- **工序 1 素人復現**:5 條 differentiator 全在 F0 純度樣本(n=22)同向復現 → 非純名人效應。fm_license_any 未復現 → 已降 observation-only(出局)。
- **工序 2 雙結果變數 ⚠ 重大限制**:**所有 differentiator 對 fork_star_ratio 的 ρ 幾乎全負(−0.12 ~ −0.07)**,只有 contributor_count 正相關。意即這些差異化項**未被「fork 來實際使用」的行為背書**——與星數同向、與 fork 反向。marketing_suspect 判準已收緊(median + fork 全負隔離),has_marketplace_json 與 readme_has_before_after 因此被標記,不計入 craft。
- **工序 3 機制陳述**:5 條皆有因果機制(見 rubric.yaml)。
- **cohort C3(n=3)**:過薄,複算方向全 None,結果封頂 weak(G1 裁決 4)。
- **domain**:T0 design-ui 偏斜擴樣後未消(G1 已知限制),hygiene 門檻推導帶 design-ui 領域特性,列為限制。

## 6. Rubric 權重與 tier 門檻推導依據(G3 定稿)

- **weight 公式(G3-Q2 定稿)**:`base = 1 + round(4×min(gap,60)/60)`,乘 evidence 係數(strong×1/moderate×0.6/weak×0.3),**packaging signal 上限 3**(packaging 是可安裝性非工藝,不得與 craft 同權),clamp 1..5。
- **判定常數**:hygiene ≥70% 且層間差 ≤20pp;differentiator 單調且 gap ≥30pp;min_tier_n=3;marketing rho_max=0.1。
- **三分類最終分布**:hygiene 2 / differentiator 5 / observation-only 1 / numeric-profile 6 / noise 14。
- **craft 維度改由 LLM 承載**(G3-Q3):trigger/style/scope 量化落 noise,故 rubric 的 craft 規則(L-001~004)為 check_type=llm,證據=54 份質化筆記。
- **hygiene 門檻改由 triangulation**(G3-Q4):樣本篩選使多數 hygiene 特徵天花板化,門檻源改官方 spec。
- **安全維度**(G3-Q6):S-001~003 紅旗 + S-101 正面防禦,一律 hygiene(不加分不過即 fail)。

## 7. 對 skill-reviewer 的總結論

- **script 差異化項本質是 packaging benchmark**;craft verdict 必須靠 LLM 層。
- **星數 ≠ 品質有大量實證**:T0/400★ turbo、T0/968★ jezweb、T0/962★ icm-architect craft 達 T2/T3 水準;T3/117k★ nextlevelbuilder 有關鍵字堆疊與 mega-skill 重複。
- **packaging 低 ≠ craft 差**:i-have-adhd(T2 craft 標竿)packaging 僅 7/14;自家 4 skills packaging 0/14 但 craft 高(見 self-audit.md)。
- 對標須用同 taxonomy 參照類,勿拿單一 skill(B)對標框架(C)。
