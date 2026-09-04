import { ROLE_OPTIONS, buildBook, mergeImports, validateBook } from './import-core.mjs';

const $ = (sel, root = document) => root.querySelector(sel);
const state = { nodes: [], sources: [], files: [] };

const DB_NAME = 'multiwrite-v1';
const STORE = 'books';

function openDb() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(DB_NAME, 1);
    request.onupgradeneeded = () => {
      const db = request.result;
      if (!db.objectStoreNames.contains(STORE)) db.createObjectStore(STORE, { keyPath: 'id' });
    };
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}

async function saveBook(book) {
  const db = await openDb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE, 'readwrite');
    tx.objectStore(STORE).put(book);
    tx.oncomplete = () => resolve(book);
    tx.onerror = () => reject(tx.error);
  });
}

async function listBooks() {
  const db = await openDb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE, 'readonly');
    const request = tx.objectStore(STORE).getAll();
    request.onsuccess = () => resolve(request.result || []);
    request.onerror = () => reject(request.error);
  });
}

async function loadScript(src) {
  if ([...document.scripts].some((s) => s.src === src)) return;
  await new Promise((resolve, reject) => {
    const s = document.createElement('script');
    s.src = src;
    s.onload = resolve;
    s.onerror = reject;
    document.head.appendChild(s);
  });
}

async function extractDocx(file) {
  await loadScript('https://cdn.jsdelivr.net/npm/mammoth@1.8.0/mammoth.browser.min.js');
  if (!window.mammoth) throw new Error('DOCX 解析器載入失敗');
  const arrayBuffer = await file.arrayBuffer();
  const result = await window.mammoth.extractRawText({ arrayBuffer });
  return result.value;
}

async function extractPdf(file) {
  const pdfjs = await import('https://cdnjs.cloudflare.com/ajax/libs/pdf.js/4.10.38/pdf.min.mjs');
  pdfjs.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/4.10.38/pdf.worker.min.mjs';
  const data = new Uint8Array(await file.arrayBuffer());
  const pdf = await pdfjs.getDocument({ data }).promise;
  const pages = [];
  for (let pageNo = 1; pageNo <= pdf.numPages; pageNo += 1) {
    const page = await pdf.getPage(pageNo);
    const text = await page.getTextContent();
    const pageText = text.items
      .map((item) => `${item.str}${item.hasEOL ? '\n' : ' '}`)
      .join('')
      .replace(/[ \t]+\n/g, '\n')
      .replace(/[ \t]{2,}/g, ' ')
      .trim();
    pages.push(pageText);
  }
  return pages.join('\n\n');
}

async function extractFile(file) {
  const ext = file.name.split('.').pop()?.toLowerCase();
  if (['txt', 'md', 'markdown'].includes(ext)) return file.text();
  if (ext === 'docx') return extractDocx(file);
  if (ext === 'pdf') return extractPdf(file);
  throw new Error(`暫不支援 .${ext || '未知'} 檔案`);
}

function escapeHtml(value = '') {
  return String(value).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' }[c]));
}

function roleOptions(selected) {
  return ROLE_OPTIONS.map(([value, label]) => `<option value="${value}" ${value === selected ? 'selected' : ''}>${label}</option>`).join('');
}

function renderPreview() {
  const preview = $('#preview');
  $('#previewCount').textContent = `${state.nodes.length} 個區塊`;
  preview.innerHTML = state.nodes.map((node, index) => `
    <article class="preview-item" data-index="${index}">
      <div class="preview-index">${String(index + 1).padStart(2, '0')}</div>
      <div class="preview-main">
        <div class="preview-controls">
          <select data-field="role" aria-label="內容類型">${roleOptions(node.role)}</select>
          <input data-field="title" value="${escapeHtml(node.title)}" aria-label="標題">
          <button type="button" data-move="up" aria-label="上移">↑</button>
          <button type="button" data-move="down" aria-label="下移">↓</button>
        </div>
        <div class="source-label">${escapeHtml(node.sourceFile)}</div>
        <pre>${escapeHtml(node.content.slice(0, 900))}${node.content.length > 900 ? '\n…' : ''}</pre>
      </div>
    </article>`).join('');
  $('#importAction').disabled = !state.nodes.length;
}

function swapNodes(a, b) {
  if (b < 0 || b >= state.nodes.length) return;
  [state.nodes[a], state.nodes[b]] = [state.nodes[b], state.nodes[a]];
  state.nodes.forEach((node, index) => { node.order = index; });
  renderPreview();
}

function bindPreview() {
  $('#preview').addEventListener('input', (event) => {
    const item = event.target.closest('.preview-item');
    if (!item) return;
    const node = state.nodes[Number(item.dataset.index)];
    const field = event.target.dataset.field;
    if (field) node[field] = event.target.value;
  });
  $('#preview').addEventListener('click', (event) => {
    const button = event.target.closest('[data-move]');
    if (!button) return;
    const item = button.closest('.preview-item');
    const index = Number(item.dataset.index);
    swapNodes(index, button.dataset.move === 'up' ? index - 1 : index + 1);
  });
}

async function consumeFiles(files) {
  const accepted = [];
  const failures = [];
  for (const file of files) {
    try {
      const text = await extractFile(file);
      accepted.push({ sourceFile: file.name, text });
      state.sources.push({ name: file.name, type: file.type || 'unknown', size: file.size });
    } catch (error) {
      failures.push(`${file.name}: ${error.message}`);
    }
  }
  if (accepted.length) {
    state.nodes = mergeImports(accepted);
    renderPreview();
    $('#stepPreview').hidden = false;
    $('#stepPreview').scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
  if (failures.length) showStatus(failures.join('；'), 'error');
}

function showStatus(message, kind = 'ok') {
  const status = $('#status');
  status.textContent = message;
  status.dataset.kind = kind;
  status.hidden = false;
}

async function renderLibrary() {
  const list = $('#bookList');
  try {
    const local = await listBooks();
    const golden = await fetch('./books/kingdom-language/manifest.json').then((r) => r.ok ? r.json() : null).catch(() => null);
    const items = [...(golden ? [golden] : []), ...local];
    if (!items.length) {
      list.innerHTML = '<div class="empty">還沒有書稿。可以建立新書，或把舊稿匯入。</div>';
      return;
    }
    list.innerHTML = items.map((book) => {
      const isGolden = Boolean(book.import?.goldenCase);
      const body = `
        <div class="book-kicker">${isGolden ? 'IMPORTED · GOLDEN CASE' : 'MY BOOK'}</div>
        <h3>${escapeHtml(book.title)}</h3>
        <p>${escapeHtml(book.subtitle || '')}</p>
        <div class="book-meta">${book.nodes?.length ?? book.structure?.length ?? 0} 個內容單元</div>`;
      return isGolden
        ? `<a class="book-card book-card-link" href="./book.html?id=${encodeURIComponent(book.id)}" aria-label="打開《${escapeHtml(book.title)}》">${body}<div class="book-open">打開書稿 →</div></a>`
        : `<article class="book-card">${body}</article>`;
    }).join('');
  } catch (error) {
    list.innerHTML = `<div class="empty">書庫讀取失敗：${escapeHtml(error.message)}</div>`;
  }
}

function resetImport() {
  state.nodes = [];
  state.sources = [];
  $('#pasteInput').value = '';
  $('#fileInput').value = '';
  $('#stepPreview').hidden = true;
  $('#status').hidden = true;
  renderPreview();
}

function init() {
  const dropZone = $('#dropZone');
  const fileInput = $('#fileInput');

  $('#openImport').addEventListener('click', () => {
    $('#importPanel').hidden = false;
    $('#importPanel').scrollIntoView({ behavior: 'smooth' });
  });
  $('#cancelImport').addEventListener('click', () => {
    resetImport();
    $('#importPanel').hidden = true;
  });
  $('#chooseFiles').addEventListener('click', () => fileInput.click());
  fileInput.addEventListener('change', () => consumeFiles([...fileInput.files]));
  ['dragenter', 'dragover'].forEach((name) => dropZone.addEventListener(name, (event) => {
    event.preventDefault();
    dropZone.classList.add('dragging');
  }));
  ['dragleave', 'drop'].forEach((name) => dropZone.addEventListener(name, (event) => {
    event.preventDefault();
    dropZone.classList.remove('dragging');
  }));
  dropZone.addEventListener('drop', (event) => consumeFiles([...event.dataTransfer.files]));

  $('#parsePaste').addEventListener('click', () => {
    const text = $('#pasteInput').value;
    if (!text.trim()) return showStatus('請先貼上文字。', 'error');
    state.sources = [{ name: '貼上文字', type: 'text/plain', size: new Blob([text]).size }];
    state.nodes = mergeImports([{ sourceFile: '貼上文字', text }]);
    renderPreview();
    $('#stepPreview').hidden = false;
    $('#stepPreview').scrollIntoView({ behavior: 'smooth', block: 'start' });
  });

  $('#importAction').addEventListener('click', async () => {
    const explicitTitle = $('#bookTitle').value.trim();
    const book = buildBook({ title: explicitTitle, nodes: state.nodes, sources: state.sources });
    const validation = validateBook(book);
    if (!validation.valid) return showStatus(validation.errors.join('；'), 'error');
    await saveBook(book);
    showStatus(`《${book.title}》已加入我的書。原稿內容未經 AI 改寫。`);
    await renderLibrary();
    setTimeout(() => {
      resetImport();
      $('#importPanel').hidden = true;
      $('#library').scrollIntoView({ behavior: 'smooth' });
    }, 500);
  });

  bindPreview();
  renderPreview();
  renderLibrary();
}

init();
