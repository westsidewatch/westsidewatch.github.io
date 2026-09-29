const DEFAULT_CONTRACT={
  schema:'dawn-library-view-model/v1',
  identity:{name:'黎明書局',purpose:'read-and-read-in-Chinese'},
  leftPage:{
    role:'discovery-index',
    primaryEntries:[
      {id:'morning-stars',label:'三晨星',kind:'recommendation-standard'},
      {id:'catalogue',label:'館藏',kind:'catalogue'},
      {id:'search',label:'搜尋',kind:'search'}
    ]
  },
  rightPage:{
    role:'reader',emptyState:'select-work',defaultMode:'bilingual',
    modes:[{id:'source',label:'原文'},{id:'zh-Hant',label:'繁中'},{id:'bilingual',label:'對照'}],
    contentFetch:'on-demand',translation:'dore-language-faculty'
  },
  invariants:{
    threeMorningStarsBelongsToLibrary:true,
    threeMorningStarsIsNotSpectrum:true,
    threeMorningStarsIsNotCuratedCollection:true,
    spectrumAndCuratedCollectionAreSiteLevelEditorialSurfaces:true,
    uiMayBeReplacedWithoutCorpusMigration:true,
    fullTextStoredLocally:false,
    initialFullCatalogueLoad:false
  }
};

export async function loadLibraryContract(){
  try{
    const response=await fetch('../catalogue-ui/view-model.json',{cache:'no-cache'});
    if(response.ok)return {...DEFAULT_CONTRACT,...await response.json()};
  }catch{}
  return structuredClone(DEFAULT_CONTRACT);
}

export function libraryEntries(contract){return contract?.leftPage?.primaryEntries||DEFAULT_CONTRACT.leftPage.primaryEntries}
export function readerModes(contract){return contract?.rightPage?.modes||DEFAULT_CONTRACT.rightPage.modes}
export function isLibrarySurface(id){return ['morning-stars','catalogue','search','reader'].includes(id)}
export function isSiteEditorialSurface(id){return ['spectrum','curated-collection'].includes(id)}
