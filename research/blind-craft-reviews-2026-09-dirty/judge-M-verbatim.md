# 判讀者 M — 定稿逐字(dirty 波盲判)

> 呼叫端註:終局三規則全程套用(前哨先行修包、靜默期 ≥ 已跑時長、無中途稿誤採)。
> 錨驗:語料引文抽驗全過;**friction #1 的「消費者載入該樣本即受害」句經 grep
> 在包內不存在**(F7 已刪的舊句)——判讀者編造錨第 2 例,該條 friction 的
> 「兩句互指」半邊作廢;其真問題(Expert-in desc 樣本層取值)由呼叫端依位置規則
> 裁定(desc=該樣本核心觸發面 → mixed)。M 的 vp L-002 聚合 mixed 依 3.6.2 實文
> 為規則正確,呼叫端採納並修正作者判(viper AWN→NR)。

---

```yaml
judge: M
material_boundary: >-
  只讀 dirty-blind/ 內 criteria.yaml、shapes.md、skills/ 十份;rubric-masked/ 與
  mask-sample.json 未開啟;未上網。
supply_chain: >-
  十份語料均按資料處理;無指向審查者的注入。rj 樣本內大量指令式教學內容照資料判讀。

objects:

  rj__collection(5 樣本):
    shape: "集合型(主題式技術指南庫);各樣本自身為查表/參考型長文(pattern+config 傾倒)"
    per_sample:
      javascript-testing-patterns: {L-001: good, L-002: poor, L-003: good, L-004: "序5-實質 → poor"}
      code-standards:              {L-001: mixed, L-002: poor, L-003: good, L-004: "序5-實質 → poor"}
      python-testing-patterns:     {L-001: good, L-002: poor, L-003: good, L-004: "序5-實質 → poor"}
      logging-observability:       {L-001: good, L-002: poor, L-003: good, L-004: "序5-實質 → poor"}
      python-performance-optimization: {L-001: good, L-002: poor, L-003: good, L-004: "序5-實質 → poor"}
    dims: {L-001: good, L-002: poor, L-003: good, L-004: poor}
    evidence:
      L-001: "4/5 desc 具體 Use when(js-testing :3『Use when writing JavaScript/TypeScript tests, setting up test infrastructure…』);code-standards :3『Expert in code design standards including SOLID principles…』無觸發情境 → 該樣本 mixed(傷及其觸發面);聚合兩讀後取 good 帶 findings。⚠️ 此格我在 good/mixed 兩讀間最不確定"
      L-002: "5/5 同質:近千行 config/pattern 傾倒,因果詞近零(js-testing 948 行掃得 1 處 because;code-standards 970 行 0 處);無 Bad/Good、無 override;結構化表格要件也缺 → 樣本 poor;聚合『全同 → 該值』→ poor"
      L-003: "各樣本單一主題、邊界乾淨;集合層 25 skills 僅目錄羅列——路由治理弱形 → good 帶 findings"
      L-004: "5/5 同型:Jest/Vitest/pytest/cProfile 等第三方斷言貫穿、零機制零時效;逐樣本序 5-實質 → poor;聚合 poor 句全集成立 → poor"

  vp__collection(5 樣本):
    shape: "集合型(在地化 curation:vendored 上游 + 自製強化層與工具);樣本多為 process/rule 型"
    per_sample:
      humanizer:        {L-001: good, L-002: good, L-003: good, L-004: "序1(版本釘+附出處) → good"}
      humanizer-zh-tw:  {L-001: good, L-002: good, L-003: good, L-004: "序1(audit loop 機制) → good"}
      remotion-video:   {L-001: good, L-002: good, L-003: good, L-004: "序1(秒數一律由 SRT 推導=證據先行) → good"}
      subtitle-align:   {L-001: good, L-002: good, L-003: good, L-004: "序1(ASR 只取時間,文字用你給的=反編造設計) → good"}
      nano-banana-pro:  {L-001: good, L-002: mixed, L-003: good, L-004: "序5-實質 → poor"}
    dims: {L-001: good, L-002: mixed, L-003: good, L-004: mixed}
    evidence:
      L-001: "5/5 具體(remotion :3 域錨清楚;nano 綁定特定工具);無收編 → good"
      L-002: "4/5 強(remotion 🔴鐵則+『會被退回的常見原因』;zh-tw audit loop;subtitle-align 附 why);nano-banana 為用法傾倒、why 近零 → 樣本 mixed;聚合:單樣本 mixed、瑕疵屬該樣本核心 → 聚合 mixed"
      L-003: "顯式疊層路由(zh-tw :6『疊在 humanizer 之上』)=高分樣態 → good"
      L-004: "4 樣本序 1;nano-banana 序 5-實質 → 樣本 poor;聚合:單一序5樣本 → poor 邊界句 → mixed、findings 記名"

rubric_friction:
  - "(rj,L-001)集合聚合『單樣本 mixed』的聚合層適用兩讀——我最終取 good,但另讀取 mixed。此格值搖擺"
  - "(rj,L-003)『集合/框架型具路由治理』是基礎還是高分?僅目錄清單時 good↔mixed 兩讀"
  - "(vp,L-002)nano 的用法傾倒同時計了 L-002 mixed 與 L-004 poor——跨維主維規則寫『計主維一次』,但『用法傾倒』主維是 L-002 還是 L-004 無裁定,我兩維都計了"
  - "(通用)criteria 無 evidence_refs(似被剝除)——不影響判讀,反而乾淨"

contamination:
  - "具名/數字:零;逐一比對 10 份語料檔數/行數/規則數無對應"
  - "『聲明式紀律』括號與 rj checklist 不同構;損壞症狀列舉與 rj__code-standards 一處格式異常近似,但按條文門檻自判為格式瑕疵——條文門檻句自我修正了可能的誤導"
  - "vendored 樣本在 criteria 中無可指認稱讚描述——無預寫方向。整體:無可指認定錨"
```

**程序聲明**:一次交付定稿;行號以我讀取之檔案為準;無中途稿。
