from http.server import BaseHTTPRequestHandler
import glob, json, os, sys, urllib.request, urllib.parse
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _stats_template import TEMPLATE  # noqa: E402

UPSTASH_URL = os.environ.get("UPSTASH_REDIS_REST_URL", "")
UPSTASH_TOKEN = os.environ.get("UPSTASH_REDIS_REST_TOKEN", "")
STATS_SECRET = os.environ.get("STATS_SECRET", "")

DAYS = 180  # history sent to the dashboard: 90 days shown, plus the 90 before to compare with
VISITS_PER_PAGE = 50
VISITS_RECENT = 40
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _post(path, payload):
    if not UPSTASH_URL or not UPSTASH_TOKEN:
        return None
    req = urllib.request.Request(
        UPSTASH_URL.rstrip("/") + path,
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {UPSTASH_TOKEN}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            return json.loads(resp.read())
    except Exception:
        return None


def pipe(cmds):
    """Run many commands in one round trip. Returns one result per command."""
    out = []
    for i in range(0, len(cmds), 200):
        chunk = cmds[i:i + 200]
        res = _post("/pipeline", chunk) or []
        out += [r.get("result") if isinstance(r, dict) else None for r in res]
        out += [None] * (len(chunk) - len(res))
    return out


def mget(keys):
    """MGET in chunks, as ints."""
    if not keys:
        return []
    chunks = [keys[i:i + 1000] for i in range(0, len(keys), 1000)]
    vals = []
    for res in pipe([["MGET", *c] for c in chunks]):
        vals += res or []
    vals += [None] * (len(keys) - len(vals))
    return [int(v) if v else 0 for v in vals]


def hash_to_dict(flat):
    """Upstash returns HGETALL as [k1, v1, k2, v2, ...]."""
    if not flat:
        return {}
    return {flat[i]: flat[i + 1] for i in range(0, len(flat) - 1, 2)}


def load_packs():
    """Every job pack in jobs/, so pages nobody has opened still show."""
    packs = {}
    for path in glob.glob(os.path.join(ROOT, "jobs", "*.json")):
        slug = os.path.basename(path)[:-5]
        if slug == "exempel":
            continue
        try:
            with open(path, encoding="utf-8") as f:
                d = json.load(f)
        except Exception:
            d = {}
        packs[slug] = {"company": d.get("company") or "", "role": d.get("roleName") or ""}
    return packs


def gather():
    today = datetime.now(timezone.utc).date()
    dates = [(today - timedelta(days=i)).isoformat() for i in range(DAYS - 1, -1, -1)]

    packs = load_packs()
    page_keys = pipe([["KEYS", "stats:page:*"]])[0] or []
    tracked = [k[len("stats:page:"):] for k in page_keys]
    # Pages only Marcus has opened still need a row in "Mina besök".
    own_seen = hash_to_dict(pipe([["HGETALL", "stats:own:pages"]])[0])
    slugs = sorted(set(tracked) | set(packs) | set(own_seen))

    totals = dict(zip(tracked, mget(page_keys)))

    # Site-wide series
    daily = mget([f"stats:daily:{d}" for d in dates])
    visitors = mget([f"stats:visitors:{d}" for d in dates])
    ai_daily = mget([f"stats:ai:daily:{d}" for d in dates])
    bots_daily = mget([f"stats:bots:{d}" for d in dates])

    # Per-page daily series, one flat MGET
    flat = mget([f"stats:daily:{d}:{s}" for s in slugs for d in dates])
    per_page = {s: flat[i * DAYS:(i + 1) * DAYS] for i, s in enumerate(slugs)}

    # Marcus's own visits, kept apart from visitor numbers
    own_daily = mget([f"stats:own:daily:{d}" for d in dates])
    own_flat = mget([f"stats:own:daily:{d}:{s}" for s in slugs for d in dates])
    own_per_page = {s: own_flat[i * DAYS:(i + 1) * DAYS] for i, s in enumerate(slugs)}

    # Per-page detail (only collected since the tracking upgrade)
    detail = pipe(
        [["HGETALL", "stats:last"], ["GET", "stats:v2since"], ["GET", "stats:total"],
         ["GET", "stats:ai:total"], ["KEYS", "stats:ref:*"], ["KEYS", "stats:click:*"],
         ["LRANGE", "stats:ai:questions", "0", "29"],
         ["GET", "stats:device:mobile"], ["GET", "stats:device:desktop"], ["GET", "stats:bots"],
         ["ZREVRANGE", "stats:visits", "0", str(VISITS_RECENT - 1)], ["HGETALL", "stats:os"],
         ["GET", "stats:own:total"], ["HGETALL", "stats:own:pages"], ["HGETALL", "stats:own:last"],
         ["ZREVRANGE", "stats:ownvisits", "0", "199"]]
        + [["HGETALL", f"stats:pref:{s}"] for s in slugs]
        + [["HGETALL", f"stats:pdev:{s}"] for s in slugs]
        + [["GET", f"stats:uniq:{s}"] for s in slugs]
        + [["ZREVRANGE", f"stats:visits:{s}", "0", str(VISITS_PER_PAGE - 1)] for s in slugs]
        + [["HGETALL", f"stats:pos:{s}"] for s in slugs]
        + [["HGETALL", f"stats:osd:{d}"] for d in dates]
    )
    (last, v2since, total, ai_total, ref_keys, click_keys, raw_q, mob, desk, bots, recent, os_all,
     own_total, own_pages, own_last, own_recent) = detail[:16]
    n, o = len(slugs), 16
    own_pages = {k: int(v) for k, v in hash_to_dict(own_pages).items()}
    own_last = hash_to_dict(own_last)
    prefs = detail[o:o + n]
    pdevs = detail[o + n:o + 2 * n]
    uniqs = detail[o + 2 * n:o + 3 * n]
    vids = detail[o + 3 * n:o + 4 * n]
    poss = detail[o + 4 * n:o + 5 * n]
    os_daily = [{k: int(v) for k, v in hash_to_dict(h).items()} for h in detail[o + 5 * n:o + 5 * n + DAYS]]
    last = hash_to_dict(last)

    # Visit records: the latest per page, plus the latest across the site.
    recent_ids = [m.split("|", 1)[1] for m in (recent or []) if "|" in m]
    own_ids = [m.split("|", 1)[1] for m in (own_recent or []) if "|" in m]
    all_ids = sorted({i for ids in vids for i in (ids or [])} | set(recent_ids) | set(own_ids))
    raw = pipe([["MGET", *all_ids[i:i + 500]] for i in range(0, len(all_ids), 500)]) if all_ids else []
    visit_by_id = {}
    for chunk in raw:
        for item in chunk or []:
            try:
                v = json.loads(item)
                visit_by_id[v["id"]] = v
            except Exception:
                pass

    ref_keys = ref_keys or []
    click_keys = click_keys or []
    referrers = dict(zip([k[len("stats:ref:"):] for k in ref_keys], mget(ref_keys)))
    clicks = dict(zip([k[len("stats:click:"):] for k in click_keys], mget(click_keys)))

    questions = []
    for item in raw_q or []:
        try:
            questions.append(json.loads(item))
        except Exception:
            pass

    pages = []
    for i, s in enumerate(slugs):
        pages.append({
            "slug": s,
            "total": totals.get(s, 0),
            "daily": per_page[s],
            "uniq": int(uniqs[i]) if uniqs[i] else 0,
            "last": last.get(s),
            "refs": {k: int(v) for k, v in hash_to_dict(prefs[i]).items()},
            "devices": {k: int(v) for k, v in hash_to_dict(pdevs[i]).items()},
            "os": {k: int(v) for k, v in hash_to_dict(poss[i]).items()},
            "ownTotal": own_pages.get(s, 0),
            "ownDaily": own_per_page[s],
            "ownLast": own_last.get(s),
            "pack": packs.get(s),
            "visits": [visit_by_id[v] for v in (vids[i] or []) if v in visit_by_id],
        })

    return {
        "generated": datetime.now(timezone.utc).isoformat(),
        "connected": bool(UPSTASH_URL and UPSTASH_TOKEN),
        "dates": dates,
        "v2since": v2since,
        "total": int(total) if total else 0,
        "aiTotal": int(ai_total) if ai_total else 0,
        "daily": daily,
        "visitors": visitors,
        "aiDaily": ai_daily,
        "pages": pages,
        "referrers": referrers,
        "clicks": clicks,
        "devices": {"mobile": int(mob) if mob else 0, "desktop": int(desk) if desk else 0},
        "questions": questions,
        "bots": int(bots) if bots else 0,
        "botsDaily": bots_daily,
        "os": {k: int(v) for k, v in hash_to_dict(os_all).items()},
        "osDaily": os_daily,
        "ownTotal": int(own_total) if own_total else 0,
        "ownDaily": own_daily,
        "ownVisits": [visit_by_id[v] for v in own_ids if v in visit_by_id],
        "recent": [visit_by_id[v] for v in recent_ids if v in visit_by_id],
    }


def render(data):
    # "</" would let a stored question close the <script> tag early.
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    return TEMPLATE.replace("/*__DATA__*/null", blob)


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        qs = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(self.path).query))
        if not STATS_SECRET or qs.get("key") != STATS_SECRET:
            self._send(403, "text/html", "<h1>Access denied</h1>")
            return
        data = gather()
        if qs.get("format") == "json":
            self._send(200, "application/json", json.dumps(data, ensure_ascii=False))
        else:
            self._send(200, "text/html", render(data))

    def _send(self, code, ctype, content):
        body = content.encode()
        self.send_response(code)
        self.send_header("Content-Type", f"{ctype}; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Robots-Tag", "noindex")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
