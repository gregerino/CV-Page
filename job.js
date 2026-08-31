// Job-specific pages.
//
// The base CV lives at "/" and is never edited for an application. To tailor
// the page for a job, drop a JSON file in /jobs/ and visit its slug:
//
//   jobs/picadeli.json  ->  https://<site>/picadeli
//
// Everything the pack does not mention keeps the base wording, so a pack can
// be as small as a new hero line. If the slug has no pack, or anything fails,
// the base page stands unchanged.
//
// Colours are not handled here: an optional jobs/<slug>.css is linked by the
// head script in index.html, before the first paint, so the page never has to
// be repainted in the company's palette after the fact.
//
// See jobs/README.md for the full list of fields.
(function () {
  'use strict';

  var params = new URLSearchParams(location.search);
  var slug = (params.get('job') ||
              location.pathname.replace(/^\/+|\/+$/g, '').replace(/\.html$/, '')
             ).toLowerCase().trim();

  var RESERVED = ['', 'index', 'cv'];

  function done() {
    document.documentElement.classList.remove('job-pending');
  }

  if (RESERVED.indexOf(slug) !== -1 || !/^[a-z0-9-]+$/.test(slug)) { done(); return; }

  // Never leave the page hidden because a request hung.
  var safety = setTimeout(done, 4000);

  fetch('/jobs/' + encodeURIComponent(slug) + '.json')
    .then(function (r) {
      if (!r.ok) throw new Error('no pack for ' + slug);
      return r.json();
    })
    .then(apply)
    .catch(function () { /* unknown slug: the base CV is a fine fallback */ })
    .then(function () { clearTimeout(safety); done(); });

  /* ── Applying a pack ────────────────────────────────────────────────── */

  // Text is stored the same way as in the HTML: English on the element,
  // Swedish in data-sv. Writing both keeps the language toggle working.
  function put(selector, value) {
    if (!value) return;
    var el = document.querySelector(selector);
    if (el) write(el, value);
  }

  function write(el, value) {
    var en = value.en != null ? value.en : value;
    var sv = value.sv != null ? value.sv : en;
    el.removeAttribute('data-sv-html');
    el.removeAttribute('data-en-html');
    el.setAttribute('data-en', en);
    el.setAttribute('data-sv', sv);
    el.textContent = en;
  }

  // The rest of the page, keyed by CSS selector. A string (or an {en, sv}
  // pair) rewrites the first element the selector matches. An array rewrites
  // every element it matches, in order: spare elements are removed and
  // missing ones cloned from the last, so a list can grow or shrink with the
  // pack. Selectors that match nothing are skipped, so a pack can never break
  // the page — the base wording simply stays.
  function applyText(map) {
    Object.keys(map).forEach(function (selector) {
      var value = map[selector];
      if (Array.isArray(value)) fill(selector, value);
      else put(selector, value);
    });
  }

  function fill(selector, items) {
    var nodes = [].slice.call(document.querySelectorAll(selector));
    if (!nodes.length || !items.length) return;

    var last = nodes[nodes.length - 1];
    while (nodes.length < items.length) {
      var clone = last.cloneNode(false);
      last.parentNode.insertBefore(clone, last.nextSibling);
      nodes.push(clone);
      last = clone;
    }
    nodes.splice(items.length).forEach(function (node) {
      node.parentNode.removeChild(node);
    });
    items.forEach(function (item, i) { write(nodes[i], item); });
  }

  function apply(job) {
    put('.hero .eyebrow', job.eyebrow);
    put('.hero-role', job.role);
    put('.hero-lead', job.lead);
    put('.hero-cta .btn-primary .btn-label', job.cta);

    put('#match .eyebrow', job.matchEyebrow);
    put('#match .sec-title', job.matchTitle);
    put('#match .sec-lead', job.matchLead);

    if (Array.isArray(job.points) && job.points.length) buildPoints(job.points);

    if (job.text) applyText(job.text);

    if (job.pageTitle) {
      document.title = job.pageTitle.en != null ? job.pageTitle.en : job.pageTitle;
    } else if (job.company) {
      document.title = 'Marcus Hultberg — ' + (job.roleName ? job.roleName + ', ' : '') + job.company;
    }

    // An application page is for one reader, not for search engines.
    var robots = document.createElement('meta');
    robots.name = 'robots';
    robots.content = 'noindex, nofollow';
    document.head.appendChild(robots);

    carrySlug();

    if (window.CVLang) window.CVLang.refresh();
  }

  // The CV is a separate page, so the slug has to travel with the click for
  // the reader to keep the application's colours and title. cv.html reads it
  // from the query string; see the head script there.
  function carrySlug() {
    document.querySelectorAll('a[href="cv.html"]').forEach(function (a) {
      a.setAttribute('href', 'cv.html?job=' + encodeURIComponent(slug));
    });
  }

  function buildPoints(points) {
    var host = document.querySelector('#match .points');
    if (!host) return;
    host.textContent = '';

    points.forEach(function (p, i) {
      var card = el('article', 'card point reveal');

      var numWrap = el('div', 'point-num-wrap');
      numWrap.appendChild(el('div', 'point-rule'));
      var num = el('div', 'point-num');
      num.textContent = ('0' + (i + 1)).slice(-2);
      numWrap.appendChild(num);

      var body = el('div');
      body.appendChild(text('h3', 'point-title', p.title));
      if (p.quote) body.appendChild(text('p', 'point-quote', p.quote));
      if (p.body) body.appendChild(text('p', 'point-body', p.body));

      card.appendChild(numWrap);
      card.appendChild(body);
      host.appendChild(card);
    });

    if (window.CVSite) window.CVSite.watchReveals(host);
  }

  function el(tag, className) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    return node;
  }

  function text(tag, className, value) {
    var node = el(tag, className);
    write(node, value || '');
    return node;
  }
})();
