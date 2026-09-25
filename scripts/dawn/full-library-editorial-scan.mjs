#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const repo=process.cwd();
const living=path.join(repo,'static/dawn-library/living');
const root=JSON.parse(fs.readFileSync(path.join(living,'root.json'),'utf8'));
const shardFiles=fs.readdirSync(living).filter(n=>/^wall-\d+\.json$/.test(n)).sort();
const LANG={eng:'en',en:'en',English:'en',chi:'zh',cmn:'zh',zh:'zh',ger:'de',German:'de',fre:'fr',French:'fr',spa:'es',Spanish:'es',gre:'el',grc:'grc'};
const VIDEO_HINT=/(video|movie|film|cinema|sermon|lecture|documentary|youtube|vimeo|影音|視頻|影片|電影|講道|紀錄片)/i;
const inc=(m,k,n=1)=>m.set(k,(m.get(k)||0)+n);
const obj=m=>Object.fromEntries([...m.entries()].sort((a,b)=>b[1]-a[1]||String(a[0]).localeCompare(String(b[0]))));
const arr=v=>v==null?[]:(Array.isArray(v)?v:[v]);
const stats={works:0,shards:shardFiles.length,rawLanguages:new Map(),languages:new Map(),periods:new Map(),roots:new Map(),leaves:new Map(),authors:new Map(),rootPairs:new Map(),mediums:new Map(),missing:{language:0,period:0,classification:0,author:0,medium:0},chinese:{works:0,byRoot:new Map(),byPeriod:new Map(),videoWorks:0},video:{works:0,byRoot:new Map(),byPeriod:new Map(),byLanguage:new Map(),byMedium:new Map(),cinemaCandidates:[]}};
for(const file of shardFiles){
 const payload=JSON.parse(fs.readFileSync(path.join(living,file),'utf8'));
 const works=Array.isArray(payload)?payload:(payload.workRefs||payload.works||payload.items||[]);
 if(payload.workCount!=null&&works.length!==payload.workCount)throw new Error(`${file}: declared ${payload.workCount} Works but found ${works.length}`);
 for(const w of works){
  stats.works++;
  const facets=w.facets||{};
  const langs=[...new Set([...arr(facets.languages),...arr(w.languages),...arr(w.language)].filter(Boolean))];
  if(!langs.length)stats.missing.language++;
  const normalized=[...new Set(langs.map(x=>LANG[x]||String(x).toLowerCase()))];
  langs.forEach(x=>inc(stats.rawLanguages,x)); normalized.forEach(x=>inc(stats.languages,x));
  const period=facets.period||w.period||w.classification?.period||'unknown'; inc(stats.periods,period); if(period==='unknown')stats.missing.period++;
  const roots=[...new Set(w.classification?.roots||[])]; const leaves=[...new Set(w.classification?.leaves||[])];
  if(!roots.length&&!leaves.length)stats.missing.classification++;
  roots.forEach(x=>inc(stats.roots,x)); leaves.forEach(x=>inc(stats.leaves,x));
  for(let i=0;i<roots.length;i++)for(let j=i+1;j<roots.length;j++)inc(stats.rootPairs,[roots[i],roots[j]].sort().join(' × '));
  const aa=[...arr(w.authors),...arr(w.author)].filter(Boolean); if(!aa.length)stats.missing.author++; aa.forEach(x=>inc(stats.authors,typeof x==='string'?x:(x.name||x.label||'unknown')));
  const rawMedium=[...arr(facets.mediums),...arr(facets.medium),...arr(w.medium),...arr(w.mediaType),...arr(w.resourceType),...arr(w.format),...arr(w.type),...arr(w.kind)].filter(Boolean).map(String); if(!rawMedium.length)stats.missing.medium++; rawMedium.forEach(x=>inc(stats.mediums,x));
  const pointers=[...arr(w.pointer),...arr(w.pointers),...arr(w.url),...arr(w.urls),...arr(w.source),...arr(w.sources),...arr(w.access)].filter(Boolean); const pointerText=JSON.stringify(pointers); const mediumText=rawMedium.join(' '); const titleText=[w.title,w.label,w.name].filter(Boolean).join(' '); const isVideo=VIDEO_HINT.test(`${mediumText} ${pointerText} ${titleText}`);
  const isChinese=normalized.includes('zh');
  if(isChinese){stats.chinese.works++; roots.forEach(x=>inc(stats.chinese.byRoot,x)); inc(stats.chinese.byPeriod,period); if(isVideo)stats.chinese.videoWorks++}
  if(isVideo){stats.video.works++; roots.forEach(x=>inc(stats.video.byRoot,x)); inc(stats.video.byPeriod,period); normalized.forEach(x=>inc(stats.video.byLanguage,x)); rawMedium.forEach(x=>inc(stats.video.byMedium,x)); if(stats.video.cinemaCandidates.length<5000)stats.video.cinemaCandidates.push({id:w.id||w.workId||w.canonicalId||null,title:w.title||w.label||w.name||null,languages:normalized,period,roots,medium:rawMedium,pointers})}
 }
}
const report={schema:'dawn.library.editorial-scan.v1',generatedAt:new Date().toISOString(),canonicalWorkCount:root.canonicalWorkCount,scannedWorkCount:stats.works,shardCount:stats.shards,integrity:{countMatchesRoot:stats.works===root.canonicalWorkCount,missing:stats.missing},languages:{raw:obj(stats.rawLanguages),normalized:obj(stats.languages)},media:{mediums:obj(stats.mediums)},topology:{periods:obj(stats.periods),roots:obj(stats.roots),leaves:obj(stats.leaves),rootCooccurrence:obj(stats.rootPairs),topAuthors:Object.fromEntries(Object.entries(obj(stats.authors)).slice(0,250))},chinese:{normalizedWorkCount:stats.chinese.works,share:stats.works?stats.chinese.works/stats.works:0,videoWorkCount:stats.chinese.videoWorks,byRoot:obj(stats.chinese.byRoot),byPeriod:obj(stats.chinese.byPeriod)},video:{workCount:stats.video.works,projectionSurface:'cinema',byRoot:obj(stats.video.byRoot),byPeriod:obj(stats.video.byPeriod),byLanguage:obj(stats.video.byLanguage),byMedium:obj(stats.video.byMedium),cinemaCandidates:stats.video.cinemaCandidates}};
const out=path.join(repo,'static/dawn-library/editorial'); fs.mkdirSync(out,{recursive:true}); fs.writeFileSync(path.join(out,'full-library-scan-v1.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({works:report.scannedWorkCount,shards:report.shardCount,countMatchesRoot:report.integrity.countMatchesRoot,chinese:report.chinese.normalizedWorkCount,video:report.video.workCount,chineseVideo:report.chinese.videoWorkCount,missing:report.integrity.missing},null,2));
