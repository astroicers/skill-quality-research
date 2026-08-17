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
    print("[selftest] mask_rubric_for_raters: 遮蔽/邊界/過泛保留/逐行驗證 全過 ✔")


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
        after, hits = mask_text(before, sample)
        problems = verify_only_expected_lines_changed(before, after)
        if problems:
            print("❌ 遮蔽改動了非預期的內容,中止:", *problems, sep="\n  ", file=sys.stderr)
            return 1
        dst = os.path.join(args.root, args.out, os.path.basename(rel))
        header = (f"# ⚠️ 這是**遮蔽版**副本,由 scripts/mask_rubric_for_raters.py 從 canonical 產生。\n"
                  f"# 具名證據({PLACEHOLDER})被移除,以免審查者被先前結論定錨。\n"
                  f"# canonical 在 {rel};**不要**編輯本檔。\n")
        with open(dst, "w", encoding="utf-8") as f:
            f.write(header + after)
        changed = sum(1 for x, y in zip(before.splitlines(), after.splitlines()) if x != y)
        print(f"{rel} → {dst}  遮蔽 {sum(hits.values())} 處 / {changed} 行")
        for k, v in sorted(hits.items(), key=lambda kv: -kv[1]):
            total[k] = total.get(k, 0) + v
    print(f"\n遮蔽 token 統計:{dict(sorted(total.items(), key=lambda kv: -kv[1]))}")
    未命中 = [s for s in sample if not any(t in total for t in tokens_for(s))]
    if 未命中:
        print(f"未在 rubric 中出現(無需遮蔽):{未命中}")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
