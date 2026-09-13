import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import { buildCatalog } from '../static/dawn-library/formal-edition/runtime/discovery.mjs';
import { projectEditorialArtifact, validateEditorialArtifact } from '../static/dawn-library/formal-edition/runtime/editorial.mjs';
import { serializeContext, restoreContext } from '../static/dawn-library/formal-edition/runtime/relation-context.mjs';

const read = async path => JSON.parse(await fs.readFile(new URL(path, import.meta.url), 'utf8'));
const [canonical, surface, baseContext, morningStar, collection, spectrum] = await Promise.all([
  read('../static/dawn-library/canonical-index.json'),
  read('../static/dawn-library/surfaces/multiwrite-biblical-world.json'),
  read('../static/dawn-library/formal-edition/contexts/second-temple.v1.json'),
  read('../static/dawn-library/formal-edition/editorial/second-temple-morning-star.v1.json'),
  read('../static/dawn-library/formal-edition/editorial/second-temple-collection.v1.json'),
  read('../static/dawn-library/formal-edition/editorial/second-temple-spectrum.v1.json')
]);

assert.equal(canonical.schema, 'dawn.library.canonical-index.v1');
assert.ok(canonical.workCount >= 10000);
const canonicalIds = new Set(Object.keys(canonical.works || {}));
assert.equal(canonicalIds.size, canonical.workCount);
const catalog = buildCatalog({ canonical, surface });
assert.equal(catalog.length, canonical.workCount, 'Editorial World must project the full canonical substrate, not a surface-owned subset');

const artifacts = [morningStar, collection, spectrum];
const kinds = artifacts.map(a => a.kind);
assert.deepEqual(kinds, ['morning-star', 'curated-collection', 'spectrum-editorial']);

const forbiddenIdentityFields = new Set(['author','authors','creator','cover','edition','editions','readingPointer','authorityIds','metadata']);
function assertNoCopiedIdentity(node, path = 'artifact') {
  if (Array.isArray(node)) return node.forEach((v, i) => assertNoCopiedIdentity(v, `${path}[${i}]`));
  if (!node || typeof node !== 'object') return;
  for (const [key, value] of Object.entries(node)) {
    assert.ok(!forbiddenIdentityFields.has(key), `${path} copies canonical identity field: ${key}`);
    assertNoCopiedIdentity(value, `${path}.${key}`);
  }
}

for (const artifact of artifacts) {
  assert.equal(validateEditorialArtifact(artifact, canonicalIds), true);
  assertNoCopiedIdentity(artifact);
  const projected = projectEditorialArtifact({ artifact, catalog, context: structuredClone(baseContext) });
  assert.equal(projected.schema, 'dawn.editorial-projection.v1');
  assert.equal(projected.items.length, artifact.canonicalRefs.length, `${artifact.id} lost canonical refs during projection`);
  assert.deepEqual(projected.items.map(item => item.workId), artifact.canonicalRefs, `${artifact.id} changed editorial order`);
  for (const section of projected.sections) {
    assert.equal(section.items.length, section.canonicalRefs.length, `${artifact.id}/${section.id} has unresolved refs`);
  }
  const restored = restoreContext(serializeContext(projected.context));
  assert.equal(restored.semanticIntent, artifact.contextPatch.semanticIntent);
  assert.deepEqual(restored.anchors, artifact.contextPatch.anchors);
}

const starIds = new Set(morningStar.canonicalRefs);
assert.equal(starIds.size, 3, 'Three Morning Stars must contain exactly three distinct canonical Works');
assert.ok(morningStar.canonicalRefs.every(id => collection.canonicalRefs.includes(id)), 'Morning Stars must remain readable inside the curated world');
assert.deepEqual(spectrum.canonicalRefs, collection.canonicalRefs, 'Spectrum and curated collection must be alternate projections of the same editorial Work set');

console.log(JSON.stringify({
  phase: 5,
  status: 'PASS',
  canonicalWorks: canonical.workCount,
  authorityBackedWorks: canonical.authorityBackedWorks,
  editorialArtifacts: artifacts.map(a => ({ id: a.id, kind: a.kind, refs: a.canonicalRefs.length })),
  threeMorningStars: morningStar.canonicalRefs,
  curatedWorldRefs: collection.canonicalRefs.length,
  spectrumRefs: spectrum.canonicalRefs.length,
  identityCopied: false,
  sharedCollectionContext: true
}, null, 2));
