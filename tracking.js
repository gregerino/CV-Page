// CV Page Analytics - lightweight tracking
(function() {
  var endpoint = 'https://cv-page-mocha.vercel.app/api/track';
  var page = location.pathname.replace(/^\//, '') || 'home';

  // Detect device type
  var device = /Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent) ? 'mobile' : 'desktop';

  // Get referrer source
  var ref = document.referrer || '';

  // Track page view
  fetch(endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ page: page, event: 'pageview', device: device, referrer: ref })
  }).catch(function(){});

  // Track nav clicks
  document.addEventListener('click', function(e) {
    var link = e.target.closest('.nav-links a, .nav-mobile a');
    if (link) {
      fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ page: page, event: 'click', target: link.textContent.trim() })
      }).catch(function(){});
    }
  });
})();
