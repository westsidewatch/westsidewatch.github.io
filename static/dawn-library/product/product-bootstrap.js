import { createLibraryRendererBoundary, assertLibraryRendererBoundary } from './library-renderer-boundary.js';

// Contract-first bootstrap. Semantic ownership is decided here, outside the
// renderer, so future visual rewrites do not move corpus/editorial
// responsibilities again.
const boundary=await createLibraryRendererBoundary();
assertLibraryRendererBoundary(boundary);

Object.defineProperty(globalThis,'__DAWN_LIBRARY_BOUNDARY__',{
  value:boundary,
  configurable:false,
  enumerable:false,
  writable:false
});

await import('./product.js');
await import('./product-finalize.js');

document.documentElement.dataset.libraryOwnership='contract-v1';
