import { buildBookIntent, buildBookModel, buildBookBuild, publicationProjection } from './book-model.mjs';
import { analyzeBookForPublication, applyMechanicalEditorialFixes } from './book-editor.mjs';

const DB_NAME = 'multiwrite-v1';
const DB_VERSION = 3;
const BOOK_STORE = 'books';
const DRAFT_STORE = 'drafts';
const params = new URLSearchParams(location.search);
const bookId = params.get('id') || 'kingdom-language';

function openDb() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(DB_NAME, DB_VERSION);
    request.onupgradeneeded = () => {
      const db = request.result;
      if (!db.objectStoreNames.contains(BOOK_STORE)) db.createObjectStore(BOOK_STORE, { keyPath: 'id' });
      if (!db.objectStoreNames.contains(DRAFT_STORE)) db.createObjectStore(DRAFT_STORE, { keyPath: 'id' });
      if (!db.objectStoreNames.contains('studyDocuments')) db.createObjectStore('studyDocuments', { keyPath: 'id' });
    };
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}

async function getStoreValue(storeName, id) {
  const db = await openDb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(storeName, 'readonly');
    const request = tx.objectStore(storeName).get(id);
    request.onsuccess = () => {
      const value = request.result || null;
      db.close();
      resolve(value);
    };
    request.onerror = () => {
      db.close();
      reject(request.error);
    };
  });
}

async function fetchText(path) {
  const response = await fetch(path, { cache: 'no-store' });
  if (!response.ok) throw new Error(`無法載入 ${path}`);
  return response.text();
}

async function sourceText(item, local) {
  if (local) return String(item?.content || '');
  const base = `./books/${bookId}/`;
  if (item?.file) return fetchText(base + item.file);
  if (Array.isArray(item?.files)) {
    return (await Promise.all(item.files.map(file => fetchText(base + file)))).join('\n\n');
  }
  return String(item?.content || '');
}

async function resolveSourceBook() {
  const local = await getStoreValue(BOOK_STORE, bookId).catch(() => null);
  if (local) {
    return {
      source: local,
      local: true,
      structure: Array.isArray(local.nodes) ? local.nodes : []
    };
  }

  const response = await fetch(`./books/${bookId}/manifest.json`, { cache: 'no-store' });
  if (!response.ok) throw new Error('找不到這本書。');
  const manifest = await response.json();
  return {
    source: manifest,
    local: false,
    structure: Array.isArray(manifest.structure) ? manifest.structure : []
  };
}

async function collectSections(structure, local) {
  return Promise.all(structure.map(async (item, index) => {
    const draft = await getStoreValue(DRAFT_STORE, `${bookId}:${index}`).catch(() => null);
    return {
      id: item.id || `section-${index + 1}`,
      index,
      role: item.role || 'chapter',
      title: item.title || '',
      draft: Boolean(draft),
      text: draft?.text ?? await sourceText(item, local)
    };
  }));
}

export async function compileCurrentBook() {
  const { source, local, structure } = await resolveSourceBook();
  if (!structure.length) throw new Error('這本書還沒有可成書的章節。');

  const sections = await collectSections(structure, local);
  const intent = buildBookIntent(source);
  let bookModel = buildBookModel({
    source: { ...source, id: source.id || bookId },
    sections,
    intent,
    internalProvenance: {
      sourceSurface: 'multiwrite',
      sourceBookId: bookId,
      sourceKind: local ? 'indexeddb' : 'static-manifest',
      compiledAt: new Date().toISOString()
    }
  });

  const editorialReport = analyzeBookForPublication(bookModel);
  const mechanical = applyMechanicalEditorialFixes(bookModel, editorialReport);
  bookModel = mechanical.bookModel;
  bookModel.validation = {
    ...bookModel.validation,
    editorial: {
      schema: editorialReport.schema,
      readiness: editorialReport.readiness,
      counts: editorialReport.counts
    }
  };

  const bookBuild = buildBookBuild({
    bookModel,
    sourceFolioId: bookId,
    sourceRevision: source.updatedAt || source.revision || ''
  });
  bookBuild.qaResult = {
    ...bookBuild.qaResult,
    editorialReadiness: editorialReport.readiness,
    editorialIssueCount: editorialReport.counts.issues,
    authorialDecisionCount: editorialReport.counts.authorialDecisions
  };

  window.__doreBookCompile = { bookModel, bookBuild, editorialReport };
  window.dispatchEvent(new CustomEvent('multiwrite:book-model-ready', {
    detail: {
      publication: publicationProjection(bookModel),
      build: bookBuild,
      editorial: editorialReport
    }
  }));

  return { bookModel, bookBuild, editorialReport };
}

function setState(message) {
  const state = document.querySelector('#saveState');
  if (state) state.textContent = message;
}

function wrapExistingExportHandlers() {
  document.querySelectorAll('[data-export]').forEach(button => {
    if (button.dataset.bookSpine === '1') return;
    const original = button.onclick;
    if (typeof original !== 'function') return;
    button.dataset.bookSpine = '1';
    button.onclick = async event => {
      try {
        setState('建立 Book Model…');
        const { editorialReport } = await compileCurrentBook();
        if (editorialReport.readiness === 'blocked') {
          setState(`成書暫停：編輯檢查有 ${editorialReport.counts.issues} 項問題`);
          return undefined;
        }
        setState(editorialReport.readiness === 'review-required'
          ? `編輯檢查完成 · ${editorialReport.counts.authorialDecisions} 項需作者決定`
          : 'Book Model 與編輯檢查已完成');
        return await original.call(button, event);
      } catch (error) {
        setState(`成書前置檢查失敗：${error.message}`);
        return undefined;
      }
    };
  });
}

wrapExistingExportHandlers();
window.addEventListener('multiwrite:book-ready', wrapExistingExportHandlers);
