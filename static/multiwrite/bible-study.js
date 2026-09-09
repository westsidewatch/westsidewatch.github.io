const params = new URLSearchParams(location.search);
const bookId = params.get('id') || 'kingdom-language';
const DB_NAME = 'multiwrite-v1';
const DB_VERSION = 3;
const STORE = 'studyDocuments';
let controller = null;

function openDb() {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(DB_NAME, DB_VERSION);
    req.onupgradeneeded = () => {
      const db = req.result;
      if (!db.objectStoreNames.contains('books')) db.createObjectStore('books', { keyPath: 'id' });
      if (!db.objectStoreNames.contains('drafts')) db.createObjectStore('drafts', { keyPath: 'id' });
      if (!db.objectStoreNames.contains(STORE)) db.createObjectStore(STORE, { keyPath: 'id' });
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

function currentPart() {
  const active = document.querySelector('.toc-link.active');
  return Number(active?.dataset.index || 0);
}

function documentId() { return `${bookId}:${currentPart()}`; }

async function readStudyDocument() {
  const db = await openDb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE, 'readonly');
    const req = tx.objectStore(STORE).get(documentId());
    req.onsuccess = () => { const value = req.result || null; db.close(); resolve(value); };
    req.onerror = () => { db.close(); reject(req.error); };
  });
}

async function writeStudyDocument(mutator) {
  const existing = await readStudyDocument();
  const base = existing || { id: documentId(), bookId, partIndex: currentPart(), schema: 'dore.study-document.v1', kept: [], flow: [], updatedAt: null };
  const next = mutator(structuredClone(base)) || base;
  next.id = documentId();
  next.bookId = bookId;
  next.partIndex = currentPart();
  next.updatedAt = new Date().toISOString();
  const db = await openDb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE, 'readwrite');
    tx.objectStore(STORE).put(next);
    tx.oncomplete = () => { db.close(); resolve(next); };
    tx.onerror = () => { db.close(); reject(tx.error); };
  });
}

function evidenceFrom(payload) {
  return {
    result_id: payload.result_id,
    canonical_reference: payload.canonical_reference,
    source_ref: payload.source_ref,
    evidence_status: payload.evidence_status,
    result: payload.result,
    saved_at: new Date().toISOString(),
  };
}

async function handleAction(payload) {
  if (payload.action === 'present') {
    window.dispatchEvent(new CustomEvent('dore:bible-study-present', { detail: payload }));
    return;
  }
  const evidence = evidenceFrom(payload);
  await writeStudyDocument((doc) => {
    const target = payload.action === 'flow' ? doc.flow : doc.kept;
    const key = evidence.result_id || evidence.canonical_reference || evidence.source_ref;
    const exists = target.some((item) => (item.result_id || item.canonical_reference || item.source_ref) === key);
    if (!exists) target.push(evidence);
    return doc;
  });
  await renderStudyDocument();
}

async function renderStudyDocument() {
  const box = document.querySelector('#bibleStudyDocument');
  if (!box) return;
  const doc = await readStudyDocument();
  const kept = doc?.kept || [];
  const flow = doc?.flow || [];
  const refs = (items) => items.map((x) => x.canonical_reference || x.result?.title || x.result_id).filter(Boolean).join(' · ');
  box.innerHTML = `<div class="study-doc-row"><span>KEEP</span><strong>${kept.length}</strong><p>${refs(kept) || '尚未保留證據'}</p></div><div class="study-doc-row"><span>FLOW</span><strong>${flow.length}</strong><p>${refs(flow) || '尚未加入流程'}</p></div>`;
}

async function invokeFuzzySearch(query, context) {
  const capabilities = window.DoreCapabilities || window.DoreCapabilityBus || window.DoreCore;
  if (capabilities && typeof capabilities.invoke === 'function') {
    return capabilities.invoke('context.fuzzy-search', { query, context });
  }
  if (window.DoreContext && typeof window.DoreContext.fuzzySearch === 'function') {
    return window.DoreContext.fuzzySearch(query, context);
  }
  return new Promise((resolve, reject) => {
    const requestId = `bi3-${Date.now()}-${Math.random().toString(36).slice(2)}`;
    let settled = false;
    const timeout = setTimeout(() => {
      if (settled) return;
      settled = true;
      window.removeEventListener('dore:context-fuzzy-search-result', onResult);
      reject(new Error('context.fuzzy-search capability unavailable'));
    }, 1800);
    function onResult(event) {
      if (event.detail?.request_id !== requestId || settled) return;
      settled = true;
      clearTimeout(timeout);
      window.removeEventListener('dore:context-fuzzy-search-result', onResult);
      resolve(event.detail.payload || event.detail.results || []);
    }
    window.addEventListener('dore:context-fuzzy-search-result', onResult);
    window.dispatchEvent(new CustomEvent('dore:context-fuzzy-search', { detail: { request_id: requestId, capability: 'context.fuzzy-search', query, context } }));
  });
}

function setPanel(open) {
  const panel = document.querySelector('#bibleStudyPanel');
  const toggle = document.querySelector('#toggleBibleStudy');
  if (!panel || !toggle) return;
  panel.hidden = !open;
  toggle.setAttribute('aria-expanded', String(open));
  if (open) document.querySelector('#bibleStudyMount input')?.focus();
}

function mount() {
  const api = window.DoreMultiwriteBibleStudy;
  const mountPoint = document.querySelector('#bibleStudyMount');
  if (!api?.createPrepareController || !mountPoint) return;
  controller = api.createPrepareController({
    host: 'multiwrite',
    embedded: false,
    maxResults: 5,
    search: invokeFuzzySearch,
    onAction: (payload) => handleAction(payload).catch(console.error),
    onError: (error) => console.warn('[DORÉ BI-3]', error),
  });
  controller.mount(mountPoint);
  renderStudyDocument().catch(console.error);
}

document.querySelector('#toggleBibleStudy')?.addEventListener('click', () => setPanel(document.querySelector('#bibleStudyPanel')?.hidden));
document.querySelector('#closeBibleStudy')?.addEventListener('click', () => setPanel(false));
document.querySelector('#toc')?.addEventListener('click', () => setTimeout(() => renderStudyDocument().catch(console.error), 0));
mount();