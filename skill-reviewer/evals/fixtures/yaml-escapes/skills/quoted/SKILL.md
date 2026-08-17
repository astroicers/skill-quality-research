---
name: quoted
description: "Use this skill when the user says \"deck,\" \"slides,\" or \"presentation\" — the escaped quotes are the point of this fixture. It also has a tab\there and a literal backslash\\in the middle."
license: Fixture. Not a real skill.
---
# Why this fixture exists

真實案例回歸夾具。2026-08-17 在 `anthropics/skills` 的 `pptx` / `xlsx` /
`slack-gif-creator` 三份 SKILL.md 上發現:**沒裝 PyYAML 時**,naive fallback parser 不會
還原雙引號內的 `\"` 轉義,於是同一份檔案在有/沒有 PyYAML 的機器上 `desc_len` 相差 6 字元。

原始語料(`research/repos/`)是 gitignored 的第三方 clone,CI 拿不到,所以那 161 份真實檔
無法當回歸夾具。這個檔案把該 bug 的形狀固化成**已提交、CI 拿得到**的樣本,
讓 `scripts/check_parser_agreement.py` 在只有 fixtures 的環境下也真的走到轉義路徑。

配套的兩道防線:
- `_unquote_scalar` 的單元斷言(`extract_features.py` 與 `lint_skill.py` 兩支 selftest 各一份)
- 本檔 —— 端到端:三條 parser 路徑讀同一份檔案必須得到同一個 description
