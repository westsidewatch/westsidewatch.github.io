(()=>{
'use strict';
const root=typeof window!=='undefined'?window:globalThis;
const VERSION='dore.bible-intelligence.v0.1';
const graph=new Map();
const edgeKeys=new Set();
const sourceRegistry=new Map();
const ZH={'圣':'聖','灵':'靈','经':'經','书':'書','马':'馬','约':'約','后':'後','来':'來','为':'為','国':'國','门':'門','东':'東','亚':'亞','罗':'羅','传':'傳','创':'創','数':'數','历':'歷','启':'啟','结':'結','赛':'賽','扫':'掃','耶稣':'耶穌','旷':'曠','试':'試','炼':'煉','旧':'舊','里':'裡'};
const fold=s=>String(s??'').normalize('NFKC').replace(/[\u3400-\u9fff]/g,ch=>ZH[ch]||ch).toLowerCase();
const compact=s=>fold(s).replace(/[\s.,;:!?，。；：！？「」『』()（）\-–—_'"`]/g,'');
const canonicalRef=ref=>{
  const s=String(ref??'').trim();
  if(!s)return'';
  const m=s.match(/(?:bible\.ref\.)?([1-3]?[A-Z]{2,3})\.(\d+)\.(\d+)/i);
  return m?`bible.ref.${m[1].toUpperCase()}.${Number(m[2])}.${Number(m[3])}`:s;
};
const relationWeight={quotation:1,parallel:.98,entity_history:.94,event:.92,person:.9,place:.88,allusion:.86,lexical_original_language:.84,topic:.8,traditional_cross_reference:.76,'cross-reference':.74};
function registerSource(source){if(!source?.id)return;sourceRegistry.set(source.id,{...source});}
function addEdge(edge){
  const a=canonicalRef(edge.source_ref||edge.source||edge.from),b=canonicalRef(edge.target_ref||edge.target||edge.to);
  if(!a||!b||a===b)return false;
  const relation=edge.relation_type||edge.relation||'cross-reference';
  const origin=edge.relation_origin||'source';
  const source=edge.source_dataset||edge.dataset||'dore-curated-scripture';
  const key=[a,b,relation,source].join('|');
  if(edgeKeys.has(key))return false;
  edgeKeys.add(key);
  const rec={source_ref:a,target_ref:b,relation_type:relation,relation_origin:origin,source_dataset:source,source_weight:Number(edge.source_weight??edge.weight??relationWeight[relation]??.7),source_votes:Number(edge.source_votes||0),phrase_anchor:edge.phrase_anchor||'',entity_keys:Array.isArray(edge.entity_keys)?edge.entity_keys:[],provenance:edge.provenance||null,note:edge.note||''};
  if(!graph.has(a))graph.set(a,[]);graph.get(a).push(rec);
  if(edge.bidirectional!==false){const rev={...rec,source_ref:b,target_ref:a};if(!graph.has(b))graph.set(b,[]);graph.get(b).push(rev)}
  return true;
}
function ingestEdges(edges,meta={}){let added=0;(edges||[]).forEach(e=>{if(addEdge({...e,...(meta.source_dataset&&!e.source_dataset?{source_dataset:meta.source_dataset}:{}),...(meta.provenance&&!e.provenance?{provenance:meta.provenance}:{})}))added++});return{added,total_edges:edgeKeys.size};}
function ingestScriptureThreads(threads,meta={}){
  let added=0;
  for(const thread of threads||[]){
    const refs=(thread.refs||[]).map(r=>canonicalRef(typeof r==='string'?r:(r.reference||r.ref))).filter(Boolean);
    for(let i=0;i<refs.length;i++)for(let j=i+1;j<refs.length;j++){
      if(addEdge({source_ref:refs[i],target_ref:refs[j],relation_type:thread.relation||'traditional_cross_reference',relation_origin:'source',source_dataset:thread.source||meta.source_dataset||'one-scripture-thread',source_weight:Number(thread.weight||.76),phrase_anchor:thread.phrase_anchor||'',entity_keys:thread.entity_keys||[],provenance:thread.provenance||meta.provenance||{consumer:meta.consumer||'one',thread_id:thread.id||null},note:thread.note||''}))added++;
    }
  }
  return{added,total_edges:edgeKeys.size};
}
function related(ref,opts={}){
  const start=canonicalRef(ref),maxDepth=Math.max(1,Math.min(4,Number(opts.depth||2))),limit=Math.max(1,Math.min(100,Number(opts.limit||30)));
  if(!start)return[];
  const seen=new Map([[start,{score:1,depth:0,path:[start],via:null}]]),queue=[start];
  while(queue.length){const cur=queue.shift(),base=seen.get(cur);if(base.depth>=maxDepth)continue;for(const edge of graph.get(cur)||[]){const target=edge.target_ref,depth=base.depth+1,score=base.score*Number(edge.source_weight||.7)*Math.pow(.82,depth-1);const old=seen.get(target);if(!old||score>old.score){seen.set(target,{score,depth,path:[...base.path,target],via:edge});queue.push(target)}}}
  return[...seen.entries()].filter(([r])=>r!==start).map(([reference,x])=>({reference,score:Number(x.score.toFixed(4)),depth:x.depth,path:x.path,relation_type:x.via?.relation_type||null,source_dataset:x.via?.source_dataset||null,provenance:x.via?.provenance||null,phrase_anchor:x.via?.phrase_anchor||''})).sort((a,b)=>b.score-a.score||a.depth-b.depth||a.reference.localeCompare(b.reference)).slice(0,limit);
}
registerSource({id:'dore-curated-scripture',type:'canonical-scripture-relations',license:'references/facts',status:'active',authority:'Scripture relationship anchors; not a Bible text license'});
const CONCEPTS=[
 {id:'gilead-jabesh-saul',match:q=>/(基列雅比|雅比.*掃羅|掃羅.*雅比|基列.*掃羅|掃羅.*基列)/u.test(fold(q)),lead:'基列雅比與掃羅的關係不是一個孤立地名，而是一條跨越士師時代、掃羅作王與掃羅死後的歷史線。',refs:['bible.ref.JDG.21.8','bible.ref.1SA.11.1','bible.ref.1SA.31.11','bible.ref.2SA.2.4','bible.ref.1CH.10.11'],relations:['entity_history','entity_history','entity_history','parallel'],keywords:['基列雅比','掃羅','士師','基列']},
 {id:'wilderness-temptation-deuteronomy',match:q=>/(曠野.*(?:耶穌|試探)|耶穌.*(?:曠野|試探)|試探.*申命記|申命記.*試探)/u.test(fold(q)),lead:'耶穌在曠野受試探的三卷福音記載，應與祂回答所引用／呼應的申命記 6–8 章一起閱讀。',refs:['bible.ref.MAT.4.1','bible.ref.MRK.1.12','bible.ref.LUK.4.1','bible.ref.DEU.8.3','bible.ref.DEU.6.16','bible.ref.DEU.6.13'],relations:['parallel','parallel','quotation','quotation','quotation'],keywords:['曠野','耶穌','試探','申命記']},
 {id:'ot-spirit-false-premise',match:q=>/(舊約.*(?:沒有|無).*聖靈|為什麼.*舊約.*聖靈|舊約.*聖靈)/u.test(fold(q)),lead:'這個前提不成立：舊約多次提到神的靈、耶和華的靈，也直接出現「聖靈」的表述。',refs:['bible.ref.GEN.1.2','bible.ref.JDG.3.10','bible.ref.1SA.16.13','bible.ref.PSA.51.11','bible.ref.ISA.63.10','bible.ref.EZK.36.27'],relations:['topic','topic','topic','topic','topic'],keywords:['神的靈','耶和華的靈','聖靈','我的靈']}
];
for(const c of CONCEPTS){for(let i=0;i<c.refs.length-1;i++)addEdge({source_ref:c.refs[i],target_ref:c.refs[i+1],relation_type:c.relations[i]||'topic',relation_origin:'dore-curated',source_dataset:'dore-curated-scripture',source_weight:relationWeight[c.relations[i]]||.82,provenance:{concept_id:c.id,evidence:'canonical Scripture references; verse text resolved from Doré local Scripture index'}})}
let scripturePromise=null;
async function scriptureData(){if(scripturePromise)return scripturePromise;scripturePromise=(typeof fetch==='function'?fetch('/dore/search-index.json',{cache:'no-cache'}).then(r=>r.ok?r.json():Promise.reject(new Error(`search-index HTTP ${r.status}`))):Promise.resolve(null)).catch(()=>null);return scripturePromise;}
function refMap(data){const m=new Map();for(const v of data?.verses||[])m.set(v.r,v);return m;}
function label(v,ref){return v?`${v.n?.[0]||v.b} ${v.c}:${v.v}`:ref.replace('bible.ref.','').replace(/\.(\d+)\.(\d+)$/, ' $1:$2');}
async function conceptSearch(q){const concept=CONCEPTS.find(c=>c.match(q));if(!concept)return null;const data=await scriptureData(),byRef=refMap(data);const evidence=concept.refs.map((ref,i)=>{const v=byRef.get(ref);return{reference:ref,label:label(v,ref),zh:v?.z||'',en:v?.e||'',relation_type:i?concept.relations[i-1]||'topic':'anchor',source_dataset:'dore-curated-scripture',provenance:{corpus:data?.schema||'dore-search-index',concept_id:concept.id}}});return{schema:VERSION,kind:'bible-intelligence',concept_id:concept.id,query:q,lead:concept.lead,evidence,keywords:concept.keywords,traceable:true};}
function isIntelligenceQuery(q){return CONCEPTS.some(c=>c.match(q));}
const esc=s=>String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
function renderSearchResult(result){if(typeof document==='undefined'||!result)return false;const box=document.querySelector('#results'),count=document.querySelector('#result-count'),wrap=document.querySelector('#results-wrap');if(!box||!count)return false;count.textContent=`Doré Bible Intelligence · ${result.evidence.length} 條可追溯經文`;box.innerHTML=`<article class="brain-answer bible-intelligence-answer"><header><strong>DORÉ</strong><span>BIBLE INTELLIGENCE · ${esc(result.concept_id)}</span></header><h3>${esc(result.lead)}</h3><p class="brain-scripture"><strong>關係：</strong>${result.keywords.map(esc).join(' · ')}</p></article>`+result.evidence.map((x,i)=>`<article class="result-card" data-dore-intelligence-ref="${esc(x.reference)}"><header><strong>${esc(x.label)}</strong><span>${esc(x.relation_type)}</span></header>${x.zh?`<p lang="zh-Hant">${esc(x.zh)}</p>`:''}${x.en?`<p class="english" lang="en">${esc(x.en)}</p>`:''}<footer><span>${esc(x.source_dataset)}</span><span>traceable · ${esc(result.concept_id)} · ${i+1}/${result.evidence.length}</span></footer></article>`).join('');wrap?.scrollIntoView({behavior:'smooth',block:'start'});return true;}
function installSearchInterceptor(){if(typeof document==='undefined'||document.documentElement?.dataset.doreBibleIntelligenceBound)return;if(document.documentElement)document.documentElement.dataset.doreBibleIntelligenceBound='1';document.addEventListener('submit',async e=>{const form=e.target;if(!(form instanceof HTMLFormElement)||form.id!=='search-form')return;const q=form.querySelector('#search-input,input[name="q"]')?.value?.trim();if(!q||!isIntelligenceQuery(q))return;e.preventDefault();e.stopImmediatePropagation();const result=await conceptSearch(q);renderSearchResult(result);},true);}
const api={version:VERSION,fold,compact,canonicalRef,registerSource,addEdge,ingestEdges,ingestScriptureThreads,related,conceptSearch,isIntelligenceQuery,renderSearchResult,installSearchInterceptor,stats:()=>({schema:VERSION,nodes:graph.size,edges:edgeKeys.size,sources:[...sourceRegistry.values()]})};
root.DoreBibleIntelligence=api;
installSearchInterceptor();
if(typeof root.dispatchEvent==='function'&&typeof CustomEvent!=='undefined')root.dispatchEvent(new CustomEvent('dore:bible-intelligence-ready',{detail:api.stats()}));
})();
