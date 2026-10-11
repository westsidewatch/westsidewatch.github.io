// Cap completed shared cities; protected active layers can never be evicted.
// Staging generation and the canonical Herodian city are outside this cache.
export function trimCityCache(entries, { limit, protectedIds, lastUsed }) {
  if (!Number.isInteger(limit) || limit < 2) throw new Error('City cache requires at least two slots');
  const residents = entries.filter(entry => entry.runtime.status === 'ready');
  const candidates = residents.filter(entry => !protectedIds.has(entry.id))
    .sort((a,b) => (lastUsed.get(a.id) || 0) - (lastUsed.get(b.id) || 0));
  const evicted = [];
  while (residents.length - evicted.length > limit && candidates.length) {
    const entry = candidates.shift();
    entry.runtime.evict(); evicted.push(entry.id);
  }
  return evicted;
}
