import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import { buildCatalog, discoverCatalog, discoverCatalogWindow, updateDiscoveryContext, facetOptions, toggleCompareWork, compareSelection } from '../static/dawn-library/formal-edition/runtime/discovery.mjs';
import { serializeContext, restoreContext } from '../static/dawn-library/formal-edition/runtime/relation-context.mjs';

const surface = JSON.parse(await fs.readFile(new URL('../static/dawn-library/surfaces/multiwrite-biblical-world.json', import.meta.url), 'utf8'));
const canonical = JSON.parse(await fs.readFile(new URL('../static/dawn-library/canonical-index.json', import.meta.url), 'utf8'));
const initialContext = JSON.parse(await fs.readFile(new URL('../static/dawn-library/formal-edition/contexts/second-temple.v1.json', import.meta.url), 'utf8'));
const catalog = buildCatalog({ surface, canonical });
const canonicalIds = new Set(Object.keys(canonical.works || {}));

assert.equal(canonical.schema, 'dawn.library.canonical-index.v1');
assert.equal(canonical.identityAuthority, 'Dawn');
assert.ok(canonical.workCount >= 10000, `Canonical index baseline is below 10k: ${canonical.workCount}`);
assert.equal(catalog.length, canonical.workCount, `Phase 4 must expose every canonical Work; catalog=${catalog.length}, canonical=${canonical.workCount}`);
assert.equal(canonicalIds.size, canonical.workCount);
assert.ok(catalog.every(item => canonicalIds.has(item.workId)), 'Every discovery row must be a Work ID owned by the Dawn canonical index');
assert.ok(catalog.some(item => item.workId.startsWith('dawn:')), 'Fallback dawn:* IDs must remain supported');
assert.ok(catalog.some(item => !item.workId.startsWith('dawn:')), 'Authority-backed canonical IDs must remain supported without rewriting');

let context = structuredClone(initialContext);
const firstWindow = discoverCatalogWindow({ catalog, context, windowSize: 72 });
assert.equal(firstWindow.items.length, 72, 'Large catalog projection must cap the rendered window');
assert.equal(firstWindow.total, canonical.workCount);
assert.ok(firstWindow.nextCursor, '10k+ catalog must expose a next cursor');
context = updateDiscoveryContext(context, { cursor: firstWindow.nextCursor });
const secondWindow = discoverCatalogWindow({ catalog, context, windowSize: 72 });
assert.equal(secondWindow.offset, 72);
assert.equal(secondWindow.items.length, 72);
assert.ok(secondWindow.items.every(item => canonicalIds.has(item.workId)));

context = updateDiscoveryContext(context, { cursor: null, query: 'second temple', discoveryDistance: 0.85 });
const fuzzy = discoverCatalog({ catalog, context, limit: 72 });
assert.ok(fuzzy.length > 0, 'Fuzzy search must produce results against the full canonical catalog');
assert.ok(fuzzy.every(item => canonicalIds.has(item.workId)));

context = updateDiscoveryContext(context, { query: '', facets: { relation: '第二聖殿' } });
const filtered = discoverCatalog({ catalog, context, limit: 72 });
assert.ok(filtered.length > 0, 'Surface relation facets must still work after canonical expansion');
assert.ok(filtered.every(item => item.relations.includes('第二聖殿')));
assert.ok(facetOptions(catalog, 'relation').some(item => item.value === '第二聖殿'));

const compareIds = surface.items.slice(0, 2).map(item => item.workId);
context = updateDiscoveryContext(context, { facets: { relation: null }, ordering: 'title' });
for (const workId of compareIds) context = toggleCompareWork(context, workId);
const compared = compareSelection({ catalog, context });
assert.deepEqual(compared.map(item => item.workId), compareIds);
assert.equal(context.semanticIntent, 'compare');

const restored = restoreContext(serializeContext(context));
assert.deepEqual(restored.facets.compareWorks, context.facets.compareWorks, 'Compare selection must survive CollectionContext serialization');
assert.equal(restored.ordering, 'title');

console.log(JSON.stringify({
  phase: 4,
  status: 'PASS',
  canonicalWorkCount: canonical.workCount,
  authorityBackedWorks: canonical.authorityBackedWorks,
  fallbackDawnIds: catalog.filter(item => item.workId.startsWith('dawn:')).length,
  renderWindow: firstWindow.items.length,
  secondWindowOffset: secondWindow.offset,
  fuzzyResults: fuzzy.length,
  relationFacetResults: filtered.length,
  compareWorks: compared.map(item => item.workId),
  contextSchema: restored.schema
}, null, 2));
