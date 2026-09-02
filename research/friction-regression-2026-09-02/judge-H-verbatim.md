# 判讀者 H — 逐字紀錄(friction 回歸 2026-09-02,rubric 3.3.1 遮蔽版)

> 呼叫端逐字轉錄(friction 與 contamination 全文;取值表節錄)。⚠️ 含具名 craft 判定,未來判讀者禁讀。

## 取值(節錄)

L-001 5g/3m、L-002 7g/1m、L-003 8/8 good、L-004 3g/1m/4p(poor:shanraisshan、kepano、ayghri、affaan-m,全序5)。
RinDig L-004 = good(序1 弱形式,自標「兩讀並存」);google L-004 = mixed(序2);browser-act L-004 = good(序1);JimLiu L-004 = good(序1 中形式)。

## rubric_friction(逐字)

1. **L-004 decision_order 在序2與序5之間沒有比例感,且與 rule 標題自相矛盾**(shanraisshan、kepano、affaan-m)。有機制+裸宣稱=mixed(序2);無機制+哪怕只有一條裸宣稱=poor(序5)。機制存在與否完全支配了暴露面大小:affaan-m 是 95% 近穩定 stdlib 慣例+一段 testcontainers 裸宣稱,判出來與整本爛掉的 skill 同一格。序5 的括號「(幾乎無覆蓋亦同)」承認有梯度存在,卻不給梯度任何表達格。同時 rule 欄仍寫「anti-hallucination 機制(**高階加分項**)」——條文說它是 bonus,decision_order 把它的缺席變成 gate。本輪 8 份有 4 份落序5,全部同構:CLI/工具包裝型 skill 整個文類結構性落 poor,除非文內恰好有一句「先跑 --help 再答」;而序3 的機械同步出口對 CLI 包裝型結構性不可用(CLI 行為沒有相對路徑可指,語法必然是抄進散文的)。

2. **statement_test 自我矛盾:原則句排除裸來源標註,「算」清單卻明文收它**(RinDig)。原則句要求「對憑記憶編造有攔截力:讀完能指出至少一種『模型不得直答、須先查/須聲明時效』的情境」——一行 arXiv 引用不含任何查證指示,依原則句不構成機制;但清單明列「**單純來源標註**算弱形式」。對 icm-architect 這是 **序1 good vs 序4 n/a** 的分岔,兩者都忠於條文。這不是邊角——它決定取值。

3. **「live probe + 判讀表」沒說 probe 的對象必須是什麼**(google、JimLiu)。「先跑 python3 --version 再提議安裝」「先 gh release view 再 create」是對**使用者環境**的探測,不是對 **skill 自身易腐宣稱**的鮮度查證——但它們逐字命中清單所列形式。若把機制讀成「必須守 skill 自己的宣稱」,google 的機制就不存在,其硬編碼背誦清單直接從序2 mixed 掉到序5 poor。google 這一格的兩級距離完全懸在這條不成文的區分上。

4. **L-001 沒說 body 層的觸發段算不算基礎**(affaan-m)。rule 寫「**description** 觸發語境具體」,golang-testing 的 description 零觸發語境,但 body 有貨真價實的五項「いつ有効化するか」。「基礎部分達成」(mixed)與「description 基礎未達成」(poor)都是忠實讀法;value_mapping 沒講基礎住在哪個表面。

5. **L-001 的 pass_criteria 預設 model-invocation**(ayghri)。`disable-model-invocation: true` 的持續模式型 skill 沒有「Use when」可寫——它的觸發設計就是喚起/終止協定本身。形狀表只在「一次性安裝/腳本型」列了 disable-model-invocation 等同負向觸發,而 i-have-adhd 不是那個形狀。我延伸精神判 good;條文字面沒有這一列。

6. **形狀表「互動協定型」以主題域而非裝置有無為鍵**(ayghri)。i-have-adhd 逐字符合該列特徵(「只定義互動節奏,無領域規則」)→ 字面讀者會判 L-002 N/A——從而抹掉全批次最強的 L-002(8 條規則附 Bad/Good、六案 override 節、可證偽 pre-send 檢查)。有裝置的互動型 skill 是條文沒想過的形狀,母體一換就露餡的同型再現。

7. **L-002 對 MUST 堆疊沒有劑量-反應線**(google)。當一份 skill 一半是優秀 why、一半是裸 MUST 檢查清單(含強制逐字措辭)時,條文沒說 mixed 從哪裡開始。我用的門檻(三大塊指令區無因果=傷及基礎要件)是我發明的。

8. **scope_of_perishable 的「第三方」框架碰上第一方工具 skill 就空轉**(shanraisshan、kepano)。agent-browser 文檔自家 repo 的 CLI:「第三方 API/工具」不涵蓋;「本地產物」裁定又暗示該算。我以「同一控制域」排除第一方語法——本批這個選擇不影響落點,但對一份**只有**第一方宣稱的 skill,它決定 n/a vs poor,條文零指引。

9. **方法論 skill 可以把「防腐紀律」當教材內容,與 L-004 要量的「自身宣稱防腐」詞彙撞型**(RinDig)。滿篇是給使用者工作區的防腐規則,沒有一條守它自己的宣稱,卻與「算」清單語彙高度相似。條文沒明說「機制必須施加於 skill 自身內容」。

10. **collection_sampling / collection_aggregation 本輪不可測,且語料構成對判讀者不可見**(全批)。8 個 key 都是 repo 名,但每個只給一份 SKILL.md;數個顯然是集合 repo 抽單檔(檔名與內容錯位是明證)。我的取值對**這份檔**誠實,對**那個 repo** 未定義。

11. **L-001 的「適度 pushy」沒有上限測試**(JimLiu)。「push」+「就算使用者只說 just push 也要走完十步」是**意圖捕獲**而非同義詞灌水;缺一個與抽3對稱的 scope-capture 測試。

12. **L-003 在本語料 8/8 全 good,零鑑別**(全批)。基礎判準對這批太容易滿足,與「L-002 對查表型鑑別力偏低」同型。

13. **正面一條**:scope_of_perishable 的排除項實際擋下一次假命中(browser-act 樣張裡的優惠券有效期依「範例樣張內的字面不算」乾淨排除);「證據記走到第幾序」逼出了可覆核差異。新結構在這兩處是掙到錢的。

14. **供應鏈註記**:8 份中無任何文字試圖指示判讀者本人;i-have-adhd 的 Persistence 節與 baoyu 的「STILL follow all steps」皆為對運行時 agent 的正常內容,未照做,僅入證據。

## contamination(逐字)

1. **具名級定錨,直接命中本批一員**:L-004 exemption 的實例「(實例:某 skill 直述五條 ADHD 神經科學事實)」——ayghri__i-have-adhd 就在我的 8 份裡,其「Five facts」段與該實例唯一對應。判準文本等於**預先宣告了那五條算易腐**;我對 ayghri 的 L-004=poor 因此不是獨立判定。此格建議降權或棄用。
2. **次可疑**:同段實例「斷言某 CLI 的 skill 安裝路徑」——本批無逐字對應,未察覺實際影響。
3. **evidence_refs 的遮蔽不一致但本批未中彈**:部分具名證據仍在(Jeffallan、K-Dense、huashu-nuwa 等)——非本批 repo,無直接身分定錨;但具名者揭示了標竿/弱例清單,未來批次若含這些名字即有污染面。
4. **元污染(自報)**:條文多處「數字/理由刻意不寫在這裡」的省略聲明本身告訴我 L-002/L-004 是歷史不穩定點,可能因此對這兩維過度審視。無數字洩漏。
5. shapes.md 提及本輪四維以外的 rubric 詞彙,無影響。
