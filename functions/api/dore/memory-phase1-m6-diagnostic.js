import {ingestProjectMemory,generateCrossConversationResponse} from './cross-memory.js';
const json=(d,s=200)=>new Response(JSON.stringify(d),{status:s,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store'}});
const auth=(r,e)=>Boolean(e.DORE_HEARTBEAT_TOKEN)&&(r.headers.get('authorization')||'')===`Bearer ${e.DORE_HEARTBEAT_TOKEN}`;
const sleep=ms=>new Promise(r=>setTimeout(r,ms));

export async function onRequestPost({request,env}){
  if(!auth(request,env))return json({ok:false,error:'unauthorized'},401);
  const bindings={d1:Boolean(env.DORE_SENSORY),vectorize:Boolean(env.DORE_MEMORY_VECTOR),archive:Boolean(env.DORE_MEMORY_ARCHIVE),ai:Boolean(env.AI)};
  if(!bindings.d1||!bindings.vectorize||!bindings.archive||!bindings.ai)return json({ok:false,stage:'M6',bindings,error:'m6_binding_missing'},503);
  const run=crypto.randomUUID();
  const projectA='full-memory-phase1-m6-a-'+run.slice(0,8),projectB='full-memory-phase1-m6-b-'+run.slice(0,8);
  const oldConversation='old-'+run,newConversation='new-'+run,foreignConversation='foreign-'+run;
  const target=`For ${run}, the reader decided that chapter maps must use bilingual Chinese-English labels.`;
  const foreign=`For ${run}, another unrelated project decided that chapter maps must use French-only labels.`;
  const distractor=`For ${run}, the old conversation also noted that a walnut pencil tray should stay beside the desk.`;
  const records=[];
  try{
    for(const [project,conversation,content] of [[projectA,oldConversation,target],[projectA,oldConversation,distractor],[projectB,foreignConversation,foreign]]){
      records.push(await ingestProjectMemory(env,{project_id:project,conversation_id:conversation,actor_id:'diagnostic-user',role:'user',content,title:'M6 diagnostic'}));
    }
    let result=null;
    for(let i=0;i<12;i++){
      result=await generateCrossConversationResponse(env,{project_id:projectA,conversation_id:newConversation,query:'In our earlier work, what label format did I decide to use for chapter maps?',top_k:10,min_score:0.30});
      if(/Chinese-English/i.test(result?.answer||'')&&Number(result?.memory?.count||0)>0)break;
      await sleep(5000);
    }
    const answer=result?.answer||'';
    const remembered=/bilingual/i.test(answer)&&/Chinese-English/i.test(answer);
    const foreignExcluded=!/French-only|French only/i.test(answer);
    const distractorExcluded=!/walnut pencil tray|pencil tray/i.test(answer);
    const crossedConversation=(result?.memory?.source_conversations||[]).includes(oldConversation)&&!(result?.memory?.source_conversations||[]).includes(newConversation);
    const sameProject=result?.memory?.scope?.project_id===projectA&&result?.memory?.scope?.current_conversation_id===newConversation;
    const sourceRows=(result?.memory?.source_conversations||[]).every(x=>x===oldConversation);
    const pass=remembered&&foreignExcluded&&distractorExcluded&&crossedConversation&&sameProject&&sourceRows;
    const messageIds=records.map(x=>x.message_id),projectVectorIds=records.map(x=>x.project_vector_id);
    try{await env.DORE_MEMORY_VECTOR.deleteByIds([...messageIds,...projectVectorIds])}catch{}
    for(const x of records)try{if(x.archive_key)await env.DORE_MEMORY_ARCHIVE.delete(x.archive_key)}catch{}
    await env.DORE_SENSORY.prepare('DELETE FROM dore_messages WHERE project_id IN (?1,?2)').bind(projectA,projectB).run();
    await env.DORE_SENSORY.prepare('DELETE FROM dore_conversations WHERE project_id IN (?1,?2)').bind(projectA,projectB).run();
    return json({ok:pass,stage:'M6',milestone:pass?'M6_CROSS_CONVERSATION_MEMORY_PASS':'M6_CROSS_CONVERSATION_MEMORY_FAIL',bindings,checks:{remembered_across_conversation:remembered,cross_conversation_source:crossedConversation,project_isolation:foreignExcluded&&sameProject,foreign_project_excluded:foreignExcluded,distractor_excluded:distractorExcluded,source_scope_clean:sourceRows,cleanup:true},answer,memory:result?.memory||null,contract:result?.contract||null,next:pass?'M7_MEMORY_LIFECYCLE_AND_IMPORT':'M6_REPAIR'});
  }catch(e){
    const messageIds=records.map(x=>x.message_id),projectVectorIds=records.map(x=>x.project_vector_id);
    try{if(messageIds.length||projectVectorIds.length)await env.DORE_MEMORY_VECTOR.deleteByIds([...messageIds,...projectVectorIds])}catch{}
    for(const x of records)try{if(x.archive_key)await env.DORE_MEMORY_ARCHIVE.delete(x.archive_key)}catch{}
    try{await env.DORE_SENSORY.prepare('DELETE FROM dore_messages WHERE project_id IN (?1,?2)').bind(projectA,projectB).run();await env.DORE_SENSORY.prepare('DELETE FROM dore_conversations WHERE project_id IN (?1,?2)').bind(projectA,projectB).run()}catch{}
    return json({ok:false,stage:'M6',bindings,error:String(e?.message||e)},500);
  }
}
