/** Dawn Living subject membership adapter. No second index, no synthetic Work ID.
 * Authority: /dawn-library/living/root.json + its original 21 wall shards.
 * Return a bounded sample of explicitly classified canonical IDs.
 */
import {resourceWorks} from '/js/resource-fabric-client.mjs';
const ROOT='/dawn-library/living/root.json';
let rootPromise;
const shardCache=new Map();
async function json(url) {
  const response=await fetch(url,{signal:AbortSignal.timeout(20000)});
  if(!response.ok)throw Error('Dawn Living source unavailable: '+response.status);
  return response.json();
}
async function root() {
  rootPromise ||= json(ROOT).catch(error=>{rootPromise=null;throw error});
  const data=await rootPromise;
  if(data.schema!=='dawn.library.living-root.v1'||data.identityAuthority!=='Dawn'||
     data.projectionOnly!==true||data.admissionAuthority!==false||
     data.shardCount!==data.shards?.length)throw Error('Living root authority mismatch');
  return data;
}
async function shard(meta){
  const href=meta.href;
  if(typeof href!=='string'||!/^\/dawn-library\/living\/wall-\d{6}\.json$/.test(href))
    throw Error('Unexpected Living shard path');
  if(!shardCache.has(href))shardCache.set(href,json(href).catch(err=>{shardCache.delete(href);throw err}));
  const data=await shardCache.get(href);
  if(data.schema!=='dawn.library.living-wall-shard.v1'||
     data.identityAuthority!=='Dawn'||data.projectionOnly!==true||
     data.admissionAuthority!==false||!Array.isArray(data.workRefs)||
     data.ordinal!==meta.ordinal)throw Error('Living shard contract mismatch');
  return data;
}
export async function livingSubjectBooks(subjectId,{limit=36,isCurrent=()=>true}={}){
  const data=await root();
  const category=[...data.classification.roots,
    ...data.classification.roots.flatMap(group=>group.children||[])]
    .find(item=>item.id===subjectId);
  if(!category)throw Error('Unknown canonical subject: '+subjectId);
  const leaf=subjectId.includes('.'),ids=[],seen=new Set();
  let visited=0,complete=false;
  for(const meta of data.shards){
    if(!isCurrent())return null;
    const part=await shard(meta);
    visited++;
    for(const ref of part.workRefs){
      const memberships=leaf?ref.classification?.leaves:ref.classification?.roots;
      if(!Array.isArray(memberships)||!memberships.includes(subjectId))continue;
      if(typeof ref.workId!=='string'||seen.has(ref.workId))continue;
      seen.add(ref.workId);ids.push(ref.workId);
      if(ids.length>=limit)break;
    }
    if(ids.length>=limit)break;
  }
  complete=visited===data.shards.length;
  if(!isCurrent())return null;
  const works=await resourceWorks(ids);
  if(!isCurrent())return null;
  const books=ids.map(id=>works.get(id)).filter(work=>work?.workId&&work?.title)
    .map(work=>({
      workId:work.workId,title:work.title,creator:(work.authors||[]).join(' · '),
      cover:work.cover,authorityIds:work.authorityIds,edition:work.edition,
      readingPointer:work.readingPointer
    }));
  return {books,visited,totalShards:data.shards.length,
    sampleComplete:complete,matchedIds:ids.length,subjectId,declaredCount:category.workCount};
}
