(()=>{
'use strict';
if(window.DoreSearchRuntime?.version)return;
const EVENT='dore:search-query';
const $=s=>document.querySelector(s);
function snapshot(){
  const form=$('#search-form'),input=$('#search-input');
  return{
    query:input?.value?.trim()||'',
    form,
    input,
    results:$('#results'),
    count:$('#result-count'),
    status:$('#search-status'),
    timestamp:Date.now()
  };
}
function dispatch(detail){
  if(!detail?.query)return;
  window.dispatchEvent(new CustomEvent(EVENT,{detail}));
}
function onSubmit(event){
  const form=event.target;
  if(!(form instanceof HTMLFormElement)||form.id!=='search-form')return;
  const detail=snapshot();
  if(!detail.query)return;
  setTimeout(()=>dispatch(detail),0);
}
function init(){
  if(document.documentElement.dataset.doreRuntimeBound)return;
  document.documentElement.dataset.doreRuntimeBound='1';
  document.addEventListener('submit',onSubmit,true);
}
window.DoreSearchRuntime={version:'1.1.0',event:EVENT,snapshot,dispatch};
init();
})();
