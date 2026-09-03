# rubric 3.7.0 首戰使用輪(2026-09-03)

> rubric **3.7.0** / 工具 **2.3.12**。語料 `clone-manifest-rubric370-wave.json`(7 標的,
> GitHub 搜尋對 140 條既往去重);預登記 `rubric370-wave-preregistration.md` 先 commit。
> ⚠️ 含具名 craft 證據,加入審查者禁讀清單。盲判逐字另檔。
> 判讀依判讀包協定 v3(`judge-package-protocol.md`)——**首次全程**。

## 總表(作者判;集合逐樣本全文讀 + 聚合;verdict = `craft_verdict_rollup()`)

| repo | SKILL× | L-001 | L-002 | L-003 | L-004 | verdict | lint pkg |
|---|---|---|---|---|---|---|---|
| bitjaru/styleseed | 23×2(抽5) | good(router desc + ss-dial 反模式自限) | good(dial 的 why 稠密+ramp 表) | good(**單選路由表+bounded clarification**,位階梯中集合達成) | **mixed(序2)**:a11y 樣本——機制在(verify-with-skin+re-gate ≥80 迴圈+無截圖不得宣稱驗證)但覆蓋外裸露記名[Radix「自動處理 ARIA」runtime 斷言;44px 掛 WCAG 2.2 AA 傘下**需查證,記疑不判罪**] | **AWN** | 7/14 T1 |
| Tugoukezhang/workbuddy-skills | 80 目錄/141 檔(抽5) | good(五樣本觸發面皆實;自定觸發欄×2 記 findings) | **mixed**(content-repurposer 行銷頁型樣本) | **mixed**(位階梯:README 目錄+一行鉤,但**重複對** frontend-dev/前端开发 等使「何時用哪個」自答失敗=弱形) | **mixed**(序5-實質 2/4=**恰半→分流句首開**,記名 content-repurposer[平台字數規格=載重無機制]、data-model-creation[vendor DSL 面無機制;鄰檔 web-dev 反而有 never-from-memory]) | **NR** | 6/14 T1 |
| photon-hq/skills | 5(全讀) | **mixed**(3/5 desc 帶 Keywords 塊,含裸通用詞 login/terminal/github actions=**收編**) | good | good(CLI/SDK 邊界註+分支路由表) | **mixed**(F8:chat-adapter 單樣本序5-實質[無釘版無機制、API 面即課文]→聚合 mixed 記名;imessage/spectrum 為**釘版合約+文檔漂移處置**的序1 標竿) | **NR** | 3/14 <T1 |
| LearnPrompt/andrej-karpathy-skills | 15(抽5) | good(觸發語皆品牌限定;README 自知撞詞) | good | good(router+每檔上下游工作流表) | **mixed**(序2 記名 supply-chain[工具推薦殘餘覆蓋外];餘樣本 cite-docs 指令+證據先行契約) | **AWN** | 6/14 T1 |
| appleboy/skills | 7(抽5) | good | good(**patterns 級**:遮罩取捨全說理、race 分析、fix-report 範本) | good(位階梯小集合:名稱自明+互引=目錄即足) | **good**(codex/copilot-review 皆有**措辭漂移 fallback**——bot 換詞不誤停;序1) | **approved** | 6/14 T1 |
| JetBrains/skills | 129(抽5) | good | **mixed**(yeet 樣本裸命令式) | **mixed**(位階梯:策展+逐檔溯源+**Cisco skill-scanner CI** 是 packaging/信任面強項,但 129 平鋪近重複族 vue/vue-best-practices 自答失敗=弱形) | **mixed**(記名 speech[模型釘名+能力矩陣裸];gws-docs 的 schema-inspect 為序1) | **NR** | 2/14 <T1 |
| yan-labs/yan-skills | 9(抽5) | **mixed**(autopilot 收編泛修復請求入無人值守;rankup **捕獲即路由**新形→ledger) | good(硬規則\|理由雙欄表通篇) | good(rankup 逐句路由到段/姊妹 skill=dispatcher;codex 雙能力共享同一本體不塌) | **mixed**(序2 記名 rankup[2026 搜索範式 desc 載重]、codex[CLI 行為裸];autopilot 的取證用詞分級+rejected.md 紀律是真機制) | **AWN** | 7/14 T1 |

**1 approved / 3 AWN / 3 NR。** hygiene error 全零(七件 H-001 皆過)。
security:workbuddy S-003 ×2 複核——`cred_in_argv`(medium)命中含 **vendored
nano-banana-pro 副本(AI绘图)**,dirty 波已實錘之 `--api-key` 判定直接移轉,成立、
warning 不翻 verdict;`self_update`(low-static)命中 clawhub sync 類安裝指示,記 findings。
speech 的「Never ask user to paste key in chat」與 imessage 的 untrusted-data 不變式為 S-101 型正面樣態。

## 六刀 rung 開火紀錄(預登記 §1)

| rung | 開火 | 單讀? |
|---|---|---|
| L-003 位階梯 | **三格全開**:good(styleseed 中集合顯式路由;appleboy 小集合名稱自明)、mixed(workbuddy 重複對;JetBrains 129 平鋪近重複族)、poor 未見 | ✓ 自答提問在四案上給出可分辨答案;「發布打包不充抵」在 JetBrains 上有實用(策展≠路由) |
| 傾倒判別 | codex-review/cloudbase 等多次「兩維各計 vs 只計 L-004」判別 | ✓ |
| L-001 自定觸發欄 | **×3 形**:`read_when`(2D游戏)、`description_zh/_en`(content-repurposer)、frontmatter 前置散文致 desc 可能不被載入(self-improving) | ✓ 記 findings 不改值夠用;第三形(前置散文)是**載入器根本讀不到**——比「不保證消費」更深一層,記觀察 |
| 序5 輔助線+聚合 poor 句要件 | **恰半分流首開**(workbuddy 2/4→mixed 記名);量級輔助線在 content-repurposer(整節=實質)與 supply-chain(一行工具=殘餘)兩側可分 | ✓ |
| 序1 載重判別 | styleseed 44px(**規則內容即數字→載重**,與 remotion 9成的修辭側相反向)+ appleboy gh 版本釘(殘餘) | ✓ 兩側可分 |
| 樣張判別+傘式 | **反向雙開**:cloudbase auth 流程碼=載具(換偽碼教學仍立→排除)vs js-testing 型 API 面=本體;傘式:WCAG 2.2 AA 傘蓋 44px 之涵蓋面存疑(記疑不判罪) | ✓ |

**六刀全部開火、全數單讀。** 3.7.0 新句無一在本語料上出現 verdict-swinging 兩讀。

## 誤判/friction(→ ledger 蓄積)

1. **「捕獲即路由」無裁定**(yan-labs/rankup):desc 枚舉**他人 job 的觸發語**
   (帮我改稿/文案/Reddit 調研)但本體逐句路由到姊妹 skill——收編判別會判 mixed,
   dispatcher 例外又不豁免 desc 層。總控型的 desc 收編與 body 路由的抵扣關係無條文
2. **自定觸發欄第三形**(workbuddy/self-improving):frontmatter 前置散文使整個
   frontmatter 可能不被解析——desc 寫得再好載入器也讀不到。評估面條文只處理
   「非標準欄」,未處理「標準欄因格式損壞而失效」;與位置規則(照字面讀即壞)的
   關係待裁定
3. **44px/WCAG 類「傘下錯掛主張」的查證義務**(styleseed):傘式引用句要求
   「出處實際涵蓋」,但審查者無法在不查外部標準的情況下裁定涵蓋面——
   「記疑不判罪」是我本輪的臨時處置,宜入正文(或明訂:涵蓋面存疑記 findings、
   不得憑記憶判罪──與「拿間接訊號當直接證據」教訓同族)

## F4 誤判率(方向訊號)

| 輪 | 對象 | 新 ledger 列 | 率 |
|---|---|---|---|
| fresh 波(勘誤後) | 12 | 6 | 0.50 |
| dirty 波(定稿勘誤後終值) | 7 | 9 | 1.29 |
| **rubric370 波(作者半;盲判前)** | **7** | **3** | **0.43** |

confound 照預登記(盲判定稿到貨可能追加——dirty 波即為前例,此數為**中途讀數**)。

## 過程誠實記錄

- manifest 首版**全空 SHA 已 commit**——`tr '/' '__'` 只換單字元、路徑對不上,
  腳本靜默吞錯。amend 修正並補斷言(SHA 長度、計數>0)。08e9e01 型第 3 例,
  self-caught 於 push 前
- copilot-review 曾想用 diff 指令證「雙生」代替閱讀,指令失敗後**改回實讀**
  (token-optimizer 教訓的正向應用:讀了,而不是拿工具輸出當讀過)
- JetBrains 與 workbuddy 均**vendored 已知家族**(anthropics/openai/google 上游;
  viper nano-banana 副本、clawhub skill)——依協定 v3 選樣端標記,
  **盲判標的刻意避開此二者**(遮蔽清單會爆炸且環境必然認出),選 styleseed+photon-hq

## 盲判抽查(協定 v3 首全程)

抽選:**styleseed** 與 **photon-hq**(開火最多且零 vendored 重疊)。
前哨指定攻擊:語意監看名單全部條目(含第五批預登記的兩條 M 衍生判別句——
它們自 dirty 語料歸納,對本波語料屬**跨語料首測**)+ fp-registry 警告面 + 遮蔽悖論面。
判讀者 prompt 含環境既識申報必填段。逐字與裁決:見本檔下方增補與 blind 目錄。
**採信一律暫定**;後到產出強制勘誤複核。
