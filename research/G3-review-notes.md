# G3 審查材料(Gate G3 — rubric 逐條證據審查,最高風險 gate)

- 審查對象:`research/rubric-draft.yaml`(8 條)+ 權重公式 + 門檻常數 + 三分類機制
- 證據來源:`research/gradient_analysis.json`(n=54)、`research/qualitative_notes/*`(54 份)
- 樣本剖面:rubric 樣本 54(A:1/B:19/C:13/D:21);tier T3:6/T2:33/T1:8/T0:7;純度樣本 14
- 形式:grill-with-docs 逐題裁決,決議即時落盤
- 狀態:**審查進行中**

---

## 0. 我的獨立覆核發現(不只逐條看規則,先看大結構)

### 發現 A(最重要):script 能抓的 differentiator 全是 packaging/docs,沒有一個是 craft

6 條 differentiator:has_marketplace_json、install_oneliner_in_readme、has_tests_or_evals、
dir_examples、readme_has_before_after、fm_license_any。**全部是「可安裝/可發現/可信任」的打包行銷面**,
沒有一條是寫作工藝(trigger/style/scope)。這強力印證 BRIEF §9 核心警語:
**高星關聯的是「容易被裝、被找到、被信任」,不是 skill 本身的工藝。**
→ rubric 定位須明確:script 差異化項幾乎等於 packaging benchmark;craft 只能靠 LLM 維度(見發現 B)。

### 發現 B:觸發設計(專案自認的核心維度)量化上是 noise,且 T0 反而更高

`desc_has_trigger_majority`:T0 71.4 / T1 50.0 / T2 60.6 / T3 50.0(ρ=−0.131)。
二元 regex「有無觸發語」完全不是 differentiator。質化筆記解釋了原因:高星 repo 常「有觸發語但
關鍵字轟炸」(browser-act 20+ 變體 SEO 式、Leonxlnx/taste 五份全無 Use when 卻 scope 清楚),
低星卻常有優質觸發(nicobailon 量化門檻、turbo 逐字自然語句)。
→ trigger 品質**不可**用 `desc_has_trigger` 當 script differentiator;必須下放 LLM 維度(BRIEF §8-2)。

### 發現 C:hygiene 分類幾乎崩塌(只剩 1 條有效)

hygiene 僅 2 條,其中 `skill_spec_compliant` 已標 selection_artifact(樣本本就以合規 SKILL.md 篩選,
100% 是循環)。真正有效的 hygiene 只有 `dir_scripts`(且 T0=71.4% 不算「各層皆高且平坦」)。
原因:G2 裁決 2 的樣本篩選把許多本該當 hygiene 門檻的特徵推到天花板或推出樣本。
→ hygiene 門檻的推導基礎薄弱,G3 須決定:hygiene 清單要不要改由「規範三角驗證」(anthropics/skills +
官方 spec)補充,而非只靠本樣本 prevalence。

### 發現 D:所有 differentiator 的 ρ(log_stars) 僅 0.19–0.32(很弱)

prevalence 表看似單調,但 Spearman 相關全部微弱。BRIEF 統計誠實條款禁跑迴歸/宣稱顯著;
這裡連效果量都弱,措辭必須誠實為「剖面關聯」而非「梯度驅動」。

### 發現 E:fork_star_ratio 的 ρ 幾乎全負(−0.12 ~ −0.07)

工序 2 雙結果變數中,fork/star 這個 engagement 指標與 differentiator 方向與星數相反,
只有 contributor_count 正相關撐住「非 marketing-suspect」判定。marketing_suspect 目前用
`max(eng_rhos) < 0.1`(取最寬鬆的結果變數),等於「只要有一個 engagement 指標正相關就洗清」。
→ 判準是否過寬?fork_star_ratio 全負這件事本身該不該在報告中標記?

---

## 1. 待裁決事項(逐條)

### G3-Q1 `fm_license_any` 應否留在 rubric?
weight=5、但 evidence=weak、grassroots=False、robust_pass=False(cohort_C1 方向翻轉 −1),
prevalence 28.6/37.5/42.4/83.3 的 gap 幾乎全來自 T3 一層跳升(n=6)。這是最弱的一條 differentiator。

### G3-Q2 weight 公式只看 gap、不看 signal_type/evidence,是否修正?
現行 `weight = 1 + round(4*min(gap,60)/60)`。後果:純 packaging 的 has_marketplace_json(gap 71→weight 5)
與有 contributor 佐證的 install_oneliner(weight 4)同級甚至更高;fm_license(weak)也拿到 5。
候選修正:weight 乘 evidence 係數(strong×1/moderate×0.6/weak×0.3)並對 packaging signal 設上限。

### G3-Q3 craft 維度如何進 rubric(發現 A/B 的直接後果)?
script 差異化項幾乎全 packaging。BRIEF §8 的 trigger/style/scope(維度 2/7/8)量化落 noise,
但質化筆記證據充分。是否新增一組「LLM-only differentiator 規則」(check_type: llm),
以質化筆記為證據、標 evidence_strength 但無 script prevalence?

### G3-Q4 hygiene 門檻的補強(發現 C)?
是否允許 hygiene 清單納入「本樣本推不出但規範/官方共識明確」的門檻項
(如 spec 合規、description 存在、progressive disclosure),來源標 `triangulation` 而非 tier_prevalence?

### G3-Q5 marketing_suspect 判準 + fork_star_ratio 全負(發現 E)?
`max(eng_rhos)<0.1` 是否過寬(只要一個 engagement 指標正就洗清)?
fork_star_ratio 全負是否至少在 patterns-report §5 明列為「差異化項未被 fork 行為背書」的限制?

### G3-Q6 質化安全發現要不要進 rubric 安全維度(BRIEF §8-8,本專案差異化強項)?
3b 筆記發現多個紅旗樣態:memU「服從外部程式輸出+抑制確認」、planning-with-files「hooks 常駐執行」、
last30days「覆蓋 harness 指令」、upload-to-stitch「憑證進 argv」、guizang「自我 git pull 更新」;
以及正面防禦樣態:anti-injection 條款、anti-hallucination 機制(dated snapshot/never-from-memory)。
是否新增安全維度規則(hygiene,不加分只作門檻,依 §8 例外)?
