const json=(d,s=200)=>new Response(JSON.stringify(d),{status:s,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store'}});
const auth=(r,e)=>Boolean(e.DORE_HEARTBEAT_TOKEN)&&(r.headers.get('authorization')||'')===`Bearer ${e.DORE_HEARTBEAT_TOKEN}`;
const ns=(project,conversation)=>`${project}::${conversation}`.slice(0,64);
async function embed(env,texts){const r=await env.AI.run('@cf/baai/bge-small-en-v1.5',{text:texts});if(!r?.data||!Array.isArray(r.data))throw new Error('embedding_response_invalid');return r.data;}
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function waitForQuery(env,vector,namespace,expectedId){let last=null;for(let i=0;i<12;i++){last=await env.DORE_MEMORY_VECTOR.query(vector,{topK:3,namespace,returnMetadata:'all'});if(last?.matches?.some(m=>m?.id===expectedId))return last;await sleep(5000);}return last;}
export async function onRequestPost({request,env}){
  if(!auth(request,env))return json({ok:false,error:'unauthorized'},401);
  const bindings={d1:Boolean(env.DORE_SENSORY),vectorize:Boolean(env.DORE_MEMORY_VECTOR),archive:Boolean(env.DORE_MEMORY_ARCHIVE),ai:Boolean(env.AI)};
  if(!env.DORE_MEMORY_VECTOR||!env.AI)return json({ok:false,stage:'M2',bindings,error:'m2_binding_missing',required:['DORE_MEMORY_VECTOR','AI']},503);
  const run=crypto.randomUUID();const project='full-memory-phase1-m2';const a='alpha-'+run,b='beta-'+run;const na=ns(project,a),nb=ns(project,b);
  const alpha='The watchman placed a brass lamp beside the eastern gate before dawn.';
  const beta='The gardener stored a cedar spade beneath the western greenhouse bench.';
  try{
    const [va,vb]=await embed(env,[alpha,beta]);
    if(va.length!==384||vb.length!==384)throw new Error(`unexpected_embedding_dimensions:${va.length}/${vb.length}`);
    const ida=`m2-a-${run}`,idb=`m2-b-${run}`;
    await env.DORE_MEMORY_VECTOR.upsert([
      {id:ida,values:va,namespace:na,metadata:{project_id:project,conversation_id:a,role:'user',kind:'diagnostic'}},
      {id:idb,values:vb,namespace:nb,metadata:{project_id:project,conversation_id:b,role:'user',kind:'diagnostic'}}
    ]);
    const [qa]=await embed(env,['Which memory mentions a lamp near a gate at sunrise?']);
    const [qb]=await embed(env,['Which memory talks about a gardening tool under a greenhouse bench?']);
    const [ra,rb]=await Promise.all([
      waitForQuery(env,qa,na,ida),
      waitForQuery(env,qb,nb,idb)
    ]);
    const crossA=await env.DORE_MEMORY_VECTOR.query(qb,{topK:3,namespace:na,returnMetadata:'all'});
    const crossB=await env.DORE_MEMORY_VECTOR.query(qa,{topK:3,namespace:nb,returnMetadata:'all'});
    const topA=ra?.matches?.find(m=>m?.id===ida)||ra?.matches?.[0]||null,topB=rb?.matches?.find(m=>m?.id===idb)||rb?.matches?.[0]||null,topCrossA=crossA?.matches?.[0]||null,topCrossB=crossB?.matches?.[0]||null;
    const scoped=topA?.id===ida&&topB?.id===idb&&topCrossA?.id===ida&&topCrossB?.id===idb;
    const semantic=Number(topA?.score||0)>0.45&&Number(topB?.score||0)>0.45;
    const pass=scoped&&semantic;
    try{await env.DORE_MEMORY_VECTOR.deleteByIds([ida,idb])}catch{}
    return json({ok:pass,stage:'M2',milestone:pass?'M2_VECTOR_SEMANTIC_SCOPE_PASS':'M2_VECTOR_SEMANTIC_SCOPE_FAIL',bindings,model:'@cf/baai/bge-small-en-v1.5',dimensions:384,checks:{embedding:true,upsert:true,namespace_scope:scoped,semantic_recall:semantic,alpha:{id:topA?.id||null,score:topA?.score||null},beta:{id:topB?.id||null,score:topB?.score||null},cross_alpha_namespace:{id:topCrossA?.id||null,score:topCrossA?.score||null},cross_beta_namespace:{id:topCrossB?.id||null,score:topCrossB?.score||null},cleanup:true},next:pass?'M3_CONVERSATION_INGESTION':'M2_REPAIR'})
  }catch(e){return json({ok:false,stage:'M2',bindings,error:String(e?.message||e)},500)}
}
