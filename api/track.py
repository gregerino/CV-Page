from http.server import BaseHTTPRequestHandler
import json, os, urllib.request, urllib.parse
from datetime import datetime, timezone

# Traffic from these is our own, not a referral. "www." is stripped before the check.
OWN_HOSTS = ("cv-page-mocha.vercel.app", "marcushultberg.dev", "localhost")

UPSTASH_URL = os.environ.get("UPSTASH_REDIS_REST_URL", "")
UPSTASH_TOKEN = os.environ.get("UPSTASH_REDIS_REST_TOKEN", "")


def redis_cmd(*args):
    """Execute a Redis command via Upstash REST API."""
    if not UPSTASH_URL or not UPSTASH_TOKEN:
        return None
    url = UPSTASH_URL
    for arg in args:
        url += "/" + urllib.parse.quote(str(arg), safe="")
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {UPSTASH_TOKEN}"})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read())
    except Exception:
        return None


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length))

        page = body.get("page", "unknown").strip("/") or "home"
        event = body.get("event", "pageview")  # pageview or click
        target = body.get("target", "")  # nav link clicked
        device = body.get("device", "unknown")  # mobile or desktop
        referrer = body.get("referrer", "").strip()

        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        # Total page views
        redis_cmd("INCR", "stats:total")

        # Page views per page
        redis_cmd("INCR", f"stats:page:{page}")

        # Daily page views
        redis_cmd("INCR", f"stats:daily:{today}")

        # Daily per page
        redis_cmd("INCR", f"stats:daily:{today}:{page}")

        # Nav click tracking
        if event == "click" and target:
            redis_cmd("INCR", f"stats:click:{target}")

        # Device tracking
        if device in ("mobile", "desktop"):
            redis_cmd("INCR", f"stats:device:{device}")
            redis_cmd("INCR", f"stats:device:{device}:{today}")

        # Referrer tracking
        if referrer:
            try:
                from urllib.parse import urlparse
                host = urlparse(referrer).hostname or ""
                host = host.lower().replace("www.", "")
                if "linkedin" in host:
                    source = "LinkedIn"
                elif "google" in host:
                    source = "Google"
                elif "facebook" in host or "fb.com" in host:
                    source = "Facebook"
                elif "instagram" in host:
                    source = "Instagram"
                elif "twitter" in host or "x.com" in host or "t.co" in host:
                    source = "X / Twitter"
                elif "github" in host:
                    source = "GitHub"
                elif host and host not in OWN_HOSTS:
                    source = host
                else:
                    source = ""
                if source:
                    redis_cmd("INCR", f"stats:ref:{source}")
            except Exception:
                pass
        else:
            redis_cmd("INCR", "stats:ref:Direct")

        # Unique visitors (approximate, by day)
        redis_cmd("INCR", f"stats:visitors:{today}")

        self._json(200, {"ok": True})

    def _json(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
