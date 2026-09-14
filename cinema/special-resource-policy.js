(()=>{
  const ids=new Set(['cinema:video:goodtv:holy-spirit-power-workplace-testimony']);
  const api=Object.freeze({
    schema:'dore.cinema-special-resource-policy.v0',
    has(canonicalId){return ids.has(canonicalId);},
    filter(items){return Array.isArray(items)?items.filter(item=>!ids.has(item?.canonicalId)):[];},
    ids:Object.freeze([...ids])
  });
  window.ParadiseCinemaSpecialResources=api;

  const nativeFetch=window.fetch.bind(window);
  window.fetch=async function(input,init){
    const response=await nativeFetch(input,init);
    let url='';
    try{url=new URL(typeof input==='string'?input:input.url,location.href).pathname;}catch(_error){return response;}
    const isCinemaCatalog=url.endsWith('/cinema/data/video-resource.v0.json')||url.endsWith('/cinema/data/bible-media-coordinate.v0.json');
    if(!isCinemaCatalog||!response.ok)return response;
    try{
      const payload=await response.clone().json();
      if(!Array.isArray(payload.items))return response;
      payload.items=api.filter(payload.items);
      return new Response(JSON.stringify(payload),{status:response.status,statusText:response.statusText,headers:response.headers});
    }catch(_error){return response;}
  };
})();
