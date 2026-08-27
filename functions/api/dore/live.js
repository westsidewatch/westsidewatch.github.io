import {ingestMessage} from './memory.js';
import {generateMemoryAwareResponse} from './respond.js';

const json=(data,status=200)=>new Response(JSON.stringify(data),{status,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store'}});
const clean=(v,max=12000)=>String(v??'').normalize('NFKC').trim().slice(0,max);
const safeId=(v,f='')=>clean(v,160).replace(/[^a-zA-Z0-9._:-]/g,'-')||f;

/**
 * Canonical Doré live-conversation turn.
 * A caller sends only the current user turn. The endpoint itself persists the
 * user turn, retrieves prior memory, generates Doré's answer, then persists
 * that answer. No separate "remember" call is required.
 */
export async function runLiveTurn(env,input={}){
  const projectId=safeId(input.project_id,'dore-live');
  const conversationId=safeId(input.conversation_id);
  const actorId=safeId(input.actor_id,'user');
  const content=clean(input.content||input.query,12000);
  if(!conversationId)throw new Error('missing_conversation_id');
  if(!content)throw new Error('empty_content');

  const userMemory=await ingestMessage(env,{
    project_id:projectId,
    conversation_id:conversationId,
    actor_id:actorId,
    role:'user',
    content,
    title:clean(input.title,240)||null,
    mode:'LIVE_MEMORY'
  });

  const response=await generateMemoryAwareResponse(env,{
    project_id:projectId,
    conversation_id:conversationId,
    query:content,
    top_k:input.top_k??8,
    recent_limit:input.recent_limit??8,
    min_score:input.min_score??0.35,
    max_chars:input.max_chars??12000
  });

  const assistantMemory=await ingestMessage(env,{
    project_id:projectId,
    conversation_id:conversationId,
    actor_id:'dore',
    role:'assistant',
    content:response.answer,
    title:clean(input.title,240)||null,
    mode:'LIVE_MEMORY'
  });

  return {
    ok:true,
    answer:response.answer,
    conversation_id:conversationId,
    project_id:projectId,
    memory:{
      automatic:true,
      user_persisted:Boolean(userMemory?.ok),
      assistant_persisted:Boolean(assistantMemory?.ok),
      retrieval_used:Boolean(response?.memory?.used),
      retrieval_count:response?.memory?.count??0,
      user_message_id:userMemory?.message_id||null,
      assistant_message_id:assistantMemory?.message_id||null
    },
    contract:{schema:'dore.live-memory.v1',rule:'every live turn persists user and assistant automatically'}
  };
}

export async function onRequestPost({request,env}){
  let body;try{body=await request.json()}catch{return json({ok:false,error:'invalid_json'},400)}
  try{return json(await runLiveTurn(env,body),201)}catch(error){
    const detail=String(error?.message||error);
    const status=['missing_conversation_id','empty_content'].includes(detail)?400:detail.endsWith('_unbound')?503:500;
    return json({ok:false,error:'live_memory_turn_failed',detail},status);
  }
}
