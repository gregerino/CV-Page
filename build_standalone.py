#!/usr/bin/env python3
"""Build a single self-contained HTML file with all pages, styles, and embedded images."""
import base64, pathlib

root = pathlib.Path("/Users/marcus/CV Page")

def b64img(name):
    data = (root / name).read_bytes()
    return f"data:image/jpeg;base64,{base64.b64encode(data).decode()}"

goteborg = b64img("goteborg.jpg")
marcus = b64img("marcus.jpg")

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Marcus Hultberg – People & Culture</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
:root {{
  --bg: #f2ede4; --bg2: #ece6da; --bg3: #e4ddd0;
  --white: #faf8f4;
  --border: rgba(216,208,192,0.5); --border-light: rgba(228,221,208,0.4); --border-strong: rgba(184,173,152,0.5);
  --ink: #1c1710; --ink-mid: #3a3328; --ink-light: #6b6050; --ink-dim: #9e9282;
  --amber: #9e6a1a; --amber-light: #b87d2a; --amber-pale: rgba(158,106,26,0.08);
  --radius: 10px; --max: 1020px;
  --shadow: 0 2px 12px rgba(28,23,16,0.1), 0 1px 3px rgba(28,23,16,0.06);
}}
html {{ scroll-behavior: smooth; }}
body {{ background: var(--bg); color: var(--ink); font-family: 'Inter', system-ui, sans-serif; font-size: 15px; line-height: 1.7; -webkit-font-smoothing: antialiased; }}

.hero-bg {{ position: fixed; inset: 0; z-index: 0; background-image: url('{goteborg}'); background-size: cover; background-position: center 60%; }}
.hero-bg::after {{ content: ''; position: absolute; inset: 0; background: linear-gradient(160deg, rgba(242,237,228,0.96) 0%, rgba(236,230,218,0.93) 40%, rgba(228,221,208,0.88) 70%, rgba(220,212,198,0.82) 100%); }}

nav {{ position: fixed; top: 0; left: 0; right: 0; z-index: 100; background: rgba(250,248,244,0.7); backdrop-filter: blur(12px); border-bottom: 1px solid var(--border); }}
.nav-inner {{ max-width: var(--max); margin: 0 auto; padding: 0 2.5rem; display: flex; align-items: center; justify-content: space-between; height: 60px; }}
.nav-logo {{ font-family: 'Lora', Georgia, serif; font-size: 1.1rem; font-weight: 500; color: var(--ink); text-decoration: none; }}
.nav-logo span {{ color: var(--amber); }}
.nav-links {{ display: flex; gap: 0; list-style: none; }}
.nav-links a {{ font-size: 0.72rem; font-weight: 500; letter-spacing: 0.1em; text-transform: uppercase; color: var(--ink-light); text-decoration: none; padding: 0.4rem 0.85rem; transition: color 0.15s; cursor: pointer; }}
.nav-links a:hover {{ color: var(--ink); }}
.nav-links a.active {{ color: var(--amber); }}

.page {{ position: relative; z-index: 1; max-width: var(--max); margin: 0 auto; padding: 96px 2.5rem 80px; }}
.section {{ display: none; }}
.section.active {{ display: block; }}

.section-header {{ margin-bottom: 3rem; }}
.section-eyebrow {{ font-size: 0.67rem; font-weight: 600; letter-spacing: 0.25em; text-transform: uppercase; color: var(--amber); margin-bottom: 0.7rem; }}
.section-title {{ font-family: 'Lora', Georgia, serif; font-size: 2.5rem; font-weight: 500; color: var(--ink); line-height: 1.15; }}
.section-divider {{ display: flex; align-items: center; gap: 0.6rem; margin-top: 1.1rem; }}
.section-divider::before {{ content: ''; width: 32px; height: 1px; background: var(--amber); }}
.section-divider::after {{ content: ''; width: 6px; height: 6px; background: var(--amber); transform: rotate(45deg); }}

.btn {{ font-size: 0.72rem; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; text-decoration: none; padding: 0.75rem 1.7rem; border-radius: var(--radius); transition: all 0.18s; display: inline-block; cursor: pointer; }}
.btn-primary {{ background: var(--ink); color: var(--white); border: 1px solid var(--ink); }}
.btn-primary:hover {{ background: var(--ink-mid); border-color: var(--ink-mid); }}
.btn-outline {{ background: transparent; border: 1px solid var(--border-strong); color: var(--ink-light); }}
.btn-outline:hover {{ border-color: var(--ink); color: var(--ink); }}

footer {{ position: relative; z-index: 1; border-top: 1px solid var(--border); padding: 2rem 2.5rem; max-width: var(--max); margin: 0 auto; display: flex; justify-content: space-between; align-items: center; }}
footer p {{ font-size: 0.72rem; color: var(--ink-dim); }}
footer a {{ font-size: 0.72rem; font-weight: 500; color: var(--ink-mid); text-decoration: none; cursor: pointer; }}
footer a:hover {{ color: var(--amber); }}

/* AI SEARCH */
.ai-bar {{ max-width: var(--max); margin: 0 auto; padding: 80px 2.5rem 0; display: flex; flex-direction: column; align-items: center; }}
.ai-bar-wrap {{ position: relative; max-width: 620px; width: 100%; }}
.ai-bar-input {{ width: 100%; font-family: 'Inter', sans-serif; font-size: 0.95rem; color: var(--ink); background: rgba(250,248,244,0.6); backdrop-filter: blur(8px); border: 1px solid var(--border-strong); border-radius: 100px; padding: 0.95rem 3.5rem 0.95rem 1.5rem; outline: none; box-shadow: 0 2px 12px rgba(28,23,16,0.06), inset 0 1px 0 rgba(255,255,255,0.4); transition: border-color 0.15s, box-shadow 0.15s; }}
.ai-bar-input:focus {{ border-color: var(--amber); box-shadow: 0 2px 20px rgba(158,106,26,0.12); }}
.ai-bar-input::placeholder {{ color: var(--ink-dim); }}
.ai-bar-btn {{ position: absolute; right: 6px; top: 50%; transform: translateY(-50%); width: 38px; height: 38px; background: var(--ink); border: none; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: background 0.15s; }}
.ai-bar-btn:hover {{ background: var(--ink-mid); }}
.ai-bar-btn:disabled {{ opacity: 0.4; cursor: not-allowed; }}
.ai-bar-btn svg {{ width: 16px; height: 16px; }}
.ai-bar-response {{ display: none; margin-top: 0.75rem; background: rgba(250,248,244,0.55); backdrop-filter: blur(8px); border: 1px solid var(--border); border-radius: 16px; padding: 1.2rem 1.5rem; box-shadow: 0 2px 12px rgba(28,23,16,0.08); max-width: 620px; }}
.ai-bar-response.visible {{ display: block; }}
.ai-bar-response-label {{ font-size: 0.6rem; font-weight: 600; letter-spacing: 0.2em; text-transform: uppercase; color: var(--amber); margin-bottom: 0.5rem; }}
.ai-bar-response-text {{ font-size: 0.9rem; color: var(--ink-mid); line-height: 1.75; }}
.ai-bar-loading {{ display: none; margin-top: 0.75rem; align-items: center; gap: 0.5rem; color: var(--ink-dim); font-size: 0.82rem; max-width: 620px; background: rgba(250,248,244,0.55); backdrop-filter: blur(8px); border: 1px solid var(--border); border-radius: 16px; padding: 1rem 1.5rem; box-shadow: 0 2px 12px rgba(28,23,16,0.04), inset 0 1px 0 rgba(255,255,255,0.4); }}
.ai-bar-loading.visible {{ display: flex; }}
.ai-dot {{ width: 5px; height: 5px; background: var(--amber); border-radius: 50%; animation: pulse 1.2s ease-in-out infinite; }}
.ai-dot:nth-child(2) {{ animation-delay: 0.2s; }}
.ai-dot:nth-child(3) {{ animation-delay: 0.4s; }}
@keyframes pulse {{ 0%, 100% {{ opacity: 0.2; transform: scale(0.8); }} 50% {{ opacity: 1; transform: scale(1); }} }}

/* HERO */
.hero {{ min-height: calc(100vh - 200px); display: flex; align-items: center; }}
.hero-grid {{ display: grid; grid-template-columns: 1fr 370px; gap: 5rem; align-items: center; width: 100%; }}
.hero-eyebrow {{ font-size: 0.67rem; font-weight: 600; letter-spacing: 0.25em; text-transform: uppercase; color: var(--amber); margin-bottom: 1rem; }}
.hero-name {{ font-family: 'Lora', Georgia, serif; font-size: clamp(3rem, 5.5vw, 4.8rem); font-weight: 500; color: var(--ink); line-height: 1.05; margin-bottom: 0.5rem; }}
.hero-rule {{ display: flex; align-items: center; gap: 0.6rem; margin-bottom: 1.4rem; }}
.hero-rule::before {{ content: ''; width: 24px; height: 1px; background: var(--amber); }}
.hero-rule span {{ font-size: 0.72rem; font-weight: 500; letter-spacing: 0.14em; text-transform: uppercase; color: var(--ink-light); }}
.hero-subtitle {{ font-family: 'Lora', Georgia, serif; font-size: 1rem; font-style: italic; color: var(--ink-light); margin-bottom: 2rem; line-height: 1.8; max-width: 400px; }}
.hero-tags {{ display: flex; flex-wrap: wrap; gap: 0.4rem; margin-bottom: 2.4rem; }}
.hero-tag {{ font-size: 0.7rem; font-weight: 500; color: var(--ink-mid); background: rgba(250,248,244,0.5); backdrop-filter: blur(6px); border: 1px solid var(--border); border-radius: var(--radius); padding: 0.28rem 0.8rem; }}
.hero-cta {{ display: flex; gap: 0.75rem; flex-wrap: wrap; }}
.hero-stats {{ display: flex; margin-top: 3rem; padding-top: 2rem; border-top: 1px solid var(--border); }}
.hero-stat {{ flex: 1; padding-right: 2rem; border-right: 1px solid var(--border); margin-right: 2rem; }}
.hero-stat:last-child {{ border-right: none; margin-right: 0; padding-right: 0; }}
.hero-stat-num {{ font-family: 'Lora', Georgia, serif; font-size: 2rem; font-weight: 500; color: var(--ink); line-height: 1; margin-bottom: 0.3rem; }}
.hero-stat-label {{ font-size: 0.65rem; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; color: var(--ink-dim); }}
.hero-photo-wrap {{ position: relative; }}
.hero-photo-frame {{ position: relative; }}
.hero-photo-card {{ position: relative; z-index: 1; background: transparent; border-radius: 10px; overflow: hidden; aspect-ratio: 4/5; box-shadow: 0 8px 40px rgba(28,23,16,0.12); }}
.hero-photo-card::after {{ content: ''; position: absolute; inset: 0; border-radius: 10px; box-shadow: inset 0 0 30px 10px rgba(242,237,228,0.5); pointer-events: none; z-index: 1; }}
.hero-photo-card img {{ width: 100%; height: 100%; object-fit: cover; object-position: top center; display: block; }}
.hero-name-badge {{ position: absolute; bottom: 0; left: 0; right: 0; background: rgba(28,23,16,0.75); backdrop-filter: blur(12px); padding: 1.1rem 1.4rem; z-index: 2; }}
.hero-name-badge-name {{ font-family: 'Lora', Georgia, serif; font-size: 0.95rem; font-weight: 600; color: var(--white); }}
.hero-name-badge-title {{ font-size: 0.7rem; color: rgba(242,237,228,0.5); margin-top: 0.15rem; }}
.hero-badge-dot {{ display: inline-block; width: 6px; height: 6px; background: #6dbe8d; border-radius: 50%; margin-right: 0.4rem; }}

/* ABOUT */
.om-grid {{ display: grid; grid-template-columns: 280px 1fr; gap: 4.5rem; align-items: start; }}
.om-photo-wrap {{ position: sticky; top: 84px; }}
.om-photo {{ border: 1px solid var(--border-strong); border-radius: var(--radius); overflow: hidden; aspect-ratio: 3/4; }}
.om-photo img {{ width: 100%; height: 100%; object-fit: cover; object-position: top center; display: block; }}
.profil-ingress {{ font-family: 'Lora', Georgia, serif; font-size: 1.1rem; font-style: italic; line-height: 1.85; color: var(--ink-mid); margin-bottom: 2rem; padding-left: 1.4rem; border-left: 2px solid var(--amber); }}
.profil-body {{ font-size: 0.93rem; color: var(--ink-light); line-height: 1.8; margin-bottom: 1rem; }}
.om-cards {{ display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; margin-top: 2.5rem; }}
.om-card {{ background: rgba(250,248,244,0.55); backdrop-filter: blur(8px); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.2rem 1.4rem; box-shadow: 0 2px 12px rgba(28,23,16,0.04), inset 0 1px 0 rgba(255,255,255,0.4); }}
.om-card-label {{ font-size: 0.65rem; font-weight: 600; letter-spacing: 0.2em; text-transform: uppercase; color: var(--amber); margin-bottom: 0.35rem; }}
.om-card-value {{ font-size: 0.88rem; color: var(--ink-mid); line-height: 1.5; }}
.om-card-value a {{ color: var(--ink-mid); text-decoration: none; }}
.om-card-value a:hover {{ color: var(--amber); }}
.drives-section {{ margin-top: 2.5rem; }}
.drives-title {{ font-size: 0.65rem; font-weight: 600; letter-spacing: 0.2em; text-transform: uppercase; color: var(--ink-dim); margin-bottom: 1rem; }}
.drives-list {{ list-style: none; display: flex; flex-direction: column; gap: 0.6rem; }}
.drives-list li {{ font-size: 0.88rem; color: var(--ink-light); display: flex; align-items: flex-start; gap: 0.8rem; line-height: 1.55; }}
.drives-list li::before {{ content: '◆'; color: var(--amber); font-size: 0.45rem; margin-top: 0.5em; flex-shrink: 0; }}

/* CV */
.role-cards {{ display: flex; flex-direction: column; gap: 1.5rem; }}
.role-card {{ background: rgba(250,248,244,0.65); backdrop-filter: blur(8px); border: 1px solid var(--border); border-radius: var(--radius); padding: 2.25rem 2.5rem; box-shadow: 0 2px 16px rgba(28,23,16,0.05), inset 0 1px 0 rgba(255,255,255,0.5); }}
.role-card-header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.75rem; flex-wrap: wrap; gap: 0.5rem; }}
.role-card-title {{ font-family: 'Lora', Georgia, serif; font-size: 1.25rem; font-weight: 500; color: var(--ink); }}
.role-card-period {{ font-size: 0.7rem; font-weight: 600; color: var(--amber); letter-spacing: 0.05em; white-space: nowrap; margin-top: 0.25rem; }}
.role-card-company {{ font-size: 0.82rem; color: var(--ink-light); margin-bottom: 0.2rem; }}
.role-card-location {{ font-size: 0.7rem; color: var(--ink-dim); margin-bottom: 0.6rem; }}
.role-card-about {{ font-size: 0.78rem; color: var(--ink-dim); font-style: italic; margin-bottom: 1rem; }}
.role-card-desc {{ font-family: 'Lora', Georgia, serif; font-style: italic; font-size: 0.88rem; color: var(--ink-light); line-height: 1.75; margin-bottom: 1.2rem; }}
.role-card-bullets {{ list-style: none; display: flex; flex-direction: column; gap: 0.45rem; }}
.role-card-bullets li {{ font-size: 0.84rem; color: var(--ink-light); padding-left: 1.2rem; position: relative; line-height: 1.55; }}
.role-card-bullets li::before {{ content: '◆'; position: absolute; left: 0; color: var(--amber); font-size: 0.4rem; top: 0.5em; }}

/* SKILLS */
.skills-section {{ margin-bottom: 3.5rem; }}
.skills-section-title {{ font-size: 0.65rem; font-weight: 600; letter-spacing: 0.2em; text-transform: uppercase; color: var(--ink-dim); margin-bottom: 1.25rem; padding-bottom: 0.6rem; border-bottom: 1px solid var(--border-light); }}
.core-skills {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 0.75rem; }}
.core-skill-card {{ background: rgba(250,248,244,0.55); backdrop-filter: blur(8px); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.3rem 1.5rem; display: flex; align-items: flex-start; gap: 1rem; box-shadow: 0 2px 12px rgba(28,23,16,0.04), inset 0 1px 0 rgba(255,255,255,0.4); }}
.core-skill-icon {{ width: 32px; height: 32px; min-width: 32px; background: var(--amber-pale); border-radius: var(--radius); display: flex; align-items: center; justify-content: center; font-size: 1rem; }}
.core-skill-name {{ font-size: 0.88rem; font-weight: 600; color: var(--ink); margin-bottom: 0.2rem; }}
.core-skill-desc {{ font-size: 0.77rem; color: var(--ink-dim); line-height: 1.5; }}
.tools-grid {{ display: flex; flex-wrap: wrap; gap: 0.5rem; }}
.tool-chip {{ background: rgba(250,248,244,0.55); backdrop-filter: blur(8px); border: 1px solid var(--border); border-radius: var(--radius); padding: 0.4rem 1rem; font-size: 0.8rem; color: var(--ink-light); box-shadow: 0 2px 12px rgba(28,23,16,0.04), inset 0 1px 0 rgba(255,255,255,0.4); }}
.highlight-box {{ background: rgba(28,23,16,0.75); backdrop-filter: blur(12px); border-radius: var(--radius); padding: 2.5rem; margin-top: 3rem; position: relative; overflow: hidden; box-shadow: 0 4px 24px rgba(28,23,16,0.15); }}
.highlight-box::before {{ content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, var(--amber), transparent); }}
.highlight-box-title {{ font-family: 'Lora', Georgia, serif; font-size: 1.25rem; font-weight: 500; color: var(--white); margin-bottom: 0.75rem; }}
.highlight-box-text {{ font-size: 0.88rem; color: rgba(242,237,228,0.65); line-height: 1.8; }}

/* EDUCATION */
.edu-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1.25rem; margin-bottom: 4rem; }}
.edu-card {{ background: rgba(250,248,244,0.55); backdrop-filter: blur(8px); border: 1px solid var(--border); border-radius: var(--radius); padding: 2.25rem; position: relative; overflow: hidden; box-shadow: 0 2px 12px rgba(28,23,16,0.04), inset 0 1px 0 rgba(255,255,255,0.4); }}
.edu-card::before {{ content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, var(--amber), transparent); }}
.edu-card-year {{ font-size: 0.65rem; font-weight: 600; letter-spacing: 0.2em; text-transform: uppercase; color: var(--amber); margin-bottom: 0.9rem; }}
.edu-card-degree {{ font-family: 'Lora', Georgia, serif; font-size: 1.15rem; font-weight: 500; color: var(--ink); line-height: 1.35; margin-bottom: 0.5rem; }}
.edu-card-school {{ font-size: 0.83rem; color: var(--ink-light); margin-bottom: 1.5rem; }}
.edu-card-desc {{ font-size: 0.84rem; color: var(--ink-dim); line-height: 1.7; }}
.edu-focus {{ background: rgba(28,23,16,0.75); backdrop-filter: blur(12px); border-radius: var(--radius); padding: 2.5rem; margin-bottom: 3rem; position: relative; overflow: hidden; box-shadow: 0 4px 24px rgba(28,23,16,0.15); }}
.edu-focus::before {{ content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, var(--amber), transparent); }}
.edu-focus-label {{ font-size: 0.65rem; font-weight: 600; letter-spacing: 0.2em; text-transform: uppercase; color: rgba(242,237,228,0.4); margin-bottom: 0.6rem; }}
.edu-focus-title {{ font-family: 'Lora', Georgia, serif; font-size: 1.4rem; font-weight: 500; color: var(--white); margin-bottom: 0.75rem; }}
.edu-focus-text {{ font-size: 0.88rem; color: rgba(242,237,228,0.65); line-height: 1.8; }}
.edu-areas-title {{ font-size: 0.65rem; font-weight: 600; letter-spacing: 0.2em; text-transform: uppercase; color: var(--ink-dim); margin-bottom: 1.1rem; padding-bottom: 0.6rem; border-bottom: 1px solid var(--border-light); }}
.edu-areas {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(210px, 1fr)); gap: 0.6rem; }}
.edu-area {{ background: rgba(250,248,244,0.55); backdrop-filter: blur(8px); border: 1px solid var(--border); border-radius: var(--radius); padding: 0.85rem 1.1rem; font-size: 0.83rem; color: var(--ink-light); display: flex; align-items: center; gap: 0.6rem; box-shadow: 0 2px 12px rgba(28,23,16,0.04), inset 0 1px 0 rgba(255,255,255,0.4); }}
.edu-area::before {{ content: '◆'; color: var(--amber); font-size: 0.4rem; flex-shrink: 0; }}

/* PERSONAL */
.personal-intro {{ font-family: 'Lora', Georgia, serif; font-size: 1.1rem; font-style: italic; line-height: 1.85; color: var(--ink-mid); margin-bottom: 3rem; max-width: 640px; }}
.personal-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1.25rem; margin-bottom: 2rem; }}
.personal-card {{ background: rgba(250,248,244,0.55); backdrop-filter: blur(8px); border: 1px solid var(--border); border-radius: var(--radius); padding: 2rem 2.25rem; box-shadow: 0 2px 12px rgba(28,23,16,0.04), inset 0 1px 0 rgba(255,255,255,0.4); }}
.personal-card-icon {{ font-size: 1.5rem; margin-bottom: 0.8rem; }}
.personal-card-title {{ font-family: 'Lora', Georgia, serif; font-size: 1.1rem; font-weight: 500; color: var(--ink); margin-bottom: 0.5rem; }}
.personal-card-text {{ font-size: 0.86rem; color: var(--ink-light); line-height: 1.75; }}
.personal-card-text a {{ color: var(--amber); text-decoration: underline; }}
.personal-highlight {{ background: rgba(28,23,16,0.75); backdrop-filter: blur(12px); border-radius: var(--radius); padding: 2.5rem; margin-top: 1.25rem; position: relative; overflow: hidden; box-shadow: 0 4px 24px rgba(28,23,16,0.15); }}
.personal-highlight::before {{ content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, var(--amber), transparent); }}
.personal-highlight-title {{ font-family: 'Lora', Georgia, serif; font-size: 1.25rem; font-weight: 500; color: var(--white); margin-bottom: 0.75rem; }}
.personal-highlight-text {{ font-size: 0.88rem; color: rgba(242,237,228,0.65); line-height: 1.8; }}
.quick-picks {{ background: rgba(250,248,244,0.55); backdrop-filter: blur(8px); border: 1px solid var(--border); border-radius: var(--radius); padding: 2rem 2.25rem; margin-top: 1.25rem; margin-bottom: 1.25rem; box-shadow: 0 2px 12px rgba(28,23,16,0.04), inset 0 1px 0 rgba(255,255,255,0.4); }}
.quick-picks-title {{ font-family: 'Lora', Georgia, serif; font-size: 1.15rem; font-weight: 500; color: var(--ink); margin-bottom: 1.25rem; }}
.quick-picks-list {{ display: flex; flex-wrap: wrap; gap: 0.75rem; }}
.quick-pick {{ display: flex; align-items: center; gap: 0.6rem; background: rgba(250,248,244,0.6); border: 1px solid var(--border); border-radius: 100px; padding: 0.5rem 1.2rem; font-size: 0.82rem; color: var(--ink-light); }}
.quick-pick-or {{ font-size: 0.65rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; color: var(--ink-dim); }}
.quick-pick-chosen {{ font-weight: 600; color: var(--amber); }}

/* CONTACT */
.kontakt-layout {{ display: grid; grid-template-columns: 1fr 360px; gap: 4rem; align-items: start; }}
.kontakt-intro {{ font-family: 'Lora', Georgia, serif; font-style: italic; font-size: 1.05rem; color: var(--ink-light); line-height: 1.85; margin-bottom: 2.5rem; }}
.kontakt-cards {{ display: flex; flex-direction: column; gap: 0.75rem; }}
.kontakt-card {{ background: rgba(250,248,244,0.55); backdrop-filter: blur(8px); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.3rem 1.6rem; display: flex; align-items: center; gap: 1.2rem; text-decoration: none; transition: border-color 0.15s; box-shadow: 0 2px 12px rgba(28,23,16,0.04), inset 0 1px 0 rgba(255,255,255,0.4); }}
.kontakt-card:hover {{ border-color: var(--amber); }}
.kontakt-card-icon {{ width: 38px; height: 38px; min-width: 38px; border-radius: var(--radius); background: var(--amber-pale); display: flex; align-items: center; justify-content: center; font-size: 1rem; }}
.kontakt-card-label {{ font-size: 0.65rem; font-weight: 600; letter-spacing: 0.18em; text-transform: uppercase; color: var(--ink-dim); margin-bottom: 0.2rem; }}
.kontakt-card-value {{ font-size: 0.92rem; font-weight: 500; color: var(--ink); }}
.kontakt-card-arrow {{ margin-left: auto; font-size: 0.9rem; color: var(--ink-dim); transition: transform 0.15s; }}
.kontakt-card:hover .kontakt-card-arrow {{ transform: translateX(3px); color: var(--amber); }}
.availability-box {{ background: rgba(28,23,16,0.75); backdrop-filter: blur(12px); border-radius: var(--radius); padding: 2rem; margin-bottom: 1rem; position: relative; overflow: hidden; box-shadow: 0 4px 24px rgba(28,23,16,0.15); }}
.availability-box::before {{ content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, var(--amber), transparent); }}
.availability-dot {{ display: inline-block; width: 7px; height: 7px; background: #6dbe8d; border-radius: 50%; margin-right: 0.45rem; }}
.availability-status {{ font-size: 0.72rem; color: rgba(242,237,228,0.45); margin-bottom: 0.7rem; }}
.availability-title {{ font-family: 'Lora', Georgia, serif; font-size: 1.15rem; font-weight: 500; color: var(--white); margin-bottom: 0.7rem; }}
.availability-text {{ font-size: 0.83rem; color: rgba(242,237,228,0.6); line-height: 1.75; }}
.info-box {{ background: rgba(250,248,244,0.55); backdrop-filter: blur(8px); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.5rem; box-shadow: 0 2px 12px rgba(28,23,16,0.04), inset 0 1px 0 rgba(255,255,255,0.4); }}
.info-box-title {{ font-size: 0.65rem; font-weight: 600; letter-spacing: 0.2em; text-transform: uppercase; color: var(--ink-dim); margin-bottom: 1rem; padding-bottom: 0.65rem; border-bottom: 1px solid var(--border-light); }}
.info-row {{ display: flex; justify-content: space-between; align-items: baseline; padding: 0.5rem 0; border-bottom: 1px solid var(--border-light); }}
.info-row:last-child {{ border-bottom: none; }}
.info-row-label {{ font-size: 0.78rem; color: var(--ink-dim); }}
.info-row-value {{ font-size: 0.82rem; color: var(--ink-light); text-align: right; }}

@media (max-width: 760px) {{ .hero-grid {{ grid-template-columns: 1fr; gap: 2.5rem; }} .hero-photo-wrap {{ max-width: 280px; }} }}
@media (max-width: 700px) {{ .om-grid {{ grid-template-columns: 1fr; }} .om-photo-wrap {{ position: static; max-width: 220px; }} .om-cards {{ grid-template-columns: 1fr; }} }}
@media (max-width: 720px) {{ .kontakt-layout {{ grid-template-columns: 1fr; }} }}
@media (max-width: 680px) {{ .page {{ padding: 84px 1.5rem 60px; }} .nav-links {{ display: none; }} footer {{ flex-direction: column; gap: 0.5rem; text-align: center; }} .role-card {{ padding: 1.5rem; }} }}
@media (max-width: 600px) {{ .edu-grid {{ grid-template-columns: 1fr; }} .core-skills {{ grid-template-columns: 1fr; }} .personal-grid {{ grid-template-columns: 1fr; }} }}
</style>
</head>
<body>
<div class="hero-bg"></div>
<nav>
  <div class="nav-inner">
    <a class="nav-logo" onclick="show('home')">Marcus <span>Hultberg</span></a>
    <ul class="nav-links">
      <li><a onclick="show('home')">Home</a></li>
      <li><a onclick="show('about')">About</a></li>
      <li><a onclick="show('cv')">CV</a></li>
      <li><a onclick="show('skills')">Skills</a></li>
      <li><a onclick="show('education')">Education</a></li>
      <li><a onclick="show('personal')">Personal</a></li>
      <li><a onclick="show('contact')">Contact</a></li>
    </ul>
  </div>
</nav>

<div class="page">

<!-- HOME -->
<div class="section active" id="sec-home">
  <div class="ai-bar">
    <div class="ai-bar-wrap">
      <input class="ai-bar-input" id="ai-input" type="text" placeholder="Ask anything about Marcus" />
      <button class="ai-bar-btn" id="ai-btn" onclick="askAI()">
        <svg viewBox="0 0 24 24" fill="none" stroke="#faf8f4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
      </button>
    </div>
    <div class="ai-bar-loading" id="ai-loading"><div class="ai-dot"></div><div class="ai-dot"></div><div class="ai-dot"></div><span>Thinking&hellip;</span></div>
    <div class="ai-bar-response" id="ai-response"><p class="ai-bar-response-label">Answer</p><p class="ai-bar-response-text" id="ai-response-text"></p></div>
  </div>
  <div class="hero">
    <div class="hero-grid">
      <div>
        <p class="hero-eyebrow">People &amp; Culture &middot; HR &middot; Recruitment</p>
        <h1 class="hero-name">Marcus<br>Hultberg</h1>
        <div class="hero-rule"><span>Gothenburg, Sweden</span></div>
        <p class="hero-subtitle">Specialist in Talent Acquisition, Learning &amp; Development and organisational development, with 7+ years of experience in technical environments.</p>
        <div class="hero-tags">
          <span class="hero-tag">Talent Acquisition</span>
          <span class="hero-tag">People &amp; Culture</span>
          <span class="hero-tag">L&amp;D</span>
          <span class="hero-tag">Employer Branding</span>
        </div>
        <div class="hero-cta">
          <a class="btn btn-primary" onclick="show('cv')">View CV</a>
          <a class="btn btn-outline" onclick="show('contact')">Get in touch</a>
        </div>
        <div class="hero-stats">
          <div class="hero-stat"><div class="hero-stat-num">7+</div><div class="hero-stat-label">Years experience</div></div>
          <div class="hero-stat"><div class="hero-stat-num">Tech</div><div class="hero-stat-label">Industry focus</div></div>
        </div>
      </div>
      <div class="hero-photo-wrap">
        <div class="hero-photo-frame">
          <div class="hero-photo-card">
            <img src="{marcus}" alt="Marcus Hultberg" />
          </div>
          <div class="hero-name-badge">
            <div class="hero-name-badge-name">Marcus Hultberg</div>
            <div class="hero-name-badge-title"><span class="hero-badge-dot"></span>People &amp; Culture &middot; Recruitment</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- ABOUT -->
<div class="section" id="sec-about">
  <div class="section-header"><p class="section-eyebrow">Background &amp; motivations</p><h1 class="section-title">About me</h1><div class="section-divider"></div></div>
  <div class="om-grid">
    <div class="om-photo-wrap"><div class="om-photo"><img src="{marcus}" alt="Marcus Hultberg" /></div></div>
    <div>
      <p class="profil-ingress">Experienced in working broadly within recruitment, HR, Learning &amp; Development and organisational development, primarily in technical environments.</p>
      <p class="profil-body">What drives me is the opportunity to work closely with people and business, and to create conditions for both individuals and organisations to grow. Through my roles I have had the chance to build and improve processes within recruitment, onboarding and competence development, always with a focus on creating a great and engaging employee experience.</p>
      <p class="profil-body">I thrive in collaboration with managers and teams, contributing with structure, perspective and support in how we can work smarter and more sustainably over time.</p>
      <div class="drives-section">
        <p class="drives-title">What I'm passionate about</p>
        <ul class="drives-list">
          <li>Matching the right person with the right role, and creating conditions for them to succeed</li>
          <li>Building structures and processes that create long-term sustainability</li>
          <li>Working closely with the business to understand its needs</li>
          <li>Creating engaging employee experiences from day one</li>
          <li>Combining data-driven thinking with a genuine focus on people</li>
        </ul>
      </div>
      <div class="om-cards">
        <div class="om-card"><p class="om-card-label">Location</p><p class="om-card-value">Gothenburg, Sweden</p></div>
        <div class="om-card"><p class="om-card-label">Focus</p><p class="om-card-value">People &amp; Culture &middot; Recruitment &middot; L&amp;D</p></div>
        <div class="om-card"><p class="om-card-label">Email</p><p class="om-card-value"><a href="mailto:marcus.hultberg@live.se">marcus.hultberg@live.se</a></p></div>
        <div class="om-card"><p class="om-card-label">Phone</p><p class="om-card-value"><a href="tel:+46703445947">0703 44 59 47</a></p></div>
      </div>
    </div>
  </div>
</div>

<!-- CV -->
<div class="section" id="sec-cv">
  <div class="section-header"><p class="section-eyebrow">Career</p><h1 class="section-title">Work experience</h1><div class="section-divider"></div></div>
  <div class="role-cards">
    <div class="role-card"><div class="role-card-header"><h2 class="role-card-title">Recruitment Consultant</h2><span class="role-card-period">June 2024 &ndash; June 2026</span></div><p class="role-card-company">Mpya Sci &amp; Tech</p><p class="role-card-location">Gothenburg</p><p class="role-card-about">Recruitment and consulting firm specialising in science, technology and engineering.</p><p class="role-card-desc">Matching the right person with the right workplace while acting as an advisor to hiring managers on competence and cultural fit.</p><ul class="role-card-bullets"><li>Drove and managed full recruitment processes from needs analysis to final placement, within technical roles</li><li>Advised managers on competence profiles, selection, process and candidate evaluation</li><li>Ensured a structured and high-quality candidate experience throughout the process</li><li>Developed and improved recruitment processes and ways of working</li><li>Worked in ATS systems to ensure quality and structure in candidate data</li><li>Wrote and published job ads based on business needs</li><li>Proactively sourced and built candidate pipelines</li></ul></div>
    <div class="role-card"><div class="role-card-header"><h2 class="role-card-title">Course Developer</h2><span class="role-card-period">Sep 2023 &ndash; June 2024</span></div><p class="role-card-company">Simployer</p><p class="role-card-location">Gothenburg</p><p class="role-card-about">Leading Nordic HR tech company providing HR systems, payroll solutions and training.</p><p class="role-card-desc">Developed and improved training content in HR, payroll, tax and VAT for a leading HR system with a strong focus on the employee experience.</p><ul class="role-card-bullets"><li>Developed and improved courses within HR and Learning &amp; Development</li><li>Ensured content was up to date and aligned with current HR trends and needs</li><li>Collaborated with subject matter experts to create relevant and high-quality training</li><li>Planned and executed conferences and training sessions focused on participant value</li><li>Improved course materials and pedagogical structures</li><li>Integrated market insights and research into training content</li></ul></div>
    <div class="role-card"><div class="role-card-header"><h2 class="role-card-title">Business Manager</h2><span class="role-card-period">April 2022 &ndash; Sep 2023</span></div><p class="role-card-company">A Society</p><p class="role-card-location">Gothenburg</p><p class="role-card-about">IT consulting firm connecting tech talent with companies across Sweden.</p><p class="role-card-desc">Responsible for recruitment and matching of IT consultants alongside ongoing HR support in a fast-moving consulting environment.</p><ul class="role-card-bullets"><li>Responsible for recruitment and matching of IT consultants</li><li>Coordinated dialogue between clients and candidates throughout the process</li><li>Worked with onboarding and ongoing HR support to consultants, including invoicing and follow-up</li><li>Developed internal onboarding structures to increase engagement and retention</li><li>Managed multiple parallel processes in a fast-changing environment</li></ul></div>
    <div class="role-card"><div class="role-card-header"><h2 class="role-card-title">Talent Acquisition Lead / Consultant Manager</h2><span class="role-card-period">Nov 2020 &ndash; April 2022</span></div><p class="role-card-company">ZoCom</p><p class="role-card-location">Gothenburg</p><p class="role-card-about">Fast-growing IT consulting company focused on web development and digital solutions.</p><p class="role-card-desc">Part of the management team with full responsibility for talent acquisition and a consultant group of 15+ people in a high-growth IT company.</p><ul class="role-card-bullets"><li>Led and developed the company's talent acquisition work</li><li>Worked with employer branding and improvement of internal processes</li><li>Implemented and developed ATS workflows</li><li>Managed full recruitment processes from start to onboarding</li><li>HR support and development for a consultant group of 15+ people</li><li>Developed and implemented onboarding structure for new employees</li><li>Created and ran internal workshops and training initiatives</li><li>Initiated and built a career programme for junior talent</li><li>Contributed to organisational development by establishing an internal LMS that was later sold B2B</li></ul></div>
    <div class="role-card"><div class="role-card-header"><h2 class="role-card-title">Education Manager / ICT Manager</h2><span class="role-card-period">June 2019 &ndash; Oct 2020</span></div><p class="role-card-company">IT-H&ouml;gskolan</p><p class="role-card-location">Gothenburg</p><p class="role-card-about">One of Sweden's largest providers of vocational higher education within IT and tech.</p><p class="role-card-desc">Led education programmes at one of Sweden's largest vocational IT schools and supported students in their transition into the tech industry.</p><ul class="role-card-bullets"><li>Led and developed education programmes in close collaboration with the labour market</li><li>Coached and guided students in their career journey into the IT industry</li><li>Worked with competence supply by matching education to market needs</li><li>Participated in recruiting teachers and ensured relevant competence</li><li>Built and maintained partnerships with companies and external stakeholders</li><li>Secured internship placements and supported students in transitioning to working life</li><li>Improved internal communication flows and developed LMS structure</li></ul></div>
    <div class="role-card"><div class="role-card-header"><h2 class="role-card-title">First Line Support / Store Sales</h2><span class="role-card-period">May 2013 &ndash; Aug 2018</span></div><p class="role-card-company">Telia Company</p><p class="role-card-location">Gothenburg / Ume&aring;</p><p class="role-card-about">Sweden's largest telecom operator, providing mobile, broadband and TV services.</p><p class="role-card-desc">Full-time for three years and part-time for two years at Sweden's largest telecom provider, with a focus on customer service and internal employee support.</p><ul class="role-card-bullets"><li>Supported onboarding of new employees through coaching and participating in recruitment</li><li>Contributed to improved knowledge sharing and working methods in support</li><li>Worked with customer service via phone, chat and email</li><li>Developed strong communication and problem-solving skills</li></ul></div>
  </div>
</div>

<!-- SKILLS -->
<div class="section" id="sec-skills">
  <div class="section-header"><p class="section-eyebrow">What I bring</p><h1 class="section-title">Skills</h1><div class="section-divider"></div></div>
  <div class="skills-section">
    <p class="skills-section-title">Core competencies</p>
    <div class="core-skills">
      <div class="core-skill-card"><div class="core-skill-icon">&#127919;</div><div><p class="core-skill-name">Talent Acquisition</p><p class="core-skill-desc">Full recruitment process: from needs analysis and sourcing to offer and onboarding</p></div></div>
      <div class="core-skill-card"><div class="core-skill-icon">&#129309;</div><div><p class="core-skill-name">People &amp; Culture</p><p class="core-skill-desc">Employee experience, engagement, culture and HR processes in technical environments</p></div></div>
      <div class="core-skill-card"><div class="core-skill-icon">&#128218;</div><div><p class="core-skill-name">Learning &amp; Development</p><p class="core-skill-desc">Course development, education management, LMS and competence development programmes</p></div></div>
      <div class="core-skill-card"><div class="core-skill-icon">&#128188;</div><div><p class="core-skill-name">HR</p><p class="core-skill-desc">Personnel matters, onboarding, retention and support to managers and employees</p></div></div>
      <div class="core-skill-card"><div class="core-skill-icon">&#10024;</div><div><p class="core-skill-name">Employer Branding</p><p class="core-skill-desc">Building and communicating employer brand to attract the right talent</p></div></div>
      <div class="core-skill-card"><div class="core-skill-icon">&#128203;</div><div><p class="core-skill-name">Project Management</p><p class="core-skill-desc">Driving parallel processes, structuring work and delivering in fast-changing environments</p></div></div>
      <div class="core-skill-card"><div class="core-skill-icon">&#127959;&#65039;</div><div><p class="core-skill-name">Organisational Development</p><p class="core-skill-desc">Building structures, processes and programmes that create long-term sustainability</p></div></div>
      <div class="core-skill-card"><div class="core-skill-icon">&#127760;</div><div><p class="core-skill-name">Stakeholder Management</p><p class="core-skill-desc">Advisory collaboration with managers, leadership and external stakeholders</p></div></div>
      <div class="core-skill-card"><div class="core-skill-icon">&#128172;</div><div><p class="core-skill-name">Communication</p><p class="core-skill-desc">Clear and adapted communication in candidate meetings, workshops and conferences</p></div></div>
      <div class="core-skill-card"><div class="core-skill-icon">&#129302;</div><div><p class="core-skill-name">AI Tools</p><p class="core-skill-desc">Practical experience using ChatGPT and Claude to enhance productivity and work quality</p></div></div>
    </div>
  </div>
  <div class="skills-section">
    <p class="skills-section-title">Systems &amp; tools</p>
    <div class="tools-grid">
      <span class="tool-chip">Teamtailor</span><span class="tool-chip">Workbuster</span><span class="tool-chip">Slack</span><span class="tool-chip">Notion</span><span class="tool-chip">Google Workspace</span><span class="tool-chip">LinkedIn Recruiter</span><span class="tool-chip">ChatGPT</span><span class="tool-chip">Claude</span>
    </div>
  </div>
  <div class="highlight-box">
    <h2 class="highlight-box-title">Technical environments as home turf</h2>
    <p class="highlight-box-text">The majority of my career has been spent in IT and tech companies, which means I understand the language, needs and challenges of the business. This creates better recruitment processes, more accurate competence profiles and stronger trust from both candidates and hiring managers.</p>
  </div>
</div>

<!-- EDUCATION -->
<div class="section" id="sec-education">
  <div class="section-header"><p class="section-eyebrow">Academic background</p><h1 class="section-title">Education</h1><div class="section-divider"></div></div>
  <div class="edu-grid">
    <div class="edu-card"><p class="edu-card-year">2016 &ndash; 2019</p><h2 class="edu-card-degree">BSc. Behavioural Science with focus on IT environments</h2><p class="edu-card-school">Ume&aring; University</p><p class="edu-card-desc">Bachelor's degree focused on human behaviour in digital and technical organisations: a solid foundation for People &amp; Culture work in the tech industry.</p></div>
    <div class="edu-card"><p class="edu-card-year">2020</p><h2 class="edu-card-degree">Certified Education Manager</h2><p class="edu-card-school">Myndigheten f&ouml;r Yrkesh&ouml;gskolan</p><p class="edu-card-desc">Certification in education management focused on vocational higher education, directly applicable in L&amp;D roles with emphasis on pedagogical planning and course design.</p></div>
  </div>
  <div class="edu-focus"><p class="edu-focus-label">The core of the education</p><h2 class="edu-focus-title">Behavioural science meets technical environments</h2><p class="edu-focus-text">The combination of behavioural science and an IT perspective provides a unique understanding of how people function in modern, fast-changing organisations, and the ability to bridge the gap between HR and the business.</p></div>
  <div><p class="edu-areas-title">Relevant knowledge areas</p><div class="edu-areas"><div class="edu-area">Organisational psychology</div><div class="edu-area">Pedagogy &amp; didactics</div><div class="edu-area">Recruitment &amp; selection</div><div class="edu-area">Group dynamics</div><div class="edu-area">Employment law basics</div><div class="edu-area">Leadership &amp; coaching</div><div class="edu-area">Quality assurance</div><div class="edu-area">Competence supply</div></div></div>
</div>

<!-- PERSONAL -->
<div class="section" id="sec-personal">
  <div class="section-header"><p class="section-eyebrow">Beyond work</p><h1 class="section-title">Personal</h1><div class="section-divider"></div></div>
  <p class="personal-intro">There's more to life than work. Here's a glimpse of who I am outside the office: the things that keep me curious, grounded and energised.</p>
  <div class="personal-grid">
    <div class="personal-card"><div class="personal-card-icon">&#127922;</div><h2 class="personal-card-title">Hobbies</h2><p class="personal-card-text">I'm a creative person at heart. I read a lot of fantasy and channel that into writing D&amp;D adventures as a Game Master. I have a huge passion for food and cooking, and love all food, from street food joints to Michelin restaurants. I also really enjoy getting together over board games, and love watching Critical Role, a live-action D&amp;D series that fuels my creativity as a Game Master.</p></div>
    <div class="personal-card"><div class="personal-card-icon">&#9992;&#65039;</div><h2 class="personal-card-title">Travel</h2><p class="personal-card-text">I love to travel, especially to Spain and Costa del Sol. I also grew up half and half in Thailand, and I've even been stuck on the African savannah. Ask me about it!</p></div>
    <div class="personal-card"><div class="personal-card-icon">&#128104;&#8205;&#128105;&#8205;&#128103;&#8205;&#128102;</div><h2 class="personal-card-title">Friends &amp; family</h2><p class="personal-card-text">I live in Gothenburg with my fianc&eacute;e and our 2.5-year-old son. Time with the people I care about is what matters most: good conversations, dinners and shared experiences.</p></div>
    <div class="personal-card"><div class="personal-card-icon">&#127911;</div><h2 class="personal-card-title">Music &amp; podcasts</h2><p class="personal-card-text">I'm a music omnivore, always listening to something. Right now I'm stuck on funk soul. Check out <a href="https://open.spotify.com/track/2XW7ow6JU8wPGWwKBw5a5a?si=f484c2111e4a4f32" target="_blank" rel="noopener">Beirut by Wanda Wonderful</a>. I definitely prefer music over podcasts.</p></div>
    <div class="personal-card"><div class="personal-card-icon">&#128214;</div><h2 class="personal-card-title">Curiosity &amp; learning</h2><p class="personal-card-text">I love reading and watching videos to learn new things, especially about AI and how to streamline and optimise the way we work. Being creative in my work is something that genuinely makes me feel good.</p></div>
  </div>
  <div class="quick-picks">
    <h2 class="quick-picks-title">My quick picks</h2>
    <div class="quick-picks-list">
      <div class="quick-pick">&#127828; <span class="quick-pick-chosen">Burger</span> <span class="quick-pick-or">or</span> Pizza</div>
      <div class="quick-pick">&#127863; <span class="quick-pick-chosen">Wine</span> <span class="quick-pick-or">or</span> Beer</div>
      <div class="quick-pick">&#127956;&#65039; Mountains <span class="quick-pick-or">or</span> <span class="quick-pick-chosen">Beach</span></div>
      <div class="quick-pick">&#127749; Morning <span class="quick-pick-or">or</span> <span class="quick-pick-chosen">Night</span></div>
      <div class="quick-pick">&#127916; <span class="quick-pick-chosen">Series</span> <span class="quick-pick-or">or</span> Movie</div>
      <div class="quick-pick">&#128172; <span class="quick-pick-chosen">Slack</span> <span class="quick-pick-or">or</span> Teams</div>
      <div class="quick-pick">&#128241; <span class="quick-pick-chosen">iPhone</span> <span class="quick-pick-or">or</span> Android</div>
      <div class="quick-pick">&#127798;&#65039; <span class="quick-pick-chosen">Spicy</span> <span class="quick-pick-or">or</span> Mild</div>
      <div class="quick-pick">&#129464; <span class="quick-pick-chosen">Marvel</span> <span class="quick-pick-or">or</span> Star Wars</div>
      <div class="quick-pick">&#129302; ChatGPT <span class="quick-pick-or">or</span> <span class="quick-pick-chosen">Claude</span></div>
    </div>
  </div>
  <div class="personal-highlight"><h2 class="personal-highlight-title">What drives me</h2><p class="personal-highlight-text">At the core, I'm someone who genuinely cares about people. Whether it's at work or in my personal life, I believe in building real connections, staying curious and always trying to grow. The best version of me shows up when I balance meaningful work with the things and people that inspire me outside of it.</p></div>
</div>

<!-- CONTACT -->
<div class="section" id="sec-contact">
  <div class="section-header"><p class="section-eyebrow">Reach me</p><h1 class="section-title">Contact</h1><div class="section-divider"></div></div>
  <div class="kontakt-layout">
    <div>
      <p class="kontakt-intro">Want to learn more about my background, discuss an opportunity or just have a conversation? Feel free to reach out.</p>
      <div class="kontakt-cards">
        <a href="mailto:marcus.hultberg@live.se" class="kontakt-card"><div class="kontakt-card-icon">&#9993;&#65039;</div><div><p class="kontakt-card-label">Email</p><p class="kontakt-card-value">marcus.hultberg@live.se</p></div><span class="kontakt-card-arrow">&rarr;</span></a>
        <a href="tel:+46703445947" class="kontakt-card"><div class="kontakt-card-icon">&#128222;</div><div><p class="kontakt-card-label">Phone</p><p class="kontakt-card-value">0703 44 59 47</p></div><span class="kontakt-card-arrow">&rarr;</span></a>
        <div class="kontakt-card" style="cursor:default;"><div class="kontakt-card-icon">&#128205;</div><div><p class="kontakt-card-label">Address</p><p class="kontakt-card-value">Hed&aring;sgatan 10, 412 53 Gothenburg</p></div></div>
        <a href="https://www.linkedin.com/in/marcus-hultberg-505b386a/" target="_blank" rel="noopener" class="kontakt-card"><div class="kontakt-card-icon">&#128188;</div><div><p class="kontakt-card-label">LinkedIn</p><p class="kontakt-card-value">Marcus Hultberg</p></div><span class="kontakt-card-arrow">&rarr;</span></a>
      </div>
    </div>
    <div>
      <div class="availability-box"><p class="availability-status"><span class="availability-dot"></span>Available for conversations</p><h2 class="availability-title">Open to new opportunities</h2><p class="availability-text">I'm always interested in hearing about exciting roles within People &amp; Culture, Talent Acquisition and Learning &amp; Development, especially in technical environments.</p></div>
      <div class="info-box"><p class="info-box-title">Quick facts</p><div class="info-row"><span class="info-row-label">Location</span><span class="info-row-value">Gothenburg</span></div><div class="info-row"><span class="info-row-label">Experience</span><span class="info-row-value">7+ years</span></div><div class="info-row"><span class="info-row-label">Focus</span><span class="info-row-value">People &amp; Culture &middot; HR</span></div><div class="info-row"><span class="info-row-label">Industry</span><span class="info-row-value">Tech &amp; IT</span></div><div class="info-row"><span class="info-row-label">Education</span><span class="info-row-value">BSc. Behavioural Science</span></div></div>
    </div>
  </div>
</div>

</div>

<footer>
  <p>&copy; 2026 Marcus Hultberg</p>
  <a onclick="show('contact')">Get in touch &rarr;</a>
</footer>

<script>
function show(id) {{
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  document.getElementById('sec-' + id).classList.add('active');
  document.querySelectorAll('.nav-links a').forEach(a => {{
    a.classList.toggle('active', a.textContent.trim().toLowerCase() === id || (id === 'cv' && a.textContent.trim() === 'CV'));
  }});
  window.scrollTo(0, 0);
}}

const aiInput = document.getElementById('ai-input');
const aiBtn = document.getElementById('ai-btn');
const aiLoading = document.getElementById('ai-loading');
const aiResponse = document.getElementById('ai-response');
const aiResponseText = document.getElementById('ai-response-text');
aiInput.addEventListener('keydown', e => {{ if (e.key === 'Enter') askAI(); }});

async function askAI(question) {{
  const q = question || aiInput.value.trim();
  if (!q) return;
  aiInput.value = q;
  aiBtn.disabled = true;
  aiLoading.classList.add('visible');
  aiResponse.classList.remove('visible');
  try {{
    const res = await fetch('https://cv-page-mocha.vercel.app/api/ask', {{
      method: 'POST',
      headers: {{ 'Content-Type': 'application/json' }},
      body: JSON.stringify({{ question: q }})
    }});
    const data = await res.json();
    if (data.answer) {{
      aiResponseText.textContent = data.answer;
      aiResponse.classList.add('visible');
    }} else {{
      aiResponseText.textContent = data.error || 'Something went wrong. Please try again.';
      aiResponse.classList.add('visible');
    }}
  }} catch (e) {{
    aiResponseText.textContent = 'Could not reach the server. Please try again later.';
    aiResponse.classList.add('visible');
  }} finally {{
    aiBtn.disabled = false;
    aiLoading.classList.remove('visible');
  }}
}}
</script>
</body>
</html>'''

(root / "marcus-hultberg-cv.html").write_text(html, encoding="utf-8")
print(f"Done! File size: {len(html):,} bytes ({len(html)/1024/1024:.1f} MB)")
