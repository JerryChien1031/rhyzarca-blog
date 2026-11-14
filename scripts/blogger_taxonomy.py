"""Publish canonical category UI with page HTML, not a browser-cached theme script.

The old theme asset can stay in readers' browser caches for seven days.
A CDN purge cannot invalidate those copies. This idempotent runtime uses the
same canonical taxonomy as the theme and does not modify article sources.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
RUNTIME = r"""(function () {
  'use strict';
  if (location.hostname !== 'blog.rhyzarca.com') return;
  var version = '__VERSION__';
  if (window.__rhyzarcaPublishedTaxonomy === version) return;
  window.__rhyzarcaPublishedTaxonomy = version;
  var categories = __CATEGORIES__;
  var scheduled = false;
  function categoryFor(path) {
    var match = path.match(/^\/search\/label\/([^/]+)\/?$/);
    if (!match) return null;
    var value;
    try { value = decodeURIComponent(match[1]); } catch (error) { return null; }
    return categories.find(function (item) {
      return item.id === value || item.aliases.indexOf(value) !== -1;
    }) || null;
  }
  function linkTo(href, text) {
    var a = document.createElement('a');
    a.href = href;
    a.className = 'nav-link';
    a.textContent = text;
    return a;
  }
  function render() {
    scheduled = false;
    var nav = document.getElementById('rhyzarca-nav');
    var header = document.querySelector('.header-outer, #header, .header, header, .Header');
    if (!nav && header && header.parentNode) {
      nav = document.createElement('nav');
      nav.id = 'rhyzarca-nav';
      var box = document.createElement('div');
      box.className = 'nav-container';
      box.appendChild(linkTo('/', '首頁'));
      box.appendChild(linkTo('/p/about.html', '關於我'));
      categories.forEach(function (item) {
        box.appendChild(linkTo('/search/label/' + item.id, item.name + ' (' + item.english + ')'));
      });
      nav.appendChild(box);
      header.parentNode.insertBefore(nav, header.nextSibling);
    }
    document.querySelectorAll('a[href*="/search/label/"]').forEach(function (link) {
      var url;
      try { url = new URL(link.href, location.href); } catch (error) { return; }
      if (url.origin !== location.origin) return;
      var item = categoryFor(url.pathname);
      if (!item) return;
      var inNav = !!link.closest('#rhyzarca-nav');
      var text = link.textContent.trim();
      var isRaw = text === item.id || item.aliases.indexOf(text) !== -1;
      var isLegacyPractice = item.id === 'architecture' && /^(系統日誌|實作日誌)(\s*\([^)]*\))?$/.test(text);
      if (inNav || isRaw || isLegacyPractice) {
        var label = inNav ? item.name + ' (' + item.english + ')' : item.name;
        if (link.textContent !== label) link.textContent = label;
        if (url.pathname !== '/search/label/' + item.id) link.href = '/search/label/' + item.id + url.search + url.hash;
      }
    });
    if (nav) nav.setAttribute('data-published-taxonomy', version);
    var current = categoryFor(location.pathname);
    var posts = document.querySelector('#Blog1 .blog-posts, .blog-posts');
    if (current && posts) {
      var section = document.getElementById('rhyzarca-category-description');
      if (!section) {
        section = document.createElement('section');
        section.id = 'rhyzarca-category-description';
        section.style.cssText = 'margin:0 0 1.5rem;padding:1rem;max-width:100%;box-sizing:border-box;overflow-wrap:anywhere;';
        section.appendChild(document.createElement('h2'));
        section.appendChild(document.createElement('p'));
        posts.parentNode.insertBefore(section, posts);
      }
      var heading = section.querySelector('h2');
      var summary = section.querySelector('p');
      if (heading && heading.textContent !== current.name) heading.textContent = current.name;
      if (summary && summary.textContent !== current.summary) summary.textContent = current.summary;
    }
  }
  function schedule() {
    if (!scheduled) { scheduled = true; requestAnimationFrame(render); }
  }
  render();
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', render, {once:true});
  window.addEventListener('pageshow', render);
  if (document.body) new MutationObserver(schedule).observe(document.body, {childList:true, subtree:true});
}());"""


def render_category_runtime(categories=None) -> str:
    """Embed public canonical taxonomy safely; repeated index entries run once."""
    if categories is None:
        categories = json.loads((ROOT / '_data/blog_categories.json').read_text(encoding='utf-8'))
    payload = json.dumps(categories, ensure_ascii=True, separators=(',', ':'))
    payload = payload.replace('<', r'\u003c').replace('>', r'\u003e').replace('&', r'\u0026')
    version = hashlib.sha256(payload.encode('utf-8')).hexdigest()[:16]
    source = RUNTIME.replace('__VERSION__', version).replace('__CATEGORIES__', payload)
    return '\n<script data-rhyzarca-taxonomy="' + version + '">' + source + '</script>\n'
