# earthtojake/text-to-cad（T2 / D / 13485★）

## 抽讀樣本
- skills/bambu-labs/SKILL.md（前 200 行）
- skills/cad-viewer/SKILL.md（全文）
- skills/sendcutsend/SKILL.md（全文）
- skills/step-parts/SKILL.md（全文）
- skills/urdf/SKILL.md（全文）

## trigger 設計：good
- description 具體到副檔名與場景：cad-viewer「Use when visually reviewing `.step`, `.stp`, …especially when handed off from CAD…skills」；urdf 還在 description 內劃出 sibling 邊界（SRDF/cad-viewer/CAD skill 各管什麼）。sendcutsend 有「Use only for SendCutSend.com preflight reports」的收斂限定。
- step-parts 的 description 過長（塞滿關鍵字近 100 詞），偏 SEO 式堆疊，是唯一扣分點。

## 寫作風格：mixed
- 多數 skill 是高品質 imperative + why：cad-viewer 解釋為何必須絕對路徑、為何 path 是 workspace 而非檔案夾（「hides the rest of the project, which is almost never what the user wants」）；urdf 講「validation is a guardrail, not spatial proof」；bambu-labs 的 dry-run 預設 + `--execute --confirm-start-print` 雙閘門是實體安全的正例。
- 但 bambu-labs 正文與 karpathy repo 同病：機械壓縮去掉文法詞（「Use skill local-network Bambu Lab print handoffs plain `.gcode` file already exists validated」），安全規則段落因此難讀——安全文本最不該壓縮。sendcutsend 單段規則長達 5-8 行的稠密串列，資訊對但認知負荷高。
- 「you must ALWAYS hand … to `$cad-viewer`」的跨 skill 強制 handoff 在多個 skill 重複出現，屬 MUST 式耦合。

## scope 清晰度：good
- 一個 skill 一個 job（列印交付 / 檢視器 / 製造預檢 / 零件庫查詢 / URDF 撰寫），邊界在 description 與正文都有明說；repo 規則還強制 skill 之間 runtime 零依賴。

## 其他觀察
- 每個 skill 開頭有 Provenance 段聲明「installed local skill files 是 runtime source of truth」——對抗供應鏈混淆的少見做法。
- 無 injection-suspect 內容。
