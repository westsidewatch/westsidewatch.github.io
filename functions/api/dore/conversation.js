import {ingestMessage} from './memory.js';
import {retrieveContext} from './retrieval.js';
import {createWorkersAIResponse} from './workers-ai-response.js';

const cors={'access-control-allow-origin':'https://westsidewatch.github.io','access-control-allow-methods':'GET, POST, OPTIONS','access-control-allow-headers':'content-type, accept','vary':'Origin'};
const json=(data,status=200)=>new Response(JSON.stringify(data),{status,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store',...cors}});
const clean=(v,max=12000)=>String(v??'').normalize('NFKC').trim().slice(0,max);
const safeId=(v,f='')=>clean(v,160).replace(/[^a-zA-Z0-9._:-]/g,'-')||f;
const newId=()=>typeof crypto.randomUUID==='function'?crypto.randomUUID():`${Date.now().toString(36)}-${Math.random().toString(36).slice(2)}`;

function memoryBlock(messages=[]){
 if(!messages.length)return '(no relevant memory retrieved)';
 return messages.map((m,i)=>`[memory ${i+1}] role=${m.role}; created_at=${m.created_at}\n${m.content}`).join('\n\n');
}

export function onRequestOptions(){return new Response(null,{status:204,headers:cors})}
export function onRequestGet({env}){
 const configured=Boolean(env?.AI?.run);
 return json({ok:configured,schema:'dore.workers-ai-readiness.v1',configured,provider:{name:'cloudflare-workers-ai'},model:clean(env?.DORE_WORKERS_AI_MODEL,180)||'@cf/zai-org/glm-4.7-flash',billing_guard:'workers-free-plan-hard-limit'},configured?200:503);
}

export async function onRequestPost({request,env}){
 let body;try{body=await request.json()}catch{return json({ok:false,error:'invalid_json'},400)}
 const query=clean(body?.query,4000);if(!query)return json({ok:false,error:'query_required'},400);
 const projectId=safeId(body?.project_id,'dore-search');
 const conversationId=safeId(body?.conversation_id)||newId();
 const actorId=safeId(body?.actor_id,'public');
 try{
  if(!env?.AI?.run)throw new Error('workers_ai_binding_unbound');
  const user=await ingestMessage(env,{project_id:projectId,conversation_id:conversationId,actor_id:actorId,role:'user',content:query,mode:'CONVERSATION_WORKERS_AI',title:clean(body?.title,240)||query.slice(0,80)});
  const retrieval=await retrieveContext(env,{project_id:projectId,conversation_id:conversationId,query,top_k:6,recent_limit:6,min_score:.35,max_chars:8000});
  const memories=retrieval?.context?.messages||[];
  const system='You are Doré. Answer in the user language. Use supplied conversation memory only when relevant. Preserve prior decisions and constraints. Do not invent remembered facts. Be concise and useful.';
  const prompt=`Conversation memory:\n${memoryBlock(memories)}\n\nCurrent user question:\n${query}`;
  const out=await createWorkersAIResponse(env,{system,prompt,max_tokens:body?.max_output_tokens||700});
  const assistant=await ingestMessage(env,{project_id:projectId,conversation_id:conversationId,actor_id:'dore',role:'assistant',content:out.answer,mode:'CONVERSATION_WORKERS_AI'});
  return json({ok:true,schema:'dore.search-workers-ai-conversation.v1',conversation_id:conversationId,project_id:projectId,answer:out.answer,memory:{used:memories.length>0,count:memories.length},provider:{name:out.provider,model:out.model},persistence:{user_message_id:user.message_id,assistant_message_id:assistant.message_id}});
 }catch(error){const detail=String(error?.message||error);const status=detail.endsWith('_unbound')?503:500;return json({ok:false,error:'conversation_failed',detail,conversation_id:conversationId,project_id:projectId},status)}
}
