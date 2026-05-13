// CV Page Analytics - lightweight tracking
(function() {
  var endpoint = 'https://cv-page-mocha.vercel.app/api/track';
  var page = location.pathname.replace(/^\//, '') || 'home';

  // Track page view
  fetch(endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ page: page, event: 'pageview' })
  }).catch(function(){});

  // Track nav clicks
  document.addEventListener('click', function(e) {
    var link = e.target.closest('.nav-links a, .nav-mobile-overlay a');
    if (link) {
      fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ page: page, event: 'click', target: link.textContent.trim() })
      }).catch(function(){});
    }
  });
})();
