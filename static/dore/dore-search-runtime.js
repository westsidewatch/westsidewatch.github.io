(()=>{
'use strict';
if(window.DoreSearchRuntime?.version)return;
const CONVERSATION_KEY='dore.conversation.id.v4';
const CONVERSATION_API='https://westsidewatch-github-io.pages.dev/api/dore/conversation';
const $=s=>document.querySelector(s);
const uuid=()=>crypto.randomUUID?.()||`${Date.now().toString(36)}-${Math.random().toString(36).slice(2)}`;
function conversationId(){let v=sessionStorage.getItem(CONVERSATION_KEY);if(!v){v=uuid();sessionStorage.setItem(CONVERSATION_KEY,v)}return v}
function snapshot(){const input=$('#search-input');return{query:input?.value?.trim()||'',input,results:$('#results'),count:$('#result-count'),conversation_id:conversationId()}}
function parseConversationQuery(value=''){const m=String(value).trim().match(/^(?:多雷|dor[eé])\s*[,，:：]?\s*(.+)$/i);return m?.[1]?.trim()||''}
function renderConversation(user,answer,error=''){
 const box=$('#results'),count=$('#result-count');if(!box)return;
 const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 box.innerHTML=`<article class="result-card"><header><strong>DORÉ</strong><span>Conversation · Workers AI</span></header><p>${esc(answer||'Doré 對話目前不可用。')}</p><footer><span>${esc(user)}</span><span>${esc(error)}</span></footer></article>`;
 if(count)count.textContent=error?'對話失敗':'Doré 回應';
 $('#results-wrap')?.scrollIntoView({behavior:'smooth',block:'start'});
}
async function converse(detail){
 const q=detail.query;
 renderConversation(q,'Doré 回應中…');
 try{
  const r=await fetch(CONVERSATION_API,{method:'POST',headers:{'content-type':'application/json',accept:'application/json'},body:JSON.stringify({query:q,conversation_id:detail.conversation_id,project_id:'dore-search',actor_id:'public'})});
  const type=r.headers.get('content-type')||'';
  if(!type.includes('application/json'))throw new Error(`conversation endpoint returned ${r.status} ${type||'non-JSON'}`);
  const d=await r.json();
  if(!r.ok||!d?.ok)throw new Error(d?.detail||d?.error||`HTTP ${r.status}`);
  if(d?.provider?.name!=='cloudflare-workers-ai')throw new Error('unexpected_ai_provider');
  renderConversation(q,d.answer||'');
  window.dispatchEvent(new CustomEvent('dore:conversation-response',{detail:d}));
  return d;
 }catch(e){renderConversation(q,'Doré 對話目前不可用。',String(e?.message||e));return null}
}
function onSubmit(event){
 const form=event.target;if(!(form instanceof HTMLFormElement)||form.id!=='search-form')return;
 const snap=snapshot(),q=parseConversationQuery(snap.query);if(!q)return;
 event.preventDefault();event.stopImmediatePropagation();
 converse({...snap,query:q});
}
function newConversation(){sessionStorage.removeItem(CONVERSATION_KEY);return conversationId()}
function init(){if(document.documentElement.dataset.doreConversationBound)return;document.documentElement.dataset.doreConversationBound='1';document.addEventListener('submit',onSubmit,true)}
window.DoreSearchRuntime={version:'4.2.0',snapshot,conversationId,newConversation,converse,parseConversationQuery};
init();
})();
