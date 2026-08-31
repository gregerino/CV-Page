from http.server import BaseHTTPRequestHandler
import json, os, urllib.request, urllib.parse
from datetime import datetime, timedelta, timezone

STOCKHOLM = timezone(timedelta(hours=2))

UPSTASH_URL = os.environ.get("UPSTASH_REDIS_REST_URL", "")
UPSTASH_TOKEN = os.environ.get("UPSTASH_REDIS_REST_TOKEN", "")
STATS_SECRET = os.environ.get("STATS_SECRET", "")


def redis_cmd(*args):
    if not UPSTASH_URL or not UPSTASH_TOKEN:
        return None
    url = UPSTASH_URL
    for arg in args:
        url += "/" + urllib.parse.quote(str(arg), safe="")
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {UPSTASH_TOKEN}"})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            return data.get("result")
    except Exception:
        return None


def get_val(key):
    v = redis_cmd("GET", key)
    return int(v) if v else 0


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse query string
        path = self.path
        qs = {}
        if "?" in path:
            qs_str = path.split("?", 1)[1]
            qs = dict(urllib.parse.parse_qsl(qs_str))

        # Auth check
        if not STATS_SECRET or qs.get("key") != STATS_SECRET:
            self._html(403, "<h1>Access denied</h1>")
            return

        # Gather stats
        total = get_val("stats:total")

        pages = ["home", "index.html", "about.html", "experience.html",
                 "skills.html", "education.html", "personal.html", "contact.html"]
        page_stats = {}
        for p in pages:
            v = get_val(f"stats:page:{p}")
            if v:
                name = p.replace(".html", "").capitalize()
                if p == "index.html":
                    name = "Home"
                page_stats[name] = v

        clicks = {}
        nav_targets = ["Home", "About", "CV", "Skills", "Education", "Personal", "Contact"]
        for t in nav_targets:
            v = get_val(f"stats:click:{t}")
            if v:
                clicks[t] = v

        # Daily stats (last 14 days)
        today = datetime.now(timezone.utc)
        daily = []
        for i in range(14):
            d = (today - timedelta(days=i)).strftime("%Y-%m-%d")
            v = get_val(f"stats:daily:{d}")
            visitors = get_val(f"stats:visitors:{d}")
            if v or i < 7:
                daily.append({"date": d, "views": v, "visitors": visitors})

        # Referrer stats
        ref_sources = ["Direct", "LinkedIn", "Google", "Facebook", "Instagram",
                        "X / Twitter", "GitHub"]
        referrers = {}
        # Check known sources
        for src in ref_sources:
            v = get_val(f"stats:ref:{src}")
            if v:
                referrers[src] = v
        # Also scan for unknown referrer keys
        all_keys = redis_cmd("KEYS", "stats:ref:*")
        if all_keys:
            for key in all_keys:
                src_name = key.replace("stats:ref:", "")
                if src_name not in referrers:
                    v = get_val(f"stats:ref:{src_name}")
                    if v:
                        referrers[src_name] = v

        # Device stats
        device_mobile = get_val("stats:device:mobile")
        device_desktop = get_val("stats:device:desktop")
        device_mobile_today = get_val(f"stats:device:mobile:{today.strftime('%Y-%m-%d')}")
        device_desktop_today = get_val(f"stats:device:desktop:{today.strftime('%Y-%m-%d')}")

        # AI search stats
        ai_total = get_val("stats:ai:total")
        ai_today = get_val(f"stats:ai:daily:{today.strftime('%Y-%m-%d')}")

        # Recent AI questions (last 20)
        raw_questions = redis_cmd("LRANGE", "stats:ai:questions", "0", "19")
        ai_questions = []
        if raw_questions:
            for item in raw_questions:
                try:
                    q = json.loads(item)
                    ai_questions.append(q)
                except Exception:
                    pass

        # Build HTML dashboard
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>CV Stats Dashboard</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#f2ede4;font-family:'Inter',sans-serif;color:#1c1710;padding:2rem}}
.container{{max-width:800px;margin:0 auto}}
h1{{font-size:1.6rem;font-weight:600;margin-bottom:0.3rem}}
.subtitle{{color:#9e9282;font-size:0.85rem;margin-bottom:2rem}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:1rem;margin-bottom:2rem}}
.card{{background:rgba(250,248,244,0.7);border:1px solid rgba(216,208,192,0.5);border-radius:10px;padding:1.2rem}}
.card-label{{font-size:0.65rem;font-weight:600;letter-spacing:0.2em;text-transform:uppercase;color:#9e9282;margin-bottom:0.4rem}}
.card-value{{font-size:1.8rem;font-weight:600;color:#1c1710}}
h2{{font-size:1rem;font-weight:600;margin-bottom:1rem;color:#3a3328}}
table{{width:100%;border-collapse:collapse;margin-bottom:2rem;background:rgba(250,248,244,0.7);border-radius:10px;overflow:hidden;border:1px solid rgba(216,208,192,0.5)}}
th,td{{padding:0.7rem 1rem;text-align:left;font-size:0.85rem;border-bottom:1px solid rgba(216,208,192,0.3)}}
th{{background:rgba(158,106,26,0.08);color:#9e6a1a;font-weight:600;font-size:0.7rem;letter-spacing:0.1em;text-transform:uppercase}}
tr:last-child td{{border-bottom:none}}
.bar-wrap{{display:flex;align-items:center;gap:0.6rem}}
.bar{{height:18px;background:linear-gradient(90deg,#9e6a1a,#b87d2a);border-radius:4px;min-width:2px}}
.bar-label{{font-size:0.75rem;color:#6b6050;white-space:nowrap}}
</style>
</head>
<body>
<div class="container">
<h1>CV Stats Dashboard</h1>
<p class="subtitle">Private analytics for marcushultberg.dev</p>

<div class="grid">
<div class="card"><p class="card-label">Total page views</p><p class="card-value">{total}</p></div>
<div class="card"><p class="card-label">Today</p><p class="card-value">{get_val(f"stats:daily:{today.strftime('%Y-%m-%d')}")}</p></div>
<div class="card"><p class="card-label">AI questions total</p><p class="card-value">{ai_total}</p></div>
<div class="card"><p class="card-label">AI questions today</p><p class="card-value">{ai_today}</p></div>
</div>

<h2>Devices</h2>
<div class="grid">
<div class="card"><p class="card-label">📱 Mobile — total</p><p class="card-value">{device_mobile}</p></div>
<div class="card"><p class="card-label">🖥️ Desktop — total</p><p class="card-value">{device_desktop}</p></div>
<div class="card"><p class="card-label">📱 Mobile — today</p><p class="card-value">{device_mobile_today}</p></div>
<div class="card"><p class="card-label">🖥️ Desktop — today</p><p class="card-value">{device_desktop_today}</p></div>
</div>

<h2>Traffic sources</h2>
<table>
<tr><th>Source</th><th>Visits</th><th></th></tr>
"""
        max_ref = max(referrers.values()) if referrers else 1
        for name, count in sorted(referrers.items(), key=lambda x: -x[1]):
            pct = int(count / max_ref * 100)
            html += f'<tr><td>{name}</td><td>{count}</td><td><div class="bar-wrap"><div class="bar" style="width:{pct}%"></div></div></td></tr>\n'
        if not referrers:
            html += '<tr><td colspan="3" style="color:#9e9282">No data yet</td></tr>\n'

        html += """</table>

<h2>Page views by page</h2>
<table>
<tr><th>Page</th><th>Views</th><th></th></tr>
"""
        max_page = max(page_stats.values()) if page_stats else 1
        for name, count in sorted(page_stats.items(), key=lambda x: -x[1]):
            pct = int(count / max_page * 100)
            html += f'<tr><td>{name}</td><td>{count}</td><td><div class="bar-wrap"><div class="bar" style="width:{pct}%"></div></div></td></tr>\n'
        if not page_stats:
            html += '<tr><td colspan="3" style="color:#9e9282">No data yet</td></tr>\n'

        html += """</table>

<h2>Navigation clicks</h2>
<table>
<tr><th>Link</th><th>Clicks</th><th></th></tr>
"""
        max_click = max(clicks.values()) if clicks else 1
        for name, count in sorted(clicks.items(), key=lambda x: -x[1]):
            pct = int(count / max_click * 100)
            html += f'<tr><td>{name}</td><td>{count}</td><td><div class="bar-wrap"><div class="bar" style="width:{pct}%"></div></div></td></tr>\n'
        if not clicks:
            html += '<tr><td colspan="3" style="color:#9e9282">No data yet</td></tr>\n'

        html += """</table>

<h2>AI search questions</h2>
<table>
<tr><th>Question</th><th>Time</th></tr>
"""
        if ai_questions:
            for q in ai_questions:
                question_text = q.get("q", "")
                # Escape HTML
                question_text = question_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                ts = q.get("t", "")
                # Format timestamp nicely
                try:
                    dt = datetime.fromisoformat(ts).astimezone(STOCKHOLM)
                    time_str = dt.strftime("%Y-%m-%d %H:%M")
                except Exception:
                    time_str = ts[:16] if ts else ""
                html += f'<tr><td>{question_text}</td><td style="white-space:nowrap;color:#9e9282">{time_str}</td></tr>\n'
        else:
            html += '<tr><td colspan="2" style="color:#9e9282">No questions yet</td></tr>\n'

        html += """</table>

<h2>Daily views (last 14 days)</h2>
<table>
<tr><th>Date</th><th>Views</th><th>Visitors</th><th></th></tr>
"""
        max_daily = max((d["views"] for d in daily), default=1) or 1
        for d in daily:
            pct = int(d["views"] / max_daily * 100) if d["views"] else 0
            html += f'<tr><td>{d["date"]}</td><td>{d["views"]}</td><td>{d["visitors"]}</td><td><div class="bar-wrap"><div class="bar" style="width:{pct}%"></div></div></td></tr>\n'

        html += """</table>
</div>
</body>
</html>"""

        self._html(200, html)

    def _html(self, code, content):
        body = content.encode()
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
