# 自家兩工具 skill 的 3.8.0 自審(2026-09-03,使用驅動輪)

> 動機:盤點確認外部零未審對象後,發現 **skill-reviewer 上次被審是 rubric 1.x
> 時代的 self-audit r1**,其後判準改了三個 major 版——自家高風險標的反而是
> 最舊判定。⚠️ **作者=審查者=被審者的作者**,利益衝突全程在場;
> 本檔結論標「自審」,建議下輪盲判抽查覆核。⚠️ 含具名 craft 證據,審查者禁讀。

## skill-reviewer/SKILL.md(204 行;rubric 3.8.0 / 工具 2.3.14 現行版)

| 維 | 值 | 錨 |
|---|---|---|
| L-001 | good | desc 全為限定式複合詞(「review skill」「評估 SKILL.md」,N 對同構詞的裁定);name 前綴佐證(第六批刀8 首用);findings:無 NOT-for(高分面缺) |
| L-002 | good | 方法論前提整段 why;step 5「複核=去查不是憑印象」附實錯教訓;措辭正反例並列 |
| L-003 | good | 單一 job;gate-checker 模式例外顯式;references 相對路徑路由 |
| L-004 | **good(序1)** | 機制稠密:step 5 三動作協定(實測→grep→讀畢才判=證據先行)、confidence=舉證責任+drift-guard、references 相對路徑=權威源機械同步(CI 鏡像斷言)。findings(殘餘不改序):具名 FP 例一行屬殘餘;自述統計為版控內事實 |

**verdict(自審)= approved**(0 mixed)。

## readme-reviewer/SKILL.md(195 行;rr rubric 0.4.0)

| 維 | 值 | 錨 |
|---|---|---|
| L-001 | good | desc 全限定式;findings:無 NOT-for |
| L-002 | good | 「權重是選的不是量出來的」誠實段+41/41 敘事作為規則 4 的 why;「可以說/不可以說」對照對 |
| L-003 | good | 單一 job;與姊妹專案分界句;形狀表路由讀法 |
| L-004 | **good(序1)** | 機制:序號必填、canonical 單一出處(相對路徑)、「鏈腐世界知識須具名」聲明紀律。**第五批序1 判別句乾淨首用於自家**:κ 數字與 41/41——模型行動於「先懷疑 R-004」這條**規則**,數字是修辭支撐→非載重 findings,不降序 |

**verdict(自審)= approved**(0 mixed)。

## 本輪真正的產出:lint 對自家 repo 的兩個形狀盲點(→ ledger)

1. **evals/fixtures 污染**:故意壞的夾具 SKILL.md 入 H-005 warning,且
   `craft_llm_todo` 確定性抽樣把 **5 格中 4 格抽給了測試夾具**——外部審查者
   審本 repo 會浪費 4/5 的 craft 名額在故意壞的檔上
2. **偵測器文件型 FP**:SKILL.md 引用「ignore previous」等攻擊樣例觸發 S-001、
   patterns.md 描述憑證案例觸發 S-003——偵測器打中自己對攻擊的**描述**。
   step 5 複核紀律接得住(本輪複核:全 FP),但這是繼 anthropics FP 類、
   workbuddy 安全 skill 後的第三批同型實例

兩者同根:**lint 對「工具開發/偵測器文件」形狀無排除規則**。單源雙實例,
入 ledger 一列蓄積(1/5–10,續蓄)。

## 誠實邊界

- 兩個 approved 都是作者自判,證據錨在但**視角是同一顆腦**;下輪任何盲判波
  可把這兩檔混入語料覆核(名字須入遮蔽清單——它們在每個判讀者的宿主環境裡,
  環境既識申報必然命中,屆時照協定 v3 處理)
- 本輪含三條新刀的首次自然使用:name 前綴佐證(刀8)、序1「行動於規則抑或
  數字」(第五批刀)在 κ 數字上乾淨分流、傘式內文出處(rr 的 Standard Readme
  具名)——皆單讀
