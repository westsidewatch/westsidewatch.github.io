import {ingestMessage} from './memory.js';
const json=(d,s=200)=>new Response(JSON.stringify(d),{status:s,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store'}});
const auth=(r,e)=>Boolean(e.DORE_HEARTBEAT_TOKEN)&&(r.headers.get('authorization')||'')===`Bearer ${e.DORE_HEARTBEAT_TOKEN}`;
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function embed(env,text){const r=await env.AI.run('@cf/baai/bge-small-en-v1.5',{text:[text]});return r?.data?.[0]||null;}
async function waitForVector(env,vector,namespace,expectedId){let last=null;for(let i=0;i<12;i++){last=await env.DORE_MEMORY_VECTOR.query(vector,{topK:5,namespace,returnMetadata:'all'});if(last?.matches?.some(m=>m?.id===expectedId))return last;await sleep(5000);}return last;}
export async function onRequestPost({request,env}){
  if(!auth(request,env))return json({ok:false,error:'unauthorized'},401);
  const bindings={d1:Boolean(env.DORE_SENSORY),vectorize:Boolean(env.DORE_MEMORY_VECTOR),archive:Boolean(env.DORE_MEMORY_ARCHIVE),ai:Boolean(env.AI)};
  if(!bindings.d1||!bindings.vectorize||!bindings.archive||!bindings.ai)return json({ok:false,stage:'M3',bindings,error:'m3_binding_missing'},503);
  const run=crypto.randomUUID(),project='full-memory-phase1-m3',conversation='conversation-'+run;
  const userText=`Before dawn ${run}, the reader placed an olive-wood bookmark beside the open Gospel manuscript.`;
  const assistantText=`Doré recorded ${run} as a conversation memory and preserved its project and conversation scope.`;
  const ids=[],archives=[];
  try{
    const first=await ingestMessage(env,{project_id:project,conversation_id:conversation,actor_id:'diagnostic-user',role:'user',content:userText,title:'M3 diagnostic'});ids.push(first.message_id);archives.push(first.archive_key);
    const second=await ingestMessage(env,{project_id:project,conversation_id:conversation,actor_id:'dore',role:'assistant',content:assistantText,title:'M3 diagnostic'});ids.push(second.message_id);archives.push(second.archive_key);
    const duplicate=await ingestMessage(env,{project_id:project,conversation_id:conversation,actor_id:'diagnostic-user',role:'user',content:userText,title:'M3 diagnostic'});
    const rows=await env.DORE_SENSORY.prepare('SELECT id,conversation_id,project_id,actor_id,role,content,archive_key,created_at FROM dore_messages WHERE conversation_id=?1 AND project_id=?2 ORDER BY created_at,id').bind(conversation,project).all();
    const stored=rows?.results||[];
    const exactReplay=stored.length===2&&stored.some(x=>x.id===first.message_id&&x.content===userText&&x.role==='user')&&stored.some(x=>x.id===second.message_id&&x.content===assistantText&&x.role==='assistant');
    const dedupe=duplicate.deduplicated===true&&duplicate.message_id===first.message_id&&stored.length===2;
    const a1=await env.DORE_MEMORY_ARCHIVE.get(first.archive_key),a2=await env.DORE_MEMORY_ARCHIVE.get(second.archive_key);
    const p1=a1?JSON.parse(await a1.text()):null,p2=a2?JSON.parse(await a2.text()):null;
    const archiveRoundtrip=p1?.content===userText&&p1?.conversation_id===conversation&&p1?.project_id===project&&p2?.content===assistantText&&p2?.role==='assistant';
    const q=await embed(env,'Which conversation memory mentions a wooden bookmark next to a Gospel manuscript before sunrise?');
    const vr=await waitForVector(env,q,first.namespace,first.message_id);
    const match=vr?.matches?.find(m=>m?.id===first.message_id)||null;
    const vectorMetadata=Boolean(match)&&match.metadata?.conversation_id===conversation&&match.metadata?.project_id===project&&match.metadata?.role==='user'&&match.metadata?.archive_key===first.archive_key;
    const pass=exactReplay&&dedupe&&archiveRoundtrip&&vectorMetadata;
    await env.DORE_MEMORY_VECTOR.deleteByIds(ids);
    for(const key of archives)if(key)await env.DORE_MEMORY_ARCHIVE.delete(key);
    await env.DORE_SENSORY.prepare('DELETE FROM dore_messages WHERE conversation_id=?1 AND project_id=?2').bind(conversation,project).run();
    await env.DORE_SENSORY.prepare('DELETE FROM dore_conversations WHERE id=?1 AND project_id=?2').bind(conversation,project).run();
    return json({ok:pass,stage:'M3',milestone:pass?'M3_CONVERSATION_INGESTION_PASS':'M3_CONVERSATION_INGESTION_FAIL',bindings,checks:{conversation_rows:stored.length,exact_replay:exactReplay,deduplication:dedupe,archive_roundtrip:archiveRoundtrip,vector_metadata:vectorMetadata,semantic_score:match?.score||null,cleanup:true},contract:{schema:'dore.conversation-message.v2',embedding_model:first.embedding_model,namespace:first.namespace},next:pass?'M4_RETRIEVAL_CONTEXT_ASSEMBLY':'M3_REPAIR'});
  }catch(e){
    try{if(ids.length)await env.DORE_MEMORY_VECTOR.deleteByIds(ids)}catch{}
    for(const key of archives)try{if(key)await env.DORE_MEMORY_ARCHIVE.delete(key)}catch{}
    try{await env.DORE_SENSORY.prepare('DELETE FROM dore_messages WHERE conversation_id=?1 AND project_id=?2').bind(conversation,project).run();await env.DORE_SENSORY.prepare('DELETE FROM dore_conversations WHERE id=?1 AND project_id=?2').bind(conversation,project).run()}catch{}
    return json({ok:false,stage:'M3',bindings,error:String(e?.message||e)},500);
  }
}
