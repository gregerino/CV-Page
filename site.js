// Interaction for the single-page CV: mobile nav, scroll reveal,
// active-section highlighting, the tiles and their popups, and the
// floating AI assistant.
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
  var revealer = null;

  if (!reduced && 'IntersectionObserver' in window) {
    revealer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          revealer.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
  }

  function watchReveals(root) {
    var els = (root || document).querySelectorAll('.reveal');
    els.forEach(function (el) {
      if (revealer) revealer.observe(el); else el.classList.add('in');
    });
  }
  watchReveals();

  /* ── Tiles and popups ──
     The start page is one screen of tiles. A tile shows the short version;
     a click opens the full text in a popup. Everything stays in the HTML,
     so search engines, job packs and the language toggle all reach it.

     A popup is a <dialog> inside the tile's own section, holding a copy of
     what was clicked, so the section's styles (and a job theme's) still
     apply. An item is copied together with its list, the other items
     hidden, so :nth-of-type colours and tags stay on the right one. */

  var lastTrigger = null;

  function text(en, sv) {
    return '<span data-sv="' + sv + '">' + en + '</span>';
  }

  function closeButton(dialog) {
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'dialog-close';
    btn.innerHTML = '<span class="sr-only">' + text('Close', 'Stäng') + '</span>' +
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" ' +
      'stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>';
    btn.addEventListener('click', function () { dialog.close(); });
    return btn;
  }

  function wireDialog(dialog) {
    // A click on the backdrop lands on the dialog element itself.
    dialog.addEventListener('click', function (e) {
      if (e.target === dialog) dialog.close();
    });
    dialog.addEventListener('close', function () {
      if (lastTrigger && document.contains(lastTrigger)) lastTrigger.focus();
      lastTrigger = null;
      if (dialog.classList.contains('detail')) dialog.querySelector('.detail-body').textContent = '';
      if (location.hash && dialog.querySelector(location.hash)) {
        history.replaceState(null, '', location.pathname + location.search);
      }
    });
  }

  function detailDialog(section) {
    var dialog = section.querySelector(':scope > dialog.detail');
    if (dialog) return dialog;
    dialog = document.createElement('dialog');
    dialog.className = 'detail';
    var body = document.createElement('div');
    body.className = 'detail-body';
    dialog.appendChild(closeButton(dialog));
    dialog.appendChild(body);
    section.appendChild(dialog);
    wireDialog(dialog);
    return dialog;
  }

  function scrub(node) {
    if (node.nodeType !== 1) return node;
    [node].concat([].slice.call(node.querySelectorAll('*'))).forEach(function (el) {
      el.removeAttribute('id');
      el.classList.remove('reveal');
    });
    node.querySelectorAll('.tile-hit, .tile-more').forEach(function (el) { el.remove(); });
    return node;
  }

  function show(section, nodes, kind) {
    var dialog = detailDialog(section);
    var body = dialog.querySelector('.detail-body');
    body.textContent = '';
    body.className = 'detail-body detail-body--' + kind;
    nodes.forEach(function (n) { body.appendChild(scrub(n)); });
    if (window.CVLang) window.CVLang.refresh();
    dialog.showModal();
    dialog.scrollTop = 0;
    body.scrollTop = 0;
  }

  // One item: its list is copied and every other item switched off.
  function openItem(item) {
    var list = item.parentNode;
    var index = [].indexOf.call(list.children, item);
    var copy = list.cloneNode(true);
    [].forEach.call(copy.children, function (child, i) {
      if (i !== index) child.classList.add('is-off');
    });
    show(item.closest('.tile'), [copy], 'item');
  }

  // The whole section, in full.
  function openSection(section) {
    var wrap = section.querySelector(':scope > .wrap');
    var nodes = [].map.call(wrap.children, function (n) { return n.cloneNode(true); });
    show(section, nodes, 'section');
  }

  var ITEMS = '#match .point, #experience .job, #built .built-card, #education .edu-card';

  // Each item gets a button over the whole of it: the title is its label.
  function enhance(root) {
    (root || document).querySelectorAll(ITEMS).forEach(function (item) {
      if (item.querySelector(':scope > .tile-hit')) return;
      var title = item.querySelector('.point-title, .job-title, .built-title, .edu-degree');
      if (!title) return;
      if (!title.id) title.id = 'tile-' + Math.random().toString(36).slice(2, 9);
      var hit = document.createElement('button');
      hit.type = 'button';
      hit.className = 'tile-hit';
      hit.setAttribute('aria-describedby', title.id);
      hit.innerHTML = '<span class="sr-only">' + text('Read more:', 'Läs mer:') + '</span>';
      hit.addEventListener('click', function () { lastTrigger = hit; openItem(item); });
      item.appendChild(hit);
    });
    if (window.CVLang) window.CVLang.refresh();
  }

  // Colour helpers for the link below: the first opaque background up the
  // tree, and the WCAG contrast ratio between two rgb() strings.
  function rgb(c) { return (c.match(/[\d.]+/g) || []).map(Number); }
  function backdrop(el) {
    for (; el; el = el.parentElement) {
      var c = rgb(getComputedStyle(el).backgroundColor);
      if (c.length && (c.length < 4 || c[3] > 0.5)) return c;
    }
    return [255, 255, 255];
  }
  function luminance(c) {
    var v = c.slice(0, 3).map(function (x) {
      x /= 255;
      return x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2];
  }
  function contrast(color, ground) {
    var a = luminance(rgb(color)), b = luminance(ground);
    return (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
  }

  // The link at the foot of a tile that opens the whole section.
  var MORE = {
    match:      { en: 'Everything in full', sv: 'Allt i sin helhet' },
    experience: { en: 'All roles in full', sv: 'Alla roller i sin helhet' },
    built:      { en: 'View all projects', sv: 'Visa alla projekt' },
    education:  { en: 'Skills, tools and languages', sv: 'Kompetenser, verktyg och språk' }
  };

  Object.keys(MORE).forEach(function (id) {
    var section = document.getElementById(id);
    if (!section) return;
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'tile-more';
    btn.innerHTML = text(MORE[id].en, MORE[id].sv) + ' <span aria-hidden="true">→</span>';
    btn.addEventListener('click', function () { lastTrigger = btn; openSection(section); });
    section.querySelector(':scope > .wrap').appendChild(btn);
    // Job themes paint some tiles dark without touching --ink, and some
    // give the small label a pale accent. Take whichever of the label's and
    // the heading's colour stands out more against the tile.
    var picks = [section.querySelector('.eyebrow'), section.querySelector('.sec-title')]
      .filter(Boolean)
      .map(function (el) { return getComputedStyle(el).color; });
    if (picks.length) {
      var ground = backdrop(section);
      picks.sort(function (a, b) { return contrast(b, ground) - contrast(a, ground); });
      btn.style.color = picks[0];
    }
  });

  enhance();

  // The Experience tile puts its dates in a column; size it to the widest
  // date once the fonts are in, since a job theme may bring a wide one.
  function sizeDates() {
    var tl = document.querySelector('#experience > .wrap .timeline');
    if (!tl) return;
    var widest = 0;
    tl.querySelectorAll('.job-date').forEach(function (d) {
      widest = Math.max(widest, d.getBoundingClientRect().width);
    });
    if (widest) tl.style.setProperty('--date-col', Math.ceil(widest) + 'px');
  }
  sizeDates();
  if (document.fonts) document.fonts.ready.then(sizeDates);

  // About and Personal live in sheets: <dialog class="sheet"> around the
  // section. A link to #about (the nav, "More about me", an old /about.html
  // redirect) opens the sheet instead of scrolling.
  document.querySelectorAll('dialog.sheet').forEach(function (sheet) {
    sheet.insertBefore(closeButton(sheet), sheet.firstChild);
    wireDialog(sheet);
  });

  function sheetFor(hash) {
    if (!hash || hash.length < 2) return null;
    var target = document.getElementById(hash.slice(1));
    return target ? target.closest('dialog.sheet') : null;
  }

  document.addEventListener('click', function (e) {
    var link = e.target.closest('a[href^="#"]');
    if (!link) return;
    var sheet = sheetFor(link.getAttribute('href'));
    if (!sheet) return;
    e.preventDefault();
    lastTrigger = link;
    sheet.showModal();
  });

  var initial = sheetFor(location.hash);
  if (initial) initial.showModal();

  // job.js builds cards and roles after load and needs them picked up too.
  window.CVSite = {
    watchReveals: watchReveals,
    enhance: function (root) { enhance(root); sizeDates(); }
  };

  /* ── Active section in the nav ── */
  var navLinks = document.querySelectorAll('.nav-links a, .nav-mobile a');
  var sections = [];
  navLinks.forEach(function (link) {
    var href = link.getAttribute('href');
    if (!href || href.charAt(0) !== '#') return; // links to other pages, e.g. index.html#about
    var el = document.querySelector(href);
    if (el && sections.indexOf(el) === -1) sections.push(el);
  });
  // Page order, not nav order: the nav lists Experience before Projects.
  sections.sort(function (a, b) {
    return a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING ? -1 : 1;
  });

  function markActive(id) {
    navLinks.forEach(function (link) {
      var on = link.getAttribute('href') === '#' + id;
      link.classList.toggle('active', on);
      if (on) link.setAttribute('aria-current', 'true'); else link.removeAttribute('aria-current');
    });
  }

  // The section whose top has most recently passed the reading line wins.
  // An IntersectionObserver is unreliable here because sections are taller
  // than the viewport and several can qualify at once.
  function updateActive() {
    // The one-screen start page has its tiles side by side: there is no
    // section to follow, so Home stays marked.
    var scrolls = document.body.scrollHeight > window.innerHeight + 120;
    if (!scrolls) { markActive(sections[0] ? sections[0].id : ''); return; }
    var line = window.scrollY + window.innerHeight * 0.35;
    var current = null;
    sections.forEach(function (s) {
      // A hidden section (e.g. #personal switched off) reports offsetTop 0.
      // Tiles share a top edge, so the lowest one past the line wins and a
      // tie goes to the first in the page.
      if (s.offsetParent !== null && s.offsetTop <= line &&
          (!current || s.offsetTop > current.offsetTop)) current = s;
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

  /* ── AI assistant (start page only) ── */
  if (!document.getElementById('ai-input')) return;

  var fab = document.getElementById('ask-open');
  var panel = document.getElementById('ask-panel');
  var closeBtn = document.getElementById('ask-close');
  var input = document.getElementById('ai-input');
  var askBtn = document.getElementById('ai-btn');
  var loading = document.getElementById('ai-loading');
  var log = document.getElementById('ask-log');

  function openPanel() {
    panel.hidden = false;
    fab.setAttribute('aria-expanded', 'true');
    document.documentElement.classList.add('ask-open');
    input.focus();
  }

  function closePanel() {
    panel.hidden = true;
    fab.setAttribute('aria-expanded', 'false');
    document.documentElement.classList.remove('ask-open');
    fab.focus();
  }

  fab.addEventListener('click', function () {
    if (panel.hidden) openPanel(); else closePanel();
  });
  closeBtn.addEventListener('click', closePanel);
  panel.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closePanel();
  });

  function fallback(sv, en) {
    return document.documentElement.lang === 'sv' ? sv : en;
  }

  function line(className, text) {
    var p = document.createElement('p');
    p.className = className;
    p.textContent = text;
    return p;
  }

  // Each question and its answer stay in the panel, newest last. The
  // assistant answers every question on its own; the log is only for the
  // reader.
  function addExchange(question) {
    var item = document.createElement('div');
    item.className = 'ask-item';
    item.appendChild(line('ask-q', question));
    log.appendChild(item);
    return item;
  }

  // The assistant writes a little markdown: **bold**, and lists in lines that
  // start with "- " or "* ". Those become real elements; everything is set
  // as text, never as HTML, so an answer cannot inject markup.
  function inline(parent, text) {
    text.split(/\*\*(.+?)\*\*/).forEach(function (part, i) {
      if (!part) return;
      if (i % 2) {
        var b = document.createElement('strong');
        b.textContent = part;
        parent.appendChild(b);
      } else {
        parent.appendChild(document.createTextNode(part));
      }
    });
  }

  function formatted(text) {
    var box = document.createElement('div');
    box.className = 'ask-out-text';
    var list = null;
    text.split('\n').forEach(function (raw) {
      var l = raw.trim();
      if (!l) { list = null; return; }
      var bullet = /^[-*•]\s+/.exec(l);
      if (bullet) {
        if (!list) { list = document.createElement('ul'); box.appendChild(list); }
        var li = document.createElement('li');
        inline(li, l.slice(bullet[0].length));
        list.appendChild(li);
      } else {
        list = null;
        var p = document.createElement('p');
        inline(p, l.replace(/^#+\s*/, ''));
        box.appendChild(p);
      }
    });
    return box;
  }

  function answer(item, text) {
    var out = document.createElement('div');
    out.className = 'ask-out visible';
    out.appendChild(line('ask-out-label', fallback('Svar', 'Answer')));
    out.appendChild(formatted(text));
    item.appendChild(out);
    log.scrollTop = log.scrollHeight;
  }

  async function ask(question) {
    var q = (question || input.value).trim();
    if (!q) return;
    input.value = '';

    var item = addExchange(q);
    askBtn.disabled = true;
    loading.classList.add('visible');
    log.scrollTop = log.scrollHeight;

    try {
      var res = await fetch('/api/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: q })
      });
      var data = await res.json();
      answer(item, data.answer || data.error ||
        fallback('Något gick fel. Försök gärna igen.', 'Something went wrong. Please try again.'));
    } catch (e) {
      answer(item, fallback('Kunde inte nå servern. Försök gärna igen senare.',
                            'Could not reach the server. Please try again later.'));
    } finally {
      askBtn.disabled = false;
      loading.classList.remove('visible');
      input.focus();
    }
  }

  askBtn.addEventListener('click', function () { ask(); });
  input.addEventListener('keydown', function (e) { if (e.key === 'Enter') ask(); });

  document.getElementById('ask-chips').addEventListener('click', function (e) {
    var chip = e.target.closest('.ask-chip');
    if (chip) ask(chip.textContent);
  });
})();
