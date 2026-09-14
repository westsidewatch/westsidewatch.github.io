// DORÉ Cover Resolver — canonical/local runtime only.
// External catalogs belong to discovery/reconciliation, never to browser runtime.
import {canonicalCover,canonicalIndex} from './canonical-library.mjs';

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
    provenance: cover?.provenance || 'local cover',
  };
}

function canonicalWorkId(book) {
  return String(
    book?.library?.canonicalWorkId ||
    book?.canonical?.workId ||
    book?.workId ||
    ''
  ).trim();
}

async function dawnCover(book) {
  const workId = canonicalWorkId(book);
  if (!workId) return null;
  const index = await canonicalIndex();
  const work = index?.works?.[workId];
  if (!work) return null;
  return canonicalCover(work);
}

export async function resolveCover(book) {
  if (!book) return null;
  return localCover(book) || await dawnCover(book);
}
