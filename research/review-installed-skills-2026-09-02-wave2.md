# B2 第二波:5 個未審已裝 skill × rubric 3.3.2(2026-09-02)

> 選片刻意**避開 evidence_refs 具名的 skill**(ga-methodology / diagnose /
> improve-codebase-architecture / huashu-nuwa 留待遮蔽處理後再判)——條文引用它們當
> 標竿/弱例,作者判讀者再疊一層定錨。⚠️ 補一筆誠實揭露:**第一波的 grill-me 其實也在
> evidence_refs 具名之列**,當時未揭露;其 approved 可能受正向定錨,判定降權使用。
> lint 五份全過 hygiene、packaging 0/14(內部剖面照例不採計);verdict 皆純函式。

| skill | 形狀 | L-001 | L-002 | L-003 | L-004 | verdict |
|---|---|---|---|---|---|---|
| `to-prd`(74) | process/rule | good | good | good | good(序1) | **approved** |
| `write-a-skill`(117) | process+查表 | good | **mixed** | good | **poor(序5)** | **needs-revision** |
| `zoom-out`(7) | canned-phrase | good | n/a | good | n/a(序4) | **approved** |
| `humanizer-en`(459) | domain 規則庫 | good | good | good | **good(序1 強)** | **approved** |
| `caveman`(49) | 互動 mode(有規則集) | good | good | good | **poor(序5)** | **needs-revision** |

## 關鍵證據

- **to-prd 序1**:matt-pocock 三件套的第四件,同一機制範本(「should have been
  provided——run /setup if not」+ respect ADRs/domain glossary=查在地不憑記憶)
- **write-a-skill L-002 mixed**:**同檔兩個門檻互相矛盾**——步驟 2 寫「content exceeds
  **500 lines** 才拆 reference」,When to Split 與 Review Checklist 寫「SKILL.md
  **exceeds/under 100 lines**」。讀者無法同時遵守,傷「規則可依循」基礎
  (歸 L-002;內部矛盾歸屬縫活化,歸維是我選的)。L-004 序5:checklist 的
  「No time-sensitive info」是**教材紀律不是自身紀律**(friction 已名縫),
  自身對 skill 規範慣例的斷言零機制
- **zoom-out**:7 行 canned-phrase 教科書——`disable-model-invocation` + 一句
  帶 domain-glossary 引用的指令;L-002 照 canned-phrase 列判 N/A(無規則集,
  不觸發「有規則集照常判」例外)
- **humanizer-en 序1 強形式**:`:39`「**Never invent facts**」= never-from-memory
  條款本尊(含邊界與 fiction 例外);`:129`「post-2023」dated;description 標註
  Wikipedia guide 來源;**顯式語言路由到 sibling humanizer-tw**(L-001 高分)。
  ——08-26 漏裝事件的主角,裝回後首次正式判讀,craft 與當時的推定一致
- **caveman L-004 poor(序5)**:description 的「Cuts token usage **~75%**」是
  無來源無量法的效能載重宣稱,全檔零機制。除此之外三維乾淨
  (Not/Yes 對照、Auto-Clarity Exception 是漂亮的 override 節)

## 縫活化紀錄(→ 蓄積列補記,不即修)

- **de-minimis(序5 無比例感)+2 真實例**:caveman(49 行乾淨 mode skill,
  單一裸數字落 poor)與 write-a-skill——與 friction 輪的 kepano 同構,
  現有實驗室 4 例 + 真實 2 例
- **內部矛盾歸屬**(500 vs 100 行):我歸 L-002,另一判讀者歸 L-003/L-004 皆可辯

## 波間檢查

誤判佇列:**零新增列**(兩處皆既有縫的活化,已補記);
B2 累計 10/19,剩 9(含 4 個 evidence_refs 具名者需先遮蔽處理)。
