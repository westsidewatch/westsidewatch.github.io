import {ingestMessage} from './memory.js';
import {generateMemoryAwareResponse} from './respond.js';

const json=(data,status=200)=>new Response(JSON.stringify(data),{status,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store'}});
const clean=(v,max=12000)=>String(v??'').normalize('NFKC').trim().slice(0,max);
const safeId=(v,f='')=>clean(v,160).replace(/[^a-zA-Z0-9._:-]/g,'-')||f;
const newId=()=>typeof crypto.randomUUID==='function'?crypto.randomUUID():`${Date.now().toString(36)}-${Math.random().toString(36).slice(2)}`;

export async function onRequestPost({request,env}){
 let body;try{body=await request.json()}catch{return json({ok:false,error:'invalid_json'},400)}
 const query=clean(body?.query,4000);if(!query)return json({ok:false,error:'query_required'},400);
 const projectId=safeId(body?.project_id,'dore-search');
 const conversationId=safeId(body?.conversation_id)||newId();
 const actorId=safeId(body?.actor_id,'public');
 try{
  const user=await ingestMessage(env,{project_id:projectId,conversation_id:conversationId,actor_id:actorId,role:'user',content:query,mode:'CONVERSATION_BETA',title:clean(body?.title,240)||query.slice(0,80)});
  const response=await generateMemoryAwareResponse(env,{project_id:projectId,conversation_id:conversationId,query,top_k:body?.top_k,recent_limit:body?.recent_limit,min_score:body?.min_score,max_chars:body?.max_chars});
  const assistant=await ingestMessage(env,{project_id:projectId,conversation_id:conversationId,actor_id:'dore',role:'assistant',content:response.answer,mode:'CONVERSATION_BETA'});
  return json({ok:true,schema:'dore.conversation.v1',conversation_id:conversationId,project_id:projectId,answer:response.answer,memory:response.memory,persistence:{user_message_id:user.message_id,assistant_message_id:assistant.message_id,user_deduplicated:user.deduplicated,assistant_deduplicated:assistant.deduplicated}});
 }catch(error){const detail=String(error?.message||error);const status=detail.endsWith('_unbound')?503:500;return json({ok:false,error:'conversation_failed',detail,conversation_id:conversationId,project_id:projectId},status)}
}
