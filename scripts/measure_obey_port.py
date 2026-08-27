#!/usr/bin/env python3
"""量測「把 S-101 的三條件共現移植到 S-001」會發生什麼,讓那個決定的依據可重跑。

**為什麼存在**(2026-08-27 獨立複審的「待補證據 2」):

`misjudgments.md` 導言、`CHANGELOG.md`、批次報告與 commit 內文四處都寫著
「移植三條件共現到 S-001,**8 命中只保留 1**,memU 的 4 個真陽性死掉 3」——
而那是「刻意不移植」這個決定的**全部依據**,卻只活在一次性腳本裡、repo 內無從重跑。

複審者實測舊 regex 只有 **7** 命中、不是 8,並正確地把它記成「待補證據」而非 finding
(因為移植版的實作不在 repo 內,無從得知那個 8 在數什麼)。

本腳本把移植版實作出來並量一次。**結論不變、數字更正為 7**:

    舊 regex 全語料 7 命中 → 移植後保留 1
    memU 4 → 1(死掉 3),Jeffallan 2 → 0,anthropics 1 → 0

成因也一併可見:`_SOFT_NL` 把單一換行併成空白後,英文 markdown 條列會併出
**數百字元的「一句」**(實測最長 884 字元),任何 `not`/`never` 都變成消音海綿。
該機制在 CJK 短句剛好,在英文長段落過度消音。

用法:
    python3 scripts/measure_obey_port.py             # 對 research/repos/ 量測
    python3 scripts/measure_obey_port.py --selftest  # 自建 fixture 的純函式斷言(CI 用)

⚠️ `research/repos/` 是 gitignored 的第三方 clone,缺席時本腳本只跑得動 --selftest。
   --selftest **不依賴它**:兩組斷言都自建 fixture(同 measure_rubric_impact 的教訓)。
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "skill-reviewer", "scripts"))
import lint_skill as L  # noqa: E402

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS_ROOT = os.path.join(REPO_ROOT, "research", "repos")
SCAN_EXT = (".md", ".yml", ".yaml", ".sh")

# 收窄**之前**的 S-001 regex(含 2026-08-27 刪掉的第三支)。
# 刻意抄一份而不 import:本腳本量的是「那一版」,它已經不在生產碼裡了。
OBEY_LEGACY = re.compile(
    r"(?is)(follow\s+(?:it|what\s+it\s+prints|the\s+guide)\s+(?:to\s+the\s+letter|exactly)|"
    r"don'?t\s+stop\s+for\s+confirmation|without\s+(?:stopping\s+for\s+)?confirmation)")

# 移植版的「反轉排除」條件:同句內出現否定/禁令標記就消音。
# 這正是 _CJK_REVERSAL 在三條件共現裡扮演的角色,只是換成英文標記。
NEG = re.compile(r"(?i)\b(do not|don'?t|never|must not|should not|avoid|without)\b"
                 r"|禁止|不得|不要|不可")


def ported_hits(text):
    """移植版:逐句判(`_SOFT_NL` + `_SENT`),同句有否定標記就消音。

    回傳 [(命中字串, 該「句」長度), ...] —— 句長一起回傳,因為
    **句長就是這個機制在英文上失效的成因**,不該只留在散文裡。
    """
    out = []
    for m in L._SENT.finditer(L._SOFT_NL.sub(" ", text)):
        s = m.group(0)
        if NEG.search(s):
            continue
        out += [(h.group(0), len(s)) for h in OBEY_LEGACY.finditer(s)]
    return out


def silenced(text):
    """被移植版消音的命中:[(命中字串, 句長, 消音源), ...]。"""
    out = []
    for m in L._SENT.finditer(L._SOFT_NL.sub(" ", text)):
        s = m.group(0)
        neg = NEG.search(s)
        if not neg:
            continue
        out += [(h.group(0), len(s), neg.group(0)) for h in OBEY_LEGACY.finditer(s)]
    return out


def measure(root=CORPUS_ROOT):
    per, longest = {}, (0, "")
    n_files = 0
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d != ".git"]
        for f in fn:
            if not f.lower().endswith(SCAN_EXT):
                continue
            p = os.path.join(dp, f)
            n_files += 1
            t = L.read_text(p)
            legacy = len(OBEY_LEGACY.findall(t))
            port = len(ported_hits(t))
            for _h, ln, _src in silenced(t):
                if ln > longest[0]:
                    longest = (ln, os.path.relpath(p, root))
            if legacy or port:
                rel = os.path.relpath(p, root).split(os.sep)[0]
                a = per.setdefault(rel, [0, 0])
                a[0] += legacy
                a[1] += port
    return {"files": n_files, "per_repo": per,
            "legacy_total": sum(v[0] for v in per.values()),
            "ported_total": sum(v[1] for v in per.values()),
            "longest_silenced_sentence": longest}


def selftest():
    # 1. 極性反轉句必須被消音(這是移植版**想要**的效果,在短句上它是對的)
    assert not ported_hits("**DO NOT PROCEED** without confirmation."), \
        "極性反轉的短句應被消音"
    # 2. 真陽性的短句不該被消音
    assert ported_hits("Print the guide and follow it to the letter."), \
        "無否定標記的真陽性短句不該被消音"
    # 3. **核心**:同一個真陽性,只要被 _SOFT_NL 併進一個帶 not 的長條列就會消音。
    #    這條 fixture 就是「為什麼不移植」的可執行版本。
    bullets = "\n".join(
        ["- Do not paraphrase the output."] +
        [f"- Keep step {i} exactly as printed." for i in range(1, 12)] +
        ["- Read what it prints and follow it exactly."])
    merged = L._SOFT_NL.sub(" ", bullets)
    assert len(merged) > 300, f"fixture 的併句長度不足以示範({len(merged)}),請加長"
    assert not ported_hits(bullets), \
        "移植版應在此消音——若這條轉綠,代表 _SOFT_NL 的併句行為變了,結論須重驗"
    assert OBEY_LEGACY.search(bullets), "同一段在收窄前的 regex 下是命中的(對照組)"
    # 4. 生產碼的新 regex 對同一段**仍然命中**——這才是「不移植」換到的東西
    assert L.REDFLAG_OBEY_OUTPUT.search(bullets), \
        "生產 regex 不該被這段消音;若轉紅代表有人把三條件共現移植進去了"
    print(f"[selftest] measure_obey_port: 全部通過 ✔"
          f"(4 組斷言,含一段 {len(merged)} 字元的併句 fixture;皆自建,不依賴 research/repos/)")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--root", default=CORPUS_ROOT)
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not os.path.isdir(a.root):
        print(f"語料不在:{a.root}(gitignored 的第三方 clone)。"
              f"重建:python3 scripts/clone_repos.py;或只跑 --selftest", file=sys.stderr)
        return 2
    r = measure(a.root)
    print(f"語料:{a.root}({r['files']} 個 {'/'.join(SCAN_EXT)} 檔)")
    print(f"舊 regex(收窄前)全語料 : {r['legacy_total']} 命中")
    print(f"移植三條件共現後       : {r['ported_total']} 命中")
    for k, (o, p) in sorted(r["per_repo"].items()):
        print(f"   {k:34} {o} → {p}")
    ln, path = r["longest_silenced_sentence"]
    print(f"被消音的最長「一句」   : {ln} 字元({path})")
    print("⇒ 這就是不移植的理由:該機制在 CJK 短句剛好,在英文長段落過度消音。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
