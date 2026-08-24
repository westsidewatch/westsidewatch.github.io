const json=(data,status=200)=>new Response(JSON.stringify(data),{status,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store'}});

export async function onRequestGet({request,env}){
  if(!env.DORE_SENSORY)return json({ok:false,error:'asset_registry_unbound'},503);
  const url=new URL(request.url);
  const q=(url.searchParams.get('q')||'').trim();
  if(!q)return json({ok:true,query:'',results:[]});
  try{
    const info=await env.DORE_SENSORY.prepare('PRAGMA table_info(asset_registry)').all();
    const cols=new Set((info?.results||[]).map(r=>r.name));
    if(!cols.size)return json({ok:true,query:q,results:[]});
    const select=['id','storage_backend','storage_locator','content_hash','media_type','byte_size','preservation_class','lifecycle_state'];
    for(const c of ['asset_code','title','description','alt_text','scripture_refs_json','products_using_it_json','social_uses_json','liming_resource_ids_json','review_status'])if(cols.has(c))select.push(c);
    const searchable=[];
    for(const c of ['asset_code','title','description','alt_text','storage_locator','scripture_refs_json','products_using_it_json','social_uses_json','liming_resource_ids_json'])if(cols.has(c))searchable.push(c);
    if(!searchable.length)return json({ok:true,query:q,results:[]});
    const where=searchable.map(c=>`${c} LIKE ?1`).join(' OR ');
    const rows=await env.DORE_SENSORY.prepare(`SELECT ${select.join(',')} FROM asset_registry WHERE (${where}) AND lifecycle_state!='deleted' ORDER BY CASE WHEN ${cols.has('review_status')?'review_status':'lifecycle_state'}='approved' THEN 0 ELSE 1 END, updated_at DESC LIMIT 24`).bind(`%${q}%`).all();
    return json({ok:true,query:q,count:(rows?.results||[]).length,results:rows?.results||[]});
  }catch(error){
    if(String(error?.message||'').includes('no such table'))return json({ok:true,query:q,results:[]});
    return json({ok:false,error:'asset_search_failed',detail:String(error?.message||error)},500);
  }
}
