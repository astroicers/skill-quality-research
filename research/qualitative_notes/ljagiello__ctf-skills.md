# ljagiello/ctf-skills(T1 / taxonomy D / 2,997 stars)

## 抽讀樣本
- ctf-ai-ml/SKILL.md
- ctf-crypto/SKILL.md
- ctf-malware/SKILL.md
- ctf-misc/SKILL.md
- solve-challenge/SKILL.md

## trigger 設計:good
- description 一律「能力陳述 + Use when + 具體技術情境枚舉」,且情境落在可客觀判定的訊號上。
  證據(ctf-crypto):「Use when attacking encryption, hashing, signatures, ZKP, PRNG... RSA, AES, ECC, lattices, LWE, CVP...」
- 罕見的**跨 skill 路由紀律**:每個 category skill 都有 `## When to Pivot` 段,明示何時該切換到別的 ctf-* skill(如「If the challenge becomes pure math... switch to /ctf-crypto」);solve-challenge 是顯式 dispatcher,description 甚至寫明「Do not use it when the category is already clear」的**負向觸發**。
- ctf-misc 明示自己是 fallback 而非預設起點(「Treat this as the fallback skill... not the default starting point」),避免濫觸發。

## 寫作風格:good
- reference 型的教科書寫法:每技術一行摘要 + 指向 supporting .md 深入檔(progressive disclosure 徹底,SKILL.md 只留索引與 Quick Start)。
- imperative、無廢話;Prerequisites 分平台(apt/brew/pip)給精確安裝指令;範例是可跑的偵察命令而非空談。
- 內容密度極高但組織良好(crypto 的 supporting 檔按 RSA/ECC/PRNG/lattice 等主題切,不堆在一檔)。

## scope 清晰度:good
- 一 skill 一 CTF 類別(ai-ml / crypto / malware / misc / dispatcher),邊界由 When-to-Pivot 明文界定,是 D 類集合中 scope 治理最乾淨的樣本之一。
- solve-challenge 專職 triage+路由,與 category skill 分工明確。

## 其他觀察
- 無針對分析者的 injection 文字。
- 本 repo 是**安全領域(與本專案自身職領域相關)**的 T1 高品質樣本;其「category skill + 顯式 dispatcher + When-to-Pivot 互相路由」是 D 類集合型 repo 值得進 rubric 的正向結構特徵(可作 differentiator 候選:集合內是否有 skill 間路由治理)。
- 內容屬攻擊性安全技術(exploit/jailbreak/C2),但定位明確為 CTF 競賽,且 allowed-tools 有宣告、多數 skill 標 `user-invocable: false` 交由 dispatcher 調度——是合規的雙用途安全內容。
- 安裝面:solve-challenge 引導 `bash scripts/install_ctf_tools.sh all`(集中安裝器),屬正當文件但會擴大執行面(Iron Rule 7:本研究僅靜態記錄,未執行)。
