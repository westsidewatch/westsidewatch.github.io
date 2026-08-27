(()=>{
'use strict';
if(window.DoreSearchRuntime?.version)return;

const EVENT='dore:search-query';
const CONVERSATION_KEY='dore.conversation.id.v3';
const $=selector=>document.querySelector(selector);
const uuid=()=>crypto.randomUUID?.()||`${Date.now().toString(36)}-${Math.random().toString(36).slice(2)}`;

function conversationId(){
  let value=sessionStorage.getItem(CONVERSATION_KEY);
  if(!value){value=uuid();sessionStorage.setItem(CONVERSATION_KEY,value)}
  return value;
}

function snapshot(){
  const form=$('#search-form'),input=$('#search-input');
  return{query:input?.value?.trim()||'',form,input,results:$('#results'),count:$('#result-count'),status:$('#search-status'),conversation_id:conversationId(),timestamp:Date.now()};
}

function dispatch(detail){if(detail?.query)window.dispatchEvent(new CustomEvent(EVENT,{detail}))}
function log(){return $('#conversation-log')}
function appendTurn(role,text,meta={}){
  const box=log();if(!box)return null;
  const article=document.createElement('article');
  article.className=`conversation-turn conversation-turn--${role}`;
  article.dataset.turnId=meta.turnId||uuid();
  const header=document.createElement('header');
  const name=document.createElement('strong');name.textContent=role==='user'?'你':'DORÉ';
  const detail=document.createElement('span');detail.textContent=meta.label||'';
  const body=document.createElement('p');body.textContent=text;
  header.append(name,detail);article.append(header,body);box.append(article);
  return article;
}
function updateTurn(article,text,meta={}){
  if(!article)return;
  const body=article.querySelector('p');if(body)body.textContent=text;
  const detail=article.querySelector('header span');if(detail)detail.textContent=meta.label||'';
  article.classList.toggle('conversation-turn--error',Boolean(meta.error));
}
function setBusy(busy){
  const button=$('#chat-button');if(button){button.disabled=busy;button.textContent=busy?'Doré 回應中…':'問 Doré'}
}

async function converse(detail){
  appendTurn('user',detail.query,{label:'Conversation'});
  const pending=appendTurn('assistant','正在思考…',{label:'Cloudflare Workers AI'});
  setBusy(true);
  try{
    const response=await fetch('/api/dore/conversation',{method:'POST',headers:{'content-type':'application/json',accept:'application/json'},body:JSON.stringify({query:detail.query,conversation_id:detail.conversation_id,project_id:'dore-search',actor_id:'public'})});
    const data=await response.json();
    if(!response.ok||!data?.ok)throw new Error(data?.detail||data?.error||`HTTP ${response.status}`);
    if(data?.provider?.name!=='cloudflare-workers-ai')throw new Error('unexpected_ai_provider');
    updateTurn(pending,data.answer,{label:`Workers AI · ${data.provider.model||''}`});
    window.dispatchEvent(new CustomEvent('dore:conversation-response',{detail:data}));
    return data;
  }catch(error){
    updateTurn(pending,'Doré 對話目前不可用；普通搜索不受影響。',{error:true,label:String(error?.message||error)});
    return null;
  }finally{setBusy(false)}
}

function onSubmit(event){
  const form=event.target;if(!(form instanceof HTMLFormElement)||form.id!=='search-form')return;
  const detail=snapshot();if(!detail.query)return;
  // Enter / Search is deliberately search-only: no Workers AI call, no AI tokens/neurons.
  dispatch(detail);
}
function onChat(event){
  const button=event.target.closest?.('#chat-button');if(!button)return;
  event.preventDefault();
  const detail=snapshot();if(!detail.query)return;
  converse(detail);
}
function newConversation(){sessionStorage.removeItem(CONVERSATION_KEY);log()?.replaceChildren();return conversationId()}
function init(){
  if(document.documentElement.dataset.doreRuntimeBound)return;
  document.documentElement.dataset.doreRuntimeBound='1';
  document.addEventListener('submit',onSubmit,true);
  document.addEventListener('click',onChat,true);
}
window.DoreSearchRuntime={version:'4.0.0',event:EVENT,snapshot,dispatch,conversationId,newConversation,converse};
init();
})();
