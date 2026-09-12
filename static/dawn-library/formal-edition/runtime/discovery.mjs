const DEFAULT_LIMIT = 80;
const DISCOVERY_FACETS = new Set(['relation', 'author', 'chronology', 'readingDepth', 'tags']);

export function normalizeText(value = '') {
  return String(value).normalize('NFKC').toLowerCase().replace(/[^\p{L}\p{N}:]+/gu, ' ').trim();
}

function grams(value) {
  const s = `  ${normalizeText(value)}  `;
  const out = new Set();
  for (let i = 0; i < Math.max(0, s.length - 2); i += 1) out.add(s.slice(i, i + 3));
  return out;
}

export function fuzzyScore(query, value) {
  const q = normalizeText(query);
  const v = normalizeText(value);
  if (!q) return 1;
  if (!v) return 0;
  if (v.includes(q)) return 1;
  const qg = grams(q);
  const vg = grams(v);
  let overlap = 0;
  for (const gram of qg) if (vg.has(gram)) overlap += 1;
  return qg.size ? overlap / qg.size : 0;
}

function recordSearchText(record) {
  return [record.workId, record.title, record.author, ...(record.relations || []), ...(record.tags || [])].filter(Boolean).join(' ');
}

export function buildCatalog({ surface, canonical = null }) {
  const works = canonical?.works || canonical?.items || canonical?.canonicalWorks || [];
  const byId = new Map(Array.isArray(works) ? works.map(work => [work.workId || work.id, work]) : Object.entries(works));
  return (surface?.items || []).filter(item => item?.workId?.startsWith('dawn:')).map(item => {
    const source = byId.get(item.workId) || {};
    return {
      workId: item.workId,
      title: source.title || source.name || '',
      author: source.author || source.creator || '',
      relations: [...new Set(item.relations || [])],
      tags: source.tags || [],
      chronology: source.chronology || source.year || null,
      readingDepth: source.readingDepth || null
    };
  });
}

export function updateDiscoveryContext(context, patch = {}) {
  const facets = patch.facets ? { ...(context.facets || {}), ...patch.facets } : { ...(context.facets || {}) };
  for (const [key, value] of Object.entries(facets)) {
    if (value == null || value === '' || (Array.isArray(value) && value.length === 0)) delete facets[key];
  }
  return {
    ...context,
    ...(Object.hasOwn(patch, 'query') ? { query: patch.query } : {}),
    ...(Object.hasOwn(patch, 'semanticIntent') ? { semanticIntent: patch.semanticIntent } : {}),
    ...(Object.hasOwn(patch, 'ordering') ? { ordering: patch.ordering } : {}),
    ...(Object.hasOwn(patch, 'discoveryDistance') ? { discoveryDistance: patch.discoveryDistance } : {}),
    facets,
    cursor: null
  };
}

function passesFacets(record, facets = {}) {
  for (const [key, selected] of Object.entries(facets)) {
    if (key === 'compareWorks' || !DISCOVERY_FACETS.has(key)) continue;
    if (selected == null || selected === '' || (Array.isArray(selected) && !selected.length)) continue;
    const values = Array.isArray(selected) ? selected : [selected];
    const recordValue = key === 'relation' ? record.relations : record[key];
    const haystack = Array.isArray(recordValue) ? recordValue : [recordValue];
    if (!values.some(value => haystack.includes(value))) return false;
  }
  return true;
}

export function discoverCatalog({ catalog, context, limit = DEFAULT_LIMIT }) {
  const query = context.query || '';
  const threshold = Math.max(0.08, 0.56 - (context.discoveryDistance || 0) * 0.38);
  let rows = catalog.filter(record => passesFacets(record, context.facets));
  rows = rows.map(record => ({ ...record, score: fuzzyScore(query, recordSearchText(record)) }))
    .filter(record => !query || record.score >= threshold);

  const ordering = context.ordering || 'relevance';
  if (ordering === 'title') rows.sort((a, b) => (a.title || a.workId).localeCompare(b.title || b.workId));
  else if (ordering === 'author') rows.sort((a, b) => (a.author || '').localeCompare(b.author || '') || a.workId.localeCompare(b.workId));
  else rows.sort((a, b) => b.score - a.score || a.workId.localeCompare(b.workId));

  return rows.slice(0, Math.max(1, limit));
}

export function facetOptions(catalog, key = 'relation') {
  const counts = new Map();
  for (const record of catalog) {
    const values = key === 'relation' ? record.relations : Array.isArray(record[key]) ? record[key] : [record[key]];
    for (const value of values || []) if (value) counts.set(value, (counts.get(value) || 0) + 1);
  }
  return [...counts.entries()].map(([value, count]) => ({ value, count })).sort((a, b) => b.count - a.count || String(a.value).localeCompare(String(b.value)));
}

export function toggleCompareWork(context, workId, max = 4) {
  if (!workId?.startsWith('dawn:')) throw new Error('Compare requires a canonical dawn:* Work ID');
  const current = [...((context.facets || {}).compareWorks || [])];
  const next = current.includes(workId) ? current.filter(id => id !== workId) : [...current, workId].slice(-max);
  return updateDiscoveryContext(context, {
    facets: { compareWorks: next },
    semanticIntent: next.length > 1 ? 'compare' : context.semanticIntent || ''
  });
}

export function compareSelection({ catalog, context }) {
  const ids = (context.facets || {}).compareWorks || [];
  const byId = new Map(catalog.map(record => [record.workId, record]));
  return ids.map(id => byId.get(id)).filter(Boolean);
}
