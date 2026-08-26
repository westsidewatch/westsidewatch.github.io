const json=(data,status=200)=>new Response(JSON.stringify(data),{status,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store'}});
export async function onRequestGet({env}){
  return json({ok:true,bridge:'dore.penpot.mcp.v0.1',secret_bound:Boolean(String(env?.PENPOT_MCP_KEY||'').trim())});
}
