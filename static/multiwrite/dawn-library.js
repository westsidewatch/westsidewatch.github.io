const CATALOG_URL='/dawn-library/biblical-world/catalog.json';

function esc(value=''){return String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));}

function fallbackCover(book){
  const cover=book.cover||{};
  return `<div class="dawn-cover dawn-cover-one" aria-hidden="true"><div class="dawn-cover-rule"></div><div class="dawn-cover-copy"><span>黎明書局</span><strong>${esc(cover.title||book.work?.title||'UNTITLED')}</strong><small>${esc(cover.author||book.work?.author||'')}</small></div></div>`;
}

function renderBook(book){
  const work=book.work||{}, edition=book.edition||{}, source=book.sources?.[0];
  const cover=book.cover?.url?`<div class="dawn-cover"><img src="${esc(book.cover.url)}" alt="${esc(work.title||'書籍封面')}" loading="lazy"></div>`:fallbackCover(book);
  const action=source?.url?`<a class="dawn-read" href="${esc(source.url)}" target="_blank" rel="noopener">開始閱讀 →</a>`:'<span class="dawn-read dawn-read-pending">來源整理中</span>';
  return `<article class="dawn-book">${cover}<div class="dawn-book-copy"><p>${edition.publicDomain?'PUBLIC DOMAIN':'黎明書局'}</p><h3>${esc(work.title||'未命名')}</h3><div>${esc(work.author||'')}</div><small>${(book.relations||[]).map(esc).join(' · ')}</small>${action}</div></article>`;
}

async function renderDawnLibrary(){
  const wall=document.getElementById('dawnLibraryWall'), status=document.getElementById('dawnLibraryStatus');
  if(!wall)return;
  try{
    const response=await fetch(CATALOG_URL,{cache:'force-cache'});
    if(!response.ok)throw new Error(`catalog ${response.status}`);
    const catalog=await response.json();
    wall.innerHTML=(catalog.items||[]).map(renderBook).join('');
    if(status)status.textContent=`${catalog.items?.length||0} 本公版書 · 只讀取索引與封面，不下載全文`;
  }catch(error){
    wall.innerHTML='<p class="dawn-library-error">黎明書局索引暫時無法讀取。</p>';
    if(status)status.textContent='';
    console.warn('Dawn Library projection failed',error);
  }
}

document.addEventListener('DOMContentLoaded',renderDawnLibrary);
