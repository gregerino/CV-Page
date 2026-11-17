from http.server import BaseHTTPRequestHandler
import glob, json, os, sys, urllib.request, urllib.parse
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _stats_template import TEMPLATE  # noqa: E402

UPSTASH_URL = os.environ.get("UPSTASH_REDIS_REST_URL", "")
UPSTASH_TOKEN = os.environ.get("UPSTASH_REDIS_REST_TOKEN", "")
STATS_SECRET = os.environ.get("STATS_SECRET", "")

DAYS = 90  # history sent to the dashboard; it slices 7/30/90 itself
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
    slugs = sorted(set(tracked) | set(packs))

    totals = dict(zip(tracked, mget(page_keys)))

    # Site-wide series
    daily = mget([f"stats:daily:{d}" for d in dates])
    visitors = mget([f"stats:visitors:{d}" for d in dates])
    ai_daily = mget([f"stats:ai:daily:{d}" for d in dates])

    # Per-page daily series, one flat MGET
    flat = mget([f"stats:daily:{d}:{s}" for s in slugs for d in dates])
    per_page = {s: flat[i * DAYS:(i + 1) * DAYS] for i, s in enumerate(slugs)}

    # Per-page detail (only collected since the tracking upgrade)
    detail = pipe(
        [["HGETALL", "stats:last"], ["GET", "stats:v2since"], ["GET", "stats:total"],
         ["GET", "stats:ai:total"], ["KEYS", "stats:ref:*"], ["KEYS", "stats:click:*"],
         ["LRANGE", "stats:ai:questions", "0", "29"],
         ["GET", "stats:device:mobile"], ["GET", "stats:device:desktop"]]
        + [["HGETALL", f"stats:pref:{s}"] for s in slugs]
        + [["HGETALL", f"stats:pdev:{s}"] for s in slugs]
        + [["GET", f"stats:uniq:{s}"] for s in slugs]
    )
    last, v2since, total, ai_total, ref_keys, click_keys, raw_q, mob, desk = detail[:9]
    n = len(slugs)
    prefs = detail[9:9 + n]
    pdevs = detail[9 + n:9 + 2 * n]
    uniqs = detail[9 + 2 * n:9 + 3 * n]
    last = hash_to_dict(last)

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
            "pack": packs.get(s),
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
