import { resourceManifest, resourceWorks } from '../js/resource-fabric-client.mjs';

const SURFACE_ROOT='/dawn-library/surfaces/';
const forbidden=/wikisource|openlibrary\.org/i;

async function json(url){const r=await fetch(url,{cache:'no-store'});if(!r.ok)throw new Error(`${url} ${r.status}`);return r.json();}

export async function canonicalIndex(){
  const manifest=await resourceManifest();
  if(manifest?.identityAuthority!=='Dawn'||manifest?.canonicalMonolithRequired!==false)throw new Error('Resource Fabric canonical boundary mismatch');
  return {
    schema:'dawn.library.canonical-index.resource-fabric.v1',
    identityAuthority:'Dawn',
    workCount:manifest.workCount,
    authorityBackedWorks:manifest.authorityBackedWorks,
    runtimePolicy:{surfaceOwnsIdentity:false,openLibraryRuntime:false,wikisource:'forbidden',canonicalMonolithRequired:false}
  };
}

export async function canonicalCoverRegistry(){
  return {schema:'dawn.library.cover-registry.resource-fabric.v1',runtimePolicy:{browserExternalLookup:false,wikisource:'forbidden'},covers:{}};
}

export async function canonicalSurface(name){
  const [index,surface]=await Promise.all([canonicalIndex(),json(`${SURFACE_ROOT}${name}.json`)]);
  if(surface?.schema!=='dawn.library.surface.v1')throw new Error('Dawn surface schema mismatch');
  const refs=Array.isArray(surface.shelves)?surface.shelves.flatMap(s=>s.items||[]):(surface.items||[]);
  const ids=refs.map(ref=>ref?.workId).filter(Boolean);
  const works=await resourceWorks(ids);
  const resolve=ref=>{
    const work=works.get(ref?.workId);
    if(!ref?.workId||!work)throw new Error(`unresolved Resource Fabric Work ID: ${ref?.workId||'missing'}`);
    return {ref,work};
  };
  if(Array.isArray(surface.shelves))return {...surface,identityAuthority:index.identityAuthority,shelves:surface.shelves.map(s=>({...s,items:(s.items||[]).map(resolve)}))};
  return {...surface,identityAuthority:index.identityAuthority,items:(surface.items||[]).map(resolve)};
}

export async function canonicalCover(work={}){
  const url=String(work?.resourceCoverPointer||'');
  if(!url||!url.startsWith('/dawn-library/covers/')||forbidden.test(url)||/^https?:\/\//i.test(url))return null;
  return {url,kind:'canonical-local',provider:'Dawn',provenance:'Resource Fabric projection',contentType:null,sha256:null};
}

export function canonicalReadHref(work={}){
  const pointer=work?.readingPointer||'';
  if(!pointer||forbidden.test(pointer)||/^https?:\/\//i.test(pointer))return null;
  return pointer.startsWith('/')?pointer:null;
}

export function canonicalBook(pair={}){
  const work=pair.work||{},ref=pair.ref||{};
  return {
    id:work.workId,
    workId:work.workId,
    work:{title:work.title||'未命名',author:(work.authors||[]).join(', '),language:(work.languages||[])[0]||'',identifiers:work.authorityIds||{}},
    edition:work.edition||{},
    cover:work.cover||null,
    readingPointer:work.readingPointer||null,
    relations:ref.relations||[],
    canonical:true,
    resourceFabric:true
  };
}
