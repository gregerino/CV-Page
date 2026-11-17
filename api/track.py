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

        if event == "click":
            # Nav clicks are not page views; they only feed the click counter.
            target = str(body.get("target", ""))[:40]
            if target:
                cmds.append(["INCR", f"stats:click:{target}"])
            pipeline(cmds)
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

    def _json(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
