const DB_NAME = 'multiwrite-v1';
const DB_VERSION = 3;
const STORE = 'studyDocuments';
const HOME_DOC_ID = 'multiwrite:home';
const BROWSER_CORPUS_URL = '/dore/browser-fuzzy-corpus.json';
let controller = null;
let noteTimer = null;
let browserCorpusPromise = null;

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
    notes: '',
    kept: [],
    flow: [],
    updatedAt: null,
  };
  if (typeof base.notes !== 'string') base.notes = '';
  const next = mutator(structuredClone(base)) || base;
  next.id = HOME_DOC_ID;
  next.host = 'multiwrite';
  next.surface = 'home';
  if (typeof next.notes !== 'string') next.notes = '';
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

function normalizeSearchText(value = '') {
  return String(value).toLowerCase().replace(/[\s\p{P}\p{S}]+/gu, '');
}

function bigrams(value) {
  const text = normalizeSearchText(value);
  if (text.length < 2) return text ? [text] : [];
  const out = [];
  for (let i = 0; i < text.length - 1; i += 1) out.push(text.slice(i, i + 2));
  return out;
}

function scoreBrowserItem(item, query) {
  const q = normalizeSearchText(query);
  if (!q) return 0;
  const fields = [item.canonical_reference, item.title, item.snippet, ...(item.aliases || [])].filter(Boolean);
  let score = 0;
  for (const field of fields) {
    const text = normalizeSearchText(field);
    if (!text) continue;
    if (text === q) score = Math.max(score, 120);
    else if (text.includes(q)) score = Math.max(score, 90 + Math.min(20, q.length));
    else if (q.includes(text) && text.length >= 3) score = Math.max(score, 72);
  }
  if (score) return score;
  const queryPairs = bigrams(q);
  if (!queryPairs.length) return 0;
  const haystack = normalizeSearchText(fields.join(' '));
  const hits = queryPairs.filter((pair) => haystack.includes(pair)).length;
  const ratio = hits / queryPairs.length;
  return ratio >= 0.45 ? Math.round(ratio * 60) : 0;
}

async function loadBrowserCorpus() {
  if (!browserCorpusPromise) {
    browserCorpusPromise = fetch(BROWSER_CORPUS_URL, { cache: 'no-store' })
      .then((res) => {
        if (!res.ok) throw new Error(`browser corpus ${res.status}`);
        return res.json();
      })
      .then((data) => Array.isArray(data) ? data : []);
  }
  return browserCorpusPromise;
}

async function browserFuzzySearch(query) {
  const corpus = await loadBrowserCorpus();
  return corpus
    .map((item) => ({ item, score: scoreBrowserItem(item, query) }))
    .filter(({ score }) => score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, 5)
    .map(({ item, score }) => ({
      ...item,
      result_id: item.id,
      evidence_status: 'browser-corpus',
      confidence: Math.min(1, score / 120),
      actions: ['keep', 'flow', 'present'],
      provenance: ['dore-browser-corpus'],
    }));
}

function companionFuzzySearch(query, context) {
  return new Promise((resolve, reject) => {
    const requestId = `home-bi3-${Date.now()}-${Math.random().toString(36).slice(2)}`;
    let settled = false;
    const timeout = setTimeout(() => {
      if (settled) return;
      settled = true;
      window.removeEventListener('dore:context-fuzzy-search-result', onResult);
      reject(new Error('context.fuzzy-search companion unavailable'));
    }, 650);
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

async function invokeFuzzySearch(query, context) {
  const capabilities = window.DoreCapabilities || window.DoreCapabilityBus || window.DoreCore;
  if (capabilities && typeof capabilities.invoke === 'function') {
    try {
      const result = await capabilities.invoke('context.fuzzy-search', { query, context });
      const rows = Array.isArray(result) ? result : result?.results;
      if (Array.isArray(rows) && rows.length) return result;
    } catch (error) {
      console.debug('[DORÉ HOME BIBLE STUDY] Core route unavailable; using browser route.', error);
    }
  }
  if (window.DoreContext && typeof window.DoreContext.fuzzySearch === 'function') {
    try {
      const result = await window.DoreContext.fuzzySearch(query, context);
      const rows = Array.isArray(result) ? result : result?.results;
      if (Array.isArray(rows) && rows.length) return result;
    } catch (error) {
      console.debug('[DORÉ HOME BIBLE STUDY] Context route unavailable; using browser route.', error);
    }
  }
  try {
    const result = await companionFuzzySearch(query, context);
    const rows = Array.isArray(result) ? result : result?.results;
    if (Array.isArray(rows) && rows.length) return result;
  } catch (error) {
    console.debug('[DORÉ HOME BIBLE STUDY] Companion route unavailable; using browser route.', error);
  }
  return browserFuzzySearch(query);
}

function setNoteStatus(message) {
  const node = document.querySelector('#homeBibleNoteStatus');
  if (node) node.textContent = message;
}

async function loadNotes() {
  const textarea = document.querySelector('#homeBibleNotes');
  if (!textarea) return;
  const doc = await readDocument();
  textarea.value = doc?.notes || '';
  setNoteStatus(doc?.updatedAt ? '已載入筆記' : '尚未開始');
}

function bindNotes() {
  const textarea = document.querySelector('#homeBibleNotes');
  if (!textarea) return;
  textarea.addEventListener('input', () => {
    setNoteStatus('未儲存');
    clearTimeout(noteTimer);
    noteTimer = setTimeout(async () => {
      try {
        const value = textarea.value;
        await writeDocument((doc) => { doc.notes = value; return doc; });
        setNoteStatus('已自動儲存');
      } catch (error) {
        setNoteStatus('儲存失敗');
        console.warn('[DORÉ HOME BIBLE STUDY] note save failed', error);
      }
    }, 600);
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
  bindNotes();
  loadNotes().catch(console.error);
  renderDocument().catch(console.error);
}

mount();
