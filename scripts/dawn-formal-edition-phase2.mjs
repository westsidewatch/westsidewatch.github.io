import fs from 'node:fs';
import path from 'node:path';
import { relatedWorkIds, focusContext, clearFocus, serializeContext, restoreContext } from '../static/dawn-library/formal-edition/runtime/relation-context.mjs';

const root = process.cwd();
const read = p => JSON.parse(fs.readFileSync(path.join(root, p), 'utf8'));
const fixture = read('static/dawn-library/formal-edition/fixtures/biblical-vertical-slice.v1.json');
const overlay = read('static/dawn-library/formal-edition/relations/biblical-world.v1.json');
const contexts = [
  read('static/dawn-library/formal-edition/contexts/second-temple.v1.json'),
  read('static/dawn-library/formal-edition/contexts/early-church.v1.json')
];
const fixtureIds = new Set(fixture.workIds);
const allowedSources = new Set(['authoritative', 'semantic', 'editorial']);

function assert(ok, message) {
  if (!ok) throw new Error(message);
}

assert(overlay.schema === 'dawn.relation-overlay.v1', 'wrong relation schema');
assert(overlay.edges.length > 0, 'empty relation overlay');
for (const edge of overlay.edges) {
  assert(fixtureIds.has(edge.from), `relation from non-fixture work: ${edge.from}`);
  assert(edge.to.startsWith('concept:'), `relation target must be concept:*: ${edge.to}`);
  assert(allowedSources.has(edge.source), `invalid relation source: ${edge.source}`);
  assert(typeof edge.provenance === 'string' && edge.provenance.length > 0, 'missing provenance');
  assert(edge.confidence >= 0 && edge.confidence <= 1, 'confidence outside 0..1');
}

for (const context of contexts) {
  assert(context.schema === 'dawn.collection-context.v1', 'wrong context schema');
  const items = relatedWorkIds(overlay, context);
  assert(items.length >= 2, `context too weak: ${context.anchors.join(',')}`);
  assert(items.every(x => fixtureIds.has(x.workId)), 'context leaked non-fixture identity');
  const focused = focusContext(context, items[0].workId);
  assert(focused.focusedWork === items[0].workId, 'focus failed');
  const restored = restoreContext(serializeContext(focused));
  assert(restored.focusedWork === focused.focusedWork, 'round-trip lost focus');
  assert(JSON.stringify(restored.anchors) === JSON.stringify(focused.anchors), 'round-trip lost anchors');
  assert(clearFocus(restored).focusedWork === null, 'clear focus failed');
}

const fabricatedJob = overlay.edges.some(edge => /job/i.test(`${edge.from} ${edge.to}`) || /約伯/.test(`${edge.from} ${edge.to}`));
assert(!fabricatedJob, 'Job relation must not be fabricated before canonical evidence exists');

console.log(JSON.stringify({
  phase: 2,
  status: 'PASS',
  fixtureWorks: fixture.workIds.length,
  relationEdges: overlay.edges.length,
  contexts: contexts.map(context => ({
    anchor: context.anchors[0],
    works: relatedWorkIds(overlay, context).map(x => x.workId)
  })),
  jobAnchor: 'UNRESOLVED_NOT_FABRICATED'
}, null, 2));
