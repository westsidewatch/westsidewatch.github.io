const TEXT_PROXY_ROOT='/dawn-library/reading';
const POINTER_MAP='/dawn-library/reading-pointer-map.json';
const READING_PACK_INDEX='/dawn-library/reading-packs/index.json';
let pointerMapPromise;
let readingPackIndexPromise;

function clean(value){return String(value||'').trim();}
function ol(value,kind){const v=clean(value);return new RegExp(`^OL\\d+${kind}$`,'i').test(v)?v:null;}

export function readingDescriptor(work={}){
  const pointer=clean(work.readingPointer);
  const ids=work.authorityIds||{};
  const edition=work.edition||{};
  const isbn=clean(ids.isbn||edition.isbn).replace(/[^0-9Xx]/g,'');
  const editionId=ol(edition.editionId,'M');
  const workId=ol(ids.openLibraryWork,'W');
  return {
    schema:'dawn.reading-descriptor/v1',
    workId:clean(work.workId),
    readingPointer:pointer||null,
    authority:{isbn:isbn||null,openLibraryEdition:editionId,openLibraryWork:workId},
    localText:pointer&&pointer.startsWith('dawn://reading/')?`${TEXT_PROXY_ROOT}/${encodeURIComponent(pointer.slice('dawn://reading/'.length))}.json`:null,
    sourcePage:editionId?`https://openlibrary.org/books/${editionId}`:workId?`https://openlibrary.org/works/${workId}`:isbn?`https://openlibrary.org/isbn/${isbn}`:null
  };
}

async function json(url){const r=await fetch(url,{cache:'no-store',signal:AbortSignal.timeout(15000)});if(!r.ok)throw new Error(`reading source ${r.status}`);return r.json();}

async function mappedPointer(workId){
  if(!workId)return null;
  try{
    pointerMapPromise ||= json(POINTER_MAP);
    const map=await pointerMapPromise;
    return (map?.items||[]).find(item=>item.workId===workId)||null;
  }catch{
    return null;
  }
}

/**
 * Reading packs are published with Dawn itself. They are deliberately bounded
 * bilingual segments—not a proxy or downloader for a remote corpus.
 */
export async function localReadingPack(workId){
  if(!workId)return null;
  try{
    readingPackIndexPromise ||= json(READING_PACK_INDEX);
    const index=await readingPackIndexPromise;
    const entry=(index?.items||[]).find(item=>item.workId===workId);
    if(!entry?.href)return null;
    const pack=await json(`${READING_PACK_INDEX.slice(0,READING_PACK_INDEX.lastIndexOf('/')+1)}${encodeURIComponent(entry.href)}`);
    if(pack?.workId!==workId||!Array.isArray(pack?.segments))return null;
    return pack;
  }catch{
    return null;
  }
}

export async function resolveReading(work={}){
  const mapped=await mappedPointer(clean(work.workId));
  const pointer=clean(work.readingPointer)||clean(mapped?.readingPointer);
  const descriptor=readingDescriptor({...work,readingPointer:pointer});
  // Project Gutenberg is a human-reader surface. Keep its text at the source
  // and hand the reader to its canonical page instead of fetching or copying it.
  if(mapped?.accessMode==='external_reader'&&mapped?.sourceUrl){
    return {ok:true,kind:'external-reader',descriptor,provider:mapped.provider||'external source',sourcePage:mapped.sourceUrl,text:null,translation:null};
  }
  if(descriptor.localText){
    try{
      const payload=await json(descriptor.localText);
      if(payload?.text||payload?.sourceText)return {ok:true,kind:'text',descriptor,text:payload.text||payload.sourceText,language:payload.language||null,translation:payload.translation||null};
    }catch(error){/* canonical text not materialized yet; continue to authority handoff */}
  }
  if(descriptor.sourcePage)return {ok:true,kind:'authority-handoff',descriptor,sourcePage:descriptor.sourcePage,text:null,translation:null};
  return {ok:false,kind:'unavailable',descriptor,text:null,translation:null};
}

export function readingTranslationCapability(reading){
  if(reading?.pack?.segments?.length)return {available:true,mode:'local-reading-pack',target:'zh-Hant'};
  if(reading?.kind==='text'&&reading.text)return {available:true,mode:'text-ready',target:'zh-Hant'};
  return {available:false,mode:'awaiting-local-reading-pack',target:'zh-Hant'};
}

export const dawnReadingResolver={descriptor:readingDescriptor,resolve:resolveReading,localReadingPack,translationCapability:readingTranslationCapability};
