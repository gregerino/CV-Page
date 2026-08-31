// Language switcher for Marcus Hultberg's CV site.
//
// Translations live inline in index.html, next to the text they translate:
//   data-sv="..."       swaps textContent
//   data-sv-html="..."  swaps innerHTML (use when the text contains markup)
//   data-sv-ph="..."    swaps an input's placeholder
//
// The element's own content is the English version. When you customise this
// page for a new application you only edit one file, with both languages
// side by side.
(function () {
  'use strict';

  var STORAGE_KEY = 'cv-lang';

  function getLang() {
    return localStorage.getItem(STORAGE_KEY) === 'sv' ? 'sv' : 'en';
  }

  // Remember the English original the first time we touch an element,
  // so switching back is lossless.
  function cache(el, attr, value) {
    if (!el.hasAttribute(attr)) el.setAttribute(attr, value);
    return el.getAttribute(attr);
  }

  function applyLang(lang) {
    document.documentElement.lang = lang;

    document.querySelectorAll('[data-sv]').forEach(function (el) {
      var en = cache(el, 'data-en', el.textContent.trim());
      el.textContent = lang === 'sv' ? el.getAttribute('data-sv') : en;
    });

    document.querySelectorAll('[data-sv-html]').forEach(function (el) {
      var en = cache(el, 'data-en-html', el.innerHTML.trim());
      el.innerHTML = lang === 'sv' ? el.getAttribute('data-sv-html') : en;
    });

    document.querySelectorAll('[data-sv-ph]').forEach(function (el) {
      var en = cache(el, 'data-en-ph', el.placeholder);
      el.placeholder = lang === 'sv' ? el.getAttribute('data-sv-ph') : en;
    });

    document.querySelectorAll('.lang-toggle').forEach(function (b) {
      b.textContent = lang === 'sv' ? 'EN' : 'SV';
      b.title = lang === 'sv' ? 'Switch to English' : 'Byt till svenska';
    });
  }

  function setLang(lang) {
    localStorage.setItem(STORAGE_KEY, lang);
    applyLang(lang);
  }

  function createToggle() {
    var host = document.querySelector('.nav-actions');
    if (!host) return;
    var btn = document.createElement('button');
    btn.className = 'lang-toggle';
    btn.type = 'button';
    btn.onclick = function () { setLang(getLang() === 'en' ? 'sv' : 'en'); };
    host.insertBefore(btn, host.firstChild);
  }

  createToggle();
  applyLang(getLang());
})();
