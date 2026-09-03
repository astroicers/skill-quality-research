#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""判準數字清單守衛(熟成輪 2 A1)。

**為什麼需要**:數字錨滑進判準散文已三度復發(「20+」3.3.2、「~25」批次 3 前哨 A-1
的殘留、「172 檔」批次 4 終審 F1)——第三次甚至發生在「零數字」污染自查聲明之後,
且是把複審建議的乾淨泛稱**落地時**換成語料指紋數字。散文自查抓不住這隻手,
只有機械清單抓得住。

**機制**(仿 `lint_skill.DEFENSE_CALIB` 慣用法:語料釘在常數、selftest 斷言):
抽出判準檔中**判讀者會讀到的散文區**(`craft_value_mapping:` 至
`craft_verdict_rollup:`——與盲判包摘錄同一 span)的全部數字 token,
與下方 `REGISTERED` 清單做集合比對:
  - 出現未登記的新數字 → **紅**(退出碼 1),逼一次有意識登記
  - 已登記的數字消失 → 提示(不紅)——縮減是好事,但清單要同步瘦身
登記操作 = 編輯本檔 `REGISTERED` 並在 commit 訊息說明該數字是什麼、為何無污染。

用法:
  python3 scripts/check_criteria_numbers.py            # 檢查(CI 用)
  python3 scripts/check_criteria_numbers.py --selftest
"""
import re
import sys

SOURCE = "research/rubric-manual-dimensions.yaml"
SPAN = (r"craft_value_mapping: \|", r"\ncraft_verdict_rollup:")

# 已登記數字(2026-09-03 盤點基線)。每個 token 都該說得出來歷:
#   0-6      = 取值域/序號/百分比構件(序 1-5、L-00x 的個位、0-100 語境)
#   02/08/09/16/17/18/22/25/31/33/35、2026 = 日期(2026-08-17 等)與沿革引註
#   11       = 「11 行即完整」互動協定型例(3.3.2 類屬化時保留的結構描述)
#   25       = 「~25 片語」(既有例示;與日期 25 共用 token)
#   31/35    = ADR-031 引註、「35 pattern」evidence_ref
#   001-004  = L-001~L-004 id
REGISTERED = [
    "0", "1", "2", "3", "4", "5", "6",
    "02", "08", "09", "11", "16", "17", "18", "22", "25", "31", "33", "35",
    "001", "002", "003", "004", "031", "2026",
]


def extract_numbers(text):
    m = re.search(SPAN[0] + r"(.*?)" + SPAN[1], text, re.S)
    if not m:
        raise SystemExit(f"❌ 在 {SOURCE} 找不到判準散文區(span 錨變了?)")
    return set(re.findall(r"\d+", m.group(1)))


def check(text):
    found = extract_numbers(text)
    reg = set(REGISTERED)
    new = sorted(found - reg, key=lambda x: (len(x), x))
    gone = sorted(reg - found, key=lambda x: (len(x), x))
    return new, gone


def selftest():
    base = "craft_value_mapping: |\n  序 1 到 5,L-001,2026-08-17。\ncraft_verdict_rollup:\n"
    found = extract_numbers(base)
    assert found == {"1", "5", "001", "2026", "08", "17"}, found
    # 突變:塞一個未登記數字 → 必須被抓到(單側突變,只動散文區)
    mut = base.replace("到 5,", "到 5(全 repo 172 檔),")
    f2 = extract_numbers(mut)
    assert "172" in f2 and "172" not in REGISTERED
    # 真實檔:現行基線必須乾淨(新數字=0)
    import os
    real = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", SOURCE)
    assert os.path.exists(real), "selftest 找不到判準檔——守衛不得靜默跳過"
    new, _gone = check(open(real, encoding="utf-8").read())
    assert not new, f"真實判準含未登記數字:{new}"
    print("[selftest] check_criteria_numbers: 抽取/突變轉紅/真實基線 全過 ✔")


def main():
    if "--selftest" in sys.argv:
        return selftest()
    new, gone = check(open(SOURCE, encoding="utf-8").read())
    if gone:
        print(f"ℹ️ 已登記但不再出現(可自清單移除):{gone}")
    if new:
        print(f"❌ 判準散文區出現未登記數字:{new}", file=sys.stderr)
        print("   數字錨已三度滑進條文(20+、~25、172)。若此數字無污染,", file=sys.stderr)
        print("   在 scripts/check_criteria_numbers.py 的 REGISTERED 登記並於 commit 說明來歷。", file=sys.stderr)
        return 1
    print(f"✅ 判準數字清單:{len(extract_numbers(open(SOURCE, encoding='utf-8').read()))} 種 token 全數已登記")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
