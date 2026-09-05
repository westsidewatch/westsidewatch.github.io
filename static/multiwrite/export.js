import { buildExportBackup, mergeExportSections, safeFilename } from './export-core.mjs';

const DB_NAME = 'multiwrite-v1';
const DB_VERSION = 2;
const DRAFT_STORE = 'drafts';
const params = new URLSearchParams(location.search);
const bookId = params.get('id') || 'kingdom-language';

function openDb() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(DB_NAME, DB_VERSION);
    request.onupgradeneeded = () => {
      const db = request.result;
      if (!db.objectStoreNames.contains('books')) db.createObjectStore('books', { keyPath: 'id' });
      if (!db.objectStoreNames.contains(DRAFT_STORE)) db.createObjectStore(DRAFT_STORE, { keyPath: 'id' });
    };
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}

function draftId(index) {
  return `${bookId}:${index}`;
}

async function getDraft(index) {
  const db = await openDb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(DRAFT_STORE, 'readonly');
    const req = tx.objectStore(DRAFT_STORE).get(draftId(index));
    req.onsuccess = () => { const value = req.result || null; db.close(); resolve(value); };
    req.onerror = () => { db.close(); reject(req.error); };
  });
}

async function putDraft(index, text) {
  const db = await openDb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(DRAFT_STORE, 'readwrite');
    tx.objectStore(DRAFT_STORE).put({ id: draftId(index), bookId, index, text, updatedAt: new Date().toISOString() });
    tx.oncomplete = () => { db.close(); resolve(); };
    tx.onerror = () => { db.close(); reject(tx.error); };
  });
}

async function fetchText(path) {
  const response = await fetch(path, { cache: 'no-store' });
  if (!response.ok) throw new Error(`無法載入 ${path}`);
  return response.text();
}

async function fetchOriginal(item) {
  const base = `./books/${bookId}/`;
  if (item.file) return fetchText(base + item.file);
  if (Array.isArray(item.files)) {
    const parts = await Promise.all(item.files.map((file) => fetchText(base + file)));
    return parts.join('\n\n');
  }
  return '';
}

async function persistOpenEditor() {
  const editor = document.querySelector('#chapterEditor');
  const active = document.querySelector('.toc-link.active');
  if (!editor || !active) return;
  const index = Number(active.dataset.index);
  if (!Number.isInteger(index)) return;
  await putDraft(index, editor.value);
}

async function collectBook() {
  const manifestResponse = await fetch(`./books/${bookId}/manifest.json`, { cache: 'no-store' });
  if (!manifestResponse.ok) throw new Error('找不到這本書。');
  const book = await manifestResponse.json();

  const sections = await Promise.all(book.structure.map(async (item, index) => {
    const draft = await getDraft(index);
    const text = draft?.text ?? await fetchOriginal(item);
    return {
      index,
      role: item.role,
      title: item.title || '',
      draft: Boolean(draft),
      text,
    };
  }));

  return { book, sections };
}

function downloadFile(filename, content, type) {
  const blob = new Blob([content], { type });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement('a');
  anchor.href = url;
  anchor.download = filename;
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

function injectControls() {
  if (document.querySelector('#exportBook')) return;
  const actions = document.querySelector('.book-actions');
  if (!actions) return;

  const wrap = document.createElement('div');
  wrap.className = 'export-controls';
  wrap.innerHTML = `
    <select id="exportFormat" class="export-select" aria-label="導出格式">
      <option value="md">Markdown</option>
      <option value="txt">TXT</option>
      <option value="json">JSON 備份</option>
    </select>
    <button id="exportBook" class="book-action" type="button">導出</button>`;
  actions.before(wrap);

  document.querySelector('#exportBook').addEventListener('click', exportBook);
}

async function exportBook() {
  const button = document.querySelector('#exportBook');
  const format = document.querySelector('#exportFormat')?.value || 'md';
  const saveState = document.querySelector('#saveState');
  if (!button) return;

  const originalLabel = button.textContent;
  button.disabled = true;
  button.textContent = '導出中…';

  try {
    await persistOpenEditor();
    const { book, sections } = await collectBook();
    const baseName = safeFilename(book.title || bookId);

    if (format === 'json') {
      const payload = buildExportBackup(book, sections);
      downloadFile(`${baseName}.multiwrite.json`, JSON.stringify(payload, null, 2), 'application/json;charset=utf-8');
    } else {
      const body = mergeExportSections(sections);
      const ext = format === 'txt' ? 'txt' : 'md';
      const type = format === 'txt' ? 'text/plain;charset=utf-8' : 'text/markdown;charset=utf-8';
      downloadFile(`${baseName}.${ext}`, body, type);
    }

    if (saveState) saveState.textContent = '已導出整本書';
  } catch (error) {
    if (saveState) saveState.textContent = `導出失敗：${error.message}`;
  } finally {
    button.disabled = false;
    button.textContent = originalLabel;
  }
}

injectControls();
