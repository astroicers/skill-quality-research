# DietrichGebert/ponytail（T3 / B / 103,682★）

## 抽讀樣本
- skills/ponytail-debt/SKILL.md
- skills/ponytail-gain/SKILL.md
- skills/ponytail-help/SKILL.md
- skills/ponytail-review/SKILL.md
- skills/ponytail/SKILL.md

## trigger 設計：good
- 每個 description 都列出具體觸發語並含負向排除。證據：「Use when the user says "ponytail debt", "/ponytail-debt", "what did ponytail defer"」（ponytail-debt）。
- 主 skill 適度 pushy 但有明確 non-trigger 條款：「Do NOT use for non-coding requests (general knowledge, prose, translation…)」。
- one-shot vs persistent mode 在 description 裡就講清楚（「One-shot report, changes nothing」），觸發後行為可預期。

## 寫作風格：good
- 幾乎全 imperative，且解釋 why 而非堆 MUST。證據：「clever is what someone decodes at 3am」、「the unbuilt version was never written, so there is no real baseline」。
- ❌/✅ 對照範例品質極高（ponytail-review 的五個 tag 各附一行實例）。
- 有自我節制條款（Honesty boundary：「NEVER print a per-repo savings number」）——用大寫但附完整理由，非空洞命令。

## scope 清晰度：good
- 一 skill 一 job 的教科書級示範：debt=收集帳、gain=顯示計分板、review=只抓 over-engineering、help=速查卡。每個都有 Boundaries 節明確劃界（review：「Correctness bugs, security holes… explicitly out of scope」）。
- 主 skill ponytail 較廣（persistent coding mode），但這正是它的單一 job；「When NOT to be lazy」節防止過度套用。

## 其他觀察
- 全家族統一的 deactivation 協議（"stop ponytail" / "normal mode"）與 intensity levels，是可移植的機制設計。
- 無 injection 疑慮。
