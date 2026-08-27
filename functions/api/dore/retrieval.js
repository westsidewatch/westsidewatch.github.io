const json=(data,status=200)=>new Response(JSON.stringify(data),{status,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store'}});
const clean=(value,max=12000)=>String(value??'').normalize('NFKC').trim().slice(0,max);
const safeId=(value,fallback='')=>clean(value,160).replace(/[^a-zA-Z0-9._:-]/g,'-')||fallback;
const ns=(project,conversation)=>`${project}::${conversation}`.slice(0,64);
const EMBEDDING_MODEL='@cf/baai/bge-small-en-v1.5';

async function embed(env,text){
  if(!env.AI)throw new Error('ai_unbound');
  const r=await env.AI.run(EMBEDDING_MODEL,{text:[text]});
  const vector=r?.data?.[0];
  if(!Array.isArray(vector)||vector.length!==384)throw new Error('embedding_response_invalid');
  return vector;
}

async function semanticMessages(env,{projectId,conversationId,query,topK=6,minScore=0.45}){
  if(!env.DORE_MEMORY_VECTOR)throw new Error('memory_vector_unbound');
  const vector=await embed(env,query);
  const result=await env.DORE_MEMORY_VECTOR.query(vector,{topK,namespace:ns(projectId,conversationId),returnMetadata:'all'});
  return (result?.matches||[])
    .filter(m=>Number(m?.score||0)>=minScore&&m?.metadata?.kind==='conversation_message')
    .map(m=>({id:m.id,score:Number(m.score||0),metadata:m.metadata||{}}));
}

async function recentMessages(env,{projectId,conversationId,limit=8}){
  if(!env.DORE_SENSORY)throw new Error('memory_db_unbound');
  const result=await env.DORE_SENSORY.prepare('SELECT id,conversation_id,project_id,actor_id,role,content,archive_key,created_at FROM dore_messages WHERE conversation_id=?1 AND project_id=?2 ORDER BY created_at DESC,id DESC LIMIT ?3').bind(conversationId,projectId,limit).all();
  return result?.results||[];
}

async function hydrateSemantic(env,hits){
  if(!hits.length)return [];
  const out=[];
  for(const hit of hits){
    const key=hit.metadata?.archive_key;
    let archived=null;
    if(key&&env.DORE_MEMORY_ARCHIVE){
      try{const obj=await env.DORE_MEMORY_ARCHIVE.get(key);if(obj)archived=JSON.parse(await obj.text())}catch{}
    }
    if(archived?.content){
      out.push({id:hit.id,conversation_id:archived.conversation_id,project_id:archived.project_id,actor_id:archived.actor_id,role:archived.role,content:archived.content,archive_key:key,created_at:archived.created_at,semantic_score:hit.score,source:'semantic_archive'});
      continue;
    }
    const row=await env.DORE_SENSORY.prepare('SELECT id,conversation_id,project_id,actor_id,role,content,archive_key,created_at FROM dore_messages WHERE id=?1 LIMIT 1').bind(hit.id).first();
    if(row)out.push({...row,semantic_score:hit.score,source:'semantic_d1'});
  }
  return out;
}

function assemble({semantic,recent,maxChars=9000}){
  const byId=new Map();
  for(const item of semantic)byId.set(item.id,{...item,semantic:true,recent:false});
  for(const item of recent){
    const prev=byId.get(item.id);
    byId.set(item.id,prev?{...prev,recent:true}:{...item,semantic_score:null,source:'recent_d1',semantic:false,recent:true});
  }
  const ranked=[...byId.values()].sort((a,b)=>{
    const as=Number(a.semantic_score||0),bs=Number(b.semantic_score||0);
    if(bs!==as)return bs-as;
    return String(b.created_at||'').localeCompare(String(a.created_at||''));
  });
  const selected=[];let used=0;
  for(const item of ranked){
    const cost=(item.content||'').length+120;
    if(selected.length&&used+cost>maxChars)continue;
    selected.push(item);used+=cost;
  }
  selected.sort((a,b)=>String(a.created_at||'').localeCompare(String(b.created_at||''))||String(a.id).localeCompare(String(b.id)));
  return {messages:selected,used_chars:used};
}

export async function retrieveContext(env,input={}){
  const projectId=safeId(input.project_id,'unscoped');
  const conversationId=safeId(input.conversation_id);
  const query=clean(input.query,4000);
  if(!conversationId)throw new Error('missing_conversation_id');
  if(!query)throw new Error('empty_query');
  const topK=Math.max(1,Math.min(12,Number(input.top_k||6)));
  const recentLimit=Math.max(0,Math.min(20,Number(input.recent_limit??6)));
  const minScore=Math.max(0,Math.min(1,Number(input.min_score??0.45)));
  const maxChars=Math.max(1000,Math.min(24000,Number(input.max_chars||9000)));
  const [hits,recent]=await Promise.all([
    semanticMessages(env,{projectId,conversationId,query,topK,minScore}),
    recentLimit?recentMessages(env,{projectId,conversationId,limit:recentLimit}):Promise.resolve([])
  ]);
  const semantic=await hydrateSemantic(env,hits);
  const assembled=assemble({semantic,recent,maxChars});
  return {ok:true,stage:'M4',scope:{project_id:projectId,conversation_id:conversationId},query,retrieval:{semantic_hits:semantic.length,recent_hits:recent.length,min_score:minScore,top_k:topK},context:{messages:assembled.messages,used_chars:assembled.used_chars,max_chars:maxChars},contract:{schema:'dore.retrieval-context.v1',embedding_model:EMBEDDING_MODEL,namespace:ns(projectId,conversationId)}};
}

export async function onRequestPost({request,env}){
  let body;try{body=await request.json()}catch{return json({ok:false,error:'invalid_json'},400)}
  try{return json(await retrieveContext(env,body))}catch(error){
    const detail=String(error?.message||error);
    const status=['missing_conversation_id','empty_query'].includes(detail)?400:detail.endsWith('_unbound')?503:500;
    return json({ok:false,error:'memory_retrieval_failed',detail},status);
  }
}
