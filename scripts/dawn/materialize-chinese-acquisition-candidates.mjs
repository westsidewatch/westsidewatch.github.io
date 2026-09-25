#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const repo=process.cwd();
const dawn=path.join(repo,'static/dawn-library');
const canonicalDir=path.join(dawn,'canonical');
const acquisitionDir=path.join(dawn,'acquisition','chinese');
const outDir=path.join(dawn,'editorial','chinese-acquisition');
fs.mkdirSync(outDir,{recursive:true});

const norm=s=>String(s||'').normalize('NFKC').toLowerCase().replace(/[\s\p{P}\p{S}]+/gu,'').trim();
const canonicalRoot=JSON.parse(fs.readFileSync(path.join(canonicalDir,'root.json'),'utf8'));
const byTitle=new Map();
const byTitleAuthor=new Map();
let canonicalWorks=0;
for(const shard of canonicalRoot.shards||[]){
  const payload=JSON.parse(fs.readFileSync(path.join(canonicalDir,shard.href),'utf8'));
  const raw=payload.works??payload.items??payload.workRefs??payload;
  const works=Array.isArray(raw)?raw:Object.values(raw||{});
  for(const w of works){
    canonicalWorks++;
    const id=w.workId||w.id||w.canonicalId;
    const title=w.title||w.name||w.label||'';
    const authors=[...(Array.isArray(w.authors)?w.authors:[]),...(w.author?[w.author]:[])].map(a=>typeof a==='string'?a:(a?.name||a?.label||'')).filter(Boolean);
    const nt=norm(title); if(nt){if(!byTitle.has(nt))byTitle.set(nt,[]);byTitle.get(nt).push(id)}
    for(const a of authors){const k=`${nt}|${norm(a)}`;if(nt&&norm(a)){if(!byTitleAuthor.has(k))byTitleAuthor.set(k,[]);byTitleAuthor.get(k).push(id)}}
  }
}

const files=fs.existsSync(acquisitionDir)?fs.readdirSync(acquisitionDir).filter(n=>/\.(json|jsonl)$/i.test(n)).sort():[];
const rows=[];
for(const file of files){
  const text=fs.readFileSync(path.join(acquisitionDir,file),'utf8');
  let data=[];
  if(file.endsWith('.jsonl')) data=text.split(/\r?\n/).filter(Boolean).map(x=>JSON.parse(x));
  else {const j=JSON.parse(text);data=Array.isArray(j)?j:(j.candidates||j.items||j.rows||[])}
  for(const c of data){
    const title=c.title||c.name||c.label||''; if(!title)continue;
    const author=typeof c.author==='string'?c.author:(c.author?.name||c.primaryAuthor||'');
    const nt=norm(title), key=`${nt}|${norm(author)}`;
    const exact=author?(byTitleAuthor.get(key)||[]):[];
    const titleMatches=byTitle.get(nt)||[];
    let disposition='NEW_WORK_CANDIDATE',matches=[];
    if(exact.length){disposition='MATCH_EXISTING';matches=exact}
    else if(titleMatches.length){disposition='EDITION_OR_RESOURCE';matches=titleMatches}
    if(c.policyRejected===true)disposition='POLICY_REJECTED';
    else if(c.rightsStatus==='deferred'||c.rights==='deferred')disposition='RIGHTS_DEFERRED';
    rows.push({sourcePool:c.sourcePool||c.pool||c.source||file,title,author,year:c.year||c.date||null,language:c.language||c.languages||'zh',resourceType:c.resourceType||c.type||'text',providerId:c.providerId||c.id||null,providerUrl:c.providerUrl||c.url||null,rightsStatus:c.rightsStatus||c.rights||'unknown',normalizedTitle:nt,disposition,canonicalMatches:matches});
  }
}
const counts={};for(const r of rows)counts[r.disposition]=(counts[r.disposition]||0)+1;
const report={schema:'dawn.chinese-acquisition.materialization.v1',generatedAt:new Date().toISOString(),canonicalWorksScanned:canonicalWorks,inputFiles:files,candidateRows:rows.length,counts,rows};
fs.writeFileSync(path.join(outDir,'candidate-materialization-v1.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({canonicalWorksScanned:canonicalWorks,inputFiles:files.length,candidateRows:rows.length,counts},null,2));
