const clean=(v,max=24000)=>String(v??'').normalize('NFKC').trim().slice(0,max);
export const DEFAULT_WORKERS_AI_MODEL='@cf/zai-org/glm-4.7-flash';

function answerText(out={}){
  if(typeof out?.response==='string')return clean(out.response);
  const c=out?.choices?.[0]?.message?.content;
  return clean(c);
}

export async function createWorkersAIResponse(env,{system='',prompt='',max_tokens=700}={}){
  if(!env?.AI?.run)throw new Error('workers_ai_binding_unbound');
  const model=clean(env?.DORE_WORKERS_AI_MODEL,180)||DEFAULT_WORKERS_AI_MODEL;
  const out=await env.AI.run(model,{
    messages:[
      {role:'system',content:clean(system,12000)},
      {role:'user',content:clean(prompt,22000)}
    ],
    max_completion_tokens:Math.max(128,Math.min(900,Number(max_tokens)||700)),
    reasoning_effort:'low',
    chat_template_kwargs:{enable_thinking:false}
  });
  const answer=answerText(out);
  if(!answer)throw new Error('workers_ai_empty_response');
  return {answer,provider:'cloudflare-workers-ai',model};
}
