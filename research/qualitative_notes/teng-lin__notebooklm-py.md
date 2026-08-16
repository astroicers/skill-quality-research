# teng-lin/notebooklm-py(T2 / B / 18729★)

## 抽讀樣本
- SKILL.md(單一 skill,附掛在 Python 套件 repo 根目錄)

## trigger 設計:good
description 同時給顯式與意圖式觸發:「Activates on explicit /notebooklm or intent like "create a podcast about X"」,body 再以「When This Skill Activates」一節列 10 個具體 intent 例句(「Turn this into an audio overview」等)。觸發面寬但都對應真實能力,不算過度 pushy。

## 寫作風格:good
Imperative、agent-first,且大量解釋 why——這是它的招牌:「bare "status": "ok" (without --test) is a false-positive trap — a stale cookie file passes the parse check」;安裝腳本連「為何刻意跳過 [cookies] 而非吞錯」都講明(「that lets *real* install failures…surface for the agent」)。Autonomy Rules 把「可自動跑 / 需先問」的命令逐條分級,是少見的權限意識設計。缺點:單檔極長(Quick Reference 近 100 列),未做 progressive disclosure,對 context 成本不友善。

## scope 清晰度:good
一個 job:程式化操作 NotebookLM。雖涵蓋 auth/來源/生成/下載多子域,但都是同一工具面的操作手冊;並明確處理 parallel-agent、sandbox(Claude Cowork)等執行環境邊界。

## 其他觀察
- 無 injection 疑慮;對 bearer credential 有明確保護指引(「never print or log it, and unset NOTEBOOKLM_AUTH_JSON when finished」),安全敘述屬正向示範。
- 「Autonomy Rules(免確認/需確認命令白名單)」是值得納入 rubric 的高階特徵:skill 主動定義破壞性操作的 HITL 邊界。
