import * as THREE from 'three';
// Reversible presentation only: original geometry/materials/evidence stay intact.
export function createTempleSectionView(){
 let enabled=false;const entries=new Map();
 function update(root){
  if(!enabled)return;
  root.traverse(mesh=>{
   if(!mesh.isMesh||!Number.isFinite(mesh.userData.templeSectionHeight)||entries.has(mesh))return;
   const original=mesh.material;if(Array.isArray(original))return;
   const material=original.clone();
   material.onBeforeCompile=original.onBeforeCompile;
   material.customProgramCacheKey=original.customProgramCacheKey;
   material.clippingPlanes=[new THREE.Plane(new THREE.Vector3(0,-1,0),mesh.userData.templeSectionHeight)];
   material.clipShadows=true;material.needsUpdate=true;
   // Hide upper construction shadows with exactly the same presentation plane.
   const depth=mesh.customDepthMaterial,sectionDepth=depth?.clone();
   if(sectionDepth){sectionDepth.onBeforeCompile=depth.onBeforeCompile;sectionDepth.customProgramCacheKey=depth.customProgramCacheKey;sectionDepth.clippingPlanes=material.clippingPlanes;sectionDepth.clipShadows=true;mesh.customDepthMaterial=sectionDepth;}
   entries.set(mesh,{original,material,depth,sectionDepth});mesh.material=material;
  });
 }
 function restore(){for(const [mesh,e]of entries){mesh.material=e.original;mesh.customDepthMaterial=e.depth;e.material.dispose();e.sectionDepth?.dispose();}entries.clear();}
 return {set(value,root){enabled=Boolean(value);if(enabled)update(root);else restore();return enabled;},update,diagnostics(){return{enabled,clippedMeshes:entries.size,mode:'interpretive-horizontal-cut-not-historical-demolition'};},dispose(){enabled=false;restore();}};
}
