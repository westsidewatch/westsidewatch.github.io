(()=>{
'use strict';
if(window.DoreSearchRuntime?.version)return;
const EVENT='dore:search-query',KEY='dore.conversation.id.v1';
const $=s=>document.querySelector(s);
const id=()=>{let v=sessionStorage.getItem(KEY);if(!v){v=crypto.randomUUID?.()||`${Date.now().toString(36)}-${Math.random().toString(36).slice(2)}`;sessionStorage.setItem(KEY,v)}return v};
function snapshot(){const form=$('#search-form'),input=$('#search-input');return{query:input?.value?.trim()||'',form,input,results:$('#results'),count:$('#result-count'),status:$('#search-status'),conversation_id:id(),timestamp:Date.now()}}
function dispatch(detail){if(detail?.query)window.dispatchEvent(new CustomEvent(EVENT,{detail}))}
async function remember(detail){try{const r=await fetch('/api/dore/conversation',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({query:detail.query,conversation_id:detail.conversation_id,project_id:'dore-search',actor_id:'public'})});const data=await r.json();window.dispatchEvent(new CustomEvent('dore:conversation-response',{detail:data}));return data}catch(error){console.error('Doré conversation persistence failed',error);return null}}
function onSubmit(event){const form=event.target;if(!(form instanceof HTMLFormElement)||form.id!=='search-form')return;const detail=snapshot();if(!detail.query)return;setTimeout(()=>{dispatch(detail);remember(detail)},0)}
function newConversation(){sessionStorage.removeItem(KEY);return id()}
function init(){if(document.documentElement.dataset.doreRuntimeBound)return;document.documentElement.dataset.doreRuntimeBound='1';document.addEventListener('submit',onSubmit,true)}
window.DoreSearchRuntime={version:'2.0.0',event:EVENT,snapshot,dispatch,conversationId:id,newConversation,remember};init();
})();
