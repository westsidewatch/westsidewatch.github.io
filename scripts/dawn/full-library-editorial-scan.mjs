#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const repo=process.cwd();
const canonical=path.join(repo,'static/dawn-library/canonical');
const root=JSON.parse(fs.readFileSync(path.join(canonical,'root.json'),'utf8'));
const shardFiles=(root.shards||[]).map(s=>s.href);
const LANG={eng:'en',en:'en',English:'en',chi:'zh',cmn:'zh',zh:'zh',zho:'zh',ger:'de',German:'de',deu:'de',fre:'fr',French:'fr',fra:'fr',spa:'es',Spanish:'es',gre:'el',grc:'grc'};
const inc=(m,k,n=1)=>m.set(k,(m.get(k)||0)+n);
const obj=m=>Object.fromEntries([...m.entries()].sort((a,b)=>b[1]-a[1]||String(a[0]).localeCompare(String(b[0]))));
const arr=v=>v==null?[]:(Array.isArray(v)?v:[v]);
const strings=v=>arr(v).flatMap(x=>typeof x==='string'?[x]:(x?.name||x?.label||x?.title?[x.name||x.label||x.title]:[])).filter(Boolean);
const stats={works:0,authority:0,languages:new Map(),rawLanguages:new Map(),authors:new Map(),subjects:new Map(),years:new Map(),sources:new Map(),missing:{title:0,language:0,author:0,subjects:0},chinese:{works:0,authors:new Map(),subjects:new Map(),years:new Map()},samples:{chinese:[],bridge:[]}};
for(const file of shardFiles){
 const payload=JSON.parse(fs.readFileSync(path.join(canonical,file),'utf8'));
 const works=Array.isArray(payload)?payload:(payload.works||payload.items||payload.workRefs||[]);
 const declared=(root.shards||[]).find(s=>s.href===file)?.workCount;
 if(declared!=null&&works.length!==declared)throw new Error(`${file}: declared ${declared} Works but found ${works.length}`);
 for(const w of works){
  stats.works++;
  const title=w.title||w.name||w.label||''; if(!title)stats.missing.title++;
  const rawLang=[...new Set([...strings(w.languages),...strings(w.language),...strings(w.editions?.languages)].filter(Boolean))]; if(!rawLang.length)stats.missing.language++;
  const langs=[...new Set(rawLang.map(x=>LANG[x]||String(x).toLowerCase()))]; rawLang.forEach(x=>inc(stats.rawLanguages,x)); langs.forEach(x=>inc(stats.languages,x));
  const authors=[...new Set([...strings(w.authors),...strings(w.author),...strings(w.authorNames)])]; if(!authors.length)stats.missing.author++; authors.forEach(x=>inc(stats.authors,x));
  const subjects=[...new Set([...strings(w.subjects),...strings(w.subject),...strings(w.topics),...strings(w.tags)])]; if(!subjects.length)stats.missing.subjects++; subjects.forEach(x=>inc(stats.subjects,x));
  const year=w.firstPublishYear||w.first_publish_year||w.publishYear||w.year||null; if(year)inc(stats.years,String(year));
  const source=w.authority?.source||w.source||w.provenance?.source||null; if(source)inc(stats.sources,typeof source==='string'?source:(source.name||source.id||'unknown'));
  if(w.authorityBacked||w.authority?.backed||w.authority?.status==='backed')stats.authority++;
  const zh=langs.includes('zh'); if(zh){stats.chinese.works++; authors.forEach(x=>inc(stats.chinese.authors,x)); subjects.forEach(x=>inc(stats.chinese.subjects,x)); if(year)inc(stats.chinese.years,String(year)); if(stats.samples.chinese.length<200)stats.samples.chinese.push({id:w.id||w.workId,title,authors,subjects:subjects.slice(0,12),year,languages:langs});}
 }
}
const allSubjects=obj(stats.subjects), zhSubjects=obj(stats.chinese.subjects);
const gaps=Object.entries(allSubjects).filter(([s,n])=>n>=10).map(([subject,total])=>({subject,total,chinese:zhSubjects[subject]||0,chineseShare:(zhSubjects[subject]||0)/total})).sort((a,b)=>a.chineseShare-b.chineseShare||b.total-a.total).slice(0,1000);
const report={schema:'dawn.library.canonical-scan.v2',phase:'P2_ACTIVE',generatedAt:new Date().toISOString(),source:'static/dawn-library/canonical/root.json + canonical/works-*',canonicalWorkCount:root.workCount,scannedWorkCount:stats.works,shardCount:shardFiles.length,integrity:{countMatchesRoot:stats.works===root.workCount,missing:stats.missing},languages:{raw:obj(stats.rawLanguages),normalized:obj(stats.languages)},topology:{topAuthors:Object.fromEntries(Object.entries(obj(stats.authors)).slice(0,500)),topSubjects:Object.fromEntries(Object.entries(allSubjects).slice(0,2000)),years:obj(stats.years),sources:obj(stats.sources)},chinese:{workCount:stats.chinese.works,share:stats.works?stats.chinese.works/stats.works:0,topAuthors:Object.fromEntries(Object.entries(obj(stats.chinese.authors)).slice(0,500)),topSubjects:Object.fromEntries(Object.entries(zhSubjects).slice(0,2000)),years:obj(stats.chinese.years),samples:stats.samples.chinese},p2:{chineseSubjectGaps:gaps}};
const out=path.join(repo,'static/dawn-library/editorial'); fs.mkdirSync(out,{recursive:true}); fs.writeFileSync(path.join(out,'canonical-scan-v2.json'),JSON.stringify(report,null,2)+'\n');
if(!report.integrity.countMatchesRoot)throw new Error(`canonical scan count mismatch: ${stats.works}/${root.workCount}`);
console.log(JSON.stringify({phase:report.phase,works:report.scannedWorkCount,shards:report.shardCount,chinese:report.chinese.workCount,subjectGapCandidates:gaps.length,missing:report.integrity.missing},null,2));
