const json=(data,status=200)=>new Response(JSON.stringify(data),{status,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store'}});
const clean=(v,max=12000)=>String(v??'').normalize('NFKC').trim().slice(0,max);
const safeId=(v,f='')=>clean(v,240).replace(/[^a-zA-Z0-9._:-]/g,'-')||f;
const newId=()=>typeof crypto.randomUUID==='function'?crypto.randomUUID():`${Date.now().toString(36)}-${Math.random().toString(36).slice(2)}`;
const sha256=async value=>{const b=new TextEncoder().encode(value);const d=await crypto.subtle.digest('SHA-256',b);return [...new Uint8Array(d)].map(x=>x.toString(16).padStart(2,'0')).join('')};

async function schema(db){
 await db.prepare(`CREATE TABLE IF NOT EXISTS dore_raw_history (
  id TEXT PRIMARY KEY,
  source TEXT NOT NULL,
  source_conversation_id TEXT NOT NULL,
  source_message_id TEXT,
  project_id TEXT NOT NULL DEFAULT 'dore-global',
  actor_id TEXT NOT NULL DEFAULT 'import',
  role TEXT NOT NULL,
  title TEXT,
  content TEXT NOT NULL,
  content_sha256 TEXT NOT NULL,
  source_created_at TEXT NOT NULL,
  source_updated_at TEXT,
  archive_key TEXT,
  imported_at TEXT NOT NULL,
  import_id TEXT,
  provenance_json TEXT
 )`).run();
 await db.prepare('CREATE UNIQUE INDEX IF NOT EXISTS idx_dore_raw_history_source_message ON dore_raw_history(source,source_conversation_id,source_message_id)').run();
 await db.prepare('CREATE INDEX IF NOT EXISTS idx_dore_raw_history_time ON dore_raw_history(source_created_at)').run();
 await db.prepare('CREATE INDEX IF NOT EXISTS idx_dore_raw_history_conversation_time ON dore_raw_history(source_conversation_id,source_created_at)').run();
 await db.prepare('CREATE INDEX IF NOT EXISTS idx_dore_raw_history_project_time ON dore_raw_history(project_id,source_created_at)').run();
}

function validTimestamp(v){const s=clean(v,80);return s&&Number.isFinite(Date.parse(s))?new Date(s).toISOString():''}

export async function ingestRawHistory(env,input={}){
 if(!env.DORE_SENSORY)throw new Error('memory_db_unbound');
 if(!env.DORE_MEMORY_ARCHIVE)throw new Error('memory_archive_unbound');
 await schema(env.DORE_SENSORY);
 const source=safeId(input.source,'chatgpt');
 const conversationId=safeId(input.source_conversation_id||input.conversation_id);
 const sourceMessageId=safeId(input.source_message_id||input.message_id);
 const projectId=safeId(input.project_id,'dore-global');
 const actorId=safeId(input.actor_id,'import');
 const role=clean(input.role,24).toLowerCase();
 const title=clean(input.title,500);
 const content=clean(input.content,120000);
 const sourceCreatedAt=validTimestamp(input.source_created_at||input.created_at);
 const sourceUpdatedAt=validTimestamp(input.source_updated_at||input.updated_at)||null;
 if(!conversationId)throw new Error('missing_source_conversation_id');
 if(!['system','user','assistant','tool','dore'].includes(role))throw new Error('invalid_role');
 if(!content)throw new Error('empty_content');
 if(!sourceCreatedAt)throw new Error('missing_or_invalid_source_created_at');
 const hash=await sha256(content);
 let existing=null;
 if(sourceMessageId)existing=await env.DORE_SENSORY.prepare('SELECT id,archive_key,source_created_at FROM dore_raw_history WHERE source=?1 AND source_conversation_id=?2 AND source_message_id=?3 LIMIT 1').bind(source,conversationId,sourceMessageId).first();
 if(!existing)existing=await env.DORE_SENSORY.prepare('SELECT id,archive_key,source_created_at FROM dore_raw_history WHERE source=?1 AND source_conversation_id=?2 AND content_sha256=?3 AND role=?4 AND source_created_at=?5 LIMIT 1').bind(source,conversationId,hash,role,sourceCreatedAt).first();
 if(existing)return {ok:true,deduplicated:true,id:existing.id,archive_key:existing.archive_key,source_created_at:existing.source_created_at};
 const id=newId(),importedAt=new Date().toISOString();
 const archiveKey=`raw-history/${encodeURIComponent(source)}/${sourceCreatedAt.slice(0,10)}/${encodeURIComponent(conversationId)}/${id}.json`;
 const provenance={source,source_conversation_id:conversationId,source_message_id:sourceMessageId||null,project_id:projectId,actor_id:actorId,role,title:title||null,source_created_at:sourceCreatedAt,source_updated_at:sourceUpdatedAt,import_id:safeId(input.import_id)||null,source_url:clean(input.source_url,2000)||null,source_export:clean(input.source_export,500)||null};
 const payload={schema:'dore.raw-history.v1',id,...provenance,content,content_sha256:hash,imported_at:importedAt};
 await env.DORE_MEMORY_ARCHIVE.put(archiveKey,JSON.stringify(payload),{httpMetadata:{contentType:'application/json'}});
 try{
  await env.DORE_SENSORY.prepare(`INSERT INTO dore_raw_history(id,source,source_conversation_id,source_message_id,project_id,actor_id,role,title,content,content_sha256,source_created_at,source_updated_at,archive_key,imported_at,import_id,provenance_json) VALUES(?1,?2,?3,?4,?5,?6,?7,?8,?9,?10,?11,?12,?13,?14,?15,?16)`).bind(id,source,conversationId,sourceMessageId||null,projectId,actorId,role,title||null,content,hash,sourceCreatedAt,sourceUpdatedAt,archiveKey,importedAt,provenance.import_id,JSON.stringify(provenance)).run();
 }catch(e){try{await env.DORE_MEMORY_ARCHIVE.delete(archiveKey)}catch{}throw e}
 return {ok:true,deduplicated:false,id,archive_key:archiveKey,source_created_at:sourceCreatedAt,provider_independent:true,workers_ai_used:false};
}

export async function importRawBatch(env,input={}){
 const messages=Array.isArray(input.messages)?input.messages:[];
 if(!messages.length)throw new Error('empty_import');
 const limit=Math.max(1,Math.min(100,Number(input.batch_size||50)));
 const start=Math.max(0,Number(input.cursor||0));
 const end=Math.min(messages.length,start+limit);
 let inserted=0,deduplicated=0,failed=0;const errors=[];
 for(let i=start;i<end;i++)try{const r=await ingestRawHistory(env,{...messages[i],source:messages[i]?.source||input.source||'chatgpt',project_id:messages[i]?.project_id||input.project_id||'dore-global',import_id:input.import_id});r.deduplicated?deduplicated++:inserted++}catch(e){failed++;errors.push({index:i,error:String(e?.message||e)})}
 return {ok:failed===0,schema:'dore.raw-history-import.v1',import_id:safeId(input.import_id)||null,total:messages.length,processed:end,inserted,deduplicated,failed,cursor:end,completed:end>=messages.length,errors:errors.slice(0,20),workers_ai_used:false};
}

export async function recallRawHistory(env,input={}){
 if(!env.DORE_SENSORY)throw new Error('memory_db_unbound');await schema(env.DORE_SENSORY);
 const from=validTimestamp(input.from)||'1970-01-01T00:00:00.000Z';
 const to=validTimestamp(input.to)||'9999-12-31T23:59:59.999Z';
 const source=safeId(input.source);
 const conversationId=safeId(input.source_conversation_id||input.conversation_id);
 const q=clean(input.query,1000).toLowerCase();
 const limit=Math.max(1,Math.min(500,Number(input.limit||100)));
 let sql='SELECT id,source,source_conversation_id,source_message_id,project_id,actor_id,role,title,content,source_created_at,source_updated_at,archive_key,import_id FROM dore_raw_history WHERE source_created_at>=?1 AND source_created_at<=?2';
 const binds=[from,to];
 if(source){binds.push(source);sql+=` AND source=?${binds.length}`}
 if(conversationId){binds.push(conversationId);sql+=` AND source_conversation_id=?${binds.length}`}
 if(q){binds.push(`%${q}%`);sql+=` AND (lower(content) LIKE ?${binds.length} OR lower(COALESCE(title,'')) LIKE ?${binds.length})`}
 binds.push(limit);sql+=` ORDER BY source_created_at ASC,id ASC LIMIT ?${binds.length}`;
 const r=await env.DORE_SENSORY.prepare(sql).bind(...binds).all();
 return {ok:true,schema:'dore.raw-history-recall.v1',retrieval:'structured-time-and-text',provider_independent:true,workers_ai_used:false,scope:{from,to,source:source||null,source_conversation_id:conversationId||null,query:q||null},messages:r?.results||[]};
}

export async function coverage(env,input={}){
 if(!env.DORE_SENSORY)throw new Error('memory_db_unbound');await schema(env.DORE_SENSORY);
 const from=validTimestamp(input.from)||'1970-01-01T00:00:00.000Z',to=validTimestamp(input.to)||'9999-12-31T23:59:59.999Z',source=safeId(input.source,'chatgpt');
 const summary=await env.DORE_SENSORY.prepare(`SELECT COUNT(*) messages,COUNT(DISTINCT source_conversation_id) conversations,MIN(source_created_at) earliest,MAX(source_created_at) latest FROM dore_raw_history WHERE source=?1 AND source_created_at>=?2 AND source_created_at<=?3`).bind(source,from,to).first();
 const days=await env.DORE_SENSORY.prepare(`SELECT substr(source_created_at,1,10) day,COUNT(*) messages,COUNT(DISTINCT source_conversation_id) conversations FROM dore_raw_history WHERE source=?1 AND source_created_at>=?2 AND source_created_at<=?3 GROUP BY substr(source_created_at,1,10) ORDER BY day`).bind(source,from,to).all();
 return {ok:true,schema:'dore.raw-history-coverage.v1',source,from,to,summary,days:days?.results||[],workers_ai_used:false};
}

export async function onRequestPost({request,env}){let b;try{b=await request.json()}catch{return json({ok:false,error:'invalid_json'},400)}try{if(b.action==='recall')return json(await recallRawHistory(env,b));if(b.action==='coverage')return json(await coverage(env,b));if(b.action==='import')return json(await importRawBatch(env,b));return json(await ingestRawHistory(env,b),201)}catch(e){const detail=String(e?.message||e);const bad=detail.startsWith('missing_')||detail==='invalid_role'||detail==='empty_content'||detail==='empty_import';return json({ok:false,error:'raw_history_failed',detail,workers_ai_used:false},bad?400:500)}}
