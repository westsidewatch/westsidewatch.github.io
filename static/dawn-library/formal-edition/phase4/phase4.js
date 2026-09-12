import { serializeContext, restoreContext, focusContext, clearFocus } from '../runtime/relation-context.mjs';
import { buildCatalog, discoverCatalog, updateDiscoveryContext, facetOptions, toggleCompareWork, compareSelection } from '../runtime/discovery.mjs';

const [source, fallback, canonical] = await Promise.all([
  fetch('../../surfaces/multiwrite-biblical-world.json').then(r => r.json()),
  fetch('../contexts/second-temple.v1.json').then(r => r.json()),
  fetch('../../canonical-index.json').then(r => r.ok ? r.json() : null).catch(() => null)
]);

const catalog = buildCatalog({ surface: source, canonical });
const hash = new URLSearchParams(location.hash.slice(1));
let context = (() => { try { return hash.get('context') ? restoreContext(hash.get('context')) : structuredClone(fallback); } catch { return structuredClone(fallback); } })();
let kind = ['flow','shelf','spectrum'].includes(hash.get('kind')) ? hash.get('kind') : 'flow';
let focusedRecord = null;
const $ = s => document.querySelector(s);

function workLabel(record) { return record.title || `Work ${record.workId.slice(-8)}`; }
function currentRows() { return discoverCatalog({ catalog, context, limit: 80 }); }
function syncHash() {
  const out = new URLSearchParams();
  out.set('kind', kind);
  out.set('context', serializeContext(context));
  history.replaceState(null, '', `#${out.toString()}`);
}
function setContext(patch) { context = updateDiscoveryContext(context, patch); render(); }
function setKind(next) {
  if (!['flow','shelf','spectrum'].includes(next)) return;
  if ((next === 'flow' || next === 'shelf') && context.focusedWork) context = clearFocus(context);
  kind = next;
  $('#card').hidden = true;
  render();
}
function toggleCompare(workId, event) {
  event?.stopPropagation();
  context = toggleCompareWork(context, workId);
  render();
}
function openCard(record) {
  focusedRecord = record;
  context = focusContext(context, record.workId);
  $('#card-title').textContent = workLabel(record);
  $('#card-author').textContent = record.author || 'Dawn canonical Work';
  $('#card-id').textContent = record.workId;
  $('#card-relations').textContent = record.relations.join(' · ');
  $('#card-compare').textContent = (context.facets?.compareWorks || []).includes(record.workId) ? 'Remove from compare' : 'Add to compare';
  $('#card').hidden = false;
  renderContext();
}
function closeCard() {
  $('#card').hidden = true;
  context = clearFocus(context);
  focusedRecord = null;
  renderContext();
}
function makeToken(record, index, total) {
  const el = document.createElement('button');
  el.type = 'button';
  el.className = 'work-token';
  el.dataset.workId = record.workId;
  const num = document.createElement('span'); num.className = 'token-index'; num.textContent = String(index + 1).padStart(2,'0');
  const title = document.createElement('div'); title.className = 'token-title'; title.textContent = workLabel(record);
  const id = document.createElement('div'); id.className = 'token-id'; id.textContent = record.workId;
  const cue = document.createElement('span'); cue.className = 'token-cue'; cue.textContent = record.relations.slice(0,3).join(' · ') || 'canonical Work';
  const compare = document.createElement('button'); compare.type = 'button'; compare.className = 'token-compare'; compare.textContent = '≍'; compare.setAttribute('aria-pressed', String((context.facets?.compareWorks || []).includes(record.workId))); compare.addEventListener('click', e => toggleCompare(record.workId, e));
  el.append(num,title,id,cue,compare);
  el.addEventListener('click', () => openCard(record));
  if (kind === 'spectrum') {
    const angle = Math.PI * 2 * index / Math.max(1,total);
    const compact = innerWidth < 760;
    el.style.setProperty('--x', `${Math.cos(angle) * (compact ? 130 : 330)}px`);
    el.style.setProperty('--y', `${Math.sin(angle) * (compact ? 210 : 245)}px`);
  }
  return el;
}
function renderCompare() {
  const rows = compareSelection({ catalog, context });
  $('#compare-count').textContent = String(rows.length);
  $('#compare-open').disabled = rows.length < 2;
  const grid = $('#compare-grid'); grid.replaceChildren();
  for (const record of rows) {
    const item = document.createElement('article'); item.className = 'compare-item';
    const title = document.createElement('h3'); title.textContent = workLabel(record);
    const author = document.createElement('p'); author.textContent = record.author || '—';
    const id = document.createElement('code'); id.textContent = record.workId;
    const rel = document.createElement('p'); rel.textContent = record.relations.join(' · ');
    item.append(title,author,id,rel); grid.append(item);
  }
}
function renderContext() {
  $('#context-focus').textContent = context.focusedWork ? `Focus · ${context.focusedWork}` : 'Focus · none';
  $('#state-token').textContent = decodeURIComponent(serializeContext(context));
  $('.projection-nav').querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.kind === kind)));
  $('#query').value = context.query || '';
  $('#relation-facet').value = context.facets?.relation || '';
  $('#ordering').value = ['relevance','title','author'].includes(context.ordering) ? context.ordering : 'relevance';
  $('#distance').value = String(context.discoveryDistance ?? .35);
  renderCompare(); syncHash();
}
function render() {
  const rows = currentRows();
  const surface = $('#surface');
  surface.className = `surface surface-${kind}`;
  surface.dataset.kind = kind;
  surface.dataset.motion = kind === 'flow' ? 'flow' : kind === 'shelf' ? 'settle' : 'expand';
  surface.replaceChildren();
  if (!rows.length) { const empty = document.createElement('p'); empty.className = 'empty'; empty.textContent = '沒有符合目前 CollectionContext 的館藏。'; surface.append(empty); }
  else rows.forEach((record,index) => surface.append(makeToken(record,index,rows.length)));
  $('#result-count').textContent = `${rows.length} / ${catalog.length} canonical Works`;
  renderContext();
}

for (const option of facetOptions(catalog,'relation')) { const el = document.createElement('option'); el.value = option.value; el.textContent = `${option.value} · ${option.count}`; $('#relation-facet').append(el); }
$('#query').addEventListener('input', e => setContext({ query:e.target.value }));
$('#relation-facet').addEventListener('change', e => setContext({ facets:{ relation:e.target.value || null } }));
$('#ordering').addEventListener('change', e => setContext({ ordering:e.target.value }));
$('#distance').addEventListener('input', e => setContext({ discoveryDistance:Number(e.target.value) }));
$('.projection-nav').querySelectorAll('button').forEach(b => b.addEventListener('click', () => setKind(b.dataset.kind)));
$('#card-close').addEventListener('click', closeCard);
$('#card-spectrum').addEventListener('click', () => { if (context.focusedWork) { kind='spectrum'; $('#card').hidden=true; render(); } });
$('#card-compare').addEventListener('click', () => { if (context.focusedWork) { context=toggleCompareWork(context,context.focusedWork); if (focusedRecord) openCard(focusedRecord); render(); } });
$('#compare-open').addEventListener('click', () => { renderCompare(); $('#compare-dialog').showModal(); });
render();
