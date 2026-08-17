#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lint_skill.py — skill-reviewer 的 deterministic 檢查層(Phase 5, BRIEF §3/§8)

對「一個 skill repo 目錄」做純靜態分析,輸出結構化 findings JSON。
SKILL.md 指示 LLM 先讀本輸出,再做 craft_llm 質化維度。

設計原則(繼承本研究方法論):
  - 純靜態讀取,絕不執行目標 repo 任何檔案(供應鏈警覺)
  - script 部分本質是 packaging benchmark;craft 由 LLM 層補(見 SKILL.md)
  - 措辭紀律:輸出「符合 X 星級剖面」,不宣稱「會得 X 星」

用法:
  python3 lint_skill.py <repo_dir>            # 人類可讀
  python3 lint_skill.py <repo_dir> --json     # 機器可讀(給 SKILL.md 的 LLM 讀)
  python3 lint_skill.py --selftest
"""
import argparse, json, os, re, sys, statistics

# Windows 可攜性:輸出重導向時 Python 用 locale 編碼(cp950/cp1252),本工具的訊息含中文,
# 不處理會直接 UnicodeEncodeError 而不是印出結果。出貨工具必須自己站得住,
# 不能要求使用者先設 PYTHONUTF8=1。(reconfigure 是 3.7+;失敗就維持原狀,不讓它擋住主流程。)
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8")
        except (OSError, ValueError):
            pass

SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "dist", "build", "__pycache__"}
MAX_READ = 2_000_000
CODE_EXT = {".py", ".sh", ".js", ".ts", ".mjs", ".rb", ".go", ".rs"}

TRIGGER_RE = re.compile(
    r"(?i)\b(use\s+(?:this\s+)?(?:skill\s+)?when|use\s+when|use\s+it\s+when|"
    r"trigger(?:s|ed)?\s+(?:when|if|include|whenever)|whenever\s+the\s+user|"
    r"use\s+this\s+(?:skill|tool)\s+(?:for|to|whenever)|invoke\s+when|"
    r"(?:should|can|may)\s+be\s+used\s+when|used\s+when|activates?\s+(?:for|when)|"
    r"當使用者|當你|使用時機|何時使用|觸發)")
INSTALL_RE = re.compile(
    r"(npx\s+skills|gh\s+skill|/plugin\s+(?:install|marketplace)|"
    r"curl[^\n]{0,140}install\.sh|npm\s+i(?:nstall)?\s+(?:-g|--global)|pipx?\s+install|brew\s+install)")
# code-review F1:對齊 extract_features 的校準版正則(weight 由該版偵測校準),否則出貨審查器
# 會系統性低估 readme_has_before_after 並在 gap_list 錯報缺項
BEFORE_AFTER_RE = re.compile(
    r"(?is)(before\W{0,3}after|with\s+(?:the\s+)?skill.{0,120}?without|"
    r"without.{0,120}?with\s+(?:the\s+)?skill|❌.{0,500}?✅|✅.{0,500}?❌|\bBefore\b.{0,800}?\bAfter\b)")
# 安全紅旗(S-001/S-003 靜態可測部分)
REDFLAG_OBEY_OUTPUT = re.compile(r"(?is)(follow\s+(?:it|what\s+it\s+prints|the\s+guide)\s+(?:to\s+the\s+letter|exactly)|"
                                 r"don'?t\s+stop\s+for\s+confirmation|without\s+(?:stopping\s+for\s+)?confirmation)")
REDFLAG_CRED_ARGV = re.compile(r"--api[-_]?key[= ]\$?\w|--token[= ]\$?\w")
REDFLAG_SELF_UPDATE = re.compile(r"(?im)git\s+pull|git\s+fetch[^\n]{0,60}(pull|merge)")
DEFENSE_UNTRUSTED = re.compile(r"(?is)(untrusted\s+data|as\s+data,?\s+not\s+instructions|"
                               r"never\s+follow\s+(?:instructions|embedded)|treat\s+external\s+content\s+as\s+data)")


def read_text(p):
    try:
        with open(p, encoding="utf-8", errors="replace") as f: return f.read(MAX_READ)
    except OSError: return ""

def walk(root, exclude=None):
    """exclude:相對 root 的路徑前綴清單,用來排除 vendored/第三方 clone 目錄。
    預設不排除任何東西——與研究 pipeline 的 extract_features.py 行為一致(避免分歧)。"""
    exclude = [e.strip("/") for e in (exclude or [])]
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in SKIP_DIRS]
        if exclude:
            rel_dp = os.path.relpath(dp, root).replace(os.sep, "/")
            rel_dp = "" if rel_dp == "." else rel_dp
            dns[:] = [d for d in dns
                      if not any((f"{rel_dp}/{d}" if rel_dp else d) == e
                                 or (f"{rel_dp}/{d}" if rel_dp else d).startswith(e + "/")
                                 for e in exclude)]
        for fn in fns: yield os.path.join(dp, fn)

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


def parse_fm(text):
    m = re.match(r"^﻿?---[ \t]*\n(.*?)\n---[ \t]*(?:\n|$)", text, re.S)
    if not m: return {}, text
    d = {}
    lines = m.group(1).splitlines()
    i = 0
    while i < len(lines):
        # YAML 多行純量,兩種寫法都要收後續縮排行:
        #   (a) 顯式 block scalar:`key: |` / `key: >`(含 |- 、|2 等 chomping/indent 指示)
        #   (b) 隱式多行純量:`key:` 後直接換行,接縮排文字(vercel-labs/agent-skills 實例)
        # (b) 必須排除巢狀 mapping(如 `metadata:` 後接 `  author: x`),否則會把字典折成字串。
        mb = re.match(r"^([A-Za-z0-9_\-]+)\s*:\s*[|>][+-]?\d*\s*$", lines[i])
        if not mb and re.match(r"^([A-Za-z0-9_\-]+)\s*:\s*$", lines[i]):
            nxt = next((l for l in lines[i+1:] if l.strip()), "")
            # 縮排且「不是 key: value 形式」→ 判為多行純量;否則是 mapping,交給下方一般分支
            if re.match(r"^\s+", nxt) and not re.match(r"^\s+[A-Za-z0-9_\-]+\s*:", nxt):
                mb = re.match(r"^([A-Za-z0-9_\-]+)\s*:\s*$", lines[i])
        if mb:
            key = mb.group(1).lower(); i += 1; block = []
            while i < len(lines) and (lines[i].strip() == "" or re.match(r"^\s+", lines[i])):
                block.append(lines[i].strip()); i += 1
            d[key] = " ".join(x for x in block if x).strip()
            continue
        mm = re.match(r"^([A-Za-z0-9_\-]+)\s*:\s*(.*)$", lines[i])
        if mm: d[mm.group(1).lower()] = _unquote_scalar(mm.group(2))
        i += 1
    return d, text[m.end():]

def analyze(root, exclude=None):
    files = list(walk(root, exclude))
    rel = [os.path.relpath(p, root).replace(os.sep, "/") for p in files]  # Windows 可攜性:relpath 用 os.sep,但下游全部以 "/" 比對
    # ((^|/)scripts(/|$) 之類的 regex、changed_files 交集、.github/workflows/ 前綴),
    # 反斜線會讓那些比對全部靜默失效(dir_* 誤判 false、H-005 交集永遠空)。
    # POSIX 上 os.sep 就是 "/",此行為 no-op。
    lower = [p.lower() for p in rel]
    skills = []
    for i, p in enumerate(lower):
        if os.path.basename(p) == "skill.md":
            t = read_text(files[i]); fm, _ = parse_fm(t)
            desc = fm.get("description", "")
            skills.append({"path": rel[i], "lines": t.count("\n")+1,
                           "name": fm.get("name",""), "desc": desc,
                           "compliant": bool(fm.get("name","").strip()) and bool(desc.strip()),
                           "has_trigger": bool(TRIGGER_RE.search(desc)),
                           "text_head": t[:4000]})
    readme = next((read_text(files[i]) for i,p in enumerate(lower)
                   if os.path.basename(p) in ("readme.md","readme")), "")
    def has(pat): rx=re.compile(pat); return any(rx.search(p) for p in lower)
    all_text = "\n".join(read_text(f) for f in files if f.lower().endswith((".md",".yml",".yaml",".sh")))[:2_000_000]
    # S-003 self_update 收窄:只掃 agent 會讀的指令面(SKILL.md / hooks / scripts),不掃 README。
    # 理由(實證):README 的「## 更新 → git pull」是給人看的手動更新說明,非 agent 自我更新;
    # 3/3 已發布 repo 皆因此誤報(final review M4 預測的 flag 疲勞)。真陽性樣態是 SKILL.md 內
    # 指示 agent 每次啟動 git fetch 檢查上游(guizang-ppt-skill)。
    # agent-facing = SKILL.md 全文 + hooks(agent 自動讀/自動跑的東西)。
    # 刻意排除 README(給人看)與 install.sh(人為明示執行的安裝器,非 runtime 自我更新)。
    agent_facing = "\n".join(
        read_text(files[i]) for i, p in enumerate(lower)
        if os.path.basename(p) == "skill.md" or "/hooks/" in p or p.startswith("hooks/")
    )[:1_000_000]

    # 條 2 支援:純知識/參考型偵測(壓倒性 Markdown、幾乎無程式碼)
    n_files = max(len(rel), 1)
    n_md = sum(1 for p in lower if p.endswith(".md"))
    n_code = sum(1 for p in lower if os.path.splitext(p)[1] in CODE_EXT)
    pct_markdown = round(100 * n_md / n_files, 1)
    knowledge_only = pct_markdown >= 85.0 and n_code <= 2 and not has(r"(^|/)scripts(/|$)")

    # 條 3:S-002 收窄——只認 .claude/hooks/ 或 hooks/ 下的實際腳本、或 SKILL.md frontmatter 註冊 hook 事件;
    # 不再掃內文 "hook" 字(會誤中 React hooks / GSAP hook)
    hook_dir = has(r"(^|/)\.?claude/hooks/") or has(r"(^|/)hooks/[^/]+\.(sh|js|ts|py)$")
    hook_fm = any(re.search(r"(?im)^\s*(hooks|PreToolUse|PostToolUse|UserPromptSubmit|SessionStart)\s*:",
                            s["text_head"][:800]) for s in skills)
    return {
        "skill_md_count": len(skills),
        "skill_md_compliant_count": sum(s["compliant"] for s in skills),
        # H-005:逐檔不合規清單。呼叫端(如 ASP G5)可與「本次變更檔案」取交集,
        # 精準判定「這次改壞了」——關閉 H-001 只問 repo 級「≥1 合規」的盲點。
        "noncompliant_skills": [s["path"] for s in skills if not s["compliant"]],
        "skill_md_max_lines": max((s["lines"] for s in skills), default=0),
        "desc_has_trigger_pct": round(100*sum(s["has_trigger"] for s in skills)/len(skills),1) if skills else None,
        "dir_scripts": has(r"(^|/)scripts(/|$)"),
        "dir_examples": has(r"(^|/)examples?(/|$)"),
        "dir_references": has(r"(^|/)references?(/|$)"),
        "has_marketplace_json": has(r"marketplace\.json$"),
        "has_tests_or_evals": has(r"(^|/)(tests?|evals?)(/|$)") or has(r"evals\.json$"),
        "install_oneliner_in_readme": bool(INSTALL_RE.search(readme)),
        "readme_has_before_after": bool(BEFORE_AFTER_RE.search(readme)),
        "pct_markdown": pct_markdown, "code_file_count": n_code, "knowledge_only": knowledge_only,
        "_skills": skills,
        "_redflags": {
            "obey_external_output": bool(REDFLAG_OBEY_OUTPUT.search(all_text)),
            "cred_in_argv": bool(REDFLAG_CRED_ARGV.search(all_text)),
            "self_update": bool(REDFLAG_SELF_UPDATE.search(agent_facing)),  # 只掃 agent 指令面
            "registers_hooks": hook_dir or hook_fm,
        },
        "_defense_untrusted": bool(DEFENSE_UNTRUSTED.search(all_text)),
    }

# 5 條 script differentiator(weight 來自 G3 定稿 rubric.yaml)
DIFFERENTIATORS = [
    ("has_tests_or_evals", 4, "craft"),
    ("install_oneliner_in_readme", 3, "packaging"),
    ("has_marketplace_json", 3, "packaging"),
    ("dir_examples", 2, "craft"),
    ("readme_has_before_after", 2, "marketing"),
]

def build_findings(m, changed_files=None):
    findings = {"hygiene": [], "differentiators": [], "security": [], "craft_llm_todo": []}
    # H-001/002/003/004 hygiene 門檻
    findings["hygiene"].append({"id":"H-001","pass": m["skill_md_compliant_count"]>=1,
        "detail": f"合規 SKILL.md 數={m['skill_md_compliant_count']}", "severity":"error"})
    # H-005:逐檔合規(關閉 H-001 的 repo 級盲點)。
    # severity 的情境判定在此處**一次決定**,呼叫端只消費結果——不得在呼叫端重新編碼政策
    # (ADR-031:同一意義兩處編碼會 drift)。給了 --changed-files 就是 change-scoped 情境。
    nc = m["noncompliant_skills"]
    hit = sorted(set(nc) & set(changed_files or [])) if changed_files else []
    if changed_files is not None:
        # change-scoped:只有「本次變更改壞的」才 error;既有不合規檔不擋(不因別人的爛攤子阻斷你)
        h5 = {"id":"H-005", "scope":"change-scoped", "pass": not hit,
              "severity": "error" if hit else "warning",
              "detail": (f"本次變更含 {len(hit)} 個不合規 SKILL.md:{hit}" if hit else
                         (f"本次變更未觸及不合規檔(repo 內另有 {len(nc)} 個既有不合規,不擋)"
                          if nc else "全部 SKILL.md 合規")),
              "noncompliant": nc, "changed_noncompliant": hit}
    else:
        # repo-wide:一律 warning,不因既有爛攤子擋住無關改動
        h5 = {"id":"H-005", "scope":"repo-wide", "pass": not nc, "severity":"warning",
              "detail": (f"{len(nc)} 個 SKILL.md 缺 name/description:{nc[:5]}"
                         + (f" …共 {len(nc)} 個" if len(nc)>5 else "")) if nc else "全部 SKILL.md 合規",
              "noncompliant": nc, "changed_noncompliant": []}
    findings["hygiene"].append(h5)
    findings["hygiene"].append({"id":"H-003","pass": m["skill_md_max_lines"]<500 or m["dir_references"],
        "detail": f"max_lines={m['skill_md_max_lines']}, references/={m['dir_references']}",
        "severity":"warning", "note":"長度非絕對(jezweb 反證);references/ 分層亦可"})
    # 條 2:純知識/參考型 skill 豁免 deterministic offloading(本就無確定性操作)
    if m["knowledge_only"] and not m["dir_scripts"]:
        findings["hygiene"].append({"id":"H-004","pass": None, "exempt": True,
            "detail": f"純知識型豁免(md={m['pct_markdown']}%, code={m['code_file_count']})", "severity":"info"})
    else:
        findings["hygiene"].append({"id":"H-004","pass": m["dir_scripts"],
            "detail": f"dir_scripts={m['dir_scripts']}", "severity":"info"})
    # differentiators 計分
    score = 0; maxscore = 0
    for feat, w, sig in DIFFERENTIATORS:
        got = bool(m[feat]); maxscore += w; score += w if got else 0
        findings["differentiators"].append({"feature":feat,"present":got,"weight":w,"signal":sig})
    findings["_score"] = score; findings["_maxscore"] = maxscore
    # security(S-001/S-002/S-003 靜態部分 + S-101 正面)
    rf = m["_redflags"]
    # confidence:靜態 regex 假陽性高者標 low → SKILL.md 指示 LLM 複核,不得單憑 lint 判死
    for key, sid, sev, conf in [("obey_external_output","S-001","error","low-static-needs-llm"),
                                ("registers_hooks","S-002","warning","low-static-needs-llm"),
                                ("cred_in_argv","S-003","warning","medium"),
                                ("self_update","S-003","warning","low-static-needs-llm")]:
        if rf[key]:
            findings["security"].append({"id":sid,"flag":key,"severity":sev,"confidence":conf})
    if m["_defense_untrusted"]:
        findings["security"].append({"id":"S-101","flag":"defensive_untrusted_clause","polarity":"positive"})
    # craft LLM 待判(把樣本餵給 SKILL.md 的 LLM 層)
    findings["craft_llm_todo"] = [{"path":s["path"],"desc_has_trigger":s["has_trigger"],
        "desc_head":s["desc"][:160]} for s in sorted(m["_skills"], key=lambda s:-s["lines"])[:5]]
    return findings

def tier_benchmark(score, maxscore):
    """措辭紀律:符合剖面,非『會得星』。門檻由 G3 樣本 differentiator 分布近似。"""
    pct = score/maxscore if maxscore else 0
    if pct >= 0.8: return "符合 T3(頂層)剖面"
    if pct >= 0.55: return "符合 T2(10k 星級)剖面"
    if pct >= 0.3: return "符合 T1(1k 星級)剖面"
    return "低於 T1 剖面(packaging 面待補)"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo_dir", nargs="?")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--changed-files", default=None,
                    help="逗號分隔的本次變更檔案(repo 相對路徑)。給了就切換為 change-scoped 情境:"
                         "只有變更集內的不合規 SKILL.md 才升 error;既有不合規仍只是 warning。"
                         "severity 由本工具一次決定,呼叫端不得自行重算(ADR-031 防 drift)")
    ap.add_argument("--exclude", default=None,
                    help="逗號分隔的相對路徑,排除 vendored/第三方 clone 目錄"
                         "(例:--exclude research/repos)。預設不排除,與研究 pipeline 行為一致")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: return selftest()
    if not a.repo_dir or not os.path.isdir(a.repo_dir):
        print("usage: lint_skill.py <repo_dir> [--changed-files a,b] [--json]", file=sys.stderr); return 2
    changed = None
    if a.changed_files is not None:
        changed = [p.strip() for p in a.changed_files.split(",") if p.strip()]
    excl = [p.strip() for p in a.exclude.split(",") if p.strip()] if a.exclude else None
    m = analyze(a.repo_dir, excl); f = build_findings(m, changed)
    # 條 1:tier 分軌——packaging tier 僅為 packaging 面,非總評;總評 tier 由 craft(LLM)決定
    out = {"repo": a.repo_dir, "hygiene": f["hygiene"], "differentiators": f["differentiators"],
           "packaging_score": f["_score"], "packaging_max": f["_maxscore"],
           "tier_benchmark_packaging": tier_benchmark(f["_score"], f["_maxscore"]),
           "knowledge_only": m["knowledge_only"],
           # H-005 的判定結果在 hygiene[] 內(severity 已定案);此處僅保留原始清單供人閱讀
           "noncompliant_skills": m["noncompliant_skills"],
           "scope": "change-scoped" if changed is not None else "repo-wide",
           "benchmark_note": ("僅 packaging 面,非總評;craft tier 由 SKILL.md 的 LLM 層判。"
                              + ("此 repo 疑為純知識/內部型:packaging 面天然偏低,tier 應以 craft 剖面為準,"
                                 "packaging 子分數可宣告不採計。" if m["knowledge_only"] else "")),
           "craft_tier": "PENDING-LLM(讀 craft_llm_todo 後由 SKILL.md 層填)",
           "security": f["security"], "craft_llm_todo": f["craft_llm_todo"],
           "gap_list": [d["feature"] for d in sorted(f["differentiators"], key=lambda x:-x["weight"])
                        if not d["present"]]}
    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=2)); return 0
    hyg_fail = [h for h in f["hygiene"] if h["pass"] is False and h["severity"]=="error"]
    def hmark(h): return "—" if h["pass"] is None else ("✓" if h["pass"] else "✗")
    print(f"== skill-reviewer lint: {a.repo_dir} ==")
    print(f"[hygiene] {'FAIL' if hyg_fail else 'pass'}  " +
          " ".join(f"{h['id']}={hmark(h)}" for h in f["hygiene"]) +
          ("  (— = 純知識型豁免)" if any(h['pass'] is None for h in f['hygiene']) else ""))
    print(f"[packaging tier · 僅 packaging 面] {f['_score']}/{f['_maxscore']} → {out['tier_benchmark_packaging']}")
    print(f"[craft tier] {out['craft_tier']}")
    if m["knowledge_only"]:
        print("  ⚠ 純知識/內部型:packaging 天然偏低,總評應以 craft 剖面為準(packaging 可宣告不採計)")
    print(f"[gap list · packaging] {out['gap_list'] or '(packaging 面已滿)'}")
    if f["security"]:
        print(f"[security] " + "; ".join(
            f"{s['id']}:{s.get('flag')}" + (f"({s['confidence']})" if s.get('confidence') else "")
            for s in f["security"]))
    print(f"[craft→LLM] 交 SKILL.md 質化審 {len(f['craft_llm_todo'])} 個樣本(trigger/style/scope)")
    print("\n措辭紀律:packaging tier 非總評、非星數預測。總評 craft verdict 需 LLM 讀 craft_llm_todo 後才完成。")
    return 0

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
        sd = os.path.join(td,"s"); os.makedirs(os.path.join(sd,"scripts"))
        os.makedirs(os.path.join(td,"examples")); os.makedirs(os.path.join(td,"evals"))
        open(os.path.join(td,"examples","demo.md"),"w").write("x")   # 非空目錄才會被 walk 命中
        open(os.path.join(td,"evals","evals.json"),"w").write("[]")
        open(os.path.join(sd,"SKILL.md"),"w").write("---\nname: s\ndescription: Does X. Use when the user asks for X.\n---\nbody\n")
        open(os.path.join(td,"README.md"),"w").write("Install: npx skills add s\nBefore: slow ❌ After: fast ✅\n")
        open(os.path.join(td,"marketplace.json"),"w").write("{}")
        m = analyze(td); f = build_findings(m)
        assert m["skill_md_compliant_count"]==1 and m["desc_has_trigger_pct"]==100.0
        assert f["_score"]==f["_maxscore"], (f["_score"], f["_maxscore"])  # 全 packaging 特徵齊備
        assert tier_benchmark(f["_score"], f["_maxscore"]).startswith("符合 T3")

        # --- 模擬 Windows 路徑分隔符 ---
        # 這段存在的原因:相對路徑正規化(relpath → "/")在 POSIX 上是 no-op,
        # 所以「沒有正規化」和「有正規化」在 Linux CI 上跑出來一模一樣 —— 等於沒測到。
        # 這裡把 os.path.relpath 與 os.sep 換成 Windows 行為,逼那條路徑真的被執行。
        # 沒有正規化時會發生什麼:每條 has() 的 (^|/) regex 都比不到 → dir_scripts /
        # dir_examples / dir_references / has_tests_or_evals 全誤判 false(packaging 分數系統性偏低),
        # 且 noncompliant_skills 變成 "bad\\SKILL.md" → G5 與 changed_files 的交集永遠是空,
        # H-005 change-scoped 靜默失效。
        _rp, _sep = os.path.relpath, os.sep
        try:
            os.path.relpath = lambda q, start: _rp(q, start).replace("/", "\\")
            os.sep = "\\"
            mw = analyze(td); fw = build_findings(mw)
            # 該守的不變式是「平台不改變判定」,不是某個特徵一定為 True
            # (fixture 的 scripts/ 是空目錄,os.walk 不產檔,所以 dir_scripts 兩邊都是 False)
            PATH_SENSITIVE = ("dir_scripts", "dir_examples", "dir_references",
                              "has_tests_or_evals", "has_marketplace_json", "knowledge_only")
            for k in PATH_SENSITIVE:
                assert mw[k] == m[k], f"Windows 分隔符改變了 {k}: {mw[k]} != {m[k]}"
            assert fw["_score"] == f["_score"], (fw["_score"], f["_score"])
            assert mw["_redflags"] == m["_redflags"], (mw["_redflags"], m["_redflags"])
            assert all("\\" not in sk["path"] for sk in mw["_skills"]), \
                [sk["path"] for sk in mw["_skills"]]                          # 對外路徑一律 "/"
        finally:
            os.path.relpath, os.sep = _rp, _sep
        # 安全紅旗偵測
        open(os.path.join(sd,"SKILL.md"),"w").write("---\nname: s\ndescription: d\n---\nInstall in one pass; don't stop for confirmation.\n")
        m2 = analyze(td); f2 = build_findings(m2)
        assert any(s["id"]=="S-001" for s in f2["security"]), f2["security"]
    # 條 3:內文提到 React hooks 不應觸發 S-002(收窄後)
    with tempfile.TemporaryDirectory() as td:
        sd = os.path.join(td,"s"); os.makedirs(sd)
        open(os.path.join(sd,"SKILL.md"),"w").write("---\nname: s\ndescription: d\n---\nUse React hooks and GSAP hook wisely.\n")
        m3 = analyze(td)
        assert m3["_redflags"]["registers_hooks"] is False, "內文 hook 字不應觸發 S-002"
        # frontmatter 註冊 hook 事件才算
        open(os.path.join(sd,"SKILL.md"),"w").write("---\nname: s\ndescription: d\nhooks:\n  PreToolUse: x\n---\nbody\n")
        assert analyze(td)["_redflags"]["registers_hooks"] is True, "frontmatter hooks 應觸發 S-002"
    # 條 2:純知識型豁免 H-004
    with tempfile.TemporaryDirectory() as td:
        sd = os.path.join(td,"s"); os.makedirs(os.path.join(sd,"references"))
        open(os.path.join(sd,"SKILL.md"),"w").write("---\nname: s\ndescription: Use when writing.\n---\nbody\n")
        open(os.path.join(sd,"references","g.md"),"w").write("guide")
        m4 = analyze(td); f4 = build_findings(m4)
        assert m4["knowledge_only"] is True, (m4["pct_markdown"], m4["code_file_count"])
        h004 = next(h for h in f4["hygiene"] if h["id"]=="H-004")
        assert h004["pass"] is None and h004.get("exempt"), h004
    # H-005:逐檔合規(關閉 H-001 repo 級盲點)——1 好 1 壞時 H-001 仍 pass,H-005 須列出壞的
    with tempfile.TemporaryDirectory() as td:
        good = os.path.join(td,"good"); bad = os.path.join(td,"bad")
        os.makedirs(good); os.makedirs(bad)
        open(os.path.join(good,"SKILL.md"),"w").write("---\nname: g\ndescription: Use when X.\n---\nbody\n")
        open(os.path.join(bad,"SKILL.md"),"w").write("# 無 frontmatter 的壞檔\n")
        m5 = analyze(td); f5 = build_findings(m5)
        h001 = next(h for h in f5["hygiene"] if h["id"]=="H-001")
        h005 = next(h for h in f5["hygiene"] if h["id"]=="H-005")
        assert h001["pass"] is True, "H-001 應仍 pass(repo 有 ≥1 合規)——這正是盲點所在"
        assert h005["pass"] is False and h005["severity"]=="warning", h005
        assert m5["noncompliant_skills"] == ["bad/SKILL.md"], m5["noncompliant_skills"]
        # 必須出現在 --json 頂層,否則 G5 取交集拿不到(回歸腳本實際踩過這個洞)
        import subprocess as _sp
        _j = json.loads(_sp.run([sys.executable, os.path.abspath(__file__), td, "--json"],
                                capture_output=True, text=True).stdout)
        assert _j["noncompliant_skills"] == ["bad/SKILL.md"], "noncompliant_skills 未出現在 JSON 頂層"
        # change-scoped(ADR-031 防 drift:severity 由 lint 一次決定,呼叫端不重算)
        f5c = build_findings(m5, ["bad/SKILL.md"])          # 變更改壞了 → error
        h5c = next(h for h in f5c["hygiene"] if h["id"]=="H-005")
        assert h5c["severity"]=="error" and h5c["scope"]=="change-scoped" and h5c["changed_noncompliant"]==["bad/SKILL.md"], h5c
        f5d = build_findings(m5, ["good/SKILL.md"])         # 變更沒碰到壞檔 → 既有不合規不擋
        h5d = next(h for h in f5d["hygiene"] if h["id"]=="H-005")
        assert h5d["severity"]=="warning" and h5d["changed_noncompliant"]==[], h5d
        f5e = build_findings(m5, [])                        # 空變更集也算 change-scoped,不擋
        assert next(h for h in f5e["hygiene"] if h["id"]=="H-005")["severity"]=="warning"
        # 全合規時 H-005 應 pass 且清單為空
        open(os.path.join(bad,"SKILL.md"),"w").write("---\nname: b\ndescription: Use when Y.\n---\nbody\n")
        m5b = analyze(td)
        assert m5b["noncompliant_skills"] == [], m5b["noncompliant_skills"]
    # --exclude:vendored/第三方 clone 目錄不該被算成自己的(自審時實際踩過)
    with tempfile.TemporaryDirectory() as td:
        own = os.path.join(td,"skills","mine"); vend = os.path.join(td,"vendor","theirs")
        os.makedirs(own); os.makedirs(vend)
        open(os.path.join(own,"SKILL.md"),"w").write("---\nname: m\ndescription: Use when X.\n---\nbody\n")
        open(os.path.join(vend,"SKILL.md"),"w").write("# 第三方的壞檔,無 frontmatter\n")
        assert analyze(td)["noncompliant_skills"] == ["vendor/theirs/SKILL.md"], "未排除時應看到第三方檔"
        assert analyze(td, ["vendor"])["noncompliant_skills"] == [], "排除後不該再算第三方檔"
        assert analyze(td, ["vendor"])["skill_md_count"] == 1, "排除後只剩自己的 1 個"

    # S-003 self_update 收窄:README 的手動更新說明不該觸發,SKILL.md 內的自我更新才算
    with tempfile.TemporaryDirectory() as td:
        sd = os.path.join(td,"s"); os.makedirs(sd)
        open(os.path.join(sd,"SKILL.md"),"w").write("---\nname: s\ndescription: d\n---\nbody\n")
        open(os.path.join(td,"README.md"),"w").write("## 更新\n\n```bash\ngit pull\n./install.sh --force\n```\n")
        assert analyze(td)["_redflags"]["self_update"] is False, "README 的手動更新說明不該觸發 S-003"
        open(os.path.join(sd,"SKILL.md"),"w").write("---\nname: s\ndescription: d\n---\nStep 0: git pull 檢查上游更新\n")
        assert analyze(td)["_redflags"]["self_update"] is True, "SKILL.md 內的自我更新應觸發 S-003"
    # §7 bug fix:YAML block scalar description 應被解析、觸發語應抓到
    fm_b, _ = parse_fm("---\nname: s\ndescription: |\n  多行描述第一行。\n  當你要做 X 時必須載入。\n  Triggers: a, b, c\n---\nbody")
    assert "當你要做" in fm_b["description"] and TRIGGER_RE.search(fm_b["description"]), fm_b
    # 隱式多行純量(`description:` 後直接換行接縮排)——vercel-labs/agent-skills 實例
    fm_i, _ = parse_fm("---\nname: n\ndescription:\n  React patterns. Use when refactoring\n  components.\nlicense: MIT\n---\nbody")
    assert fm_i["description"].startswith("React patterns"), fm_i
    assert fm_i["license"] == "MIT", "隱式純量不可吞掉後續同層 key"
    # 巢狀 mapping 不可被折成字串
    fm_m, _ = parse_fm("---\nname: n\ndescription: d\nmetadata:\n  author: vercel\n  version: '1.0'\n---\nbody")
    assert fm_m["description"] == "d" and "author" not in str(fm_m.get("metadata","")), fm_m
    # code-review F5 drift-guard:硬編 DIFFERENTIATORS weights 必須與 references/rubric.yaml 一致
    # (lint runtime 不讀 yaml 以保零依賴;僅 selftest 以 naive 正則比對,rubric.yaml 改而此處未改即 fail)
    rubric_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                               "references", "rubric.yaml")
    if os.path.isfile(rubric_path):
        txt = read_text(rubric_path)
        yaml_w = dict(re.findall(r"feature:\s*(\S+)[\s\S]*?weight:\s*(\d+)", txt))
        for feat, w, _sig in DIFFERENTIATORS:
            if feat in yaml_w:
                assert int(yaml_w[feat]) == w, f"drift: {feat} lint={w} rubric.yaml={yaml_w[feat]}"
    print("[selftest] lint_skill: all assertions passed ✔")

if __name__ == "__main__":
    sys.exit(main())
