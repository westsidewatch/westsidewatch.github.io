const json=(data,status=200)=>new Response(JSON.stringify(data),{status,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store'}});
const authorized=(request,env)=>{const h=request.headers.get('authorization')||'';return Boolean(env.DORE_HEARTBEAT_TOKEN)&&h===`Bearer ${env.DORE_HEARTBEAT_TOKEN}`};

function endpoint(env){
  const key=String(env?.PENPOT_MCP_KEY||'').trim();
  if(!key)return null;
  return `https://design.penpot.app/mcp/stream?userToken=${encodeURIComponent(key)}`;
}

function parseSse(text){
  const out=[];
  for(const block of String(text||'').split(/\n\n+/)){
    const data=block.split(/\n/).filter(line=>line.startsWith('data:')).map(line=>line.slice(5).trim()).join('\n');
    if(!data)continue;
    try{out.push(JSON.parse(data))}catch{}
  }
  return out;
}

async function rpc(url,payload,sessionId){
  const headers={
    'content-type':'application/json',
    'accept':'application/json, text/event-stream'
  };
  if(sessionId)headers['Mcp-Session-Id']=sessionId;
  const response=await fetch(url,{method:'POST',headers,body:JSON.stringify(payload)});
  const text=await response.text();
  const returnedSession=response.headers.get('Mcp-Session-Id')||response.headers.get('mcp-session-id')||sessionId||null;
  let body=null;
  const type=response.headers.get('content-type')||'';
  if(type.includes('application/json')){
    try{body=JSON.parse(text)}catch{}
  }else if(type.includes('text/event-stream')){
    const events=parseSse(text);
    body=events.find(x=>x?.id===payload?.id)||events[events.length-1]||null;
  }else{
    try{body=JSON.parse(text)}catch{}
  }
  return {ok:response.ok,status:response.status,body,sessionId:returnedSession,contentType:type};
}

async function notifyInitialized(url,sessionId){
  const headers={'content-type':'application/json','accept':'application/json, text/event-stream'};
  if(sessionId)headers['Mcp-Session-Id']=sessionId;
  const response=await fetch(url,{method:'POST',headers,body:JSON.stringify({jsonrpc:'2.0',method:'notifications/initialized'})});
  return {ok:response.ok,status:response.status};
}

export async function onRequestGet({request,env}){
  if(!authorized(request,env))return json({ok:false,error:'unauthorized'},401);
  const url=endpoint(env);
  if(!url)return json({ok:false,error:'penpot_mcp_secret_unbound'},503);

  try{
    const init=await rpc(url,{
      jsonrpc:'2.0',
      id:1,
      method:'initialize',
      params:{
        protocolVersion:'2025-03-26',
        capabilities:{},
        clientInfo:{name:'dore-penpot-bridge',version:'0.1.0'}
      }
    });

    if(!init.ok||!init.body||init.body.error){
      return json({
        ok:false,
        stage:'initialize',
        error:init.body?.error?.message||'penpot_mcp_initialize_failed',
        upstream_status:init.status,
        content_type:init.contentType||null
      },502);
    }

    const sessionId=init.sessionId;
    await notifyInitialized(url,sessionId).catch(()=>null);

    const tools=await rpc(url,{jsonrpc:'2.0',id:2,method:'tools/list',params:{}},sessionId);
    if(!tools.ok||!tools.body||tools.body.error){
      return json({
        ok:false,
        stage:'tools/list',
        error:tools.body?.error?.message||'penpot_mcp_tools_list_failed',
        upstream_status:tools.status
      },502);
    }

    const list=Array.isArray(tools.body?.result?.tools)?tools.body.result.tools:[];
    return json({
      ok:true,
      bridge:'dore.penpot.mcp.v0.1',
      protocol_version:init.body?.result?.protocolVersion||null,
      server_info:init.body?.result?.serverInfo||null,
      tool_count:list.length,
      tools:list.map(tool=>({name:String(tool?.name||''),description:String(tool?.description||'').slice(0,280)}))
    });
  }catch(error){
    return json({ok:false,stage:'transport',error:'penpot_mcp_transport_failed',detail:String(error?.message||error)},502);
  }
}
