# ayghri/i-have-adhd（T2 / taxonomy B / 20,993 stars）

## 抽讀樣本
- skills/i-have-adhd/SKILL.md（全檔 141 行）

## trigger 設計：good
- 明確選擇「僅手動觸發」：`disable-model-invocation: true`，description 寫清楚開關語：「Invoke with /i-have-adhd; stays on until "stop adhd mode"」。
- description 前半是可掃描的能力摘要（「lead with the next action, number multi-step work, restate state across turns」），對 output-style 類 skill 而言，手動觸發 + 明示 persistence 是正確設計，完全不 pushy。
- body 內建 Persistence 節處理「規則何時失效」的模糊地帶：「If you are unsure whether they still apply, they do.」

## 寫作風格：good
- 教科書級：先給 5 條認知科學式的 why（「Working memory is small. Anything not on screen is forgotten」），再推出 10 條規則，每條附 Bad/Good 對照例。
  證據：「Bad: "This will take some work." Good: "About 15 minutes if tests already cover this."」
- 罕見地寫了「何時打破規則」（6 條 override：破壞性操作、debug spiral、規則與任務衝突時「the task wins; the shape stays」），避免規則被機械執行。
- 收尾有可自檢的 Pre-send check（「delete the first sentence if it announces what you are about to do」）。

## scope 清晰度：good
- 單一 job-to-be-done：把輸出塑形成 ADHD 讀者可行動的格式。不碰工具、不碰流程、不碰領域知識，邊界乾淨。
- repo 僅 2 個 SKILL.md，無湊數現象。

## 其他觀察
- 無 injection-suspect。
- 本檔是「行為塑形類（taxonomy B）」的品質上界錨點：why → rules → 例外 → 自檢的完整結構，且全檔 <1500 詞。rubric 中「解釋 why 的密度」「Bad/Good 對照例存在」「override/例外節存在」可由此類樣本校準。
