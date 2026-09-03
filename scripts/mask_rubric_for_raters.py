#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""產生「遮蔽具名證據」的 rubric 副本,供一致性量測的審查者使用。

**為什麼需要**:2026-08-17 首輪量測中,兩位審查者各自獨立揭露——
brief 要求必讀的 canonical rubric,其 `evidence_refs` **具名了本批樣本中的 6 個 repo**
而且帶著結論(如「browser-act(20+ 變體轟炸=反例)」)。分開計分後定錨效應被量化證實:
那些格的一致性是 **1.000(零分歧)**,其餘 55 格是 0.824。

**為什麼要用程式產生而不是手工改副本**:手工副本會與 canonical 漂移,
而 rubric 漂移正是 ADR-031 記錄的老問題。本腳本每次從 canonical 重新產生,
遮蔽後**逐行比對**確認只有預期的行被改動——不容許任何其他差異。

遮蔽對象 = 樣本清單裡每個 repo 的 `owner/name`、`owner`、`name` 三種寫法。
不只 `evidence_refs`:修訂條文的舉例、mechanism 的敘述都可能具名
(實例:2026-08-17 修 L-002/L-004 時,我自己在 `decision_order` 與 `exemption` 裡
引用了 `obra/superpowers` 與 `kepano/obsidian-skills` 當例子——修正動作本身
製造了新的定錨源)。

用法:
  python3 scripts/mask_rubric_for_raters.py \\
      --sample research/inter-rater-sample.json \\
      --out research/inter-rater/rubric-masked/
  python3 scripts/mask_rubric_for_raters.py --selftest
"""
import argparse
import json
import os
import re
import sys

SOURCES = [
    "skill-reviewer/references/rubric-manual-dimensions.yaml",
    "skill-reviewer/references/rubric.yaml",
]
PLACEHOLDER = "〔具名證據已遮蔽〕"
# 太泛的 token 不遮:遮了會把無關文字也蓋掉,反而改變條文語意
TOO_GENERIC = {"skills", "agent-skills", "google", "claude", "skill"}

# ---- 內容指紋(3.4.0)----
# 名字可遮、內容指紋遮不掉:條文引樣張時抄入的內容片段可反查出樣張
# (盲判實測:遮名後 4 個受審對象仍有可指認指紋,污染稽核者自己漏抓其中 2 處)。
# registry 住在 manual-dimensions 檔尾的 fp-registry 區塊;本工具:
#   剝除該區塊(判讀者不得見 name→quote 映射)、樣本命中時警告、quote 漂移轉紅。
FP_BEGIN = "# fp-registry-begin"
FP_END = "# fp-registry-end"
FP_LINE = re.compile(r'^\s*-\s*\{name:\s*"([^"]+)",\s*section:\s*"([^"]+)",\s*quote:\s*"([^"]+)"\}')


def parse_fingerprints(text):
    """回傳 registry 區塊內的 (name, section, quote) 清單;無區塊回空。

    區塊內只允許:entry 行、`fingerprints:` 鍵、註解、空行——其他一律 raise
    (終審 F5c:格式寫壞的 entry 若被靜默丟棄,該指紋就無警告、無漂移檢查地消失)。
    """
    entries, inside = [], False
    for i, line in enumerate(text.splitlines(), 1):
        if line.strip() == FP_BEGIN:
            inside = True
            continue
        if line.strip() == FP_END:
            inside = False
            continue
        if inside:
            m = FP_LINE.match(line)
            if m:
                entries.append(m.groups())
            elif line.strip() and not line.lstrip().startswith("#") \
                    and line.strip() != "fingerprints:":
                raise ValueError(f"fp-registry L{i} 不是合法 entry(靜默丟棄=指紋消失):{line.strip()[:60]!r}")
    return entries


def strip_fingerprint_block(text):
    """剝除 fp-registry 區塊(含前導註解段落至上一個空行)。回傳 (text, 剝除行數)。"""
    lines = text.splitlines(keepends=True)
    try:
        b = next(i for i, l in enumerate(lines) if l.strip() == FP_BEGIN)
        e = next(i for i, l in enumerate(lines) if l.strip() == FP_END)
    except StopIteration:
        return text, 0
    # 往前吃連續的 # 註解與區塊標題(它們描述 registry 本身,同樣不該給判讀者看)
    start = b
    while start > 0 and (lines[start - 1].lstrip().startswith("#") or not lines[start - 1].strip()):
        start -= 1
    return "".join(lines[:start] + lines[e + 1:]), (e + 1 - start)


EVREF_LINE = re.compile(r"^\s*evidence_refs\s*:")

def strip_evidence_refs(text):
    """剝除全部 evidence_refs 行(判讀包協定 v3,dirty 波前哨實錘後規則化)。

    refs 是作者材料,判讀者不需要;遮名+數字類屬化仍擋不住其結構描述
    (三要素類屬化在同批語料唯一映射即定錨),整類消滅是唯一可靠修法。
    行首樣式比對——版本沿革註解裡「提及」該詞不受影響。剝除後任何殘留
    的 evidence_refs 行都視為失敗(多行形式漂移時寧可紅燈,不得靜默漏剝)。
    """
    kept, removed = [], 0
    lines = text.splitlines(keepends=True)
    i = 0
    while i < len(lines):
        line = lines[i]
        if EVREF_LINE.match(line):
            removed += 1
            indent = len(line) - len(line.lstrip())
            i += 1
            # 多行 YAML 形式:吃掉後續更深縮排的列表項/續行(孤兒項不得殘留)
            while i < len(lines):
                nxt = lines[i]
                if nxt.strip() and (len(nxt) - len(nxt.lstrip())) > indent:
                    i += 1
                    continue
                break
            continue
        kept.append(line)
        i += 1
    out = "".join(kept)
    assert not any(EVREF_LINE.match(l) for l in out.splitlines()), "evidence_refs 殘留"
    return out, removed

def check_fp_quotes(text, entries):
    """漂移守衛:每條 quote 必須存在於 registry 區塊之外(條文改寫後指紋失效要轉紅)。"""
    body, _ = strip_fingerprint_block(text)
    return [f"{n}: quote 已不存在於條文({q[:40]}…)" for n, _s, q in entries if q not in body]


def fp_warnings(entries, sample):
    """遮蔽樣本命中 registry → 警告清單(該對象的對應維度屬污染下判讀)。

    比對集合含 full/owner/name 三種寫法(複審 MEDIUM-1:原版漏 owner,
    樣本若把 skill 名寫在 owner 位會漏警告)。
    註:quote 漂移檢查刻意**逐檔自治**——registry 只治理它所在檔的條文;
    若未來 registry 複製到多個 SOURCES,各檔各自守各自的 quotes,這是設計不是洞。
    """
    names = set()
    for full in sample:
        owner, _, name = full.partition("/")
        names.update(x for x in (full, owner, name) if x)
    return [f"⚠️ 指紋不可遮:{n} @ {s}『{q[:24]}…』—— 判讀該對象時此格屬污染下判讀,需人工處理(刪段/類屬化)"
            for n, s, q in entries if n in names]


def tokens_for(full_name):
    """一個 repo 的所有可能寫法。過泛的裸 token 排除,但 owner/name 全名一律保留。"""
    owner, _, name = full_name.partition("/")
    out = [full_name]
    for t in (owner, name):
        if t and t.lower() not in TOO_GENERIC and len(t) > 4:
            out.append(t)
    return sorted(set(out), key=len, reverse=True)      # 長的先replace,避免子字串先被吃掉


def mask_text(text, sample):
    """回傳 (遮蔽後文字, 命中統計)。只替換 token,不動其他任何字元。"""
    hits = {}
    for full in sample:
        for tok in tokens_for(full):
            # 邊界:前後不得是識別字元或 '-'。
            # ⚠️ 刻意**不**排除前面的 '/'——第一版排除了,結果 S-101 的
            # "K-Dense/khazix/text-to-cad" 裡的 text-to-cad 整個漏遮(實測抓到)。
            # rubric 裡出現的 owner/name 一律是「在指涉那個 repo」,即使夾在斜線串裡也是,
            # 所以應該遮。代價是路徑樣式的字串也會被遮——對只給審查者看的副本無妨。
            rx = re.compile(r"(?<![\w-])" + re.escape(tok) + r"(?![\w-])")
            text, n = rx.subn(PLACEHOLDER, text)
            if n:
                hits[tok] = hits.get(tok, 0) + n
    return text, hits


def verify_only_expected_lines_changed(before, after):
    """逐行比對:改動過的行**必須**含 PLACEHOLDER,行數必須相同。

    這道檢查是本腳本的重點——它保證遮蔽沒有順手改壞條文。
    """
    b, a = before.splitlines(), after.splitlines()
    if len(b) != len(a):
        return [f"行數改變:{len(b)} → {len(a)}"]
    bad = []
    for i, (x, y) in enumerate(zip(b, a), 1):
        if x != y and PLACEHOLDER not in y:
            bad.append(f"L{i} 被改動但不含遮蔽標記:{y[:80]!r}")
    return bad


def selftest():
    sample = ["obra/superpowers", "kepano/obsidian-skills", "google/skills"]
    src = (
        'evidence_refs: ["obra/superpowers(好例)", "kepano(表格)", "google/skills"]\n'
        "note: obsidian-skills 的 schema 表;superpowers 的 ledger\n"
        "keep: google 這個字太泛不該被遮;skills 也是\n"
        "path: a/obra/superpowers/b 夾在斜線串裡也要遮\n"
    )
    out, hits = mask_text(src, sample)
    assert PLACEHOLDER in out
    assert "obra/superpowers(" not in out and "kepano(" not in out
    assert "obsidian-skills 的" not in out and "superpowers 的" not in out
    # 過泛 token 保留:否則會把無關文字一起蓋掉
    assert "google 這個字太泛" in out, out
    assert "skills 也是" in out, out
    # 夾在斜線串裡的 repo 名**也要**遮(第一版漏遮 K-Dense/khazix/text-to-cad 的回歸案例)
    assert "a/obra/superpowers/b" not in out, out
    assert f"a/{PLACEHOLDER}/b" in out, out
    assert not verify_only_expected_lines_changed(src, out), \
        verify_only_expected_lines_changed(src, out)
    # 沒命中時原文一字不動
    same, h = mask_text("nothing here\n", sample)
    assert same == "nothing here\n" and not h
    # 行數改變要被抓到
    assert verify_only_expected_lines_changed("a\nb\n", "a\n")

    # ---- 內容指紋(3.4.0)----
    fp_src = (
        "some rule text with 獨特片段A here\n"
        "\n"
        "# 說明註解\n"
        "# fp-registry-begin\n"
        "fingerprints:\n"
        '  - {name: "alpha-skill", section: "L-002.x", quote: "獨特片段A"}\n'
        '  - {name: "beta-skill", section: "L-003.y", quote: "不存在的片段B"}\n'
        "# fp-registry-end\n"
    )
    ents = parse_fingerprints(fp_src)
    assert [(e[0], e[2]) for e in ents] == [("alpha-skill", "獨特片段A"), ("beta-skill", "不存在的片段B")], ents
    stripped, removed = strip_fingerprint_block(fp_src)
    assert removed and "fp-registry" not in stripped and "alpha-skill" not in stripped, stripped
    assert "獨特片段A here" in stripped                     # 條文本體不受剝除影響
    # 漂移守衛:quote 不在條文 → 轉紅;在 → 過
    drift = check_fp_quotes(fp_src, ents)
    assert len(drift) == 1 and "beta-skill" in drift[0], drift
    # 樣本命中 registry → 警告;未命中 → 無;名字寫在 owner 位也要中(複審 MEDIUM-1)
    assert fp_warnings(ents, ["local/alpha-skill"]) and not fp_warnings(ents, ["local/gamma"])
    assert fp_warnings(ents, ["alpha-skill/anything"]), "owner 位的 skill 名應命中"
    # 無區塊的檔:全部安靜通過
    assert parse_fingerprints("plain\n") == [] and strip_fingerprint_block("plain\n") == ("plain\n", 0)

    # 區塊內壞行必須 raise,不得靜默丟棄(終審 F5c)
    bad_src = fp_src.replace('  - {name: "beta-skill", section: "L-003.y", quote: "不存在的片段B"}',
                             '  - {name: "beta-skill" section: "L-003.y"}')
    try:
        parse_fingerprints(bad_src)
        raise AssertionError("壞 entry 行被靜默丟棄")
    except ValueError:
        pass

    # 真實 rubric 的指紋漂移守衛——以腳本位置定位,**檔案不存在即硬失敗**
    # (終審 F5b:原版 `if os.path.exists` 在 CWD 非 repo 根時整段守衛靜默消失)
    real = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", SOURCES[0])
    assert os.path.exists(real), f"selftest 找不到 {SOURCES[0]}——守衛不得靜默跳過"
    with open(real, encoding="utf-8") as f:
        rt = f.read()
    rents = parse_fingerprints(rt)
    assert rents, f"{real} 應含 fp-registry(3.4.0 起)"
    rdrift = check_fp_quotes(rt, rents)
    assert not rdrift, f"指紋漂移(條文改寫後 registry 未同步):{rdrift}"

    # evidence_refs 剝除(判讀包協定 v3)——合成 + 真實檔雙驗
    syn = "a: 1\n    evidence_refs: [\"x(好例)\"]\nb: 2\n# 註解提及 evidence_refs 不剝\n"
    out, nr = strip_evidence_refs(syn)
    assert nr == 1 and "x(好例)" not in out and "註解提及 evidence_refs 不剝" in out, "合成剝除失敗"
    rout, rn = strip_evidence_refs(rt)
    assert rn >= 5, f"真實檔 evidence_refs 剝除數異常({rn})——多行形式漂移?"
    assert not any(EVREF_LINE.match(l) for l in rout.splitlines()), "真實檔殘留"
    print("[selftest] mask_rubric_for_raters: 遮蔽/邊界/過泛保留/逐行驗證/指紋(解析·壞行·剝除·漂移·警告)/evidence_refs 剝除 全過 ✔")


def main():
    ap = argparse.ArgumentParser(description="產生遮蔽具名證據的 rubric 副本")
    ap.add_argument("--sample", default="research/inter-rater-sample.json")
    ap.add_argument("--out", default="research/inter-rater/rubric-masked")
    ap.add_argument("--root", default=".")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()

    with open(os.path.join(args.root, args.sample), encoding="utf-8") as f:
        sample = [r["full_name"] for r in json.load(f)]
    os.makedirs(os.path.join(args.root, args.out), exist_ok=True)

    total = {}
    for rel in SOURCES:
        with open(os.path.join(args.root, rel), encoding="utf-8") as f:
            before = f.read()
        # 指紋:漂移守衛先行(quote 不在條文 = registry 沒跟上改寫,硬失敗);
        # 樣本命中 registry = 名字遮得掉、內容遮不掉,印警告交人工處理
        fps = parse_fingerprints(before)
        drift = check_fp_quotes(before, fps)
        if drift:
            print("❌ 指紋 registry 與條文漂移,中止:", *drift, sep="\n  ", file=sys.stderr)
            return 1
        for w in fp_warnings(fps, sample):
            print(w)
        after, hits = mask_text(before, sample)
        # 行變更數必須在任何「剝行」之前算——剝行後 zip 錯位,計數會灌水說謊
        changed = sum(1 for x, y in zip(before.splitlines(), after.splitlines()) if x != y)
        problems = verify_only_expected_lines_changed(before, after)
        if problems:
            print("❌ 遮蔽改動了非預期的內容,中止:", *problems, sep="\n  ", file=sys.stderr)
            return 1
        # registry 區塊本身(name→quote 映射)不得進判讀包:逐行驗證後才剝除
        after, removed = strip_fingerprint_block(after)
        if fps and not removed:
            print("❌ 有 registry 卻剝除失敗,中止", file=sys.stderr)
            return 1
        after, n_refs = strip_evidence_refs(after)
        if n_refs:
            print(f"  剝除 evidence_refs {n_refs} 行(判讀包協定 v3)")
        dst = os.path.join(args.root, args.out, os.path.basename(rel))
        header = (f"# ⚠️ 這是**遮蔽版**副本,由 scripts/mask_rubric_for_raters.py 從 canonical 產生。\n"
                  f"# 具名證據({PLACEHOLDER})被移除,以免審查者被先前結論定錨。\n"
                  f"# canonical 在 {rel};**不要**編輯本檔。\n")
        with open(dst, "w", encoding="utf-8") as f:
            f.write(header + after)
        print(f"{rel} → {dst}  遮蔽 {sum(hits.values())} 處 / {changed} 行(遮蔽行數,不含剝行)")
        for k, v in sorted(hits.items(), key=lambda kv: -kv[1]):
            total[k] = total.get(k, 0) + v
    print("⚠️ 判讀包協定 v3:本產出目錄不得置於(或殘留於)判讀交付目錄——組包後即刪。")
    print(f"\n遮蔽 token 統計:{dict(sorted(total.items(), key=lambda kv: -kv[1]))}")
    未命中 = [s for s in sample if not any(t in total for t in tokens_for(s))]
    if 未命中:
        print(f"未在 rubric 中出現(無需遮蔽):{未命中}")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
