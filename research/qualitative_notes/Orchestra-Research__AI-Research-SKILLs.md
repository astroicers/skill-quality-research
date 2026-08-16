# Orchestra-Research/AI-Research-SKILLs(T2/D/11740)

## 抽讀樣本
- 08-distributed-training/ray-train/SKILL.md
- 09-infrastructure/lambda-labs/SKILL.md
- 14-agents/autogpt/SKILL.md
- 19-emerging-techniques/speculative-decoding/SKILL.md
- 20-ml-paper-writing/ml-paper-writing/SKILL.md

## trigger 設計:good
五份皆有觸發語且語境具體。ml-paper-writing 最佳:「Use when drafting papers from research repos…preparing camera-ready submissions. For systems venues (OSDI, NSDI…), use systems-paper-writing instead」——Use when + 顯式跨 skill 負向路由。ray-train「Use when training massive models across multiple machines or running distributed hyperparameter sweeps」、speculative-decoding 甚至在 description 量化收益(「1.5-3.6× speedup」)。工程類 skill 觸發語一致到位。

## 寫作風格:good
imperative + 大量可複製程式碼,每份都有「When to use vs alternatives」段給出決策界線(ray-train 列 Accelerate/Lightning/DeepSpeed/DDP 的取捨)。ml-paper-writing 是本批 why 解釋最強者:整段「⚠ CRITICAL: Never Hallucinate Citations」講清 ~40% 錯誤率的機制、給出 placeholder 協定、對照 ✅/❌ 表,並引用具名研究者的寫作哲學(Nanda/Farquhar/Gopen&Swan)。少數瑕疵:autogpt 偏 tutorial 式知識傾倒,較像文件搬運而非行為指令。

## scope 清晰度:good
一 skill 一工具/技術,依研究生命週期分 23 類目錄,邊界由 CLAUDE.md 明訂(200-500 行、progressive disclosure、references 一層深)。ml-paper-writing↔systems-paper-writing 互相指名切分。輕微張力:autogpt/lambda-labs 偏「平台百科」,job-to-be-done 較鬆(涵蓋安裝/部署/監控/計費全景),但仍屬單一平台範疇。

## 其他觀察
- CLAUDE.md 本身是高品質的 skill-authoring 規範(明列 name gerund、description 第三人稱含 what+when、500 行上限、禁 nested references),與樣本一致度高——是「repo 有自我品質標準」的正面訊號,可作 rubric 佐證。
- ml-paper-writing 的 anti-hallucination 條款(never generate BibTeX from memory)與 K-Dense 的模式呼應,強化「高品質 skill 內建防幻覺機制」的跨 repo 觀察。
- 無 injection-suspect 內容。
