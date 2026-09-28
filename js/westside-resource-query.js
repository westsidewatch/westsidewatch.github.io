(() => {
  'use strict';

  const ROOT = '/data/westside-index';
  const ALLOWED_INDEXES = new Set([
    'by-type', 'by-speaker', 'by-series', 'by-scripture',
    'by-theme', 'by-place', 'by-ministry', 'by-language'
  ]);
  const encodeKey = (value) => encodeURIComponent(String(value).trim());
  async function fetchJson(path) {
    const response = await fetch(path, { credentials: 'same-origin' });
    if (!response.ok) throw new Error(`Westside Core query failed: ${response.status} ${path}`);
    return response.json();
  }
  async function index(indexName, key) {
    if (!ALLOWED_INDEXES.has(indexName)) throw new Error(`Westside Core index not allowed: ${indexName}`);
    if (key === undefined || key === null || String(key).trim() === '') throw new Error('Westside Core scoped query requires a key');
    return fetchJson(`${ROOT}/${indexName}/${encodeKey(key)}.json`);
  }
  async function resource(id) {
    if (!id) throw new Error('Westside Core resource query requires an id');
    return fetchJson(`${ROOT}/by-id/${encodeKey(id)}.json`);
  }
  async function selection(id) {
    if (!id) throw new Error('Westside Core editorial selection requires an id');
    return fetchJson(`${ROOT}/selection/${encodeKey(id)}.json`);
  }
  async function query(spec = {}) {
    if (spec.resource) return resource(spec.resource);
    if (spec.selection) return selection(spec.selection);
    if (spec.index && Object.prototype.hasOwnProperty.call(spec, 'key')) return index(spec.index, spec.key);
    throw new Error('Westside Core query must use resource, selection, or scoped index + key');
  }
  window.WestsideResources = Object.freeze({ query, index, resource, selection });
})();
