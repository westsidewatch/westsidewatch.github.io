import {bookAllowed} from '../resources/resource-selection.mjs';
export const LIBRARY_ORIGIN=Object.freeze({PERSONAL:'personal',DAWN:'dawn'});

function makePersonalId(catalogId='book'){
  const safe=String(catalogId||'book').replace(/[^a-z0-9-]+/gi,'-').replace(/^-+|-+$/g,'').toLowerCase()||'book';
  return `book-dawn-${safe}-${Date.now().toString(36)}`;
}

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
export function canImportToPersonal(entry){return entry?.origin===LIBRARY_ORIGIN.DAWN&&bookAllowed(entry.book);}

export function createPersonalReferenceFromDawn(catalogBook={}){
  if(!bookAllowed(catalogBook))throw new Error('此資源未通過書籍與內容審核，無法加入館藏');
  if(!catalogBook?.id)throw new Error('黎明書局條目缺少 catalog id');
  const now=new Date().toISOString();
  const work=catalogBook.work||{},edition=catalogBook.edition||{},sources=Array.isArray(catalogBook.sources)?catalogBook.sources:[];
  const preferredSource=sources.find(source=>source?.url)||null;
  const title=work.title||'未命名';
  const author=work.author||'';
  return {
    schema:'multiwrite.book.v2',
    id:makePersonalId(catalogBook.id),
    title,
    subtitle:author,
    createdAt:now,
    updatedAt:now,
    library:{
      origin:LIBRARY_ORIGIN.PERSONAL,
      ownership:'user-local',
      intake:'dawn-reference',
      sourceCatalog:'dawn-library',
      catalogId:catalogBook.id,
      sourceStorage:'remote-on-demand',
      contentDownloaded:false
    },
    identity:{work:{...work},edition:{...edition}},
    cover:catalogBook.cover?{...catalogBook.cover}:null,
    relations:[...(catalogBook.relations||[])],
    sources:sources.map(source=>({...source})),
    import:{mode:'dawn-reference',aiTransformed:false,sourceCount:sources.length,sources:sources.map(source=>({...source}))},
    nodes:[{
      id:`remote-${catalogBook.id}`,
      role:'front_matter',
      title:'閱讀入口',
      content:[
        '這本書來自黎明書局的公版館藏索引。',
        '',
        '全文未下載到多寫；閱讀時按需從核定的公開來源取得。',
        preferredSource?.url?`\n來源：${preferredSource.provider||'Public source'}\n${preferredSource.url}`:'\n公開全文來源整理中。'
      ].join('\n'),
      sourceFile:'Dawn Library',
      order:0,
      headingLevel:1,
      remote:true,
      sourceRef:preferredSource?{...preferredSource}:null
    }]
  };
}

export function libraryLayers({personal=[],dawn=[]}={}){
  return {
    personal:personal.map(personalBookEntry),
    dawn:dawn.filter(bookAllowed).map(dawnBookEntry)
  };
}
