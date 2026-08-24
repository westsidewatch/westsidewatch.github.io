const J=(d,s=200)=>new Response(JSON.stringify(d),{status:s,headers:{'content-type':'application/json','cache-control':'no-store'}});
const okAuth=(r,e)=>(r.headers.get('authorization')||'')===`Bearer ${e.DORE_HEARTBEAT_TOKEN}`;
const hex=b=>[...new Uint8Array(b)].map(x=>x.toString(16).padStart(2,'0')).join('');
const sha=async b=>hex(await crypto.subtle.digest('SHA-256',b));
const MAP={
 'background.jpg':'site/api/dore/assets/site-file?code=SITE-BACKGROUND',
 'static/api/dore/assets/site-file?code=SITE-DAMASCUS-GATE':'site/damascus-gate.jpg',
 'static/api/dore/assets/site-file?code=SITE-JERUSALEM-WALL':'site/jerusalem-wall.png',
 'static/api/dore/assets/site-file?code=SITE-TEMPLE-STONE-LIGHT':'site/temple-stone-light.png',
 'static/api/dore/assets/site-file?code=SITE-WECHAT-QR':'site/api/dore/assets/site-file?code=SITE-WECHAT-QR'
};
export async function onRequestPost({request,env}){
 if(!env.DORE_HEARTBEAT_TOKEN||!okAuth(request,env))return J({ok:false,error:'unauthorized'},401);
 if(!env.DORE_SENSORY||!env.DORE_ASSETS)return J({ok:false,error:'required_binding_unbound'},503);
 let b;try{b=await request.json()}catch{return J({ok:false,error:'invalid_json'},400)}
 const p=String(b.source_path||'').replace(/^\/+/,''), key=MAP[p], code=String(b.asset_code||'');
 if(!key||!code)return J({ok:false,error:'site_source_not_allowed'},400);
 const u=`https://raw.githubusercontent.com/westsidewatch/westsidewatch.github.io/main/${p}`;
 const r=await fetch(u,{headers:{'user-agent':'dore-site-migrator/1.0'}}); if(!r.ok)return J({ok:false,error:'github_source_fetch_failed',status:r.status},502);
 const bytes=await r.arrayBuffer(), h=await sha(bytes), type=r.headers.get('content-type')||'application/octet-stream';
 const dupe=await env.DORE_SENSORY.prepare('SELECT id,asset_code,storage_locator FROM asset_registry WHERE content_hash=?1 LIMIT 1').bind(h).first();
 if(dupe)return J({ok:true,action:'dedupe_no_copy',sha256:h,existing:dupe});
 const old=await env.DORE_ASSETS.get(key); if(old&&await sha(await old.arrayBuffer())!==h)return J({ok:false,error:'r2_target_collision'},409);
 if(!old)await env.DORE_ASSETS.put(key,bytes,{httpMetadata:{contentType:type},customMetadata:{sha256:h,source_path:p,migrated_by:'dore'}});
 const id=crypto.randomUUID(), now=new Date().toISOString();
 try{await env.DORE_SENSORY.prepare(`INSERT INTO asset_registry (id,asset_code,storage_backend,storage_locator,content_hash,media_type,byte_size,title,source_name,source_url,provenance,generated_by,preservation_class,lifecycle_state,products_using_it_json,review_status,created_at,updated_at) VALUES (?1,?2,'r2',?3,?4,?5,?6,?7,'GitHub',?8,?9,'dore','working','active',?10,'pending',?11,?11)`).bind(id,code,key,h,type,bytes.byteLength,b.title||code,u,`Migrated from GitHub:${p}`,JSON.stringify(b.products_using_it||['SITE']),now).run()}catch(e){if(!old)await env.DORE_ASSETS.delete(key);return J({ok:false,error:'registry_write_failed',detail:String(e.message||e)},500)}
 const v=await env.DORE_ASSETS.get(key), row=await env.DORE_SENSORY.prepare('SELECT content_hash,storage_locator FROM asset_registry WHERE id=?1').bind(id).first();
 const pass=!!v&&await sha(await v.arrayBuffer())===h&&row?.content_hash===h&&row?.storage_locator===key;
 return J({ok:pass,action:old?'registered_existing_r2':'migrated_github_to_r2',asset_code:code,target_key:key,sha256:h,bytes:bytes.byteLength,registry_verified:pass},pass?200:500);
}