// DORÉ Cover Resolver — canonical/local runtime only.
// External catalogs belong to discovery/reconciliation, never to browser runtime.
const FORBIDDEN = /(?:openlibrary\.org|wikisource|zh\.wikisource\.org)/i;

function localCover(book) {
  const cover = book?.cover;
  const url = String(cover?.url || '');
  if (!url || FORBIDDEN.test(url)) return null;
  if (!url.startsWith('/')) return null;
  return {
    url,
    kind: cover?.kind || 'canonical-local',
    provider: cover?.provider || 'Dawn',
    provenance: cover?.provenance || 'Dawn canonical index',
  };
}

export async function resolveCover(book) {
  if (!book) return null;
  return localCover(book);
}
