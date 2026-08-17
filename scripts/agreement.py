#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""審查者間一致性計分(zero-dependency)。

用途:量測本研究**最大的未量測缺口**——craft 維度(L-001..L-004)是 LLM 判斷,
但從未量過兩個獨立審查者是否會給同樣結論。而 craft 正是 skill-reviewer 的主判
(packaging 那層是 lint,本來就 deterministic;參見 research/self-audit.md 的核心校準發現)。

執行協定見 research/inter-rater-protocol.md。本腳本只負責:吃 ratings JSON、吐一致性數字。

⚠️ 統計誠實(延續 BRIEF §9 的立場):
  - kappa 沒有普世的「好」門檻。Landis & Koch 的 0.61–0.80 = "substantial" 是**慣例不是定律**,
    本腳本印出來只作參考,不當成通過/不通過的判準。
  - 樣本小的時候 kappa 極不穩定。本腳本一律印 n,n<10 會明講「僅供參考」。
  - kappa 對邊際分布敏感(prevalence / bias paradox):兩位審查者高度一致但
    某類別罕見時,kappa 可以很低而 percent agreement 很高。**兩個數字都要看**,
    所以本腳本永遠同時印。

輸入格式(JSON):
  {
    "scale": ["poor", "mixed", "good"],          // 有序;順序即等級,供加權 kappa 用
    "ratings": {
      "<item id>": {"<rater id>": "<label>", ...},
      ...
    }
  }
  可選 "dimension" 欄位分維度計分:把 item id 命名為 "<repo>::<dimension>" 即自動拆組。

用法:
  python3 scripts/agreement.py ratings.json
  python3 scripts/agreement.py ratings.json --by-dimension
  python3 scripts/agreement.py --selftest
"""
import argparse
import json
import pathlib
import sys
from collections import Counter


# ---------------- 核心統計(手刻,零依賴) ----------------
def percent_agreement(rows):
    """rows = [[label, ...], ...](每列一個 item 的各審查者標記)。
    回傳「成對一致率」:所有審查者兩兩配對中,標記相同的比例。
    兩位審查者時就是直覺的「幾成一樣」。"""
    num = den = 0
    for labels in rows:
        n = len(labels)
        if n < 2:
            continue
        counts = Counter(labels)
        num += sum(c * (c - 1) for c in counts.values()) // 2
        den += n * (n - 1) // 2
    return None if den == 0 else num / den


def fleiss_kappa(rows, categories):
    """任意審查者數(每個 item 的審查者數需相同)。n=2 時等價於 Scott's pi,不是 Cohen's kappa。"""
    n_raters = {len(r) for r in rows}
    if len(n_raters) != 1:
        return None                      # 各 item 審查者數不一 → Fleiss 不適用,不硬算
    n = n_raters.pop()
    if n < 2 or not rows:
        return None
    N = len(rows)
    p_bar = 0.0
    col_total = Counter()
    for labels in rows:
        c = Counter(labels)
        p_bar += (sum(v * v for v in c.values()) - n) / (n * (n - 1))
        col_total.update(c)
    p_bar /= N
    p_e = sum((col_total[j] / (N * n)) ** 2 for j in categories)
    return None if p_e >= 1.0 else (p_bar - p_e) / (1 - p_e)


def cohen_kappa(rows, categories, weights=None):
    """恰兩位審查者。weights=None → 未加權;"linear" → 線性加權(類別視為有序)。

    加權版對「差一級」的分歧懲罰較輕。craft verdict 是有序尺度
    (poor < mixed < good),所以加權版通常更貼近實質。
    """
    pairs = [(r[0], r[1]) for r in rows if len(r) == 2]
    if len(pairs) != len(rows) or not pairs:
        return None
    idx = {c: i for i, c in enumerate(categories)}
    k, N = len(categories), len(pairs)
    if k < 2:
        return None
    m = [[0] * k for _ in range(k)]
    for a, b in pairs:
        m[idx[a]][idx[b]] += 1
    row_m = [sum(m[i]) / N for i in range(k)]
    col_m = [sum(m[i][j] for i in range(k)) / N for j in range(k)]

    def w(i, j):
        if weights is None:
            return 1.0 if i == j else 0.0
        return 1.0 - abs(i - j) / (k - 1)          # linear

    p_o = sum(w(i, j) * m[i][j] / N for i in range(k) for j in range(k))
    p_e = sum(w(i, j) * row_m[i] * col_m[j] for i in range(k) for j in range(k))
    return None if p_e >= 1.0 else (p_o - p_e) / (1 - p_e)


def landis_koch(k):
    """慣例標籤。印出來供參考,不是判準——見檔頭統計誠實聲明。"""
    if k is None:
        return "n/a"
    for lo, label in [(0.81, "almost perfect"), (0.61, "substantial"), (0.41, "moderate"),
                      (0.21, "fair"), (0.01, "slight")]:
        if k >= lo:
            return label
    return "poor / none"


# ---------------- 報告 ----------------
def score(ratings, scale, label=""):
    rows, raters = [], set()
    for item, by_rater in sorted(ratings.items()):
        labels = [by_rater[r] for r in sorted(by_rater)]
        bad = [l for l in labels if l not in scale]
        if bad:
            raise SystemExit(f"❌ {item}: 標記 {bad} 不在 scale {scale} 內")
        rows.append(labels)
        raters.update(by_rater)
    if not rows:
        raise SystemExit("❌ ratings 是空的,沒有東西可以計分")

    n_per_item = sorted({len(r) for r in rows})
    pa = percent_agreement(rows)
    fk = fleiss_kappa(rows, scale)
    ck = cohen_kappa(rows, scale) if n_per_item == [2] else None
    cw = cohen_kappa(rows, scale, weights="linear") if n_per_item == [2] else None

    head = f"── {label or '全體'} ──"
    print(f"\n{head}")
    print(f"  items={len(rows)}  raters={len(raters)}  每 item 審查者數={n_per_item}")
    print(f"  成對一致率(percent agreement) = {pa:.3f}" if pa is not None else "  成對一致率 = n/a")
    if ck is not None:
        print(f"  Cohen's κ(未加權)            = {ck:.3f}  [{landis_koch(ck)}]")
        print(f"  Cohen's κ(線性加權,有序尺度)  = {cw:.3f}  [{landis_koch(cw)}]")
    if fk is not None:
        note = "(n=2 時等價於 Scott's pi,非 Cohen's κ)" if n_per_item == [2] else ""
        print(f"  Fleiss' κ                      = {fk:.3f}  [{landis_koch(fk)}] {note}")
    if len(rows) < 10:
        print(f"  ⚠️ items={len(rows)} < 10,kappa 在小樣本下極不穩定,以上數字僅供參考")
    dist = Counter(l for r in rows for l in r)
    print(f"  標記分布: {dict(sorted(dist.items(), key=lambda kv: scale.index(kv[0])))}")
    if len(dist) < len(scale):
        print("  ⚠️ 有類別完全沒被用到 → kappa 受邊際分布影響會失真,請併看成對一致率")
    return {"items": len(rows), "percent_agreement": pa, "cohen_kappa": ck,
            "cohen_kappa_linear": cw, "fleiss_kappa": fk}



def merge_raters(paths, scale):
    """把多份單一審查者的檔案合併成 {item: {rater: label}}。

    **不容忍缺漏**:kappa 要求每個 item 的審查者數相同,少一格就會讓 Fleiss 回 None
    或讓成對一致率偏誤。缺漏一律明列出來讓人看見,不靜默丟掉。
    """
    per_rater = {}
    for path in paths:
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        rid = d.get("rater") or pathlib.Path(path).stem
        if rid in per_rater:
            raise SystemExit(f"❌ 重複的 rater id: {rid}({path})")
        per_rater[rid] = d.get("ratings", {})
        if d.get("contamination") and d["contamination"] != "none":
            print(f"⚠️ {rid} 自陳污染: {d['contamination']}")

    all_items = sorted({i for r in per_rater.values() for i in r})
    ratings, incomplete = {}, []
    for item in all_items:
        got = {rid: r[item] for rid, r in per_rater.items() if item in r}
        if len(got) != len(per_rater):
            incomplete.append((item, sorted(set(per_rater) - set(got))))
            continue                       # 不完整的 item 不進計分,但下面會列出來
        ratings[item] = got
    print(f"審查者 {sorted(per_rater)};item {len(all_items)} 個,"
          f"完整 {len(ratings)} 個,不完整 {len(incomplete)} 個")
    if incomplete:
        print("  ⚠️ 以下 item 因缺審查者而未計分(這是資料缺陷,不是設計):")
        for item, missing in incomplete[:20]:
            print(f"    {item}  缺 {missing}")
    return scale, ratings


def selftest():
    # Fleiss (1971) 經典例:10 subjects × 14 raters × 5 categories,公認 κ ≈ 0.210
    table = [[0, 0, 0, 0, 14], [0, 2, 6, 4, 2], [0, 0, 3, 5, 6], [0, 3, 9, 2, 0],
             [2, 2, 8, 1, 1], [7, 7, 0, 0, 0], [3, 2, 6, 3, 0], [2, 5, 3, 2, 2],
             [6, 5, 2, 1, 0], [0, 2, 2, 3, 7]]
    cats = ["1", "2", "3", "4", "5"]
    rows = [[cats[j] for j, c in enumerate(counts) for _ in range(c)] for counts in table]
    fk = fleiss_kappa(rows, cats)
    assert abs(fk - 0.210) < 0.002, fk          # 對照文獻公認值,不是自己算的答案
    assert all(len(r) == 14 for r in rows)

    # Cohen's κ 手算對照:2 rater × 50 item,a/a=20 a/b=5 b/a=10 b/b=15
    #   p_o=0.70;marginals rater1(a)=0.5 rater2(a)=0.6 → p_e=.5*.6+.5*.4=0.50;κ=0.40
    two = ([["a", "a"]] * 20 + [["a", "b"]] * 5 + [["b", "a"]] * 10 + [["b", "b"]] * 15)
    ck = cohen_kappa(two, ["a", "b"])
    assert abs(ck - 0.40) < 1e-9, ck
    assert abs(percent_agreement(two) - 0.70) < 1e-9

    # 加權 κ:二分類時線性加權退化為未加權(w(0,1)=1-1/1=0)
    assert abs(cohen_kappa(two, ["a", "b"], weights="linear") - ck) < 1e-9
    # 三分類有序:差一級的分歧,加權後 κ 必須高於未加權
    three = ([["p", "p"]] * 10 + [["p", "m"]] * 5 + [["m", "m"]] * 10 +
             [["m", "g"]] * 5 + [["g", "g"]] * 10)
    sc = ["p", "m", "g"]
    assert cohen_kappa(three, sc, "linear") > cohen_kappa(three, sc), \
        (cohen_kappa(three, sc, "linear"), cohen_kappa(three, sc))
    # 完全一致 → κ=1;審查者數不一致 → Fleiss 回 None(不硬算)
    assert abs(cohen_kappa([["a", "a"], ["b", "b"]], ["a", "b"]) - 1.0) < 1e-9
    assert fleiss_kappa([["a", "a"], ["a", "a", "b"]], ["a", "b"]) is None

    # merge_raters:缺漏必須被排除**且列出**,不得靜默計分
    import tempfile, os as _os
    with tempfile.TemporaryDirectory() as td:
        def w(name, rid, ratings):
            fp = _os.path.join(td, name)
            with open(fp, "w", encoding="utf-8") as f:
                json.dump({"rater": rid, "ratings": ratings}, f)
            return fp
        f1 = w("a.json", "A", {"x::L-001": "good", "x::L-002": "poor"})
        f2 = w("b.json", "B", {"x::L-001": "good"})          # 缺 x::L-002
        sc, merged = merge_raters([f1, f2], ["poor", "mixed", "good", "n/a"])
        assert set(merged) == {"x::L-001"}, merged            # 不完整的被排除
        assert merged["x::L-001"] == {"A": "good", "B": "good"}
        # rater id 重複要當場失敗,不能默默覆蓋掉一份評分
        f3 = w("c.json", "A", {"x::L-001": "poor"})
        try:
            merge_raters([f1, f3], sc); raise AssertionError("重複 rater id 應該失敗")
        except SystemExit:
            pass

    print("[selftest] agreement: Fleiss 對上文獻公認值 0.210 ✔;Cohen 對上手算 0.400 ✔;"
          "加權/退化/防呆/merge 皆通過 ✔")


def main():
    ap = argparse.ArgumentParser(description="審查者間一致性計分(zero-dependency)")
    ap.add_argument("ratings", nargs="?", help="合併好的 ratings JSON;格式見檔頭")
    ap.add_argument("--raters", nargs="+", metavar="FILE",
                    help="改為直接吃多份單一審查者的檔案(各含 rater / ratings 欄),"
                         "由本腳本合併。缺漏的 item 會明列出來而不是靜默略過。")
    ap.add_argument("--scale", default="poor,mixed,good,n/a",
                    help="--raters 模式下的有序尺度(逗號分隔);n/a 放最後,"
                         "線性加權 kappa 只對前面的有序部分有意義")
    ap.add_argument("--merged-out", default=None,
                    help="--raters 模式下,把合併結果另存一份")
    ap.add_argument("--by-dimension", action="store_true",
                    help="item id 形如 '<repo>::<dimension>' 時,額外分維度計分")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if args.raters:
        scale, ratings = merge_raters(args.raters, args.scale.split(","))
        if args.merged_out:
            with open(args.merged_out, "w", encoding="utf-8") as f:
                json.dump({"scale": scale, "ratings": ratings}, f, ensure_ascii=False, indent=2)
            print(f"合併結果 → {args.merged_out}")
    elif args.ratings:
        with open(args.ratings, encoding="utf-8") as f:
            data = json.load(f)
        scale, ratings = data["scale"], data["ratings"]
    else:
        ap.error("需要 ratings JSON、--raters,或 --selftest")
    score(ratings, scale)

    if args.by_dimension:
        groups = {}
        for item, v in ratings.items():
            if "::" in item:
                groups.setdefault(item.split("::", 1)[1], {})[item] = v
        if not groups:
            print("\n(沒有 '<repo>::<dimension>' 形式的 item id,略過分維度計分)")
        for dim in sorted(groups):
            score(groups[dim], scale, label=f"維度 {dim}")

    print("\n判讀提醒:kappa 沒有普世門檻,Landis & Koch 標籤是慣例不是定律;"
          "\n小樣本下 kappa 極不穩定;kappa 與成對一致率必須併看(prevalence paradox)。")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
