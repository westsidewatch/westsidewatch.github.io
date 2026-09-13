import { projectCollection, transitionProjection, restoreProjection } from '../runtime/projection.mjs';
import { serializeContext, restoreContext } from '../runtime/relation-context.mjs';

const [overlay, initialContext] = await Promise.all([
  fetch('../relations/biblical-world.v1.json').then(r => r.json()),
  fetch('../contexts/second-temple.v1.json').then(r => r.json())
]);

const state = {
  kind: 'flow',
  context: restoreInitialContext(initialContext),
  overlay
};

const surface = document.querySelector('#surface');
const anchorOut = document.querySelector('#context-anchor');
const focusOut = document.querySelector('#context-focus');
const tokenOut = document.querySelector('#state-token');
const card = document.querySelector('#card');
const cardTitle = document.querySelector('#card-title');
const cardId = document.querySelector('#card-id');
const cardRelation = document.querySelector('#card-relation');

function restoreInitialContext(fallback) {
  const hash = new URLSearchParams(location.hash.slice(1));
  const saved = hash.get('context');
  if (!saved) return structuredClone(fallback);
  try { return restoreContext(saved); } catch { return structuredClone(fallback); }
}

function writeHash() {
  const params = new URLSearchParams();
  params.set('kind', state.kind);
  params.set('context', serializeContext(state.context));
  history.replaceState(null, '', `#${params.toString()}`);
}

function workLabel(workId) {
  return `Work ${workId.slice(-8)}`;
}

function token(item, index, spectrum = false) {
  const button = document.createElement('button');
  button.className = 'work-token';
  button.dataset.workId = item.workId;
  button.innerHTML = `<span class="token-index">${String(index + 1).padStart(2,'0')}</span><div class="token-id">${item.workId}</div><span class="token-cue">${item.relationCue.replace('concept:','')}</span>`;
  if (spectrum) {
    const angle = (Math.PI * 2 * index) / Math.max(1, currentProjection().items.length);
    const rx = innerWidth < 760 ? 150 : 290;
    const ry = innerWidth < 760 ? 180 : 230;
    button.style.setProperty('--x', `${Math.cos(angle) * rx}px`);
    button.style.setProperty('--y', `${Math.sin(angle) * ry}px`);
  }
  button.addEventListener('click', () => openCard(item));
  return button;
}

function currentProjection() {
  return projectCollection({ overlay: state.overlay, context: state.context, kind: state.kind });
}

function setKind(kind) {
  const transition = transitionProjection({
    overlay: state.overlay,
    context: state.context,
    from: state.kind,
    to: kind
  });
  state.kind = kind;
  state.context = transition.to.context;
  render();
}

function openCard(item) {
  const transition = transitionProjection({
    overlay: state.overlay,
    context: state.context,
    from: state.kind,
    to: 'card',
    workId: item.workId
  });
  state.context = transition.to.context;
  cardTitle.textContent = workLabel(item.workId);
  cardId.textContent = item.workId;
  cardRelation.textContent = `Relation cue · ${item.relationCue.replace('concept:','')}`;
  card.hidden = false;
  renderContextOnly();
}

function closeCard() {
  card.hidden = true;
  state.context = { ...state.context, focusedWork: null };
  renderContextOnly();
}

function expandFocusedToSpectrum() {
  if (!state.context.focusedWork) return;
  state.kind = 'spectrum';
  card.hidden = true;
  render();
}

function renderContextOnly() {
  anchorOut.textContent = `Anchor · ${(state.context.anchors || []).join(', ')}`;
  focusOut.textContent = state.context.focusedWork ? `Focus · ${state.context.focusedWork}` : 'Focus · none';
  tokenOut.textContent = serializeContext(state.context);
  writeHash();
}

function render() {
  const projection = currentProjection();
  surface.className = `surface surface-${state.kind}`;
  surface.dataset.kind = state.kind;
  surface.replaceChildren();

  projection.items.forEach((item, index) => surface.append(token(item, index, state.kind === 'spectrum')));

  document.querySelectorAll('[data-kind]').forEach(button => {
    if (button.matches('button')) button.setAttribute('aria-pressed', String(button.dataset.kind === state.kind));
  });

  renderContextOnly();
}

document.querySelectorAll('.projection-nav button').forEach(button => {
  button.addEventListener('click', () => setKind(button.dataset.kind));
});
document.querySelector('#card-close').addEventListener('click', closeCard);
document.querySelector('#card-spectrum').addEventListener('click', expandFocusedToSpectrum);

window.addEventListener('popstate', () => {
  const params = new URLSearchParams(location.hash.slice(1));
  const serialized = params.get('context');
  const kind = params.get('kind');
  if (!serialized || !['flow','shelf','spectrum'].includes(kind)) return;
  const restored = restoreProjection({ overlay: state.overlay, serializedContext: serialized, kind });
  state.context = restored.context;
  state.kind = kind;
  render();
});

const hashKind = new URLSearchParams(location.hash.slice(1)).get('kind');
if (['flow','shelf','spectrum'].includes(hashKind)) state.kind = hashKind;
render();
