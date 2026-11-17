from http.server import BaseHTTPRequestHandler
import json, os, re, urllib.request
from datetime import datetime, timezone
from urllib.parse import urlparse

# Traffic from these is our own, not a referral. "www." is stripped before the check.
OWN_HOSTS = ("cv-page-mocha.vercel.app", "marcushultberg.dev", "localhost")

UPSTASH_URL = os.environ.get("UPSTASH_REDIS_REST_URL", "")
UPSTASH_TOKEN = os.environ.get("UPSTASH_REDIS_REST_TOKEN", "")

# The catch-all rewrite serves index.html for any slug, so junk paths reach us.
# Anything that doesn't look like one of our pages is counted as "other".
PAGE_RE = re.compile(r"^[a-z0-9][a-z0-9.-]{0,59}$")

# Crawlers, link previewers, monitors and headless browsers. Matched against the
# User-Agent header; a request with no User-Agent at all is treated as a bot too.
BOT_RE = re.compile(
    r"bot\b|bot/|crawl|spider|slurp|preview|scrap|fetch|headless|phantom|puppeteer|playwright|"
    r"selenium|lighthouse|pagespeed|gtmetrix|pingdom|uptime|monitor|curl|wget|python-|"
    r"go-http|java/|okhttp|axios|node-fetch|httpclient|facebookexternalhit|embedly|"
    r"whatsapp|telegram|discord|skype|vercel|bingpreview|google-inspectiontool|chrome-lighthouse",
    re.I,
)

def os_for(ua):
    """Operating system from the User-Agent header. Mobile is checked first:
    Android UAs also say Linux, and iPhone UAs also say Mac OS X."""
    if re.search(r"iPhone|iPad|iPod", ua):
        return "iOS"
    if "Android" in ua:
        return "Android"
    if "Windows" in ua:
        return "Windows"
    if "CrOS" in ua:
        return "ChromeOS"
    if re.search(r"Macintosh|Mac OS X", ua):
        return "macOS"
    if re.search(r"Linux|X11|Ubuntu|Fedora", ua):
        return "Linux"
    return "Annat"


VISIT_ID_RE = re.compile(r"^[a-z0-9]{8,24}$")
MAX_DURATION = 4 * 3600      # a tab left open all day isn't a 9-hour read
VISIT_TTL = 180 * 86400      # visit records expire after ~6 months
VISITS_PER_PAGE = 200
VISITS_TOTAL = 500


def entry_link(referrer):
    """The link the visitor followed: host + path, no query string
    (those carry tracking ids, not anything worth reading)."""
    try:
        u = urlparse(referrer.strip())
    except Exception:
        return ""
    host = (u.hostname or "").lower()
    if not host:
        return ""
    host = host[4:] if host.startswith("www.") else host
    return (host + (u.path if u.path not in ("", "/") else ""))[:160]


def pipeline(cmds):
    """Run all commands in one round trip to Upstash."""
    if not UPSTASH_URL or not UPSTASH_TOKEN or not cmds:
        return None
    req = urllib.request.Request(
        UPSTASH_URL.rstrip("/") + "/pipeline",
        data=json.dumps(cmds).encode(),
        headers={"Authorization": f"Bearer {UPSTASH_TOKEN}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read())
    except Exception:
        return None


def source_for(referrer):
    if not referrer:
        return "Direct"
    try:
        host = (urlparse(referrer).hostname or "").lower().replace("www.", "")
    except Exception:
        return ""
    if "linkedin" in host or host == "lnkd.in":
        return "LinkedIn"
    if "google" in host:
        return "Google"
    if "facebook" in host or "fb.com" in host:
        return "Facebook"
    if "instagram" in host:
        return "Instagram"
    if "twitter" in host or "x.com" in host or host == "t.co":
        return "X / Twitter"
    if "github" in host:
        return "GitHub"
    if host and host not in OWN_HOSTS:
        return host
    return ""  # internal navigation


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length) or b"{}")
        except Exception:
            self._json(400, {"ok": False})
            return

        page = str(body.get("page", "")).strip("/").lower() or "home"
        if not PAGE_RE.match(page):
            page = "other"
        event = body.get("event", "pageview")
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        cmds = []

        # Bots: counted, so the dashboard can say how many, but kept out of every
        # other number. The browser flags automation it can see (webdriver).
        ua = self.headers.get("User-Agent", "")
        if not ua or BOT_RE.search(ua) or body.get("bot"):
            if event == "pageview":
                pipeline([["INCR", "stats:bots"], ["INCR", f"stats:bots:{today}"]])
            self._json(200, {"ok": True})
            return

        if event == "click":
            # Nav clicks are not page views; they only feed the click counter.
            target = str(body.get("target", ""))[:40]
            if target and not body.get("own"):
                cmds.append(["INCR", f"stats:click:{target}"])
            pipeline(cmds)
            self._json(200, {"ok": True})
            return

        system = os_for(ua)
        own = bool(body.get("own"))

        if event == "visit":
            self._visit(page, body, system, own)
            return

        if own:
            # Marcus's own visits: kept in their own keys, never in visitor numbers.
            if event == "pageview":
                pipeline([
                    ["INCR", "stats:own:total"],
                    ["HINCRBY", "stats:own:pages", page, 1],
                    ["INCR", f"stats:own:daily:{today}"],
                    ["INCR", f"stats:own:daily:{today}:{page}"],
                    ["HSET", "stats:own:last", page, datetime.now(timezone.utc).isoformat(timespec="seconds")],
                ])
            self._json(200, {"ok": True})
            return

        device = body.get("device", "")
        source = source_for(str(body.get("referrer", "")).strip())

        cmds += [
            ["SETNX", "stats:v2since", today],
            ["INCR", "stats:total"],
            ["INCR", f"stats:page:{page}"],
            ["INCR", f"stats:daily:{today}"],
            ["INCR", f"stats:daily:{today}:{page}"],
            ["HINCRBY", "stats:os", system, 1],
            ["HINCRBY", f"stats:pos:{page}", system, 1],
            ["HINCRBY", f"stats:osd:{today}", system, 1],
            ["HSET", "stats:last", page, datetime.now(timezone.utc).isoformat(timespec="seconds")],
        ]
        if device in ("mobile", "desktop"):
            cmds += [
                ["INCR", f"stats:device:{device}"],
                ["INCR", f"stats:device:{device}:{today}"],
                ["HINCRBY", f"stats:pdev:{page}", device, 1],
            ]
        if source:
            cmds += [
                ["INCR", f"stats:ref:{source}"],
                ["HINCRBY", f"stats:pref:{page}", source, 1],
            ]
        # The browser remembers what it has seen, so these count people, not loads.
        if body.get("newDay"):
            cmds.append(["INCR", f"stats:visitors:{today}"])
        if body.get("newPage"):
            cmds.append(["INCR", f"stats:uniq:{page}"])

        pipeline(cmds)
        self._json(200, {"ok": True})

    def _visit(self, page, body, system, own=False):
        """Store one visit: entry link, time on screen and clicks.

        The browser sends the same visit id each time the tab is hidden, so the
        record is overwritten, never duplicated."""
        vid = str(body.get("id", ""))
        if not VISIT_ID_RE.match(vid):
            self._json(400, {"ok": False})
            return
        try:
            start = int(body.get("start", 0)) // 1000
            dur = max(0, min(int(body.get("dur", 0)), MAX_DURATION))
        except (TypeError, ValueError):
            self._json(400, {"ok": False})
            return
        now = int(datetime.now(timezone.utc).timestamp())
        if not (now - 86400 < start <= now + 60):
            start = now

        clicks = []
        for c in (body.get("clicks") or [])[:30]:
            if isinstance(c, dict):
                try:
                    s = int(c.get("s", 0))
                except (TypeError, ValueError):
                    s = 0
                clicks.append({"l": str(c.get("l", ""))[:60], "h": str(c.get("h", ""))[:120], "s": s})

        record = {
            "id": vid,
            "page": page,
            "t": start,
            "dur": dur,
            "os": system,
            "dev": body.get("device") if body.get("device") in ("mobile", "desktop") else "",
            "from": entry_link(str(body.get("referrer", ""))),
            "clicks": clicks,
        }
        if own:
            record["own"] = True
            pipeline([
                ["SET", f"stats:visit:{vid}", json.dumps(record, ensure_ascii=False), "EX", VISIT_TTL],
                ["ZADD", "stats:ownvisits", start, f"{page}|{vid}"],
                ["ZREMRANGEBYRANK", "stats:ownvisits", 0, -(VISITS_TOTAL + 1)],
            ])
            self._json(200, {"ok": True})
            return
        pipeline([
            ["SET", f"stats:visit:{vid}", json.dumps(record, ensure_ascii=False), "EX", VISIT_TTL],
            ["ZADD", f"stats:visits:{page}", start, vid],
            ["ZADD", "stats:visits", start, f"{page}|{vid}"],
            # Keep the latest visits only.
            ["ZREMRANGEBYRANK", f"stats:visits:{page}", 0, -(VISITS_PER_PAGE + 1)],
            ["ZREMRANGEBYRANK", "stats:visits", 0, -(VISITS_TOTAL + 1)],
        ])
        self._json(200, {"ok": True})

    def _json(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
