import { createLibraryRendererBoundary, assertLibraryRendererBoundary } from './library-renderer-boundary.js';

// Contract-first bootstrap. The existing renderer is imported only after the
// semantic boundary is available and validated. No DOM or visual behaviour is
// changed by this bootstrap itself.
const boundary=await createLibraryRendererBoundary();
assertLibraryRendererBoundary(boundary);

Object.defineProperty(globalThis,'__DAWN_LIBRARY_BOUNDARY__',{
  value:boundary,
  configurable:false,
  enumerable:false,
  writable:false
});

await import('./product.js');
