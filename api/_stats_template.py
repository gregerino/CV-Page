# The stats dashboard page. stats.py swaps the DATA placeholder for the JSON it
# gathers; everything else is drawn in the browser.
TEMPLATE = r"""<!DOCTYPE html>
<html lang="sv">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex">
<title>Statistik · Marcus Hultberg</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Work+Sans:wght@400;500;600;700&family=Fira+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#f4f0ff; --surface:#ffffff; --surface2:#f8f5ff; --line:#e6dff7; --line2:#d8cdf2;
  --ink:#0c051d; --ink2:#463f58; --muted:#6a6380;
  --accent:#6b2fd1; --accent-soft:rgba(107,47,209,.12); --accent2:#bb8af7;
  --good:#1f7a4d; --good-soft:rgba(31,122,77,.12); --bad:#b3261e;
  --shadow:0 1px 3px rgba(12,5,29,.06),0 8px 24px rgba(12,5,29,.05);
  --r:14px; --sans:'Work Sans',system-ui,sans-serif; --mono:'Fira Mono',ui-monospace,monospace;
}
@media (prefers-color-scheme:dark){:root{
  --bg:#0d0718; --surface:#171024; --surface2:#1e162e; --line:#2a2140; --line2:#3a2f55;
  --ink:#f4f0ff; --ink2:#cfc7e3; --muted:#9a91b3;
  --accent:#bb8af7; --accent-soft:rgba(187,138,247,.16); --accent2:#7c4ad8;
  --good:#5fd39a; --good-soft:rgba(95,211,154,.14); --bad:#ff8a80;
  --shadow:0 1px 2px rgba(0,0,0,.4);
}}
*{box-sizing:border-box;margin:0;padding:0}
html{-webkit-text-size-adjust:100%}
body{background:var(--bg);color:var(--ink);font-family:var(--sans);font-size:15px;line-height:1.45;padding:28px 16px 48px}
button,input,select{font:inherit;color:inherit}
a{color:inherit}
.wrap{max-width:1200px;margin:0 auto}
.num{font-variant-numeric:tabular-nums}
.mono{font-family:var(--mono)}

/* header */
header{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:16px;margin-bottom:24px}
.eyebrow{font-size:.7rem;font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:var(--accent)}
h1{font-size:1.9rem;font-weight:700;letter-spacing:-.02em;line-height:1.1;margin-top:4px}
.sub{color:var(--muted);font-size:.85rem;margin-top:4px}
.controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.seg{display:inline-flex;background:var(--surface);border:1px solid var(--line);border-radius:999px;padding:3px}
.seg button{border:0;background:none;padding:6px 14px;border-radius:999px;cursor:pointer;font-size:.85rem;font-weight:500;color:var(--ink2)}
.seg button[aria-pressed=true]{background:var(--accent);color:#fff}
@media (prefers-color-scheme:dark){.seg button[aria-pressed=true]{color:#0d0718}}
.os-sel{border:1px solid var(--line);background:var(--surface);border-radius:999px;padding:7px 12px;font-size:.85rem;color:var(--ink2);cursor:pointer}
.os-sel.on{border-color:var(--accent);color:var(--accent);background:var(--accent-soft);font-weight:600}
.osbar{display:flex;flex-wrap:wrap;gap:8px 12px;align-items:center;background:var(--accent-soft);color:var(--ink);border-radius:10px;padding:10px 14px;margin-bottom:16px;font-size:.88rem}
.osbar button{border:0;background:none;color:var(--accent);font-weight:600;cursor:pointer;text-decoration:underline}
#oss .hbars li{cursor:pointer;border-radius:6px}
#oss .hbars li:hover .n{color:var(--accent)}
#oss .hbars li.sel .n{color:var(--accent);font-weight:600}
.icon-btn{border:1px solid var(--line);background:var(--surface);border-radius:999px;padding:7px 12px;cursor:pointer;font-size:.85rem;color:var(--ink2)}
.icon-btn:hover{border-color:var(--line2)}

/* cards */
.card{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);box-shadow:var(--shadow)}
.card-h{display:flex;align-items:baseline;justify-content:space-between;gap:12px;padding:18px 20px 0}
.card-h h2{font-size:.95rem;font-weight:600}
.card-h .hint{font-size:.78rem;color:var(--muted)}
.card-b{padding:14px 20px 20px}

/* kpis */
.kpis{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-bottom:16px}
.kpi{padding:16px 18px}
.kpi .l{font-size:.72rem;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.kpi .v{font-size:1.9rem;font-weight:700;letter-spacing:-.02em;margin-top:6px;line-height:1}
.kpi .d{font-size:.78rem;color:var(--muted);margin-top:8px;display:flex;gap:6px;align-items:center;flex-wrap:wrap}
.delta{font-weight:600;padding:1px 7px;border-radius:999px;font-size:.74rem}
.delta.up{color:var(--good);background:var(--good-soft)}
.delta.down{color:var(--bad);background:rgba(179,38,30,.1)}
.delta.flat{color:var(--muted);background:var(--surface2)}
@media (max-width:980px){.kpis{grid-template-columns:repeat(3,1fr)}}
@media (max-width:560px){.kpis{grid-template-columns:repeat(2,1fr)}.kpi .v{font-size:1.6rem}}

/* chart */
.chart{position:relative;width:100%}
.chart svg{display:block;width:100%;overflow:visible}
.axis text{fill:var(--muted);font-size:11px;font-family:var(--sans)}
.grid line{stroke:var(--line);stroke-width:1}
.bar{fill:var(--accent)}
.bar.dim{opacity:.35}
.hit{fill:transparent;cursor:crosshair}
.tip{position:absolute;pointer-events:none;background:var(--ink);color:var(--bg);padding:7px 10px;border-radius:8px;font-size:.78rem;white-space:nowrap;transform:translate(-50%,-100%);opacity:0;transition:opacity .1s;z-index:5}
.tip b{font-weight:600}
.tip .s{opacity:.75}

/* layout */
.cols{display:grid;grid-template-columns:minmax(0,1fr) 340px;gap:16px;margin-top:16px;align-items:start}
.side{display:grid;gap:16px}
@media (max-width:980px){.cols{grid-template-columns:1fr}}

/* pages */
.toolbar{display:flex;flex-wrap:wrap;gap:10px;align-items:center;justify-content:space-between;padding:16px 20px;border-bottom:1px solid var(--line)}
.tabs{display:flex;gap:4px;flex-wrap:wrap}
.tabs button{border:0;background:none;padding:6px 10px;border-radius:8px;cursor:pointer;font-size:.85rem;font-weight:500;color:var(--muted)}
.tabs button[aria-selected=true]{background:var(--accent-soft);color:var(--accent)}
.tabs .c{font-size:.75rem;opacity:.8;margin-left:3px}
.filters{display:flex;gap:8px;flex-wrap:wrap}
.filters input,.filters select{border:1px solid var(--line);background:var(--surface2);border-radius:8px;padding:6px 10px;font-size:.85rem}
.filters input[type=search]{width:180px}
.filters input:focus,.filters select:focus{outline:2px solid var(--accent-soft);border-color:var(--accent)}
.rows{list-style:none}
.row{display:grid;grid-template-columns:minmax(0,1fr) 128px 74px 70px 60px 120px;gap:14px;align-items:center;padding:12px 20px;border-bottom:1px solid var(--line);cursor:pointer;transition:background .1s}
.row:last-child{border-bottom:0}
.row:hover,.row:focus-visible{background:var(--surface2);outline:none}
.row.head{cursor:default;padding-top:10px;padding-bottom:8px;font-size:.7rem;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.row.head:hover{background:none}
.row .r{text-align:right}
.name{min-width:0}
.name .t{font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;display:flex;align-items:center;gap:8px}
.name .s{font-size:.8rem;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.name .s .mono{color:var(--ink2)}
.live{width:8px;height:8px;border-radius:50%;background:var(--good);box-shadow:0 0 0 3px var(--good-soft);flex:none}
.chip{font-size:.7rem;font-weight:600;padding:2px 8px;border-radius:999px;background:var(--surface2);color:var(--muted);border:1px solid var(--line);flex:none}
.chip.new{background:var(--good-soft);color:var(--good);border-color:transparent}
.big{font-weight:600;font-size:1rem}
.when{font-size:.82rem;color:var(--ink2);text-align:right}
.when.never{color:var(--muted)}
.spark{display:block;width:128px;height:30px;overflow:visible}
.spark path.l{fill:none;stroke:var(--accent);stroke-width:2;stroke-linejoin:round;stroke-linecap:round}
.spark path.a{fill:var(--accent-soft)}
.spark circle{fill:var(--accent)}
.spark .zero{stroke:var(--line2);stroke-width:2;stroke-dasharray:2 4}
.trend{display:block;font-size:.72rem;font-weight:600;margin-top:2px}
.trend.up{color:var(--good)}
.trend.down{color:var(--bad)}
.tog{display:inline-flex;align-items:center;gap:6px;font-size:.85rem;color:var(--ink2);border:1px solid var(--line);background:var(--surface2);border-radius:8px;padding:5px 10px;cursor:pointer;user-select:none}
.tog input{accent-color:var(--accent)}
.visits{list-style:none;display:grid}
.visits li{padding:12px 0;border-bottom:1px solid var(--line);display:grid;gap:5px;font-size:.85rem}
.visits li:last-child{border-bottom:0}
.visits li[data-slug]{cursor:pointer}
.visits li[data-slug]:hover .vp{color:var(--accent)}
.vh{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}
.vt{color:var(--muted);font-size:.8rem;min-width:92px}
.vp{font-weight:600}
.vd{font-weight:600;background:var(--accent-soft);color:var(--accent);border-radius:999px;padding:0 8px;font-size:.78rem}
.vr{display:flex;gap:10px;align-items:baseline;min-width:0}
.vr .k{color:var(--muted);font-size:.74rem;text-transform:uppercase;letter-spacing:.06em;min-width:72px;flex:none}
.vr a{color:var(--accent);word-break:break-all}
.cls{display:flex;flex-wrap:wrap;gap:4px}
.cl{font-size:.76rem;background:var(--surface2);border:1px solid var(--line);border-radius:6px;padding:1px 7px}
.wide{margin-top:16px}
.wide .visits{max-height:560px;overflow:auto;padding-right:6px}
.dur{white-space:nowrap}
.empty{padding:32px 20px;text-align:center;color:var(--muted);font-size:.9rem}
@media (max-width:720px){
  .row{grid-template-columns:minmax(0,1fr) auto;gap:4px 12px}
  .row.head{display:none}
  .row .sp,.row .tot,.row .dur{display:none}
  .row .rv{grid-column:2;grid-row:1}
  .row .when{grid-column:1/-1;text-align:left;font-size:.78rem}
  .filters input[type=search]{width:100%}
  .filters{width:100%}
}

/* side lists */
.hbars{list-style:none;display:grid;gap:10px}
.hbars li{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:4px 10px;font-size:.86rem}
.hbars .n{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.hbars .track{grid-column:1/-1;height:6px;border-radius:3px;background:var(--surface2);overflow:hidden}
.hbars .fill{height:100%;background:var(--accent);border-radius:3px}
.split{display:flex;height:10px;border-radius:5px;overflow:hidden;gap:2px;margin:6px 0 12px}
.split div:first-child{background:var(--accent)}
.split div:last-child{background:var(--accent2)}
.legend{display:flex;gap:16px;font-size:.84rem;flex-wrap:wrap}
.legend span{display:inline-flex;align-items:center;gap:6px}
.legend i{width:10px;height:10px;border-radius:3px;display:inline-block}
.qs{list-style:none;display:grid;gap:10px;max-height:340px;overflow:auto}
.qs li{font-size:.86rem;border-left:2px solid var(--line2);padding-left:10px}
.qs .tm{font-size:.74rem;color:var(--muted);margin-top:2px}
.muted{color:var(--muted);font-size:.85rem}

/* drawer */
dialog{border:0;padding:0;margin:0 0 0 auto;height:100%;max-height:100%;width:min(560px,100%);background:var(--surface);color:var(--ink);box-shadow:-20px 0 60px rgba(12,5,29,.25)}
dialog::backdrop{background:rgba(12,5,29,.35)}
dialog[open]{animation:slide .18s ease-out}
@keyframes slide{from{transform:translateX(30px);opacity:0}}
.dw{padding:24px;display:grid;gap:20px}
.dw-h{display:flex;justify-content:space-between;gap:12px;align-items:flex-start}
.dw-h h3{font-size:1.35rem;font-weight:700;letter-spacing:-.01em;line-height:1.2}
.dw-h .s{color:var(--muted);font-size:.85rem;margin-top:4px}
.close{border:1px solid var(--line);background:var(--surface2);border-radius:999px;width:34px;height:34px;cursor:pointer;flex:none;font-size:1.1rem}
.mini{display:grid;grid-template-columns:repeat(auto-fit,minmax(92px,1fr));gap:8px}
.mini div{background:var(--surface2);border-radius:10px;padding:10px 12px}
.mini .l{font-size:.68rem;color:var(--muted);font-weight:600;text-transform:uppercase;letter-spacing:.06em}
.mini .v{font-size:1.25rem;font-weight:700;margin-top:2px}
@media (max-width:480px){.mini{grid-template-columns:repeat(2,1fr)}}
.dw h4{font-size:.8rem;font-weight:600;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin-bottom:10px}
.open-link{display:inline-flex;align-items:center;gap:6px;font-size:.85rem;font-weight:600;color:var(--accent);text-decoration:none}
.open-link:hover{text-decoration:underline}

footer{margin-top:24px;color:var(--muted);font-size:.8rem;display:flex;flex-wrap:wrap;gap:8px 16px;justify-content:space-between}
footer button{background:none;border:0;color:var(--accent);cursor:pointer;font-size:.8rem;text-decoration:underline}
.warn{background:rgba(179,38,30,.08);border:1px solid rgba(179,38,30,.25);color:var(--bad);padding:12px 16px;border-radius:10px;margin-bottom:16px;font-size:.88rem}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div>
      <p class="eyebrow">Privat statistik</p>
      <h1>Mina sidor</h1>
      <p class="sub" id="sub"></p>
    </div>
    <div class="controls">
      <div class="seg" role="group" aria-label="Vems besök" id="who">
        <button data-w="visitors">Besökare</button><button data-w="me">Mina besök</button>
      </div>
      <div class="seg" role="group" aria-label="Period" id="range">
        <button data-r="7">7 dagar</button><button data-r="30">30 dagar</button><button data-r="90">90 dagar</button>
      </div>
      <select id="os" class="os-sel" aria-label="Operativsystem">
        <option value="">Alla system</option>
        <option>Windows</option><option>macOS</option><option>Linux</option>
        <option>iOS</option><option>Android</option><option>ChromeOS</option><option>Annat</option>
      </select>
      <button class="icon-btn" onclick="location.reload()" title="Hämta ny data">↻ Uppdatera</button>
    </div>
  </header>

  <div id="warn"></div>
  <div id="mebar"></div>
  <div id="osbar"></div>
  <section class="kpis" id="kpis"></section>

  <section class="card">
    <div class="card-h"><h2 id="chart-title">Visningar per dag</h2><span class="hint" id="chart-hint"></span></div>
    <div class="card-b"><div class="chart" id="chart"></div></div>
  </section>

  <div class="cols">
    <section class="card" aria-label="Sidor">
      <div class="toolbar">
        <div class="tabs" role="tablist" id="tabs"></div>
        <div class="filters">
          <input type="search" id="q" placeholder="Sök företag eller sida…" aria-label="Sök">
          <select id="sort" aria-label="Sortera">
            <option value="last">Senast besökt</option>
            <option value="rising">Ökar mest</option>
            <option value="range">Flest visningar i perioden</option>
            <option value="time">Längst besökstid</option>
            <option value="total">Flest visningar totalt</option>
            <option value="name">Namn A–Ö</option>
          </select>
          <label class="tog"><input type="checkbox" id="rising"> Bara ökande</label>
        </div>
      </div>
      <ul class="rows" id="rows"></ul>
    </section>

    <aside class="side">
      <section class="card"><div class="card-h"><h2>Trafikkällor</h2><span class="hint">sedan start</span></div><div class="card-b" id="refs"></div></section>
      <section class="card"><div class="card-h"><h2>Operativsystem</h2><span class="hint">klicka för att filtrera</span></div><div class="card-b" id="oss"></div></section>
      <section class="card"><div class="card-h"><h2>Enheter</h2><span class="hint">sedan start</span></div><div class="card-b" id="devs"></div></section>
      <section class="card"><div class="card-h"><h2>AI-frågor</h2><span class="hint" id="ai-hint"></span></div><div class="card-b" id="qs"></div></section>
      <section class="card"><div class="card-h"><h2>Bortfiltrerade botar</h2><span class="hint" id="bot-hint"></span></div><div class="card-b" id="bots"></div></section>
      <section class="card"><div class="card-h"><h2>Klick i menyn</h2><span class="hint">sedan start</span></div><div class="card-b" id="clicks"></div></section>
    </aside>
  </div>

  <section class="card wide">
    <div class="card-h"><h2 id="recent-title">Senaste besöken</h2>
      <label class="tog"><input type="checkbox" id="hideshort"> Dölj besök under 5 s</label></div>
    <div class="card-b" id="recent"></div>
  </section>

  <footer><span id="own"></span><span id="gen"></span></footer>
</div>

<dialog id="dw" aria-labelledby="dw-title"><div class="dw" id="dw-body"></div></dialog>

<script>
const D = /*__DATA__*/null;
const $ = s => document.querySelector(s);
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fmt = n => n.toLocaleString('sv-SE');
const sum = a => a.reduce((x, y) => x + y, 0);
const store = (fn) => { try { return fn(localStorage); } catch (e) { return null; } };
const N = D.dates.length;
const MONTHS = ['jan','feb','mar','apr','maj','jun','jul','aug','sep','okt','nov','dec'];
const dayLabel = iso => { const [y, m, d] = iso.split('-'); return +d + ' ' + MONTHS[+m - 1]; };
const WEEKDAYS = ['sön','mån','tis','ons','tor','fre','lör'];
const weekday = iso => WEEKDAYS[new Date(iso + 'T12:00:00Z').getUTCDay()];

let R = +(store(s => s.getItem('stats-range')) || 30);
if (![7, 30, 90].includes(R)) R = 30;
let TAB = store(s => s.getItem('stats-tab')) || 'pack';
let SORT = store(s => s.getItem('stats-sort')) || 'last';
let RISING = store(s => s.getItem('stats-rising')) === '1';
let OS = store(s => s.getItem('stats-os')) || '';
let ME = store(s => s.getItem('stats-who')) === 'me';

// Everything below reads a page through these, so one switch flips the whole
// dashboard between visitors and Marcus's own visits.
const dl = p => ME ? (p.ownDaily || []) : p.daily;
const tot = p => ME ? (p.ownTotal || 0) : p.total;
const lastISO = p => ME ? p.ownLast : p.last;
const lastIdxOf = p => ME ? p.ownLastIdx : p.lastIdx;
const visitsOf = p => ME ? (D.ownVisits || []).filter(v => v.page === p.slug) : (p.visits || []);
const siteDaily = () => ME ? (D.ownDaily || []) : D.daily;
const osViews = p => OS && !ME ? (p.os || {})[OS] || 0 : tot(p);

// Opening the dashboard proves it's you: from now on this browser's visits on
// this domain are recorded as yours, under "Mina besök", not as visitors.
store(s => s.setItem('cv-notrack', '1'));

/* ---------- derived page data ---------- */
const BASE_NAMES = {'home':'Startsidan', 'index.html':'Startsidan (index.html)', 'cv.html':'CV-sidan', 'other':'Okända sökvägar'};
const v2idx = D.v2since ? D.dates.indexOf(D.v2since) : -1;

function groupOf(p) {
  if (p.pack) return 'pack';
  if (p.slug === 'home' || p.slug.endsWith('.html')) return 'base';
  return 'other';
}
function nameOf(p) {
  if (p.pack && p.pack.company) return p.pack.company;
  return BASE_NAMES[p.slug] || p.slug.replace(/\.html$/, '');
}
function urlOf(p) {
  return p.slug === 'home' ? '/' : '/' + p.slug;
}
const PAGES = D.pages.map(p => {
  const lastOf = a => { for (let i = (a || []).length - 1; i >= 0; i--) if (a[i] > 0) return i; return -1; };
  return {...p, group: groupOf(p), name: nameOf(p), lastIdx: lastOf(p.daily), ownLastIdx: lastOf(p.ownDaily)};
});

// When a page was last opened: exact time if we have it, otherwise the day.
function lastSeen(p) {
  if (lastISO(p)) return {t: new Date(lastISO(p)).getTime(), exact: true};
  // Start of the day, so an exact time from today still sorts above a day-only one.
  const li = lastIdxOf(p);
  if (li >= 0) return {t: new Date(D.dates[li] + 'T00:00:00Z').getTime(), exact: false, idx: li};
  if (tot(p) > 0) return {t: 1, exact: false, old: true};
  return null;
}
function ago(p) {
  const s = lastSeen(p);
  if (!s) return 'Aldrig öppnad';
  if (s.old) return 'Över ' + N + ' dagar sedan';
  if (!s.exact) {
    const d = N - 1 - s.idx;
    return d === 0 ? 'Idag' : d === 1 ? 'Igår' : d < 14 ? 'För ' + d + ' dagar sedan' : dayLabel(D.dates[s.idx]);
  }
  const m = Math.round((Date.now() - s.t) / 60000);
  if (m < 2) return 'Nyss';
  if (m < 60) return 'För ' + m + ' min sedan';
  const h = Math.round(m / 60);
  if (h < 24) return 'För ' + h + ' h sedan';
  const d = Math.round(h / 24);
  if (d < 14) return d === 1 ? 'Igår' : 'För ' + d + ' dagar sedan';
  const dt = new Date(s.t);
  return dt.getDate() + ' ' + MONTHS[dt.getMonth()];
}
function isFresh(p) {
  const s = lastSeen(p);
  if (!s || s.old) return false;
  return s.exact ? Date.now() - s.t < 864e5 : s.idx === N - 1;
}
const rangeViews = p => sum(dl(p).slice(-R));

// Views this period against the period just before it.
function trendOf(p) {
  const cur = rangeViews(p), prev = sum(dl(p).slice(-2 * R, -R));
  return {cur, prev, diff: cur - prev};
}
// "Rising" = more views now than in the period before.
const isRising = p => trendOf(p).diff > 0;
function trendBadge(p) {
  const {diff} = trendOf(p);
  if (!diff) return '';
  return `<span class="trend ${diff > 0 ? 'up' : 'down'}" title="Jämfört med ${R} dagar innan">${diff > 0 ? '▲' : '▼'} ${fmt(Math.abs(diff))}</span>`;
}

/* ---------- visits ---------- */
const OWN = ['cv-page-mocha.vercel.app', 'marcushultberg.dev', 'localhost'];
const SHORT = 5;  // seconds; shorter visits are mostly bounces and bots
let HIDE_SHORT = store(s => s.getItem('stats-hideshort')) !== '0';
const keepVisit = v => (!HIDE_SHORT || v.dur >= SHORT) && (!OS || v.os === OS);

function fmtDur(s, short) {
  if (s == null) return '–';
  if (s < 60) return s + ' s';
  const m = Math.floor(s / 60);
  if (m < 60) return m + ' min' + (!short && s % 60 ? ' ' + (s % 60) + ' s' : '');
  return Math.floor(m / 60) + ' h ' + (m % 60) + ' min';
}
function median(a) {
  if (!a.length) return null;
  const s = [...a].sort((x, y) => x - y), m = s.length >> 1;
  return s.length % 2 ? s[m] : Math.round((s[m - 1] + s[m]) / 2);
}
// Typical time on the page: the median, so one tab left open doesn't skew it.
const typicalDur = p => median(visitsOf(p).filter(keepVisit).map(v => v.dur));

function fromLink(v) {
  if (!v.from) return '<span class="muted">Direkt</span> <span class="muted" title="Ingen avsändare: mejl, PDF, app eller inskriven adress">ⓘ</span>';
  const host = v.from.split('/')[0];
  if (OWN.includes(host)) return 'Din sida <span class="mono">' + esc(v.from.slice(host.length) || '/') + '</span>';
  return `<a href="https://${esc(v.from)}" target="_blank" rel="noopener noreferrer">${esc(v.from)}</a>`;
}
function clickChips(v) {
  if (!v.clicks || !v.clicks.length) return '<span class="muted">Inga klick</span>';
  return v.clicks.map(c => {
    const to = c.h === 'mailto' ? 'E-post' : c.h === 'tel' ? 'Telefon' : c.h;
    return `<span class="cl" title="${esc(to ? '→ ' + to : '')} · efter ${fmtDur(c.s)}">${esc(c.l || to || 'Klick')}</span>`;
  }).join('');
}
function visitTime(v) {
  return new Date(v.t * 1000).toLocaleString('sv-SE', {timeZone: 'Europe/Stockholm', day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit'});
}
function visitList(list, withPage) {
  const shown = list.filter(keepVisit);
  if (!shown.length) {
    const hidden = list.length - shown.length;
    return `<p class="muted">${hidden ? hidden + ' besök dolda av filtren.' : 'Inga besök registrerade ännu. Besökstid, länkar och klick samlas in från och med nu.'}</p>`;
  }
  return '<ul class="visits">' + shown.map(v => {
    const p = withPage ? PAGES.find(x => x.slug === v.page) : null;
    return `<li${p ? ` data-slug="${esc(p.slug)}"` : ''}>
      <div class="vh"><span class="vt">${visitTime(v)}</span>${p ? `<b class="vp">${esc(p.name)}</b>` : ''}
        <span class="vd num">${fmtDur(v.dur)}</span><span class="muted">${[v.os, v.dev === 'mobile' ? 'Mobil' : v.dev === 'desktop' ? 'Dator' : ''].filter(Boolean).join(' · ')}</span></div>
      <div class="vr"><span class="k">Kom från</span>${fromLink(v)}</div>
      <div class="vr"><span class="k">Klickade</span><span class="cls">${clickChips(v)}</span></div>
    </li>`;
  }).join('') + '</ul>';
}

/* ---------- KPIs ---------- */
function delta(cur, prev) {
  if (!prev && !cur) return '<span class="delta flat">±0</span>';
  if (!prev) return '<span class="delta up">ny</span>';
  const pct = Math.round((cur - prev) / prev * 100);
  const cls = pct > 0 ? 'up' : pct < 0 ? 'down' : 'flat';
  return `<span class="delta ${cls}">${pct > 0 ? '+' : ''}${pct}%</span>`;
}
function renderKpis() {
  if (ME) return renderOwnKpis();
  const cur = sum(D.daily.slice(-R)), prev = sum(D.daily.slice(-2 * R, -R));
  const packs = PAGES.filter(p => p.group === 'pack');
  const activePacks = packs.filter(p => rangeViews(p) > 0).length;
  const neverPacks = packs.filter(p => p.total === 0).length;
  const aiCur = sum(D.aiDaily.slice(-R)), aiPrev = sum(D.aiDaily.slice(-2 * R, -R));
  const today = D.daily[N - 1], yday = D.daily[N - 2];
  const hasPrev = 2 * R <= N;
  const tiles = [
    ['Visningar', fmt(cur), (hasPrev ? delta(cur, prev) + ' ' : '') + `senaste ${R} dagarna`],
    ['Idag', fmt(today), `igår ${fmt(yday)}`],
    ['Ansökningssidor öppnade', `${activePacks}<span class="muted" style="font-size:1rem;font-weight:500"> / ${packs.length}</span>`, neverPacks ? `${neverPacks} aldrig öppnade` : 'alla har öppnats'],
    ['AI-frågor', fmt(aiCur), (hasPrev ? delta(aiCur, aiPrev) + ' ' : '') + `${fmt(D.aiTotal)} totalt`],
    ['Totalt sedan start', fmt(D.total), 'alla sidor'],
  ];
  $('#kpis').innerHTML = tiles.map(([l, v, d]) =>
    `<div class="card kpi"><p class="l">${l}</p><p class="v num">${v}</p><p class="d">${d}</p></div>`).join('');
}

function renderOwnKpis() {
  const d = D.ownDaily || [];
  const cur = sum(d.slice(-R)), prev = sum(d.slice(-2 * R, -R));
  const opened = PAGES.filter(p => rangeViews(p) > 0).length;
  const vis = (D.ownVisits || []).filter(v => v.t * 1000 > Date.now() - R * 864e5);
  const tiles = [
    ['Mina visningar', fmt(cur), delta(cur, prev) + ` senaste ${R} dagarna`],
    ['Idag', fmt(d[N - 1] || 0), `igår ${fmt(d[N - 2] || 0)}`],
    ['Sidor jag öppnat', fmt(opened), `senaste ${R} dagarna`],
    ['Typisk tid', fmtDur(median(vis.map(v => v.dur))), `${fmt(vis.length)} besök med tid`],
    ['Totalt sedan start', fmt(D.ownTotal || 0), 'mina visningar'],
  ];
  $('#kpis').innerHTML = tiles.map(([l, v, x]) =>
    `<div class="card kpi"><p class="l">${l}</p><p class="v num">${v}</p><p class="d">${x}</p></div>`).join('');
}

/* ---------- bar chart ---------- */
function niceMax(v) {
  if (v <= 20) return Math.max(4, Math.ceil(v / 4) * 4);  // whole-number gridlines
  const p = Math.pow(10, Math.floor(Math.log10(v))), n = v / p;
  return (n <= 1 ? 1 : n <= 2 ? 2 : n <= 5 ? 5 : 10) * p;
}
function barChart(el, values, dates, opts = {}) {
  const W = Math.max(el.clientWidth, 280), H = opts.height || 220;
  const L = 32, B = 24, T = 8, iw = W - L, ih = H - B - T;
  const max = niceMax(Math.max(...values, 1));
  const n = values.length, step = iw / n, gap = n > 45 ? 1 : 2;
  const bw = Math.max(step - gap, 1), rad = Math.min(4, bw / 2);
  const y = v => T + ih - (v / max) * ih;
  let g = '<g class="grid">', ax = '<g class="axis">';
  for (let i = 0; i <= 4; i++) {
    const v = max / 4 * i, yy = y(v);
    g += `<line x1="${L}" x2="${W}" y1="${yy}" y2="${yy}"/>`;
    ax += `<text x="${L - 8}" y="${yy + 4}" text-anchor="end">${fmt(Math.round(v))}</text>`;
  }
  const every = Math.ceil(n / Math.max(2, Math.floor(iw / 70)));
  dates.forEach((d, i) => {
    if ((n - 1 - i) % every === 0) ax += `<text x="${L + i * step + step / 2}" y="${H - 6}" text-anchor="middle">${dayLabel(d)}</text>`;
  });
  g += '</g>'; ax += '</g>';
  let bars = '', hits = '';
  values.forEach((v, i) => {
    const x = L + i * step + gap / 2, top = y(v), h = T + ih - top;
    if (v > 0) {
      const r = Math.min(rad, h);
      bars += `<path class="bar" data-i="${i}" d="M${x},${T + ih}V${top + r}Q${x},${top} ${x + r},${top}H${x + bw - r}Q${x + bw},${top} ${x + bw},${top + r}V${T + ih}Z"/>`;
    }
    hits += `<rect class="hit" data-i="${i}" x="${L + i * step}" y="${T}" width="${step}" height="${ih}"/>`;
  });
  const label = (opts.title || 'Visningar per dag') + ': ' + fmt(sum(values)) + ' totalt, högst ' + fmt(Math.max(...values)) + ' på en dag.';
  el.innerHTML = `<svg viewBox="0 0 ${W} ${H}" height="${H}" role="img" aria-label="${esc(label)}">${g}${bars}${ax}${hits}</svg><div class="tip"></div>`;
  const tip = el.querySelector('.tip'), svg = el.querySelector('svg');
  svg.addEventListener('mousemove', e => {
    const i = e.target.dataset && e.target.dataset.i;
    if (i === undefined) { tip.style.opacity = 0; return; }
    const k = +i;
    svg.querySelectorAll('.bar').forEach(b => b.classList.toggle('dim', +b.dataset.i !== k));
    const extra = opts.extra ? opts.extra(k) : '';
    tip.innerHTML = `<span class="s">${weekday(dates[k])} ${dayLabel(dates[k])}</span><br><b>${fmt(values[k])}</b> visningar${extra}`;
    tip.style.left = Math.min(Math.max(L + k * step + step / 2, 70), W - 70) + 'px';
    tip.style.top = Math.min(y(values[k]), T + ih - 20) - 8 + 'px';
    tip.style.opacity = 1;
  });
  svg.addEventListener('mouseleave', () => {
    tip.style.opacity = 0;
    svg.querySelectorAll('.bar').forEach(b => b.classList.remove('dim'));
  });
}
const osSeries = () => (D.osDaily || []).map(h => (h || {})[OS] || 0);
function renderChart() {
  const off = N - R;
  const series = ME ? siteDaily() : OS ? osSeries() : D.daily;
  $('#chart-title').textContent = ME ? 'Mina visningar per dag' : OS ? 'Visningar per dag från ' + OS : 'Visningar per dag';
  barChart($('#chart'), series.slice(-R), D.dates.slice(-R), {
    title: ME ? 'Mina visningar' : OS ? 'Visningar från ' + OS : undefined,
    extra: k => {
      const i = off + k;
      return !OS && !ME && v2idx >= 0 && i >= v2idx ? `<br>${fmt(D.visitors[i])} besökare` : '';
    }
  });
  const max = Math.max(...series.slice(-R));
  const best = series.slice(-R).indexOf(max);
  $('#chart-hint').textContent = max ? `Bästa dag: ${dayLabel(D.dates[off + best])} (${fmt(max)})` : '';
}

/* ---------- sparkline ---------- */
function spark(values) {
  const w = 128, h = 30, n = values.length, max = Math.max(...values);
  if (!max) return `<svg class="spark" viewBox="0 0 ${w} ${h}" aria-hidden="true"><line class="zero" x1="0" x2="${w}" y1="${h - 2}" y2="${h - 2}"/></svg>`;
  const x = i => n === 1 ? w : i / (n - 1) * w, y = v => h - 2 - v / max * (h - 6);
  const pts = values.map((v, i) => `${x(i).toFixed(1)},${y(v).toFixed(1)}`);
  const line = 'M' + pts.join('L');
  return `<svg class="spark" viewBox="0 0 ${w} ${h}" aria-hidden="true"><path class="a" d="${line}L${w},${h}L0,${h}Z"/><path class="l" d="${line}"/><circle cx="${x(n - 1)}" cy="${y(values[n - 1])}" r="${values[n - 1] ? 2.5 : 0}"/></svg>`;
}

/* ---------- pages list ---------- */
const TABS = [['pack', 'Ansökningar'], ['base', 'Bassidor'], ['other', 'Övrigt'], ['all', 'Alla']];
function renderTabs() {
  $('#tabs').innerHTML = TABS.map(([k, l]) => {
    const c = k === 'all' ? PAGES.length : PAGES.filter(p => p.group === k).length;
    if (!c && k === 'other') return '';
    return `<button role="tab" data-t="${k}" aria-selected="${TAB === k}">${l}<span class="c">${c}</span></button>`;
  }).join('');
}
function sortPages(list) {
  const by = {
    last: (a, b) => ((lastSeen(b) || {t: 0}).t - (lastSeen(a) || {t: 0}).t) || b.total - a.total,
    range: (a, b) => rangeViews(b) - rangeViews(a) || b.total - a.total,
    total: (a, b) => osViews(b) - osViews(a),
    name: (a, b) => a.name.localeCompare(b.name, 'sv'),
    rising: (a, b) => trendOf(b).diff - trendOf(a).diff || rangeViews(b) - rangeViews(a),
    time: (a, b) => (typicalDur(b) ?? -1) - (typicalDur(a) ?? -1),
  };
  return list.sort(by[SORT] || by.last);
}
function renderRows() {
  const q = $('#q').value.trim().toLowerCase();
  let list = PAGES.filter(p => TAB === 'all' || p.group === TAB);
  if (RISING) list = list.filter(isRising);
  if (OS && !ME) list = list.filter(p => osViews(p) > 0);
  if (ME) list = list.filter(p => tot(p) > 0);
  if (q) list = list.filter(p => (p.name + ' ' + p.slug + ' ' + (p.pack ? p.pack.role : '')).toLowerCase().includes(q));
  list = sortPages(list);
  const head = `<li class="row head" aria-hidden="true"><span>Sida</span><span>Senaste ${R} d</span><span class="r">${R} d</span><span class="r" title="Typisk besökstid (median)">Tid</span><span class="r">${ME ? 'Mina' : OS ? esc(OS) : 'Totalt'}</span><span class="r">Senast</span></li>`;
  if (!list.length) { $('#rows').innerHTML = head + `<li class="empty">${ME ? 'Du har inte öppnat några sidor här ännu sedan dina egna besök började registreras.' : OS ? `Inga visningar från ${esc(OS)} ännu${RISING ? ' bland ökande sidor' : ''}.` : RISING ? `Ingen sida har fler visningar än de ${R} dagarna innan.` : 'Inga sidor matchar.'}</li>`; return; }
  $('#rows').innerHTML = head + list.map(p => {
    const role = p.pack ? p.pack.role : '';
    const fresh = isFresh(p);
    const badge = fresh ? '<span class="live" title="Öppnad senaste dygnet"></span>' : tot(p) === 0 && !ME ? '<span class="chip">Ej öppnad</span>' : '';
    return `<li class="row" tabindex="0" data-slug="${esc(p.slug)}">
      <div class="name"><div class="t"><span style="overflow:hidden;text-overflow:ellipsis">${esc(p.name)}</span>${badge}</div>
        <div class="s">${role ? esc(role) + ' · ' : ''}<span class="mono">${esc(urlOf(p))}</span></div></div>
      <div class="sp">${spark(dl(p).slice(-R))}</div>
      <div class="r rv"><span class="big num">${fmt(rangeViews(p))}</span>${trendBadge(p)}</div>
      <div class="r dur num muted">${fmtDur(typicalDur(p), true)}</div>
      <div class="r tot num muted">${fmt(osViews(p))}</div>
      <div class="when ${tot(p) ? '' : 'never'}">${ago(p)}</div>
    </li>`;
  }).join('');
}

/* ---------- side cards ---------- */
function hbars(obj, empty) {
  const e = Object.entries(obj).filter(([, v]) => v > 0).sort((a, b) => b[1] - a[1]);
  if (!e.length) return `<p class="muted">${empty}</p>`;
  const max = e[0][1], tot = sum(e.map(x => x[1]));
  return '<ul class="hbars">' + e.slice(0, 10).map(([k, v]) =>
    `<li><span class="n">${esc(k)}</span><span class="num">${fmt(v)} <span class="muted">${Math.round(v / tot * 100)}%</span></span><span class="track"><span class="fill" style="display:block;width:${Math.max(v / max * 100, 2)}%"></span></span></li>`).join('') + '</ul>';
}
function devices(d, empty) {
  const m = d.mobile || 0, k = d.desktop || 0, t = m + k;
  if (!t) return `<p class="muted">${empty}</p>`;
  const pm = Math.round(m / t * 100);
  return `<div class="split" role="img" aria-label="Mobil ${pm}%, dator ${100 - pm}%"><div style="width:${pm}%"></div><div style="width:${100 - pm}%"></div></div>
    <div class="legend"><span><i style="background:var(--accent)"></i>Mobil <b class="num">${pm}%</b> <span class="muted">(${fmt(m)})</span></span>
    <span><i style="background:var(--accent2)"></i>Dator <b class="num">${100 - pm}%</b> <span class="muted">(${fmt(k)})</span></span></div>`;
}
function renderOs() {
  $('#os').value = OS;
  $('#os').classList.toggle('on', !!OS);
  $('#oss').innerHTML = hbars(D.os || {}, 'Samlas in från och med nu.');
  $('#oss').querySelectorAll('.hbars li').forEach(li => {
    const name = li.querySelector('.n').textContent;
    li.classList.toggle('sel', name === OS);
    li.title = name === OS ? 'Visa alla system' : 'Visa bara ' + name;
    li.onclick = () => setOs(name === OS ? '' : name);
  });
  $('#osbar').innerHTML = OS
    ? `<div class="osbar"><span>Filtrerat på <b>${esc(OS)}</b>: diagrammet, besöken och vilka sidor som visas. Kolumnen ${esc(OS)} visar sidans visningar därifrån; nyckeltalen och kurvorna gäller alla system. Registreras sedan 17 nov.</span><button onclick="setOs('')">Visa alla</button></div>`
    : '';
}
function setOs(v) {
  OS = v; store(s => s.setItem('stats-os', OS));
  renderOs(); renderChart(); renderRows(); renderRecent();
}
function renderRecent() {
  $('#recent-title').textContent = ME ? 'Mina senaste besök' : 'Senaste besöken';
  $('#recent').innerHTML = visitList(ME ? (D.ownVisits || []) : (D.recent || []), true);
}
function renderBots() {
  const cur = sum((D.botsDaily || []).slice(-R));
  $('#bot-hint').textContent = `${fmt(D.bots)} totalt`;
  $('#bots').innerHTML = `<p><b class="num" style="font-size:1.4rem">${fmt(cur)}</b> <span class="muted">senaste ${R} dagarna</span></p>
    <p class="muted" style="margin-top:6px">Sökmotorer, länkförhandsvisningar och automatiserade webbläsare räknas här och ingen annanstans. Siffror från före 17 nov kan innehålla botar.</p>`;
}
function renderSide() {
  $('#refs').innerHTML = hbars(D.referrers, 'Ingen data ännu.');
  $('#devs').innerHTML = devices(D.devices, 'Ingen data ännu.');
  $('#clicks').innerHTML = hbars(D.clicks, 'Inga klick ännu.');
  $('#ai-hint').textContent = fmt(D.aiTotal) + ' totalt';
  $('#qs').innerHTML = D.questions.length ? '<ul class="qs">' + D.questions.map(q => {
    let t = '';
    try { t = new Date(q.t).toLocaleString('sv-SE', {timeZone: 'Europe/Stockholm', day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit'}); } catch (e) {}
    return `<li>${esc(q.q)}<div class="tm">${esc(t)}</div></li>`;
  }).join('') + '</ul>' : '<p class="muted">Inga frågor ännu.</p>';
}

/* ---------- drawer ---------- */
const dw = $('#dw');
function openPage(slug) {
  const p = PAGES.find(x => x.slug === slug);
  if (!p) return;
  const since = D.v2since ? `Samlas in sedan ${dayLabel(D.v2since)}.` : 'Samlas in från nästa besök.';
  const role = p.pack ? p.pack.role : '';
  $('#dw-body').innerHTML = `
    <div class="dw-h"><div><h3 id="dw-title">${esc(p.name)}</h3><p class="s">${role ? esc(role) + ' · ' : ''}<span class="mono">${esc(urlOf(p))}</span></p></div>
      <button class="close" aria-label="Stäng" onclick="dw.close()">×</button></div>
    <a class="open-link" href="${esc(urlOf(p))}" target="_blank" rel="noopener">Öppna sidan ↗</a>
    <div class="mini">
      <div><p class="l">${R} dagar</p><p class="v num">${fmt(rangeViews(p))}</p></div>
      <div><p class="l">${ME ? 'Mina totalt' : 'Totalt'}</p><p class="v num">${fmt(tot(p))}</p></div>
      <div><p class="l">Unika</p><p class="v num">${D.v2since ? fmt(p.uniq) : '–'}</p></div>
      <div><p class="l">Typisk tid</p><p class="v num">${fmtDur(typicalDur(p))}</p></div>
      <div><p class="l">Senast</p><p class="v" style="font-size:.95rem;padding-top:4px">${ago(p)}</p></div>
    </div>
    <div><h4>Visningar per dag</h4><div class="chart" id="dw-chart"></div></div>
    <div><h4>Källor</h4>${hbars(p.refs, 'Ingen data för sidan ännu. ' + since)}</div>
    <div><h4>Operativsystem</h4>${hbars(p.os || {}, 'Ingen data för sidan ännu. ' + since)}</div>
    <div><h4>Enheter</h4>${devices(p.devices, 'Ingen data för sidan ännu. ' + since)}</div>
    <div><h4>${ME ? 'Mina besök' : 'Besök'}</h4>${visitList(visitsOf(p), false)}</div>
    ${lastISO(p) ? `<p class="muted">${ME ? 'Mitt senaste besök' : 'Senaste besök'}: ${new Date(lastISO(p)).toLocaleString('sv-SE', {timeZone: 'Europe/Stockholm', dateStyle: 'medium', timeStyle: 'short'})}</p>` : ''}`;
  dw.showModal();
  barChart($('#dw-chart'), dl(p).slice(-R), D.dates.slice(-R), {height: 180, title: p.name});
}
dw.addEventListener('click', e => { if (e.target === dw) dw.close(); });

/* ---------- wiring ---------- */
function renderAll() {
  document.querySelectorAll('#range button').forEach(b => b.setAttribute('aria-pressed', +b.dataset.r === R));
  document.querySelectorAll('#who button').forEach(b => b.setAttribute('aria-pressed', (b.dataset.w === 'me') === ME));
  $('#mebar').innerHTML = ME
    ? `<div class="osbar"><span>Du tittar på <b>dina egna besök</b>: de som gjorts i webbläsare där du öppnat den här sidan eller använt <span class="mono">?notrack=1</span>. De räknas aldrig in bland besökarna. Registreras sedan 17 nov.</span><button onclick="setWho(false)">Visa besökare</button></div>`
    : '';
  renderKpis(); renderChart(); renderTabs(); renderRows(); renderBots();
}
$('#range').addEventListener('click', e => {
  const r = +e.target.dataset.r; if (!r) return;
  R = r; store(s => s.setItem('stats-range', R)); renderAll();
});
$('#tabs').addEventListener('click', e => {
  const b = e.target.closest('button'); if (!b) return;
  TAB = b.dataset.t; store(s => s.setItem('stats-tab', TAB)); renderTabs(); renderRows();
});
$('#q').addEventListener('input', renderRows);
$('#rising').checked = RISING;
$('#rising').addEventListener('change', e => { RISING = e.target.checked; store(s => s.setItem('stats-rising', RISING ? '1' : '0')); renderRows(); });
$('#sort').value = SORT;
$('#sort').addEventListener('change', e => { SORT = e.target.value; store(s => s.setItem('stats-sort', SORT)); renderRows(); });
$('#rows').addEventListener('click', e => { const r = e.target.closest('.row[data-slug]'); if (r) openPage(r.dataset.slug); });
$('#rows').addEventListener('keydown', e => {
  if (e.key !== 'Enter' && e.key !== ' ') return;
  const r = e.target.closest('.row[data-slug]'); if (r) { e.preventDefault(); openPage(r.dataset.slug); }
});
// Redraw when the chart's own box changes width (first layout, window resize, fonts).
let rt, lastW = 0;
new ResizeObserver(([e]) => {
  const w = Math.round(e.contentRect.width);
  if (w === lastW) return; lastW = w;
  clearTimeout(rt); rt = setTimeout(renderChart, 60);
}).observe($('#chart'));

if (!D.connected) $('#warn').innerHTML = '<div class="warn">Ingen anslutning till databasen (Upstash-nycklarna saknas). Siffrorna nedan är tomma.</div>';
$('#sub').textContent = `${PAGES.filter(p => p.group === 'pack').length} ansökningssidor · ${location.host}`;
$('#gen').textContent = 'Hämtad ' + new Date(D.generated).toLocaleString('sv-SE', {timeZone: 'Europe/Stockholm', dateStyle: 'medium', timeStyle: 'short'});
function renderOwn() {
  const off = store(s => s.getItem('cv-notrack')) === '1';
  $('#own').innerHTML = off
    ? `Dina besök på ${esc(location.host)} i den här webbläsaren hamnar under "Mina besök", inte bland besökarna. På andra enheter eller domäner: öppna sidan med <span class="mono">?notrack=1</span>. <button id="own-btn">Räkna mig som besökare</button>`
    : `Dina besök räknas just nu som vanliga besökare. <button id="own-btn">Flytta mina besök till "Mina besök"</button>`;
  $('#own-btn').onclick = () => { store(s => off ? s.removeItem('cv-notrack') : s.setItem('cv-notrack', '1')); renderOwn(); };
}
$('#hideshort').checked = HIDE_SHORT;
$('#hideshort').addEventListener('change', e => {
  HIDE_SHORT = e.target.checked; store(s => s.setItem('stats-hideshort', HIDE_SHORT ? '1' : '0'));
  renderRecent(); renderRows();
});
$('#recent').addEventListener('click', e => {
  if (e.target.closest('a')) return;
  const li = e.target.closest('li[data-slug]'); if (li) openPage(li.dataset.slug);
});
$('#os').addEventListener('change', e => setOs(e.target.value));
function setWho(me) {
  ME = me; store(s => s.setItem('stats-who', ME ? 'me' : 'visitors'));
  renderAll(); renderRecent();
}
$('#who').addEventListener('click', e => { const w = e.target.dataset.w; if (w) setWho(w === 'me'); });
renderOwn(); renderSide(); renderOs(); renderRecent(); renderAll();
</script>
</body>
</html>
"""
