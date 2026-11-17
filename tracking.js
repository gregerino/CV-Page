// CV Page Analytics - lightweight tracking
(function() {
  // Relative on purpose: the site answers on more than one domain.
  var endpoint = '/api/track';
  var page = location.pathname.replace(/^\//, '') || 'home';

  function store(fn) { try { return fn(window.localStorage); } catch (e) { return null; } }

  // Your own visits: open any page with ?notrack=1 once per browser and domain
  // (?notrack=0 undoes it). Opening the stats dashboard does the same.
  var flag = new URLSearchParams(location.search).get('notrack');
  if (flag === '1') store(function(s) { s.setItem('cv-notrack', '1'); });
  if (flag === '0') store(function(s) { s.removeItem('cv-notrack'); });
  if (store(function(s) { return s.getItem('cv-notrack'); }) === '1') return;

  // Automated browsers announce themselves through webdriver or their UA.
  // The server checks the UA as well; this flag catches the ones that hide it.
  var bot = !!navigator.webdriver ||
    /bot|crawl|spider|headless|lighthouse|preview|phantom/i.test(navigator.userAgent) ||
    (navigator.languages !== undefined && navigator.languages.length === 0);

  var device = /Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent) ? 'mobile' : 'desktop';
  var ref = document.referrer || '';

  // First visit to this page, and first visit to the site today, in this browser.
  var today = new Date().toISOString().slice(0, 10);
  var newPage = bot ? false : store(function(s) {
    if (s.getItem('cv-seen:' + page)) return false;
    s.setItem('cv-seen:' + page, '1'); return true;
  });
  var newDay = bot ? false : store(function(s) {
    if (s.getItem('cv-day') === today) return false;
    s.setItem('cv-day', today); return true;
  });

  function send(data, beacon) {
    var body = JSON.stringify(data);
    if (beacon && navigator.sendBeacon) {
      navigator.sendBeacon(endpoint, new Blob([body], { type: 'application/json' }));
      return;
    }
    fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: body,
      keepalive: true
    }).catch(function(){});
  }

  send({ page: page, event: 'pageview', device: device, referrer: ref, bot: bot,
         newPage: newPage !== false, newDay: newDay !== false });
  if (bot) return;  // counted as a bot above; nothing else to record

  // ---- The visit: how long the page was actually on screen, and what was clicked.
  var visit = {
    id: Date.now().toString(36) + Math.random().toString(36).slice(2, 8),
    start: Date.now(),
    clicks: []
  };
  var activeMs = 0;
  var shownAt = document.visibilityState === 'visible' ? Date.now() : 0;

  function seconds() {
    var ms = activeMs + (shownAt ? Date.now() - shownAt : 0);
    return Math.round(ms / 1000);
  }

  function where(href) {
    if (!href) return '';
    if (/^mailto:/i.test(href)) return 'mailto';
    if (/^tel:/i.test(href)) return 'tel';
    try {
      var u = new URL(href, location.href);
      if (u.host === location.host) return u.pathname + u.hash;
      return u.host.replace(/^www\./, '') + u.pathname;
    } catch (e) { return ''; }
  }

  // Sent every time the page is hidden; the server keeps the latest copy per visit,
  // so a visitor who comes back to the tab just extends the same visit.
  function report() {
    send({ page: page, event: 'visit', id: visit.id, start: visit.start,
           dur: seconds(), device: device, referrer: ref, clicks: visit.clicks }, true);
  }

  document.addEventListener('visibilitychange', function() {
    if (document.visibilityState === 'hidden') {
      if (shownAt) { activeMs += Date.now() - shownAt; shownAt = 0; }
      report();
    } else if (!shownAt) {
      shownAt = Date.now();
    }
  });
  window.addEventListener('pagehide', function() {
    if (shownAt) { activeMs += Date.now() - shownAt; shownAt = 0; }
    report();
  });

  document.addEventListener('click', function(e) {
    var el = e.target.closest('a, button, [role="button"]');
    if (!el) return;

    // Nav links keep feeding the site-wide menu counter.
    if (el.matches('.nav-links a, .nav-mobile a')) {
      send({ page: page, event: 'click', target: el.textContent.trim() });
    }

    var label = (el.getAttribute('aria-label') || el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 60);
    if (!label && !el.href) return;
    if (visit.clicks.length < 30) {
      visit.clicks.push({ l: label, h: where(el.getAttribute('href')), s: seconds() });
    }
    // Leaving for another page or site: report now, before the page goes.
    if (el.href && el.target !== '_blank' && !/^#/.test(el.getAttribute('href') || '')) report();
  }, true);
})();
