import { loadLibraryContract, libraryEntries, readerModes, isLibrarySurface, isSiteEditorialSurface } from './library-contract.js';

const PUBLICATION_TYPES=Object.freeze(['work','book','publication','manuscript']);

/**
 * Stable renderer boundary for Dawn Library.
 *
 * Dawn Library is a publication product projection over the global Resource
 * Fabric. AV, maps, places, tools and datasets remain global resources but are
 * never owned or rendered by this product boundary.
 */
export async function createLibraryRendererBoundary(){
  const contract=await loadLibraryContract();
  return Object.freeze({
    contract,
    navigation:libraryEntries(contract),
    readerModes:readerModes(contract),
    resourceTypes:PUBLICATION_TYPES,
    acceptsResourceType(type){
      return PUBLICATION_TYPES.includes(String(type||'').trim().toLowerCase());
    },
    owns(surfaceId){return isLibrarySurface(surfaceId)},
    delegates(surfaceId){return isSiteEditorialSurface(surfaceId)},
    renderPolicy:Object.freeze({
      library:['morning-stars','catalogue','chinese-collection','search','reader'],
      siteEditorial:['spectrum','curated-collection'],
      resourceProjection:'publication-only',
      fullCatalogueInitialLoad:false,
      contentFetch:'on-demand'
    })
  });
}

export function assertLibraryRendererBoundary(boundary){
  if(!boundary?.contract)throw new Error('Dawn Library contract unavailable');
  if(boundary.owns('curated-collection'))throw new Error('Curated Collection must not be owned by Dawn Library renderer');
  if(!boundary.owns('morning-stars'))throw new Error('Three Morning Stars must remain a Dawn Library recommendation surface');
  if(!boundary.owns('reader'))throw new Error('Reader must remain owned by Dawn Library');
  for(const forbidden of ['video','audio','map','place','tool','dataset','resource']){
    if(boundary.acceptsResourceType(forbidden))throw new Error(`Dawn Library must reject non-publication resource type: ${forbidden}`);
  }
  for(const required of PUBLICATION_TYPES){
    if(!boundary.acceptsResourceType(required))throw new Error(`Dawn Library publication type missing: ${required}`);
  }
  return true;
}
