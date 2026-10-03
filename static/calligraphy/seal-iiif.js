(()=>{"use strict";
function arr(v){return Array.isArray(v)?v:v?[v]:[]}
function text(v){if(typeof v==="string")return v;if(Array.isArray(v))return v.join(" / ");if(v?.none)return arr(v.none).join(" / ");if(v?.zh)return arr(v.zh).join(" / ");if(v?.en)return arr(v.en).join(" / ");return""}
function canvases(m){return m.items||m.sequences?.flatMap(s=>s.canvases||[])||[]}
function imageBody(c){const page=c.items?.[0],anno=page?.items?.[0],body=anno?.body;if(body)return body;return c.images?.[0]?.resource||null}
function service(body){const s=arr(body?.service)[0]||arr(body?.services)[0];return s||null}
function feature(c,i){const body=imageBody(c),svc=service(body),w=Number(c.width||body?.width||0),h=Number(c.height||body?.height||0);return{canvasId:c.id||c["@id"]||"",index:i,width:w,height:h,aspect:w&&h?w/h:null,imageService:svc?.id||svc?.["@id"]||"",imageId:body?.id||body?.["@id"]||"",label:text(c.label)}}
async function inspect(manifestUrl){const res=await fetch(manifestUrl,{headers:{Accept:"application/ld+json, application/json"}});if(!res.ok)throw new Error(`IIIF ${res.status}`);const m=await res.json(),fs=canvases(m).map(feature).filter(x=>x.width&&x.height);return{manifestUrl,id:m.id||m["@id"]||manifestUrl,label:text(m.label),rights:m.rights||m.license||"",requiredStatement:text(m.requiredStatement?.value),provider:arr(m.provider).map(p=>text(p.label)).filter(Boolean),canvasCount:fs.length,features:fs}}
function summarize(records=[]){const fs=records.flatMap(r=>r.features||[]).filter(x=>x.aspect),ratios=fs.map(x=>x.aspect);return{manifests:records.length,canvases:fs.length,meanAspect:ratios.length?ratios.reduce((a,v)=>a+v,0)/ratios.length:null,aspectRatios:ratios}}
window.SEAL_IIIF={inspect,summarize};
})();