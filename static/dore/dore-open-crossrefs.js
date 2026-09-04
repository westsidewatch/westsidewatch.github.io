(()=>{
'use strict';
const root=typeof window!=='undefined'?window:globalThis;
const D=root.DoreBibleIntelligence;
if(!D||D.openCrossrefs)return;
const VERSION='dore.open-crossrefs.v1';
const MANIFEST_URL='/dore/crossrefs/manifest.json';
let manifestPromise=null;
const shardPromises=new Map();
const canonical=ref=>D.canonicalRef(ref);
const osis=ref=>canonical(ref).replace(/^bible\.ref\./,'');
const split=ref=>{const m=osis(ref).match(/^([1-3]?[A-Z]{2,3})\.(\d+)\.(\d+)$/);return m?{book:m[1],key:`${Number(m[2])}.${Number(m[3])}`} : null};
const weight=(votes,mask)=>{
  const v=Math.max(0,Number(votes)||0);
  const sourceBonus=mask===3?.12:(mask&1?.07:.03);
  return Math.min(.99,.58+Math.log1p(v)*.055+sourceBonus);
};
const sourceLabel=mask=>mask===3?'OpenBible + TSK':(mask&1?'OpenBible':'TSK');
async function loadManifest(){
  if(manifestPromise)return manifestPromise;
  manifestPromise=fetch(MANIFEST_URL,{cache:'force-cache'}).then(r=>{if(!r.ok)throw new Error(`crossrefs manifest HTTP ${r.status}`);return r.json()}).then(m=>{
    if(m?.schema!=='dore.crossrefs.manifest.v1')throw new Error('invalid Doré cross-reference manifest');
    D.registerSource?.({id:m.source_dataset||'neuu-bible-crossrefs',type:'cross-reference-dataset',license:m.license,status:'active',authority:'OpenBible community votes + TSK historical cross references',upstream_repository:m.upstream_repository,upstream_commit:m.upstream_commit});
    return m;
  });
  return manifestPromise;
}
async function loadShard(book){
  const b=String(book||'').toUpperCase();
  if(shardPromises.has(b))return shardPromises.get(b);
  const p=loadManifest().then(async m=>{
    if(!m.shards?.[b])return null;
    const r=await fetch(`/dore/crossrefs/${encodeURIComponent(b)}.json`,{cache:'force-cache'});
    if(!r.ok)throw new Error(`crossrefs ${b} HTTP ${r.status}`);
    const data=await r.json();
    if(data?.schema!=='dore.crossrefs.book.v1'||data.book!==b)throw new Error(`invalid cross-reference shard ${b}`);
    return data;
  });
  shardPromises.set(b,p);return p;
}
async function direct(ref,opts={}){
  const parsed=split(ref);if(!parsed)return[];
  const shard=await loadShard(parsed.book);if(!shard)return[];
  const minVotes=Math.max(0,Number(opts.minVotes||0));
  const wanted=String(opts.source||'').toLowerCase();
  const limit=Math.max(1,Math.min(250,Number(opts.limit||40)));
  const rows=shard.refs?.[parsed.key]||[];
  return rows.filter(row=>Number(row[1]||0)>=minVotes).filter(row=>!wanted||wanted==='all'||(wanted==='openbible'&&(row[2]&1))||((wanted==='tsk'||wanted==='souliberty')&&(row[2]&2))).map(row=>({
    reference:canonical(row[0]),
    score:Number(weight(row[1],row[2]).toFixed(4)),
    depth:1,
    path:[canonical(ref),canonical(row[0])],
    relation_type:'traditional_cross_reference',
    source_dataset:shard.source_dataset||'neuu-bible-crossrefs',
    source_votes:Number(row[1]||0),
    source_mask:Number(row[2]||0),
    source_label:sourceLabel(Number(row[2]||0)),
    provenance:{dataset:shard.source_dataset||'neuu-bible-crossrefs',license:shard.license,source:sourceLabel(Number(row[2]||0)),manifest:MANIFEST_URL,book_shard:`/dore/crossrefs/${parsed.book}.json`}
  })).sort((a,b)=>b.score-a.score||b.source_votes-a.source_votes||a.reference.localeCompare(b.reference)).slice(0,limit);
}
async function graph(ref,opts={}){
  const start=canonical(ref);if(!start)return[];
  const maxDepth=Math.max(1,Math.min(3,Number(opts.depth||1)));
  const limit=Math.max(1,Math.min(150,Number(opts.limit||40)));
  const frontier=[{reference:start,score:1,depth:0,path:[start]}];
  const seen=new Map([[start,frontier[0]]]);
  while(frontier.length){
    const cur=frontier.shift();if(cur.depth>=maxDepth)continue;
    const links=await direct(cur.reference,{...opts,limit:Math.max(limit,80)});
    for(const link of links){
      const depth=cur.depth+1;
      const score=cur.score*link.score*Math.pow(.8,depth-1);
      const old=seen.get(link.reference);
      if(!old||score>old.score){
        const rec={...link,score:Number(score.toFixed(4)),depth,path:[...cur.path,link.reference]};
        seen.set(link.reference,rec);frontier.push(rec);
      }
    }
  }
  return [...seen.values()].filter(x=>x.reference!==start).sort((a,b)=>b.score-a.score||a.depth-b.depth||b.source_votes-a.source_votes).slice(0,limit);
}
async function relatedAsync(ref,opts={}){
  const open=await graph(ref,opts);
  const curated=D.related?.(ref,{depth:opts.depth||1,limit:opts.limit||40})||[];
  const merged=new Map();
  for(const item of [...open,...curated]){
    const old=merged.get(item.reference);
    if(!old||Number(item.score||0)>Number(old.score||0))merged.set(item.reference,item);
  }
  return [...merged.values()].sort((a,b)=>Number(b.score||0)-Number(a.score||0)||Number(a.depth||0)-Number(b.depth||0)).slice(0,Math.max(1,Math.min(150,Number(opts.limit||40))));
}
async function trace(from,to,opts={}){
  const target=canonical(to);const links=await graph(from,{...opts,depth:opts.depth||2,limit:opts.limit||150});
  return links.find(x=>x.reference===target)||null;
}
const api={version:VERSION,loadManifest,loadShard,direct,graph,relatedAsync,trace,stats:async()=>{const m=await loadManifest();return{schema:VERSION,dataset:m.source_dataset,license:m.license,...m.stats,loaded_shards:[...shardPromises.keys()]}}};
D.openCrossrefs=api;
D.relatedAsync=relatedAsync;
D.openRelated=direct;
D.traceOpenCrossref=trace;
if(typeof root.dispatchEvent==='function'&&typeof CustomEvent!=='undefined')root.dispatchEvent(new CustomEvent('dore:open-crossrefs-ready',{detail:{schema:VERSION}}));
})();
