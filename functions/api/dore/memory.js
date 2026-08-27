const json=(data,status=200)=>new Response(JSON.stringify(data),{status,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store'}});
const newId=()=>typeof crypto.randomUUID==='function'?crypto.randomUUID():`${Date.now().toString(36)}-${Math.random().toString(36).slice(2)}`;
const clean=(value,max=12000)=>String(value??'').normalize('NFKC').trim().slice(0,max);
const safeId=(value,fallback='')=>clean(value,160).replace(/[^a-zA-Z0-9._:-]/g,'-')||fallback;
const ns=(project,conversation)=>`${project}::${conversation}`.slice(0,64);
const sha256=async value=>{const b=new TextEncoder().encode(value);const d=await crypto.subtle.digest('SHA-256',b);return [...new Uint8Array(d)].map(x=>x.toString(16).padStart(2,'0')).join('')};
const EMBEDDING_MODEL='@cf/baai/bge-small-en-v1.5';

async function ensureSchema(db){
  await db.prepare(`CREATE TABLE IF NOT EXISTS dore_conversations (id TEXT PRIMARY KEY,project_id TEXT NOT NULL,actor_id TEXT NOT NULL DEFAULT 'internal',mode TEXT NOT NULL DEFAULT 'INTERNAL_ALPHA',title TEXT,created_at TEXT NOT NULL,updated_at TEXT NOT NULL)`).run();
  await db.prepare(`CREATE TABLE IF NOT EXISTS dore_messages (id TEXT PRIMARY KEY,conversation_id TEXT NOT NULL,project_id TEXT NOT NULL,actor_id TEXT NOT NULL DEFAULT 'internal',role TEXT NOT NULL,content TEXT NOT NULL,content_sha256 TEXT NOT NULL,archive_key TEXT,created_at TEXT NOT NULL)`).run();
  await db.prepare('CREATE UNIQUE INDEX IF NOT EXISTS idx_dore_messages_conversation_hash ON dore_messages(conversation_id,content_sha256,role)').run();
  await db.prepare('CREATE INDEX IF NOT EXISTS idx_dore_messages_conversation_created ON dore_messages(conversation_id,created_at DESC)').run();
  await db.prepare('CREATE INDEX IF NOT EXISTS idx_dore_messages_project_created ON dore_messages(project_id,created_at DESC)').run();
}

async function embed(env,text){
  if(!env.AI)throw new Error('ai_unbound');
  const r=await env.AI.run(EMBEDDING_MODEL,{text:[text]});
  const vector=r?.data?.[0];
  if(!Array.isArray(vector)||vector.length!==384)throw new Error('embedding_response_invalid');
  return vector;
}

export async function ingestMessage(env,input={}){
  if(!env.DORE_SENSORY)throw new Error('memory_db_unbound');
  if(!env.DORE_MEMORY_VECTOR)throw new Error('memory_vector_unbound');
  if(!env.DORE_MEMORY_ARCHIVE)throw new Error('memory_archive_unbound');
  const projectId=safeId(input?.project_id,'unscoped');
  const conversationId=safeId(input?.conversation_id);
  const actorId=safeId(input?.actor_id,'internal');
  const role=clean(input?.role,24).toLowerCase();
  const content=clean(input?.content);
  if(!conversationId)throw new Error('missing_conversation_id');
  if(!['system','user','assistant','dore','tool'].includes(role))throw new Error('invalid_role');
  if(!content)throw new Error('empty_content');
  await ensureSchema(env.DORE_SENSORY);
  const hash=await sha256(content);
  const existing=await env.DORE_SENSORY.prepare('SELECT id,archive_key,created_at FROM dore_messages WHERE conversation_id=?1 AND content_sha256=?2 AND role=?3 LIMIT 1').bind(conversationId,hash,role).first();
  if(existing)return {ok:true,deduplicated:true,message_id:existing.id,vector_id:existing.id,conversation_id:conversationId,project_id:projectId,archive_key:existing.archive_key||null,created_at:existing.created_at,namespace:ns(projectId,conversationId),embedding_model:EMBEDDING_MODEL};
  const now=new Date().toISOString(),messageId=newId(),mode=clean(input?.mode,40)||'INTERNAL_ALPHA';
  const archiveKey=`conversations/${encodeURIComponent(projectId)}/${encodeURIComponent(conversationId)}/${messageId}.json`;
  const archivePayload={schema:'dore.conversation-message.v2',message_id:messageId,conversation_id:conversationId,project_id:projectId,actor_id:actorId,role,content,content_sha256:hash,created_at:now,embedding_model:EMBEDDING_MODEL};
  const namespace=ns(projectId,conversationId);
  let archiveWritten=false,vectorWritten=false;
  try{
    const vector=await embed(env,content);
    await env.DORE_MEMORY_ARCHIVE.put(archiveKey,JSON.stringify(archivePayload),{httpMetadata:{contentType:'application/json'}});archiveWritten=true;
    await env.DORE_MEMORY_VECTOR.upsert([{id:messageId,values:vector,namespace,metadata:{kind:'conversation_message',schema:'v2',message_id:messageId,conversation_id:conversationId,project_id:projectId,actor_id:actorId,role,archive_key:archiveKey,content_sha256:hash,created_at:now}}]);vectorWritten=true;
    await env.DORE_SENSORY.prepare(`INSERT INTO dore_conversations(id,project_id,actor_id,mode,title,created_at,updated_at) VALUES(?1,?2,?3,?4,?5,?6,?6) ON CONFLICT(id) DO UPDATE SET project_id=excluded.project_id,actor_id=excluded.actor_id,updated_at=excluded.updated_at`).bind(conversationId,projectId,actorId,mode,clean(input?.title,240)||null,now).run();
    await env.DORE_SENSORY.prepare(`INSERT INTO dore_messages(id,conversation_id,project_id,actor_id,role,content,content_sha256,archive_key,created_at) VALUES(?1,?2,?3,?4,?5,?6,?7,?8,?9)`).bind(messageId,conversationId,projectId,actorId,role,content,hash,archiveKey,now).run();
    return {ok:true,deduplicated:false,message_id:messageId,vector_id:messageId,conversation_id:conversationId,project_id:projectId,archive_key:archiveKey,namespace,embedding_model:EMBEDDING_MODEL,created_at:now};
  }catch(error){
    if(vectorWritten)try{await env.DORE_MEMORY_VECTOR.deleteByIds([messageId])}catch{}
    if(archiveWritten)try{await env.DORE_MEMORY_ARCHIVE.delete(archiveKey)}catch{}
    throw error;
  }
}

export async function onRequestPost({request,env}){
  let body;try{body=await request.json()}catch{return json({ok:false,error:'invalid_json'},400)}
  try{return json(await ingestMessage(env,body),201)}catch(error){
    const detail=String(error?.message||error);
    const status=['missing_conversation_id','invalid_role','empty_content'].includes(detail)?400:detail.endsWith('_unbound')?503:500;
    return json({ok:false,error:'memory_ingestion_failed',detail},status);
  }
}

export async function onRequestGet({request,env}){
  if(!env.DORE_SENSORY)return json({ok:false,error:'memory_db_unbound'},503);
  const url=new URL(request.url),conversationId=safeId(url.searchParams.get('conversation_id')),projectId=safeId(url.searchParams.get('project_id'));
  const limit=Math.max(1,Math.min(80,Number(url.searchParams.get('limit')||24)));
  if(!conversationId&&!projectId)return json({ok:false,error:'scope_required'},400);
  try{
    await ensureSchema(env.DORE_SENSORY);
    let result;
    if(conversationId&&projectId)result=await env.DORE_SENSORY.prepare('SELECT id,conversation_id,project_id,actor_id,role,content,archive_key,created_at FROM dore_messages WHERE conversation_id=?1 AND project_id=?2 ORDER BY created_at DESC LIMIT ?3').bind(conversationId,projectId,limit).all();
    else if(conversationId)result=await env.DORE_SENSORY.prepare('SELECT id,conversation_id,project_id,actor_id,role,content,archive_key,created_at FROM dore_messages WHERE conversation_id=?1 ORDER BY created_at DESC LIMIT ?2').bind(conversationId,limit).all();
    else result=await env.DORE_SENSORY.prepare('SELECT id,conversation_id,project_id,actor_id,role,content,archive_key,created_at FROM dore_messages WHERE project_id=?1 ORDER BY created_at DESC LIMIT ?2').bind(projectId,limit).all();
    return json({ok:true,scope:{conversation_id:conversationId||null,project_id:projectId||null},retrieval_mode:'scoped_recent',vectorize_bound:Boolean(env.DORE_MEMORY_VECTOR),archive_bound:Boolean(env.DORE_MEMORY_ARCHIVE),messages:(result?.results||[]).reverse()});
  }catch(error){return json({ok:false,error:'memory_read_failed',detail:String(error?.message||error)},500)}
}
