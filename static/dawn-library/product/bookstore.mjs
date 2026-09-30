import { localReadingPack, resolveReading } from '../../js/dawn-reading-resolver.mjs';
import { dawnLibrary } from './library-system.mjs';

const $ = selector => document.querySelector(selector);
const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;'}[c]));
const scroll = selector => $(selector).scrollIntoView({behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start'});
const fabric = () => Promise.resolve(dawnLibrary);
const author = work => (work.authors || []).join(' · ');
const safeUrl = value => {
  try { const url = new URL(value, location.href); return ['https:', 'http:'].includes(url.protocol) ? url.href : ''; }
  catch { return ''; }
};
function cover(work, className) {
  const src = safeUrl(work.cover?.src || work.cover?.url || '');
  const fallback = className === 'cover' ? 'cover-fallback' : 'dawn-cover-stream__fallback';
  return src && (work.cover?.src || work.cover?.url)
    ? `<img class="${className}" src="${esc(src)}" alt="" loading="lazy" decoding="async" data-fallback="${fallback}">`
    : `<span class="${fallback}">暫無封面</span>`;
}
// A missing cover must never trigger one metadata request per book.
document.addEventListener('error', event => {
  const img = event.target;
  if (!img.matches?.('img[data-fallback]')) return;
  const fallback = document.createElement('span');
  fallback.className = img.dataset.fallback;
  fallback.textContent = '暫無封面';
  img.replaceWith(fallback);
}, true);
function cards(host, rows, className) {
  host.innerHTML = rows.map((work, i) => `<button type="button" class="${className}" data-i="${i}">${cover(work, className === 'dawn-cover-stream__work' ? 'collection-cover' : 'cover')}<span><strong>${esc(work.title)}</strong><small>${esc(author(work))}</small></span></button>`).join('');
  host.querySelectorAll('[data-i]').forEach(button => {
    button.onclick = () => choose(rows[Number(button.dataset.i)]);
  });
}
function packText(pack, activeMode) {
  const source = pack.segments.map(segment => `<p class="reader-text">${esc(segment.source)}</p>`).join('');
  const translation = pack.segments.map(segment => `<p class="reader-text" lang="zh-Hant">${esc(segment.translation)}</p>`).join('');
  if (activeMode === 'zh-Hant') return translation;
  if (activeMode === 'bilingual') return `<div class="reader-columns"><div>${source}</div><div>${translation}</div></div>`;
  return source;
}

let selected, reading, selectionTicket = 0, mode = 'source';
function renderReader() {
  const hasTranslation = Boolean(reading?.translation || reading?.pack?.segments?.length);
  document.querySelectorAll('[data-mode]').forEach(button => {
    button.disabled = button.dataset.mode !== 'source' && !hasTranslation;
    button.setAttribute('aria-pressed', String(button.dataset.mode === mode));
    button.removeAttribute('aria-current');
  });
  if (!reading) {
    $('#reader-body').textContent = selected ? '正在載入閱讀版本…' : '左頁尋書。右頁閱讀。';
  } else if (reading.pack?.segments?.length) {
    const url = safeUrl(reading.sourcePage || reading.pack.source?.url || '');
    const notice = reading.pack.scope === 'editorial-sample'
      ? '這是黎明隨站發佈、逐段對照的試讀。完整原文保留在原館藏。'
      : '這是黎明隨站發佈、逐段對照的閱讀包。';
    $('#reader-body').innerHTML = `<p class="reader-note">${notice}</p>${packText(reading.pack, mode)}${url ? `<a class="reader-link" href="${esc(url)}" target="_blank" rel="noopener noreferrer">閱讀完整原文 ↗</a>` : ''}`;
  } else if (reading.kind === 'text') {
    const source = `<div class="reader-text">${esc(reading.text)}</div>`;
    const translation = `<div class="reader-text">${esc(reading.translation)}</div>`;
    $('#reader-body').innerHTML = mode === 'bilingual' && hasTranslation ? `<div class="reader-columns">${source}${translation}</div>` : mode === 'zh-Hant' && hasTranslation ? translation : source;
    if (!hasTranslation) $('#reader-body').insertAdjacentHTML('beforeend', '<p class="reader-note">此版本暫無繁中譯文。</p>');
  } else {
    const url = safeUrl(reading.sourcePage || '');
    $('#reader-body').innerHTML = reading.sourcePage && url
      ? `<p class="reader-note">原文保留在原館藏。本書尚未有隨站發佈的繁中閱讀包，因此不會以機器翻譯替代。</p><a class="reader-link" href="${esc(url)}" target="_blank" rel="noopener noreferrer">前往原館藏 ↗</a>`
      : '<p class="reader-note">這本書目前尚未提供可閱讀版本。</p>';
  }
}
async function choose(preview) {
  const ticket = ++selectionTicket;
  selected = preview;
  reading = null;
  mode = 'source';
  $('#reader-title').textContent = preview.title;
  $('#reader-author').textContent = author(preview);
  renderReader();
  scroll('#reader');
  try {
    const api = await fabric();
    const canonical = await api.resourceWork(preview.workId);
    if (ticket !== selectionTicket) return;
    if (!canonical) throw new Error('Missing canonical work');
    const [result, pack] = await Promise.all([resolveReading(canonical), localReadingPack(canonical.workId)]);
    if (ticket !== selectionTicket) return;
    selected = canonical;
    reading = {...result, pack};
    $('#reader-title').textContent = canonical.title;
    $('#reader-author').textContent = author(canonical);
    renderReader();
  } catch (error) {
    if (ticket !== selectionTicket) return;
    $('#reader-body').innerHTML = '<p class="reader-note">閱讀資料暫時無法載入，請稍後重新選書。</p>';
    console.error('[Dawn] reader', error);
  }
}
document.querySelectorAll('[data-mode]').forEach(button => button.onclick = () => { mode = button.dataset.mode; renderReader(); });
$('#jump-morning').onclick = () => scroll('#morning');
$('#jump-reading').onclick = () => scroll('#reading-entry');
$('#jump-catalogue').onclick = () => scroll('#catalogue');
$('#jump-lower').onclick = () => scroll('#library-lower');
$('#jump-search').onclick = () => { scroll('#catalogue'); $('#search').focus({preventScroll: true}); };
renderReader();

async function readingShelf() {
  try {
    $('#reading-entry .reader-note').textContent = '閱讀包含原文與繁中對照，隨網站版本發佈；不下載館藏正文、翻譯模型，也不呼叫翻譯 API。';
    const packs = await dawnLibrary.readingPacks();
    const rows = packs.items || [];
    $('#reader-ready').innerHTML = rows.map((item, i) => `<button type="button" class="reader-ready-card" data-reader-pack="${i}"><strong>${esc(item.title)}</strong><small>原文 · 繁中 · 對照</small></button>`).join('');
    $('#reader-ready').querySelectorAll('[data-reader-pack]').forEach(button => {
      button.onclick = async () => {
        const item = rows[Number(button.dataset.readerPack)];
        try {
          const api = await fabric();
          const work = await api.resourceWork(item.workId);
          if (work) choose(work);
        } catch (error) { console.error('[Dawn] reading shelf', error); }
      };
    });
    $('#reader-ready-status').textContent = rows.length ? '所有試讀內容隨本頁發佈；閱讀過程不下載正文或模型。' : '尚無可用閱讀包。';
  } catch (error) {
    $('#reader-ready-status').textContent = '閱讀包暫時無法載入。';
    console.error('[Dawn] reading packs', error);
  }
}

function chineseCards(items) {
  return items.map(item => {
    const title = item.work?.title || '';
    const creator = item.work?.creator || '';
    const meta = [item.edition?.year, item.classification?.label].filter(Boolean).join(' · ');
    const source = safeUrl(item.cover?.url || '');
    const visual = source
      ? `<img class="chinese-cover" src="${esc(source)}" alt="${esc(title)} 封面" loading="lazy" decoding="async">`
      : `<span class="chinese-cover chinese-cover--fallback" role="img" aria-label="${esc(title)} 黎明書局版封面"><i>DAWN LIBRARY</i><strong>${esc(title)}</strong><small>${esc(creator)}</small></span>`;
    const href = safeUrl(item.access?.url || item.source?.catalogUrl || '');
    const body = `${visual}<span><strong>${esc(title)}</strong><small>${esc(creator)}</small>${meta ? `<small>${esc(meta)}</small>` : ''}<em>${esc(item.access?.label || '查看館藏')} ↗</em></span>`;
    return href
      ? `<a class="chinese-work" href="${esc(href)}" target="_blank" rel="noopener noreferrer">${body}</a>`
      : `<div class="chinese-work">${body}</div>`;
  }).join('');
}

async function chineseCollection() {
  try {
    const collection = await dawnLibrary.chineseCollection();
    const works = collection.works || [];
    const section = document.createElement('section');
    section.className = 'section chinese-collection';
    section.id = 'chinese-collection';
    const render = expanded => {
      const visible = expanded ? works : works.slice(0, 8);
      section.innerHTML = `<div class="section-title"><h2>Chinese Collection</h2><span>中文館藏 · ${esc(collection.count)} 本</span></div><p class="reader-note">早期中文基督教著作。依靈修、教會歷史、神學與倫理編目；正文保留於原館藏。</p><div class="chinese-works">${chineseCards(visible)}</div>${expanded ? '' : '<button type="button" class="show-chinese">查看完整索引</button>'}`;
      section.querySelector('.show-chinese')?.addEventListener('click', () => render(true));
    };
    render(false);
    $('#morning').before(section);
  } catch (error) {
    console.error('[Dawn] Chinese collection', error);
  }
}

// Each surface starts independently. Catalogue failure cannot hide covers.
async function morningStars() {
  try {
    const morning = await dawnLibrary.morningStars();
    const api = await fabric();
    const ids = morning.items.map(item => item.workId);
    const works = await api.resourceWorks(ids);
    const rows = ids.map(id => works.get(id)).filter(Boolean);
    cards($('#stars'), rows, 'star');
    $('#stars-status').textContent = rows.length === 3 ? '' : '部分推薦書目暫時無法載入。';
  } catch (error) {
    $('#stars-status').textContent = '三晨星暫時無法載入；仍可瀏覽下方館藏。';
    console.error('[Dawn] morning stars', error);
  }
}
let featured = [], total = null, searchTicket = 0, searchTimer;
function showCatalogue(rows, count) {
  cards($('#works'), rows.slice(0, 24), 'work');
  $('#count').textContent = count == null ? '' : `${count.toLocaleString()} WORKS`;
  $('#catalogue-status').textContent = rows.length > 24 ? `顯示前 24 筆，共 ${rows.length.toLocaleString()} 筆符合；可輸入更完整的書名或作者縮小範圍。` : rows.length ? '' : '沒有符合的館藏。';
}
async function catalogue() {
  try {
    const api = await fabric();
    featured = await api.resourceFeatured({limit: 24});
    if (!$('#search').value.trim()) showCatalogue(featured, total);
  } catch (error) {
    if (!$('#search').value.trim()) $('#catalogue-status').textContent = '精選館藏暫時無法載入；可嘗試搜尋或瀏覽下方封面。';
    console.error('[Dawn] catalogue', error);
  }
}
$('#search').oninput = () => {
  const query = $('#search').value.trim(), ticket = ++searchTicket;
  clearTimeout(searchTimer);
  if (!query) { showCatalogue(featured, total); return; }
  $('#catalogue-status').textContent = '正在搜尋…';
  searchTimer = setTimeout(async () => {
    try {
      const api = await fabric(), rows = await api.resourceSearch(query);
      if (ticket === searchTicket) showCatalogue(rows, rows.length);
    } catch (error) {
      if (ticket === searchTicket) $('#catalogue-status').textContent = '搜尋暫時無法完成，請稍後再試。';
      console.error('[Dawn] search', error);
    }
  }, 300);
};

// Explicit batches avoid unbounded IntersectionObserver / iframe resize loops.
let coverRoot, shardIndex = 0, pending = [], visible = [], busy = false;
async function moreCovers() {
  if (busy) return;
  busy = true;
  $('#collection-more').disabled = true;
  $('#collection-status').textContent = '正在載入封面…';
  try {
    coverRoot ||= await dawnLibrary.coverPreviewRoot();
    while (!pending.length && shardIndex < coverRoot.shards.length) {
      const shard = await dawnLibrary.coverPreviewShard(coverRoot.shards[shardIndex].href);
      pending = shard.items || [];
      shardIndex++;
    }
    const batch = pending.splice(0, 36);
    visible.push(...batch);
    // Keep the document bounded even during a long browsing session.
    visible = visible.slice(-144);
    cards($('#collection-rail'), visible, 'dawn-cover-stream__work');
    $('#collection-status').textContent = `目前顯示 ${visible.length} 本書；無可用封面的書目仍可選取。`;
    $('#collection-more').hidden = !pending.length && shardIndex >= coverRoot.shards.length;
  } catch (error) {
    $('#collection-status').textContent = '封面暫時無法載入，請按下方按鈕重試。';
    console.error('[Dawn] covers', error);
  } finally {
    busy = false;
    $('#collection-more').disabled = false;
  }
}
$('#collection-more').onclick = moreCovers;
moreCovers();
readingShelf();
chineseCollection();
morningStars();
catalogue();
fabric().then(api => api.resourceManifest()).then(manifest => {
  total = manifest.workCount;
  if (manifest.indexedWorkCount < total) $('#search-scope').textContent = `目前可搜尋 ${manifest.indexedWorkCount.toLocaleString()} 本已索引書目；完整館藏可於下方分批瀏覽。`;
  $('#lower-count').textContent = `${total.toLocaleString()} Works`;
  if (!$('#search').value.trim()) $('#count').textContent = `${total.toLocaleString()} WORKS`;
}).catch(() => { $('#lower-count').textContent = '館藏'; });
