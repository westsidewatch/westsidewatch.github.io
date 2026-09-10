import { ROLE_OPTIONS, buildBook, mergeImports, validateBook } from './import-core.mjs';

const $ = (sel, root = document) => root.querySelector(sel);
const state = { nodes: [], sources: [], files: [] };

const DB_NAME = 'multiwrite-v1';
const DB_VERSION = 3;
const STORE = 'books';
const DRAFT_STORE = 'drafts';
const STUDY_STORE = 'studyDocuments';

function openDb() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(DB_NAME, DB_VERSION);
    request.onupgradeneeded = () => {
      const db = request.result;
      if (!db.objectStoreNames.contains(STORE)) db.createObjectStore(STORE, { keyPath: 'id' });
      if (!db.objectStoreNames.contains(DRAFT_STORE)) db.createObjectStore(DRAFT_STORE, { keyPath: 'id' });
      if (!db.objectStoreNames.contains(STUDY_STORE)) db.createObjectStore(STUDY_STORE, { keyPath: 'id' });
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
    tx.oncomplete = () => { db.close(); resolve(book); };
    tx.onerror = () => { db.close(); reject(tx.error); };
  });
}

async function listBooks() {
  const db = await openDb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE, 'readonly');
    const request = tx.objectStore(STORE).getAll();
    request.onsuccess = () => { const result = request.result || []; db.close(); resolve(result); };
    request.onerror = () => { db.close(); reject(request.error); };
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
    const pageText = text.items.map((item) => `${item.str}${item.hasEOL ? '\n' : ' '}`).join('').replace(/[ \t]+\n/g, '\n').replace(/[ \t]{2,}/g, ' ').trim();
    pages.push(pageText);
  }
  const result = pages.join('\n\n').trim();
  if (!result) throw new Error('這份 PDF 沒有可擷取文字；目前不自動 OCR。');
  return result;
}

function htmlToText(html) {
  const doc = new DOMParser().parseFromString(html, 'text/html');
  doc.querySelectorAll('script,style,noscript,svg').forEach((node) => node.remove());
  doc.querySelectorAll('h1,h2,h3,h4,h5,h6,p,li,blockquote,br,section,article,div').forEach((node) => {
    if (node.tagName === 'BR') node.replaceWith('\n');
    else node.append('\n');
  });
  return (doc.body?.textContent || '').replace(/\u00a0/g, ' ').replace(/[ \t]+\n/g, '\n').replace(/\n{3,}/g, '\n\n').trim();
}

function xmlToText(xml) {
  const doc = new DOMParser().parseFromString(xml, 'application/xml');
  if (doc.querySelector('parsererror')) throw new Error('電子書 XML 結構無法解析');
  doc.querySelectorAll('title,p,subtitle,epigraph,text-author').forEach((node) => node.append('\n'));
  return (doc.documentElement?.textContent || '').replace(/\u00a0/g, ' ').replace(/[ \t]+\n/g, '\n').replace(/\n{3,}/g, '\n\n').trim();
}

function normalizeArchivePath(path) {
  const out = [];
  path.split('/').forEach((part) => {
    if (!part || part === '.') return;
    if (part === '..') out.pop(); else out.push(part);
  });
  return out.join('/');
}

function resolveArchivePath(baseFile, href) {
  const base = baseFile.includes('/') ? baseFile.slice(0, baseFile.lastIndexOf('/') + 1) : '';
  return normalizeArchivePath(base + href.split('#')[0]);
}

async function extractEpub(file) {
  await loadScript('https://cdn.jsdelivr.net/npm/jszip@3.10.1/dist/jszip.min.js');
  if (!window.JSZip) throw new Error('EPUB 解析器載入失敗');
  const zip = await window.JSZip.loadAsync(await file.arrayBuffer());
  const containerEntry = zip.file('META-INF/container.xml');
  if (!containerEntry) throw new Error('不是有效的 EPUB：缺少 container.xml');
  const containerXml = await containerEntry.async('string');
  const containerDoc = new DOMParser().parseFromString(containerXml, 'application/xml');
  const opfPath = containerDoc.querySelector('rootfile')?.getAttribute('full-path');
  if (!opfPath) throw new Error('EPUB 找不到 package 文件');
  const opfEntry = zip.file(opfPath);
  if (!opfEntry) throw new Error('EPUB package 文件不存在');
  const opf = new DOMParser().parseFromString(await opfEntry.async('string'), 'application/xml');
  const manifest = new Map([...opf.querySelectorAll('manifest item')].map((item) => [item.getAttribute('id'), item.getAttribute('href')]));
  const spine = [...opf.querySelectorAll('spine itemref')].map((item) => item.getAttribute('idref')).filter(Boolean);
  const chunks = [];
  for (const idref of spine) {
    const href = manifest.get(idref);
    if (!href) continue;
    const entry = zip.file(resolveArchivePath(opfPath, href));
    if (!entry) continue;
    const text = htmlToText(await entry.async('string'));
    if (text) chunks.push(text);
  }
  const result = chunks.join('\n\n').trim();
  if (!result) throw new Error('EPUB 沒有找到可讀正文');
  return result;
}

async function extractFile(file) {
  const ext = file.name.split('.').pop()?.toLowerCase();
  if (['txt', 'md', 'markdown'].includes(ext)) return file.text();
  if (['html', 'htm', 'xhtml'].includes(ext)) return htmlToText(await file.text());
  if (ext === 'fb2') return xmlToText(await file.text());
  if (ext === 'epub') return extractEpub(file);
  if (ext === 'docx') return extractDocx(file);
  if (ext === 'pdf') return extractPdf(file);
  if (['mobi', 'azw', 'azw3', 'kfx'].includes(ext)) throw new Error('Kindle/MOBI 格式尚未接入解析器；DRM 電子書也不能直接解析。請先使用 EPUB 或無 DRM 的來源版本。');
  throw new Error(`暫不支援 .${ext || '未知'} 檔案`);
}

function escapeHtml(value = '') { return String(value).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' }[c])); }
function roleOptions(selected) { return ROLE_OPTIONS.map(([value, label]) => `<option value="${value}" ${value === selected ? 'selected' : ''}>${label}</option>`).join(''); }

function renderPreview() {
  const preview = $('#preview');
  $('#previewCount').textContent = `${state.nodes.length} 個區塊`;
  preview.innerHTML = state.nodes.map((node, index) => `
    <article class="preview-item" data-index="${index}"><div class="preview-index">${String(index + 1).padStart(2, '0')}</div><div class="preview-main"><div class="preview-controls"><select data-field="role" aria-label="內容類型">${roleOptions(node.role)}</select><input data-field="title" value="${escapeHtml(node.title)}" aria-label="標題"><button type="button" data-move="up" aria-label="上移">↑</button><button type="button" data-move="down" aria-label="下移">↓</button></div><div class="source-label">${escapeHtml(node.sourceFile)}</div><pre>${escapeHtml(node.content.slice(0, 900))}${node.content.length > 900 ? '\n…' : ''}</pre></div></article>`).join('');
  $('#importAction').disabled = !state.nodes.length;
}

function swapNodes(a, b) { if (b < 0 || b >= state.nodes.length) return; [state.nodes[a], state.nodes[b]] = [state.nodes[b], state.nodes[a]]; state.nodes.forEach((node, index) => { node.order = index; }); renderPreview(); }
function bindPreview() { $('#preview').addEventListener('input', (event) => { const item = event.target.closest('.preview-item'); if (!item) return; const node = state.nodes[Number(item.dataset.index)]; const field = event.target.dataset.field; if (field) node[field] = event.target.value; }); $('#preview').addEventListener('click', (event) => { const button = event.target.closest('[data-move]'); if (!button) return; const item = button.closest('.preview-item'); const index = Number(item.dataset.index); swapNodes(index, button.dataset.move === 'up' ? index - 1 : index + 1); }); }

async function consumeFiles(files) {
  const accepted = [], failures = [];
  for (const file of files) {
    try { const text = await extractFile(file); accepted.push({ sourceFile: file.name, text }); state.sources.push({ name: file.name, type: file.type || 'unknown', size: file.size }); }
    catch (error) { failures.push(`${file.name}: ${error.message}`); }
  }
  if (accepted.length) { state.nodes = mergeImports(accepted); renderPreview(); $('#stepPreview').hidden = false; $('#stepPreview').scrollIntoView({ behavior: 'smooth', block: 'start' }); }
  if (failures.length) showStatus(failures.join('；'), 'error');
}
function showStatus(message, kind = 'ok') { const status = $('#status'); status.textContent = message; status.dataset.kind = kind; status.hidden = false; }

async function renderLibrary() {
  const list = $('#bookList');
  try {
    const local = await listBooks(); const golden = await fetch('./books/kingdom-language/manifest.json').then((r) => r.ok ? r.json() : null).catch(() => null); const items = [...(golden ? [golden] : []), ...local];
    if (!items.length) { list.innerHTML = '<div class="empty">還沒有書稿。可以建立新書，或把舊稿匯入。</div>'; return; }
    list.innerHTML = items.map((book) => { const isGolden = Boolean(book.import?.goldenCase); const body = `<div class="book-kicker">${isGolden ? 'IMPORTED · GOLDEN CASE' : 'MY BOOK'}</div><h3>${escapeHtml(book.title)}</h3><p>${escapeHtml(book.subtitle || '')}</p><div class="book-meta">${book.nodes?.length ?? book.structure?.length ?? 0} 個內容單元</div>`; return `<a class="book-card book-card-link" href="/multiwrite/book.html?id=${encodeURIComponent(book.id)}" aria-label="打開《${escapeHtml(book.title)}》">${body}<div class="book-open">打開書稿 →</div></a>`; }).join('');
  } catch (error) { list.innerHTML = `<div class="empty">書庫讀取失敗：${escapeHtml(error.message)}</div>`; }
}

function resetImport() { state.nodes = []; state.sources = []; $('#pasteInput').value = ''; $('#fileInput').value = ''; $('#stepPreview').hidden = true; $('#status').hidden = true; renderPreview(); }
function init() {
  const dropZone = $('#dropZone'), fileInput = $('#fileInput');
  $('#openImport').addEventListener('click', () => { $('#importPanel').hidden = false; $('#importPanel').scrollIntoView({ behavior: 'smooth' }); });
  $('#cancelImport').addEventListener('click', () => { resetImport(); $('#importPanel').hidden = true; });
  $('#chooseFiles').addEventListener('click', () => fileInput.click()); fileInput.addEventListener('change', () => consumeFiles([...fileInput.files]));
  ['dragenter', 'dragover'].forEach((name) => dropZone.addEventListener(name, (event) => { event.preventDefault(); dropZone.classList.add('dragging'); }));
  ['dragleave', 'drop'].forEach((name) => dropZone.addEventListener(name, (event) => { event.preventDefault(); dropZone.classList.remove('dragging'); }));
  dropZone.addEventListener('drop', (event) => consumeFiles([...event.dataTransfer.files]));
  $('#parsePaste').addEventListener('click', () => { const text = $('#pasteInput').value; if (!text.trim()) return showStatus('請先貼上文字。', 'error'); state.sources = [{ name: '貼上文字', type: 'text/plain', size: new Blob([text]).size }]; state.nodes = mergeImports([{ sourceFile: '貼上文字', text }]); renderPreview(); $('#stepPreview').hidden = false; $('#stepPreview').scrollIntoView({ behavior: 'smooth', block: 'start' }); });
  $('#importAction').addEventListener('click', async () => { const explicitTitle = $('#bookTitle').value.trim(); const book = buildBook({ title: explicitTitle, nodes: state.nodes, sources: state.sources }); const validation = validateBook(book); if (!validation.valid) return showStatus(validation.errors.join('；'), 'error'); await saveBook(book); showStatus(`《${book.title}》已加入我的書。原稿內容未經 AI 改寫。`); await renderLibrary(); setTimeout(() => { resetImport(); $('#importPanel').hidden = true; $('#library').scrollIntoView({ behavior: 'smooth' }); }, 500); });
  bindPreview(); renderPreview(); renderLibrary();
}
init();