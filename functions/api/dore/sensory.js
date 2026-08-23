const json=(data,status=200)=>new Response(JSON.stringify(data),{status,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store'}});
const normalize=q=>String(q||'').normalize('NFKC').trim().replace(/\s+/g,' ').slice(0,600);
const fingerprint=async q=>{const bytes=new TextEncoder().encode(q.toLowerCase());const digest=await crypto.subtle.digest('SHA-256',bytes);return [...new Uint8Array(digest)].map(b=>b.toString(16).padStart(2,'0')).join('')};

export async function onRequestPost({request,env}){
  if(!env.DORE_SENSORY)return json({ok:false,error:'sensory_memory_unbound'},503);
  let body;try{body=await request.json()}catch{return json({ok:false,error:'invalid_json'},400)}
  const query=normalize(body?.query);
  if(query.length<2)return json({ok:false,error:'query_too_short'},400);
  const fp=await fingerprint(query);
  const now=new Date().toISOString();
  const id=crypto.randomUUID();
  const existing=await env.DORE_SENSORY.prepare('SELECT id,state,heard_count FROM sensory_signals WHERE fingerprint=?1 LIMIT 1').bind(fp).first();
  if(existing){
    await env.DORE_SENSORY.prepare('UPDATE sensory_signals SET heard_count=heard_count+1,last_heard_at=?1 WHERE id=?2').bind(now,existing.id).run();
    return json({ok:true,signal_id:existing.id,state:existing.state,heard_count:Number(existing.heard_count||1)+1,deduplicated:true});
  }
  await env.DORE_SENSORY.prepare(`INSERT INTO sensory_signals (id,fingerprint,query,state,heard_count,first_heard_at,last_heard_at,updated_at) VALUES (?1,?2,?3,'QUEUED',1,?4,?4,?4)`).bind(id,fp,query,now).run();
  return json({ok:true,signal_id:id,state:'QUEUED',heard_count:1,deduplicated:false},201);
}

export async function onRequestGet({request,env}){
  if(!env.DORE_SENSORY)return json({ok:false,error:'sensory_memory_unbound'},503);
  const url=new URL(request.url);
  const id=url.searchParams.get('id');
  if(!id)return json({ok:false,error:'missing_id'},400);
  const row=await env.DORE_SENSORY.prepare('SELECT id,state,brain_node,updated_at FROM sensory_signals WHERE id=?1 LIMIT 1').bind(id).first();
  if(!row)return json({ok:false,error:'not_found'},404);
  return json({ok:true,signal_id:row.id,state:row.state,brain_node:row.brain_node||null,updated_at:row.updated_at});
}
