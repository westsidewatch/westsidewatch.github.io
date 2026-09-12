import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import { buildCatalog, discoverCatalog, updateDiscoveryContext, facetOptions, toggleCompareWork, compareSelection } from '../static/dawn-library/formal-edition/runtime/discovery.mjs';
import { serializeContext, restoreContext } from '../static/dawn-library/formal-edition/runtime/relation-context.mjs';

const surface = JSON.parse(await fs.readFile(new URL('../static/dawn-library/surfaces/multiwrite-biblical-world.json', import.meta.url), 'utf8'));
const initialContext = JSON.parse(await fs.readFile(new URL('../static/dawn-library/formal-edition/contexts/second-temple.v1.json', import.meta.url), 'utf8'));

const canonicalProbe = {
  works: [
    { workId: 'dawn:4ef73b08ef18424f1900', title: 'Second Temple History', author: 'A' },
    { workId: 'dawn:157e63ed1adf50df2385', title: 'Jerusalem in the Second Temple', author: 'B' },
    { workId: 'dawn:c27499c2be405628d9a9', title: 'Early Church Fathers', author: 'C' }
  ]
};

const catalog = buildCatalog({ surface, canonical: canonicalProbe });
assert.ok(catalog.length >= 20, 'Phase 4 must operate on the real canonical-backed surface, not a tiny demo catalog');
assert.ok(catalog.every(item => item.workId.startsWith('dawn:')), 'Every discovery row must retain canonical dawn:* identity');

let context = structuredClone(initialContext);
context = updateDiscoveryContext(context, { query: 'Jeruslem', discoveryDistance: 0.85 });
const fuzzy = discoverCatalog({ catalog, context });
assert.equal(fuzzy[0]?.workId, 'dawn:157e63ed1adf50df2385', 'Fuzzy search must recover a misspelled Jerusalem query when canonical metadata is available');

context = updateDiscoveryContext(context, { query: '', facets: { relation: '第二聖殿' } });
const filtered = discoverCatalog({ catalog, context });
assert.ok(filtered.length >= 3, 'Facet filtering must work over the real surface relations');
assert.ok(filtered.every(item => item.relations.includes('第二聖殿')));

const relationFacets = facetOptions(catalog, 'relation');
assert.ok(relationFacets.some(item => item.value === '第二聖殿' && item.count >= 3), 'Facet counts must be derived from the same canonical-backed catalog');

context = updateDiscoveryContext(context, { facets: { relation: null }, ordering: 'title' });
context = toggleCompareWork(context, 'dawn:4ef73b08ef18424f1900');
context = toggleCompareWork(context, 'dawn:c27499c2be405628d9a9');
const compared = compareSelection({ catalog, context });
assert.deepEqual(compared.map(item => item.workId), ['dawn:4ef73b08ef18424f1900', 'dawn:c27499c2be405628d9a9']);
assert.equal(context.semanticIntent, 'compare');

const restored = restoreContext(serializeContext(context));
assert.deepEqual(restored.facets.compareWorks, context.facets.compareWorks, 'Compare selection must survive CollectionContext serialization');
assert.equal(restored.ordering, 'title');
assert.equal(restored.focusedWork, context.focusedWork ?? null);

console.log(JSON.stringify({
  phase: 4,
  status: 'PASS',
  catalogSize: catalog.length,
  fuzzyTop: fuzzy[0]?.workId || null,
  secondTempleFacetCount: filtered.length,
  compareWorks: compared.map(item => item.workId),
  contextSchema: restored.schema
}, null, 2));
