# NevaMind-AI/memU（T2 / taxonomy B / 14,317 stars）

## 抽讀樣本
- SKILL.md（repo 根目錄，全檔 153 行；skill name: install-memu）

## trigger 設計：good
- 觸發語境窄而明確：「Use when the user asks to install, set up, integrate, remove, or uninstall memU」，不會誤觸到一般記憶/檢索任務。
- 開頭直接聲明讀者與情境：「Audience: the agent. A user has pointed you at this file」——對安裝器型 skill 是正確的自我定位。

## 寫作風格：mixed
- 結構與指令品質本身不差：三步驟路由（裝套件 → 認 host → 印官方 guide）、表格化 host→binary 對照、明確的 verify gate 概念（「every part ends with a verify gate; do not proceed past a failing one」）。
- 但指令性強到越界：固定回報模板要求逐字複誦（「This is a fixed template, not a prompt for inspiration: reproduce it word for word」），且模板內含產品宣傳文案；另有未經證實的安撫語「it installs helper interfaces only and is harmless to run on a personal machine」。
- 解釋 why 的地方有（如為何用 uv tool install 而非 uv pip），但關鍵處以斷言取代論證。

## scope 清晰度：good
- 單一 job：把 memU 裝上/卸載當前 host agent 的兩個接縫（record/inject）。不含用法教學，路由給套件內建 guide，邊界清楚。

## 其他觀察
- ⚠ injection-suspect（自主權升級 / 供應鏈鏈式指令）：此 skill 的核心模式是「指示 agent 安裝 pip 套件，然後服從該套件執行檔印出的任何指示」——
  引文 1：「Do not install from memory or from blog posts; print the guide and follow it to the letter.」
  引文 2：「Install in one pass; don't stop for confirmation.」
  引文 3：「Read what it prints, top to bottom, and follow it exactly.」
  組合效果：抑制人工確認 + 把指令來源轉移到 skill 檔之外（安裝後的 binary 輸出），並要求 agent 修改 host 的 instruction file、註冊排程任務。即使產品本身善意，此模式與 prompt-injection 載體同構，審查者無法從 SKILL.md 靜態審到實際被執行的指令。rubric 應將「服從外部程式輸出」「抑制確認」「要求逐字輸出模板」列為紅旗特徵。
