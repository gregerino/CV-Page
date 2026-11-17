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

  var device = /Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent) ? 'mobile' : 'desktop';
  var ref = document.referrer || '';

  // First visit to this page, and first visit to the site today, in this browser.
  var today = new Date().toISOString().slice(0, 10);
  var newPage = store(function(s) {
    if (s.getItem('cv-seen:' + page)) return false;
    s.setItem('cv-seen:' + page, '1'); return true;
  });
  var newDay = store(function(s) {
    if (s.getItem('cv-day') === today) return false;
    s.setItem('cv-day', today); return true;
  });

  function send(data) {
    fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
      keepalive: true
    }).catch(function(){});
  }

  send({ page: page, event: 'pageview', device: device, referrer: ref,
         newPage: newPage !== false, newDay: newDay !== false });

  document.addEventListener('click', function(e) {
    var link = e.target.closest('.nav-links a, .nav-mobile a');
    if (link) send({ page: page, event: 'click', target: link.textContent.trim() });
  });
})();
