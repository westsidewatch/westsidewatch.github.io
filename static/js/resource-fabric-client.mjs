const ROOT='/dawn-library/resource-fabric';
const manifestPromise=fetch(`${ROOT}/manifest.json`,{cache:'no-store'}).then(async r=>{
  if(!r.ok)throw new Error(`Resource Fabric manifest ${r.status}`);
  const manifest=await r.json();
  if(manifest?.schema!=='dore.resource-fabric.surface-manifest.v0')throw new Error('Resource Fabric manifest schema mismatch');
  if(manifest?.canonicalMonolithRequired!==false)throw new Error('Resource Fabric canonical monolith boundary violated');
  if(manifest?.identityAuthority!=='Dawn')throw new Error('Resource Fabric identity authority mismatch');
  return manifest;
});
const shardCache=new Map();
const encoder=new TextEncoder();

function fnv1a(text=''){
  let h=0x811c9dc5;
  for(const b of encoder.encode(String(text))){h^=b;h=Math.imul(h,0x01000193)>>>0;}
  return h>>>0;
}
function hex(i){return Number(i).toString(16).padStart(2,'0');}
function decode(row=[]){
  const [workId,title,author,coverPointer,readingPointer,authorityBacked,authors,languages,authorityIds,edition]=row;
  return {
    workId,
    title:title||'Untitled',
    authors:Array.isArray(authors)&&authors.length?authors:(author?[author]:[]),
    languages:Array.isArray(languages)?languages:[],
    authorityIds:authorityIds||{},
    edition:edition||{},
    cover:{pointer:`dawn://cover/${workId}`,mode:'resource-fabric'},
    resourceCoverPointer:coverPointer||null,
    readingPointer:readingPointer||null,
    authorityBacked:Boolean(authorityBacked),
  };
}
async function loadShard(index){
  const key=Number(index);
  if(!shardCache.has(key)){
    shardCache.set(key,fetch(`${ROOT}/work-${hex(key)}.json`,{cache:'force-cache'}).then(r=>{if(!r.ok)throw new Error(`Resource Fabric shard ${key} ${r.status}`);return r.json();}));
  }
  return shardCache.get(key);
}
export async function resourceManifest(){return manifestPromise;}
export async function resourceWork(workId){
  if(!workId)return null;
  const manifest=await manifestPromise;
  const index=fnv1a(workId)%manifest.workShardCount;
  const shard=await loadShard(index);
  const row=(shard.rows||[]).find(r=>r[0]===workId);
  return row?decode(row):null;
}
export async function resourceWorks(workIds=[]){
  const manifest=await manifestPromise;
  const unique=[...new Set(workIds.filter(Boolean))];
  const groups=new Map();
  for(const id of unique){const index=fnv1a(id)%manifest.workShardCount;if(!groups.has(index))groups.set(index,[]);groups.get(index).push(id);}
  const out=new Map();
  await Promise.all([...groups.entries()].map(async([index,ids])=>{
    const shard=await loadShard(index);const wanted=new Set(ids);
    for(const row of shard.rows||[])if(wanted.has(row[0]))out.set(row[0],decode(row));
  }));
  return out;
}
export async function resourceFeatured(){
  const r=await fetch(`${ROOT}/featured.json`,{cache:'force-cache'});if(!r.ok)throw new Error(`Resource Fabric featured ${r.status}`);
  const data=await r.json();return (data.rows||[]).map(decode);
}
export async function resourceSearch(query){
  const q=String(query||'').trim().toLocaleLowerCase();if(!q)return [];
  const token=(q.match(/[\p{L}\p{N}_]+/u)||[])[0]||'';if(!token)return [];
  const prefix=token.slice(0,Math.min(4,token.length));
  const manifest=await manifestPromise;
  const bucket=fnv1a(prefix)%manifest.searchBucketCount;
  const r=await fetch(`${ROOT}/search-${hex(bucket)}.json`,{cache:'force-cache'});if(!r.ok)throw new Error(`Resource Fabric search bucket ${bucket} ${r.status}`);
  const data=await r.json();
  const ids=(data.rows||[]).filter(row=>row[0]===prefix&&`${row[2]} ${row[3]}`.toLocaleLowerCase().includes(q)).map(row=>row[1]);
  const works=await resourceWorks(ids);
  return ids.map(id=>works.get(id)).filter(Boolean);
}
export const resourceFabric={manifest:resourceManifest,work:resourceWork,works:resourceWorks,featured:resourceFeatured,search:resourceSearch};
