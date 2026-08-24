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
function onSubmit(){
  const detail=snapshot();
  if(!detail.query)return;
  setTimeout(()=>dispatch(detail),0);
}
function init(){
  const form=$('#search-form');
  if(!form||form.dataset.doreRuntimeBound)return;
  form.dataset.doreRuntimeBound='1';
  form.addEventListener('submit',onSubmit,false);
}
window.DoreSearchRuntime={version:'1.0.0',event:EVENT,snapshot,dispatch};
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();
