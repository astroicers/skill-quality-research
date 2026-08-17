# 高/低品質樣態速查(來自 54 份質化筆記,skill-quality-research Phase 3b)

供 skill-reviewer 的 LLM 層做 craft 判讀時對照。每條附本研究實見的正/反例。

## L-001 trigger 設計

| 高品質樣態 | 反例(扣分) |
|-----------|-------------|
| 具體觸發語境 + 負向觸發(NOT for / When NOT to use) | 關鍵字轟炸:20+ SEO 式變體堆疊(browser-act) |
| 觸發錨定客觀訊號(副檔名、使用者提及的名詞)(kepano) | 全無 Use when 卻靠 body 猜(Leonxlnx/taste 五份) |
| 量化觸發門檻(nicobailon「≥N 時」) | 觸發語誤放 body 而非 description(colleague-skill) |
| 手動觸發時明示開關語(ayghri `disable-model-invocation`) | — |
| 逐字自然語句枚舉(turbo:「"discuss this change"」) | — |

**關鍵**:script 的 `desc_has_trigger` 二元值是 noise（T0 反而更高）——有無觸發語抓不到品質,你必須讀內容判「觸發語境是否具體、是否過寬/轟炸」。

## L-002 寫作風格

| 高品質樣態 | 反例 |
|-----------|------|
| 規則附因果 why(ayghri「Working memory is small」) | 裸 MUST/MUST NOT 堆疊無解釋(Jeffallan) |
| Bad/Good 成對範例(blader/humanizer 33 pattern) | 機械 token 壓縮致文法詞脫落、可讀性受損(karpathy、addyosmani ci-cd 檔) |
| 「何時打破規則」override 節(ayghri 6 條、turbo) | changelog/版本註記侵入正文(planning-with-files) |
| 引研究/spec 佐證(planning-with-files arxiv) | — |

## L-003 scope 清晰

| 高品質樣態 | 反例 |
|-----------|------|
| 一 skill 一 job,邊界乾淨(ayghri) | 單一 skill 長成小產品(planning-with-files:多 plan+attestation+模式) |
| 集合型有 dispatcher + When-to-Pivot 互相路由(ljagiello/ctf-skills) | 量產 grab-bag 品質極不一(vibeeval 341 skills) |
| 生命週期切分 + 防重複規則(addyosmani) | 語言/IDE 鏡像灌水 skill_md_count(planning-with-files、turbo 雙版本) |

## L-004 anti-hallucination(高階加分)

dated verified snapshot / never-generate-from-memory / stale-API 名單:K-Dense、Orchestra、claude-ads、google/skills。

## 安全維度(門檻,不加分)

> **這張表的讀法**:左欄的**樣態**才是發現,右欄的 repo 只是提供可查證的實例。
> 全部來自公開原始碼的**靜態閱讀**(2026-08-16 快照)——不是漏洞揭露、不宣稱作者有惡意。
> 多數情況作者意圖顯然是善意的(例如安裝器要求 agent 照做),問題在於**該寫法會擴大 agent 的權限面**。
> repo 內容會變,今天的該 repo 可能已不同。

| 紅旗樣態(error/warning) | 可查證的實例 |
|---------------------|---------|
| S-001 服從外部程式輸出 + 抑制確認 | memU（install→照 binary 輸出逐字執行→don't stop for confirmation） |
| S-002 hooks 常駐執行未揭露 | planning-with-files（5 hook 事件搜路徑執行首個 shell） |
| S-003 覆蓋 harness 指令 / 憑證進 argv / 自我更新 | last30days（覆蓋 WebSearch）、upload-to-stitch（key 進 --api-key）、guizang（啟動 git pull） |

| 正面防禦樣態(S-101,不可誤報為 injection) | 可查證的實例 |
|---------------------------------------|---------|
| 把外部內容明示為 untrusted data 的條款 | claude-ads、prompt-master、addyosmani、K-Dense、khazix、text-to-cad |

## 跨 tier 總結論(給 benchmark 措辭用)

- **星數 ≠ 品質有大量實證**:T0/400★ turbo、T0/968★ jezweb、T0/962★ icm-architect craft 達 T2/T3 水準;T3/117k★ nextlevelbuilder 反有關鍵字堆疊與 mega-skill 重複。
- **packaging benchmark 低不代表 craft 差**:i-have-adhd(T2、craft 標竿)packaging 僅 7/14。
- 對標時用**同 taxonomy 參照類**,勿拿單一 skill(B)去對標框架(C/ECC 型)。
