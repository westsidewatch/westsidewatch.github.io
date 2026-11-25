import * as THREE from 'three';
import {cityObjectIdForMesh} from './city-lifecycle-projection.js';
import {cityVisualRole} from './city-visual-hierarchy.js';
// Screen-space shading bands, not geometry LOD or a historical house-height rule.
// The original model remains the near representation and the export authority.
export const RESIDENTIAL_DISTANCE_BANDS=Object.freeze({farPixelsPerMetre:1.5,nearPixelsPerMetre:5,maxLightingBlend:.45});
export function residentialDistanceWeight(pixelsPerMetre){const {farPixelsPerMetre:a,nearPixelsPerMetre:b,maxLightingBlend:m}=RESIDENTIAL_DISTANCE_BANDS,t=THREE.MathUtils.clamp((pixelsPerMetre-a)/(b-a),0,1);return m*(1-t*t*(3-2*t));}
export function createResidentialDistancePresentation({root,getRecord}){
 const uniforms={j3kResidentialDistanceEnabled:{value:1},j3kResidentialViewportHeight:{value:1}},variants=new Map(),originals=new Map(),centre=new THREE.Vector3();let enabled=true,stats={};
 function style(base){
  if(base.userData.j3kResidentialDistance)return base;
  if(!base.isMeshStandardMaterial&&!base.isMeshLambertMaterial&&!base.isMeshPhongMaterial)return base;
  if(variants.has(base))return variants.get(base);
  const copy=base.clone(),compile=base.onBeforeCompile,key=base.customProgramCacheKey.bind(base);
  copy.userData.j3kResidentialDistance=true;
  copy.onBeforeCompile=function(shader,...args){compile.call(this,shader,...args);Object.assign(shader.uniforms,uniforms);
   shader.vertexShader='uniform float j3kResidentialViewportHeight; varying float vJ3kResidentialPixelsPerMetre;\n'+shader.vertexShader.replace('#include <project_vertex>','#include <project_vertex>\nvJ3kResidentialPixelsPerMetre=.5*j3kResidentialViewportHeight*projectionMatrix[1][1]/max(.01,-mvPosition.z);');
   shader.fragmentShader='uniform float j3kResidentialDistanceEnabled; varying float vJ3kResidentialPixelsPerMetre;\n'+shader.fragmentShader.replace('#include <opaque_fragment>',`// Suppress sub-pixel facade contrast while keeping every roof/court silhouette.
float j3kResidentialSide=smoothstep(.15,.65,1.-abs(dot(normal,normalize((viewMatrix*vec4(0.,1.,0.,0.)).xyz))));
float j3kResidentialBlend=j3kResidentialDistanceEnabled*${RESIDENTIAL_DISTANCE_BANDS.maxLightingBlend.toFixed(4)}*(1.-smoothstep(${RESIDENTIAL_DISTANCE_BANDS.farPixelsPerMetre.toFixed(4)},${RESIDENTIAL_DISTANCE_BANDS.nearPixelsPerMetre.toFixed(4)},vJ3kResidentialPixelsPerMetre))*j3kResidentialSide;
if(j3kResidentialBlend>0.)outgoingLight=mix(outgoingLight,diffuseColor.rgb*.6,j3kResidentialBlend);
#include <opaque_fragment>`);
  };
  copy.customProgramCacheKey=()=>key()+':j3k-residential-distance-v1';copy.needsUpdate=true;variants.set(base,copy);return copy;
 }
 return {
  apply({camera,viewportHeight,phase}){
   uniforms.j3kResidentialViewportHeight.value=Math.max(1,viewportHeight);uniforms.j3kResidentialDistanceEnabled.value=enabled?1:0;
   root.updateMatrixWorld(true);
   const topology={trackedMeshes:0,referenceTriangles:0,renderedTriangles:0,omittedTriangles:0,referencePositionBytes:0,positionBytes:0,generationMilliseconds:0};const counts={near:0,middle:0,far:0},objects=new Set();let eligibleMeshes=0;
   root.traverse(mesh=>{if(!mesh.isMesh||mesh.userData.displayAnnotation)return;for(let p=mesh;p;p=p.parent)if(!p.visible)return;const id=cityObjectIdForMesh(mesh),record=id&&getRecord(id);if(cityVisualRole(record,mesh)!=='housing'||(!mesh.userData.overview&&!['building','block'].includes(record.type)))return;
    const source=mesh.material,materials=[].concat(source);if(!materials.some(m=>m.userData.j3kResidentialDistance||m.isMeshStandardMaterial||m.isMeshLambertMaterial||m.isMeshPhongMaterial))return;
    if(!originals.has(mesh))originals.set(mesh,source);mesh.material=Array.isArray(source)?source.map(style):style(source);eligibleMeshes++;objects.add(id);const economy=mesh.geometry.userData.housingTopology;if(economy){topology.trackedMeshes++;for(const k of ['referenceTriangles','renderedTriangles','omittedTriangles','referencePositionBytes','positionBytes','generationMilliseconds'])topology[k]+=economy[k];}
    if(!mesh.geometry.boundingSphere)mesh.geometry.computeBoundingSphere();if(mesh.geometry.boundingSphere)centre.copy(mesh.geometry.boundingSphere.center);else centre.set(0,0,0);centre.applyMatrix4(mesh.matrixWorld);centre.applyMatrix4(camera.matrixWorldInverse);const ppm=.5*viewportHeight*camera.projectionMatrix.elements[5]/Math.max(.01,-centre.z);counts[ppm>=RESIDENTIAL_DISTANCE_BANDS.nearPixelsPerMetre?'near':ppm<=RESIDENTIAL_DISTANCE_BANDS.farPixelsPerMetre?'far':'middle']++;
   });
   stats={phase,enabled,housingTopology:topology,eligibleMeshes,objects:objects.size,bands:counts,materialVariants:variants.size,viewportHeight,bandsPixelsPerMetre:RESIDENTIAL_DISTANCE_BANDS,geometryChanged:false,drawCallReduction:0,triangleReduction:0,evidenceReclassified:false,historicalTypologyVerified:false};return stats;
  },
  set(value){enabled=Boolean(value);uniforms.j3kResidentialDistanceEnabled.value=enabled?1:0;return enabled;},
  diagnostics:()=>structuredClone(stats),
  dispose(){for(const[mesh,material]of originals)mesh.material=material;for(const material of variants.values())material.dispose();originals.clear();variants.clear();}
 };
}
