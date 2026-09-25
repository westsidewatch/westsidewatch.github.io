#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const repo=process.cwd();
const dawn=path.join(repo,'static/dawn-library');
const canonicalDir=path.join(dawn,'canonical');
const livingDir=path.join(dawn,'living');
const fabricDir=path.join(dawn,'resource-fabric');
const canonicalRoot=JSON.parse(fs.readFileSync(path.join(canonicalDir,'root.json'),'utf8'));
const livingRoot=JSON.parse(fs.readFileSync(path.join(livingDir,'root.json'),'utf8'));
const fabricManifest=JSON.parse(fs.readFileSync(path.join(fabricDir,'manifest.json'),'utf8'));

const canonicalIds=new Set();
for(const shard of canonicalRoot.shards||[]){
  const payload=JSON.parse(fs.readFileSync(path.join(canonicalDir,shard.href),'utf8'));
  const raw=payload.works??payload.items??payload.workRefs??payload;
  const entries=Array.isArray(raw)?raw:Object.values(raw||{});
  for(const w of entries){const id=w.workId||w.id||w.canonicalId;if(id)canonicalIds.add(id)}
}

const semanticByWork=new Map();
const semanticCounts={roots:new Map(),leaves:new Map(),periods:new Map(),languages:new Map()};
const inc=(m,k)=>m.set(k,(m.get(k)||0)+1);
let livingRefs=0,livingOrphans=0;
for(const shard of livingRoot.shards||[]){
  const payload=JSON.parse(fs.readFileSync(path.join(livingDir,path.basename(shard.href)),'utf8'));
  for(const ref of payload.workRefs||[]){
    livingRefs++;
    if(!canonicalIds.has(ref.workId))livingOrphans++;
    const roots=[...new Set(ref.classification?.roots||[])],leaves=[...new Set(ref.classification?.leaves||[])];
    roots.forEach(x=>inc(semanticCounts.roots,x));leaves.forEach(x=>inc(semanticCounts.leaves,x));
    const period=ref.facets?.period||null;if(period)inc(semanticCounts.periods,period);
    const languages=[...new Set(ref.facets?.languages||[])];languages.forEach(x=>inc(semanticCounts.languages,x));
    semanticByWork.set(ref.workId,{roots,leaves,period,languages});
  }
}

// Resource Fabric v0 is search-bucket routed, not works-* file routed.
// rows are [searchKey, workId, title, primaryAuthor]. Multiple rows may point to one Work.
const fabricIds=new Set();
const fabricTitles=new Map();
let fabricRows=0;
for(const name of fs.readdirSync(fabricDir).filter(n=>/^search-[0-9a-f]{2}\.json$/i.test(n)).sort()){
  const payload=JSON.parse(fs.readFileSync(path.join(fabricDir,name),'utf8'));
  for(const row of payload.rows||[]){
    fabricRows++;
    const workId=row?.[1]; if(!workId)continue;
    fabricIds.add(workId);
    if(!fabricTitles.has(workId))fabricTitles.set(workId,{title:row?.[2]||'',primaryAuthor:row?.[3]||''});
  }
}
const fabricOrphans=[...fabricIds].filter(id=>!canonicalIds.has(id));
const canonicalWithSemantic=[...canonicalIds].filter(id=>semanticByWork.has(id)).length;
const canonicalWithFabric=[...canonicalIds].filter(id=>fabricIds.has(id)).length;
const canonicalWithBoth=[...canonicalIds].filter(id=>semanticByWork.has(id)&&fabricIds.has(id)).length;
const top=m=>Object.fromEntries([...m.entries()].sort((a,b)=>b[1]-a[1]).slice(0,500));

const report={
 schema:'dawn.shared-resource-join-audit.v2',generatedAt:new Date().toISOString(),
 authority:{identity:'Dawn canonical Work ID',semantic:'Living classification/facets projection',resource:'Resource Fabric search buckets'},
 counts:{canonicalWorks:canonicalIds.size,livingRefs,resourceFabricRows:fabricRows,resourceFabricWorks:fabricIds.size,resourceFabricManifestWorks:fabricManifest.workCount,canonicalWithSemantic,canonicalWithFabric,canonicalWithBoth},
 integrity:{canonicalMatchesRoot:canonicalIds.size===canonicalRoot.workCount,livingMatchesRoot:livingRefs===livingRoot.canonicalWorkCount,livingOrphans,resourceFabricMatchesManifest:fabricIds.size===fabricManifest.workCount,resourceFabricOrphans:fabricOrphans.length,resourceFabricOrphanSample:fabricOrphans.slice(0,100)},
 semanticTopology:{roots:top(semanticCounts.roots),leaves:top(semanticCounts.leaves),periods:top(semanticCounts.periods),languages:top(semanticCounts.languages)},
 coverage:{semantic:canonicalIds.size?canonicalWithSemantic/canonicalIds.size:0,resourceFabric:canonicalIds.size?canonicalWithFabric/canonicalIds.size:0,both:canonicalIds.size?canonicalWithBoth/canonicalIds.size:0},
 interpretation:{identityLayer:'complete canonical corpus',semanticLayer:'full Living projection joined by Work ID',resourceLayer:'legacy/partial Resource Fabric v0; absence is a coverage gap, not missing canonical identity'}
};
const out=path.join(dawn,'editorial');fs.mkdirSync(out,{recursive:true});fs.writeFileSync(path.join(out,'shared-resource-join-audit-v2.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({counts:report.counts,integrity:report.integrity,coverage:report.coverage},null,2));
if(!report.integrity.canonicalMatchesRoot||!report.integrity.livingMatchesRoot||livingOrphans||!report.integrity.resourceFabricMatchesManifest)process.exitCode=1;
