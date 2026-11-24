#!/usr/bin/env node
/**
 * Read-only Dawn cover repair STAGING BUILDER. Never edits canonical or
 * published cover files. Outputs a complete replacement root manifest and
 * append-only missing-Work preview shards to a separate staging directory.
 *
 * 407 existing preview shards are preserved as-is; only root metadata points
 * at their actual SHA/count. 1,020 missing Work IDs receive truthful text-only
 * cover records derived from canonical Works (never invented cover images).
 *
 * node scripts/stage-dawn-cover-reconciliation.cjs --out /tmp/dawn-cover-stage
 */
'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const ROOT=path.resolve(__dirname,'../static/dawn-library');
const MAX=500;
const args=process.argv;
const at=args.indexOf('--out');
if(at<0||!args[at+1])throw Error('Use --out <staging directory>');
const OUT=path.resolve(args[at+1]);
if(OUT===ROOT||OUT.startsWith(ROOT+path.sep))throw Error('Refusing to stage inside published Dawn source');
fs.mkdirSync(OUT,{recursive:true});
const input=rel=>fs.readFileSync(path.join(ROOT,rel));
const parse=rel=>JSON.parse(input(rel).toString('utf8'));
const digest=bytes=>crypto.createHash('sha256').update(bytes).digest('hex');
const write=(name,value)=>{
 const content=Buffer.from(JSON.stringify(value)+'\n','utf8');
 fs.writeFileSync(path.join(OUT,name),content);
 return digest(content);
};
const canonical=parse('canonical/root.json');
const original=parse('cover-preview/root.json');
if(canonical.identityAuthority!=='Dawn'||canonical.shardCount!==21||
   original.shardCount!==407||canonical.workCount!==original.workCount)
 throw Error('Dawn source root contract differs from tested baseline');
const all=new Map();
for(const shard of canonical.shards){
 const data=parse('canonical/'+shard.href);
 const works=data.works||{};
 if(Object.keys(works).length!==shard.workCount)throw Error('Canonical count mismatch '+shard.href);
 for(const [id,work] of Object.entries(works)){
  if(all.has(id))throw Error('Duplicated canonical Work '+id);
  all.set(id,work);
 }
}
if(all.size!==canonical.workCount)throw Error('Canonical total differs');
const known=new Set(),corrected=[];
let active=0,changed=0;
for(const shard of original.shards){
 const rel='cover-preview/'+shard.href,bytes=input(rel),data=JSON.parse(bytes.toString('utf8'));
 if(data.schema!=='dawn.library.cover-preview-shard.v1'||!Array.isArray(data.items))
  throw Error('Invalid preview shard '+shard.href);
 for(const item of data.items){
  if(!all.has(item.workId)||known.has(item.workId))throw Error('Invalid or duplicate preview Work '+item.workId);
  known.add(item.workId);
 }
 const newMeta={...shard,offset:active,count:data.items.length,sha256:digest(bytes)};
 if(shard.offset!==active||shard.count!==data.items.length||shard.sha256!==newMeta.sha256)changed++;
 corrected.push(newMeta);
 active+=data.items.length;
}
const missing=[...all.keys()].filter(id=>!known.has(id));
if(missing.length!==canonical.workCount-known.size)throw Error('Missing Work count mismatch');
const repairShards=[];
for(let start=0;start<missing.length;start+=MAX){
 const ids=missing.slice(start,start+MAX);
 const number=original.shards.length+repairShards.length+1;
 const href='covers-'+String(number).padStart(6,'0')+'.json';
 const items=ids.map(id=>{
  const work=all.get(id),authors=Array.isArray(work.authors)?work.authors:
    (work.author?[work.author]:[]);
  return {workId:id,motionKey:'dawn-work:'+id,
   title:String(work.title||'原始書名未提供'),authors,
   languages:Array.isArray(work.languages)?work.languages:[],
   cover:{src:null,source:'dawn-placeholder',width:null,height:null,aspectRatio:null,
     workLookup:null},
   motion:{layer:'cover',detachable:true,layoutStable:false,
     preferredProperties:['transform','opacity']}};
 });
 const payload={schema:'dawn.library.cover-preview-shard.v1',offset:active,
  count:items.length,items};
 const sha256=write(href,payload);
 const meta={offset:active,count:items.length,href,sha256};
 repairShards.push(meta);active+=items.length;
}
if(active!==canonical.workCount)throw Error('Proposed manifest not equal to canonical total');
const proposed={...original,shards:[...corrected,...repairShards],
 shardCount:corrected.length+repairShards.length,
 reconciliation:{schema:'dawn.cover-preview-reconciliation.v1',
   baseOriginalShardCount:original.shardCount,
   strategy:'append missing canonical Work IDs as honest no-image records; do not claim visual verification',
   publication:'staged-only-until-editorial-approval'}};
write('root.json',proposed);
const validation={
 schema:'dawn.cover-preview-staging-validation.v1',
 status:'PASS',canonicalWorks:canonical.workCount,originalPreviewWorks:known.size,
 missingWorkCount:missing.length,manifestChangedShards:changed,
 proposedShards:proposed.shardCount,proposedWorkCount:active,
 appendedShards:repairShards,missingWorkIds:missing,
 note:'Existing 407 original cover shards remain untouched. Proposed root and repair tail must be promoted together after QA.'
};
write('reconciliation-report.json',validation);
console.log(JSON.stringify({status:'PASS',canonicalWorks:canonical.workCount,
 originalPreviewWorks:known.size,missingWorkCount:missing.length,
 changedManifestEntries:changed,newShards:repairShards.length,
 proposedWorkCount:active,staging:OUT}));
