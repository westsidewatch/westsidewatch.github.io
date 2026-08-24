const json=(data,status=200)=>new Response(JSON.stringify(data),{status,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store'}});
const norm=s=>String(s??'').toLowerCase().normalize('NFKC').replace(/[\s.,;:!?，。；：！？「」『』()（）\-–—_'"`]/g,'');
const assetLike=q=>/(?:封面|圖片|图片|插圖|插图|圖像|图像|資產|资产|素材|動畫|动画|gif|png|jpg|jpeg|svg|r2|cloudflare|黎明書局|黎明书局|one.*(?:圖|图|封面)|(?:圖|图|封面).*one)/iu.test(q);
const statusLike=q=>/(?:多雷|dor[eé])?.*(?:學習進度|学习进度|進度|进度|學到哪|学到哪|里程碑|狀態|状态|下一步|下一階段|下一阶段)|(?:你|多雷|dor[eé]).*(?:現在在做什麼|现在在做什么|目前在做什麼|目前在做什么)/iu.test(q);
const questionLike=q=>/[?？]/.test(q)||/(?:什麼|什么|為何|为何|為什麼|为什么|如何|怎麼|怎么|是否|是不是|有沒有|有没有|哪裡|哪里|何處|何处|誰|谁|多少|意思|解釋|解释|關係|关系|區別|区别|背景|原因|目的|代表|象徵|象征|預表|预表|嗎\s*$|吗\s*$)/u.test(q);
async function assetJson(request,path){const u=new URL(path,request.url);const r=await fetch(u.toString(),{headers:{accept:'application/json','cache-control':'no-cache'}});if(!r.ok)throw new Error(`${path} HTTP ${r.status}`);return r.json()}
function envelope(query,type,payload={},confidence=1){return{ok:true,schema:'dore.query.v1',query,type,confidence,provenance:payload.provenance||[],boundary:payload.boundary||null,...payload}}
function classify(q){if(statusLike(q))return'status';if(assetLike(q))return'asset';if(questionLike(q))return'brain';return'scripture'}
function brainMatch(brain,q){const nq=norm(q);let best=null,score=0;for(const node of brain?.nodes||[]){let s=0;for(const v of node.questions||[]){const nv=norm(v);if(nv===nq)s=100;else if(nv&&(nq.includes(nv)||nv.includes(nq)))s=Math.max(s,82)}let hits=0;for(const c of node.concepts||[]){const nc=norm(c);if(nc&&nq.includes(nc))hits++}if(hits>=2)s=Math.max(s,72+Math.min(12,hits*3));if(s>score){score=s;best=node}}return score>=70?{node:best,score}:null}
export async function onRequestGet({request,env}){
 const u=new URL(request.url),q=(u.searchParams.get('q')||'').trim();if(!q)return json({ok:false,error:'query_required'},400);
 const requested=(u.searchParams.get('type')||'auto').toLowerCase(),type=requested==='auto'?classify(q):requested;
 try{
  if(type==='status')return json(envelope(q,'status',{delegated:true,endpoint:'/dore/status/current.json',provenance:['dore-status']},1));
  if(type==='asset')return json(envelope(q,'asset',{delegated:true,endpoint:`/api/dore/assets/search?q=${encodeURIComponent(q)}`,provenance:['d1.asset_registry']},1));
  if(type==='brain'){
   const brain=await assetJson(request,'/dore/brain/knowledge-index.json'),hit=brainMatch(brain,q);
   if(hit)return json(envelope(q,'brain',{results:[hit.node],provenance:['dore.brain.knowledge-index'],boundary:hit.node?.answer?.boundary||null},hit.score/100));
   return json(envelope(q,'scripture',{delegated:true,endpoint:'/dore/search-index.json',fallback_from:'brain',provenance:['dore.browser-search']},0));
  }
  return json(envelope(q,'scripture',{delegated:true,endpoint:'/dore/search-index.json',provenance:['dore.browser-search'],capabilities:['reference','chapter','range','multi-reference','exact-text','fuzzy','original-language','entity']},1));
 }catch(error){return json({ok:false,schema:'dore.query.v1',query:q,type,error:'service_query_failed',detail:String(error?.message||error)},500)}
}
export async function onRequestPost(ctx){let body={};try{body=await ctx.request.json()}catch{return json({ok:false,error:'invalid_json'},400)}const q=String(body?.query||'').trim();if(!q)return json({ok:false,error:'query_required'},400);const u=new URL(ctx.request.url);u.searchParams.set('q',q);if(body.type)u.searchParams.set('type',body.type);return onRequestGet({...ctx,request:new Request(u.toString(),ctx.request)})}
