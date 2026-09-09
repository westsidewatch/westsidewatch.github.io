export const LIBRARY_ORIGIN=Object.freeze({PERSONAL:'personal',DAWN:'dawn'});

export function personalBookEntry(book={}){
  return {
    origin:LIBRARY_ORIGIN.PERSONAL,
    ownership:'user-local',
    editable:true,
    persisted:true,
    bookId:book.id,
    title:book.title||'未命名書稿',
    book
  };
}

export function dawnBookEntry(catalogBook={}){
  return {
    origin:LIBRARY_ORIGIN.DAWN,
    ownership:'catalog-reference',
    editable:false,
    persisted:false,
    catalogId:catalogBook.id,
    title:catalogBook.work?.title||'未命名',
    book:catalogBook
  };
}

export function canDeleteEntry(entry){return entry?.origin===LIBRARY_ORIGIN.PERSONAL&&entry.ownership==='user-local';}
export function canEditEntry(entry){return entry?.origin===LIBRARY_ORIGIN.PERSONAL&&entry.editable===true;}
export function canImportToPersonal(entry){return entry?.origin===LIBRARY_ORIGIN.DAWN;}

export function libraryLayers({personal=[],dawn=[]}={}){
  return {
    personal:personal.map(personalBookEntry),
    dawn:dawn.map(dawnBookEntry)
  };
}
