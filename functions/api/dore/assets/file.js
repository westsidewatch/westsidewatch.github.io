const json=(data,status=200)=>new Response(JSON.stringify(data),{status,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store'}});
const allowed=k=>['one/share/','one/studio/','one/restorations/','one/motion/'].some(p=>k.startsWith(p));
async function resolve(env,request,head=false){
  if(!env.DORE_SENSORY||!env.DORE_ASSETS)return json({ok:false,error:'asset_delivery_unbound'},503);
  const code=(new URL(request.url).searchParams.get('code')||'').trim();
  if(!code)return json({ok:false,error:'asset_code_required'},400);
  try{
    const row=await env.DORE_SENSORY.prepare(`SELECT asset_code,storage_backend,storage_locator,content_hash,media_type,byte_size,lifecycle_state FROM asset_registry WHERE asset_code=?1 AND lifecycle_state!='deleted' LIMIT 1`).bind(code).first();
    if(!row)return json({ok:false,error:'asset_not_found'},404);
    if(row.storage_backend!=='r2'||!allowed(row.storage_locator||''))return json({ok:false,error:'asset_not_publicly_deliverable'},403);
    const obj=await env.DORE_ASSETS.get(row.storage_locator);
    if(!obj)return json({ok:false,error:'r2_object_missing'},404);
    const h=new Headers(); h.set('content-type',row.media_type||obj.httpMetadata?.contentType||'application/octet-stream'); h.set('content-length',String(row.byte_size||obj.size||0)); h.set('cache-control','public, max-age=3600, stale-while-revalidate=86400'); h.set('etag',`"sha256-${row.content_hash}"`); h.set('x-dore-asset-code',row.asset_code); h.set('x-dore-sha256',row.content_hash); h.set('x-content-type-options','nosniff');
    return new Response(head?null:obj.body,{status:200,headers:h});
  }catch(error){return json({ok:false,error:'asset_delivery_failed',detail:String(error?.message||error)},500)}
}
export const onRequestGet=ctx=>resolve(ctx.env,ctx.request,false); export const onRequestHead=ctx=>resolve(ctx.env,ctx.request,true);
