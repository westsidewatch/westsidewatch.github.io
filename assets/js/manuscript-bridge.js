/* Westside Watch Manuscript Bridge
 * Shared, dependency-free reader/edit coordination layer.
 * Keeps long Markdown addressable by heading/range without coupling consumers
 * to a CMS or to a specific reader UI.
 */
(function (global) {
  'use strict';

  const VERSION = '1.0.0';

  function normalize(text) {
    return String(text || '').replace(/\r\n?/g, '\n');
  }

  function slug(text) {
    return String(text || '')
      .replace(/[*_`~[\]()]/g, '')
      .trim()
      .toLowerCase()
      .replace(/\s+/g, '-')
      .replace(/[^\p{L}\p{N}\-]+/gu, '')
      .replace(/-+/g, '-');
  }

  function headings(text) {
    const lines = normalize(text).split('\n');
    const out = [];
    lines.forEach((line, index) => {
      const m = line.match(/^(#{1,6})\s+(.+?)\s*$/);
      if (!m) return;
      out.push({
        level: m[1].length,
        title: m[2].replace(/[*_`]/g, '').trim(),
        raw: line,
        line: index + 1,
        index,
        id: slug(m[2])
      });
    });
    return out;
  }

  function section(text, selector) {
    const source = normalize(text);
    const lines = source.split('\n');
    const hs = headings(source);
    const wanted = typeof selector === 'string' ? { title: selector } : (selector || {});
    const start = hs.find(h =>
      (wanted.id && h.id === wanted.id) ||
      (wanted.title && h.title === wanted.title) ||
      (wanted.line && h.line === Number(wanted.line))
    );
    if (!start) return null;
    const next = hs.find(h => h.index > start.index && h.level <= start.level);
    const endIndex = next ? next.index : lines.length;
    return {
      heading: start,
      startLine: start.line,
      endLine: endIndex,
      text: lines.slice(start.index, endIndex).join('\n').replace(/\n+$/, '') + '\n'
    };
  }

  function replaceSection(text, selector, replacement) {
    const source = normalize(text);
    const part = section(source, selector);
    if (!part) throw new Error('Manuscript section not found');
    const lines = source.split('\n');
    const before = lines.slice(0, part.startLine - 1);
    const after = lines.slice(part.endLine);
    const insert = normalize(replacement).replace(/^\n+|\n+$/g, '').split('\n');
    return [...before, ...insert, ...after].join('\n').replace(/\n{3,}/g, '\n\n');
  }

  function sourceWithRevision(url, revision) {
    const u = new URL(url, global.location && global.location.href || undefined);
    u.searchParams.set('_rev', revision || Date.now().toString(36));
    return u.toString();
  }

  async function read(url, options) {
    const opts = options || {};
    const target = opts.fresh === false ? url : sourceWithRevision(url, opts.revision);
    const response = await fetch(target, { cache: opts.fresh === false ? 'default' : 'no-store' });
    if (!response.ok) throw new Error(`Manuscript read failed (${response.status})`);
    const text = normalize(await response.text());
    return { text, headings: headings(text), url };
  }

  function rememberPosition(key) {
    if (!global.sessionStorage) return;
    const value = JSON.stringify({ y: global.scrollY || 0, at: Date.now() });
    global.sessionStorage.setItem(`manuscript:${key}:position`, value);
  }

  function restorePosition(key) {
    if (!global.sessionStorage) return false;
    const raw = global.sessionStorage.getItem(`manuscript:${key}:position`);
    if (!raw) return false;
    try {
      const saved = JSON.parse(raw);
      requestAnimationFrame(() => global.scrollTo(0, Number(saved.y) || 0));
      return true;
    } catch (_) { return false; }
  }

  function nearestHeading(root) {
    if (!root) return null;
    const hs = [...root.querySelectorAll('h1,h2,h3,h4,h5,h6')];
    let current = null;
    for (const h of hs) {
      if (h.getBoundingClientRect().top <= Math.max(120, global.innerHeight * .28)) current = h;
      else break;
    }
    return current ? { title: current.textContent.trim(), id: current.id || slug(current.textContent) } : null;
  }

  function rememberAnchor(key, root) {
    const anchor = nearestHeading(root);
    if (!anchor || !global.sessionStorage) return rememberPosition(key);
    global.sessionStorage.setItem(`manuscript:${key}:anchor`, JSON.stringify(anchor));
    rememberPosition(key);
  }

  function restoreAnchor(key, root) {
    if (!global.sessionStorage || !root) return restorePosition(key);
    const raw = global.sessionStorage.getItem(`manuscript:${key}:anchor`);
    if (!raw) return restorePosition(key);
    try {
      const saved = JSON.parse(raw);
      const target = [...root.querySelectorAll('h1,h2,h3,h4,h5,h6')]
        .find(h => (h.id && h.id === saved.id) || h.textContent.trim() === saved.title);
      if (!target) return restorePosition(key);
      requestAnimationFrame(() => target.scrollIntoView({ block: 'start' }));
      return true;
    } catch (_) { return restorePosition(key); }
  }

  global.ManuscriptBridge = Object.freeze({
    version: VERSION,
    normalize,
    slug,
    headings,
    section,
    replaceSection,
    sourceWithRevision,
    read,
    rememberPosition,
    restorePosition,
    rememberAnchor,
    restoreAnchor
  });
})(window);
