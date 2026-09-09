/* DORÉ site capability bridge: Westside Watch products -> Native Messaging -> DORÉ Core. */
const SITE_CAPABILITY='context.fuzzy-search';
function safeDetail(value){
  if(typeof cloneInto==='function')return cloneInto(value,window);
  return value;
}
function emitResult(requestId,payload){
  window.dispatchEvent(new CustomEvent('dore:context-fuzzy-search-result',{detail:safeDetail({request_id:requestId,payload})}));
}
window.addEventListener('dore:context-fuzzy-search',async event=>{
  const detail=event.detail||{};
  if(detail.capability!==SITE_CAPABILITY||!detail.request_id)return;
  const context=detail.context&&typeof detail.context==='object'?detail.context:{};
  const args={query:String(detail.query||''),host:String(context.host||''),mode:String(context.mode||'prepare'),embedded:Boolean(context.embedded),explicit_search:context.lane==='explicit',limit:5};
  try{
    const reply=await browser.runtime.sendMessage({type:'dore.site-capability',capability:SITE_CAPABILITY,args,caller_product:String(context.host||'site')});
    const result=reply&&reply.result?reply.result:{ok:false,status:'failed',error:{code:'bridge_failed',message:String(reply&&reply.error||'site capability bridge failed')}};
    emitResult(detail.request_id,result);
  }catch(error){
    emitResult(detail.request_id,{ok:false,status:'failed',error:{code:'bridge_transport_error',message:String(error&&error.message||error)}});
  }
});
