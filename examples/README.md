# examples — 三個 skill-reviewer 的實跑案例

每個案例都是**真實跑過的輸出**（不是示意），對應 `skill-reviewer/evals/evals.json` 的測試案例。
目的是讓你在裝之前就知道:輸出長什麼樣、怎麼讀、以及**什麼時候該不信它**。

前置:已 `./install.sh`（或用 repo 內路徑 `skill-reviewer/scripts/lint_skill.py`）。

---

## 案例 1:hygiene 擋下——「有 SKILL.md 之形,無規格之實」

```bash
python3 skill-reviewer/scripts/lint_skill.py research/repos/24kchengYe__human-skill-tree
```

```
[hygiene] FAIL  H-001=✗ H-005=✗ H-003=✗ H-004=✓
[packaging tier · 僅 packaging 面] 5/14 → 符合 T1(1k 星級)剖面
[gap list · packaging] ['has_tests_or_evals', 'has_marketplace_json', 'dir_examples']
```

**怎麼讀**:68 個檔名叫 `SKILL.md`,但**沒有一個有 frontmatter**——`H-001`(至少一個合規)
直接 fail。這是唯一會**擋 gate** 的情況。
⚠️ 「無假陽性疑慮」是本檔早期版本的說法,**已被實測否證**:純指標型 marketplace
(repo 本體是索引、天生沒有自己的 SKILL.md)會被 H-001 誤判——該形狀假陽性已記錄,
rubric 的 `H-001.scope_note` 載明適用邊界;拿它擋 gate 前先確認 repo 形狀。

注意 packaging 仍顯示「符合 T1 剖面」(5/14)——**packaging tier 與 hygiene 是兩條獨立軸**,
打包做了一些不代表內容合格。看 gate 該不該擋,只看 hygiene 那行。

---

## 案例 2:低星高質——packaging 低不代表品質差

```bash
python3 skill-reviewer/scripts/lint_skill.py research/repos/ayghri__i-have-adhd
```

```
[hygiene] pass  H-001=✓ H-005=✓ H-003=✓ H-004=✓
[packaging tier · 僅 packaging 面] 9/14 → 符合 T2(10k 星級)剖面
[gap list · packaging] ['install_oneliner_in_readme', 'dir_examples']
[security] S-002:registers_hooks(low-static-needs-llm)
```

**怎麼讀**:這個 skill 的 craft 是本研究的標竿之一(why→rules→override→自檢的完整結構),
但 packaging 只有 9/14。**這正是本專案的核心結論**——packaging 分數與工藝品質是兩件事,
不要拿 packaging tier 當總評。gap list 可以直接當 backlog 用。

---

## 案例 3:安全紅旗**不擋**,只提醒(刻意設計)

```bash
python3 skill-reviewer/scripts/lint_skill.py research/repos/NevaMind-AI__memU
```

```
[hygiene] pass  H-001=✓ H-005=✓ H-003=✓ H-004=✓
[packaging tier · 僅 packaging 面] 9/14 → 符合 T2(10k 星級)剖面
[security] S-001:obey_external_output(low-static-needs-llm)
```

**怎麼讀**:`S-001` 是真的——該 skill 指示 agent「安裝後照 binary 輸出逐字執行」
且「不要停下來確認」。但它**不擋 gate**,只發提醒。

**為什麼不擋**:同一條 regex 也會誤中 `anthropics/skills` 正當文件裡的
「follow the guide exactly」。gate 假阻的代價(阻斷正當開發、侵蝕信任)高於漏擋的代價
(仍有提醒)。`confidence: low-static-needs-llm` 就是在說「這條要人複核」。

> 複核的意思是**去查**,不是憑印象推翻。作者本人就曾看到 `.env` 就斷定某個
> `cred_in_argv` 是誤報,查證後發現那個 CLI 真的實作了 `--api_key` 且優先序高於 `.env`
> ——rubric 是對的。詳見 `research/self-audit-round2.md` §2。

---

## 進階:change-scoped(給 CI / gate 用)

```bash
python3 skill-reviewer/scripts/lint_skill.py <repo> \
  --changed-files "skills/foo/SKILL.md,README.md" --json
```

傳入本次變更的檔案後,`H-005` 切換為 change-scoped:
**只有本次改壞的** SKILL.md 會升為 `error`;repo 內既有的不合規檔仍是 `warning`
——不會因為別人留下的爛攤子擋住你的改動。

## 進階:排除 vendored 目錄

```bash
python3 skill-reviewer/scripts/lint_skill.py . --exclude "research/repos,vendor"
```

若 repo 內有第三方 clone,不排除的話它們的 SKILL.md 會被算成你的
（本專案自審時就踩過:`dir_examples` 一度被第三方 clone 的 `examples/` 誤記）。
測試 fixture 自 2.3.15 起**不用再手動排除**——`(evals|tests)/fixtures/` 下的
SKILL.md 自動豁免 hygiene 與 craft 抽樣(security 掃描刻意照掃,防路徑繞道),
`fixture_skill_md_count` 欄位讓豁免可見。

---

## 完整審查(含 craft)

lint 只是第一層。**判斷 skill 寫得好不好要靠 LLM**——在 Claude Code 對話中說:

> 用 skill-reviewer 審查 `<repo 路徑>`

它會照 `skill-reviewer/SKILL.md` 的五步流程:跑 lint → hygiene 門檻判生死 →
**判 skill 形狀**(不同形狀套不同準則)→ craft 四維度 → 安全複核,
輸出三段式 verdict。
