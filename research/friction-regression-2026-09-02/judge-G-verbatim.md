# 判讀者 G — 逐字紀錄(friction 回歸 2026-09-02,rubric 3.3.1 遮蔽版)

> 呼叫端逐字轉錄(friction 與 contamination 全文;取值節錄)。⚠️ 含具名 craft 判定,未來判讀者禁讀。

## 取值(節錄)

JimLiu m/g/g/m(L-004 序2);RinDig g/g/g/**n_a**(依 statement_test 表頭駁回裸引註;自標與字面讀法分叉);affaan p/g/g/p(序5);ayghri g/g/g/p(序5);browser-act m/g/g/g(序1 強形式);google g/m/g/m(序2);kepano g/g/g/p(序5);shanraisshan g/g/g/p(序5;曾考慮序3「references/ 相對路徑」後依機制目的駁回)。

## rubric_friction(逐字)

**F1|L-004 rule 行與 decision_order 極性相反(全批)。** rule 欄寫「anti-hallucination 機制(**高階加分項**)」,但序5 對「無機制+裸載重宣稱」判 poor。本輪 4/8 落 poor——「加分項」的缺席成了最常見的不及格來源,L-004 事實上是對工具文件類 skill 的硬要求。兩種讀法給出相反輪廓,同一文本不該同時容納兩者。

**F2|scope_of_perishable 無 de-minimis 下限,序5 只分「覆蓋」不分「暴露量」。** 單一提問幾乎抓到任何工具旗標與經驗句。41 行乾淨 CLI skill、960 行零溯源參考大全、5 句框架性事實的風格 skill 同落 poor——嚴重度差一個數量級的三案取值相同。

**F3|statement_test 表頭與 算-list 互斥(RinDig)。** 表頭要求攔截力;算-list 收「單純來源標註」為弱形式——裸引註不創造任何『須先查』情境。依表頭 → 序4 n/a;依字面+空缺為真 → 序1 good。n/a 與 good 之間沒有條文裁決。

**F4|equivalent_forms「repo 內相對路徑」未要求同步標的是權威事實源(shanraisshan)。** 手抄外部 CLI 文件放 references/ 再相對引用,依字面即序3 mixed。照這讀法**任何有 references/ 的 skill 都到不了序5**,而版控同步的是文對文、非文對事實。需要一句「同步形式須指向事實的權威來源或隨其自動更新」。

**F5|序3 無部分覆蓋規則(shanraisshan)。** 序2 有部分性語言;序3 沒有——同步形式只蓋部分載重面時無序可走。

**F6|shapes.md 互動協定型行與 L-002 exemption 前提衝突(ayghri)。** 表格命令「L-002 判 N/A」,但 exemption 成立前提是「沒有規則需要被解釋」。i-have-adhd 是互動協定形狀卻帶著本輪最完整的規則集。表格該加「若該形狀實際含規則集,L-002 照常適用」。

**F7|「一次性安裝/腳本型」邊界未定義,而它翻轉 L-004(google)。** 安裝「指南」與安裝「腳本」無判別式;歸該形狀則 L-004 從 mixed 翻 N/A,成片裸斷言直接豁免。特徵欄描述的是使用頻率、不是產物型態。需要判別式。

**F8|「基礎要件」的定義文本不明:rule、pass_criteria、disambiguation 三段把同一瑕疵放在三個位階(JimLiu/browser-act,L-001)。** 按 rule=基礎 → mixed;按 pass_criteria=基礎 → 同樣證據 good。value_mapping 的「傷及基礎要件」無從執行,因為「基礎要件」沒有唯一出處。

**F9|同一瑕疵跨維計費規則缺失(JimLiu,L-001/L-003)。**「just push 仍走全流程」同時可訴兩維;雙計派會把 L-003 也壓 mixed,輪廓改變。

**F10|L-001 的評估對象範圍未明文(affaan-m)。** desc 零觸發、body 有清單:description-only → poor;算 body → mixed。一句「L-001 只評 frontmatter description」即可消除分叉。

**F11|序1/序2 的「在機制覆蓋內」無判別式(JimLiu vs browser-act)。** 兩案機制同為 runtime probe,我一個判序1(失效會在行動點顯形+落 dated log)、一個判序2(寫錯時靜默寫入)。判據是我自造的測試——「該宣稱失效時,機制會不會在行動前讓模型發現或聲明?」——建議寫進條文。

**F12|value_mapping「基礎部分達成」無計量單位(google,L-002)。** 部分達成按條計?按節計?按篇幅多數決?

**F13|disambiguation 抽3測試對混合清單不穩定(browser-act)。** 21 個片語半正當半同義簇;抽中哪 3 個決定方向。宜改「以疑似同義簇為單位判」。

**F14|「它無法控制的東西」對同作者外部工具需類推(kepano)。** 類推站得住,但值得明文。

## contamination(逐字)

1. **判準文本直接預判了本批一個樣本(最重)**:scope_of_perishable 列舉「實例:某 skill 直述**五條 ADHD 神經科學事實**」——ayghri 正好是五條 ADHD 事實,遮蔽形同無效。我對 ayghri L-004 的 poor 無法宣稱獨立。
2. **具名弱例成為比對模板**:evidence_refs 的「Jeffallan(裸 MUST 堆疊=弱例)」在我判 google L-002 時起了作用——我在做「像不像那個具名樣態」的比對。
3. **數字定錨**:「20+ SEO 變體」與 1688 描述的約 21 個片語數量貼近,可能推了我對「轟炸」的初始感知(最終裁決依據是同義簇與能力錯配,定錨如實記)。
4. **權威暗示**:「2026-09-02 自 readme-reviewer 已驗證結構回灌」的「已驗證」標籤降低了我質疑五序結構本身的傾向。
5. **判準文本之外、執行環境之內(如實揭露)**:執行環境的專案層 CLAUDE.md 含 ayghri 的歷史裁決敘述——判準外定錨風險,可能推我對 ayghri 偏嚴。criteria 具名的 grill-me 等同時存在本機 skill 清單,不在本批,無直接影響。

**供應鏈註記**:多份含指令式文字(google 的 Mandatory Agent Directive、JimLiu 的 STILL follow),全按資料處理,無一被執行。
