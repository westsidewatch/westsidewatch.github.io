(()=>{
'use strict';
if(window.DoreSearchRuntime?.version)return;
const CONVERSATION_KEY='dore.conversation.id.v5';
const MODE_KEY='dore.ai.mode.v1';
const LOCAL_HEALTH='http://127.0.0.1:8788/health';
const LOCAL_CHAT='http://127.0.0.1:8788/chat';
const CONVERSATION_API='https://westsidewatch-github-io.pages.dev/api/dore/conversation';
const SEARCH_SURFACE='dore-search-ui';
const PROJECT_ID='dore-search';
const $=s=>document.querySelector(s);
const uuid=()=>crypto.randomUUID?.()||`${Date.now().toString(36)}-${Math.random().toString(36).slice(2)}`;
function conversationId(){let v=sessionStorage.getItem(CONVERSATION_KEY);if(!v){v=uuid();sessionStorage.setItem(CONVERSATION_KEY,v)}return v}
function snapshot(){const input=$('#search-input');return{query:input?.value?.trim()||'',input,results:$('#results'),count:$('#result-count'),conversation_id:conversationId()}}
function aiMode(){return sessionStorage.getItem(MODE_KEY)==='on'}
function setAiMode(on){if(on)sessionStorage.setItem(MODE_KEY,'on');else sessionStorage.removeItem(MODE_KEY);window.dispatchEvent(new CustomEvent('dore:ai-mode',{detail:{enabled:!!on}}));return !!on}
function isOpenCommand(v=''){return /^[問问]多雷[!！。.?？\s]*$/i.test(String(v).trim())}
function isCloseCommand(v=''){return /^搜索[!！。.?？\s]*$/i.test(String(v).trim())}
function providerLabel(provider){const name=provider?.name||'';if(name==='dore-local')return 'Conversation · Local';if(name==='cloudflare-workers-ai')return 'Conversation · Workers AI';return 'Conversation'}
function renderConversation(user,answer,error='',provider=null){
 const box=$('#results'),count=$('#result-count');if(!box)return;
 const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot',"'":'&#39;'}[c]));
 box.innerHTML=`<article class="result-card"><header><strong>DORÉ</strong><span>${esc(providerLabel(provider))}</span></header><p>${esc(answer||'Doré 對話目前不可用。')}</p><footer><span>${esc(user)}</span><span>${esc(error)}</span></footer></article>`;
 if(count)count.textContent=error?'對話失敗':'Doré 回應';
 $('#results-wrap')?.scrollIntoView({behavior:'smooth',block:'start'});
}
function renderMode(message){const box=$('#results'),count=$('#result-count');if(box)box.innerHTML=`<article class="result-card"><header><strong>DORÉ</strong></header><p>${message}</p></article>`;if(count)count.textContent=message}
async function localReady(timeoutMs=1200){
 const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),timeoutMs);
 try{const r=await fetch(LOCAL_HEALTH,{cache:'no-store',signal:controller.signal});if(!r.ok)return false;const d=await r.json();return d?.ok===true&&d?.node==='dore-local'}catch{return false}finally{clearTimeout(timer)}
}
async function converseLocal(detail){
 if(!(await localReady()))return null;
 try{
  const r=await fetch(LOCAL_CHAT,{method:'POST',headers:{'content-type':'application/json',accept:'application/json'},body:JSON.stringify({message:detail.query,conversation_id:detail.conversation_id,project_id:PROJECT_ID})});
  const type=r.headers.get('content-type')||'';if(!type.includes('application/json'))throw new Error(`local endpoint returned ${r.status} ${type||'non-JSON'}`);
  const d=await r.json();if(!r.ok||!d?.ok)throw new Error(d?.detail||d?.error||`HTTP ${r.status}`);
  return {...d,provider:d.provider||{name:'dore-local',model:d.model||'local'},routing:{primary:'local',used:'local',fallback_used:false},workers_ai_used:false};
 }catch{return null}
}
async function converseCloud(detail,localAttempted=true){
 const r=await fetch(CONVERSATION_API,{method:'POST',headers:{'content-type':'application/json',accept:'application/json'},body:JSON.stringify({query:detail.query,conversation_id:detail.conversation_id,project_id:PROJECT_ID,actor_id:'public',surface:SEARCH_SURFACE})});
 const type=r.headers.get('content-type')||'';if(!type.includes('application/json'))throw new Error(`conversation endpoint returned ${r.status} ${type||'non-JSON'}`);
 const d=await r.json();if(!r.ok||!d?.ok)throw new Error(d?.detail||d?.error||`HTTP ${r.status}`);if(d?.provider?.name!=='cloudflare-workers-ai')throw new Error('unexpected_ai_provider');
 return {...d,routing:{primary:'local',used:'cloud',fallback_used:!!localAttempted}};
}
async function converse(detail){
 const q=detail.query;renderConversation(q,'Doré 回應中…');
 try{
  let d=await converseLocal(detail);
  if(!d)d=await converseCloud(detail,true);
  renderConversation(q,d.answer||'','',d.provider);window.dispatchEvent(new CustomEvent('dore:conversation-response',{detail:d}));return d;
 }catch(e){renderConversation(q,'Doré 對話目前不可用。',String(e?.message||e));return null}
}
function onSubmit(event){
 const form=event.target;if(!(form instanceof HTMLFormElement)||form.id!=='search-form')return;
 const snap=snapshot(),raw=snap.query;
 if(isOpenCommand(raw)){event.preventDefault();event.stopImmediatePropagation();setAiMode(true);renderMode('多雷 AI 對話已開啟。輸入「搜索」可返回普通搜索。');if(snap.input)snap.input.value='';return}
 if(aiMode()){
  if(isCloseCommand(raw)){event.preventDefault();event.stopImmediatePropagation();setAiMode(false);renderMode('已返回普通搜索。');if(snap.input)snap.input.value='';return}
  if(!raw)return;event.preventDefault();event.stopImmediatePropagation();converse({...snap,query:raw});return
 }
}
function newConversation(){sessionStorage.removeItem(CONVERSATION_KEY);return conversationId()}
function init(){if(document.documentElement.dataset.doreConversationBound)return;document.documentElement.dataset.doreConversationBound='1';sessionStorage.removeItem(MODE_KEY);window.addEventListener('submit',onSubmit,true)}
window.DoreSearchRuntime={version:'6.1.0',snapshot,conversationId,newConversation,converse,aiMode,setAiMode,isOpenCommand,isCloseCommand,localReady};
init();
})();
