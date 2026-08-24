const response=(data,status=200)=>new Response(typeof data==='string'?data:JSON.stringify(data),{status,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store'}});

export async function onRequestGet({request,env}){
  const assetUrl=new URL('/dore/brain/knowledge-index.json',request.url);
  try{
    let asset=null;
    if(env?.ASSETS?.fetch){
      asset=await env.ASSETS.fetch(new Request(assetUrl.toString(),{headers:{accept:'application/json'}}));
    }else{
      asset=await fetch(assetUrl.toString(),{headers:{accept:'application/json','cache-control':'no-cache'}});
    }
    if(!asset?.ok)return response({ok:false,error:'brain_index_unavailable',status:asset?.status||0},503);
    const text=await asset.text();
    const brain=JSON.parse(text);
    return response(brain,200);
  }catch(error){
    return response({ok:false,error:'brain_load_failed',detail:String(error?.message||error)},500);
  }
}
