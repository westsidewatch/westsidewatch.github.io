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

function draftId(index) { return `${bookId}:${index}`; }
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
  if (Array.isArray(item.files)) return (await Promise.all(item.files.map((file) => fetchText(base + file)))).join('\n\n');
  return '';
}
async function persistOpenEditor() {
  const editor = document.querySelector('#chapterEditor');
  const active = document.querySelector('.toc-link.active');
  if (!editor || !active) return;
  const index = Number(active.dataset.index);
  if (Number.isInteger(index)) await putDraft(index, editor.value);
}
async function collectBook() {
  const response = await fetch(`./books/${bookId}/manifest.json`, { cache: 'no-store' });
  if (!response.ok) throw new Error('找不到這本書。');
  const book = await response.json();
  const sections = await Promise.all(book.structure.map(async (item, index) => {
    const draft = await getDraft(index);
    return { index, role: item.role, title: item.title || '', draft: Boolean(draft), text: draft?.text ?? await fetchOriginal(item) };
  }));
  return { book, sections };
}
function downloadFile(filename, content, type) {
  const blob = content instanceof Blob ? content : new Blob([content], { type });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = filename; document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1500);
}
function loadScript(src, globalName) {
  if (globalName && window[globalName]) return Promise.resolve(window[globalName]);
  return new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = src; script.onload = () => resolve(globalName ? window[globalName] : true);
    script.onerror = () => reject(new Error('導出元件載入失敗，請檢查網路後重試。'));
    document.head.appendChild(script);
  });
}
function plainLines(text = '') {
  return String(text).replace(/\r\n?/g, '\n').split('\n').map(line => line.replace(/^#{1,6}\s+/, ''));
}
async function exportDocx(book, sections, baseName) {
  const docx = await loadScript('https://cdn.jsdelivr.net/npm/docx@9.5.1/dist/index.umd.cjs', 'docx');
  const { Document, Packer, Paragraph, HeadingLevel, PageBreak, TextRun } = docx;
  const children = [
    new Paragraph({ text: book.title || '', heading: HeadingLevel.TITLE }),
    ...(book.subtitle ? [new Paragraph({ text: book.subtitle, heading: HeadingLevel.SUBTITLE })] : []),
    new Paragraph({ children: [new PageBreak()] }),
  ];
  sections.forEach((section, sectionIndex) => {
    if (section.title) children.push(new Paragraph({ text: section.title, heading: section.role === 'section' ? HeadingLevel.HEADING_2 : HeadingLevel.HEADING_1 }));
    plainLines(section.text).forEach((line) => {
      const heading = line.match(/^\s*$/) ? null : String(line);
      children.push(new Paragraph({ children: heading ? [new TextRun(heading)] : [] }));
    });
    if (sectionIndex < sections.length - 1) children.push(new Paragraph({ children: [new PageBreak()] }));
  });
  const document = new Document({ sections: [{ properties: {}, children }] });
  const blob = await Packer.toBlob(document);
  downloadFile(`${baseName}.docx`, blob, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document');
}
function escapeHtml(value = '') {
  return String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));
}
function printHtml(book, sections) {
  const body = sections.map(section => `<section class="chapter"><h1>${escapeHtml(section.title)}</h1>${String(section.text).replace(/\r\n?/g,'\n').split(/\n\s*\n/).map(p => `<p>${escapeHtml(p.replace(/^#{1,6}\s+/gm,'')).replace(/\n/g,'<br>')}</p>`).join('')}</section>`).join('');
  return `<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><title>${escapeHtml(book.title)}</title><style>@page{size:A4;margin:22mm 20mm}body{font-family:"Noto Serif TC","Songti TC","PMingLiU",serif;color:#1f1c17;font-size:12pt;line-height:1.9}main{max-width:165mm;margin:auto}.cover{height:235mm;display:flex;flex-direction:column;justify-content:center;text-align:center;page-break-after:always}.cover h1{font-size:28pt;font-weight:500}.cover h2{font-size:15pt;font-weight:400}.chapter{page-break-before:always}.chapter:first-of-type{page-break-before:auto}.chapter h1{font-size:20pt;margin:0 0 2em}.chapter p{text-indent:2em;margin:.8em 0;orphans:3;widows:3}button{position:fixed;right:18px;top:18px;padding:10px 16px}@media print{button{display:none}}</style></head><body><button onclick="window.print()">儲存為 PDF / 列印</button><main><div class="cover"><h1>${escapeHtml(book.title)}</h1>${book.subtitle ? `<h2>${escapeHtml(book.subtitle)}</h2>` : ''}</div>${body}</main><script>setTimeout(()=>window.print(),350)<\/script></body></html>`;
}
function exportPdf(book, sections) {
  const popup = window.open('', '_blank');
  if (!popup) throw new Error('瀏覽器阻止了 PDF 視窗，請允許此網站開啟彈出視窗。');
  popup.document.open(); popup.document.write(printHtml(book, sections)); popup.document.close();
}
function injectControls() {
  if (document.querySelector('#exportBook')) return;
  const actions = document.querySelector('.book-actions');
  if (!actions) return;
  const wrap = document.createElement('div');
  wrap.className = 'export-controls';
  wrap.innerHTML = `<select id="exportFormat" class="export-select" aria-label="導出格式"><option value="docx">Word · DOCX</option><option value="pdf">PDF · 列印版</option><option value="md">Markdown</option><option value="txt">TXT</option><option value="json">JSON 備份</option></select><button id="exportBook" class="book-action" type="button">導出</button>`;
  actions.before(wrap);
  document.querySelector('#exportBook').addEventListener('click', exportBook);
}
async function exportBook() {
  const button = document.querySelector('#exportBook');
  const format = document.querySelector('#exportFormat')?.value || 'docx';
  const saveState = document.querySelector('#saveState');
  if (!button) return;
  const originalLabel = button.textContent; button.disabled = true; button.textContent = '導出中…';
  try {
    await persistOpenEditor();
    const { book, sections } = await collectBook();
    const baseName = safeFilename(book.title || bookId);
    if (format === 'docx') await exportDocx(book, sections, baseName);
    else if (format === 'pdf') exportPdf(book, sections);
    else if (format === 'json') downloadFile(`${baseName}.multiwrite.json`, JSON.stringify(buildExportBackup(book, sections), null, 2), 'application/json;charset=utf-8');
    else {
      const ext = format === 'txt' ? 'txt' : 'md';
      downloadFile(`${baseName}.${ext}`, mergeExportSections(sections), format === 'txt' ? 'text/plain;charset=utf-8' : 'text/markdown;charset=utf-8');
    }
    if (saveState) saveState.textContent = format === 'pdf' ? '已開啟 PDF 列印版' : `已導出 ${format.toUpperCase()}`;
  } catch (error) { if (saveState) saveState.textContent = `導出失敗：${error.message}`; }
  finally { button.disabled = false; button.textContent = originalLabel; }
}
injectControls();
