#!/usr/bin/env node
/**
 * Dawn Library integrity audit, read-only over existing canonical/living/cover shards.
 * Usage: node scripts/audit-dawn-library-shards.cjs [--json OUTPUT]
 * Exit 1 on structural/identity corruption; exit 0 with discrepancy warnings
 * on known historical cover-preview offset/count drift.
 */
'use strict';
const fs=require('node:fs');
const path=require('node:path');
const crypto=require('node:crypto');
const base=path.resolve(__dirname,'../static/dawn-library');
const errors=[],warnings=[],stats={
 canonical:{shards:0,records:0,duplicateIds:0,hashMismatches:0},
 living:{shards:0,records:0,classified:0,duplicateIds:0,hashMismatches:0},
 covers:{shards:0,records:0,withImage:0,placeholder:0,duplicateIds:0,hashMismatches:0,declaredCountDrift:0}
};
const seen={canonical:new Set(),living:new Set(),covers:new Set()};
const coverRepairPlan=[];
function read(rel){
 const absolute=path.resolve(base,rel);
 if(!absolute.startsWith(base+path.sep))throw Error('Path escapes Dawn root: '+rel);
 const bytes=fs.readFileSync(absolute);
 return {value:JSON.parse(bytes.toString('utf8')),
   sha256:crypto.createHash('sha256').update(bytes).digest('hex')};
}
function check(condition,message,hard=true){if(!condition)(hard?errors:warnings).push(message)}
function idCheck(kind,id,where){
 check(typeof id==='string'&&id.length>0,where+': missing Work ID');
 if(typeof id!=='string'||!id)return;
 if(seen[kind].has(id)){stats[kind].duplicateIds++;errors.push(where+': duplicate '+id)}
 else seen[kind].add(id);
}
function hashCheck(kind,meta,actual,where){
 if(meta.sha256&&meta.sha256!==actual){
  stats[kind].hashMismatches++;
  warnings.push(where+': sha256 differs from manifest (possibly canonical re-serialization)');
 }
}
function scanCanonical(){
 const root=read('canonical/root.json').value;
 check(root.identityAuthority==='Dawn'&&root.shardCount===root.shards?.length,'Canonical root schema/count');
 for(const meta of root.shards||[]){
  const where='canonical/'+meta.href;
  try{
   const {value,sha256}=read(where);
   hashCheck('canonical',meta,sha256,where);
   const works=value.works||{};
   const ids=Object.keys(works);
   check(ids.length===meta.workCount,where+': work count '+ids.length+' vs '+meta.workCount);
   for(const id of ids)idCheck('canonical',id,where);
   stats.canonical.records+=ids.length;stats.canonical.shards++;
  }catch(err){errors.push(where+': '+err.message)}
 }
 check(stats.canonical.records===root.workCount,
  'Canonical actual work count '+stats.canonical.records+' vs root '+root.workCount);
 return root;
}
function scanLiving(rootCanonical){
 const root=read('living/root.json').value;
 check(root.identityAuthority==='Dawn'&&root.projectionOnly===true&&
   root.admissionAuthority===false&&root.shardCount===root.shards?.length,'Living root contract');
 check(root.canonicalWorkCount===rootCanonical.workCount,'Living canonical total differs');
 const knownLeaves=new Set((root.classification?.roots||[]).flatMap(g=>(g.children||[]).map(c=>c.id)));
 const knownRoots=new Set((root.classification?.roots||[]).map(g=>g.id));
 for(const meta of root.shards||[]){
  const relative=String(meta.href||'').replace(/^\/dawn-library\//,'');
  const where=relative;
  try{
   const {value,sha256}=read(relative);
   hashCheck('living',meta,sha256,where);
   check(value.schema==='dawn.library.living-wall-shard.v1'&&
     value.ordinal===meta.ordinal&&Array.isArray(value.workRefs),where+': contract');
   const rows=value.workRefs||[];
   check(rows.length===meta.workCount,where+': work count '+rows.length+' vs '+meta.workCount);
   for(const item of rows){
    idCheck('living',item.workId,where);
    check(seen.canonical.has(item.workId),where+': orphan Work '+item.workId);
    for(const id of item.classification?.roots||[])check(knownRoots.has(id),where+': unknown root '+id);
    for(const id of item.classification?.leaves||[])check(knownLeaves.has(id),where+': unknown leaf '+id);
    if((item.classification?.roots||[]).length||(item.classification?.leaves||[]).length)stats.living.classified++;
   }
   stats.living.records+=rows.length;stats.living.shards++;
  }catch(err){errors.push(where+': '+err.message)}
 }
 check(stats.living.records===root.canonicalWorkCount,
  'Living rows '+stats.living.records+' vs canonical '+root.canonicalWorkCount);
 return root;
}
function scanCovers(rootCanonical){
 const root=read('cover-preview/root.json').value;
 check(root.shardCount===root.shards?.length,'Cover preview root contract');
 check(root.workCount===rootCanonical.workCount,'Cover root differs from canonical count');
 for(const meta of root.shards||[]){
  const where='cover-preview/'+meta.href;
  try{
   const {value,sha256}=read(where);
   hashCheck('covers',meta,sha256,where);
   check(value.schema==='dawn.library.cover-preview-shard.v1'&&Array.isArray(value.items),
     where+': shard contract');
   const rows=value.items||[];
   if(meta.count!==rows.length){
    stats.covers.declaredCountDrift++;
    warnings.push(where+': manifest count '+meta.count+' but actual '+rows.length);
   }
   if(meta.count!==rows.length||meta.sha256!==sha256||value.count!==rows.length){
    coverRepairPlan.push({href:meta.href,manifestOffset:meta.offset,
      manifestCount:meta.count,shardDeclaredCount:value.count,
      actualCount:rows.length,manifestSha256:meta.sha256,actualSha256:sha256});
   }
   // Historic filtered preview shards may have stale internal counts. It is
   // a source discrepancy to report, not reason to block the entire audit.
   check(value.count===rows.length,where+': self count '+value.count+' differs from '+rows.length,false);
   for(const item of rows){
    idCheck('covers',item.workId,where);
    check(seen.canonical.has(item.workId),where+': orphan Work '+item.workId);
    const cover=item.cover||{};
    if(cover.src&&cover.source!=='dawn-placeholder')stats.covers.withImage++;
    else stats.covers.placeholder++;
   }
   stats.covers.records+=rows.length;stats.covers.shards++;
  }catch(err){errors.push(where+': '+err.message)}
 }
 if(stats.covers.records!==root.workCount)warnings.push(
  'Cover preview actual '+stats.covers.records+' vs canonical '+root.workCount+
  ' (preview omissions require a canonical-source audit, not a P2 count rewrite)');
 return root;
}
function main(){
 const canonical=scanCanonical();
 scanLiving(canonical);
 scanCovers(canonical);
 const missingCoverWorkIds=[...seen.canonical].filter(id=>!seen.covers.has(id));
 stats.covers.missingCanonicalWorks=missingCoverWorkIds.length;
 const report={schema:'dawn.library.integrity-report.v2',
  rootWorkCount:canonical.workCount,stats,errors,warnings,
  coverReconciliation:{missingCanonicalWorkIds:missingCoverWorkIds,shardCorrections:coverRepairPlan,
   authority:'canonical Work IDs; source data unchanged',action:'review/rebuild via existing admission pipeline'},
  status:errors.length?'FAIL':warnings.length?'WARN':'PASS',
  note:'File/hash and Work ID audit only; cannot establish remote image HTTP/rights/legibility.'};
 const i=process.argv.indexOf('--json');
 if(i>=0){
  const destination=process.argv[i+1];
  if(!destination)throw Error('Missing --json output path');
  fs.mkdirSync(path.dirname(destination),{recursive:true});
  fs.writeFileSync(destination,JSON.stringify(report,null,2)+'\n');
 }
 console.log(JSON.stringify({status:report.status,rootWorkCount:report.rootWorkCount,
  stats,errors:errors.slice(0,20),errorCount:errors.length,
  warnings:warnings.slice(0,20),warningCount:warnings.length},null,2));
 if(errors.length)process.exitCode=1;
}
if(require.main===module)main();
module.exports={main};
