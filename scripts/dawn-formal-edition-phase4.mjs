import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import { buildCatalog, discoverCatalog, discoverCatalogWindow, updateDiscoveryContext, facetOptions, toggleCompareWork, compareSelection } from '../static/dawn-library/formal-edition/runtime/discovery.mjs';
import { serializeContext, restoreContext } from '../static/dawn-library/formal-edition/runtime/relation-context.mjs';

const surface = JSON.parse(await fs.readFile(new URL('../static/dawn-library/surfaces/multiwrite-biblical-world.json', import.meta.url), 'utf8'));
const canonical = JSON.parse(await fs.readFile(new URL('../static/dawn-library/canonical-index.json', import.meta.url), 'utf8'));
const initialContext = JSON.parse(await fs.readFile(new URL('../static/dawn-library/formal-edition/contexts/second-temple.v1.json', import.meta.url), 'utf8'));
const catalog = buildCatalog({ surface, canonical });

assert.ok(catalog.length >= 10000, `Phase 4 requires the real 10k+ canonical catalog; got ${catalog.length}`);
assert.ok(catalog.every(item => item.workId.startsWith('dawn:')), 'Every discovery row must retain canonical dawn:* identity');

let context = structuredClone(initialContext);
const firstWindow = discoverCatalogWindow({ catalog, context, windowSize: 72 });
assert.equal(firstWindow.items.length, 72, 'Large catalog projection must cap the rendered window');
assert.ok(firstWindow.total >= 10000);
assert.ok(firstWindow.nextCursor, '10k+ catalog must expose a next cursor');
context = updateDiscoveryContext(context, { cursor: firstWindow.nextCursor });
const secondWindow = discoverCatalogWindow({ catalog, context, windowSize: 72 });
assert.equal(secondWindow.offset, 72);
assert.equal(secondWindow.items.length, 72);
assert.ok(secondWindow.items.every(item => item.workId.startsWith('dawn:')));

context = updateDiscoveryContext(context, { cursor: null, query: 'second temple', discoveryDistance: 0.85 });
const fuzzy = discoverCatalog({ catalog, context, limit: 72 });
assert.ok(fuzzy.length > 0, 'Fuzzy search must produce results against the full canonical catalog');

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
  catalogSize: catalog.length,
  renderWindow: firstWindow.items.length,
  secondWindowOffset: secondWindow.offset,
  fuzzyResults: fuzzy.length,
  relationFacetResults: filtered.length,
  compareWorks: compared.map(item => item.workId),
  contextSchema: restored.schema
}, null, 2));
