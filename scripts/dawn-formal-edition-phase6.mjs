import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import { serializeContext, restoreContext, focusContext } from '../static/dawn-library/formal-edition/runtime/relation-context.mjs';
import { createPersonalState, validatePersonalState, saveBookmark, removeBookmark, saveView, saveTrail, exportPersonalState, importPersonalState, createLocalPersonalStore } from '../static/dawn-library/formal-edition/runtime/personal-state.mjs';

const read = async path => JSON.parse(await fs.readFile(new URL(path, import.meta.url), 'utf8'));
const [canonical, surface, contextSeed] = await Promise.all([
  read('../static/dawn-library/canonical-index.json'),
  read('../static/dawn-library/surfaces/multiwrite-biblical-world.json'),
  read('../static/dawn-library/formal-edition/contexts/second-temple.v1.json')
]);

assert.equal(canonical.schema, 'dawn.library.canonical-index.v1');
assert.ok(canonical.workCount >= 10000);
const canonicalIds = new Set(Object.keys(canonical.works || {}));
assert.equal(canonicalIds.size, canonical.workCount);

const fallbackId = (surface.items || []).map(item => item.workId).find(id => id?.startsWith('dawn:'));
const authorityId = [...canonicalIds].find(id => !id.startsWith('dawn:'));
assert.ok(fallbackId && canonicalIds.has(fallbackId), 'Need a real Dawn fallback Work ID');
assert.ok(authorityId && canonicalIds.has(authorityId), 'Need a real authority-backed canonical Work ID');

const fixedNow = '2026-09-12T22:50:00.000Z';
let state = createPersonalState();
assert.equal(state.owner.scope, 'user');
assert.equal(state.owner.persistence, 'local');

const focused = focusContext(structuredClone(contextSeed), fallbackId);
state = saveBookmark(state, { workId: fallbackId, context: focused, projection: 'card', label: 'Second Temple focus', now: fixedNow });
state = saveBookmark(state, { workId: authorityId, context: contextSeed, projection: 'shelf', now: fixedNow });
assert.equal(state.bookmarks.length, 2);
assert.deepEqual(state.bookmarks.map(row => row.workId), [fallbackId, authorityId]);
assert.equal(restoreContext(state.bookmarks[0].context).focusedWork, fallbackId);

state = saveView(state, { id: 'view:second-temple-spectrum', context: contextSeed, projection: 'spectrum', label: 'Second Temple spectrum', now: fixedNow });
assert.equal(state.views.length, 1);
assert.equal(restoreContext(state.views[0].context).schema, contextSeed.schema);

state = saveTrail(state, {
  id: 'trail:second-temple-reading',
  label: 'Second Temple reading',
  now: fixedNow,
  steps: [
    { workId: fallbackId, context: focused, projection: 'card', visitedAt: fixedNow },
    { workId: authorityId, context: contextSeed, projection: 'spectrum', visitedAt: fixedNow }
  ]
});
assert.equal(state.trails.length, 1);
assert.deepEqual(state.trails[0].steps.map(step => step.workId), [fallbackId, authorityId]);
assert.equal(restoreContext(state.trails[0].steps[0].context).focusedWork, fallbackId);
assert.equal(validatePersonalState(state, canonicalIds), true);

const forbiddenCopiedIdentity = ['title','author','authors','creator','cover','edition','editions','authorityIds','readingPointer','metadata'];
const serializedState = JSON.stringify(state);
for (const field of forbiddenCopiedIdentity) assert.ok(!serializedState.includes(`\"${field}\"`), `Personal state copied canonical identity field: ${field}`);

const memory = new Map();
const storage = {
  getItem: key => memory.has(key) ? memory.get(key) : null,
  setItem: (key, value) => memory.set(key, value),
  removeItem: key => memory.delete(key)
};
const store = createLocalPersonalStore(storage);
store.save(state);
const reloaded = store.load();
assert.deepEqual(reloaded, state, 'Local personal persistence must round-trip exactly');

const exported = exportPersonalState(state);
assert.equal(JSON.parse(exported).owner.persistence, 'exported');
const imported = importPersonalState(exported, canonicalIds);
assert.equal(imported.owner.persistence, 'local');
assert.deepEqual(imported.bookmarks.map(row => row.workId), state.bookmarks.map(row => row.workId));
assert.deepEqual(imported.views, state.views);
assert.deepEqual(imported.trails, state.trails);

state = removeBookmark(state, fallbackId);
assert.deepEqual(state.bookmarks.map(row => row.workId), [authorityId]);
assert.equal(validatePersonalState(state, canonicalIds), true);

assert.throws(() => validatePersonalState({ ...state, bookmarks: [{ id: 'bad', workId: 'missing:work', savedAt: fixedNow }] }, canonicalIds), /Unknown canonical Work/);

console.log(JSON.stringify({
  phase: 6,
  status: 'PASS',
  canonicalWorks: canonical.workCount,
  fallbackWorkId: fallbackId,
  authorityWorkId: authorityId,
  bookmarkRoundTrip: true,
  savedViewRoundTrip: true,
  trailRoundTrip: true,
  localPersistence: true,
  exportImport: true,
  copiedCanonicalIdentity: false,
  ownerScope: 'user'
}, null, 2));
