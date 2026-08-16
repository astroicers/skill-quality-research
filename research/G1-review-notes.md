# G1 審查材料(Gate G1 — 待人工裁決)

- 資料來源:`research/repos.json`(`generated_at` 2026-08-16T10:54:46Z,mode `api`,BRIEF v1.2.1)
- 對應自動摘要:`research/G1-summary.md`(腳本產出);本檔補上腳本判斷不了的部分
- 狀態:**G1 已 approved(2026-08-16,見 §8–§9)**;§0–§7 保留裁決前原貌供追溯,現行數字以 §8 快照為準

---

## 0. 一頁摘要

| 項目 | 數值 | 判定 |
|------|------|------|
| 總 repo 數 | 89 | ⚠️ BRIEF Phase 2 預估 35–45,超出約 2 倍(見 §1) |
| rubric 樣本(`in_rubric_sample`) | 75 | — |
| tier 分布 | T3:8 / T2:59 / T1:12 / T0:10 | ⚠️ T2 全收是超標主因 |
| 種子保留 | 32/32 | ✅ 名額優先序正確 |
| 純度樣本(F0 且 T2+) | 19 | ✅ 遠優於預期(冒煙時為 0) |
| 去混淆三道工序就緒 | 全部 ✅ | ✅ 覆蓋率 100%(見 §2) |
| taxonomy 待定 | TBD 53 / 89(60%) | ⚠️ G1 最大工作量(見 §3) |
| domain 待定 | TBD 23 | ⚠️ 需人工標注 |
| `obra/superpowers` 追址 | 原址即現址 | ✅ 已結案(PHASE0 報告 §4.2) |

---

## 1. ⚠️ 裁決點一:T2「全收」與「35–45 個 repo」互相矛盾

分層名額已生效,T1/T0 各被收斂到 12 / 10(分別丟棄 168 / 176 個):

```
kept:    T3:8   T2:59  T1:12  T0:10   = 89
dropped:               T1:168 T0:176
```

超標完全來自 **T2 = 59**(BRIEF §3 定為「全收(A–D 類)」)。這是 spec 內部的矛盾:

- BRIEF §3 表格寫 T2「全收」
- BRIEF §3 Phase 2 寫「預估 35–45 個 repo(四層合計)」

「35–45」是 2026 上半年 OpenClaw 熱潮**之前**的估算,當時 10k–100k 星的 skill repo 遠少於現在。
兩者今日已不可能同時成立,必須擇一。

**選項**

| 選項 | 做法 | 影響 |
|------|------|------|
| **1-A 尊重「全收」** | 維持 89 個 | Phase 2 clone 量約 2 倍(磁碟/時間);T2 層統計基礎最厚,梯度分析最穩 |
| **1-B 尊重「35–45」** | `--cap-t2 20` 重跑 → 約 50 個 | 貼近原估算;但 T2 是「10k 星級剖面」的主要證據層,砍到 20 會削弱 RQ5 |
| **1-C 折衷** | `--cap-t2 35` → 約 65 個 | 兼顧規模與 T2 統計力 |

> 重跑成本很低:enrichment 快取(`research/.enrich-cache.json`)已存在本機,
> 已成功的欄位不會重打 API,只有新進 repo 需要抓。

**建議 1-A**。理由:BRIEF §3 的「全收」是方法論選擇(T2 是「10k 星級剖面」的證據基礎),
而「35–45」只是一句容量估算、非 spec 約束;砍 T2 會直接削弱 RQ5 的核心產出。
Phase 2 的 clone 量是可承受的工程成本,不是方法論代價。**惟此屬 spec 層取捨,請裁定。**

---

## 2. ✅ 資料完整度:三道工序全部就緒

上一輪(修正前)`nonauthor_pr_count` 因 secondary rate limit 幾乎全滅;本輪修正後:

| 欄位 | 落地率 | 失敗 |
|------|--------|------|
| `author_followers` | 75/75 (100%) | — |
| `author_fame_tier` | 75/75 (100%) | — |
| `prior_fame_proxy` | 74/75 (98.7%) | `not-searchable` ×1 |
| `contributor_count` | 75/75 (100%) | — |
| `nonauthor_pr_count` | 75/75 (100%) | — |
| `fork_star_ratio` | 75/75 (100%) | — |

- ✅ 工序 1 素人復現 — 覆蓋 100%,**純度樣本 19 個**
- ✅ 工序 2 雙結果變數 — 覆蓋 100%
- ✅ 工序 3 機制陳述 — 無資料依賴

唯一缺口:`prior_fame_proxy` 有 1 筆 `not-searchable`(**`vibeeval/vibecosystem`**,T0、followers=0;
原稿誤寫為 `parcadei`——`parcadei/Continuous-Claude-v3` 在 T1 dropped 名單,不在 kept 樣本內,G1 覆核時更正)。
該筆退回以 `followers` 粗分層(followers=0 → F0 無懸念);且該 repo 為 T0,純度樣本(需 T2+)不受影響。

`author_fame_tier` 有 14 筆 null:即 `in_rubric_sample=false` 的 E/F 類,依設計不打 enrichment API 省配額,**非資料缺口**。

---

## 3. ⚠️ 裁決點二:taxonomy TBD 53 筆,且與 Phase 2 有先有雞先有蛋問題

```
TBD:53  D:8  C:8  E:6  B:5  F:4  E?:4  A:1
```

`taxonomy_suggest()` 只認得 E 類(awesome list 的字面特徵),其餘一律回 `TBD`。
而 BRIEF §6 的邊界判定規則是:

> repo 內是否存在 ≥1 個含合規 frontmatter 的 `SKILL.md` → 有則至少 B/C/D,無則 E/F

**這條規則需要 clone 後才能判定**,但 BRIEF Phase 2 又寫「僅對 taxonomy A–D 類執行 clone」。
53 筆 TBD 因此卡住:不 clone 就分不了類,不分類就不該 clone。

**建議解法**:Phase 2 對全部 `in_rubric_sample=true`(75 筆)執行 clone,
clone 後以 `extract_features.py` 的 `skill_md_count` 依 §6 規則回填 taxonomy,
再把判定為 E/F 的排除出特徵矩陣(記錄排除原因,符合 §6「記錄排除原因」的要求)。
代價是多 clone 了最終會被排除的 E/F 類,但那是 `--depth 1` 淺 clone,成本低於人工逐一判讀 53 個 repo。

若採此解法,**BRIEF §3 Phase 2 的「僅對 A–D 類 clone」需在 G1 一併修訂**為
「對 `in_rubric_sample` clone,clone 後回填 taxonomy 並排除 E/F」。

`domain` 同樣有 23 筆 TBD,但 domain 只影響 Phase 4 的分層複算,可延後到 Phase 3 之後補標。

---

## 4. ✅ cohort 切點:對照 created_at 直方圖後的驗證結果

BRIEF §6.5 要求「切點為提案值,Phase 1 需對照 created_at 直方圖確認後定稿」。直方圖:

```
2018-04 … 2025-09   每月 0–3           ← 長尾
2025-10  11  ###########               ← ★ 陡升
2025-11   2  ##
2025-12   5  #####
2026-01  14  ##############
2026-02   8  ########
2026-03  16  ################          ← ★ 峰值
2026-04  12  ############
2026-05   4  ####
2026-06   2  ##
2026-07   2  ##
```

| 切點 | BRIEF 提案 | 直方圖證據 | 判定 |
|------|-----------|-----------|------|
| C0/C1 @ 2025-10 | Agent Skills 發布 | 由每月 0–3 陡升到 11 | ✅ **強支持,建議定稿** |
| C1/C2 @ 2026-02 | OpenClaw 熱潮高峰起點 | 2026-01 已達 14、2026-02 反而回落到 8、峰值在 2026-03 | ⚠️ **切點偏晚**,熱潮實際起於 2026-01 |
| C2/C3 @ 2026-06 | 退潮後 | 2026-05 起回落(4→2→2) | ✅ 方向正確 |

**兩個待裁定事項**

1. C1/C2 切點是否前移到 **2026-01**?移動後分布為 C0:13 / C1:18 / C2:54 / C3:4。
   前移在時序上更貼合資料,但會讓 C2 更肥、C1 更瘦。維持原切點(C1:32 / C2:40)則分層較均衡。
2. **C3 只有 4 個 repo**,無論切點怎麼移都太薄,**不足以支撐 BRIEF §4 要求的「同 launch_cohort 內複算」**。
   建議在 patterns-report 中明列此限制,C3 層的複算結果一律標 `weak`,或與 C2 合併處理。

---

## 5. ⚠️ 裁決點三:T0 抽樣的同域偏斜

BRIEF G1 檢查清單明列「四層抽樣分布合理(**尤其 T0/T1 抽樣不可全是同類同域**)」。

**T0(n=10)** — 已標注的 6 筆中 **4 筆是 `design-ui`(67%)**:
```
TBD:4  design-ui:4  meta-tooling:1  research-analysis:1
taxonomy 全部 TBD
```
T0 是 hygiene 門檻的下界證據層(「缺什麼會掉出 1k 級」),領域過度集中會讓門檻推導帶上 design-ui 的領域特性。

**T1(n=12)** — 分布良好,跨 8 個 domain(code-quality / design-ui / dev-workflow ×2 / media-gen / meta-tooling / security / writing-content + TBD ×4),taxonomy 含 D:3 / E:1 / E?:1 / TBD:7。✅

**選項**:(a) 接受現狀,在報告中標注 T0 的 design-ui 偏斜為已知限制;
(b) 調高 `--cap-t0` 到 15–20 換取領域多樣性;
(c) 改用 domain-stratified 抽樣(需改 `interleave_sample`,工程成本較高)。

**建議 (b)**:T0 只是對照層,擴到 15–20 個成本極低(快取已在,只需補抓新進的),
卻能顯著改善 hygiene 門檻的領域中立性。

---

## 6. G1 檢查清單(BRIEF §3)

- [x] **清單完整性** — 32/32 種子全部保留(名額優先序:種子 > range 抽樣 > 主查詢);
      `obra/superpowers` 追址結案,原址即現址、無改名(證據見 PHASE0 報告 §4.2)
- [ ] **taxonomy 分類正確(尤其 E/F 排除是否合理)** — ⚠️ 53 筆 TBD 待定,且與 Phase 2 有循環依賴(§3)
- [ ] **純度標籤 domain / fame / cohort 標注正確** — fame ✅ 完整;domain ⚠️ 23 筆 TBD;
      cohort ⚠️ C1/C2 切點與 C3 樣本量待裁(§4)
- [ ] **四層抽樣分布合理** — T1 ✅;T0 ⚠️ design-ui 佔已標注的 67%(§5);T2 規模待裁(§1)
- [ ] **verdict:approved / rejected(附修改指示)**

---

## 7. 待裁決事項總表

| # | 事項 | 建議 | 影響範圍 |
|---|------|------|---------|
| 1 | T2 全收(59)vs「35–45」估算 | **1-A 維持全收** | Phase 2 clone 量 |
| 2 | 53 筆 taxonomy TBD 的解法 | **clone 後回填,並修訂 §3 Phase 2 措辭** | Phase 2/3 流程 |
| 3 | cohort C1/C2 切點是否前移至 2026-01 | 資料支持前移,但兩者皆可辯護 | Phase 4 分層複算 |
| 4 | C3 僅 4 筆 | 標為已知限制,複算結果封頂 `weak` | Phase 4 證據強度 |
| 5 | T0 的 design-ui 偏斜 | **`--cap-t0 15~20` 重跑** | hygiene 門檻中立性 |
| 6 | `prior_fame_proxy` 1 筆 `not-searchable` | 退回 followers 粗分層,確認可接受 | 單一 repo 的 fame 標籤 |

事項 1 與 5 若都採建議,重跑指令為:

```bash
python3 scripts/collect_repos.py --cap-t0 18
```

快取已在本機,只需補抓新進的 T0 repo,約數分鐘。

---

## 8. G1 裁決紀錄(2026-08-16,人工 binary 裁決 via AskUserQuestion)

| # | 事項 | 裁決 | 已執行動作 |
|---|------|------|-----------|
| 1 | T2 全收 vs「35–45」 | **1-A 維持全收** | BRIEF §3「35–45」標記為過時預估(非 spec 約束) |
| 2 | taxonomy TBD 循環依賴 | **clone 後兩段式回填**(script 判 ≥1 SKILL.md;0 SKILL.md 者進候補排除名單,覆核 v1.2.1 CLAUDE.md-only 例外後才排除) | BRIEF §3 Phase 2 措辭已修訂 |
| 3 | C1/C2 切點 | **前移至 2026-01** | `collect_repos.py` COHORT_CUTS 已改,BRIEF §6.5 定稿 |
| 4 | C3 樣本過薄 | **標已知限制 + weak 封頂**(不與 C2 合併) | BRIEF §6.5 已註記;patterns-report 需明列 |
| 5 | T0 design-ui 偏斜 | **(b) cap-t0 擴至 15–20** | 預設 cap-t0=18,已重跑;BRIEF §3 表格已修訂 |
| 6 | prior_fame_proxy 缺值 | **接受 followers fallback** | §2 repo 名已更正(vibeeval/vibecosystem,非 parcadei) |

### 裁決後重跑快照(取代 §0 的數字)

- 總 repo:**97**(+8 個新 T0,無移除);rubric 樣本 **82**
- tier:T3:8 / T2:59 / T1:12 / **T0:18**
- cohort(新切點):C0:13 / C1:20 / C2:59 / C3:5
- 種子 32/32 保留;純度樣本 19(與裁決前逐筆相同)
- 資料完整度:82/82 全欄位 100%,唯 `prior_fame_proxy` 81/82(vibeeval,已裁決接受)
- taxonomy TBD 增至 60(新 T0 中 7 筆 TBD、1 筆 `rohitg00/awesome-claude-design` 被啟發式標 E? 排除於 rubric,
  故 rubric 內 T0 實為 17)——TBD 依裁決 2 於 Phase 2 clone 後回填
- Phase 2 已知跳過:`nexu-io/open-design`(1.8GB)、`yschimke/compose-ai-tools`(1.5GB)超過 BRIEF 500MB 上限

### ⚠️ 裁決 5 執行結果的誠實回報:擴樣未治好 design-ui 偏斜

新 8 筆 T0 中啟發式標注 4 筆 design-ui、2 筆 writing-content、2 筆 TBD。
擴樣後 T0(n=18)已標 12 筆中 design-ui 佔 8(仍 67%;佔全體 44%)。
原因:T0 的 900+ 星頭部帶(interleave 抽樣的 stars-sorted 半邊)本身就 design 密集,
且部分標籤疑似啟發式誤標(如 Claude-Code-Agent-Monitor、Skills-Manager 標成 design-ui,
更像 meta-tooling)。**處置:T0 的 6 筆 domain TBD 與疑似誤標於 Phase 3 人工定案後重新評估
偏斜幅度;hygiene 門檻推導時將 design-ui 領域特性列為已知限制(等同原選項 (a) 的標注義務)。**

### G1 checklist 收尾狀態

- [x] 清單完整性(種子 32/32;superpowers 已結案)
- [x] 抽樣分布:T2 規模已裁(1-A);T0 已擴樣,殘餘偏斜轉為已知限制
- [x] cohort:切點定稿 2026-01;C3 weak 封頂
- [x] fame:完整;1 筆 fallback 已裁決接受
- [~] taxonomy / domain:**依裁決 2 延至 Phase 2 clone 後回填**(此為裁決核可的流程,非未決事項)

---

## 9. G1 最終裁決:**approved**(2026-08-16)

T0 design-ui 殘留偏斜依 §8 處置轉為已知限制(Phase 3 domain 人工定案後重評,
必要時單調擴 T0 補抽,不作廢已完成工作)。G1 關閉,核准進入 Phase 2。
