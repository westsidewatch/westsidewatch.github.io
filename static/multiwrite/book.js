const $ = (sel) => document.querySelector(sel);
const params = new URLSearchParams(location.search);
const bookId = params.get('id') || 'kingdom-language';

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

async function loadPart(item, index) {
  const reader = $('#readerContent');
  document.querySelectorAll('.toc-link').forEach((el) => el.classList.toggle('active', Number(el.dataset.index) === index));
  reader.innerHTML = '<p class="reader-loading">正在載入…</p>';
  try {
    const base = `./books/${bookId}/`;
    let text = '';
    if (item.file) {
      text = await fetchText(base + item.file);
    } else if (Array.isArray(item.files)) {
      const parts = await Promise.all(item.files.map((file) => fetchText(base + file)));
      text = parts.join('\n\n');
    }
    reader.innerHTML = `<div class="reader-role">${escapeHtml(item.role === 'appendix' ? 'APPENDIX' : item.role === 'front_matter' ? 'FRONT MATTER' : 'CHAPTER')}</div><h2>${escapeHtml(item.title || '')}</h2><div class="reader-body">${renderMarkdownish(text)}</div>`;
    reader.scrollIntoView({ block: 'start' });
  } catch (error) {
    reader.innerHTML = `<p class="reader-error">${escapeHtml(error.message)}</p>`;
  }
}

async function init() {
  try {
    const manifestRes = await fetch(`./books/${bookId}/manifest.json`);
    if (!manifestRes.ok) throw new Error('找不到這本書。');
    const book = await manifestRes.json();
    document.title = `${book.title} · 多寫`;
    $('#bookTitle').textContent = book.title;
    $('#bookSubtitle').textContent = book.subtitle || '';

    const toc = $('#toc');
    toc.innerHTML = book.structure.map((item, index) => `
      <button class="toc-link toc-${escapeHtml(item.role)}" data-index="${index}" type="button">
        <span class="toc-num">${String(index + 1).padStart(2, '0')}</span>
        <span>${escapeHtml(item.title || (item.role === 'front_matter' ? '前置內容' : '未命名'))}</span>
      </button>`).join('');
    toc.addEventListener('click', (event) => {
      const button = event.target.closest('.toc-link');
      if (!button) return;
      loadPart(book.structure[Number(button.dataset.index)], Number(button.dataset.index));
    });

    const firstChapter = Math.max(0, book.structure.findIndex((item) => item.role === 'chapter'));
    loadPart(book.structure[firstChapter], firstChapter);
  } catch (error) {
    $('#readerContent').innerHTML = `<p class="reader-error">${escapeHtml(error.message)}</p>`;
  }
}

init();
