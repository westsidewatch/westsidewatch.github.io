import * as THREE from 'three';
import {cityObjectIdForMesh} from './city-lifecycle-projection.js';
import {cityVisualRole} from './city-visual-hierarchy.js';

// A transient render submission, not a new historical object or house layout.
// Source visibility, geometry and ledger bindings remain authoritative.
export function createResidentialRenderBatches({root,parent,getRecord,tileMetres=96,maxMeshes=64,maxVertices=32768,minMeshes=4,nearNdcRadius=.12}){
 if(!(Number.isFinite(tileMetres)&&tileMetres>0&&Number.isInteger(maxMeshes)&&Number.isInteger(minMeshes)&&minMeshes>=2&&maxMeshes>=minMeshes&&Number.isInteger(maxVertices)&&maxVertices>=3&&Number.isFinite(nearNdcRadius)&&nearNdcRadius>0))throw new Error('Invalid housing batch budget');
 const group=new THREE.Group();group.name='residential-render-submissions';group.visible=false;parent.add(group);
 const savedLayers=[],cache=new Map(),materialCache=new WeakMap(),layoutCache=new WeakMap(),functions=new WeakMap(),centre=new THREE.Vector3(),viewCentre=new THREE.Vector3(),vector=new THREE.Vector3(),normalMatrix=new THREE.Matrix3(),identityMatrix=new THREE.Matrix4();
 const materialIntern=new Map();let frameMaterialKeys=new Map();
 let functionSerial=0,enabled=true,phase=null,stats={},disposed=false,totalBuilds=0;
 const functionKey=f=>{if(!functions.has(f))functions.set(f,++functionSerial);return functions.get(f);};
 const materialScalars=['opacity','roughness','metalness','emissiveIntensity','envMapIntensity','side','vertexColors','flatShading','depthTest','depthWrite','colorWrite','blending','blendSrc','blendDst','blendEquation','blendSrcAlpha','blendDstAlpha','blendEquationAlpha','premultipliedAlpha','polygonOffset','polygonOffsetFactor','polygonOffsetUnits','dithering','toneMapped','wireframe','wireframeLinewidth','alphaTest','alphaHash','alphaToCoverage','clipIntersection','clipShadows','fog','visible'];
 const textureKeys=['map','alphaMap','normalMap','bumpMap','roughnessMap','metalnessMap','aoMap','lightMap','emissiveMap','displacementMap','envMap'];
 function rawMaterialKey(material){
  if(material?.onBeforeRender!==THREE.Material.prototype.onBeforeRender)return null;
  if(!material?.isMeshStandardMaterial||material.type!=='MeshStandardMaterial'||material.transparent||material.opacity!==1||!material.visible)return null;
  for(const k of textureKeys)if(material[k])return null;
  if(material.onBeforeCompile!==THREE.Material.prototype.onBeforeCompile&&!material.userData.j3kResidentialDistance)return null;
  const clips=material.clippingPlanes||[];for(const p of clips)if(p.constant<1e8||!Number.isFinite(p.constant))return null;
  const old=materialCache.get(material),c=material.color,e=material.emissive;
  let same=old&&old.version===material.version&&old.compile===material.onBeforeCompile&&old.program===material.customProgramCacheKey&&old.colors[0]===c.r&&old.colors[1]===c.g&&old.colors[2]===c.b&&old.colors[3]===e.r&&old.colors[4]===e.g&&old.colors[5]===e.b&&old.clips.length===clips.length*4;
  if(same){for(let i=0;i<materialScalars.length;i++)if(old.scalars[i]!==material[materialScalars[i]]){same=false;break;}}
  if(same){for(let i=0;i<clips.length;i++){const p=clips[i],j=i*4;if(old.clips[j]!==p.normal.x||old.clips[j+1]!==p.normal.y||old.clips[j+2]!==p.normal.z||old.clips[j+3]!==p.constant){same=false;break;}}}
  if(same)return old.key;
  const colors=[c.r,c.g,c.b,e.r,e.g,e.b],scalars=materialScalars.map(k=>material[k]),planes=clips.flatMap(p=>[p.normal.x,p.normal.y,p.normal.z,p.constant]);
  const key=[...colors,...scalars,...planes].join(',')+'|'+functionKey(material.onBeforeCompile)+'|'+material.customProgramCacheKey();materialCache.set(material,{version:material.version,compile:material.onBeforeCompile,program:material.customProgramCacheKey,colors,scalars,clips:planes,key});return key;
 }
 function materialKey(material){
  if(frameMaterialKeys.has(material))return frameMaterialKeys.get(material);const raw=rawMaterialKey(material);let id=null;if(raw!==null){if(!materialIntern.has(raw))materialIntern.set(raw,materialIntern.size+1);id=materialIntern.get(raw);}frameMaterialKeys.set(material,id);return id;
 }
 function layoutKey(geometry){
  const attrs=geometry.attributes,p=attrs.position,n=attrs.normal,c=attrs.color;
  if(geometry.index||geometry.groups.length||Object.keys(geometry.morphAttributes).length||geometry.drawRange.start!==0||geometry.drawRange.count<p?.count)return null;
  if(!p||p.count<3||p.count%3||!n||p.itemSize!==3||n.itemSize!==3||n.count!==p.count||p.normalized||n.normalized||p.isInterleavedBufferAttribute||n.isInterleavedBufferAttribute||!(p.array instanceof Float32Array)||!(n.array instanceof Float32Array))return null;
  if(c&&(c.itemSize!==3||c.count!==p.count||c.normalized||c.isInterleavedBufferAttribute||!(c.array instanceof Float32Array)))return null;
  const keys=Object.keys(attrs),old=layoutCache.get(geometry);if(old&&old.p===p&&old.n===n&&old.c===c&&old.length===keys.length)return old.key;
  if(keys.some(k=>!['position','normal','color'].includes(k)))return null;const key=keys.sort().join(',');layoutCache.set(geometry,{p,n,c,length:keys.length,key});return key;
 }
 function release(entry){entry.mesh.removeFromParent();entry.mesh.geometry.dispose();}
 function clear(){for(const e of cache.values())release(e);cache.clear();}
 function restore(){for(const m of savedLayers)m.layers.mask=1;savedLayers.length=0;group.visible=false;if(stats)stats.sourceLayersRestored=true;}
 function unchanged(entry,members){
  if(entry.members.length!==members.length)return false;for(let i=0;i<members.length;i++){const m=members[i],s=entry.states[i];if(m!==entry.members[i]||m.geometry!==s.geometry)return false;for(const k in m.geometry.attributes){const a=m.geometry.attributes[k],old=s.attributes[k];if(a!==old.attribute||a.version!==old.version)return false;}const matrix=m.matrixWorld.elements;for(let j=0;j<16;j++)if(matrix[j]!==s.matrix[j])return false;}return true;
 }
 function build(members,material){
  const names=Object.keys(members[0].geometry.attributes),count=members.reduce((n,m)=>n+m.geometry.attributes.position.count,0),geometry=new THREE.BufferGeometry();
  for(const name of names)geometry.setAttribute(name,new THREE.BufferAttribute(new Float32Array(count*3),3));
  let offset=0;const ranges=[];for(const source of members){const attrs=source.geometry.attributes,matrix=source.matrixWorld,identity=matrix.equals(identityMatrix);normalMatrix.getNormalMatrix(matrix);
   for(const name of names){const input=attrs[name],output=geometry.attributes[name].array;if(identity||name==='color')output.set(input.array,offset*3);else for(let i=0;i<input.count;i++){vector.fromBufferAttribute(input,i);if(name==='position')vector.applyMatrix4(matrix);else vector.applyNormalMatrix(normalMatrix);vector.toArray(output,(offset+i)*3);}}
   ranges.push({objectId:cityObjectIdForMesh(source),componentId:source.userData.cityObject?.componentId||source.uuid,firstVertex:offset,vertexCount:attrs.position.count});offset+=attrs.position.count;
  }
  geometry.computeBoundingBox();geometry.computeBoundingSphere();const mesh=new THREE.Mesh(geometry,material);mesh.castShadow=members[0].castShadow;mesh.receiveShadow=members[0].receiveShadow;mesh.renderOrder=members[0].renderOrder;
  mesh.userData.renderSubmission={kind:'housing-batch',sourceObjectIds:[...new Set(members.map(cityObjectIdForMesh))],ranges,historicalObject:false};group.add(mesh);totalBuilds++;
  return {mesh,members:[...members],states:members.map(m=>({geometry:m.geometry,attributes:Object.fromEntries(Object.entries(m.geometry.attributes).map(([k,a])=>[k,{attribute:a,version:a.version}])),matrix:[...m.matrixWorld.elements]}))};
 }
 return {
  apply({camera,phase:nextPhase,matricesReady=false}){
   if(disposed)throw new Error('Housing batch renderer disposed');restore();frameMaterialKeys.clear();if(nextPhase!==phase){clear();materialIntern.clear();phase=nextPhase;}
   stats={phase,enabled,eligibleMeshes:0,batchedSourceMeshes:0,batchMeshes:0,estimatedSubmissionsAvoided:0,ownedGeometryBytes:0,rebuildMilliseconds:0,rebuilds:0,totalBuilds,sourceLayersRestored:true,sourceGeometryOrEvidenceChanged:false,sourceMappingPreserved:true,additionalGeometryCache:'current-phase-only'};
   if(!enabled){clear();return stats;}if(camera.layers.mask!==1)return stats;if(!matricesReady){root.updateMatrixWorld(true);camera.updateMatrixWorld();}
   const groups=new Map();root.traverseVisible(mesh=>{
    if(!mesh.isMesh||mesh.isInstancedMesh||mesh.isBatchedMesh||mesh.isSkinnedMesh||mesh.customDepthMaterial||mesh.customDistanceMaterial||mesh.userData.displayAnnotation||mesh.layers.mask!==1||Array.isArray(mesh.material))return;
    const id=cityObjectIdForMesh(mesh),record=id&&getRecord(id);if(cityVisualRole(record,mesh)!=='housing'||!['building','block'].includes(record.type)||mesh.geometry.userData.overviewGrammar!=='terrain-courtyard-mass-v1')return;
    const schema=layoutKey(mesh.geometry),material=materialKey(mesh.material);if(!schema||material===null||mesh.geometry.attributes.position.count>maxVertices||mesh.matrixWorld.determinant()<=0)return;
    if(['onBeforeRender','onAfterRender','onBeforeShadow','onAfterShadow'].some(k=>mesh[k]!==THREE.Object3D.prototype[k]))return;
    if(!mesh.geometry.boundingSphere)mesh.geometry.computeBoundingSphere();centre.copy(mesh.geometry.boundingSphere.center).applyMatrix4(mesh.matrixWorld);viewCentre.copy(centre).applyMatrix4(camera.matrixWorldInverse);const radius=mesh.geometry.boundingSphere.radius*mesh.matrixWorld.getMaxScaleOnAxis();if(-viewCentre.z<=0||radius*camera.projectionMatrix.elements[5]/(-viewCentre.z)>nearNdcRadius)return;
    const key=[Math.floor(centre.x/tileMetres),Math.floor(centre.z/tileMetres),record.type,record.confidence,mesh.userData.cityObject?.lifecycleState||mesh.userData.cityRuinFactor||'current-source-state',mesh.castShadow,mesh.receiveShadow,mesh.renderOrder,schema,material].join('|');
    if(!groups.has(key))groups.set(key,[]);groups.get(key).push(mesh);stats.eligibleMeshes++;
   });
   const keep=new Set(),pending=[];for(const[key,members]of groups){let chunk=[],vertices=0,index=0;const submit=()=>{if(chunk.length<minMeshes)return;const cacheKey=key+'#'+index++,prior=cache.get(cacheKey);let entry=prior;if(!entry||!unchanged(entry,chunk)){const start=performance.now();entry=build(chunk,chunk[0].material);if(prior)release(prior);cache.set(cacheKey,entry);stats.rebuildMilliseconds+=performance.now()-start;stats.rebuilds++;}else entry.mesh.material=chunk[0].material;keep.add(cacheKey);pending.push(entry);};
    for(const mesh of members){const n=mesh.geometry.attributes.position.count;if(chunk.length&&(chunk.length>=maxMeshes||vertices+n>maxVertices)){submit();chunk=[];vertices=0;}chunk.push(mesh);vertices+=n;}submit();
   }
   for(const[key,entry]of cache)if(!keep.has(key)){release(entry);cache.delete(key);}
   // No source is suppressed until every replacement is ready. Restore in the
   // renderer's finally block so inspections and future projections see sources.
   for(const entry of pending){for(const mesh of entry.members){savedLayers.push(mesh);mesh.layers.disable(0);}stats.batchedSourceMeshes+=entry.members.length;stats.batchMeshes++;for(const a of Object.values(entry.mesh.geometry.attributes))stats.ownedGeometryBytes+=a.array.byteLength;}
   group.visible=pending.length>0;stats.estimatedSubmissionsAvoided=stats.batchedSourceMeshes-stats.batchMeshes;stats.totalBuilds=totalBuilds;stats.sourceLayersRestored=savedLayers.length===0;return stats;
  },
  restore,
  set(value){restore();enabled=Boolean(value);if(!enabled)clear();return enabled;},
  diagnostics({includeObjectIds=false}={}){return {...stats,...(includeObjectIds?{batches:[...cache.values()].map(e=>({batchId:e.mesh.uuid,sourceObjectIds:[...e.mesh.userData.renderSubmission.sourceObjectIds],sourceComponents:e.members.map(m=>m.uuid),ranges:e.mesh.userData.renderSubmission.ranges.map(r=>({...r})),triangles:e.mesh.geometry.attributes.position.count/3}))}:{})};},
  resolve(batchId,faceIndex){if(!Number.isInteger(faceIndex)||faceIndex<0)return null;const entry=[...cache.values()].find(e=>e.mesh.uuid===batchId);const r=entry?.mesh.userData.renderSubmission.ranges.find(r=>faceIndex*3>=r.firstVertex&&faceIndex*3<r.firstVertex+r.vertexCount);return r?{...r}:null;},
  dispose(){if(disposed)return;restore();clear();frameMaterialKeys.clear();materialIntern.clear();group.removeFromParent();disposed=true;}
 };
}
