import { createLibraryRendererBoundary, assertLibraryRendererBoundary } from './library-renderer-boundary.js';

// Contract-first bootstrap. The legacy renderer is temporary: semantic
// ownership is decided here, outside product.js, so future visual rewrites do
// not move corpus/editorial responsibilities again.
const boundary=await createLibraryRendererBoundary();
assertLibraryRendererBoundary(boundary);

Object.defineProperty(globalThis,'__DAWN_LIBRARY_BOUNDARY__',{
  value:boundary,
  configurable:false,
  enumerable:false,
  writable:false
});

await import('./product.js');

// First contraction step: site-level editorial surfaces may still be produced
// by the legacy renderer during migration, but they are not allowed to remain
// in the Dawn Library surface. Data is untouched and can be rendered by the
// site-level editorial consumer later.
function enforceLibraryOwnership(root=document){
  if(boundary.delegates('curated-collection')){
    root.querySelectorAll('.curated-collections').forEach(node=>node.remove());
  }
  document.documentElement.dataset.libraryOwnership='contract-v1';
}

enforceLibraryOwnership();

// Guard against late async legacy rendering while product.js is being split.
const ownershipGuard=new MutationObserver(()=>enforceLibraryOwnership());
ownershipGuard.observe(document.body,{childList:true,subtree:true});

window.addEventListener('pagehide',()=>ownershipGuard.disconnect(),{once:true});
