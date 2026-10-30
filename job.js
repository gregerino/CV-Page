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
// The CV page (cv.html?job=<slug>) runs this file too. There it applies the
// parts of the pack that belong on a CV — see applyCv — and both pages point
// their PDF links at the pack's own PDF, printed from that CV by
// build_cv_pdf.sh, never at the base CV.
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

  // Before the fetch, so a quick click on CV (or a pack that fails to load)
  // still takes the reader back to this page from the CV.
  carrySlug();
  linkPdf();

  // Never leave the page hidden because a request hung.
  var safety = setTimeout(done, 4000);

  fetch('/jobs/' + encodeURIComponent(slug) + '.json')
    .then(function (r) {
      if (!r.ok) throw new Error('no pack for ' + slug);
      return r.json();
    })
    .then(document.body.classList.contains('cv-page') ? applyCv : apply)
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
    // Shows the "How I match" nav link and lays the match cards out as an
    // open list rather than the base page's compact grid.
    document.documentElement.classList.add('has-pack');

    put('.hero .eyebrow', job.eyebrow);
    put('.hero-role', job.role);
    put('.hero-lead', job.lead);
    put('.hero-cta .btn-primary .btn-label', job.cta);
    // On the base page the primary button leads to Experience; an
    // application leads to how Marcus matches the role.
    var primary = document.querySelector('.hero-cta .btn-primary');
    if (primary) primary.setAttribute('href', '#match');

    put('#match .eyebrow', job.matchEyebrow);
    put('#match .sec-title', job.matchTitle);
    put('#match .sec-lead', job.matchLead);

    if (Array.isArray(job.points) && job.points.length) buildPoints(job.points);
    if (job.roles && Array.isArray(job.roles.groups)) buildRoles(job.roles);
    if (Array.isArray(job.built) && job.built.length) addBuilt(job.built);
    if (Array.isArray(job.jobs) && job.jobs.length) addJobs(job.jobs);

    if (job.text) applyText(job.text);

    // Cards and roles the pack built need their "read more" buttons.
    if (window.CVSite) window.CVSite.enhance();

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

    if (window.CVLang) window.CVLang.refresh();
  }

  // The CV for this application: what the job page says, on the CV page.
  // The heading takes the pack's eyebrow, role and lead, and roles the pack
  // adds go at the end of the timeline. "How I match" stays on the web page
  // only. `cv.text` rewrites anything else on cv.html, keyed by CSS
  // selector like `text` on the job page.
  function applyCv(job) {
    put('.cv-top .eyebrow', job.eyebrow);
    put('.cv-top .hero-role', job.role);

    if (job.lead) {
      var role = document.querySelector('.cv-top .hero-role');
      if (role) role.parentNode.insertBefore(text('p', 'cv-profile', job.lead), role.nextSibling);
    }

    if (Array.isArray(job.jobs) && job.jobs.length) addJobs(job.jobs);
    if (job.cv && job.cv.text) applyText(job.cv.text);

    if (job.company) {
      document.title = 'CV — Marcus Hultberg — ' + (job.roleName ? job.roleName + ', ' : '') + job.company;
    }
    var robots = document.createElement('meta');
    robots.name = 'robots';
    robots.content = 'noindex, nofollow';
    document.head.appendChild(robots);

    if (window.CVLang) window.CVLang.refresh();
  }

  // Every PDF link leads to this application's CV, in the language the page
  // is read in at the moment of the click. build_cv_pdf.sh writes both.
  function linkPdf() {
    var base = '/pdf/' + encodeURIComponent(slug) + '/CV Marcus Hultberg';
    document.querySelectorAll('a[href$=".pdf"]').forEach(function (a) {
      a.setAttribute('href', base + '.pdf');
      a.addEventListener('click', function () {
        var sv = window.CVLang && window.CVLang.current() === 'sv';
        a.setAttribute('href', base + (sv ? ' (sv)' : '') + '.pdf');
      });
    });
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

      // The roles the evidence comes from, as job titles from Experience.
      if (Array.isArray(p.roles) && p.roles.length) {
        var roles = el('div', 'point-roles');
        var many = p.roles.length > 1;
        roles.appendChild(text('span', 'point-roles-label',
          { en: many ? 'Roles' : 'Role', sv: many ? 'Roller' : 'Roll' }));
        p.roles.forEach(function (r) { roles.appendChild(text('span', 'pill', r)); });
        body.appendChild(roles);
      }

      card.appendChild(numWrap);
      card.appendChild(body);
      host.appendChild(card);
    });

    if (window.CVSite) window.CVSite.watchReveals(host);
  }

  // "Roles I've recruited for": a card of grouped pills in Experience, between
  // the section heading and the timeline. The base page has its own; a pack
  // that brings `roles` replaces it.
  function buildRoles(roles) {
    var timeline = document.querySelector('#experience .timeline');
    if (!timeline) return;
    var base = document.querySelector('#experience .roles-card');
    if (base) base.parentNode.removeChild(base);

    var card = el('div', 'card roles-card reveal');
    if (roles.title) card.appendChild(text('h3', 'roles-title', roles.title));
    if (roles.lead) card.appendChild(text('p', 'roles-lead', roles.lead));

    var grid = el('div', 'roles-grid');
    roles.groups.forEach(function (g) {
      var group = el('div', 'roles-group');
      group.appendChild(text('p', 'tool-label', g.label));
      var row = el('div', 'pill-row');
      (g.items || []).forEach(function (item) {
        row.appendChild(text('span', 'pill', item));
      });
      group.appendChild(row);
      grid.appendChild(group);
    });
    card.appendChild(grid);

    timeline.parentNode.insertBefore(card, timeline);
    if (window.CVSite) window.CVSite.watchReveals(card.parentNode);
  }

  // Extra cards in "What I've built", for work that belongs on one
  // application but not on the base page. They are appended after the base
  // cards, so `text` selectors that count the base cards still hit the same
  // ones. `group` is "ai" (the "Built myself" grid, the default) or "work";
  // `icon` is a list of SVG path strings in the base icons' 24×24 box.
  function addBuilt(cards) {
    var grids = document.querySelectorAll('#built .built-grid');
    if (!grids.length) return;

    cards.forEach(function (c) {
      var grid = c.group === 'work' ? grids[0] : grids[grids.length - 1];
      // A card brought for one application is shown among the featured
      // projects, not behind "View all projects".
      var card = el('article', 'card built-card reveal' + (c.group === 'work' ? '' : ' is-featured'));

      var icon = el('div', 'built-icon');
      var svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      svg.setAttribute('viewBox', '0 0 24 24');
      svg.setAttribute('stroke-linecap', 'round');
      svg.setAttribute('stroke-linejoin', 'round');
      (c.icon || ['M12 3l2.4 5 5.6.8-4 3.9 1 5.5-5-2.6-5 2.6 1-5.5-4-3.9 5.6-.8z']).forEach(function (d) {
        var path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.setAttribute('d', d);
        svg.appendChild(path);
      });
      icon.appendChild(svg);

      card.appendChild(icon);
      card.appendChild(text('h3', 'built-title', c.title));
      card.appendChild(text('p', 'built-text', c.text));
      grid.appendChild(card);
    });

    if (window.CVSite) window.CVSite.watchReveals(document.querySelector('#built'));
  }

  // Extra roles in the Experience timeline, for work that belongs on one
  // application but not on the base page. They are appended after the base
  // roles, so the timeline should stay newest first: a pack only adds roles
  // older than the last one. Each takes `title`, `date`, `company`, and
  // optionally `place`, `about`, `desc` and `bullets`, in the same markup as
  // the base roles so the theme styles them the same way.
  function addJobs(jobs) {
    var timeline = document.querySelector('#experience .timeline, .cv-main .timeline');
    if (!timeline) return;

    jobs.forEach(function (j) {
      var article = el('article', 'job reveal');

      var head = el('div', 'job-head');
      head.appendChild(text('h3', 'job-title', j.title));
      head.appendChild(text('span', 'job-date', j.date));
      article.appendChild(head);

      // The place sits in a span inside the company line, as in the base
      // markup, which the themes hang their role tags on. The company name is
      // plain text: a translated line would have its span wiped by the
      // language toggle, which rewrites the whole element.
      var company = el('p', 'job-company');
      company.appendChild(document.createTextNode(j.company + ' '));
      if (j.place) company.appendChild(text('span', '', j.place));
      article.appendChild(company);

      if (j.about) article.appendChild(text('p', 'job-about', j.about));
      if (j.desc) article.appendChild(text('p', 'job-desc', j.desc));

      if (Array.isArray(j.bullets) && j.bullets.length) {
        var list = el('ul', 'job-bullets');
        j.bullets.forEach(function (b) { list.appendChild(text('li', '', b)); });
        article.appendChild(list);
      }

      timeline.appendChild(article);
    });

    if (window.CVSite) window.CVSite.watchReveals(timeline);
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
