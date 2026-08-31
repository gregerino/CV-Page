// Interaction for the single-page CV: mobile nav, scroll reveal,
// active-section highlighting, and the AI answer bar.
(function () {
  'use strict';

  /* ── Mobile navigation ── */
  var burger = document.getElementById('hamburger');
  var mobileNav = document.getElementById('mobile-nav');

  function closeMenu() {
    burger.classList.remove('open');
    mobileNav.classList.remove('open');
    burger.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  }

  burger.addEventListener('click', function () {
    var open = burger.classList.toggle('open');
    mobileNav.classList.toggle('open', open);
    burger.setAttribute('aria-expanded', String(open));
    document.body.style.overflow = open ? 'hidden' : '';
  });

  mobileNav.querySelectorAll('a').forEach(function (a) {
    a.addEventListener('click', closeMenu);
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && mobileNav.classList.contains('open')) closeMenu();
  });

  /* ── Reveal on scroll ── */
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var revealables = document.querySelectorAll('.reveal');

  if (reduced || !('IntersectionObserver' in window)) {
    revealables.forEach(function (el) { el.classList.add('in'); });
  } else {
    var revealer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          revealer.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    revealables.forEach(function (el) { revealer.observe(el); });
  }

  /* ── Active section in the nav ── */
  var navLinks = document.querySelectorAll('.nav-links a, .nav-mobile a');
  var sections = [];
  navLinks.forEach(function (link) {
    var href = link.getAttribute('href');
    if (!href || href.charAt(0) !== '#') return; // links to other pages, e.g. cv.html
    var el = document.querySelector(href);
    if (el && sections.indexOf(el) === -1) sections.push(el);
  });

  function markActive(id) {
    navLinks.forEach(function (link) {
      link.classList.toggle('active', link.getAttribute('href') === '#' + id);
    });
  }

  // The section whose top has most recently passed the reading line wins.
  // An IntersectionObserver is unreliable here because sections are taller
  // than the viewport and several can qualify at once.
  function updateActive() {
    var line = window.scrollY + window.innerHeight * 0.35;
    var current = null;
    sections.forEach(function (s) {
      if (s.offsetTop <= line) current = s;
    });
    var atBottom = window.innerHeight + window.scrollY >= document.body.scrollHeight - 4;
    if (atBottom) current = sections[sections.length - 1];
    markActive(current ? current.id : '');
  }

  if (sections.length) {
    var ticking = false;
    window.addEventListener('scroll', function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () { updateActive(); ticking = false; });
    }, { passive: true });
    window.addEventListener('resize', updateActive);
    updateActive();
  }

  /* ── AI answer bar (start page only) ── */
  if (!document.getElementById('ai-input')) return;

  var input = document.getElementById('ai-input');
  var askBtn = document.getElementById('ai-btn');
  var loading = document.getElementById('ai-loading');
  var response = document.getElementById('ai-response');
  var responseText = document.getElementById('ai-response-text');

  function fallback(sv, en) {
    return document.documentElement.lang === 'sv' ? sv : en;
  }

  function show(text) {
    responseText.textContent = text;
    response.classList.add('visible');
  }

  async function ask(question) {
    var q = (question || input.value).trim();
    if (!q) return;
    input.value = q;

    askBtn.disabled = true;
    loading.classList.add('visible');
    response.classList.remove('visible');

    try {
      var res = await fetch('/api/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: q })
      });
      var data = await res.json();
      show(data.answer || data.error ||
        fallback('Något gick fel. Försök gärna igen.', 'Something went wrong. Please try again.'));
    } catch (e) {
      show(fallback('Kunde inte nå servern. Försök gärna igen senare.',
                    'Could not reach the server. Please try again later.'));
    } finally {
      askBtn.disabled = false;
      loading.classList.remove('visible');
    }
  }

  askBtn.addEventListener('click', function () { ask(); });
  input.addEventListener('keydown', function (e) { if (e.key === 'Enter') ask(); });

  document.getElementById('ask-chips').addEventListener('click', function (e) {
    var chip = e.target.closest('.ask-chip');
    if (chip) ask(chip.textContent);
  });
})();
