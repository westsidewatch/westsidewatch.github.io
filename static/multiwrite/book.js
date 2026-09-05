const $ = (sel) => document.querySelector(sel);
const params = new URLSearchParams(location.search);
const bookId = params.get('id') || 'kingdom-language';

let currentBook = null;
let currentItem = null;
let currentIndex = -1;
let currentOriginalText = '';
let editing = false;
let autosaveTimer = null;

const DB_NAME = 'multiwrite-v1';
const DB_VERSION = 2;
const DRAFT_STORE = 'drafts';
const SIZE_KEY = 'multiwrite-workspace-size-v3';

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
      const level = Math.min(h[1].length + 1, 5);
      out.push(`<h${level}>${escapeHtml(h[2])}</h${level}>`);
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
  const res = await fetch(path, { cache: 'no-store' });
  if (!res.ok) throw new Error(`無法載入 ${path}`);
  return res.text();
}

function setSaveState(text) {
  $('#saveState').textContent = text;
}

function roleLabel(item) {
  return item.role === 'appendix' ? 'APPENDIX' : item.role === 'front_matter' ? 'FRONT MATTER' : 'CHAPTER';
}

function renderReader(text, draft = false) {
  $('#readerContent').innerHTML = `
    <div class="reader-role">${roleLabel(currentItem)}</div>
    <h2>${escapeHtml(currentItem.title || '')}</h2>
    <div class="draft-badge" ${draft ? '' : 'hidden'}>工作版本</div>
    <div class="reader-body">${renderMarkdownish(text)}</div>`;
}

function bindEditorAutosave() {
  const editor = $('#chapterEditor');
  if (!editor) return;
  editor.addEventListener('input', () => {
    setSaveState('有未儲存修改');
    clearTimeout(autosaveTimer);
    autosaveTimer = setTimeout(async () => {
      try {
        await putDraft(currentIndex, editor.value);
        setSaveState('已自動儲存');
      } catch (error) {
        setSaveState('自動儲存失敗');
      }
    }, 700);
  });
}

function renderEditor(text) {
  $('#readerContent').innerHTML = `
    <div class="reader-role">${roleLabel(currentItem)}</div>
    <h2>${escapeHtml(currentItem.title || '')}</h2>
    <p class="edit-note">工作版本 · 可直接修改或在末尾續寫。原始匯入稿不會被覆蓋。</p>
    <textarea id="chapterEditor" class="chapter-editor" spellcheck="true" aria-label="章節內容">${escapeHtml(text)}</textarea>`;
  bindEditorAutosave();
  const editor = $('#chapterEditor');
  editor.focus();
  editor.setSelectionRange(editor.value.length, editor.value.length);
}

function autoWorkspaceScale() {
  const viewportWidth = Math.max(window.innerWidth || document.documentElement.clientWidth || 0, 1);
  if (viewportWidth <= 700) return 1;

  const screenWidth = Math.max(
    window.screen?.availWidth || 0,
    window.screen?.width || 0,
    viewportWidth
  );
  const referenceWidth = Math.max(viewportWidth, screenWidth);

  // Desktop writing distance: large displays should open at a readable scale
  // without requiring browser zoom. Keep medium screens conservative and let
  // very wide desktops approach the 150–180% range that is comfortable here.
  if (referenceWidth >= 2400) return 1.75;
  if (referenceWidth >= 2100) return 1.65;
  if (referenceWidth >= 1800) return 1.55;
  if (referenceWidth >= 1550) return 1.45;
  if (referenceWidth >= 1350) return 1.32;
  if (referenceWidth >= 1150) return 1.18;
  return 1;
}

function applyWorkspaceSize() {
  const manualRaw = localStorage.getItem(SIZE_KEY);
  const manual = Number(manualRaw || '1');
  const auto = autoWorkspaceScale();
  const effective = Math.min(2, Math.max(0.9, auto * manual));
  document.documentElement.style.setProperty('--workspace-zoom', String(effective));
  const label = $('#workspaceSizeLabel');
  if (label) label.textContent = manualRaw ? `${Math.round(effective * 100)}%` : `AUTO ${Math.round(effective * 100)}%`;
  document.documentElement.dataset.workspaceAuto = manualRaw ? 'manual' : 'auto';
}

function changeWorkspaceSize(delta) {
  const auto = autoWorkspaceScale();
  const currentEffective = Number(localStorage.getItem(SIZE_KEY) || '1') * auto;
  const targetEffective = Math.min(2, Math.max(0.9, Math.round((currentEffective + delta) * 20) / 20));
  const manualFactor = targetEffective / auto;
  localStorage.setItem(SIZE_KEY, String(manualFactor));
  applyWorkspaceSize();
}

async function loadPart(item, index) {
  clearTimeout(autosaveTimer);
  currentItem = item;
  currentIndex = index;
  editing = false;
  $('#toggleEdit').textContent = '編輯';
  $('#toggleEdit').disabled = true;
  $('#saveDraft').hidden = true;
  document.querySelectorAll('.toc-link').forEach((el) => el.classList.toggle('active', Number(el.dataset.index) === index));
  $('#readerContent').innerHTML = '<p class="reader-loading">正在載入…</p>';
  try {
    const base = `./books/${bookId}/`;
    let text = '';
    if (item.file) text = await fetchText(base + item.file);
    else if (Array.isArray(item.files)) {
      const parts = await Promise.all(item.files.map((file) => fetchText(base + file)));
      text = parts.join('\n\n');
    }
    currentOriginalText = text;
    const draft = await getDraft(index);
    renderReader(draft?.text ?? text, Boolean(draft));
    setSaveState(draft ? '工作版本已儲存' : '原稿唯讀');
    $('#toggleEdit').disabled = false;
    $('#readerContent').scrollIntoView({ block: 'start' });
  } catch (error) {
    $('#readerContent').innerHTML = `<p class="reader-error">${escapeHtml(error.message)}</p>`;
    setSaveState('載入失敗');
  }
}

async function toggleEdit() {
  if (!currentItem || $('#toggleEdit').disabled) return;
  try {
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
  } catch (error) {
    setSaveState(`編輯失敗：${error.message}`);
  }
}

async function saveDraft() {
  const editor = $('#chapterEditor');
  if (!editor) return;
  clearTimeout(autosaveTimer);
  try {
    setSaveState('儲存中…');
    await putDraft(currentIndex, editor.value);
    const savedText = editor.value;
    renderReader(savedText, true);
    editing = false;
    $('#toggleEdit').textContent = '編輯';
    $('#saveDraft').hidden = true;
    setSaveState('已儲存');
  } catch (error) {
    setSaveState(`儲存失敗：${error.message}`);
  }
}

async function init() {
  applyWorkspaceSize();
  window.addEventListener('resize', applyWorkspaceSize);
  $('#sizeDown')?.addEventListener('click', () => changeWorkspaceSize(-0.05));
  $('#sizeUp')?.addEventListener('click', () => changeWorkspaceSize(0.05));
  $('#sizeReset')?.addEventListener('click', () => { localStorage.removeItem(SIZE_KEY); applyWorkspaceSize(); });

  $('#homeLink').addEventListener('click', (event) => {
    event.preventDefault();
    location.assign('/multiwrite/');
  });
  $('#toggleEdit').addEventListener('click', toggleEdit);
  $('#saveDraft').addEventListener('click', saveDraft);

  try {
    const manifestRes = await fetch(`./books/${bookId}/manifest.json`, { cache: 'no-store' });
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

    const firstChapter = Math.max(0, currentBook.structure.findIndex((item) => item.role === 'chapter'));
    await loadPart(currentBook.structure[firstChapter], firstChapter);
  } catch (error) {
    $('#readerContent').innerHTML = `<p class="reader-error">${escapeHtml(error.message)}</p>`;
    setSaveState('載入失敗');
  }
}

init();
