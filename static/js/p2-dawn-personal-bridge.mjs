/**
 * P2 05 ↔ original Formal Edition Personal Dawn adapter.
 * This file owns NO second personal state schema, Work record, or catalog.
 * The canonical original store key is dawn.personal-state.v1, shared with
 * /dawn-library/formal-edition/phase4/.
 */
import {
  createPersonalState, createLocalPersonalStore, saveBookmark, removeBookmark,
  saveView, saveTrail, exportPersonalState, importPersonalState
} from '/dawn-library/formal-edition/runtime/personal-state.mjs';

const $=s=>document.querySelector(s);
const dialog=$('#dawn-personal-dialog');
const openButton=$('#dawn-personal-open');
const closeButton=$('#dawn-personal-close');
const shelf=$('#dawn-personal-items');
const count=$('#dawn-personal-count');
const bookmarkButton=$('#dawn-book-bookmark');
const personalView=$('#dawn-personal-view');
const personalTrail=$('#dawn-personal-trail');
const personalExport=$('#dawn-personal-export');
const personalImport=$('#dawn-personal-import');
if(!dialog||!openButton||!bookmarkButton||!shelf){
  throw new Error('Dawn Personal bridge: required reader controls missing');
}
let store;
try{store=createLocalPersonalStore(window.localStorage)}
catch{
  const memory=new Map();
  store=createLocalPersonalStore({getItem:k=>memory.get(k)||null,setItem:(k,v)=>memory.set(k,v),removeItem:k=>memory.delete(k)});
}
let state;
try{state=store.load()}catch{state=createPersonalState()}
let currentBook=null;
let currentRoute='館藏';
let currentId=null;
let trailDraft=null;
const titleById=new Map();
const canonicalShape=value=>typeof value==='string'&&(/^(?:OL\d+W|dawn:[\w:-]+)$/.test(value));
const cleanTitle=item=>String(item?.title||item?.work?.title||'').trim();
const context=()=>({
 schema:'dawn.collection-context.v1',
 anchors:[],query:'',semanticIntent:'reader-selected collection',
 relations:[],facets:{},ordering:'reader',
 discoveryDistance:0,cursor:null,
 origin:currentRoute,focusedWork:currentId
});
const save=next=>{state=store.save(next);render();return state};
function message(text){const node=$('#dawn-personal-status');if(node)node.textContent=text}
function button(label,action){
 const el=document.createElement('button');el.type='button';el.textContent=label;
 el.addEventListener('click',action);return el;
}
function section(label,rows,renderRow){
 const wrap=document.createElement('section');wrap.className='dawn-personal__group';
 const head=document.createElement('h3');head.textContent=label+' · '+rows.length;wrap.append(head);
 if(!rows.length)return wrap;
 const grid=document.createElement('div');grid.className='dawn-personal__entries';
 rows.forEach(item=>grid.append(renderRow(item)));
 wrap.append(grid);return wrap;
}
function entry(label,note){
 const card=document.createElement('div');card.className='dawn-personal__entry';
 const title=document.createElement('strong');title.textContent=label;
 card.append(title);
 if(note){const subtitle=document.createElement('small');subtitle.textContent=note;card.append(subtitle)}
 return card;
}
function render(){
 const bookmarks=state.bookmarks||[],views=state.views||[],trails=state.trails||[];
 count.textContent=String(bookmarks.length+views.length+trails.length);
 const hasId=canonicalShape(currentId);
 bookmarkButton.disabled=!hasId;
 bookmarkButton.textContent=!hasId?'此書尚待身份核對':
  bookmarks.some(row=>row.workId===currentId)?'從我的書房移除':'收藏到我的書房';
 personalTrail.textContent=trailDraft?'保存閱讀足跡':'開始記錄閱讀足跡';
 personalTrail.setAttribute('aria-pressed',String(Boolean(trailDraft)));
 shelf.replaceChildren(
  section('我的藏書',bookmarks,row=>{
   const card=entry(row.label||titleById.get(row.workId)||row.workId,row.workId);
   card.append(button('查看',()=>{dialog.close();window.dispatchEvent(new CustomEvent('dawn:p2:resume-book',{detail:{workId:row.workId,label:row.label||''}}))}));
   card.append(button('移除',()=>save(removeBookmark(state,row.workId))));
   return card
  }),
  section('保存的書架',views,row=>entry(row.label||'書架',String(row.savedAt||'').slice(0,10))),
  section('閱讀足跡',trails,row=>entry(row.label||'閱讀足跡',row.steps.length+' 部書'))
 );
}
window.addEventListener('dawn:p2:work-opened',event=>{
 const work=event.detail||{};
 currentBook=work;currentId=String(work.workId||'')||null;
 if(currentId&&cleanTitle(work))titleById.set(currentId,cleanTitle(work));
 if(trailDraft&&canonicalShape(currentId)&&trailDraft.at(-1)?.workId!==currentId){
  trailDraft.push({workId:currentId,context:context(),projection:'card'});
 }
 render();
});
window.addEventListener('dawn:p2:navigation',event=>{
 currentRoute=String(event.detail?.route||'館藏');currentId=null;currentBook=null;render();
});
window.addEventListener('storage',event=>{
 if(event.key==='dawn.personal-state.v1'){
  try{state=store.load();render()}catch{message('無法讀取個人書房記錄')}
 }
});
bookmarkButton.addEventListener('click',()=>{
 if(!canonicalShape(currentId))return;
 const existing=(state.bookmarks||[]).some(row=>row.workId===currentId);
 const next=existing?removeBookmark(state,currentId):saveBookmark(state,{
  workId:currentId,context:context(),projection:'card',label:cleanTitle(currentBook)
 });
 save(next);
 message(existing?'已從個人藏書移除':'已收藏到我的書房');
});
openButton.addEventListener('click',()=>{render();dialog.showModal()});
closeButton.addEventListener('click',()=>dialog.close());
personalView.addEventListener('click',()=>{
 const name=currentRoute||'館藏';
 save(saveView(state,{id:'view:'+Date.now(),context:context(),projection:'shelf',label:name}));
 message('已保存目前書架');
});
personalTrail.addEventListener('click',()=>{
 if(!trailDraft){trailDraft=[];message('開始記錄閱讀足跡');render();return}
 const steps=trailDraft;trailDraft=null;
 if(steps.length)save(saveTrail(state,{id:'trail:'+Date.now(),steps,label:'閱讀足跡'}));
 else render();
 message(steps.length?'閱讀足跡已保存':'尚未選擇可保存的書籍');
});
personalExport.addEventListener('click',()=>{
 const payload=exportPersonalState(state);
 const blob=new Blob([payload],{type:'application/json'});
 const link=document.createElement('a');const url=URL.createObjectURL(blob);
 link.href=url;link.download='dawn-personal-library.json';link.click();
 setTimeout(()=>URL.revokeObjectURL(url),1000);
});
personalImport?.addEventListener('change',async()=>{
 const file=personalImport.files?.[0];if(!file)return;
 try{save(importPersonalState(await file.text()));message('個人書房記錄已匯入')}
 catch{message('匯入失敗：檔案不是有效的個人書房記錄')}
 personalImport.value='';
});
render();
