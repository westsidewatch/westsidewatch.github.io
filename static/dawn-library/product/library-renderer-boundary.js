import { loadLibraryContract, libraryEntries, readerModes, isLibrarySurface, isSiteEditorialSurface } from './library-contract.js';

/**
 * Stable renderer boundary for Dawn Library.
 *
 * product.js may keep its current visual implementation while this module owns
 * the semantic split between the library reader and site-level editorial
 * surfaces. This lets the renderer be reformatted/replaced without moving
 * corpus, translation, recommendation or catalogue responsibilities again.
 */
export async function createLibraryRendererBoundary(){
  const contract=await loadLibraryContract();
  return Object.freeze({
    contract,
    navigation:libraryEntries(contract),
    readerModes:readerModes(contract),
    owns(surfaceId){return isLibrarySurface(surfaceId)},
    delegates(surfaceId){return isSiteEditorialSurface(surfaceId)},
    renderPolicy:Object.freeze({
      library:['morning-stars','catalogue','search','reader'],
      siteEditorial:['spectrum','curated-collection'],
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
  return true;
}
