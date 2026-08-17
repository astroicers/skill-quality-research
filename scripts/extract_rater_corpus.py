#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把「審查者實際需要讀的檔案」抽成一份中性語料,與 untrusted clone 脫鉤。

**為什麼需要**(三個問題一次解決,全部來自 2026-08-17/18 兩輪量測的實測):

1. **prompt-injection 面**——三位審查者**各自獨立**揭露:讀 `research/inter-rater-repos/`
   底下的檔案,會讓 harness 把該 repo 自己的 `CLAUDE.md` / `.claude/rules/*.md`
   **當作專案指令**注入 context。一個惡意 repo 可以放一份 CLAUDE.md 直接指示審查者如何評分。
   三位都把它當資料、都沒遵循(Iron Rule 7),但**路徑存在,而且是協定自己走進去的**。
2. **不受控的審查者間變異**——不同審查者依讀取順序觸發到不同的注入,
   有審查者明說那「實質影響了我對某 repo 的 L-003 判讀」。
3. **磁碟**——15 個完整 clone 383 MB,但審查者實際讀的只有 61 份 SKILL.md、939 KB(0.24%)。

中性語料只含 `craft_llm_todo` 列出的 SKILL.md,**不含 CLAUDE.md / AGENTS.md /
.claude/rules/ / hooks / scripts**,所以沒有可被注入的東西。

**刻意不進版控**:那是第三方檔案。轉散布要做授權合規(15 個 repo 各有 LICENSE),
且把 untrusted 內容 commit 進來會隨本 repo 出貨。durable 的查證依據是
`research/clone-manifest-*.json`(已進版控,含 pinned commit)——
要精確查證某一格判定,從源頭用該 commit 取,授權乾淨。

用法:
  python3 scripts/extract_rater_corpus.py \\
      --lint-dir research/inter-rater --clones research/inter-rater-repos \\
      --out research/inter-rater/corpus
  python3 scripts/extract_rater_corpus.py --selftest
"""
import argparse
import json
import os
import shutil
import sys

# 這些欄位是 deterministic 層對 craft 維度的**預判**,不可交給審查者。
# 實測:`desc_has_trigger` 正是 L-001 要判的事,審查者在建閱讀清單時就看到了,
# 且有審查者表示它有幾次不同意那個 flag(regex 讀不出中文「當…時使用」)。
STRIP_FROM_TODO = {"desc_has_trigger"}


def sanitize_lint(doc):
    """回傳可交給審查者的 lint 副本:移除對 craft 的預判欄位。"""
    out = json.loads(json.dumps(doc))          # 深拷貝,不動原物件
    for item in out.get("craft_llm_todo", []):
        for k in STRIP_FROM_TODO:
            item.pop(k, None)
    return out


def plan(lint_dir, clones):
    """回傳 [(repo, rel_path, src_abs)];src 不存在者一併回報,不靜默略過。"""
    todo, missing = [], []
    for name in sorted(os.listdir(lint_dir)):
        if not name.endswith(".lint.json"):
            continue
        repo = name[: -len(".lint.json")]
        with open(os.path.join(lint_dir, name), encoding="utf-8") as f:
            doc = json.load(f)
        for item in doc.get("craft_llm_todo", []):
            rel = item["path"]
            src = os.path.join(clones, repo, rel)
            (todo if os.path.isfile(src) else missing).append((repo, rel, src))
    return todo, missing


def selftest():
    import tempfile
    doc = {"craft_llm_todo": [{"path": "a/SKILL.md", "desc_has_trigger": True, "desc_head": "x"}],
           "hygiene": [{"id": "H-001", "pass": True}]}
    out = sanitize_lint(doc)
    assert "desc_has_trigger" not in out["craft_llm_todo"][0], out
    assert out["craft_llm_todo"][0]["desc_head"] == "x"          # 其餘欄位保留
    assert out["hygiene"] == doc["hygiene"]
    assert "desc_has_trigger" in doc["craft_llm_todo"][0]        # 原物件不得被改

    with tempfile.TemporaryDirectory() as td:
        ld, cl = os.path.join(td, "lint"), os.path.join(td, "clones")
        os.makedirs(os.path.join(cl, "r1", "a")); os.makedirs(ld)
        open(os.path.join(cl, "r1", "a", "SKILL.md"), "w").write("x")
        json.dump({"craft_llm_todo": [{"path": "a/SKILL.md"}, {"path": "gone/SKILL.md"}]},
                  open(os.path.join(ld, "r1.lint.json"), "w"))
        todo, missing = plan(ld, cl)
        assert [t[1] for t in todo] == ["a/SKILL.md"], todo
        assert [m[1] for m in missing] == ["gone/SKILL.md"], missing   # 缺檔要被列出
    print("[selftest] extract_rater_corpus: 預判欄位剝除 / 原物件不變 / 缺檔回報 全過 ✔")


def main():
    ap = argparse.ArgumentParser(description="抽出中性審查語料(無注入面)")
    ap.add_argument("--lint-dir", default="research/inter-rater")
    ap.add_argument("--clones", default="research/inter-rater-repos")
    ap.add_argument("--out", default="research/inter-rater/corpus")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()

    if not os.path.isdir(args.clones):
        print(f"❌ 找不到 clone 目錄 {args.clones}——它可能已被清除。"
              f"\n   重建見 research/inter-rater-protocol.md(須用 manifest 的 commit,"
              f"shallow clone 只會拿到上游 HEAD)", file=sys.stderr)
        return 1

    todo, missing = plan(args.lint_dir, args.clones)
    if not todo:
        print("❌ 沒有任何檔案可抽,檢查沒有實際執行", file=sys.stderr)
        return 1

    total = 0
    for repo, rel, src in todo:
        dst = os.path.join(args.out, repo, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        total += os.path.getsize(dst)

    # 同步產出 rater-safe 的 lint 副本
    safe_dir = os.path.join(args.out, "_lint")
    os.makedirs(safe_dir, exist_ok=True)
    n_lint = 0
    for name in sorted(os.listdir(args.lint_dir)):
        if not name.endswith(".lint.json"):
            continue
        with open(os.path.join(args.lint_dir, name), encoding="utf-8") as f:
            doc = json.load(f)
        with open(os.path.join(safe_dir, name), "w", encoding="utf-8") as f:
            json.dump(sanitize_lint(doc), f, ensure_ascii=False, indent=2)
        n_lint += 1

    with open(os.path.join(args.out, "PROVENANCE.md"), "w", encoding="utf-8") as f:
        f.write(
            "# 中性審查語料(產生物,不進版控)\n\n"
            f"由 `scripts/extract_rater_corpus.py` 從 `{args.clones}` 抽出。\n\n"
            f"- SKILL.md {len(todo)} 份({total/1024:.0f} KB);rater-safe lint {n_lint} 份\n"
            "- **只含 `craft_llm_todo` 列出的 SKILL.md**——不含 CLAUDE.md / AGENTS.md /\n"
            "  `.claude/rules/` / hooks / scripts,因此沒有可被 harness 當專案指令注入的東西\n"
            "- `_lint/` 內的副本已移除 `desc_has_trigger`(那是 L-001 的預判)\n\n"
            "## 這不是查證的權威來源\n\n"
            "這些是**第三方檔案**,未進版控(轉散布需授權合規,且 untrusted 內容不應隨本 repo 出貨)。\n"
            "要精確查證某一格判定,請用 `research/clone-manifest-inter-rater-repos.json` 記錄的\n"
            "commit 從源頭取——**完整** clone 後 checkout 該 commit,shallow clone 只會拿到上游 HEAD。\n")

    print(f"✅ 中性語料 → {args.out}")
    print(f"   SKILL.md {len(todo)} 份 / {total/1024:.0f} KB;rater-safe lint {n_lint} 份")
    print(f"   已剝除:CLAUDE.md、AGENTS.md、.claude/rules/、hooks、scripts(注入面)")
    print(f"   已剝除:lint 的 {sorted(STRIP_FROM_TODO)}(craft 預判)")
    if missing:
        print(f"   ⚠️ {len(missing)} 份 craft_llm_todo 列出但 clone 內找不到:")
        for repo, rel, _ in missing[:10]:
            print(f"      {repo}/{rel}")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
