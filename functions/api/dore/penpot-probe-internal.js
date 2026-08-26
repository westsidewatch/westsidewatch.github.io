const json=(data,status=200)=>new Response(JSON.stringify(data),{status,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store'}});
function parseSse(text){const out=[];for(const block of String(text||'').split(/\n\n+/)){const data=block.split(/\n/).filter(l=>l.startsWith('data:')).map(l=>l.slice(5).trim()).join('\n');if(!data)continue;try{out.push(JSON.parse(data))}catch{}}return out}
async function rpc(url,payload,sessionId){const headers={'content-type':'application/json','accept':'application/json, text/event-stream'};if(sessionId)headers['Mcp-Session-Id']=sessionId;const r=await fetch(url,{method:'POST',headers,body:JSON.stringify(payload)});const text=await r.text();const sid=r.headers.get('Mcp-Session-Id')||r.headers.get('mcp-session-id')||sessionId||null;let body=null;const type=r.headers.get('content-type')||'';try{body=type.includes('text/event-stream')?(parseSse(text).find(x=>x?.id===payload?.id)||parseSse(text).at(-1)||null):JSON.parse(text)}catch{}return {ok:r.ok,status:r.status,body,sessionId:sid}}
export async function onRequestGet({request,env}){
  const u=new URL(request.url);const proof=u.searchParams.get('proof')||'';
  const expected=String(env?.PENPOT_PROBE_PROOF||'').trim();
  if(!expected||proof!==expected)return json({ok:false,error:'not_found'},404);
  const key=String(env?.PENPOT_MCP_KEY||'').trim();if(!key)return json({ok:false,error:'penpot_mcp_secret_unbound'},503);
  const url=`https://design.penpot.app/mcp/stream?userToken=${encodeURIComponent(key)}`;
  const init=await rpc(url,{jsonrpc:'2.0',id:1,method:'initialize',params:{protocolVersion:'2025-03-26',capabilities:{},clientInfo:{name:'dore-penpot-bridge',version:'0.1.0'}}});
  if(!init.ok||!init.body||init.body.error)return json({ok:false,stage:'initialize',upstream_status:init.status,error:init.body?.error?.message||'initialize_failed'},502);
  await fetch(url,{method:'POST',headers:{'content-type':'application/json','accept':'application/json, text/event-stream',...(init.sessionId?{'Mcp-Session-Id':init.sessionId}:{})},body:JSON.stringify({jsonrpc:'2.0',method:'notifications/initialized'})}).catch(()=>null);
  const tools=await rpc(url,{jsonrpc:'2.0',id:2,method:'tools/list',params:{}},init.sessionId);
  if(!tools.ok||!tools.body||tools.body.error)return json({ok:false,stage:'tools/list',upstream_status:tools.status,error:tools.body?.error?.message||'tools_list_failed'},502);
  const list=Array.isArray(tools.body?.result?.tools)?tools.body.result.tools:[];
  return json({ok:true,bridge:'dore.penpot.mcp.v0.1',protocol_version:init.body?.result?.protocolVersion||null,server_info:init.body?.result?.serverInfo||null,tool_count:list.length,tool_names:list.map(t=>String(t?.name||''))});
}
