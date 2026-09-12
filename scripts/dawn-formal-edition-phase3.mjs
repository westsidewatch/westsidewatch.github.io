import fs from 'node:fs';
import path from 'node:path';
import { projectCollection, transitionProjection, restoreProjection } from '../static/dawn-library/formal-edition/runtime/projection.mjs';

const root = process.cwd();
const read = p => JSON.parse(fs.readFileSync(path.join(root, p), 'utf8'));
const overlay = read('static/dawn-library/formal-edition/relations/biblical-world.v1.json');
const context = read('static/dawn-library/formal-edition/contexts/second-temple.v1.json');
const fixture = read('static/dawn-library/formal-edition/fixtures/biblical-vertical-slice.v1.json');

function assert(ok, message) {
  if (!ok) throw new Error(message);
}

const fixtureIds = new Set(fixture.workIds);
const flow = projectCollection({ overlay, context, kind: 'flow' });
assert(flow.items.length >= 3, 'FLOW must contain real related Works');
assert(flow.items.every(item => fixtureIds.has(item.workId)), 'FLOW leaked non-fixture identity');

const shelfStep = transitionProjection({ overlay, context: flow.context, from: 'flow', to: 'shelf' });
const shelf = shelfStep.to;
assert(shelf.kind === 'shelf' && shelf.motion === 'settle', 'FLOW → SHELF projection/motion failed');
assert(new Set(shelf.items.map(x => x.workId)).size === shelf.items.length, 'SHELF duplicated Work identity');
assert([...flow.items.map(x => x.workId)].sort().join('|') === shelf.items.map(x => x.workId).join('|'), 'SHELF changed the Work set');

const chosen = shelf.items[0].workId;
const cardStep = transitionProjection({ overlay, context: shelf.context, from: 'shelf', to: 'card', workId: chosen });
const card = cardStep.to;
assert(card.kind === 'card' && card.motion === 'focus', 'SHELF → CARD projection/motion failed');
assert(card.context.focusedWork === chosen, 'CARD lost focusedWork');
assert(card.items.length === 1 && card.items[0].workId === chosen, 'CARD changed canonical Work identity');

const spectrum = projectCollection({ overlay, context: card.context, kind: 'spectrum' });
assert(spectrum.kind === 'spectrum' && spectrum.motion === 'expand', 'CARD → SPECTRUM projection/motion failed');
assert(spectrum.context.focusedWork === chosen, 'SPECTRUM lost focusedWork');
assert(spectrum.items.some(item => item.workId === chosen), 'SPECTRUM lost focused canonical Work');

const restoredSpectrum = restoreProjection({ overlay, serializedContext: cardStep.serializedContext, kind: 'spectrum' });
assert(restoredSpectrum.context.focusedWork === chosen, 'serialized Context lost focusedWork');
assert(JSON.stringify(restoredSpectrum.context.anchors) === JSON.stringify(context.anchors), 'serialized Context lost anchors');

const returnStep = transitionProjection({ overlay, context: restoredSpectrum.context, from: 'spectrum', to: 'shelf' });
assert(returnStep.to.context.focusedWork === null, 'return to SHELF must clear focus');
assert(JSON.stringify(returnStep.to.context.anchors) === JSON.stringify(context.anchors), 'return to SHELF lost context anchors');
assert(returnStep.to.items.some(item => item.workId === chosen), 'return to SHELF lost previously focused Work');

for (const kind of ['flow','shelf','card','spectrum']) {
  const projection = kind === 'card'
    ? projectCollection({ overlay, context: card.context, kind })
    : projectCollection({ overlay, context, kind });
  assert(projection.schema === 'dawn.projection.v1', `${kind} has wrong projection schema`);
  assert(projection.items.every(item => item.workId.startsWith('dawn:')), `${kind} contains non-canonical Work identity`);
}

console.log(JSON.stringify({
  phase: 3,
  status: 'PASS',
  anchor: context.anchors[0],
  workCount: flow.items.length,
  focusedWork: chosen,
  route: ['FLOW','SHELF','CARD','SPECTRUM','SHELF'],
  identityStable: true,
  contextRoundTrip: true,
  motions: ['flow','settle','focus','expand']
}, null, 2));
