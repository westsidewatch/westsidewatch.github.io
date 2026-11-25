import * as THREE from 'three';
// On-demand diagnostics only; no traversal or ground sampling per render frame.
export function inspectRoadSurfaceContact(root,terrain){
 const ids=new Set(),point=new THREE.Vector3();let meshes=0,triangles=0,maxError=0,outsideTerrain=0;
 root.updateMatrixWorld(true);
 root.traverseVisible(m=>{if(!m.isMesh||!m.geometry.userData.roadSurface)return;meshes++;ids.add(m.userData.cityObject?.objectId);const p=m.geometry.attributes.position;triangles+=p.count/3;
  for(let i=0;i<p.count;i+=3){point.set((p.getX(i)+p.getX(i+1)+p.getX(i+2))/3,(p.getY(i)+p.getY(i+1)+p.getY(i+2))/3,(p.getZ(i)+p.getZ(i+1)+p.getZ(i+2))/3).applyMatrix4(m.matrixWorld);const ground=terrain.heightAtWorld(point.x,point.z);if(!Number.isFinite(ground))outsideTerrain++;else maxError=Math.max(maxError,Math.abs(point.y-ground-.35));}
 });return {meshes,triangles,roadIds:[...ids].sort(),maxOffsetErrorMetres:maxError,outsideTerrain,offsetMetres:.35,scope:'shared-paving-builder-only-not-every-path-or-ancient-level',ancientStreetLevelVerified:false};
}
