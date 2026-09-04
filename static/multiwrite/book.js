const $ = (sel) => document.querySelector(sel);
const params = new URLSearchParams(location.search);
const bookId = params.get('id') || 'kingdom-language';

let currentBook = null;
let currentItem = null;
let currentIndex = -1;
let currentOriginalText = '';
let editing = false;

const DB_NAME = 'multiwrite-v1';
const DB_VERSION = 2;
const DRAFT_STORE = 'drafts';

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

function draftId(index = currentIndex) {
  return `${bookId}:${index}`;
}

async function getDraft(index) {
  const db = await openDb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(DRAFT_STORE, 'readonly');
    const req = tx.objectStore(DRAFT_STORE).get(draftId(index));
    req.onsuccess = () => resolve(req.result || null);
    req.onerror = () => reject(req.error);
  });
}

async function putDraft(index, text) {
  const db = await openDb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(DRAFT_STORE, 'readwrite');
    tx.objectStore(DRAFT_STORE).put({
      id: draftId(index),
      bookId,
      index,
      text,
      updatedAt: new Date().toISOString()
    });
    tx.oncomplete = resolve;
    tx.onerror = () => reject(tx.error);
  });
}

function escapeHtml(value = '') {
  return String(value).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' }[c]));
}

function renderMarkdownish(text = '') {
  const lines = String(text).replace(/\r\n?/g, '\n').split('\n');
  const out = [];
  let para = [];
  const flushPara = () => {
    if (!para.length) return;
    out.push(`<p>${escapeHtml(para.join(' ').trim())}</p>`);
    para = [];
  };
  for (const raw of lines) {
    const line = raw.trimEnd();
    const h = line.match(/^(#{1,4})\s+(.+)$/);
    if (h) {
      flushPara();
      out.push(`<h${Math.min(h[1].length + 1, 5)}>${escapeHtml(h[2])}</h${Math.min(h[1].length + 1, 5)}>`);
      continue;
    }
    if (!line.trim()) {
      flushPara();
      continue;
    }
    para.push(line.trim());
  }
  flushPara();
  return out.join('\n');
}

async function fetchText(path) {
  const res = await fetch(path);
  if (!res.ok) throw new Error(`無法載入 ${path}`);
  return res.text();
}

function setSaveState(text) {
  $('#saveState').textContent = text;
}

function renderReader(text, draft = false) {
  const reader = $('#readerContent');
  reader.innerHTML = `
    <div class="reader-role">${escapeHtml(currentItem.role === 'appendix' ? 'APPENDIX' : currentItem.role === 'front_matter' ? 'FRONT MATTER' : 'CHAPTER')}</div>
    <h2>${escapeHtml(currentItem.title || '')}</h2>
    <div class="draft-badge" ${draft ? '' : 'hidden'}>工作版本</div>
    <div class="reader-body">${renderMarkdownish(text)}</div>`;
}

function renderEditor(text) {
  const reader = $('#readerContent');
  reader.innerHTML = `
    <div class="reader-role">${escapeHtml(currentItem.role === 'appendix' ? 'APPENDIX' : currentItem.role === 'front_matter' ? 'FRONT MATTER' : 'CHAPTER')}</div>
    <h2>${escapeHtml(currentItem.title || '')}</h2>
    <p class="edit-note">你正在編輯工作版本。原始匯入稿不會被覆蓋。</p>
    <textarea id="chapterEditor" class="chapter-editor" spellcheck="true" aria-label="章節內容">${escapeHtml(text)}</textarea>`;
  $('#chapterEditor').focus();
}

async function loadPart(item, index) {
  currentItem = item;
  currentIndex = index;
  editing = false;
  $('#toggleEdit').textContent = '編輯';
  $('#saveDraft').hidden = true;
  document.querySelectorAll('.toc-link').forEach((el) => el.classList.toggle('active', Number(el.dataset.index) === index));
  $('#readerContent').innerHTML = '<p class="reader-loading">正在載入…</p>';
  try {
    const base = `./books/${bookId}/`;
    let text = '';
    if (item.file) {
      text = await fetchText(base + item.file);
    } else if (Array.isArray(item.files)) {
      const parts = await Promise.all(item.files.map((file) => fetchText(base + file)));
      text = parts.join('\n\n');
    }
    currentOriginalText = text;
    const draft = await getDraft(index);
    renderReader(draft?.text ?? text, Boolean(draft));
    setSaveState(draft ? '工作版本已儲存' : '原稿唯讀');
    $('#readerContent').scrollIntoView({ block: 'start' });
  } catch (error) {
    $('#readerContent').innerHTML = `<p class="reader-error">${escapeHtml(error.message)}</p>`;
  }
}

async function toggleEdit() {
  if (!currentItem) return;
  if (!editing) {
    const draft = await getDraft(currentIndex);
    renderEditor(draft?.text ?? currentOriginalText);
    editing = true;
    $('#toggleEdit').textContent = '取消';
    $('#saveDraft').hidden = false;
    setSaveState('編輯中');
  } else {
    const draft = await getDraft(currentIndex);
    renderReader(draft?.text ?? currentOriginalText, Boolean(draft));
    editing = false;
    $('#toggleEdit').textContent = '編輯';
    $('#saveDraft').hidden = true;
    setSaveState(draft ? '工作版本已儲存' : '原稿唯讀');
  }
}

async function saveDraft() {
  const editor = $('#chapterEditor');
  if (!editor) return;
  setSaveState('儲存中…');
  await putDraft(currentIndex, editor.value);
  renderReader(editor.value, true);
  editing = false;
  $('#toggleEdit').textContent = '編輯';
  $('#saveDraft').hidden = true;
  setSaveState('已儲存');
}

async function init() {
  try {
    const manifestRes = await fetch(`./books/${bookId}/manifest.json`);
    if (!manifestRes.ok) throw new Error('找不到這本書。');
    currentBook = await manifestRes.json();
    document.title = `${currentBook.title} · 多寫`;
    $('#bookTitle').textContent = currentBook.title;
    $('#bookSubtitle').textContent = currentBook.subtitle || '';

    const toc = $('#toc');
    toc.innerHTML = currentBook.structure.map((item, index) => `
      <button class="toc-link toc-${escapeHtml(item.role)}" data-index="${index}" type="button">
        <span class="toc-num">${String(index + 1).padStart(2, '0')}</span>
        <span>${escapeHtml(item.title || (item.role === 'front_matter' ? '前置內容' : '未命名'))}</span>
      </button>`).join('');
    toc.addEventListener('click', (event) => {
      const button = event.target.closest('.toc-link');
      if (!button) return;
      loadPart(currentBook.structure[Number(button.dataset.index)], Number(button.dataset.index));
    });

    $('#toggleEdit').addEventListener('click', toggleEdit);
    $('#saveDraft').addEventListener('click', saveDraft);

    const firstChapter = Math.max(0, currentBook.structure.findIndex((item) => item.role === 'chapter'));
    loadPart(currentBook.structure[firstChapter], firstChapter);
  } catch (error) {
    $('#readerContent').innerHTML = `<p class="reader-error">${escapeHtml(error.message)}</p>`;
  }
}

init();
