import {dawnBookEntry,canImportToPersonal} from './library-model.mjs';

const CATALOG_URL='/dawn-library/biblical-world/catalog.json';

function esc(value=''){return String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));}
function fallbackCover(book){const cover=book.cover||{};return `<div class="dawn-cover dawn-cover-one" aria-hidden="true"><div class="dawn-cover-rule"></div><div class="dawn-cover-copy"><span>黎明書局</span><strong>${esc(cover.title||book.work?.title||'UNTITLED')}</strong><small>${esc(cover.author||book.work?.author||'')}</small></div></div>`;}

function renderBook(raw){
  const entry=dawnBookEntry(raw),book=entry.book,work=book.work||{},edition=book.edition||{},source=book.sources?.[0];
  const cover=book.cover?.url?`<div class="dawn-cover"><img src="${esc(book.cover.url)}" alt="${esc(work.title||'書籍封面')}" loading="lazy"></div>`:fallbackCover(book);
  const read=source?.url?`<a class="dawn-read" href="${esc(source.url)}" target="_blank" rel="noopener">開始閱讀 →</a>`:'<span class="dawn-read dawn-read-pending">來源整理中</span>';
  const add=canImportToPersonal(entry)&&source?.url?`<button class="dawn-add" type="button" data-dawn-add="${esc(book.id)}" title="閱讀時按需取得內容，建立個人副本後才進入我的書">＋ 加到我的書</button>`:'';
  return `<article class="dawn-book" data-library-origin="dawn">${cover}<div class="dawn-book-copy"><p>${edition.publicDomain?'PUBLIC DOMAIN':'黎明書局'}</p><h3>${esc(work.title||'未命名')}</h3><div>${esc(work.author||'')}</div><small>${(book.relations||[]).map(esc).join(' · ')}</small><div class="dawn-actions">${read}${add}</div></div></article>`;
}

async function loadCatalog(){const response=await fetch(CATALOG_URL,{cache:'force-cache'});if(!response.ok)throw new Error(`catalog ${response.status}`);return response.json();}
async function renderDawnLibrary(){const wall=document.getElementById('dawnLibraryWall'),status=document.getElementById('dawnLibraryStatus');if(!wall)return;try{const catalog=await loadCatalog();wall.innerHTML=(catalog.items||[]).map(renderBook).join('');if(status)status.textContent=`${catalog.items?.length||0} 本公版書 · 黎明書局館藏，不等於我的書`;}catch(error){wall.innerHTML='<p class="dawn-library-error">黎明書局索引暫時無法讀取。</p>';if(status)status.textContent='';console.warn('Dawn Library projection failed',error);}}

document.getElementById('dawnLibraryWall')?.addEventListener('click',async event=>{
  const button=event.target.closest('[data-dawn-add]');if(!button)return;
  // Boundary is deliberate: catalog entries never write directly into IndexedDB.
  // The next intake step resolves/downloads the selected public edition on demand,
  // then creates a NEW personal Multiwrite book with its own local id and provenance.
  const id=button.dataset.dawnAdd;
  button.disabled=true;button.textContent='準備加入…';
  window.dispatchEvent(new CustomEvent('multiwrite:dawn-import-request',{detail:{catalogId:id}}));
  setTimeout(()=>{button.disabled=false;button.textContent='＋ 加到我的書';},800);
});

document.addEventListener('DOMContentLoaded',renderDawnLibrary);
