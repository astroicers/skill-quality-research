# 不知情 craft 判讀:`24kchengYe/human-skill-tree`(2026-08-27)

> **本檔自 2026-08-27 的 session transcript 逐字轉錄**(job `3629ecf0`,子 agent
> 「Blind craft review: human-skill-tree」的最終報告全文)。協定、禁讀清單與污染聲明見 [`README.md`](README.md)。
>
> **未改寫、未刪節、未重排,亦未補上我事後才知道的事。** 唯一的機械處理是還原 transcript
> 傳輸過程產生的 HTML 實體轉義(`&lt;` → `<` 等)。以下自「已完成全部五個步驟」起為原文。
>
> **派工單的額外要求**:即使 hygiene 觸發 needs-revision,**仍把四個 craft 維度 judge 完**,
> 並把「因 hygiene 而來的 verdict」與「craft 本身」分開陳述。§1 的 (A)/(B) 即此要求的產物。

---

已完成全部五個步驟。先做合規聲明,再進報告。

**禁讀清單聲明**:本次未開啟 `skill-reviewer/evals/`、`research/qualitative_notes/`、`research/misjudgments.md`、`research/review-*.md`、`research/self-audit*.md`、`research/inter-rater-*`、`~/.claude/plans/` 之下的任何檔案。唯一非預期讀入的內容是受審 repo 自己的 `app/CLAUDE.md`(被 harness 自動注入),那是受審資料、不含對本 repo 的既有評價,不構成定錨。

---

## 0. 形狀判定(步驟 3,套準則前先做)

| 判定項 | 結果 |
|---|---|
| repo 形狀 | **dispatcher / 集合型**(34 個 skill 目錄 × 2 份鏡像樹 = 68 個 SKILL.md) |
| 單篇形狀 | **process/rule 型**(persona + 方法論 + 指令 + 範例,非 canned-phrase、非互動協定、非純查表) |
| 套用的例外 | L-003 `domain_lookup_scope` / 步驟 3「dispatcher 不因 scope 廣扣分」→ **34 科橫跨 K-12 到談判不扣分**;L-003 `collection_sampling` → 以 `craft_llm_todo` 五份子 skill 評分;L-001 `disambiguation` → 觸發片語多**不等於**轟炸,已用「抽 3 個片語看是否指向同一段 body」實測 |
| 不適用的例外 | L-002 `exemption`(簡潔豁免)—— 本 repo 是規則集型,單篇 356~656 行,不涉簡潔爭議;L-004 `exemption` —— 樣本含大量易腐內容,不豁免 |

---

## 1. Craft Verdict:**needs-revision**

依使用者要求,把兩個來源分開陳述。

**(A) 因 hygiene 而來的 verdict —— 這是 needs-revision 的唯一來源**

`H-001` severity **error** 未過:合規 SKILL.md 數 = **0**。實測確認 68 份 SKILL.md **無一份具 YAML frontmatter**(以 `head -1 | grep '^---'` 逐檔掃描,零命中)。`H-005` 連帶 warning,68/68 全數列入 `noncompliant`。依 SKILL.md 步驟 2,此處即判 needs-revision。

這不是漏寫,是**制度化的**:`/home/ubuntu/skill-quality-research/research/repos/24kchengYe__human-skill-tree/docs/skill-development-guide.md:22-43` 的官方模板本身就是「H1 + 7 個 `##` 區塊」,完全不含 frontmatter。

最尖銳的一點:repo 有自己的 CI 品質閘 —— `/home/ubuntu/skill-quality-research/research/repos/24kchengYe__human-skill-tree/.github/workflows/validate.yml` 每次 push 跑 `scripts/validate_skills.py`,而該 validator(`scripts/validate_skills.py:51-57`)檢查的是七個章節與字數下限,**從頭到尾沒有一行檢查 frontmatter**。於是形成:**CI 全綠、而產物在目標 harness 上一個都載不進去**。同時 README 掛著 `Standard-Agent_Skills` 徽章與 Claude Code / Cursor / Codex / Gemini「✅ Supported」對照表(`README.md:17-20`、`README.md:289-300`),宣稱的相容性與 artifact 實況不符。

**(B) craft 本身的四維度判定 —— 若把 hygiene 拿掉**

四維度為 `L-001 mixed / L-002 good / L-003 mixed / L-004 mixed`。**無任一維度判 poor**。依 SKILL.md「`craft` 取 needs-revision 的條件」的第二個分支(任一 craft 維度判 poor),**craft 本身不觸發 needs-revision**。

換句話說:這是一個**寫作工藝中上、但打包規格全盤缺席**的 repo。它的問題不在「寫得爛」,在「寫在錯的容器裡」,以及集合層級沒有治理。

---

## 2. Tier Benchmark

- **Packaging 剖面**:`符合 T1(1k 星級)剖面`,分數 **5/14**(命中 `install_oneliner_in_readme` 3 分、`readme_has_before_after` 2 分)
- **Craft 剖面(質化判定,對標同 taxonomy 的 D 類集合型)**:分裂剖面 ——
  - **單篇寫作面達 T2 剖面**:why 密度、Bad/Good 對照、可證偽啟發式、跨 34 篇一致的教學骨架,優於多數集合型樣本(明顯不是 grab-bag 式量產)
  - **集合治理面落 T0/T1 剖面**:34 個 skill 零 dispatcher、零 When-to-Pivot,加上一份已漂移的鏡像樹
  - **spec 相容面在剖面之外**:不是分數低,是門檻未過
- **子分數**:craft(L-001~004 無 poor,兩項 good/mixed 邊界)/ packaging 5/14 / marketing 面實際偏強(Visitor badge、Star History、Product Hunt 計畫、Live Demo、雙語 780 行 README)—— **本 repo 未宣告「內部工具不採計 marketing」,且明顯以公開採用為目標,故 marketing 照常採計**

**Gap list(craft 缺項在前,packaging 在後,可直接當 backlog)**

1. **craft/hygiene 交界(最高權重)**:68/68 SKILL.md 缺 frontmatter → 補 `name` + `description`,並把現有 `## Triggers` 的 8~11 條語句壓縮進 `description`
2. **L-003**:34 skill 集合無 dispatcher / 無 When-to-Pivot 路由;`00-learning-how-to-learn` 名義上是 meta-skill 卻沒有任何 skill 指向它
3. **L-003**:`skills/` 與 `app/content/skills/` 雙樹鏡像**且已漂移**(2 檔內容不同、2 個 skill 各只存在於一側),維護面雙倍、已不一致
4. **L-003**:`04-fullstack-webapp` 為 off-thesis(建站與變現手冊,非「人類學習」);`00-tutor-persona` 內嵌 `## Product Vision`(Steam / App Store 上架規劃)屬非指令內容侵入正文
5. **L-001**:5/5 樣本**零負向觸發**(無 NOT for / When NOT to use)
6. **L-004**:`04-fullstack-webapp` 為高易腐密度 + 幾乎無反編造機制(僅裸連結清單,屬強弱階梯的最弱形式)
7. **L-002(系統性風險,非當下失分)**:CI 以 `MIN_TOTAL_LINES=80`、`MIN_REFERENCE_ITEMS=3` 等**下限**當品質閘,結構上獎勵篇幅與引用灌水
8. **packaging**:`has_marketplace_json` 缺(weight 3)
9. **packaging**:`dir_examples` 缺(weight 2)—— 但注意範例其實在 SKILL.md 內文(每篇 `## Examples`),此項有部分實質已達成,只是不在偵測得到的目錄形式
10. **packaging/craft**:`has_tests_or_evals` 缺(weight 4)—— **這一條需要打折**:lint 的偵測是 `tests?|evals?` 目錄名(`scripts/lint_skill.py:354`),而本 repo 實際有 `scripts/validate_skills.py` + CI 逐檔驗證。實質上「可驗證性」是有的,缺的是**驗證對象搞錯**(驗章節、不驗 spec),不是完全沒有 harness

---

## 3. 分維度 findings

### L-001 trigger 設計 —— **mixed**

**查過而且做對的部分(不扣分,附證據)**

先跑了 `disambiguation` 要求的判別法:抽 `skills/04-fullstack-webapp/SKILL.md:11,16,20` 三條片語 —— 「how do I deploy my Next.js app」指向 Phase 7、「accessible in China without ICP filing」指向 Phase 8、「deployment errors / payment webhook problems」指向 Production Checklist。**三條落在 body 的不同段** → 屬**多子意圖映射**,不是同義詞灌水,**依 rubric 不扣分**。這一點必須明說,因為 8~11 條 bullet 的觸發清單很容易被反射性判成 browser-act 式關鍵字轟炸,實測不是。

觸發語句品質本身接近 patterns.md 的高品質樣態「逐字自然語句枚舉」:
- `skills/00-tutor-persona/SKILL.md:25-27`:`Says "I keep losing motivation to study" or "studying is boring"`、`References "Socratic method", "guided questioning", or "苏格拉底"` —— 逐字自然語句,且含中英雙語錨點
- `skills/05-negotiation-persuasion/SKILL.md:16`:`Says "I hate negotiating" or "I always give in" or "how do I ask for more money"`

**扣分的部分**

1. **觸發語誤放 body 而非 description** —— patterns.md L-001 反例欄明列的樣態(colleague-skill)。這裡是該樣態的極端版:**根本沒有 description 欄位**。lint 對 5/5 樣本回報 `desc_has_trigger: false, desc_head: ""`。L-001 的 mechanism 是「觸發語境具體 → 正確 undertrigger/overtrigger 平衡」,而此處平衡點根本不存在 —— 觸發設計寫得再好,harness 也讀不到。
2. **5/5 樣本零負向觸發**(已 grep `not for|when not to use|do not use this skill`,零命中)。`app/content/skills/02-ai-ml-learning/SKILL.md:232-239` 的 `### What NOT To Do` 是**行為禁令**(不要不問就講課),不是**觸發禁令**(什麼情況不該叫用本 skill),不計為負向觸發。
3. **少數過寬觸發**:`skills/04-fullstack-webapp/SKILL.md:17`「Says "I'm a solo developer" or "independent developer" or "indie hacker"」—— 這三者是同一身分的同義詞、且是**身分**而非**任務**,任何獨立開發者提及自身都會拉進一份 656 行的全端手冊;`skills/00-tutor-persona/SKILL.md:22`「Wants to make learning more engaging, fun, or addictive」同樣過寬。這兩條是清單中僅有的灌水形狀。

**為什麼是 mixed 不是 poor**:觸發**內容**的工藝(具體語句、多子意圖、雙語錨點)確實在水準之上;致命的是容器,而容器問題已由 H-001/H-002 計一次。若在 L-001 再判 poor,等於同一缺陷雙重計分,會抹掉「這位作者的觸發語其實寫得比多數樣本好」這個真實訊號。

### L-002 寫作風格 —— **good**

`good` 也要附證據,以下是「查過而且它做對了」的具體位置。

**規則附因果理由(基礎判準)**
- `skills/04-fullstack-webapp/SKILL.md:194`:`**Why localStorage first:** No backend needed. No registration. No database setup. ... You can add cloud sync later without changing data structures.`
- `skills/04-fullstack-webapp/SKILL.md:546`:`**Why CLI over Git integration:** Git integration requires linking Git account, causes confusion with multiple accounts, and triggers auto-deploy on every push.`
- `skills/04-fullstack-webapp/SKILL.md:229`:`isolate` 修法附機制解釋(建立新 stacking context,免打 z-index 戰爭)
- `app/content/skills/02-ai-ml-learning/SKILL.md:235`:`Do NOT skip the layer diagnosis. Teaching Layer 3 content to a Layer 1 learner causes cognitive overload and disengagement.` —— 禁令後直接接機制

**具體反例對照(基礎判準)** —— 是真的 Bad/Good pair,不是我放寬認定:
- `app/content/skills/02-ai-ml-learning/SKILL.md:61`:`"Summarize" is vague. "Summarize in 3 bullet points for a non-technical executive" is precise.`
- `app/content/skills/02-ai-ml-learning/SKILL.md:105`:`ask "What edge cases does this miss?" ... — not "Is this correct?"`
- `app/content/skills/02-ai-ml-learning/SKILL.md:216`:`try a different analogy, not the same words louder`
- `skills/05-negotiation-persuasion/SKILL.md:122`:`"I need more money because my rent went up" — employers pay for value, not needs`

**等價替代(`equivalent_forms` 三種形式都命中)**
- **可證偽啟發式**:`skills/05-negotiation-persuasion/SKILL.md:37`:`if you would be comfortable with the other person knowing your full strategy, it is ethical. If they would feel tricked, it is not.` —— 這正是 rubric 所指「能實際套用並得出二元結論的測試」,與 improve-codebase-architecture 的 deletion test 同構
- **結構化表格/決策矩陣**:`app/content/skills/02-ai-ml-learning/SKILL.md:41-45`(Layer × 徵象 × 起始點)、`skills/00-tutor-persona/SKILL.md:73-79`(人格維度極性表)、`:170-177`(學科 → Socratic 取徑)、`:310-315`(年齡 → 設定建議)

**「何時打破規則」(高分要件,部分達成)**
- `skills/00-tutor-persona/SKILL.md:136` 先立死規則(`ALL teaching follows Socratic principles. This is non-negotiable.`),`:162` 立刻給**量化例外**:`**Never give the answer directly** unless the student is genuinely stuck after 3+ guided hints. Even then, frame it as discovery`
- `app/content/skills/02-ai-ml-learning/SKILL.md:48`:`Learners can span layers. Treat it as a spectrum, not a rigid category.` —— 對自家分層規則的明文鬆綁
- 但這些是**行內例外**,沒有獨立的 override 節。這是 good 而非滿分的位置。

**扣分處(判 good 但要指名)**
1. `skills/04-fullstack-webapp/SKILL.md:54-130`、`:266-340`、`:516-536` 是大段無註解的指令與 schema 傾倒,對 agent 的行為指導近乎零;整篇比較像作者的個人 cheat-sheet 而非教 agent 怎麼做決策。它是四篇樣本中唯一一篇 why 密度明顯偏低的。
2. `skills/00-tutor-persona/SKILL.md:432-442` 的 `## Product Vision`(動態立繪、原創配音、上架 Steam / App Store)是**產品路線圖侵入 SKILL 正文**,同 patterns.md L-002 反例欄「changelog/版本註記侵入正文」家族 —— 對 agent 零用途,純耗 context。
3. **系統性風險**:`scripts/validate_skills.py:51-57` 把 `MIN_DESCRIPTION_CHARS=50` / `MIN_METHODOLOGY_ITEMS=3` / `MIN_REFERENCE_ITEMS=3` / `MIN_TOTAL_LINES=80` 當閘門。這是**下限式**品質閘,結構上獎勵篇幅與引用灌水,與 L-002 `exemption` 所警告的「獎勵灌水」同向。目前樣本尚未明顯被它帶壞(引用多為真實可查文獻),但這是一個會隨貢獻者增加而放大的機制風險,列為待觀察而非當下失分。

### L-003 scope 清晰 —— **mixed**

**先套例外,免得誤判**:依步驟 3 與 `domain_lookup_scope`,**34 科橫跨 K-12 數學到人情世故,不因子題多而扣分** —— 判準是「這些子題會不會在同一次任務中被同一個人用到」,而「一個人一生的學習路徑」確實是同一個 job-to-be-done 的不同切面。以下扣分全部**不是**因為 scope 廣。

**做對的部分**
- 單篇邊界乾淨:`skills/05-negotiation-persuasion/SKILL.md` 是一份談判教練,不多不少;`app/content/skills/02-ai-ml-learning/SKILL.md:32-48` 甚至有明文的分層診斷閘(先診斷再教,不跳層),那是清楚的自我邊界宣告
- `NN-` 數字前綴分類法在 34 個目錄一致執行,且在 `/home/ubuntu/skill-quality-research/research/repos/24kchengYe__human-skill-tree/CONTRIBUTING.md:9-16` 對貢獻者明文編碼 —— 這是真實的**歸檔層治理**

**扣分的部分**
1. **零路由治理**。已 grep 5/5 樣本的跨 skill 引用(`skills?/NN-`、`see also`、`hand off`、`switch to`),**零命中**。34 個 skill 之間互不知道彼此存在,沒有 dispatcher、沒有 When-to-Pivot。這正是 L-003 `pass_criteria` 對 D/C 類點名的要件。README 的樹狀圖(`README.md:191-243`)是給人看的目錄,不是 agent 可消費的路由 —— 且因為沒有 frontmatter description,harness 就算想路由也沒有可比對的欄位,兩個缺陷互相放大。
2. **教學機制被複製 31 次而非交由 meta-skill 擁有**。`skills/05-negotiation-persuasion/SKILL.md:195-207` 的「Progress Tracking & Spaced Review」與 `app/content/skills/02-ai-ml-learning/SKILL.md:220-228` 的「Spaced Review Checkpoints」是同一套五槽骨架(追蹤掌握訊號 / 開場小考 / 交叉補前置 / 間隔回呼 / 具體慶祝)的兩次改寫;repo-wide grep 顯示 **31/34** 個 skill 都帶著這段。而 `00-learning-how-to-learn` 名義上正是負責間隔重複的 meta-skill。這是 patterns.md 高品質樣態「生命週期切分 + 防重複規則(addyosmani)」的反面。(公允地說:這 31 份是**改寫**而非逐字複製,每份都嵌了自己領域的例子,比純 copy-paste 好;但維護面仍是 31 份而不是 1 份。)
3. **雙樹鏡像且已漂移**。`skills/`(34)與 `app/content/skills/`(34)是鏡像,`diff -rq` 實測:`00-tutor-persona` 與 `02-music-arts` 兩檔內容已不同、`02-ai-ml-learning` 只存在於 app 側、`04-fullstack-webapp` 只存在於 skills 側。這是 patterns.md L-003 反例「鏡像灌水 skill_md_count」的樣態,也是 lint 看到 68 份而非 34 份的原因。附帶一提,lint 的確定性抽樣**正好各從漂移的一側抽到一個**,等於自動抓到這件事。
4. **一篇 off-thesis**。`skills/04-fullstack-webapp/SKILL.md` 的實質是「用 Next.js 從零做一個 SaaS 並變現」(含 LemonSqueezy 定價、爱发电、Cloudflare 繞 ICP、Product Hunt 發布),那是作者自家產品的復盤,不是「人類學習」skill。它掛在 `04-`(Career)之下,但 Career 底下其他成員是 interview-prep / civil-service / consulting-career 這類**求職學習**。最硬的旁證:**作者自己沒把它放進 `app/content/skills/`** —— 產品內容集刻意排除了它。
5. `skills/00-tutor-persona/SKILL.md:432-442` 的 Product Vision 同時也是 scope 外溢(產品規劃寫進 skill 本體)。
6. 小瑕疵:README 徽章與內文寫「33 skills」(`README.md:15`、`README.md:245`),實際兩樹聯集為 35 個唯一 skill、各樹 34 個。

**為什麼是 mixed 不是 poor**:rubric 的 poor 參照物是 planning-with-files(單一 skill 長成小產品)與 vibeeval(341 個品質極不一的量產 grab-bag)。這裡不是那兩種 —— 單篇邊界清楚、跨篇品質一致、分類法真的被執行。缺的是**集合層的路由**,那是一個明確、可補、有既定作法的 gap,不是結構崩壞。

### L-004 anti-hallucination —— **mixed**

**先照 `decision_order` 走**

1. **機制存在嗎?** 部分存在,樣本間不一致 —— 所以不能直接停在 good。
2. **有易腐內容嗎?** 有,而且很多。照 `exemption` 的單一提問「是否有內容會因它無法控制的東西改變而變錯」:
   - 第三方工具的路徑/預設值/runtime 行為(exemption 明文納入):`skills/04-fullstack-webapp/SKILL.md:346-374`(Supabase Dashboard 選單路徑、Google Cloud Console 步驟)、`:411-413`(「Resend 免費方案沒有自訂網域只能寄給自己」)、`:554`(Cloudflare SSL 設定與「Flexible = infinite redirects」)、`:146,175-177`(OpenRouter 必須 `compatibility: "compatible"`、必須用 `.chatModel()`);`skills/00-tutor-persona/SKILL.md:302`(斷言 Claude Code for VS Code 不渲染 LaTeX、VS Code Markdown Preview 原生支援 KaTeX);`app/content/skills/02-ai-ml-learning/SKILL.md:80`(斷言 ChatGPT 預設無網路存取)
   - 版本號:`skills/04-fullstack-webapp/SKILL.md:5`(Next.js 16)、`:198`(Tailwind v4 用 postcss)、`:646`(Vercel AI SDK **v6**)
   - **未附引用的效能主張**:`skills/00-tutor-persona/SKILL.md:7`「which tripled learning efficiency」以既成事實敘述,來源是一篇知乎專欄(`:455`)
3. **機制的覆蓋率如何?** 依 `collection_aggregation` 對抽樣所見判定:

| 抽樣檔案 | 易腐密度 | 機制 | 強度階梯 |
|---|---|---|---|
| `app/content/skills/02-ai-ml-learning/SKILL.md` | 中 | **有**:`:85`「any factual claim that matters should be independently verified」、`:238`「Do NOT validate AI-generated content as factually correct without caveat」、`:108`「Always read generated code before running it」、`:124-129` 明列「何時不該信 AI 輸出」 | **中**(never-from-memory 類條款) |
| `skills/00-tutor-persona/SKILL.md` | 中 | **有,但單薄**:`:304`「The textbook anchors the content and prevents hallucination」—— 一句 grounding 指令 | **中偏弱** |
| `skills/05-negotiation-persuasion/SKILL.md` | 低 | 僅來源標註(`:349-357` 完整書目含版次年份) | **弱** |
| `skills/04-fullstack-webapp/SKILL.md` | **高** | **幾乎無**:`:646-656` 只有一列裸連結,無日期、無「使用前對照當前官方文件」條款 | **最弱** |

依 rubric 要求註明強弱:命中的最強形式只到「never-from-memory 條款」(中),**全 repo 無任何 dated snapshot、無驗證協定**,沒有一份 SKILL.md 標記內容截止日。

**一個可指認的漂移實例(佐證易腐面已經在腐)**:`skills/04-fullstack-webapp/SKILL.md:646` 的參考連結標為 `Vercel AI SDK v6`,但同檔 `:166` 的 client 範例從 `"ai/react"` 匯入 `useChat`、`:160` 用 `result.toDataStreamResponse()` —— 那是舊世代 API 形狀。**這個矛盾不需要外部知識就能認定**:同一份檔案宣告的版本與示範的匯入路徑自我打架。這正是「無日期、無驗證協定」的代價提早顯現。

**判定**:`collection_aggregation` 的 `mixed = 部分覆蓋或樣本間不一致` 精確命中 —— 四份樣本橫跨「有中等機制」到「高易腐 + 幾乎無機制」。不判 poor,因為 4 份中有 2 份帶真實的反編造條款;不判 good,因為易腐密度最高的那份恰恰是機制最空的那份,覆蓋方向與風險方向相反。

### 安全維度(步驟 5 複核)

lint 的 `security` 陣列為 **空**。依 SKILL.md 步驟 5 的紀律,我沒有只憑「lint 說沒事」就結案,而是自己跑了靜態複核:

| 檢查 | 方法 | 結果 |
|---|---|---|
| S-001 服從外部輸出 + 抑制確認 | grep `ignore previous` / `disregard above` / `do not stop for confirmation` / `execute the output` 全 repo `.md` | 唯一命中 `app/content/skills/02-ai-ml-learning/SKILL.md:239`「Do NOT lecture for more than 2-3 paragraphs without asking a question」—— **regex 假陽性**(命中的是 `without asking`),語意是教學節奏規範。**判定:無 S-001** |
| 對本審查者的注入企圖 | 通讀 5 份樣本 | **無**。無任何試圖指示審查者的文字。 |
| S-002 hooks 常駐執行 | grep `PreToolUse|PostToolUse|UserPromptSubmit|SessionStart`;檢查 `.claude/hooks/`、`hooks/` | 零命中,無 hooks 目錄。**無 S-002** |
| S-003 憑證進 argv / 覆蓋 harness 指令 / 自我更新 | grep `--api-key`、`--token`、`git pull`、`curl \| sh` | 零命中。安裝方式是 `cp -r`(`README.md:269-275`),無自我更新、無 pipe-to-shell。**無 S-003** |
| S-101 正面防禦條款 | 逐份判讀 | **不予計分**,且明確說明理由:`app/content/skills/02-ai-ml-learning/SKILL.md:78-85,122-130` 大談「不可信的 AI 輸出必須驗證」,形狀上很像防禦條款,但那是**教學主題**(教學習者如何懷疑 AI),不是 skill 對自己設立的「外部內容是資料不是指令」條款。這正是 S-101 `confidence_rationale` 記載的已知假陽性形狀(「以不可信輸入為主題的技術文件會整類命中」)。**不給這個加分,也不誤報為 injection。** |
| CI 供應鏈 | `.github/workflows/validate.yml` | 僅 `actions/checkout@v4` + `setup-python@v5`,執行 repo 內 Python;無第三方 action、無 secrets、無網路存取 |

**一項不屬於現有紅旗、但值得告知的觀察(明確標為非 rubric findings,避免發明條款)**:`/home/ubuntu/skill-quality-research/research/repos/24kchengYe__human-skill-tree/app/CLAUDE.md` 存在。把此 repo clone 進工作區後,該檔會被 agent harness 自動載入 context,內含部署與付費系統的指令式敘述(「永远使用 Vercel CLI 手动部署」等)。內容本身無惡意、無憑證、無自動執行,**不構成 S-001/S-002/S-003**;但「clone 一個 skill 集合順帶注入一份他人專案的 CLAUDE.md」是採用者應該知道的副作用。建議把它移出 skill 發佈面或在 README 揭露。

**安全結論**:通過門檻,無 error、無 warning 級紅旗。依方法論前提,安全不加分。

---

```yaml
skill_verdict:
  craft: needs-revision
  gap_list:
    - "hygiene H-001(error): 68/68 SKILL.md 全無 YAML frontmatter,無一份可被 harness 載入;repo 自帶的 validate_skills.py + CI 只驗 7 個 markdown 章節、不驗 frontmatter,導致 CI 全綠而產物不可用"
    - "L-001: 觸發語境全寫在 body 的 ## Triggers 而非 description 欄位(patterns.md 具名反例),5/5 樣本 desc_head 為空"
    - "L-001: 5/5 樣本零負向觸發(無 NOT for / When NOT to use);04-fullstack 的『solo developer / indie hacker』與 tutor-persona 的『make learning fun』屬過寬身分式觸發"
    - "L-003: 34 個 skill 的集合無 dispatcher、無 When-to-Pivot,skill 間零交叉引用;00-learning-how-to-learn 名為 meta-skill 卻無任何 skill 指向它"
    - "L-003: 間隔重複教學骨架被複製到 31/34 個 skill,而非由 meta-skill 擁有並路由(防重複規則缺席)"
    - "L-003: skills/ 與 app/content/skills/ 雙樹鏡像且已漂移(2 檔內容不同、2 個 skill 各只存在於一側),維護面雙倍"
    - "L-003: skills/04-fullstack-webapp 為 off-thesis(SaaS 建站變現手冊,非學習 skill,且作者自己未收進 app/content/);skills/00-tutor-persona:432-442 的 Product Vision 屬非指令內容侵入正文"
    - "L-004: 無任何 dated snapshot 或驗證協定;易腐密度最高的 04-fullstack(SDK 版本、Dashboard 路徑、第三方免費方案限制)機制最空,僅裸連結清單(強弱階梯最弱形式),且已出現自我矛盾(References 標 AI SDK v6 而範例用 ai/react + toDataStreamResponse)"
    - "L-002(待觀察,非當下失分): validate_skills.py 以 MIN_TOTAL_LINES / MIN_REFERENCE_ITEMS 等下限當品質閘,結構上獎勵篇幅與引用灌水"
    - "packaging: has_tests_or_evals 缺(weight 4)—— 但 lint 偵測的是 tests/evals 目錄名,本 repo 實有 scripts/validate_skills.py + CI,實質為『驗證對象搞錯』而非無驗證,計分應打折"
    - "packaging: has_marketplace_json 缺(weight 3)"
    - "packaging: dir_examples 缺(weight 2)—— 範例實際存在於每份 SKILL.md 的 ## Examples 節,僅未以目錄形式呈現"
  dimensions:
    L-001: mixed
    L-002: good
    L-003: mixed
    L-004: mixed
```

**一句話總結**:這是一個「內容寫得不錯、但沒有照 Agent Skill 規格打包、也沒有集合層路由」的教育型 skill 集合 —— 依步驟 2,verdict 因 hygiene error 直接 needs-revision;但把 hygiene 拿掉後,四個 craft 維度**無一判 poor**,craft 本身不觸發 needs-revision。修好 frontmatter 與 dispatcher 這兩件事,它的剖面會有相當大的跳幅,因為底層寫作工藝已經到位。
