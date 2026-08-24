const J=(d,s=200)=>new Response(JSON.stringify(d),{status:s,headers:{'content-type':'application/json','cache-control':'no-store'}});
async function serve({request,env},head=false){
 if(!env.DORE_SENSORY||!env.DORE_ASSETS)return J({ok:false,error:'asset_delivery_unbound'},503);
 const code=(new URL(request.url).searchParams.get('code')||'').trim(); if(!code)return J({ok:false,error:'asset_code_required'},400);
 try{const row=await env.DORE_SENSORY.prepare(`SELECT asset_code,storage_backend,storage_locator,content_hash,media_type,byte_size FROM asset_registry WHERE asset_code=?1 AND lifecycle_state!='deleted' LIMIT 1`).bind(code).first();
 if(!row)return J({ok:false,error:'asset_not_found'},404); if(row.storage_backend!=='r2'||!String(row.storage_locator||'').startsWith('site/'))return J({ok:false,error:'asset_not_site_deliverable'},403);
 const o=await env.DORE_ASSETS.get(row.storage_locator); if(!o)return J({ok:false,error:'r2_object_missing'},404);
 const h=new Headers({'content-type':row.media_type||o.httpMetadata?.contentType||'application/octet-stream','cache-control':'public, max-age=3600, stale-while-revalidate=86400','etag':`"sha256-${row.content_hash}"`,'x-dore-asset-code':row.asset_code,'x-dore-sha256':row.content_hash,'x-content-type-options':'nosniff'}); return new Response(head?null:o.body,{status:200,headers:h});
 }catch(e){return J({ok:false,error:'asset_delivery_failed',detail:String(e.message||e)},500)}}
export const onRequestGet=c=>serve(c,false); export const onRequestHead=c=>serve(c,true);