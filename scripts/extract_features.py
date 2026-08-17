#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 3a — deterministic 特徵萃取 (BRIEF §3 Phase 3a, §7 Feature Schema)
讀取: research/repos.json + research/clone-manifest.json + research/repos/<dir>/
輸出: research/feature_matrix.json / .csv + research/skill_details.json(供 Phase 3b LLM 抽樣)

原則:
  - 零第三方依賴(PyYAML 有則用,無則退回 naive parser)
  - 純靜態讀取,絕不執行 clone 內任何檔案 (Iron Rule 7)
  - 所有 regex 啟發式都是 G2 審查對象;--limit 5 先跑小批次鎖 schema (Iron Rule 5)

用法:
  python3 scripts/extract_features.py --limit 5     # G2 小批次
  python3 scripts/extract_features.py               # 全量
  python3 scripts/extract_features.py --selftest
"""
import argparse, csv, io, json, os, re, statistics, subprocess, sys
from datetime import datetime, timezone

try:
    import yaml  # type: ignore
    HAVE_YAML = True
except Exception:
    HAVE_YAML = False

SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "dist", "build", "__pycache__"}
MAX_READ = 2_000_000  # 單檔讀取上限 2MB(防超大檔)

# ---- 啟發式 regex(G2 審查對象,BRIEF §7)----
TRIGGER_RE = re.compile(
    r"(?i)\b(use\s+(?:this\s+)?(?:skill\s+)?when|use\s+when|use\s+it\s+when|"
    r"trigger(?:s|ed)?\s+(?:when|if|include|whenever)|whenever\s+the\s+user|"
    r"use\s+this\s+(?:skill|tool)\s+(?:for|to|whenever)|invoke\s+when|"
    # G2 Q3 擴充:實證假陰性三類(小批次證據見 G2-review-notes)
    r"(?:should|can|may)\s+be\s+used\s+when|used\s+when|activates?\s+(?:for|when)|"
    r"當使用者|當你|使用時機|何時使用|觸發)")
INSTALL_RE = re.compile(
    r"(npx\s+skills|gh\s+skill|/plugin\s+(?:install|marketplace)|"
    r"curl[^\n]{0,140}install\.sh|npm\s+i(?:nstall)?\s+(?:-g|--global)|pipx?\s+install|brew\s+install)")
BEFORE_AFTER_RE = re.compile(
    r"(?is)(before\W{0,3}after|with\s+(?:the\s+)?skill.{0,120}?without|"
    r"without.{0,120}?with\s+(?:the\s+)?skill|❌.{0,500}?✅|✅.{0,500}?❌|\bBefore\b.{0,800}?\bAfter\b)")
METRIC_RE = re.compile(r"\b\d{1,3}(?:\.\d+)?\s*%|\b\d+(?:\.\d+)?x\s+(?:faster|fewer|less|more|better)|"
                       r"\bcuts?\s+\d+|\bsaves?\s+\d+", re.I)
MEDIA_RE = re.compile(r"\.gif\b|\.mp4\b|\.webm\b|<video|\bdemo\.(gif|mp4)|asciinema", re.I)
HARNESS_TERMS = ["claude code", "claude-code", "codex", "cursor", "gemini cli", "gemini-cli",
                 "openclaw", "copilot", "windsurf", "opencode", "kiro", "antigravity", "hermes"]
CODE_EXT = {".py", ".sh", ".js", ".ts", ".mjs", ".rb", ".go", ".rs"}


# ---------------- 基礎工具 ----------------
def read_text(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read(MAX_READ)
    except OSError:
        return ""

def walk_files(root):
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in SKIP_DIRS]
        for fn in fns:
            yield os.path.join(dp, fn)

def _unquote_scalar(s):
    """把 YAML 單行純量的引號與轉義還原。naive fallback 專用。

    為什麼需要:原本只做 .strip("'\"") —— 剝掉外層引號卻留著內層轉義,
    於是 `description: "... \\"deck,\\" ..."` 在無 PyYAML 時會多出反斜線,
    desc_len 因此與 PyYAML 路徑差幾個字元(2026-08-17 在 anthropics/skills 的
    pptx/xlsx/slack-gif-creator 三份實測到,161 份中分歧 3 份)。
    ⚠️ 這個函式在 scripts/extract_features.py 與 skill-reviewer/scripts/lint_skill.py
    各有一份(skill-reviewer 必須可獨立出貨,不得 import 研究腳本)。
    兩份不得漂移 —— 由 scripts/check_parser_agreement.py 三方比對把關。
    """
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] == '"':
        body, out, i = s[1:-1], [], 0
        ESC = {'n': '\n', 't': '\t', 'r': '\r', '"': '"', '\\': '\\', '/': '/', '0': '\0'}
        while i < len(body):
            if body[i] == '\\' and i + 1 < len(body):
                out.append(ESC.get(body[i + 1], body[i + 1])); i += 2
            else:
                out.append(body[i]); i += 1
        return ''.join(out)
    if len(s) >= 2 and s[0] == s[-1] == "'":
        return s[1:-1].replace("''", "'")     # YAML 單引號只有 '' 一種轉義
    return s


def parse_frontmatter(text):
    """回傳 (dict, body)。YAML 優先,失敗退回 naive `key: value`。"""
    m = re.match(r"^\ufeff?---[ \t]*\n(.*?)\n---[ \t]*(?:\n|$)", text, re.S)
    if not m:
        return {}, text
    raw, body = m.group(1), text[m.end():]
    if HAVE_YAML:
        try:
            d = yaml.safe_load(raw)
            if isinstance(d, dict):
                return {str(k).strip().lower(): v for k, v in d.items()}, body
        except Exception:
            pass
    # naive fallback(無 PyYAML):支援 YAML block scalar(`key: |`/`>`),與 lint_skill.parse_fm 對齊
    # (code-review F4:原 fallback 把 `description: |` 抓成字面 '|' 並漏掉續行)
    d = {}
    lines = raw.splitlines()
    i = 0
    while i < len(lines):
        mb = re.match(r"^([A-Za-z0-9_\-]+)\s*:\s*[|>][+-]?\d*\s*$", lines[i])
        # 隱式多行純量(`key:` 後直接換行接縮排文字);排除巢狀 mapping。與 lint_skill.parse_fm 對齊
        if not mb and re.match(r"^([A-Za-z0-9_\-]+)\s*:\s*$", lines[i]):
            nxt = next((l for l in lines[i+1:] if l.strip()), "")
            if re.match(r"^\s+", nxt) and not re.match(r"^\s+[A-Za-z0-9_\-]+\s*:", nxt):
                mb = re.match(r"^([A-Za-z0-9_\-]+)\s*:\s*$", lines[i])
        if mb:
            key = mb.group(1).lower(); i += 1; block = []
            while i < len(lines) and (lines[i].strip() == "" or re.match(r"^\s+", lines[i])):
                block.append(lines[i].strip()); i += 1
            d[key] = " ".join(x for x in block if x).strip()
            continue
        mm = re.match(r"^([A-Za-z0-9_\-]+)\s*:\s*(.*)$", lines[i])
        if mm:
            d[mm.group(1).lower()] = _unquote_scalar(mm.group(2))
        i += 1
    return d, body

def trigger_context_count(desc):
    """觸發情境數 proxy:含觸發關鍵詞句子中,逗號/分號/or 分隔的子句數(文件化的近似值)。"""
    if not desc: return 0
    total = 0
    for sent in re.split(r"(?<=[.!?。])\s+", desc):
        if TRIGGER_RE.search(sent):
            total += 1 + len(re.findall(r",|;|、|\bor\b", sent))
    return total


# ---------------- 單一 skill 解析 ----------------
def analyze_skill_md(path, repo_root):
    text = read_text(path)
    fm, body = parse_frontmatter(text)
    desc = fm.get("description")
    desc = desc if isinstance(desc, str) else (json.dumps(desc, ensure_ascii=False) if desc else "")
    parent = os.path.dirname(path)
    def has_dir(name):
        return os.path.isdir(os.path.join(parent, name))
    name_val = fm.get("name")
    return {
        "path": os.path.relpath(path, repo_root).replace(os.sep, "/"),  # 同上:一律 "/" 比對
        "lines": text.count("\n") + 1,
        "fm_fields": sorted(fm.keys()),
        "has_name": "name" in fm,
        "has_description": bool(desc),
        # G2 Q1:合規 = name 與 description 皆非空(BRIEF §6 邊界規則的操作型定義)
        "compliant": bool(str(name_val).strip() if name_val is not None else "") and bool(desc.strip()),
        "desc_len": len(desc),
        "desc_has_trigger": bool(TRIGGER_RE.search(desc)),
        "desc_trigger_contexts": trigger_context_count(desc),
        "name": fm.get("name"),
        "description_head": desc[:200],
        "dir_scripts": has_dir("scripts"), "dir_references": has_dir("references"),
        "dir_assets": has_dir("assets"), "dir_examples": has_dir("examples"),
        "dir_evals": has_dir("evals") or has_dir("eval"),
    }


def phase3b_sample(skills, k=5):
    """G2 Q4:每 repo 確定性抽 ≤k 個 skill 供 Phase 3b LLM 抽讀。
    規則:先按 skill 目錄名去重(同名取最短路徑,避免翻譯鏡像重複入選),
    再取 max-lines 1 個 + median-lines 1 個 + 其餘依 sha1(path) 排序遞補。"""
    import hashlib
    if not skills: return []
    uniq = {}
    for s in sorted(skills, key=lambda s: (len(s["path"]), s["path"])):
        uniq.setdefault(os.path.basename(os.path.dirname(s["path"])) or s["path"], s)
    skills = list(uniq.values())
    by_lines = sorted(skills, key=lambda s: (s["lines"], s["path"]))
    picks = [by_lines[-1]["path"], by_lines[len(by_lines) // 2]["path"]]
    by_hash = sorted(skills, key=lambda s: hashlib.sha1(s["path"].encode()).hexdigest())
    for s in by_hash:
        if len(set(picks)) >= min(k, len(skills)): break
        if s["path"] not in picks: picks.append(s["path"])
    return sorted(set(picks))


# ---------------- repo 級解析 ----------------
def find_readme(root):
    for cand in ("README.md", "readme.md", "README.MD", "README.rst", "README"):
        p = os.path.join(root, cand)
        if os.path.isfile(p):
            return read_text(p)
    return ""

def git_has_tags(root, offline):
    if offline: return None
    try:
        r = subprocess.run(["git", "-C", root, "ls-remote", "--tags", "origin"],
                           capture_output=True, text=True, timeout=25)
        if r.returncode != 0: return None
        return bool(r.stdout.strip())
    except Exception:
        return None

def analyze_repo(root, offline=False):
    files = list(walk_files(root))
    rel = [os.path.relpath(p, root).replace(os.sep, "/") for p in files]  # Windows 可攜性:relpath 用 os.sep,但下游全部以 "/" 比對
    # ((^|/)scripts(/|$) 之類的 regex、changed_files 交集、.github/workflows/ 前綴),
    # 反斜線會讓那些比對全部靜默失效(dir_* 誤判 false、H-005 交集永遠空)。
    # POSIX 上 os.sep 就是 "/",此行為 no-op。
    lower = [p.lower() for p in rel]

    skill_paths = [files[i] for i, p in enumerate(lower) if os.path.basename(p) == "skill.md"]
    claude_paths = [files[i] for i, p in enumerate(lower) if os.path.basename(p) == "claude.md"]
    skills = [analyze_skill_md(p, root) for p in skill_paths]

    readme = find_readme(root)
    readme_lines = readme.count("\n") + 1 if readme else 0

    workflows = [files[i] for i, p in enumerate(lower)
                 if p.startswith(".github/workflows/") and p.endswith((".yml", ".yaml"))]
    wf_text = "\n".join(read_text(w) for w in workflows[:20])
    ci_validates = bool(re.search(r"(?i)skill|frontmatter", wf_text)
                        and re.search(r"(?i)lint|valid|check|test", wf_text))

    ext_counter = {}
    for p in lower:
        _, ext = os.path.splitext(p)
        if ext: ext_counter[ext] = ext_counter.get(ext, 0) + 1
    top_ext = sorted(ext_counter.items(), key=lambda kv: -kv[1])[:3]
    md_pct = round(100 * ext_counter.get(".md", 0) / max(len(rel), 1), 1)

    def any_path(pattern):
        rx = re.compile(pattern)
        return any(rx.search(p) for p in lower)

    compliant_n = sum(1 for s in skills if s["compliant"])
    row = {
        # skill 結構
        "skill_md_count": len(skills),
        "skill_md_compliant_count": compliant_n,          # G2 Q1:name+description 皆非空
        "claude_md_count": len(claude_paths),
        "skill_spec_compliant": compliant_n > 0,          # BRIEF §6 邊界規則(G2 Q1 起綁合規計數)
        "skill_md_max_lines": max((s["lines"] for s in skills), default=0),
        "skill_md_median_lines": int(statistics.median([s["lines"] for s in skills])) if skills else 0,
        "skill_md_under_500_pct": round(100 * sum(1 for s in skills if s["lines"] < 500) / len(skills), 1) if skills else None,
        "fm_name_pct": round(100 * sum(s["has_name"] for s in skills) / len(skills), 1) if skills else None,
        "fm_description_pct": round(100 * sum(s["has_description"] for s in skills) / len(skills), 1) if skills else None,
        "fm_license_any": any("license" in s["fm_fields"] for s in skills),
        "fm_allowed_tools_any": any(("allowed-tools" in s["fm_fields"]) or ("allowed_tools" in s["fm_fields"]) for s in skills),
        "fm_metadata_any": any("metadata" in s["fm_fields"] for s in skills),
        "desc_len_median": int(statistics.median([s["desc_len"] for s in skills])) if skills else None,
        "desc_has_trigger_pct": round(100 * sum(s["desc_has_trigger"] for s in skills) / len(skills), 1) if skills else None,
        "desc_has_trigger_majority": (sum(s["desc_has_trigger"] for s in skills) * 2 > len(skills)) if skills else False,
        "desc_trigger_contexts_median": int(statistics.median([s["desc_trigger_contexts"] for s in skills])) if skills else None,
        # progressive disclosure / deterministic offloading(skill 層或 repo 根)
        "dir_scripts": any(s["dir_scripts"] for s in skills) or os.path.isdir(os.path.join(root, "scripts")),
        "dir_references": any(s["dir_references"] for s in skills) or os.path.isdir(os.path.join(root, "references")),
        "dir_assets": any(s["dir_assets"] for s in skills) or os.path.isdir(os.path.join(root, "assets")),
        "dir_examples": any(s["dir_examples"] for s in skills) or os.path.isdir(os.path.join(root, "examples")),
        "dir_evals": any(s["dir_evals"] for s in skills) or any_path(r"(^|/)evals?(/|$)"),
        # 打包與安裝
        "has_plugin_json": any_path(r"(^|/)\.claude-plugin/plugin\.json$") or any_path(r"(^|/)plugin\.json$"),
        "has_marketplace_json": any_path(r"(^|/)(\.claude-plugin/)?marketplace\.json$"),
        "has_install_sh": any_path(r"(^|/)install\.sh$"),
        "install_oneliner_in_readme": bool(INSTALL_RE.search(readme)),
        "multi_harness_claims": sorted({t for t in HARNESS_TERMS if t in readme.lower()}),
        "multi_harness_count": len({t.replace("-", " ") for t in HARNESS_TERMS if t in readme.lower()}),
        # 工程品質
        "has_ci": bool(workflows),
        "ci_validates_skills": ci_validates,
        "has_tests_or_evals": any_path(r"(^|/)(tests?|evals?)(/|$)") or any_path(r"evals\.json$|benchmark\.json$"),
        "has_changelog": any_path(r"(^|/)changelog(\.md)?$"),
        "has_version_tags": git_has_tags(root, offline),
        # README 行銷面
        "readme_lines": readme_lines,
        "readme_has_before_after": bool(BEFORE_AFTER_RE.search(readme)),
        "readme_has_metrics": bool(METRIC_RE.search(readme)),
        "readme_has_demo_media": bool(MEDIA_RE.search(readme)),
        # Phase 3b 抽讀名單(G2 Q4:確定性選 ≤5,LLM 只准讀此名單,防 cherry-pick)
        "phase3b_sample": phase3b_sample(skills),
        # misc
        "repo_file_count": len(rel),
        "pct_markdown_files": md_pct,
        "top_extensions": [e for e, _ in top_ext],
        "code_file_count": sum(c for e, c in ext_counter.items() if e in CODE_EXT),
    }
    return row, skills


IDENTITY_KEYS = ["full_name", "stars", "forks", "created_at", "pushed_at", "topics", "license",
                 "taxonomy", "domain", "star_tier", "launch_cohort", "stars_per_month",
                 "author_followers", "author_fame_tier", "prior_fame_proxy", "days_since_creation",
                 "fork_star_ratio", "contributor_count", "nonauthor_pr_count",
                 "open_issues", "owner_is_org",  # G2 Q2/Q5(backfill_repo_fields.py 回填)
                 "in_rubric_sample", "repo_size_kb"]

def main():
    ap = argparse.ArgumentParser(description="Phase 3a 特徵萃取")
    ap.add_argument("--repos", default="research/repos.json")
    ap.add_argument("--manifest", default="research/clone-manifest.json")
    ap.add_argument("--out", default="research")
    ap.add_argument("--limit", type=int, default=0, help="小批次(G2 前 5 個, Iron Rule 5)")
    ap.add_argument("--offline", action="store_true", help="跳過 git ls-remote(無網路環境)")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest: return selftest()

    with open(args.repos, encoding="utf-8") as f:
        repo_meta = {r["full_name"]: r for r in json.load(f)["records"]}
    with open(args.manifest, encoding="utf-8") as f:
        entries = [e for e in json.load(f)["entries"] if e.get("ok")]
    if args.limit: entries = entries[:args.limit]

    matrix, details = [], {}
    for i, e in enumerate(entries, 1):
        root = e["dir"]
        if not os.path.isdir(root):
            print(f"[warn] missing dir {root}, skip"); continue
        print(f"[{i}/{len(entries)}] extracting {e['full_name']}")
        row, skills = analyze_repo(root, offline=args.offline)
        meta = repo_meta.get(e["full_name"], {})
        ident = {k: meta.get(k) for k in IDENTITY_KEYS}
        ident["full_name"] = e["full_name"]
        ident["commit"] = e.get("commit")
        matrix.append({**ident, **row})
        details[e["full_name"]] = {
            "commit": e.get("commit"),
            "skills": [{k: s[k] for k in ("path", "name", "lines", "desc_len",
                                          "desc_has_trigger", "description_head")} for s in skills],
        }

    os.makedirs(args.out, exist_ok=True)
    with open(os.path.join(args.out, "feature_matrix.json"), "w", encoding="utf-8") as f:
        # frontmatter_parser 必須記錄:PyYAML 是選用依賴,有裝/沒裝會走不同 parser。
        # 這個欄位讓任何一份輸出可自我描述「是哪條路徑產出的」,重現時可比對。
        # (兩條路徑的等價性由 scripts/check_parser_agreement.py 守;2026-08-17 起在 161 份實測一致)
        json.dump({"generated_at": datetime.now(timezone.utc).isoformat(),
                   "frontmatter_parser": (f"pyyaml-{yaml.__version__}" if HAVE_YAML
                                          else "naive-fallback"),
                   "python": sys.version.split()[0],
                   "n": len(matrix), "rows": matrix}, f, ensure_ascii=False, indent=2)
    if matrix:
        cols = list(matrix[0].keys())
        with open(os.path.join(args.out, "feature_matrix.csv"), "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            for r in matrix:
                w.writerow({k: (";".join(map(str, v)) if isinstance(v, list) else v) for k, v in r.items()})
    with open(os.path.join(args.out, "skill_details.json"), "w", encoding="utf-8") as f:
        json.dump(details, f, ensure_ascii=False, indent=2)
    print(f"[ok] feature_matrix ({len(matrix)} rows) + skill_details 已輸出到 {args.out}/")
    if args.limit:
        print("[G2] 小批次完成 — 請人工審查 schema 欄位是否足夠,approved 後再全量執行 (Iron Rule 5)")


def selftest():
    # --- _unquote_scalar:naive fallback 的 YAML 轉義還原 ---
    # 這組斷言存在的原因:2026-08-17 在 161 份真實 SKILL.md 上發現 naive fallback 未解
    # 雙引號內的 \\" 轉義,導致「有裝 PyYAML / 沒裝」得到不同的 desc_len。
    # 本函式在 scripts/extract_features.py 與 skill-reviewer/scripts/lint_skill.py 各有一份複本,
    # 兩份不得漂移 —— 這裡與 scripts/check_parser_agreement.py 一起把關。
    assert _unquote_scalar('"say \\"hi\\" now"') == 'say "hi" now'
    assert _unquote_scalar("'it''s'") == "it's"
    assert _unquote_scalar('"a\\tb"') == 'a\tb'
    assert _unquote_scalar('"back\\\\slash"') == 'back\\slash'
    assert _unquote_scalar('plain: value') == 'plain: value'      # 無引號原樣保留
    assert _unquote_scalar('  spaced  ') == 'spaced'
    assert _unquote_scalar('"unclosed') == '"unclosed'            # 引號不成對 → 不動它

    import tempfile
    with tempfile.TemporaryDirectory() as td:
        skill_dir = os.path.join(td, "my-skill"); os.makedirs(os.path.join(skill_dir, "scripts"))
        os.makedirs(os.path.join(td, ".github", "workflows"))
        with open(os.path.join(skill_dir, "SKILL.md"), "w") as f:
            f.write("---\nname: my-skill\ndescription: Does X. Use this skill when the user asks for X, Y, or Z.\n---\n# body\n")
        with open(os.path.join(td, "README.md"), "w") as f:
            f.write("Install: `npx skills add my-skill`\nBefore: slow ❌\nAfter: fast ✅\ncuts 65% of tokens\nWorks with Claude Code and Cursor.\n![demo](demo.gif)\n")
        with open(os.path.join(td, ".github", "workflows", "ci.yml"), "w") as f:
            f.write("name: ci\n# validate skill frontmatter lint\n")
        # G2 Q1:空殼 SKILL.md(無 frontmatter)不合規
        empty_dir = os.path.join(td, "empty-skill"); os.makedirs(empty_dir)
        with open(os.path.join(empty_dir, "SKILL.md"), "w") as f:
            f.write("# just a title, no frontmatter\n")
        row, skills = analyze_repo(td, offline=True)
        assert row["skill_md_count"] == 2 and row["skill_md_compliant_count"] == 1
        assert row["skill_spec_compliant"] is True
        # 模擬 Windows 分隔符:relpath 正規化在 POSIX 是 no-op,不逼它跑就等於沒測
        # (未正規化時 (^|/) regex 與 ".github/workflows/" 前綴比對全部靜默失效)
        _rp, _sep = os.path.relpath, os.sep
        try:
            os.path.relpath = lambda q, start: _rp(q, start).replace("/", "\\")
            os.sep = "\\"
            roww, skillsw = analyze_repo(td, offline=True)
            assert roww["skill_md_count"] == row["skill_md_count"], (roww["skill_md_count"], row["skill_md_count"])
            assert roww["dir_scripts"] == row["dir_scripts"], "Windows 分隔符下 dir_scripts 不一致"
            assert roww["has_ci"] == row["has_ci"], "Windows 分隔符下 has_ci 不一致(.github/workflows/ 前綴比對)"
            assert all("\\" not in sk["path"] for sk in skillsw), [sk["path"] for sk in skillsw]
        finally:
            os.path.relpath, os.sep = _rp, _sep
        # G2 Q3:擴充句式與中文觸發語
        assert TRIGGER_RE.search("This skill should be used when designing a page")
        assert TRIGGER_RE.search("Activates for security questions")
        assert TRIGGER_RE.search("當使用者要求產生投影片時使用")
        assert not TRIGGER_RE.search("Toolkit for styling artifacts with a theme")
        # G2 Q4:phase3b_sample 確定性且 ≤5
        fake = [{"path": f"s{i}/SKILL.md", "lines": i * 10} for i in range(1, 9)]
        p1, p2 = phase3b_sample(fake), phase3b_sample(list(reversed(fake)))
        assert p1 == p2 and len(p1) == 5, (p1, p2)
        assert "s8/SKILL.md" in p1  # max-lines 必入選
        assert row["fm_name_pct"] == 50.0 and row["desc_has_trigger_pct"] == 50.0  # 2 skills,1 合規
        good = next(s for s in skills if s["compliant"])
        assert good["desc_trigger_contexts"] >= 3, good["desc_trigger_contexts"]
        assert row["dir_scripts"] is True and row["install_oneliner_in_readme"] is True
        assert row["readme_has_before_after"] and row["readme_has_metrics"] and row["readme_has_demo_media"]
        assert row["has_ci"] and row["ci_validates_skills"]
        assert row["multi_harness_count"] >= 2
        # CLAUDE.md-only 邊界案例 (BRIEF §6 v1.2.1)
        with tempfile.TemporaryDirectory() as td2:
            with open(os.path.join(td2, "CLAUDE.md"), "w") as f:
                f.write("# rules\n")
            row2, _ = analyze_repo(td2, offline=True)
            assert row2["skill_md_count"] == 0 and row2["claude_md_count"] == 1
            assert row2["skill_spec_compliant"] is False
    fm, body = parse_frontmatter("---\nname: a\ndescription: b\n---\nbody")
    assert fm == {"name": "a", "description": "b"} and body == "body"
    fm2, _ = parse_frontmatter("no frontmatter here")
    assert fm2 == {}
    print("[selftest] extract_features: all assertions passed ✔")

if __name__ == "__main__":
    main()
