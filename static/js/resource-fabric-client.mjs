const ROOT='/dawn-library/resource-fabric';
const CANON='/dawn-library/canonical';
const manifestPromise=fetch(`${ROOT}/manifest.json`,{cache:'no-store',signal:AbortSignal.timeout(15000)}).then(async r=>{if(!r.ok)throw new Error(`Resource Fabric manifest ${r.status}`);const manifest=await r.json();if(manifest?.schema!=='dore.resource-fabric.surface-manifest.v0')throw new Error('Resource Fabric manifest schema mismatch');if(manifest?.canonicalMonolithRequired!==false)throw new Error('Resource Fabric canonical monolith boundary violated');if(manifest?.identityAuthority!=='Dawn')throw new Error('Resource Fabric identity authority mismatch');return manifest;});
const canonicalRootPromise=fetch(`${CANON}/root.json`,{cache:'no-store',signal:AbortSignal.timeout(15000)}).then(async r=>{if(!r.ok)throw new Error(`Canonical root ${r.status}`);const root=await r.json();if(root?.identityAuthority!=='Dawn'||root?.runtimePolicy?.wikisource!=='forbidden')throw new Error('Canonical root boundary violated');return root;});
const shardCache=new Map(),segmentCache=new Map(),canonicalCache=new Map(),canonicalShardIndex=new Map(),encoder=new TextEncoder();
function fnv1a(text=''){let h=0x811c9dc5;for(const b of encoder.encode(String(text))){h^=b;h=Math.imul(h,0x01000193)>>>0;}return h>>>0;}
function hex(i){return Number(i).toString(16).padStart(2,'0');}
function coverUrl(authorityIds={},edition={}){const isbn=String(authorityIds?.isbn||edition?.isbn||'').replace(/[^0-9Xx]/g,'');if(isbn)return`https://covers.openlibrary.org/b/isbn/${encodeURIComponent(isbn)}-L.jpg?default=false`;const editionId=edition?.editionId;if(editionId&&/^OL\d+M$/i.test(editionId))return`https://covers.openlibrary.org/b/olid/${encodeURIComponent(editionId)}-L.jpg?default=false`;const workId=authorityIds?.openLibraryWork;if(workId&&/^OL\d+W$/i.test(workId))return`https://covers.openlibrary.org/b/olid/${encodeURIComponent(workId)}-L.jpg?default=false`;return null;}
function decode(row=[]){const [workId,title,author,coverPointer,readingPointer,authorityBacked,authors,languages,authorityIds,edition]=row;const ids=authorityIds||{},ed=edition||{},url=coverUrl(ids,ed);return{workId,title:title||'Untitled',authors:Array.isArray(authors)&&authors.length?authors:(author?[author]:[]),languages:Array.isArray(languages)?languages:[],authorityIds:ids,edition:ed,cover:{pointer:`dawn://cover/${workId}`,mode:url?'external-authority':'fallback',url},resourceCoverPointer:coverPointer||null,readingPointer:readingPointer||null,authorityBacked:Boolean(authorityBacked)};}
function canonicalRow(w){if(!w)return null;const authors=Array.isArray(w.authors)?w.authors:[];return[w.workId,w.title||'Untitled',authors[0]||'',null,w.readingPointer||null,Boolean(w.authorityBacked),authors,w.languages||[],w.authorityIds||{},w.edition||{}];}
async function loadJson(path,cache='force-cache'){const r=await fetch(`${ROOT}/${path}`,{cache,signal:AbortSignal.timeout(15000)});if(!r.ok)throw new Error(`Resource Fabric ${path} ${r.status}`);return r.json();}
async function loadShard(index){const key=Number(index);if(!shardCache.has(key))shardCache.set(key,loadJson(`work-${hex(key)}.json`));return shardCache.get(key);}
async function loadSegment(path){if(!segmentCache.has(path))segmentCache.set(path,loadJson(path));return segmentCache.get(path);}
function deltaRoutes(manifest,kind,key){return manifest?.delta?.[kind]?.[key]||[];}
async function loadCanonicalShard(meta){const key=meta.href;if(!canonicalCache.has(key))canonicalCache.set(key,fetch(`${CANON}/${key}`,{cache:'force-cache',signal:AbortSignal.timeout(15000)}).then(async r=>{if(!r.ok)throw new Error(`Canonical shard ${r.status}`);const shard=await r.json(),works=shard.works||{};for(const id of Object.keys(works))canonicalShardIndex.set(id,key);return works;}));return canonicalCache.get(key);}function canonicalCandidates(root, workId) {
  // Canonical shards are sorted by Work ID. Older roots without ranges retain
  // their compatibility scan; current roots need only one shard per identity.
  return (root.shards || []).filter(meta => !meta.firstWorkId || !meta.lastWorkId ||
    (workId >= meta.firstWorkId && workId <= meta.lastWorkId));
}
async function canonicalWork(workId) {
  if (canonicalCache.has(workId)) return canonicalCache.get(workId);
  const root = await canonicalRootPromise;
  for (const meta of canonicalCandidates(root, workId)) {
    const works = await loadCanonicalShard(meta);
    if (works[workId]) { canonicalCache.set(workId, works[workId]); return works[workId]; }
  }
  return null;
}
async function overlayWork(manifest,workId){const key=hex(fnv1a(workId)%manifest.workShardCount),routes=deltaRoutes(manifest,'workRoutes',key);for(let i=routes.length-1;i>=0;i--){const seg=await loadSegment(routes[i]),ops=seg.operations||[];for(let j=ops.length-1;j>=0;j--){const op=ops[j];if(op.workId!==workId)continue;if(op.op==='-Work')return null;if(op.op==='+Work')return op.record||null;}}const shard=await loadShard(parseInt(key,16)),base=(shard.rows||[]).find(r=>r[0]===workId);if(base)return base;return canonicalRow(await canonicalWork(workId));}
export async function resourceManifest(){const [manifest,canonical]=await Promise.all([manifestPromise,canonicalRootPromise]);return{...manifest,indexedWorkCount:manifest.workCount,workCount:canonical.workCount,authorityBackedWorks:canonical.authorityBackedWorks,canonicalShardCount:canonical.shardCount};}
export async function resourceWork(workId){if(!workId)return null;const manifest=await manifestPromise,row=await overlayWork(manifest,workId);return row?decode(row):null;}
export async function resourceWorks(workIds = []) {
  const unique = [...new Set(workIds.filter(Boolean))], out = new Map();
  const works = await Promise.all(unique.map(id => resourceWork(id)));
  works.forEach((work, i) => { if (work) out.set(unique[i], work); });
  return out;
}
export async function resourceFeatured({limit = Infinity} = {}) {
  const data = await loadJson('featured.json');
  const ids = (data.rows || []).slice(0, limit).map(row => row[0]);
  const works = await resourceWorks(ids);
  return ids.map(id => works.get(id)).filter(Boolean);
}
export async function resourceSearch(query){const q=String(query||'').trim().toLocaleLowerCase();if(!q)return [];const token=(q.match(/[\p{L}\p{N}_]+/u)||[])[0]||'';if(!token)return [];const prefix=token.slice(0,Math.min(4,token.length)),manifest=await manifestPromise,bucket=fnv1a(prefix)%manifest.searchBucketCount,key=hex(bucket),base=await loadJson(`search-${key}.json`),rows=[...(base.rows||[])];for(const rel of deltaRoutes(manifest,'searchRoutes',key)){const seg=await loadSegment(rel);rows.push(...(seg.searchRows||[]));}const ids=[],seen=new Set();for(let i=rows.length-1;i>=0;i--){const row=rows[i];if(row[0]!==prefix||!`${row[2]} ${row[3]}`.toLocaleLowerCase().includes(q)||seen.has(row[1]))continue;seen.add(row[1]);ids.push(row[1]);}const works=await resourceWorks(ids);return ids.map(id=>works.get(id)).filter(Boolean);}
export function resourceCoverUrl(work){return work?.cover?.url||coverUrl(work?.authorityIds||{},work?.edition||{});}
export const resourceFabric={manifest:resourceManifest,work:resourceWork,works:resourceWorks,featured:resourceFeatured,search:resourceSearch,coverUrl:resourceCoverUrl};
