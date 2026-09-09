const DB_NAME='multiwrite-v1';
const DB_VERSION=3;
const BOOK_STORE='books';
const DRAFT_STORE='drafts';
const STUDY_STORE='studyDocuments';

function openDb(){return new Promise((resolve,reject)=>{const req=indexedDB.open(DB_NAME,DB_VERSION);req.onupgradeneeded=()=>{const db=req.result;if(!db.objectStoreNames.contains(BOOK_STORE))db.createObjectStore(BOOK_STORE,{keyPath:'id'});if(!db.objectStoreNames.contains(DRAFT_STORE))db.createObjectStore(DRAFT_STORE,{keyPath:'id'});if(!db.objectStoreNames.contains(STUDY_STORE))db.createObjectStore(STUDY_STORE,{keyPath:'id'});};req.onsuccess=()=>resolve(req.result);req.onerror=()=>reject(req.error);});}
function makeId(){return `book-${Date.now().toString(36)}-${Math.random().toString(36).slice(2,9)}`;}
function escapeHtml(v=''){return String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));}
async function putBook(book){const db=await openDb();return new Promise((resolve,reject)=>{const tx=db.transaction(BOOK_STORE,'readwrite');tx.objectStore(BOOK_STORE).put(book);tx.oncomplete=()=>{db.close();resolve(book)};tx.onerror=()=>{db.close();reject(tx.error)};});}
async function listBooks(){const db=await openDb();return new Promise((resolve,reject)=>{const tx=db.transaction(BOOK_STORE,'readonly');const req=tx.objectStore(BOOK_STORE).getAll();req.onsuccess=()=>{const out=req.result||[];db.close();resolve(out)};req.onerror=()=>{db.close();reject(req.error)};});}
async function createBook(){const id=makeId();const now=new Date().toISOString();const book={schema:'multiwrite.book.v1',id,title:'未命名書稿',subtitle:'',createdAt:now,updatedAt:now,import:{mode:'new',aiTransformed:false,sourceCount:0,sources:[]},nodes:[{id:`part-${Date.now().toString(36)}`,role:'chapter',title:'第一章',content:'',sourceFile:'',order:0,headingLevel:1}]};await putBook(book);location.assign(`/multiwrite/book.html?id=${encodeURIComponent(id)}`);}
async function renderLocalLibrary(){const list=document.getElementById('bookList');if(!list)return;try{const local=await listBooks();const golden=await fetch('./books/kingdom-language/manifest.json').then(r=>r.ok?r.json():null).catch(()=>null);const items=[...(golden?[{...golden,__golden:true}]:[]),...local];if(!items.length){list.innerHTML='<div class="empty">還沒有書稿。可以建立新書，或把舊稿匯入。</div>';return;}list.innerHTML=items.map(book=>{const count=book.nodes?.length??book.structure?.length??0;const body=`<div class="book-kicker">${book.__golden?'IMPORTED · GOLDEN CASE':'MY BOOK'}</div><h3>${escapeHtml(book.title||'未命名書稿')}</h3><p>${escapeHtml(book.subtitle||'')}</p><div class="book-meta">${count} 個內容單元</div><div class="book-open">打開書稿 →</div>`;return `<a class="book-card book-card-link" href="/multiwrite/book.html?id=${encodeURIComponent(book.id)}" aria-label="打開《${escapeHtml(book.title||'未命名書稿')}》">${body}</a>`;}).join('');}catch(error){list.innerHTML=`<div class="empty">書庫讀取失敗：${escapeHtml(error.message)}</div>`;}}
const createButton=document.getElementById('createBook');
createButton?.addEventListener('click',()=>createBook().catch(error=>{const list=document.getElementById('bookList');if(list)list.innerHTML=`<div class="empty">建立新書失敗：${escapeHtml(error.message)}</div>`;}));
window.addEventListener('pageshow',renderLocalLibrary);
setTimeout(renderLocalLibrary,0);
