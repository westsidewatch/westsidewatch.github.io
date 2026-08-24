const json=(data,status=200)=>new Response(JSON.stringify(data),{status,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store'}});
const authorized=(request,env)=>{const h=request.headers.get('authorization')||'';return Boolean(env.DORE_HEARTBEAT_TOKEN)&&h===`Bearer ${env.DORE_HEARTBEAT_TOKEN}`};
const hex=bytes=>[...new Uint8Array(bytes)].map(b=>b.toString(16).padStart(2,'0')).join('');
const sha256=async bytes=>hex(await crypto.subtle.digest('SHA-256',bytes));
const id=()=>crypto.randomUUID();
const ALLOWED_PREFIXES=['static/one/share/','static/one/studio/','static/one/dore-restorations/','static/one/motion-assets/'];
const TARGET_PREFIX={
  'static/one/share/':'one/share/',
  'static/one/studio/':'one/studio/',
  'static/one/dore-restorations/':'one/restorations/',
  'static/one/motion-assets/':'one/motion/'
};

async function ensureRegistry(db){
  await db.prepare(`CREATE TABLE IF NOT EXISTS asset_registry (
    id TEXT PRIMARY KEY, storage_backend TEXT NOT NULL, storage_locator TEXT NOT NULL UNIQUE,
    content_hash TEXT NOT NULL, media_type TEXT NOT NULL, byte_size INTEGER NOT NULL,
    preservation_class TEXT NOT NULL DEFAULT 'working', lifecycle_state TEXT NOT NULL DEFAULT 'active',
    created_at TEXT NOT NULL, updated_at TEXT NOT NULL
  )`).run();
  const info=await db.prepare('PRAGMA table_info(asset_registry)').all();
  const cols=new Set((info?.results||[]).map(r=>r.name));
  const additions=[
    ['asset_code','TEXT'],['title','TEXT'],['description','TEXT'],['alt_text','TEXT'],['creator','TEXT'],
    ['source_name','TEXT'],['source_url','TEXT'],['provenance','TEXT'],['copyright_status','TEXT'],['license','TEXT'],['generated_by','TEXT'],
    ['scripture_refs_json',"TEXT NOT NULL DEFAULT '[]'"],['people_json',"TEXT NOT NULL DEFAULT '[]'"],['places_json',"TEXT NOT NULL DEFAULT '[]'"],
    ['topics_json',"TEXT NOT NULL DEFAULT '[]'"],['products_using_it_json',"TEXT NOT NULL DEFAULT '[]'"],['journal_columns_json',"TEXT NOT NULL DEFAULT '[]'"],
    ['social_uses_json',"TEXT NOT NULL DEFAULT '[]'"],['liming_resource_ids_json',"TEXT NOT NULL DEFAULT '[]'"],
    ['supersedes_asset_id','TEXT'],['superseded_by_asset_id','TEXT'],['first_used_at','TEXT'],['last_used_at','TEXT'],
    ['use_count','INTEGER NOT NULL DEFAULT 0'],['review_status',"TEXT NOT NULL DEFAULT 'pending'"],['reviewed_at','TEXT']
  ];
  for(const [name,type] of additions)if(!cols.has(name))await db.prepare(`ALTER TABLE asset_registry ADD COLUMN ${name} ${type}`).run();
  await db.prepare('CREATE UNIQUE INDEX IF NOT EXISTS idx_asset_registry_asset_code ON asset_registry(asset_code)').run();
  await db.prepare('CREATE INDEX IF NOT EXISTS idx_asset_registry_hash ON asset_registry(content_hash)').run();
}

function mapTarget(path){
  const prefix=ALLOWED_PREFIXES.find(p=>path.startsWith(p));
  return prefix?TARGET_PREFIX[prefix]+path.slice(prefix.length):null;
}

export async function onRequestPost({request,env}){
  if(!authorized(request,env))return json({ok:false,error:'unauthorized'},401);
  if(!env.DORE_SENSORY||!env.DORE_ASSETS)return json({ok:false,error:'required_binding_unbound'},503);
  let body;try{body=await request.json()}catch{return json({ok:false,error:'invalid_json'},400)}
  const sourcePath=String(body?.source_path||'').replace(/^\/+/, '');
  const targetKey=mapTarget(sourcePath);
  if(!targetKey)return json({ok:false,error:'source_path_not_allowed'},400);
  const preservation=['permanent','working','regenerable','temporary'].includes(body?.preservation_class)?body.preservation_class:'working';
  const assetCode=body?.asset_code?String(body.asset_code):null;
  const sourceUrl=`https://raw.githubusercontent.com/westsidewatch/westsidewatch.github.io/main/${sourcePath}`;
  const response=await fetch(sourceUrl,{headers:{'user-agent':'dore-asset-migrator/1.0'}});
  if(!response.ok)return json({ok:false,error:'github_source_fetch_failed',status:response.status,source_path:sourcePath},502);
  const bytes=await response.arrayBuffer();
  const hash=await sha256(bytes);
  const mediaType=response.headers.get('content-type')||'application/octet-stream';
  await ensureRegistry(env.DORE_SENSORY);
  const duplicate=await env.DORE_SENSORY.prepare('SELECT id,asset_code,storage_backend,storage_locator,lifecycle_state FROM asset_registry WHERE content_hash=?1 LIMIT 1').bind(hash).first();
  if(duplicate)return json({ok:true,action:'dedupe_no_copy',source_path:sourcePath,sha256:hash,existing:duplicate});
  const existingObj=await env.DORE_ASSETS.get(targetKey);
  if(existingObj){
    const existingHash=await sha256(await existingObj.arrayBuffer());
    if(existingHash!==hash)return json({ok:false,error:'r2_target_collision',target_key:targetKey,source_sha256:hash,r2_sha256:existingHash},409);
  }else{
    await env.DORE_ASSETS.put(targetKey,bytes,{httpMetadata:{contentType:mediaType},customMetadata:{sha256:hash,source:'github',source_path:sourcePath,migrated_by:'dore'}});
  }
  const assetId=id(); const now=new Date().toISOString();
  try{
    await env.DORE_SENSORY.prepare(`INSERT INTO asset_registry
      (id,asset_code,storage_backend,storage_locator,content_hash,media_type,byte_size,title,description,alt_text,creator,source_name,source_url,provenance,copyright_status,license,generated_by,preservation_class,lifecycle_state,scripture_refs_json,products_using_it_json,social_uses_json,review_status,created_at,updated_at)
      VALUES (?1,?2,'r2',?3,?4,?5,?6,?7,?8,?9,?10,'GitHub',?11,?12,?13,?14,?15,?16,'active',?17,?18,?19,'pending',?20,?20)`)
      .bind(assetId,assetCode,targetKey,hash,mediaType,bytes.byteLength,body?.title||null,body?.description||null,body?.alt_text||null,body?.creator||null,sourceUrl,body?.provenance||`Migrated from GitHub:${sourcePath}`,body?.copyright_status||null,body?.license||null,body?.generated_by||'dore',preservation,JSON.stringify(body?.scripture_refs||[]),JSON.stringify(body?.products_using_it||[]),JSON.stringify(body?.social_uses||[]),now).run();
  }catch(error){
    if(!existingObj)try{await env.DORE_ASSETS.delete(targetKey)}catch{}
    return json({ok:false,error:'registry_write_failed',rolled_back_r2:!existingObj,detail:String(error?.message||error)},500);
  }
  const verifyObj=await env.DORE_ASSETS.get(targetKey);
  const verifyHash=verifyObj?await sha256(await verifyObj.arrayBuffer()):null;
  const row=await env.DORE_SENSORY.prepare('SELECT id,asset_code,storage_backend,storage_locator,content_hash,byte_size,preservation_class,lifecycle_state,review_status FROM asset_registry WHERE id=?1').bind(assetId).first();
  const verified=Boolean(row&&verifyHash===hash&&row.content_hash===hash&&row.storage_backend==='r2'&&row.storage_locator===targetKey&&Number(row.byte_size)===bytes.byteLength);
  return json({ok:verified,action:existingObj?'registered_existing_r2':'migrated_github_to_r2',asset_id:assetId,asset_code:assetCode,source_path:sourcePath,target_key:targetKey,sha256:hash,bytes:bytes.byteLength,media_type:mediaType,preservation_class:preservation,registry_verified:verified,github_source_retained:true,rollback_window:true,completed_at:new Date().toISOString()},verified?200:500);
}
