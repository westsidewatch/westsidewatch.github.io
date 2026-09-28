(() => {
  'use strict';

  const ROOT = '/data/westside-index';
  const ALLOWED_INDEXES = new Set([
    'by-type', 'by-speaker', 'by-series', 'by-scripture',
    'by-theme', 'by-place', 'by-ministry', 'by-language'
  ]);
  const PREFIX = {
    'by-speaker': 'speaker:',
    'by-series': 'series:',
    'by-scripture': 'scripture:',
    'by-theme': 'theme:',
    'by-place': 'place:',
    'by-ministry': 'ministry:',
    'by-language': 'language:',
    'by-type': 'type:'
  };
  const slug = value => String(value).trim().replace(/^\/+|\/+$/g, '').replace(/:/g, '-').replace(/\s+/g, '-').toLowerCase();
  const scopedKey = (indexName, value) => {
    const raw = String(value).trim();
    const prefix = PREFIX[indexName];
    return slug(prefix && raw.startsWith(prefix) ? raw.slice(prefix.length) : raw);
  };
  async function fetchJson(path) {
    const response = await fetch(path, { credentials: 'same-origin' });
    if (!response.ok) throw new Error(`Westside Core scoped query failed: ${response.status} ${path}`);
    return response.json();
  }
  async function index(indexName, key) {
    if (!ALLOWED_INDEXES.has(indexName)) throw new Error(`Westside Core index not allowed: ${indexName}`);
    if (key === undefined || key === null || String(key).trim() === '') throw new Error('Westside Core scoped query requires a key');
    return fetchJson(`${ROOT}/${indexName}/${encodeURIComponent(scopedKey(indexName, key))}.json`);
  }
  async function resource(id) {
    if (!id) throw new Error('Westside Core resource query requires an id');
    return fetchJson(`${ROOT}/by-id/${encodeURIComponent(slug(id))}.json`);
  }
  async function selection(id) {
    if (!id) throw new Error('Westside Core editorial selection requires an id');
    return fetchJson(`${ROOT}/selection/${encodeURIComponent(slug(id))}.json`);
  }
  async function query(spec = {}) {
    if (spec.resource) return resource(spec.resource);
    if (spec.selection) return selection(spec.selection);
    if (spec.index && Object.prototype.hasOwnProperty.call(spec, 'key')) return index(spec.index, spec.key);
    throw new Error('Westside Core query must use resource, selection, or scoped index + key');
  }
  window.WestsideResources = Object.freeze({ query, index, resource, selection });
})();
