# Inter-rater 一致性量測協定(2026-08-17 定稿,**尚未執行**)

## 為什麼這是本研究最大的未量測缺口

本研究的核心結論是「**星數關聯的是打包面,不是內容工藝**」,結論是
「所以 lint 只能當 packaging 過濾器,**craft 非靠 LLM 質化判讀不可**」。

於是 skill-reviewer 的主判落在 craft 那一層(`L-001`..`L-004`)。
但整個專案**從未量過兩個獨立審查者對同一個 skill 會不會給出同樣的 craft 結論**。
如果不會,那麼:

- `research/qualitative_notes/` 的 54 份筆記是**單一審查者**的判斷
- round 2 為了消除誤判而加的 **7 個例外欄位**,全部源自單一審查者的判讀
  —— 它們可能是修正,也可能是**對單一審查者偏好的過度擬合**,目前無法區分
- G5 的 craft 降 YELLOW_FLAG 決策,建立在一個未知穩定度的判斷上

deterministic 那一層沒有這個問題(lint 是純函式,已有 selftest + 跨 5 個 Python 版本
+ Windows 的一致性驗證)。**問題完全落在 craft 這一層,也就是最重要的那一層。**

## 這個協定量什麼、不量什麼

| 量 | 不量 |
|---|---|
| 兩位以上獨立審查者對同一 skill 的 craft 判定是否一致 | 判定是否「正確」(沒有 ground truth) |
| 哪些維度(L-001..L-004)最不穩定 | rubric 是否預測星數 |
| round 2 的 7 個例外是否在不同審查者身上同樣觸發 | 審查者能力高低 |

**一致性高 ≠ 判準好**(兩個審查者可以一致地錯);**一致性低 = 判準不可靠**,這是單向推論。
所以低分是明確的壞消息,高分只是「沒有排除掉這個問題」。

## 樣本(**已預先登記**,見 `research/inter-rater-sample.json`)

15 個 repo,從 54 個 rubric 樣本中**確定性**抽出:各層依 `sha1(full_name)` 排序取前
`round(15 × 該層n / 54)` 個(至少 1)。分布 T0:2 / T1:2 / T2:9 / T3:2,與母體同比例。

**為什麼是確定性規則而非隨機或人挑**:與 `phase3b_sample` 同一道紀律——
樣本清單在跑之前就寫死並進 git,事後無法挑對自己有利的。

**快照**:重新 clone,把每個 repo 的 commit 釘進 manifest。
`research/repos/README.md` 已載明重建拿到的是上游 HEAD 而非原研究快照——
**這對本量測不構成問題**:inter-rater 量的是審查者之間的一致性,
只要求所有審查者看到**完全相同的位元組**,不要求那是原始快照。
(但因此**不得**把本次判定拿去和 `qualitative_notes/` 的舊筆記比對——那會混入內容漂移。)

## 執行步驟

1. **重建語料並釘 commit**
   ```bash
   ONLY=$(python3 -c "import json;print(','.join(r['full_name'] for r in json.load(open('research/inter-rater-sample.json'))))")
   python3 scripts/clone_repos.py --only "$ONLY" --dest research/inter-rater-repos
   # → commit 記錄在 research/clone-manifest-inter-rater-repos.json
   ```
   ⚠️ **務必用不同的 `--dest`**。2026-08-17 修正前,manifest 一律寫死
   `research/clone-manifest.json`,不論 `--dest` 指到哪——重跑會靜默覆蓋掉
   原始研究快照的 commit 紀錄(`research/repos/` 本身是 gitignored,那份 manifest
   是唯一紀錄)。現在 manifest 路徑跟著 dest 走,由 `clone_repos.py --selftest` 斷言。

2. **每個 repo 先跑 deterministic 層,產出交給所有審查者的同一份輸入**
   ```bash
   mkdir -p research/inter-rater
   for d in research/inter-rater-repos/*/; do
     python3 skill-reviewer/scripts/lint_skill.py "$d" --json \
       > "research/inter-rater/$(basename "$d").lint.json"
   done
   ```
   lint 輸出對所有審查者相同(它是純函式),所以它進共同輸入,不是變因。

3. **派 3 位獨立審查者**,每位拿到且只拿到:
   - 該 repo 的 SKILL.md(依 `phase3b_sample` 規則抽的 ≤5 份)
   - 上一步的 lint JSON
   - `skill-reviewer/SKILL.md` 的步驟 3–5 + 兩份 rubric

   **必須隔離的東西**(否則量到的是抄襲不是一致性):
   - 彼此的輸出
   - `research/qualitative_notes/`(會錨定)
   - `research/patterns-report.md` 的 §3 反模式清單(會錨定)
   - 本協定的「預期」段落(本文件刻意不寫預期值)

4. **每位審查者對每個 repo 的每個維度輸出單一標記**:
   `good` / `mixed` / `poor` / `n/a`(`n/a` = rubric 的 exemption 條款成立)

5. **計分**
   ```bash
   python3 scripts/agreement.py research/inter-rater/ratings.json --by-dimension
   ```
   `ratings.json` 格式見 `scripts/agreement.py` 檔頭;item id 用
   `<repo>::<dimension>` 才能分維度計分。

## 判讀規則(**先寫死,避免事後找有利解釋**)

- **不設通過門檻。** kappa 沒有普世門檻,Landis & Koch 的標籤是慣例不是定律。
  `agreement.py` 會印它,但那是參考,不是判準。
- **必須併看 kappa 與成對一致率**(prevalence paradox:某類別罕見時 kappa 會失真)。
- **n=15 很小,kappa 會不穩定。** 這是已知限制,不是執行失誤;報告時照實寫。
- **真正的產出是分歧本身,不是那個數字。** 每一則三位審查者判不同的案例,
  都要逐條讀:是 rubric 條文有歧義(→ 改條文)、還是判斷本來就主觀(→ 在 rubric
  標記為主觀維度並降低其在總評的份量)。這才是這次量測的可行動輸出。
- **`n/a` 的一致性要單獨看。** round 2 的 7 個例外欄位就是靠 `n/a` 生效的;
  如果三位審查者對「例外是否成立」意見分歧,那些例外就是過度擬合的證據。

## 執行後必須更新的地方

- `README.md` 的統計限制:把「未量測」換成實際數字(**無論好壞**)
- `research/EXECUTIVE-SUMMARY.md` 的措辭紀律段
- `CLAUDE.md` 未竟事項表的該列
- 若分歧顯示某條 rubric 有歧義 → 改條文並遞增 `rubric_version` 的 major

## 成本與現況

3 審查者 × 15 repo = 45 次獨立 craft 判讀,是 agent 密集的工作。
協定與計分腳本(`scripts/agreement.py`,已有 selftest 對照 Fleiss 1971 公認值 0.210)
都已備妥且可直接執行;**缺的只是執行預算**。

在執行之前,任何引用 craft 判定的地方都應附帶一句:
**「craft 判定的審查者間一致性尚未量測」**。
