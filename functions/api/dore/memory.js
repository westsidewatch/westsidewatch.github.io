const json=(data,status=200)=>new Response(JSON.stringify(data),{status,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store'}});
const newId=()=>typeof crypto.randomUUID==='function'?crypto.randomUUID():`${Date.now().toString(36)}-${Math.random().toString(36).slice(2)}`;
const clean=(value,max=12000)=>String(value??'').normalize('NFKC').trim().slice(0,max);
const safeId=(value,fallback='')=>clean(value,160).replace(/[^a-zA-Z0-9._:-]/g,'-')||fallback;
const sha256=async value=>{const b=new TextEncoder().encode(value);const d=await crypto.subtle.digest('SHA-256',b);return [...new Uint8Array(d)].map(x=>x.toString(16).padStart(2,'0')).join('')};

async function ensureSchema(db){
  await db.prepare(`CREATE TABLE IF NOT EXISTS dore_conversations (id TEXT PRIMARY KEY,project_id TEXT NOT NULL,actor_id TEXT NOT NULL DEFAULT 'internal',mode TEXT NOT NULL DEFAULT 'INTERNAL_ALPHA',title TEXT,created_at TEXT NOT NULL,updated_at TEXT NOT NULL)`).run();
  await db.prepare(`CREATE TABLE IF NOT EXISTS dore_messages (id TEXT PRIMARY KEY,conversation_id TEXT NOT NULL,project_id TEXT NOT NULL,actor_id TEXT NOT NULL DEFAULT 'internal',role TEXT NOT NULL,content TEXT NOT NULL,content_sha256 TEXT NOT NULL,archive_key TEXT,created_at TEXT NOT NULL)`).run();
  await db.prepare('CREATE UNIQUE INDEX IF NOT EXISTS idx_dore_messages_conversation_hash ON dore_messages(conversation_id,content_sha256,role)').run();
  await db.prepare('CREATE INDEX IF NOT EXISTS idx_dore_messages_conversation_created ON dore_messages(conversation_id,created_at DESC)').run();
  await db.prepare('CREATE INDEX IF NOT EXISTS idx_dore_messages_project_created ON dore_messages(project_id,created_at DESC)').run();
}

export async function onRequestPost({request,env}){
  if(!env.DORE_SENSORY)return json({ok:false,error:'memory_db_unbound'},503);
  let body;try{body=await request.json()}catch{return json({ok:false,error:'invalid_json'},400)}
  const projectId=safeId(body?.project_id,'unscoped');
  const conversationId=safeId(body?.conversation_id);
  const actorId=safeId(body?.actor_id,'internal');
  const role=clean(body?.role,24).toLowerCase();
  const content=clean(body?.content);
  if(!conversationId)return json({ok:false,error:'missing_conversation_id'},400);
  if(!['system','user','assistant','dore','tool'].includes(role))return json({ok:false,error:'invalid_role'},400);
  if(!content)return json({ok:false,error:'empty_content'},400);
  const now=new Date().toISOString(), messageId=newId(), hash=await sha256(content), mode=clean(body?.mode,40)||'INTERNAL_ALPHA';
  try{
    await ensureSchema(env.DORE_SENSORY);
    await env.DORE_SENSORY.prepare(`INSERT INTO dore_conversations(id,project_id,actor_id,mode,title,created_at,updated_at) VALUES(?1,?2,?3,?4,?5,?6,?6) ON CONFLICT(id) DO UPDATE SET project_id=excluded.project_id,actor_id=excluded.actor_id,updated_at=excluded.updated_at`).bind(conversationId,projectId,actorId,mode,clean(body?.title,240)||null,now).run();
    const existing=await env.DORE_SENSORY.prepare('SELECT id,archive_key,created_at FROM dore_messages WHERE conversation_id=?1 AND content_sha256=?2 AND role=?3 LIMIT 1').bind(conversationId,hash,role).first();
    if(existing)return json({ok:true,deduplicated:true,message_id:existing.id,conversation_id:conversationId,project_id:projectId,archive_key:existing.archive_key||null,created_at:existing.created_at});
    let archiveKey=null;
    if(env.DORE_MEMORY_ARCHIVE){
      archiveKey=`conversations/${encodeURIComponent(projectId)}/${encodeURIComponent(conversationId)}/${messageId}.json`;
      await env.DORE_MEMORY_ARCHIVE.put(archiveKey,JSON.stringify({schema:'dore.conversation-message.v1',message_id:messageId,conversation_id:conversationId,project_id:projectId,actor_id:actorId,role,content,created_at:now}),{httpMetadata:{contentType:'application/json'}});
    }
    await env.DORE_SENSORY.prepare(`INSERT INTO dore_messages(id,conversation_id,project_id,actor_id,role,content,content_sha256,archive_key,created_at) VALUES(?1,?2,?3,?4,?5,?6,?7,?8,?9)`).bind(messageId,conversationId,projectId,actorId,role,content,hash,archiveKey,now).run();
    return json({ok:true,deduplicated:false,message_id:messageId,conversation_id:conversationId,project_id:projectId,archive_key:archiveKey,vectorize_bound:Boolean(env.DORE_MEMORY_VECTOR),created_at:now},201);
  }catch(error){return json({ok:false,error:'memory_write_failed',detail:String(error?.message||error)},500)}
}

export async function onRequestGet({request,env}){
  if(!env.DORE_SENSORY)return json({ok:false,error:'memory_db_unbound'},503);
  const url=new URL(request.url), conversationId=safeId(url.searchParams.get('conversation_id')), projectId=safeId(url.searchParams.get('project_id'));
  const limit=Math.max(1,Math.min(80,Number(url.searchParams.get('limit')||24)));
  if(!conversationId&&!projectId)return json({ok:false,error:'scope_required'},400);
  try{
    await ensureSchema(env.DORE_SENSORY);
    let result;
    if(conversationId){
      result=await env.DORE_SENSORY.prepare(`SELECT id,conversation_id,project_id,actor_id,role,content,archive_key,created_at FROM dore_messages WHERE conversation_id=?1${projectId?' AND project_id=?2':''} ORDER BY created_at DESC LIMIT ?3`).bind(...(projectId?[conversationId,projectId,limit]:[conversationId,limit,limit])).all();
    }else{
      result=await env.DORE_SENSORY.prepare('SELECT id,conversation_id,project_id,actor_id,role,content,archive_key,created_at FROM dore_messages WHERE project_id=?1 ORDER BY created_at DESC LIMIT ?2').bind(projectId,limit).all();
    }
    const messages=(result?.results||[]).reverse();
    return json({ok:true,scope:{conversation_id:conversationId||null,project_id:projectId||null},retrieval_mode:'scoped_recent',vectorize_bound:Boolean(env.DORE_MEMORY_VECTOR),archive_bound:Boolean(env.DORE_MEMORY_ARCHIVE),messages});
  }catch(error){return json({ok:false,error:'memory_read_failed',detail:String(error?.message||error)},500)}
}
