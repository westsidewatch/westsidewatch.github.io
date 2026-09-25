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

const fabricIds=new Set();
for(const name of fs.readdirSync(fabricDir).filter(n=>/^works-.*\.json$/.test(n)).sort()){
  const payload=JSON.parse(fs.readFileSync(path.join(fabricDir,name),'utf8'));
  const raw=payload.works??payload.items??payload;
  const entries=Array.isArray(raw)?raw:Object.values(raw||{});
  for(const w of entries){const id=w.workId||w.id||w.canonicalId;if(id)fabricIds.add(id)}
}
const fabricOrphans=[...fabricIds].filter(id=>!canonicalIds.has(id));
const canonicalWithSemantic=[...canonicalIds].filter(id=>semanticByWork.has(id)).length;
const canonicalWithFabric=[...canonicalIds].filter(id=>fabricIds.has(id)).length;
const canonicalWithBoth=[...canonicalIds].filter(id=>semanticByWork.has(id)&&fabricIds.has(id)).length;
const top=m=>Object.fromEntries([...m.entries()].sort((a,b)=>b[1]-a[1]).slice(0,500));

const report={
 schema:'dawn.shared-resource-join-audit.v1',generatedAt:new Date().toISOString(),
 authority:{identity:'Dawn canonical Work ID',semantic:'Living classification/facets projection',resource:'Resource Fabric'},
 counts:{canonicalWorks:canonicalIds.size,livingRefs,resourceFabricWorks:fabricIds.size,resourceFabricManifestWorks:fabricManifest.workCount,canonicalWithSemantic,canonicalWithFabric,canonicalWithBoth},
 integrity:{canonicalMatchesRoot:canonicalIds.size===canonicalRoot.workCount,livingMatchesRoot:livingRefs===livingRoot.canonicalWorkCount,livingOrphans,resourceFabricOrphans:fabricOrphans.length,resourceFabricOrphanSample:fabricOrphans.slice(0,100)},
 semanticTopology:{roots:top(semanticCounts.roots),leaves:top(semanticCounts.leaves),periods:top(semanticCounts.periods),languages:top(semanticCounts.languages)},
 next:{semanticJoinCoverage:canonicalIds.size?canonicalWithSemantic/canonicalIds.size:0,resourceJoinCoverage:canonicalIds.size?canonicalWithFabric/canonicalIds.size:0,bothCoverage:canonicalIds.size?canonicalWithBoth/canonicalIds.size:0}
};
const out=path.join(dawn,'editorial');fs.mkdirSync(out,{recursive:true});fs.writeFileSync(path.join(out,'shared-resource-join-audit-v1.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report.counts,null,2));
if(!report.integrity.canonicalMatchesRoot||!report.integrity.livingMatchesRoot||livingOrphans)process.exitCode=1;
