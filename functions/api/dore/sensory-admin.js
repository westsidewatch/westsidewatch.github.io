const json=(data,status=200)=>new Response(JSON.stringify(data),{status,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store'}});
const authorized=(request,env)=>{const h=request.headers.get('authorization')||'';return Boolean(env.DORE_HEARTBEAT_TOKEN)&&h===`Bearer ${env.DORE_HEARTBEAT_TOKEN}`};
export async function onRequestGet({request,env}){
  if(!authorized(request,env))return json({ok:false,error:'unauthorized'},401);
  if(!env.DORE_SENSORY)return json({ok:false,error:'sensory_memory_unbound'},503);
  const row=await env.DORE_SENSORY.prepare("SELECT id,query,state,heard_count,first_heard_at,last_heard_at,updated_at FROM sensory_signals WHERE state IN ('QUEUED','RESEARCHING','WORKING','CANDIDATE_FOR_EXAM','REOPENED') ORDER BY CASE state WHEN 'QUEUED' THEN 0 WHEN 'REOPENED' THEN 1 ELSE 2 END, heard_count DESC, first_heard_at ASC LIMIT 1").first();
  return json({ok:true,signal:row||null});
}
export async function onRequestPatch({request,env}){
  if(!authorized(request,env))return json({ok:false,error:'unauthorized'},401);
  if(!env.DORE_SENSORY)return json({ok:false,error:'sensory_memory_unbound'},503);
  let body;try{body=await request.json()}catch{return json({ok:false,error:'invalid_json'},400)}
  const id=String(body?.signal_id||'');
  const allowed=new Set(['RESEARCHING','WORKING','CANDIDATE_FOR_EXAM','CONSOLIDATED','DISPUTED','REOPENED','REJECTED']);
  const next=String(body?.state||'');
  if(!id||!allowed.has(next))return json({ok:false,error:'invalid_transition'},400);
  const now=new Date().toISOString();
  await env.DORE_SENSORY.prepare('UPDATE sensory_signals SET state=?1,research_task=COALESCE(?2,research_task),brain_node=COALESCE(?3,brain_node),error=?4,updated_at=?5 WHERE id=?6').bind(next,body?.research_task||null,body?.brain_node||null,body?.error||null,now,id).run();
  return json({ok:true,signal_id:id,state:next,updated_at:now});
}
