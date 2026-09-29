const TEXT_PROXY_ROOT='/dawn-library/reading';

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

async function json(url){const r=await fetch(url,{cache:'no-store'});if(!r.ok)throw new Error(`reading source ${r.status}`);return r.json();}

export async function resolveReading(work={}){
  const descriptor=readingDescriptor(work);
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
  if(reading?.kind==='text'&&reading.text)return {available:true,mode:'text-ready',target:'zh-Hant'};
  return {available:false,mode:'requires-dore-language-runtime',target:'zh-Hant'};
}

export const dawnReadingResolver={descriptor:readingDescriptor,resolve:resolveReading,translationCapability:readingTranslationCapability};
