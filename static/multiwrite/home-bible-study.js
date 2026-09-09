const DB_NAME = 'multiwrite-v1';
const DB_VERSION = 3;
const STORE = 'studyDocuments';
const HOME_DOC_ID = 'multiwrite:home';
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

async function readDocument() {
  const db = await openDb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE, 'readonly');
    const req = tx.objectStore(STORE).get(HOME_DOC_ID);
    req.onsuccess = () => { const value = req.result || null; db.close(); resolve(value); };
    req.onerror = () => { db.close(); reject(req.error); };
  });
}

async function writeDocument(mutator) {
  const existing = await readDocument();
  const base = existing || {
    id: HOME_DOC_ID,
    schema: 'dore.study-document.v1',
    host: 'multiwrite',
    surface: 'home',
    kept: [],
    flow: [],
    updatedAt: null,
  };
  const next = mutator(structuredClone(base)) || base;
  next.id = HOME_DOC_ID;
  next.host = 'multiwrite';
  next.surface = 'home';
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
  await writeDocument((doc) => {
    const target = payload.action === 'flow' ? doc.flow : doc.kept;
    const key = evidence.result_id || evidence.canonical_reference || evidence.source_ref;
    if (!target.some((item) => (item.result_id || item.canonical_reference || item.source_ref) === key)) target.push(evidence);
    return doc;
  });
  await renderDocument();
}

async function renderDocument() {
  const box = document.querySelector('#homeBibleStudyDocument');
  if (!box) return;
  const doc = await readDocument();
  const kept = doc?.kept || [];
  const flow = doc?.flow || [];
  const refs = (items) => items.map((x) => x.canonical_reference || x.result?.title || x.result_id).filter(Boolean).join(' · ');
  box.innerHTML = `<div class="home-study-summary-row"><span>KEEP</span><strong>${kept.length}</strong><p>${refs(kept) || '尚未保留證據'}</p></div><div class="home-study-summary-row"><span>FLOW</span><strong>${flow.length}</strong><p>${refs(flow) || '尚未加入流程'}</p></div>`;
}

async function invokeFuzzySearch(query, context) {
  const capabilities = window.DoreCapabilities || window.DoreCapabilityBus || window.DoreCore;
  if (capabilities && typeof capabilities.invoke === 'function') return capabilities.invoke('context.fuzzy-search', { query, context });
  if (window.DoreContext && typeof window.DoreContext.fuzzySearch === 'function') return window.DoreContext.fuzzySearch(query, context);
  return new Promise((resolve, reject) => {
    const requestId = `home-bi3-${Date.now()}-${Math.random().toString(36).slice(2)}`;
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
    window.dispatchEvent(new CustomEvent('dore:context-fuzzy-search', {
      detail: {
        request_id: requestId,
        capability: 'context.fuzzy-search',
        query,
        context: { ...context, surface: 'home' },
      },
    }));
  });
}

function mount() {
  const api = window.DoreMultiwriteBibleStudy;
  const mountPoint = document.querySelector('#homeBibleStudyMount');
  if (!api?.createPrepareController || !mountPoint) return;
  controller = api.createPrepareController({
    host: 'multiwrite',
    embedded: false,
    maxResults: 5,
    search: invokeFuzzySearch,
    onAction: (payload) => handleAction(payload).catch(console.error),
    onError: (error) => console.warn('[DORÉ HOME BIBLE STUDY]', error),
  });
  controller.mount(mountPoint);
  renderDocument().catch(console.error);
}

mount();
