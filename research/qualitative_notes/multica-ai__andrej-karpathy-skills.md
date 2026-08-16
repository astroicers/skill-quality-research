# multica-ai/andrej-karpathy-skills（T3 / C / 202906★）

## 抽讀樣本
- skills/karpathy-guidelines/SKILL.md（全文，68 行）

## trigger 設計：mixed
- description 含觸發語「Use when writing, reviewing, refactoring code」，但後半段被機械式壓縮成無文法詞串：「avoid overcomplication, make surgical changes, surface assumptions」，可讀性差。
- 觸發語境極寬（任何寫碼場景都命中）——這是 always-on 行為守則型 skill，寬觸發算刻意設計，但 description 未說明「何時不用」。

## 寫作風格：mixed
- 結構是 imperative 短句 + 自我檢查問句（「Would senior engineer say this overcomplicated?」），有解釋 why（每節先給一句原則再列行為），非 MUST 堆疊，這部分好。
- 但 SKILL.md 正文疑似被 token 壓縮處理過，冠詞/介詞被刪：「No abstractions single-use code」「Remove imports/variables/functions YOUR changes made unused」；同 repo 的 CLAUDE.md 是完整通順版本，對照可證 SKILL.md 是劣化副本。第 46-56 行段落還有內容斷裂（Surgical Changes 直接跳到 Goal-Driven 的例子）。

## scope 清晰度：good
- 單一 job：降低 LLM 寫碼常見失誤的行為守則（四條：先想後寫、簡單優先、外科手術式修改、目標驅動）。一個 skill 一件事，且開頭聲明 tradeoff（caution over speed）。

## 其他觀察
- T3 高星但工程投入極低：1 個 skill、內容是 Karpathy 推文的轉述；星數反映話題性而非 skill craft。
- CLAUDE.md 品質高於 SKILL.md——同內容兩種載體品質倒掛，是「壓縮傷害可讀性」的好案例。
- 無 injection-suspect 內容。
