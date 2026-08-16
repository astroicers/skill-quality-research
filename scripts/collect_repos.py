#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 1 — 資料收集 (BRIEF §3 Phase 1, §6.5, §7)
產出: research/repos.json + research/G1-summary.md → 停在 Gate G1

用法:
  export GITHUB_TOKEN=ghp_xxx          # 或 gh auth login (腳本會自動抓 gh auth token)
  python3 scripts/collect_repos.py
  python3 scripts/collect_repos.py --offline   # 只用 seeds 建 repos.json(pipeline 測試用,無 API)
  python3 scripts/collect_repos.py --selftest  # 純函式自我測試(tier/cohort/fame/抽樣)

設計原則 (BRIEF Iron Rules):
  - deterministic 部分全部腳本化;taxonomy/domain 最終標籤留給 G1 人工確認(腳本只給 suggest)
  - API 紀律: 必須有 token;search 間隔 2.2s;印出 rate-limit 餘額
  - 所有啟發式(taxonomy_suggest 等)都是 G1 審查對象,不是結論
"""
import argparse, json, math, os, re, subprocess, sys, time, urllib.parse, urllib.request
from datetime import datetime, timezone

API = "https://api.github.com"
UA = "skill-quality-research/1.2.1"

# BRIEF §3 Phase 1 的六組查詢
QUERIES = [
    "topic:claude-skills",
    "topic:claude-code-skills",
    "topic:agent-skills",
    "topic:claude-code-plugins",
    '"claude skills" in:name,description',
    '"agent skills" in:name,description',
]
# BRIEF §3 Phase 1: T1/T0 區間抽樣(一半 sort=stars 一半 sort=updated)
RANGE_SAMPLES = [
    ("T1", "stars:1000..9999", 12),
    ("T0", "stars:100..999", 10),
]
# BRIEF §6.5 純度標籤
COHORT_CUTS = [("2025-10-01", "C0"), ("2026-02-01", "C1"), ("2026-06-01", "C2")]  # created_at < cut
DOMAIN_VOCAB = ["dev-workflow", "code-quality", "design-ui", "writing-content", "memory-context",
                "research-analysis", "security", "science", "media-gen", "meta-tooling"]
DOMAIN_HINTS = [
    (r"security|pentest|ctf|threat|vuln", "security"),
    (r"design|ui|ux|frontend|css|figma", "design-ui"),
    (r"memory|context|session|persist", "memory-context"),
    (r"research|paper|analy[sz]e|knowledge graph", "research-analysis"),
    (r"scien|biology|chemistry|physics|lab", "science"),
    (r"writ|blog|content|translat|marketing copy", "writing-content"),
    (r"video|image|audio|media|remotion", "media-gen"),
    (r"marketplace|registry|catalog|harness|control plane|skill librar", "meta-tooling"),
    (r"review|lint|test|tdd|quality", "code-quality"),
]
TAXO_E_RE = re.compile(r"(?i)\bawesome\b|curated (list|collection)|directory of|catalog of")


# ---------------- 純函式(--selftest 覆蓋) ----------------
def assign_tier(stars):
    if stars is None: return None
    if stars >= 100_000: return "T3"
    if stars >= 10_000: return "T2"
    if stars >= 1_000: return "T1"
    if stars >= 100: return "T0"
    return None  # 低於樣本地板

def assign_cohort(created_at_iso):
    if not created_at_iso: return None
    d = created_at_iso[:10]
    for cut, label in COHORT_CUTS:
        if d < cut: return label
    return "C3"

def fame_tier(followers):
    if followers is None: return None
    if followers < 1_000: return "F0"
    if followers < 10_000: return "F1"
    return "F2"

def stars_per_month(stars, created_at_iso, now=None):
    if not created_at_iso or stars is None: return None
    now = now or datetime.now(timezone.utc)
    created = datetime.fromisoformat(created_at_iso.replace("Z", "+00:00"))
    months = max((now - created).days / 30.44, 0.5)
    return round(stars / months, 1)

def interleave_sample(stars_sorted, updated_sorted, n, exclude):
    """T0/T1 抽樣: 一半取星數排序、一半取更新排序,去重、排除既有,方法可重現 (BRIEF Phase 1)。
    跳過重複/排除項時不消耗該來源的輪次,維持兩來源各半的語意。"""
    out, seen = [], set(exclude)
    a, b = list(stars_sorted), list(updated_sorted)
    take_a = True
    while len(out) < n and (a or b):
        src = a if (take_a and a) or not b else b
        item = src.pop(0)
        if item["full_name"] not in seen:
            seen.add(item["full_name"]); out.append(item)
            take_a = not take_a  # 只有實際取到才換邊
    return out

def taxonomy_suggest(name, desc):
    text = f"{name} {desc or ''}"
    if TAXO_E_RE.search(text): return "E?"
    return "TBD"  # A–D vs F 需看 repo 內容(Phase 2/3 的 skill_md_count 才能判)

def domain_suggest(name, desc):
    text = f"{name} {desc or ''}".lower()
    for pat, dom in DOMAIN_HINTS:
        if re.search(pat, text): return dom
    return "TBD"


# ---------------- GitHub API ----------------
def get_token():
    tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if tok: return tok.strip()
    try:
        r = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, timeout=10)
        if r.returncode == 0 and r.stdout.strip(): return r.stdout.strip()
    except Exception:
        pass
    return None

def gh_get(path, token, params=None):
    url = API + path + (("?" + urllib.parse.urlencode(params)) if params else "")
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": UA,
        **({"Authorization": f"Bearer {token}"} if token else {}),
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            remaining = resp.headers.get("X-RateLimit-Remaining")
            return json.load(resp), remaining, dict(resp.headers)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")[:200]
        raise RuntimeError(f"GitHub API {e.code} on {path}: {body}") from None

def search_repos(q, token, sort="stars", pages=2, per_page=50):
    items = []
    for p in range(1, pages + 1):
        data, remaining, _ = gh_get("/search/repositories", token,
                                    {"q": q, "sort": sort, "order": "desc",
                                     "per_page": per_page, "page": p})
        items += data.get("items", [])
        print(f"  [search] q={q!r} sort={sort} page={p} got={len(data.get('items', []))} rate_remaining={remaining}")
        if len(data.get("items", [])) < per_page: break
        time.sleep(2.2)  # search 30/min 紀律
    time.sleep(2.2)
    return items

def contributor_count(full_name, token):
    """Link header 的 last page 技巧: per_page=1 時 last page 數 = 貢獻者數。"""
    try:
        data, _, headers = gh_get(f"/repos/{full_name}/contributors", token,
                                  {"per_page": 1, "anon": "true"})
        link = headers.get("Link", "")
        m = re.search(r'[?&]page=(\d+)>; rel="last"', link)
        if m: return int(m.group(1))
        return len(data) if isinstance(data, list) else None
    except Exception as e:
        print(f"  [warn] contributors {full_name}: {e}"); return None

def nonauthor_pr_count(full_name, token):
    """非作者 PR 數(engagement 訊號)。org repo 對成員 PR 為近似值,已記為已知限制。"""
    owner = full_name.split("/")[0]
    try:
        data, _, _ = gh_get("/search/issues", token,
                            {"q": f"repo:{full_name} type:pr -author:{owner}", "per_page": 1})
        time.sleep(2.2)
        return data.get("total_count")
    except Exception as e:
        print(f"  [warn] nonauthor_pr {full_name}: {e}"); return None

def author_profile(login, token, cache):
    if login in cache: return cache[login]
    followers, created = None, None
    try:
        u, _, _ = gh_get(f"/users/{login}", token)
        followers, created = u.get("followers"), u.get("created_at")
    except Exception as e:
        print(f"  [warn] user {login}: {e}")
    cache[login] = {"followers": followers, "user_created_at": created}
    return cache[login]

def prior_fame(login, repo_created_at, token, cache):
    """作者在本 repo 建立前的最高星 repo(反向因果防護, BRIEF §6.5)。"""
    key = (login, repo_created_at[:10] if repo_created_at else "")
    if key in cache: return cache[key]
    val = 0
    try:
        q = f"user:{login} created:<{repo_created_at[:10]}"
        data, _, _ = gh_get("/search/repositories", token,
                            {"q": q, "sort": "stars", "order": "desc", "per_page": 1})
        time.sleep(2.2)
        items = data.get("items", [])
        val = items[0]["stargazers_count"] if items else 0
    except Exception as e:
        print(f"  [warn] prior_fame {login}: {e}"); val = None
    cache[key] = val
    return val


# ---------------- record 組裝 ----------------
def base_record(item):
    lic = (item.get("license") or {}).get("spdx_id")
    return {
        "full_name": item["full_name"],
        "stars": item.get("stargazers_count"),
        "forks": item.get("forks_count"),
        "created_at": item.get("created_at"),
        "pushed_at": item.get("pushed_at"),
        "topics": item.get("topics", []),
        "license": lic,
        "description": (item.get("description") or "")[:300],
        "repo_size_kb": item.get("size"),
        "archived": item.get("archived", False),
    }

def enrich(rec, seeds_by_name):
    seed = seeds_by_name.get(rec["full_name"], {})
    rec["taxonomy"] = seed.get("taxonomy_code") or taxonomy_suggest(rec["full_name"], rec.get("description"))
    rec["taxonomy_source"] = "seed" if seed.get("taxonomy_code") else "heuristic-needs-G1"
    rec["domain"] = seed.get("domain_suggest") or domain_suggest(rec["full_name"], rec.get("description"))
    rec["domain_source"] = "seed-suggest" if seed.get("domain_suggest") else "heuristic-needs-G1"
    rec["in_rubric_sample"] = seed.get("in_rubric_sample", rec["taxonomy"] in ("A", "B", "C", "D", "TBD"))
    rec["seed_note"] = seed.get("note")
    rec["star_tier"] = assign_tier(rec.get("stars"))
    rec["launch_cohort"] = assign_cohort(rec.get("created_at"))
    rec["stars_per_month"] = stars_per_month(rec.get("stars"), rec.get("created_at"))
    if rec.get("created_at"):
        created = datetime.fromisoformat(rec["created_at"].replace("Z", "+00:00"))
        rec["days_since_creation"] = (datetime.now(timezone.utc) - created).days
    if rec.get("stars") and rec.get("forks") is not None:
        rec["fork_star_ratio"] = round(rec["forks"] / max(rec["stars"], 1), 4)
    return rec


def write_outputs(records, sampling_log, outdir, offline):
    records.sort(key=lambda r: -(r.get("stars") or 0))
    purity = [r["full_name"] for r in records
              if r.get("author_fame_tier") == "F0" and r.get("star_tier") in ("T2", "T3")
              and r.get("in_rubric_sample")]
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": "offline-seeds-only" if offline else "api",
        "brief_version": "v1.2.1",
        "sampling_log": sampling_log,
        "purity_sample": purity,
        "records": records,
    }
    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, "repos.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    # G1 摘要
    def count(key):
        c = {}
        for r in records: c[r.get(key)] = c.get(r.get(key), 0) + 1
        return dict(sorted(c.items(), key=lambda kv: str(kv[0])))
    tbd = [r["full_name"] for r in records if "TBD" in (str(r.get("taxonomy")), str(r.get("domain")))
           or str(r.get("taxonomy")).endswith("?")]
    lines = [
        "# G1 Review Summary(Gate G1 — 人工審查用)", "",
        f"- 產生時間:{payload['generated_at']}  mode:{payload['mode']}",
        f"- 總 repo 數:{len(records)};rubric 樣本(A–D):{sum(1 for r in records if r.get('in_rubric_sample'))}",
        f"- tier 分布:{count('star_tier')}",
        f"- cohort 分布:{count('launch_cohort')}(切點為提案值,請對照 created_at 分布確認)",
        f"- fame 分布:{count('author_fame_tier')}",
        f"- taxonomy 分布:{count('taxonomy')}",
        f"- domain 分布:{count('domain')}",
        f"- 純度樣本(F0 且 T2+):{len(purity)} 個 → {purity}", "",
        "## 待人工定案(TBD / 啟發式標籤)",
        *([f"- {n}" for n in tbd] if tbd else ["- 無"]),
        "",
        "## 抽樣方法記錄", "```json", json.dumps(sampling_log, ensure_ascii=False, indent=2), "```", "",
        "## G1 檢查清單(BRIEF §3)",
        "- [ ] 清單完整性(重要 repo 未遺漏;superpowers 現址已確認)",
        "- [ ] taxonomy 分類正確(尤其 E/F 排除是否合理)",
        "- [ ] 純度標籤 domain / fame / cohort 標注正確",
        "- [ ] 四層抽樣分布合理(T0/T1 不可全是同類同域)",
        "- [ ] verdict:approved / rejected(附修改指示)",
    ]
    with open(os.path.join(outdir, "G1-summary.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"[ok] wrote {out} 與 G1-summary.md;共 {len(records)} repos,純度樣本 {len(purity)}")


# ---------------- 主流程 ----------------
def run_offline(seeds, outdir):
    print("[mode] offline:只用 seeds 建 repos.json(cohort/fame 等 API 欄位為 null,供 pipeline 測試)")
    records = []
    for s in seeds["records"]:
        rec = {"full_name": s["full_name"], "stars": s["stars_snapshot"], "forks": None,
               "created_at": None, "pushed_at": None, "topics": [], "license": None,
               "description": s.get("note", ""), "repo_size_kb": None, "archived": False}
        records.append(enrich(rec, {s["full_name"]: s}))
    write_outputs(records, {"mode": "offline", "queries": [], "range_samples": []}, outdir, offline=True)

def run_api(seeds, outdir, args):
    token = get_token()
    if not token:
        sys.exit("[fatal] 需要 GITHUB_TOKEN 或 gh auth login(BRIEF Iron Rule 6:未認證配額 60/hr 不可行)。"
                 "pipeline 測試請改用 --offline。")
    seeds_by_name = {s["full_name"]: s for s in seeds["records"]}
    merged = {}

    # 1) 六組主查詢
    for q in QUERIES:
        for item in search_repos(q, token, sort="stars", pages=args.pages):
            merged.setdefault(item["full_name"], base_record(item))

    # 2) 種子刷新(含 superpowers 追址提醒)
    for s in seeds["records"]:
        fn = s["full_name"]
        if fn in merged: continue
        try:
            item, _, _ = gh_get(f"/repos/{fn}", token)
            merged[fn] = base_record(item)
        except Exception as e:
            print(f"  [warn] seed {fn} 無法刷新({e});保留快照值" +
                  (" ← needs_relocation,G1 請確認現址" if s.get("needs_relocation") else ""))
            merged[fn] = {"full_name": fn, "stars": s["stars_snapshot"], "forks": None,
                          "created_at": None, "pushed_at": None, "topics": [], "license": None,
                          "description": s.get("note", ""), "repo_size_kb": None,
                          "archived": False, "stale_snapshot": True}

    # 3) T1/T0 區間抽樣(一半 stars 一半 updated)
    sampling_log = {"queries": QUERIES, "pages": args.pages, "range_samples": []}
    existing = set(merged.keys())
    for tier_label, star_range, n in RANGE_SAMPLES:
        base_q = f"topic:claude-skills {star_range}"
        by_stars = [base_record(i) for i in search_repos(base_q, token, sort="stars", pages=1)]
        by_updated = [base_record(i) for i in search_repos(base_q, token, sort="updated", pages=1)]
        picked = interleave_sample(by_stars, by_updated, n, existing)
        for rec in picked:
            merged[rec["full_name"]] = rec
            existing.add(rec["full_name"])
        sampling_log["range_samples"].append(
            {"tier": tier_label, "query": base_q, "n_target": n, "picked": [r["full_name"] for r in picked],
             "method": "interleave(stars-sorted, updated-sorted), dedup, deterministic"})

    # 4) tier 地板過濾 + enrich
    records = []
    for rec in merged.values():
        r = enrich(rec, seeds_by_name)
        if r["star_tier"] is None and not r.get("seed_note"):
            continue  # <100 星且非種子 → 丟棄
        records.append(r)

    # 5) 混淆因子與 engagement 欄位(只對 rubric 樣本打 API,省配額)
    ucache, pcache = {}, {}
    for r in records:
        if not r.get("in_rubric_sample"): continue
        login = r["full_name"].split("/")[0]
        prof = author_profile(login, token, ucache)
        r["author_followers"] = prof["followers"]
        r["author_fame_tier"] = fame_tier(prof["followers"])
        if r.get("created_at"):
            r["prior_fame_proxy"] = prior_fame(login, r["created_at"], token, pcache)
            # prior_fame 為主判據:既有 ≥10k 星 repo 視為 F2、≥1k 視為至少 F1(BRIEF §6.5)
            pf = r.get("prior_fame_proxy") or 0
            if pf >= 10_000: r["author_fame_tier"] = "F2"
            elif pf >= 1_000 and r["author_fame_tier"] == "F0": r["author_fame_tier"] = "F1"
        if not args.skip_engagement:
            r["contributor_count"] = contributor_count(r["full_name"], token)
            r["nonauthor_pr_count"] = nonauthor_pr_count(r["full_name"], token)

    write_outputs(records, sampling_log, outdir, offline=False)


def selftest():
    assert assign_tier(240_338) == "T3" and assign_tier(99_999) == "T2"
    assert assign_tier(10_000) == "T2" and assign_tier(9_999) == "T1"
    assert assign_tier(1_000) == "T1" and assign_tier(999) == "T0"
    assert assign_tier(100) == "T0" and assign_tier(99) is None
    assert assign_cohort("2025-09-30T00:00:00Z") == "C0"
    assert assign_cohort("2025-10-01T00:00:00Z") == "C1"
    assert assign_cohort("2026-03-15T00:00:00Z") == "C2"
    assert assign_cohort("2026-07-01T00:00:00Z") == "C3"
    assert fame_tier(999) == "F0" and fame_tier(1_000) == "F1" and fame_tier(10_000) == "F2"
    spm = stars_per_month(3000, "2026-05-16T00:00:00Z",
                          now=datetime(2026, 8, 16, tzinfo=timezone.utc))
    assert 950 < spm < 1050, spm
    a = [{"full_name": f"a{i}"} for i in range(5)]
    b = [{"full_name": f"b{i}"} for i in range(5)] + [{"full_name": "a0"}]
    got = [x["full_name"] for x in interleave_sample(a, b, 4, exclude={"a1"})]
    assert got == ["a0", "b0", "a2", "b1"], got
    assert taxonomy_suggest("x/awesome-claude-skills", "A curated list") == "E?"
    assert domain_suggest("x/ctf-skills", "pentest stuff") == "security"
    print("[selftest] collect_repos: all assertions passed ✔")


def main():
    ap = argparse.ArgumentParser(description="Phase 1 資料收集")
    ap.add_argument("--out", default="research")
    ap.add_argument("--seeds", default="seeds/seed_repos.json")
    ap.add_argument("--pages", type=int, default=2, help="每組主查詢抓幾頁(50/頁)")
    ap.add_argument("--offline", action="store_true", help="只用 seeds,無 API(pipeline 測試)")
    ap.add_argument("--skip-engagement", action="store_true", help="跳過 contributors / nonauthor PR(省配額)")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest: return selftest()
    with open(args.seeds, encoding="utf-8") as f:
        seeds = json.load(f)
    if args.offline: return run_offline(seeds, args.out)
    return run_api(seeds, args.out, args)

if __name__ == "__main__":
    main()
