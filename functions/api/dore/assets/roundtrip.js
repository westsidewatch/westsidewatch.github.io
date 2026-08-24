const json=(data,status=200)=>new Response(JSON.stringify(data),{status,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store'}});
const hex=bytes=>[...new Uint8Array(bytes)].map(b=>b.toString(16).padStart(2,'0')).join('');
const sha256=async bytes=>hex(await crypto.subtle.digest('SHA-256',bytes));
const id=()=>crypto.randomUUID();

async function ensureRegistry(db){
  await db.prepare(`CREATE TABLE IF NOT EXISTS asset_registry (
    id TEXT PRIMARY KEY,
    storage_backend TEXT NOT NULL,
    storage_locator TEXT NOT NULL UNIQUE,
    content_hash TEXT NOT NULL,
    media_type TEXT NOT NULL,
    byte_size INTEGER NOT NULL,
    preservation_class TEXT NOT NULL DEFAULT 'temporary',
    lifecycle_state TEXT NOT NULL DEFAULT 'active',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
  )`).run();
  await db.prepare('CREATE INDEX IF NOT EXISTS idx_asset_registry_hash ON asset_registry(content_hash)').run();
  await db.prepare('CREATE INDEX IF NOT EXISTS idx_asset_registry_lifecycle ON asset_registry(lifecycle_state)').run();
}

export async function onRequestPost({env}){
  if(!env.DORE_SENSORY||!env.DORE_ASSETS)return json({ok:false,error:'required_binding_unbound',d1_bound:Boolean(env.DORE_SENSORY),r2_bound:Boolean(env.DORE_ASSETS)},503);
  const assetId=id();
  const key=`_system/roundtrip/${assetId}.txt`;
  const payload=new TextEncoder().encode(`dore-asset-roundtrip:${assetId}`);
  const expectedHash=await sha256(payload);
  const now=new Date().toISOString();
  let stage='schema';
  try{
    await ensureRegistry(env.DORE_SENSORY);
    stage='r2_write';
    await env.DORE_ASSETS.put(key,payload,{httpMetadata:{contentType:'text/plain; charset=utf-8'},customMetadata:{purpose:'disposable-roundtrip',sha256:expectedHash}});
    stage='d1_register';
    await env.DORE_SENSORY.prepare(`INSERT INTO asset_registry (id,storage_backend,storage_locator,content_hash,media_type,byte_size,preservation_class,lifecycle_state,created_at,updated_at) VALUES (?1,'r2',?2,?3,'text/plain',?4,'temporary','active',?5,?5)`).bind(assetId,key,expectedHash,payload.byteLength,now).run();
    stage='r2_read';
    const obj=await env.DORE_ASSETS.get(key);
    if(!obj)throw new Error('r2_object_missing_after_write');
    const readBytes=await obj.arrayBuffer();
    const actualHash=await sha256(readBytes);
    stage='registry_verify';
    const row=await env.DORE_SENSORY.prepare('SELECT id,storage_backend,storage_locator,content_hash,byte_size,preservation_class,lifecycle_state FROM asset_registry WHERE id=?1').bind(assetId).first();
    const verified=Boolean(row&&row.storage_backend==='r2'&&row.storage_locator===key&&row.content_hash===expectedHash&&actualHash===expectedHash&&Number(row.byte_size)===payload.byteLength&&row.preservation_class==='temporary'&&row.lifecycle_state==='active');
    if(!verified)throw new Error('registry_or_hash_verification_failed');
    stage='cleanup_r2';
    await env.DORE_ASSETS.delete(key);
    stage='cleanup_d1';
    await env.DORE_SENSORY.prepare('DELETE FROM asset_registry WHERE id=?1').bind(assetId).run();
    stage='residue_check';
    const [r2Residue,d1Residue]=await Promise.all([
      env.DORE_ASSETS.head(key),
      env.DORE_SENSORY.prepare('SELECT id FROM asset_registry WHERE id=?1').bind(assetId).first()
    ]);
    const clean=!r2Residue&&!d1Residue;
    return json({ok:clean,schema:'asset_registry',asset_id:assetId,storage_locator:key,write:true,d1_registered:true,read:true,hash_verified:actualHash===expectedHash,registry_verified:verified,deleted_r2:!r2Residue,deleted_d1:!d1Residue,residue:false,clean,sha256:expectedHash,bytes:payload.byteLength,completed_at:new Date().toISOString()},clean?200:500);
  }catch(error){
    // Best-effort rollback so a failed disposable test does not intentionally leave residue.
    try{await env.DORE_ASSETS.delete(key)}catch{}
    try{await env.DORE_SENSORY.prepare('DELETE FROM asset_registry WHERE id=?1').bind(assetId).run()}catch{}
    return json({ok:false,error:'asset_roundtrip_failed',stage,asset_id:assetId,storage_locator:key,detail:String(error?.message||error)},500);
  }
}
