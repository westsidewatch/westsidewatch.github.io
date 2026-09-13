import { serializeContext, restoreContext } from './relation-context.mjs';

const PROJECTIONS = new Set(['flow','shelf','spectrum','card']);
const nowIso = now => new Date(now ?? Date.now()).toISOString();
const idPart = value => String(value || '').replace(/[^a-z0-9:_-]+/gi, '-').replace(/^-+|-+$/g, '').slice(0, 80) || 'item';

export function createPersonalState() {
  return { schema: 'dawn.personal-state.v1', owner: { scope: 'user', persistence: 'local' }, bookmarks: [], views: [], trails: [] };
}

export function validatePersonalState(state, canonicalIds = null) {
  if (!state || state.schema !== 'dawn.personal-state.v1' || state.owner?.scope !== 'user') throw new Error('Invalid Personal Dawn state');
  if (!['local','exported'].includes(state.owner?.persistence)) throw new Error('Invalid personal persistence scope');
  const assertProjection = projection => { if (!PROJECTIONS.has(projection)) throw new Error(`Invalid projection: ${projection}`); };
  const assertWork = workId => {
    if (!workId || typeof workId !== 'string') throw new Error('Personal Work reference is required');
    if (canonicalIds && !canonicalIds.has(workId)) throw new Error(`Unknown canonical Work: ${workId}`);
  };
  const assertContext = token => { if (token) restoreContext(token); };
  for (const row of state.bookmarks || []) { assertWork(row.workId); if (row.projection) assertProjection(row.projection); assertContext(row.context); }
  for (const row of state.views || []) { assertProjection(row.projection); assertContext(row.context); }
  for (const trail of state.trails || []) {
    if (!Array.isArray(trail.steps) || !trail.steps.length) throw new Error(`Trail ${trail.id || ''} has no steps`);
    for (const step of trail.steps) { assertWork(step.workId); assertProjection(step.projection); assertContext(step.context); }
  }
  return true;
}

export function saveBookmark(state, { workId, context = null, projection = 'card', label = '', now } = {}) {
  const token = context ? (typeof context === 'string' ? context : serializeContext(context)) : undefined;
  const id = `bookmark:${idPart(workId)}`;
  const row = { id, workId, ...(token ? { context: token } : {}), projection, ...(label ? { label } : {}), savedAt: nowIso(now) };
  return { ...state, bookmarks: [...(state.bookmarks || []).filter(item => item.workId !== workId), row] };
}

export function removeBookmark(state, workId) {
  return { ...state, bookmarks: (state.bookmarks || []).filter(item => item.workId !== workId) };
}

export function saveView(state, { id, context, projection = 'flow', label = '', now } = {}) {
  if (!context) throw new Error('Saved View requires CollectionContext');
  const token = typeof context === 'string' ? context : serializeContext(context);
  const viewId = id || `view:${idPart(label || projection)}`;
  const row = { id: viewId, context: token, projection, ...(label ? { label } : {}), savedAt: nowIso(now) };
  return { ...state, views: [...(state.views || []).filter(item => item.id !== viewId), row] };
}

export function saveTrail(state, { id, label = '', steps = [], now } = {}) {
  if (!steps.length) throw new Error('Trail requires at least one step');
  const trailId = id || `trail:${idPart(label || 'reading')}`;
  const normalized = steps.map(step => ({
    workId: step.workId,
    context: typeof step.context === 'string' ? step.context : serializeContext(step.context),
    projection: step.projection || 'card',
    visitedAt: nowIso(step.visitedAt ?? now)
  }));
  const row = { id: trailId, label: label || 'Reading trail', steps: normalized, savedAt: nowIso(now) };
  return { ...state, trails: [...(state.trails || []).filter(item => item.id !== trailId), row] };
}

export function exportPersonalState(state) {
  validatePersonalState(state);
  return JSON.stringify({ ...state, owner: { ...state.owner, persistence: 'exported' } });
}

export function importPersonalState(serialized, canonicalIds = null) {
  const state = JSON.parse(serialized);
  validatePersonalState(state, canonicalIds);
  return { ...state, owner: { ...state.owner, scope: 'user', persistence: 'local' } };
}

export function createLocalPersonalStore(storage, key = 'dawn.personal-state.v1') {
  if (!storage?.getItem || !storage?.setItem) throw new Error('Storage adapter requires getItem/setItem');
  return {
    load() {
      const raw = storage.getItem(key);
      if (!raw) return createPersonalState();
      const state = JSON.parse(raw);
      validatePersonalState(state);
      return state;
    },
    save(state) {
      validatePersonalState(state);
      storage.setItem(key, JSON.stringify(state));
      return state;
    },
    clear() { storage.removeItem?.(key); }
  };
}
