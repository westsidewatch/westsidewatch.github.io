import {ingestMessage} from './memory.js';
import {retrieveContext} from './retrieval.js';
const json=(d,s=200)=>new Response(JSON.stringify(d),{status:s,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store'}});
const auth=(r,e)=>Boolean(e.DORE_HEARTBEAT_TOKEN)&&(r.headers.get('authorization')||'')===`Bearer ${e.DORE_HEARTBEAT_TOKEN}`;
const sleep=ms=>new Promise(r=>setTimeout(r,ms));

export async function onRequestPost({request,env}){
  if(!auth(request,env))return json({ok:false,error:'unauthorized'},401);
  const bindings={d1:Boolean(env.DORE_SENSORY),vectorize:Boolean(env.DORE_MEMORY_VECTOR),archive:Boolean(env.DORE_MEMORY_ARCHIVE),ai:Boolean(env.AI)};
  if(!bindings.d1||!bindings.vectorize||!bindings.archive||!bindings.ai)return json({ok:false,stage:'M4',bindings,error:'m4_binding_missing'},503);
  const run=crypto.randomUUID(),project='full-memory-phase1-m4',conversation='conversation-'+run;
  const facts={
    preference:`For the ${run} research notebook, the reader decided that all chapter maps should use bilingual Chinese-English labels.`,
    distractor:`The ${run} test also mentioned that a brass desk lamp was switched off before lunch.`,
    continuation:`Later in ${run}, the reader asked Doré to keep the map-label decision available for future chapter work.`,
    assistant:`Doré acknowledged ${run} and kept the decision inside the same conversation memory scope.`
  };
  const ids=[],archives=[];
  try{
    for(const [role,content] of [['user',facts.preference],['user',facts.distractor],['user',facts.continuation],['assistant',facts.assistant]]){
      const x=await ingestMessage(env,{project_id:project,conversation_id:conversation,actor_id:role==='assistant'?'dore':'diagnostic-user',role,content,title:'M4 diagnostic'});
      ids.push(x.message_id);archives.push(x.archive_key);
    }
    await sleep(35000);
    const result=await retrieveContext(env,{project_id:project,conversation_id:conversation,query:'What label format did the reader choose for chapter maps?',top_k:6,recent_limit:2,min_score:0.35,max_chars:5000});
    const messages=result?.context?.messages||[];
    const target=messages.find(m=>m.content===facts.preference)||null;
    const recentContinuation=messages.some(m=>m.content===facts.continuation||m.content===facts.assistant);
    const semanticTarget=Boolean(target?.semantic)&&Number(target?.semantic_score||0)>0;
    const archiveHydration=Boolean(target?.source==='semantic_archive');
    const scoped=messages.every(m=>m.project_id===project&&m.conversation_id===conversation);
    const deduplicated=new Set(messages.map(m=>m.id)).size===messages.length;
    const budget=Number(result?.context?.used_chars||0)<=Number(result?.context?.max_chars||0);
    const answerable=messages.some(m=>/bilingual Chinese-English labels/i.test(m.content||''));
    const pass=semanticTarget&&archiveHydration&&recentContinuation&&scoped&&deduplicated&&budget&&answerable;
    await env.DORE_MEMORY_VECTOR.deleteByIds(ids);
    for(const key of archives)if(key)await env.DORE_MEMORY_ARCHIVE.delete(key);
    await env.DORE_SENSORY.prepare('DELETE FROM dore_messages WHERE conversation_id=?1 AND project_id=?2').bind(conversation,project).run();
    await env.DORE_SENSORY.prepare('DELETE FROM dore_conversations WHERE id=?1 AND project_id=?2').bind(conversation,project).run();
    return json({ok:pass,stage:'M4',milestone:pass?'M4_RETRIEVAL_CONTEXT_ASSEMBLY_PASS':'M4_RETRIEVAL_CONTEXT_ASSEMBLY_FAIL',bindings,checks:{semantic_target:semanticTarget,archive_hydration:archiveHydration,recent_continuity:recentContinuation,scope_isolation:scoped,deduplicated,budget_respected:budget,answerable_from_context:answerable,target_score:target?.semantic_score||null,context_messages:messages.length,cleanup:true},contract:result.contract,next:pass?'M5_MEMORY_AWARE_RESPONSE':'M4_REPAIR'});
  }catch(e){
    try{if(ids.length)await env.DORE_MEMORY_VECTOR.deleteByIds(ids)}catch{}
    for(const key of archives)try{if(key)await env.DORE_MEMORY_ARCHIVE.delete(key)}catch{}
    try{await env.DORE_SENSORY.prepare('DELETE FROM dore_messages WHERE conversation_id=?1 AND project_id=?2').bind(conversation,project).run();await env.DORE_SENSORY.prepare('DELETE FROM dore_conversations WHERE id=?1 AND project_id=?2').bind(conversation,project).run()}catch{}
    return json({ok:false,stage:'M4',bindings,error:String(e?.message||e)},500);
  }
}
