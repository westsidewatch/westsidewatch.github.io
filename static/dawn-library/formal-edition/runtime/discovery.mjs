const DEFAULT_LIMIT = 72;
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

export function canonicalWorks(canonical) {
  if (!canonical) return [];
  const candidates = [canonical.works, canonical.items, canonical.canonicalWorks, canonical.catalog, canonical.index];
  for (const candidate of candidates) {
    if (Array.isArray(candidate)) return candidate;
    if (candidate && typeof candidate === 'object') {
      return Object.entries(candidate).map(([key, value]) => ({ ...(value || {}), workId: value?.workId || value?.id || key }));
    }
  }
  if (Array.isArray(canonical)) return canonical;
  return [];
}

export function buildCatalog({ surface, canonical = null }) {
  const surfaceById = new Map((surface?.items || []).filter(item => item?.workId).map(item => [String(item.workId), item]));
  const canonicalRows = canonicalWorks(canonical).filter(item => String(item?.workId || item?.id || '').trim());
  const sourceRows = canonicalRows.length ? canonicalRows : [...surfaceById.values()];

  return sourceRows.map(source => {
    const workId = String(source.workId || source.id);
    const overlay = surfaceById.get(workId) || {};
    const metadata = source.metadata || {};
    const authors = source.authors || metadata.authors || [];
    return {
      workId,
      title: source.title || source.name || metadata.title || '',
      author: source.author || source.creator || metadata.author || metadata.creator || (Array.isArray(authors) ? authors.join(', ') : String(authors || '')),
      relations: [...new Set([...(overlay.relations || []), ...(source.relations || [])])],
      tags: source.tags || metadata.tags || [],
      chronology: source.chronology || source.firstPublishYear || source.year || metadata.year || null,
      readingDepth: source.readingDepth || metadata.readingDepth || null,
      authorityBacked: Boolean(source.authorityBacked)
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
    ...(Object.hasOwn(patch, 'cursor') ? { cursor: patch.cursor } : { cursor: null }),
    facets
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

function rankedRows({ catalog, context }) {
  const query = context.query || '';
  const threshold = Math.max(0.08, 0.56 - (context.discoveryDistance || 0) * 0.38);
  const rows = catalog.filter(record => passesFacets(record, context.facets))
    .map(record => ({ ...record, score: fuzzyScore(query, recordSearchText(record)) }))
    .filter(record => !query || record.score >= threshold);

  const ordering = context.ordering || 'relevance';
  if (ordering === 'title') rows.sort((a, b) => (a.title || a.workId).localeCompare(b.title || b.workId));
  else if (ordering === 'author') rows.sort((a, b) => (a.author || '').localeCompare(b.author || '') || a.workId.localeCompare(b.workId));
  else rows.sort((a, b) => b.score - a.score || a.workId.localeCompare(b.workId));
  return rows;
}

export function discoverCatalog({ catalog, context, limit = DEFAULT_LIMIT }) {
  return rankedRows({ catalog, context }).slice(0, Math.max(1, limit));
}

export function discoverCatalogWindow({ catalog, context, windowSize = DEFAULT_LIMIT }) {
  const rows = rankedRows({ catalog, context });
  const size = Math.max(1, windowSize);
  const requestedOffset = Number(context.cursor?.offset || 0);
  const maxOffset = Math.max(0, Math.floor(Math.max(0, rows.length - 1) / size) * size);
  const offset = Math.min(Math.max(0, requestedOffset), maxOffset);
  const items = rows.slice(offset, offset + size);
  return {
    total: rows.length,
    offset,
    windowSize: size,
    items,
    previousCursor: offset > 0 ? { offset: Math.max(0, offset - size) } : null,
    nextCursor: offset + size < rows.length ? { offset: offset + size } : null
  };
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
  const id = String(workId || '').trim();
  if (!id) throw new Error('Compare requires a canonical Work ID');
  const current = [...((context.facets || {}).compareWorks || [])];
  const next = current.includes(id) ? current.filter(value => value !== id) : [...current, id].slice(-max);
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
