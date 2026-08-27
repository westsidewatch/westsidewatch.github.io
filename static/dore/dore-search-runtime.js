(()=>{
'use strict';
if(window.DoreSearchRuntime?.version)return;

const EVENT='dore:search-query';
const CONVERSATION_KEY='dore.conversation.id.v2';
const RESPONSE_KEY='dore.openai.response.id.v1';
const $=selector=>document.querySelector(selector);
const uuid=()=>crypto.randomUUID?.()||`${Date.now().toString(36)}-${Math.random().toString(36).slice(2)}`;

function conversationId(){
  let value=sessionStorage.getItem(CONVERSATION_KEY);
  if(!value){value=uuid();sessionStorage.setItem(CONVERSATION_KEY,value)}
  return value;
}

function responseKey(){return `${RESPONSE_KEY}.${conversationId()}`}
function previousResponseId(){return sessionStorage.getItem(responseKey())||''}
function rememberResponseId(value){if(/^resp_[A-Za-z0-9_-]+$/.test(value||''))sessionStorage.setItem(responseKey(),value)}

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
  if(meta.provider)article.dataset.provider=meta.provider;
  const header=document.createElement('header');
  const name=document.createElement('strong');name.textContent=role==='user'?'你':'DORÉ · ChatGPT';
  const detail=document.createElement('span');detail.textContent=meta.label||'';
  const body=document.createElement('p');body.textContent=text;
  header.append(name,detail);article.append(header,body);box.append(article);
  $('#conversation-wrap')?.scrollIntoView({behavior:'smooth',block:'start'});
  return article;
}

function updateTurn(article,text,meta={}){
  if(!article)return;
  const body=article.querySelector('p');if(body)body.textContent=text;
  const detail=article.querySelector('header span');if(detail)detail.textContent=meta.label||'';
  article.classList.toggle('conversation-turn--error',Boolean(meta.error));
  if(meta.provider)article.dataset.provider=meta.provider;
}

function setBusy(busy){
  const button=$('#search-button');
  if(button){button.disabled=busy;button.textContent=busy?'ChatGPT 回應中…':'發送'}
}

async function remember(detail){
  const pending=appendTurn('assistant','正在連接 ChatGPT…',{label:'OpenAI Responses API'});
  setBusy(true);
  try{
    const response=await fetch('/api/dore/conversation',{
      method:'POST',
      headers:{'content-type':'application/json',accept:'application/json'},
      body:JSON.stringify({query:detail.query,conversation_id:detail.conversation_id,previous_response_id:previousResponseId(),project_id:'dore-search',actor_id:'public'})
    });
    const data=await response.json();
    if(!response.ok||!data?.ok)throw new Error(data?.detail||data?.error||`HTTP ${response.status}`);
    if(data?.provider?.name!=='openai'||data?.provider?.api!=='responses')throw new Error('response_provider_is_not_openai');
    rememberResponseId(data.provider.response_id);
    updateTurn(pending,data.answer,{provider:'openai',label:`ChatGPT · ${data.provider.model||'OpenAI'}`});
    window.dispatchEvent(new CustomEvent('dore:conversation-response',{detail:data}));
    return data;
  }catch(error){
    updateTurn(pending,'ChatGPT 連接失敗；這句話仍由 Doré 保存，但沒有偽裝成其他模型的回答。',{error:true,label:String(error?.message||error)});
    console.error('Doré → ChatGPT bridge failed',error);
    return null;
  }finally{
    setBusy(false);
  }
}

function onSubmit(event){
  const form=event.target;
  if(!(form instanceof HTMLFormElement)||form.id!=='search-form')return;
  const detail=snapshot();if(!detail.query)return;
  appendTurn('user',detail.query,{label:'經 Doré 傳送'});
  setTimeout(()=>{dispatch(detail);remember(detail)},0);
}

function newConversation(){
  const oldKey=responseKey();
  sessionStorage.removeItem(oldKey);
  sessionStorage.removeItem(CONVERSATION_KEY);
  log()?.replaceChildren();
  return conversationId();
}

function init(){
  if(document.documentElement.dataset.doreRuntimeBound)return;
  document.documentElement.dataset.doreRuntimeBound='1';
  document.addEventListener('submit',onSubmit,true);
}

window.DoreSearchRuntime={version:'3.0.0',event:EVENT,snapshot,dispatch,conversationId,newConversation,remember,previousResponseId};
init();
})();
