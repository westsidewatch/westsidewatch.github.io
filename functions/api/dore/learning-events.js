const json=(d,s=200)=>new Response(JSON.stringify(d),{status:s,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store'}});
const clean=(v,m=12000)=>String(v??'').normalize('NFKC').trim().slice(0,m);
const safeId=(v,f='')=>clean(v,160).replace(/[^a-zA-Z0-9._:-]/g,'-')||f;

async function schema(db){
  await db.prepare(`CREATE TABLE IF NOT EXISTS dore_learning_events (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    conversation_id TEXT,
    source_node TEXT NOT NULL,
    event_type TEXT NOT NULL,
    scope TEXT NOT NULL,
    brand_project_status TEXT NOT NULL,
    modality TEXT NOT NULL,
    knowledge_status TEXT NOT NULL,
    importance TEXT NOT NULL,
    summary TEXT NOT NULL,
    evidence TEXT,
    source_ref TEXT,
    journal_status TEXT NOT NULL DEFAULT 'pending',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
  )`).run();
  await db.prepare('CREATE INDEX IF NOT EXISTS idx_dore_learning_events_journal ON dore_learning_events(journal_status,importance,created_at)').run();
  await db.prepare('CREATE INDEX IF NOT EXISTS idx_dore_learning_events_project ON dore_learning_events(project_id,created_at)').run();
}

export async function collectLearningEvent(env,input={}){
  if(!env.DORE_SENSORY)throw new Error('memory_db_unbound');
  await schema(env.DORE_SENSORY);
  const now=new Date().toISOString();
  const id=safeId(input.id,`le-${Date.now()}-${crypto.randomUUID().slice(0,8)}`);
  const projectId=safeId(input.project_id,'unscoped');
  const summary=clean(input.summary,4000);
  if(!summary)throw new Error('missing_summary');
  const row={
    id,project_id:projectId,conversation_id:safeId(input.conversation_id),source_node:safeId(input.source_node,'unknown'),
    event_type:safeId(input.event_type,'observation'),scope:safeId(input.scope,'candidate'),
    brand_project_status:safeId(input.brand_project_status,'candidate'),modality:safeId(input.modality,'text'),
    knowledge_status:safeId(input.knowledge_status,'observation'),importance:safeId(input.importance,'normal'),
    summary,evidence:clean(input.evidence,8000),source_ref:clean(input.source_ref,1000),created_at:clean(input.created_at,64)||now
  };
  await env.DORE_SENSORY.prepare(`INSERT OR IGNORE INTO dore_learning_events
    (id,project_id,conversation_id,source_node,event_type,scope,brand_project_status,modality,knowledge_status,importance,summary,evidence,source_ref,journal_status,created_at,updated_at)
    VALUES(?1,?2,?3,?4,?5,?6,?7,?8,?9,?10,?11,?12,?13,'pending',?14,?15)`)
    .bind(row.id,row.project_id,row.conversation_id,row.source_node,row.event_type,row.scope,row.brand_project_status,row.modality,row.knowledge_status,row.importance,row.summary,row.evidence,row.source_ref,row.created_at,now).run();
  return {ok:true,schema:'dore.learning-event.v1',event:row,journal_status:'pending',workers_ai_required:false};
}

export async function listJournalCandidates(env,input={}){
  if(!env.DORE_SENSORY)throw new Error('memory_db_unbound');
  await schema(env.DORE_SENSORY);
  const limit=Math.max(1,Math.min(100,Number(input.limit||50)));
  const r=await env.DORE_SENSORY.prepare(`SELECT * FROM dore_learning_events WHERE journal_status='pending' ORDER BY CASE importance WHEN 'critical' THEN 4 WHEN 'high' THEN 3 WHEN 'normal' THEN 2 ELSE 1 END DESC, created_at ASC LIMIT ?1`).bind(limit).all();
  return {ok:true,schema:'dore.journal-candidates.v1',candidates:r.results||[],workers_ai_required:false};
}

export async function markJournalEvent(env,input={}){
  if(!env.DORE_SENSORY)throw new Error('memory_db_unbound');
  await schema(env.DORE_SENSORY);
  const id=safeId(input.id); if(!id)throw new Error('missing_id');
  const status=safeId(input.journal_status,'pending');
  if(!['pending','accepted','rejected','written'].includes(status))throw new Error('invalid_journal_status');
  await env.DORE_SENSORY.prepare('UPDATE dore_learning_events SET journal_status=?1,updated_at=?2 WHERE id=?3').bind(status,new Date().toISOString(),id).run();
  return {ok:true,id,journal_status:status};
}

export async function onRequestPost({request,env}){
  let b;try{b=await request.json()}catch{return json({ok:false,error:'invalid_json'},400)}
  try{
    if(b.action==='list_candidates')return json(await listJournalCandidates(env,b));
    if(b.action==='mark')return json(await markJournalEvent(env,b));
    return json(await collectLearningEvent(env,b),201);
  }catch(e){const detail=String(e?.message||e);return json({ok:false,error:'learning_event_failed',detail},detail.startsWith('missing_')||detail.startsWith('invalid_')?400:500)}
}
