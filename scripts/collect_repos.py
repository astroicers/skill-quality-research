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
import argparse, json, math, os, re, subprocess, sys, time, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timezone

API = "https://api.github.com"
UA = "skill-quality-research/1.2.1"
SEARCH_INTERVAL = 3.0   # search 主限額 30/min = 2s;實測 2.2s 仍會撞二級限額,故放寬

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
# BRIEF §3 Phase 1 分層抽樣名額:T3 全收 / T2 全收 / T1 抽 10–12 / T0 抽 15–20(G1 裁決 5)。
# None = 全收。主查詢會把整片 T1/T0 掃進來,必須靠這組名額收斂回 spec 設計。
STRATA_CAPS = {"T3": None, "T2": None, "T1": 12, "T0": 18}
# BRIEF §6.5 純度標籤;C1/C2 切點 2026-01(G1 裁決 3:對照 created_at 直方圖定稿)
COHORT_CUTS = [("2025-10-01", "C0"), ("2026-01-01", "C1"), ("2026-06-01", "C2")]  # created_at < cut
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

class GHError(RuntimeError):
    """帶 status code 與 headers 的 API 錯誤,供退避策略與失敗歸因使用。"""
    def __init__(self, code, path, body, headers=None):
        super().__init__(f"GitHub API {code} on {path}: {body}")
        self.code, self.path, self.body = code, path, body
        self.headers = dict(headers or {})

    @property
    def is_secondary(self):
        return self.code in (403, 429) and "secondary rate limit" in self.body.lower()

    @property
    def is_transient(self):
        return self.is_secondary or self.code in (429, 500, 502, 503, 504)

    @property
    def kind(self):
        """失敗歸因標籤,寫進 data_quality 供 G1 判讀。"""
        if self.is_secondary: return "secondary-rate-limit"
        if self.code == 0:    return "network"
        if self.code == 422:  return "not-searchable"   # 帳號已刪除/改名
        if self.code == 404:  return "not-found"
        if self.code == 403:  return "forbidden"
        return f"http-{self.code}"


def backoff_seconds(headers, attempt):
    """GitHub 官方退避建議:Retry-After 優先;其次 x-ratelimit-reset;
    都沒有則指數退避,二級限額至少等 60s。"""
    h = {k.lower(): v for k, v in (headers or {}).items()}
    ra = h.get("retry-after")
    if ra:
        try: return max(1, int(float(ra)))
        except (TypeError, ValueError): pass
    if str(h.get("x-ratelimit-remaining", "")) == "0":
        try:
            wait = int(h["x-ratelimit-reset"]) - int(time.time())
            if 0 < wait <= 900: return wait + 2
        except (KeyError, TypeError, ValueError): pass
    return min(600, 60 * (2 ** attempt))


def gh_get(path, token, params=None, retries=4):
    url = API + path + (("?" + urllib.parse.urlencode(params)) if params else "")
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": UA,
        **({"Authorization": f"Bearer {token}"} if token else {}),
    })
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                remaining = resp.headers.get("X-RateLimit-Remaining")
                return json.load(resp), remaining, dict(resp.headers)
        except urllib.error.HTTPError as e:   # HTTPError 是 URLError 子類,必須先接
            err = GHError(e.code, path, e.read().decode("utf-8", "replace")[:300], e.headers)
            if attempt < retries and err.is_transient:
                wait = backoff_seconds(err.headers, attempt)
                print(f"  [backoff] {err.kind} on {path} → 等 {wait}s(重試 {attempt + 1}/{retries})", flush=True)
                time.sleep(wait); continue
            raise err from None
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt < retries:
                wait = min(120, 5 * (2 ** attempt))
                print(f"  [backoff] network {e} on {path} → 等 {wait}s(重試 {attempt + 1}/{retries})", flush=True)
                time.sleep(wait); continue
            raise GHError(0, path, f"network: {e}") from None


class FieldStats:
    """逐欄成功/失敗計數 — 讓靜默的 None 在 G1 摘要裡現形(BRIEF §4 工序 2 的前提)。"""
    def __init__(self): self.ok, self.fail = 0, {}
    def hit(self): self.ok += 1
    def miss(self, kind): self.fail[kind] = self.fail.get(kind, 0) + 1
    def summary(self):
        failed = sum(self.fail.values())
        total = self.ok + failed
        return {"ok": self.ok, "failed": failed, "total": total,
                "ok_pct": round(100 * self.ok / total, 1) if total else None,
                "failure_kinds": dict(sorted(self.fail.items()))}


def search_repos(q, token, sort="stars", pages=2, per_page=50):
    items = []
    for p in range(1, pages + 1):
        data, remaining, _ = gh_get("/search/repositories", token,
                                    {"q": q, "sort": sort, "order": "desc",
                                     "per_page": per_page, "page": p})
        items += data.get("items", [])
        print(f"  [search] q={q!r} sort={sort} page={p} got={len(data.get('items', []))} rate_remaining={remaining}")
        if len(data.get("items", [])) < per_page: break
        time.sleep(SEARCH_INTERVAL)
    time.sleep(SEARCH_INTERVAL)
    return items

def _fail(stats, label, name, e):
    kind = e.kind if isinstance(e, GHError) else "other"
    print(f"  [warn] {label} {name}: {kind}", flush=True)
    if stats: stats.miss(kind)
    return None

def contributor_count(full_name, token, stats=None):
    """Link header 的 last page 技巧: per_page=1 時 last page 數 = 貢獻者數。"""
    try:
        data, _, headers = gh_get(f"/repos/{full_name}/contributors", token,
                                  {"per_page": 1, "anon": "true"})
        link = headers.get("Link", "")
        m = re.search(r'[?&]page=(\d+)>; rel="last"', link)
        val = int(m.group(1)) if m else (len(data) if isinstance(data, list) else None)
        if stats: stats.hit()
        return val
    except Exception as e:
        return _fail(stats, "contributors", full_name, e)

def nonauthor_pr_count(full_name, token, stats=None):
    """非作者 PR 數(engagement 訊號)。org repo 對成員 PR 為近似值,已記為已知限制。"""
    owner = full_name.split("/")[0]
    try:
        data, _, _ = gh_get("/search/issues", token,
                            {"q": f"repo:{full_name} type:pr -author:{owner}", "per_page": 1})
        time.sleep(SEARCH_INTERVAL)
        if stats: stats.hit()
        return data.get("total_count")
    except Exception as e:
        return _fail(stats, "nonauthor_pr", full_name, e)

def author_profile(login, token, cache, stats=None):
    if login in cache: return cache[login]
    followers, created = None, None
    try:
        u, _, _ = gh_get(f"/users/{login}", token)
        followers, created = u.get("followers"), u.get("created_at")
        if stats: stats.hit()
    except Exception as e:
        _fail(stats, "user", login, e)
    cache[login] = {"followers": followers, "user_created_at": created}
    return cache[login]

def prior_fame(login, repo_created_at, token, cache, stats=None):
    """作者在本 repo 建立前的最高星 repo(反向因果防護, BRIEF §6.5)。"""
    key = (login, repo_created_at[:10] if repo_created_at else "")
    if key in cache: return cache[key]
    try:
        q = f"user:{login} created:<{repo_created_at[:10]}"
        data, _, _ = gh_get("/search/repositories", token,
                            {"q": q, "sort": "stars", "order": "desc", "per_page": 1})
        time.sleep(SEARCH_INTERVAL)
        items = data.get("items", [])
        val = items[0]["stargazers_count"] if items else 0
        if stats: stats.hit()
    except Exception as e:
        val = _fail(stats, "prior_fame", login, e)
    cache[key] = val
    return val


# ---------------- 分層名額 / 快取 ----------------
def apply_strata_caps(records, caps, sampling_log):
    """BRIEF §3 分層抽樣落地:T3/T2 全收,T1/T0 依名額收斂。

    主查詢會把整片 T1/T0 掃進來(每組查詢每頁 50 筆、共 16 組),若不收斂,
    樣本數會是 BRIEF Phase 2 預估(35–45)的數倍,且 enrichment 呼叫量等比放大。
    保留優先序:種子 > range 抽樣 > 主查詢(星數高者優先),使結果可重現。

    ⚠ 已知限制(code-review F3,2026-08-16):cap 目前只依 star_tier,不排除 Phase 1 已可判定
    為非 rubric 的 repo(taxonomy_suggest 標到的 E/E? awesome list)。高星 E/E? 會佔掉 T1/T0 配額,
    擠掉低星 TBD 候選,使實際 rubric 樣本略小於 BRIEF §3(本次 T0 約 4 位、T1 約 2 位被 E/E? 佔)。
    註:F 類不在此列——F 是 Phase 2 clone 後才回填,Phase 1 時仍為合法 TBD 候選。
    TODO(下輪重跑時生效,不回溯動 G1 approved 樣本):cap 計數前先濾掉 taxonomy in {E,E?} 者
    (仍保留 TBD 候選),即 `if str(r.get("taxonomy")) in ("E","E?"): 直接 kept 但不佔 cap`。
    """
    def prio(r):
        if r.get("seed_note"): return 0
        if r.get("sampled_via") == "range": return 1
        return 2

    kept, counts, dropped = [], {}, {}
    for r in sorted(records, key=lambda x: (prio(x), -(x.get("stars") or 0), x["full_name"])):
        tier = r.get("star_tier")
        cap = caps.get(tier)
        n = counts.get(tier, 0)
        if cap is None or n < cap:
            counts[tier] = n + 1
            kept.append(r)
        else:
            dropped.setdefault(tier, []).append(r["full_name"])

    sampling_log["strata_caps"] = {
        "applied": True,
        "brief_ref": "BRIEF §3 Phase 1(G1 修訂):T3 全收 / T2 全收 / T1 抽 10–12 / T0 抽 15–20",
        "caps": {k: ("全收" if v is None else v) for k, v in caps.items()},
        "priority": "seed > range-sample > main-query(stars desc)",
        "kept_per_tier": dict(sorted(counts.items(), key=lambda kv: str(kv[0]))),
        "dropped_per_tier": {k: len(v) for k, v in sorted(dropped.items(), key=lambda kv: str(kv[0]))},
        "dropped_names": {k: sorted(v) for k, v in sorted(dropped.items(), key=lambda kv: str(kv[0]))},
    }
    kept.sort(key=lambda r: -(r.get("stars") or 0))
    return kept


def load_cache(path, refresh=False):
    if refresh or not os.path.exists(path): return {}
    try:
        with open(path, encoding="utf-8") as f: return json.load(f)
    except Exception as e:
        print(f"  [warn] 快取讀取失敗({e}),改為全新抓取"); return {}

def save_cache(path, cache):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=1)
    os.replace(tmp, path)   # atomic:中斷時不會留下半截檔

def cached(entry, key, fetch):
    """成功值入快取;失敗(None)不入,下次重跑會自動重試該欄。"""
    if key in entry: return entry[key]
    val = fetch()
    if val is not None: entry[key] = val
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
        "open_issues": item.get("open_issues_count"),          # G2 Q2(issues+PRs 合計,近似值 #8)
        "owner_is_org": (item.get("owner") or {}).get("type") == "Organization",  # G2 Q5
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


def coverage(records, field):
    """欄位實際落地率 — 快取命中的值不經 FieldStats,故以成品再算一次。"""
    total = sum(1 for r in records if r.get("in_rubric_sample"))
    have = sum(1 for r in records if r.get("in_rubric_sample") and r.get(field) is not None)
    return {"have": have, "total": total, "pct": round(100 * have / total, 1) if total else None}


def write_outputs(records, sampling_log, outdir, offline, data_quality=None):
    records.sort(key=lambda r: -(r.get("stars") or 0))
    purity = [r["full_name"] for r in records
              if r.get("author_fame_tier") == "F0" and r.get("star_tier") in ("T2", "T3")
              and r.get("in_rubric_sample")]
    dq = {
        "fetch_stats": data_quality or {},
        "field_coverage": {f: coverage(records, f) for f in
                           ("author_followers", "prior_fame_proxy", "author_fame_tier",
                            "contributor_count", "nonauthor_pr_count", "fork_star_ratio")},
    }
    # BRIEF §4 去混淆三道工序的資料前提是否成立
    cov = dq["field_coverage"]
    def pct(f): return cov[f]["pct"] if cov[f]["pct"] is not None else 0
    dq["deconfound_readiness"] = {
        "工序1_素人復現": {"needs": "author_fame_tier", "coverage_pct": pct("author_fame_tier"),
                            "ok": pct("author_fame_tier") >= 80, "purity_sample_n": len(purity)},
        "工序2_雙結果變數": {"needs": "fork_star_ratio + contributor_count + nonauthor_pr_count",
                             "coverage_pct": min(pct("fork_star_ratio"), pct("contributor_count"),
                                                 pct("nonauthor_pr_count")),
                             "ok": min(pct("fork_star_ratio"), pct("contributor_count"),
                                       pct("nonauthor_pr_count")) >= 80},
        "工序3_機制陳述": {"needs": "LLM 判讀,無資料依賴", "ok": True},
    }
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": "offline-seeds-only" if offline else "api",
        "brief_version": "v1.2.1",
        "sampling_log": sampling_log,
        "data_quality": dq,
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
        "## 資料完整度(BRIEF §4 去混淆三道工序的前提)", "",
        "| 欄位 | 落地率 | 抓取失敗原因 |",
        "|------|--------|--------------|",
        *[f"| `{f}` | {c['have']}/{c['total']}"
          + (f" ({c['pct']}%)" if c["pct"] is not None else "")
          + " | "
          + (", ".join(f"{k}×{v}" for k, v in
                       (dq["fetch_stats"].get(f, {}).get("failure_kinds") or {}).items()) or "—")
          + " |"
          for f, c in dq["field_coverage"].items()],
        "",
        *[f"- {'✅' if v.get('ok') else '❌'} **{k}** — 需要 {v['needs']}"
          + (f";覆蓋率 {v['coverage_pct']}%" if "coverage_pct" in v else "")
          + (f";純度樣本 {v['purity_sample_n']} 個" if "purity_sample_n" in v else "")
          for k, v in dq["deconfound_readiness"].items()],
        "",
        *(["> ⚠️ **有工序未達 80% 覆蓋率**:相關 differentiator 的 `evidence_strength` "
           "依 BRIEF §4 只能標到 `weak`。重跑 `collect_repos.py` 會自動只補失敗欄位(成功值已快取)。", ""]
          if not all(v.get("ok") for v in dq["deconfound_readiness"].values()) else []),
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
    sampling_log = {"queries": QUERIES, "pages": args.pages, "range_samples": [],
                    "search_interval_sec": SEARCH_INTERVAL}
    existing = set(merged.keys())
    for tier_label, star_range, n in RANGE_SAMPLES:
        base_q = f"topic:claude-skills {star_range}"
        by_stars = [base_record(i) for i in search_repos(base_q, token, sort="stars", pages=1)]
        by_updated = [base_record(i) for i in search_repos(base_q, token, sort="updated", pages=1)]
        picked = interleave_sample(by_stars, by_updated, n, existing)
        for rec in picked:
            rec["sampled_via"] = "range"
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

    # 4b) 分層名額(BRIEF §3):把主查詢掃進來的整片 T1/T0 收斂回 spec 設計
    caps = dict(STRATA_CAPS)
    for tier, val in (("T3", args.cap_t3), ("T2", args.cap_t2), ("T1", args.cap_t1), ("T0", args.cap_t0)):
        if val is not None: caps[tier] = (None if val <= 0 else val)   # <=0 表示全收
    if args.strict_strata:
        before = len(records)
        records = apply_strata_caps(records, caps, sampling_log)
        print(f"[strata] {before} → {len(records)} repos;名額 {sampling_log['strata_caps']['caps']};"
              f"各層保留 {sampling_log['strata_caps']['kept_per_tier']}")
    else:
        sampling_log["strata_caps"] = {"applied": False,
                                       "note": "--no-strict-strata:T1/T0 全收,偏離 BRIEF §3 抽樣設計"}
        print(f"[strata] 未套用名額(--no-strict-strata),共 {len(records)} repos")

    if args.probe:
        return write_probe(records, sampling_log, outdir)

    # 5) 混淆因子與 engagement 欄位(只對 rubric 樣本打 API,省配額)
    #    逐筆寫快取:中斷後重跑只補未取得的欄位,不重打已成功的 API。
    cache_path = os.path.join(outdir, ".enrich-cache.json")
    cache = load_cache(cache_path, args.refresh_cache)
    stats = {f: FieldStats() for f in ("author_followers", "prior_fame_proxy",
                                       "contributor_count", "nonauthor_pr_count")}
    ucache, pcache = {}, {}
    targets = [r for r in records if r.get("in_rubric_sample")]
    hits = sum(1 for r in targets if r["full_name"] in cache)
    est = (len(targets) - hits) * (2 if not args.skip_engagement else 1) * SEARCH_INTERVAL / 60
    print(f"[enrich] {len(targets)} 個 rubric 樣本(快取已有 {hits} 個);預估 search 等待約 {est:.1f} 分鐘")

    for i, r in enumerate(targets, 1):
        fn = r["full_name"]
        entry = cache.setdefault(fn, {})
        login = fn.split("/")[0]
        print(f"  [{i}/{len(targets)}] {fn}", flush=True)

        r["author_followers"] = cached(entry, "author_followers",
                                       lambda: author_profile(login, token, ucache,
                                                              stats["author_followers"])["followers"])
        r["author_fame_tier"] = fame_tier(r["author_followers"])
        if r.get("created_at"):
            r["prior_fame_proxy"] = cached(entry, "prior_fame_proxy",
                                           lambda: prior_fame(login, r["created_at"], token, pcache,
                                                              stats["prior_fame_proxy"]))
            # prior_fame 為主判據:既有 ≥10k 星 repo 視為 F2、≥1k 視為至少 F1(BRIEF §6.5)
            pf = r.get("prior_fame_proxy") or 0
            if pf >= 10_000: r["author_fame_tier"] = "F2"
            elif pf >= 1_000 and r["author_fame_tier"] == "F0": r["author_fame_tier"] = "F1"
        if not args.skip_engagement:
            r["contributor_count"] = cached(entry, "contributor_count",
                                            lambda: contributor_count(fn, token, stats["contributor_count"]))
            r["nonauthor_pr_count"] = cached(entry, "nonauthor_pr_count",
                                             lambda: nonauthor_pr_count(fn, token, stats["nonauthor_pr_count"]))
        save_cache(cache_path, cache)   # 逐筆落地:Ctrl-C 不會丟掉已抓到的資料

    write_outputs(records, sampling_log, outdir, offline=False,
                  data_quality={k: v.summary() for k, v in stats.items()})


def write_probe(records, sampling_log, outdir):
    """--probe:只跑查詢與分層,不做 enrichment。用來在開跑前確認樣本規模。"""
    def count(key):
        c = {}
        for r in records: c[r.get(key)] = c.get(r.get(key), 0) + 1
        return dict(sorted(c.items(), key=lambda kv: str(kv[0])))
    n_rubric = sum(1 for r in records if r.get("in_rubric_sample"))
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": "probe — 未做 enrichment,未寫 repos.json",
        "n_records": len(records), "n_rubric_sample": n_rubric,
        "tier": count("star_tier"), "taxonomy": count("taxonomy"), "domain": count("domain"),
        "estimated_enrichment": {
            "search_calls": n_rubric * 2, "core_calls": n_rubric * 2,
            "min_wall_clock_minutes": round(n_rubric * 2 * SEARCH_INTERVAL / 60, 1),
        },
        "sampling_log": sampling_log,
        "records": [{k: r.get(k) for k in ("full_name", "stars", "star_tier", "taxonomy",
                                           "domain", "in_rubric_sample")} for r in records],
    }
    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, "phase1-probe.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    e = payload["estimated_enrichment"]
    print(f"\n[probe] {len(records)} repos;tier {payload['tier']};rubric 樣本 {n_rubric}")
    print(f"[probe] enrichment 預估:{e['search_calls']} 次 search + {e['core_calls']} 次 core"
          f",最短 {e['min_wall_clock_minutes']} 分鐘")
    print(f"[probe] wrote {out}(未動 repos.json)")


def selftest():
    assert assign_tier(240_338) == "T3" and assign_tier(99_999) == "T2"
    assert assign_tier(10_000) == "T2" and assign_tier(9_999) == "T1"
    assert assign_tier(1_000) == "T1" and assign_tier(999) == "T0"
    assert assign_tier(100) == "T0" and assign_tier(99) is None
    assert assign_cohort("2025-09-30T00:00:00Z") == "C0"
    assert assign_cohort("2025-10-01T00:00:00Z") == "C1"
    assert assign_cohort("2025-12-31T00:00:00Z") == "C1"
    assert assign_cohort("2026-01-01T00:00:00Z") == "C2"
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

    # --- 分層名額(BRIEF §3):T3/T2 全收,T1/T0 依名額,種子與 range 抽樣優先保留 ---
    recs = (
        [{"full_name": f"t3/{i}", "stars": 150_000 + i, "star_tier": "T3"} for i in range(3)]
        + [{"full_name": f"t2/{i}", "stars": 20_000 + i, "star_tier": "T2"} for i in range(4)]
        + [{"full_name": f"t1q/{i}", "stars": 5_000 + i, "star_tier": "T1"} for i in range(30)]
        + [{"full_name": "t1seed/a", "stars": 1_100, "star_tier": "T1", "seed_note": "種子"}]
        + [{"full_name": f"t1r/{i}", "stars": 1_200 + i, "star_tier": "T1", "sampled_via": "range"}
           for i in range(2)]
        + [{"full_name": f"t0q/{i}", "stars": 500 + i, "star_tier": "T0"} for i in range(25)]
    )
    log = {}
    kept = apply_strata_caps(recs, {"T3": None, "T2": None, "T1": 12, "T0": 10}, log)
    per = log["strata_caps"]["kept_per_tier"]
    assert per == {"T0": 10, "T1": 12, "T2": 4, "T3": 3}, per
    assert len(kept) == 29, len(kept)
    names = {r["full_name"] for r in kept}
    assert "t1seed/a" in names, "種子必須保留(即使星數低於同層主查詢結果)"
    assert {"t1r/0", "t1r/1"} <= names, "range 抽樣結果優先於主查詢"
    assert sum(len(v) for v in log["strata_caps"]["dropped_names"].values()) == len(recs) - len(kept)
    assert kept == sorted(kept, key=lambda r: -r["stars"]), "輸出需依星數遞減"
    # 全收模式:名額為 None 時一筆都不丟
    assert len(apply_strata_caps(recs, {"T3": None, "T2": None, "T1": None, "T0": None}, {})) == len(recs)

    # --- 二級速率限制退避 ---
    assert backoff_seconds({"Retry-After": "17"}, 0) == 17
    assert backoff_seconds({"retry-after": "17"}, 0) == 17          # header 大小寫不敏感
    assert backoff_seconds({}, 0) == 60 and backoff_seconds({}, 2) == 240
    assert backoff_seconds({}, 99) == 600                            # 上限封頂
    reset = {"x-ratelimit-remaining": "0", "x-ratelimit-reset": str(int(time.time()) + 30)}
    assert 25 <= backoff_seconds(reset, 0) <= 35, backoff_seconds(reset, 0)
    assert backoff_seconds({"x-ratelimit-remaining": "5"}, 0) == 60   # 尚有餘額 → 不看 reset

    # --- 錯誤歸因 ---
    sec = GHError(403, "/search/issues", '{"message":"You have exceeded a secondary rate limit."}')
    assert sec.is_secondary and sec.is_transient and sec.kind == "secondary-rate-limit"
    assert GHError(422, "/search/repositories", "Validation Failed").kind == "not-searchable"
    assert not GHError(404, "/repos/x/y", "Not Found").is_transient
    assert GHError(503, "/x", "").is_transient

    # --- 快取:成功值入庫、失敗不入庫(下次重跑會重試) ---
    entry, calls = {}, []
    assert cached(entry, "k", lambda: (calls.append(1), 7)[1]) == 7 and entry["k"] == 7
    assert cached(entry, "k", lambda: (calls.append(1), 9)[1]) == 7 and len(calls) == 1
    assert cached(entry, "bad", lambda: None) is None and "bad" not in entry

    # --- 統計摘要 ---
    fs = FieldStats(); fs.hit(); fs.miss("secondary-rate-limit"); fs.miss("secondary-rate-limit")
    assert fs.summary() == {"ok": 1, "failed": 2, "total": 3, "ok_pct": 33.3,
                            "failure_kinds": {"secondary-rate-limit": 2}}, fs.summary()
    print("[selftest] collect_repos: all assertions passed ✔")


def main():
    ap = argparse.ArgumentParser(description="Phase 1 資料收集")
    ap.add_argument("--out", default="research")
    ap.add_argument("--seeds", default="seeds/seed_repos.json")
    ap.add_argument("--pages", type=int, default=2, help="每組主查詢抓幾頁(50/頁)")
    ap.add_argument("--offline", action="store_true", help="只用 seeds,無 API(pipeline 測試)")
    ap.add_argument("--skip-engagement", action="store_true",
                    help="跳過 contributors / nonauthor PR(省配額;但這兩欄是 BRIEF §4 工序 2 的輸入,正式跑勿關)")
    ap.add_argument("--probe", action="store_true",
                    help="只跑查詢與分層,印出樣本規模與 enrichment 成本估算,不打 enrichment、不寫 repos.json")
    ap.add_argument("--no-strict-strata", dest="strict_strata", action="store_false", default=True,
                    help="關閉 BRIEF §3 分層名額(T1/T0 全收)。預設開啟,否則主查詢會把整片 T1/T0 掃進來")
    ap.add_argument("--cap-t3", type=int, default=None, help="T3 名額上限(<=0 表全收;預設全收)")
    ap.add_argument("--cap-t2", type=int, default=None, help="T2 名額上限(<=0 表全收;預設全收)")
    ap.add_argument("--cap-t1", type=int, default=None, help="T1 名額上限(預設 12,BRIEF §3「抽 10–12」)")
    ap.add_argument("--cap-t0", type=int, default=None, help="T0 名額上限(預設 18,BRIEF §3 G1 修訂「抽 15–20」)")
    ap.add_argument("--refresh-cache", action="store_true",
                    help="忽略 research/.enrich-cache.json,全部重抓")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest: return selftest()
    with open(args.seeds, encoding="utf-8") as f:
        seeds = json.load(f)
    if args.offline: return run_offline(seeds, args.out)
    return run_api(seeds, args.out, args)

if __name__ == "__main__":
    main()
