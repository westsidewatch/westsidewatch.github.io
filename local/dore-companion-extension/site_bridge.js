/* DORÉ site capability bridge: Westside Watch products -> Native Messaging -> DORÉ Core. */
const FUZZY_CAPABILITY='context.fuzzy-search';
const BOOK_CAPABILITY='publishing.book-intelligence';
function safeDetail(value){
  if(typeof cloneInto==='function')return cloneInto(value,window);
  return value;
}
function emit(name,requestId,payload){
  window.dispatchEvent(new CustomEvent(name,{detail:safeDetail({request_id:requestId,payload})}));
}
async function send(capability,args,callerProduct){
  const reply=await browser.runtime.sendMessage({type:'dore.site-capability',capability,args,caller_product:callerProduct});
  return reply&&reply.result?reply.result:{ok:false,status:'failed',error:{code:'bridge_failed',message:String(reply&&reply.error||'site capability bridge failed')}};
}
window.addEventListener('dore:context-fuzzy-search',async event=>{
  const detail=event.detail||{};
  if(detail.capability!==FUZZY_CAPABILITY||!detail.request_id)return;
  const context=detail.context&&typeof detail.context==='object'?detail.context:{};
  const args={query:String(detail.query||''),host:String(context.host||''),mode:String(context.mode||'prepare'),embedded:Boolean(context.embedded),explicit_search:context.lane==='explicit',limit:5};
  try{emit('dore:context-fuzzy-search-result',detail.request_id,await send(FUZZY_CAPABILITY,args,String(context.host||'site')))}catch(error){emit('dore:context-fuzzy-search-result',detail.request_id,{ok:false,status:'failed',error:{code:'bridge_transport_error',message:String(error&&error.message||error)}})}
});
window.addEventListener('dore:book-intelligence',async event=>{
  const detail=event.detail||{};
  if(detail.capability!==BOOK_CAPABILITY||!detail.request_id)return;
  const args=detail.args&&typeof detail.args==='object'?detail.args:{};
  try{emit('dore:book-intelligence-result',detail.request_id,await send(BOOK_CAPABILITY,args,'multiwrite'))}catch(error){emit('dore:book-intelligence-result',detail.request_id,{ok:false,status:'failed',error:{code:'bridge_transport_error',message:String(error&&error.message||error)}})}
});
