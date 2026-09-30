import {
  resourceManifest,
  resourceWork,
  resourceWorks,
  resourceFeatured,
  resourceSearch,
  resourceCoverUrl
} from '../../js/resource-fabric-client.mjs';

const ROOT = '/dawn-library';
const cache = new Map();

function path(value) {
  const cleaned = String(value || '').replace(/^\/+/, '');
  if (!cleaned || cleaned.includes('..')) throw new Error('Invalid Dawn Library path');
  return cleaned;
}

async function read(value) {
  const relative = path(value);
  if (!cache.has(relative)) {
    cache.set(relative, fetch(`${ROOT}/${relative}`, {cache: 'force-cache', signal: AbortSignal.timeout(15000)}).then(async response => {
      if (!response.ok) throw new Error(`Dawn Library ${relative}: ${response.status}`);
      return response.json();
    }));
  }
  return cache.get(relative);
}

async function chineseCollection() {
  const collection = await read('chinese-collection.json');
  const preview = await read(collection.coverPreview?.href || 'cover-preview/chinese-collection.json');
  const byWorkId = new Map((preview.items || []).map(item => [item.workId, item.cover || {}]));
  return {
    ...collection,
    works: (collection.works || []).map(work => ({
      ...work,
      cover: {...work.cover, url: byWorkId.get(work.workId)?.src || work.cover?.url || null}
    }))
  };
}

export const dawnLibrary = Object.freeze({
  read,
  manifest: resourceManifest,
  work: resourceWork,
  works: resourceWorks,
  featured: resourceFeatured,
  search: resourceSearch,
  coverUrl: resourceCoverUrl,
  chineseCollection,
  coverPreviewRoot: () => read('cover-preview/root.json'),
  coverPreviewShard: href => read(`cover-preview/${path(href).replace(/^cover-preview\//, '')}`),
  morningStars: () => read('surfaces/dawn-launch.json'),
  readingPacks: () => read('reading-packs/index.json'),
  collections: () => read('collections.json')
});
