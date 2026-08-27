import {ingestMessage} from './memory.js';
import {generateMemoryAwareResponse} from './respond.js';
const json=(d,s=200)=>new Response(JSON.stringify(d),{status:s,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store'}});
const auth=(r,e)=>Boolean(e.DORE_HEARTBEAT_TOKEN)&&(r.headers.get('authorization')||'')===`Bearer ${e.DORE_HEARTBEAT_TOKEN}`;
const sleep=ms=>new Promise(r=>setTimeout(r,ms));

export async function onRequestPost({request,env}){
  if(!auth(request,env))return json({ok:false,error:'unauthorized'},401);
  const bindings={d1:Boolean(env.DORE_SENSORY),vectorize:Boolean(env.DORE_MEMORY_VECTOR),archive:Boolean(env.DORE_MEMORY_ARCHIVE),ai:Boolean(env.AI)};
  if(!bindings.d1||!bindings.vectorize||!bindings.archive||!bindings.ai)return json({ok:false,stage:'M5',bindings,error:'m5_binding_missing'},503);
  const run=crypto.randomUUID(),project='full-memory-phase1-m5',conversation='conversation-'+run;
  const decision=`For project ${run}, the reader decided that every chapter map must use bilingual Chinese-English labels.`;
  const distractor=`In project ${run}, the reader also noted that the desk lamp uses a brass shade.`;
  const followup=`Later in project ${run}, the reader asked Doré to preserve that map-label decision for future chapter work.`;
  const ids=[],archives=[];
  try{
    for(const content of [decision,distractor,followup]){
      const x=await ingestMessage(env,{project_id:project,conversation_id:conversation,actor_id:'diagnostic-user',role:'user',content,title:'M5 diagnostic'});
      ids.push(x.message_id);archives.push(x.archive_key);
    }
    let result=null;
    for(let i=0;i<12;i++){
      result=await generateMemoryAwareResponse(env,{project_id:project,conversation_id:conversation,query:'What exact label format did I decide to use for every chapter map? Answer with the remembered format.',top_k:8,recent_limit:1,min_score:0.35,max_chars:5000});
      if(Number(result?.memory?.semantic_count||0)>0&&/Chinese-English/i.test(result?.answer||''))break;
      await sleep(5000);
    }
    const answer=result?.answer||'';
    const remembered=/bilingual/i.test(answer)&&/Chinese-English/i.test(answer)&&/label/i.test(answer);
    const avoidedDistractor=!/brass shade|desk lamp/i.test(answer);
    const semanticUsed=Number(result?.memory?.semantic_count||0)>0;
    const scoped=result?.memory?.scope?.project_id===project&&result?.memory?.scope?.conversation_id===conversation;
    const modelBound=result?.contract?.response_model==='@cf/meta/llama-3.1-8b-instruct-fast';
    const pass=remembered&&avoidedDistractor&&semanticUsed&&scoped&&modelBound;
    await env.DORE_MEMORY_VECTOR.deleteByIds(ids);
    for(const key of archives)if(key)await env.DORE_MEMORY_ARCHIVE.delete(key);
    await env.DORE_SENSORY.prepare('DELETE FROM dore_messages WHERE conversation_id=?1 AND project_id=?2').bind(conversation,project).run();
    await env.DORE_SENSORY.prepare('DELETE FROM dore_conversations WHERE id=?1 AND project_id=?2').bind(conversation,project).run();
    return json({ok:pass,stage:'M5',milestone:pass?'M5_MEMORY_AWARE_RESPONSE_PASS':'M5_MEMORY_AWARE_RESPONSE_FAIL',bindings,checks:{remembered_decision:remembered,distractor_excluded:avoidedDistractor,semantic_memory_used:semanticUsed,scope_isolation:scoped,response_model:modelBound,cleanup:true},answer,memory:result?.memory||null,contract:result?.contract||null,next:pass?'M6_CROSS_CONVERSATION_MEMORY':'M5_REPAIR'});
  }catch(e){
    try{if(ids.length)await env.DORE_MEMORY_VECTOR.deleteByIds(ids)}catch{}
    for(const key of archives)try{if(key)await env.DORE_MEMORY_ARCHIVE.delete(key)}catch{}
    try{await env.DORE_SENSORY.prepare('DELETE FROM dore_messages WHERE conversation_id=?1 AND project_id=?2').bind(conversation,project).run();await env.DORE_SENSORY.prepare('DELETE FROM dore_conversations WHERE id=?1 AND project_id=?2').bind(conversation,project).run()}catch{}
    return json({ok:false,stage:'M5',bindings,error:String(e?.message||e)},500);
  }
}
