import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';

const staticRoot = new URL('../static/', import.meta.url);
let sequence = 0;
async function fixture(run) {
  const original = globalThis.fetch, requests = [];
  globalThis.fetch = async url => {
    requests.push(String(url));
    const body = await readFile(new URL(String(url).replace(/^\//, ''), staticRoot), 'utf8');
    return new Response(body, {status: 200});
  };
  try {
    const api = await import(`../static/js/resource-fabric-client.mjs?test=${sequence++}`);
    await run(api, requests);
  } finally { globalThis.fetch = original; }
}

test('three morning stars resolve without scanning the entire canonical corpus', async () => {
  await fixture(async (api, requests) => {
    const morning = JSON.parse(await readFile(new URL('dawn-library/surfaces/dawn-launch.json', staticRoot)));
    const ids = morning.items.map(item => item.workId);
    const works = await api.resourceWorks(ids);
    assert.equal(works.size, 3);
    for (const id of ids) assert.equal(works.get(id).workId, id);
    const canonical = requests.filter(url => /canonical\/works-/.test(url));
    assert.ok(canonical.length <= 2, `Expected at most 2 targeted shards, got ${canonical.length}`);
    assert.equal(new Set(canonical).size, canonical.length, 'concurrent identities share the shard fetch');
    assert.ok(requests.every(url => url.startsWith('/dawn-library/')));
  });
});

test('featured collection loads only the visible 24 canonical works', async () => {
  await fixture(async (api, requests) => {
    const works = await api.resourceFeatured({limit: 24});
    assert.equal(works.length, 24);
    assert.equal(new Set(works.map(work => work.workId)).size, 24);
    assert.ok(requests.filter(url => /resource-fabric\/work-/.test(url)).length <= 24);
  });
});

test('search and selecting a preview preserve the canonical Work identity', async () => {
  await fixture(async api => {
    const works = await api.resourceSearch('Spurgeon');
    assert.ok(works.some(work => work.authors.join(' ').includes('Spurgeon')));
    const selected = await api.resourceWork('OL1000886W');
    assert.equal(selected.workId, 'OL1000886W');
    assert.equal(selected.title.toLowerCase(), 'the radical prayer');
    const manifest = await api.resourceManifest();
    assert.ok(manifest.workCount > 200000);
  });
});

test('Reader uses a published bilingual pack and never fetches the provider text', async () => {
  const original = globalThis.fetch, requests = [];
  globalThis.fetch = async url => {
    const path = String(url);
    requests.push(path);
    const body = await readFile(new URL(path.replace(/^\//, ''), staticRoot), 'utf8');
    return new Response(body, {status: 200});
  };
  try {
    const reader = await import(`../static/js/dawn-reading-resolver.mjs?test=${sequence++}`);
    const workId = 'dawn:dbdea4adcc7625e7d64e';
    const result = await reader.resolveReading({workId, authorityIds: {}, edition: {}});
    const pack = await reader.localReadingPack(workId);
    assert.equal(result.kind, 'external-reader');
    assert.equal(result.sourcePage, 'https://www.gutenberg.org/ebooks/395');
    assert.equal(pack.workId, workId);
    assert.equal(pack.segments.length, 3);
    assert.equal(reader.readingTranslationCapability({...result, pack}).mode, 'local-reading-pack');
    assert.ok(requests.every(url => url.startsWith('/dawn-library/')),
      `Reader must not fetch external text: ${requests.join(', ')}`);
  } finally { globalThis.fetch = original; }
});

test('Chinese Collection preserves the bookstore card contract and a full-text entry', async () => {
  const collection = JSON.parse(await readFile(new URL('dawn-library/chinese-collection.json', staticRoot)));
  assert.equal(collection.schema, 'dawn.library.collection-index.v1');
  assert.equal(collection.count, 47);
  assert.equal(collection.works.length, 47);
  const fullText = collection.works.find(item => item.access?.kind === 'full-text');
  assert.equal(fullText.work.title, '靈歷集光');
  assert.equal(fullText.access.url, 'https://www.gutenberg.org/cache/epub/25716/pg25716-images.html');
  assert.match(fullText.cover.url, /^https:\/\//);
  assert.ok(collection.works.every(item => item.work?.title && item.source?.provider && item.access?.url));
  assert.ok(collection.works.every(item => ['source', 'one-fallback'].includes(item.cover?.mode)));
  assert.equal(collection.coverPreview.href, 'cover-preview/chinese-collection.json');
  const preview = JSON.parse(await readFile(new URL('dawn-library/cover-preview/chinese-collection.json', staticRoot)));
  assert.equal(preview.schema, 'dawn.library.cover-preview-shard.v1');
  assert.equal(preview.count, collection.count);
  assert.deepEqual(preview.items.map(item => item.workId), collection.works.map(item => item.workId));
  const product = await readFile(new URL('dawn-library/product/bookstore.mjs', staticRoot), 'utf8');
  assert.doesNotMatch(product, /封面待解析|閱讀入口待解析|來源整理中/);
});

test('the bookstore reads its catalogue, Chinese collection, and cover projections through one Library client', async () => {
  await fixture(async (fabric, requests) => {
    const library = await import(`../static/dawn-library/product/library-system.mjs?test=${sequence++}`);
    const [manifest, chinese, previews] = await Promise.all([
      library.dawnLibrary.manifest(), library.dawnLibrary.chineseCollection(), library.dawnLibrary.coverPreviewRoot()
    ]);
    assert.ok(manifest.workCount > 200000);
    assert.equal(chinese.works.length, 47);
    assert.equal(previews.workCount, manifest.workCount);
    assert.ok(requests.includes('/dawn-library/chinese-collection.json'));
    assert.ok(requests.includes('/dawn-library/cover-preview/chinese-collection.json'));
  });
});
