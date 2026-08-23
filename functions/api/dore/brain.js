const allowedOrigin=o=>o==='https://westsidewatch.github.io'||/^https:\/\/[a-z0-9-]+\.westsidewatch-github-io\.pages\.dev$/i.test(o||'');
const corsHeaders=request=>{const origin=request.headers.get('origin')||'';return allowedOrigin(origin)?{'access-control-allow-origin':origin,'vary':'Origin','access-control-allow-methods':'GET,OPTIONS','access-control-allow-headers':'content-type'}:{}};
const json=(request,data,status=200)=>new Response(JSON.stringify(data),{status,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store',...corsHeaders(request)}});

export async function onRequestOptions({request}){return new Response(null,{status:204,headers:corsHeaders(request)})}
export async function onRequestGet({request}){
  const source='https://raw.githubusercontent.com/westsidewatch/westsidewatch.github.io/main/static/dore/brain/knowledge-index.json';
  const r=await fetch(source,{headers:{'accept':'application/json'},cf:{cacheTtl:0,cacheEverything:false}});
  if(!r.ok)return json(request,{ok:false,error:'brain_source_unavailable',status:r.status},502);
  const body=await r.text();
  return new Response(body,{status:200,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store',...corsHeaders(request)}});
}
