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

SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "dist", "build", "__pycache__"}
MAX_READ = 2_000_000

TRIGGER_RE = re.compile(
    r"(?i)\b(use\s+(?:this\s+)?(?:skill\s+)?when|use\s+when|use\s+it\s+when|"
    r"trigger(?:s|ed)?\s+(?:when|if|include|whenever)|whenever\s+the\s+user|"
    r"use\s+this\s+(?:skill|tool)\s+(?:for|to|whenever)|invoke\s+when|"
    r"(?:should|can|may)\s+be\s+used\s+when|used\s+when|activates?\s+(?:for|when)|"
    r"當使用者|當你|使用時機|何時使用|觸發)")
INSTALL_RE = re.compile(
    r"(npx\s+skills|gh\s+skill|/plugin\s+(?:install|marketplace)|"
    r"curl[^\n]{0,140}install\.sh|npm\s+i(?:nstall)?\s+(?:-g|--global)|pipx?\s+install|brew\s+install)")
BEFORE_AFTER_RE = re.compile(
    r"(?is)(before\W{0,3}after|without.{0,120}?with\s+(?:the\s+)?skill|❌.{0,500}?✅|✅.{0,500}?❌)")
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

def walk(root):
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in SKIP_DIRS]
        for fn in fns: yield os.path.join(dp, fn)

def parse_fm(text):
    m = re.match(r"^﻿?---[ \t]*\n(.*?)\n---[ \t]*(?:\n|$)", text, re.S)
    if not m: return {}, text
    d = {}
    for line in m.group(1).splitlines():
        mm = re.match(r"^([A-Za-z0-9_\-]+)\s*:\s*(.*)$", line)
        if mm: d[mm.group(1).lower()] = mm.group(2).strip().strip("'\"")
    return d, text[m.end():]

def analyze(root):
    files = list(walk(root)); rel = [os.path.relpath(p, root) for p in files]
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
    return {
        "skill_md_count": len(skills),
        "skill_md_compliant_count": sum(s["compliant"] for s in skills),
        "skill_md_max_lines": max((s["lines"] for s in skills), default=0),
        "desc_has_trigger_pct": round(100*sum(s["has_trigger"] for s in skills)/len(skills),1) if skills else None,
        "dir_scripts": has(r"(^|/)scripts(/|$)"),
        "dir_examples": has(r"(^|/)examples?(/|$)"),
        "dir_references": has(r"(^|/)references?(/|$)"),
        "has_marketplace_json": has(r"marketplace\.json$"),
        "has_tests_or_evals": has(r"(^|/)(tests?|evals?)(/|$)") or has(r"evals\.json$"),
        "install_oneliner_in_readme": bool(INSTALL_RE.search(readme)),
        "readme_has_before_after": bool(BEFORE_AFTER_RE.search(readme)),
        "_skills": skills,
        "_redflags": {
            "obey_external_output": bool(REDFLAG_OBEY_OUTPUT.search(all_text)),
            "cred_in_argv": bool(REDFLAG_CRED_ARGV.search(all_text)),
            "self_update": bool(REDFLAG_SELF_UPDATE.search(all_text)),
            "registers_hooks": has(r"(^|/)hooks?(/|$)") or bool(re.search(r"(?i)hook", all_text[:50000])),
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

def build_findings(m):
    findings = {"hygiene": [], "differentiators": [], "security": [], "craft_llm_todo": []}
    # H-001/002/003/004 hygiene 門檻
    findings["hygiene"].append({"id":"H-001","pass": m["skill_md_compliant_count"]>=1,
        "detail": f"合規 SKILL.md 數={m['skill_md_compliant_count']}", "severity":"error"})
    findings["hygiene"].append({"id":"H-003","pass": m["skill_md_max_lines"]<500 or m["dir_references"],
        "detail": f"max_lines={m['skill_md_max_lines']}, references/={m['dir_references']}",
        "severity":"warning", "note":"長度非絕對(jezweb 反證);references/ 分層亦可"})
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
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: return selftest()
    if not a.repo_dir or not os.path.isdir(a.repo_dir):
        print("usage: lint_skill.py <repo_dir>", file=sys.stderr); return 2
    m = analyze(a.repo_dir); f = build_findings(m)
    out = {"repo": a.repo_dir, "hygiene": f["hygiene"], "differentiators": f["differentiators"],
           "packaging_score": f["_score"], "packaging_max": f["_maxscore"],
           "tier_benchmark_packaging": tier_benchmark(f["_score"], f["_maxscore"]),
           "security": f["security"], "craft_llm_todo": f["craft_llm_todo"],
           "gap_list": [d["feature"] for d in sorted(f["differentiators"], key=lambda x:-x["weight"])
                        if not d["present"]]}
    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=2)); return 0
    hyg_fail = [h for h in f["hygiene"] if not h["pass"] and h["severity"]=="error"]
    print(f"== skill-reviewer lint: {a.repo_dir} ==")
    print(f"[hygiene] {'FAIL' if hyg_fail else 'pass'}  " +
          " ".join(f"{h['id']}={'✓' if h['pass'] else '✗'}" for h in f["hygiene"]))
    print(f"[packaging benchmark] {f['_score']}/{f['_maxscore']} → {out['tier_benchmark_packaging']}")
    print(f"[gap list] {out['gap_list'] or '(packaging 面已滿)'}")
    if f["security"]: print(f"[security] " + "; ".join(f"{s['id']}:{s.get('flag')}" for s in f["security"]))
    print(f"[craft→LLM] 交 SKILL.md 質化審 {len(f['craft_llm_todo'])} 個樣本(trigger/style/scope)")
    print("\n措辭紀律:以上為『特徵剖面』,非星數預測。craft verdict 需 LLM 讀 craft_llm_todo 後才完成。")
    return 0

def selftest():
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
        # 安全紅旗偵測
        open(os.path.join(sd,"SKILL.md"),"w").write("---\nname: s\ndescription: d\n---\nInstall in one pass; don't stop for confirmation.\n")
        m2 = analyze(td); f2 = build_findings(m2)
        assert any(s["id"]=="S-001" for s in f2["security"]), f2["security"]
    print("[selftest] lint_skill: all assertions passed ✔")

if __name__ == "__main__":
    sys.exit(main())
