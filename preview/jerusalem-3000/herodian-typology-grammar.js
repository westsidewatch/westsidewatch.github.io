import * as THREE from 'three';
import { buildFacadeOpenings } from './urban-facade-grammar.js';
function centroid(poly){return{x:poly.reduce((s,p)=>s+p.x,0)/poly.length,z:poly.reduce((s,p)=>s+p.z,0)/poly.length}}
function shrink(poly,f){const c=centroid(poly);return poly.map(p=>({x:c.x+(p.x-c.x)*f,z:c.z+(p.z-c.z)*f}))}
function terrainY(terrain,x,z){const y=terrain?.heightAtWorld?.(x,z);return Number.isFinite(y)?y:0}
function shapeGeometry(poly,h){const s=new THREE.Shape();poly.forEach((p,i)=>i?s.lineTo(p.x,p.z):s.moveTo(p.x,p.z));s.closePath();const g=new THREE.ExtrudeGeometry(s,{depth:h,steps:1,bevelEnabled:false});g.rotateX(-Math.PI/2);g.computeVertexNormals();return g}
function add(group,meshes,mat,poly,h,terrain,parcel,kind,start,yOffset=0){const c=centroid(poly),local=poly.map(p=>({x:p.x-c.x,z:p.z-c.z})),ground=terrainY(terrain,c.x,c.z)+1.2+yOffset,mesh=new THREE.Mesh(shapeGeometry(local,h),mat);mesh.position.set(c.x,ground,c.z);mesh.castShadow=true;mesh.receiveShadow=true;mesh.userData.phase2={stage:`architecture-${kind}`,start,baseHeight:h,groundY:ground};mesh.userData.cityObject={parcelId:parcel.id,terrainGround:terrainY(terrain,c.x,c.z)+1.2,kind,confidence:'inferred',semantic:true};group.add(mesh);meshes.push(mesh);return mesh}
function edges(poly){return poly.map((a,i)=>{const b=poly[(i+1)%poly.length];return{a,b,length:Math.hypot(b.x-a.x,b.z-a.z)}})}
function insetBand(poly,outerFactor,innerFactor){const outer=shrink(poly,outerFactor),inner=shrink(poly,innerFactor),bands=[];for(let i=0;i<outer.length;i++)bands.push([outer[i],outer[(i+1)%outer.length],inner[(i+1)%inner.length],inner[i]]);return bands}
function facade(group,meshes,materials,terrain,parcel,edge,h,index,start,yOffset=0){if(!edge||edge.length<2.2)return 0;const dx=edge.b.x-edge.a.x,dz=edge.b.z-edge.a.z,L=edge.length||1,tx=dx/L,tz=dz/L,nx=-tz,nz=tx,c={x:(edge.a.x+edge.b.x)/2,z:(edge.a.z+edge.b.z)/2},ground=terrainY(terrain,c.x,c.z)+1.2+yOffset,openings=buildFacadeOpenings({buildingId:`${parcel.id}:${index}`,phaseId:parcel.phaseIds?.[0]||'default',face:`edge-${index}`,width:L,height:h,floors:h>15?2:1,streetFacing:true}),mat=materials.facadeOpening||new THREE.MeshStandardMaterial({color:0x3d3327,roughness:.94,metalness:0}),depth=.18;let count=0;for(const o of openings){const g=new THREE.BoxGeometry(o.width,o.height,depth),m=new THREE.Mesh(g,mat);m.position.set(c.x+tx*o.x+nx*(depth*.55),ground+o.y,c.z+tz*o.x+nz*(depth*.55));m.rotation.y=-Math.atan2(dz,dx);m.castShadow=false;m.receiveShadow=true;m.userData.phase2={stage:`architecture-facade-${o.kind}`,start:start+.006,baseHeight:o.height,groundY:ground};m.userData.cityObject={parcelId:parcel.id,terrainGround:terrainY(terrain,c.x,c.z)+1.2,kind:`facade-${o.kind}`,confidence:'inferred',semantic:true};group.add(m);meshes.push(m);count++}return count}
function roof(group,meshes,mat,terrain,parcel,poly,wallHeight,index,start){const roofPoly=shrink(poly,.94),step=.65+(index%3)*.38;add(group,meshes,mat,roofPoly,step,terrain,parcel,'roof-slab',start,wallHeight);const es=edges(roofPoly),parapetH=1.15+(index%2)*.35;for(let i=0;i<es.length;i++){const e=es[i],dx=e.b.x-e.a.x,dz=e.b.z-e.a.z,L=Math.hypot(dx,dz)||1,nx=-dz/L,nz=dx/L,t=.72,band=[{x:e.a.x+nx*t,z:e.a.z+nz*t},{x:e.b.x+nx*t,z:e.b.z+nz*t},{x:e.b.x-nx*t,z:e.b.z-nz*t},{x:e.a.x-nx*t,z:e.a.z-nz*t}];add(group,meshes,mat,band,parapetH,terrain,parcel,'roof-parapet',start+.008,wallHeight+step)}if(index%4===0){const upper=shrink(roofPoly,.34);add(group,meshes,mat,upper,3.2+(index%3),terrain,parcel,'roof-room',start+.016,wallHeight+step)}return 2+es.length}
function chooseTypology(parcel,index){const pool=parcel.typologyPool||parcel.metadata?.typologyPool||['courtyard-house'];return pool[index%pool.length]}
function heightScale(parcel){return parcel.metadata?.interiorFabric?.82:1}
function courtyardHouse(group,meshes,materials,terrain,parcel,index){const mat=materials.inferred||materials.reconstructed,fp=parcel.geometry.polygon,bands=insetBand(fp,.92,.48),base=(14+(index%5)*2.1)*heightScale(parcel);let components=0;bands.forEach((band,i)=>{const h=base*(.74+(i%3)*.11);add(group,meshes,mat,band,h,terrain,parcel,i===0?'courtyard-entry':'courtyard-range',.26+i*.018);components++;if(i===0)components+=facade(group,meshes,materials,terrain,parcel,edges(band).sort((a,b)=>b.length-a.length)[0],h,index,.26+i*.018);components+=roof(group,meshes,mat,terrain,parcel,band,h,index+i,.35+i*.012)});const c=centroid(fp),court=shrink(fp,.42),courtY=Math.min(...court.map(p=>terrainY(terrain,p.x,p.z))),paving=new THREE.Mesh(shapeGeometry(court.map(p=>({x:p.x-c.x,z:p.z-c.z})),.8),mat);paving.position.set(c.x,courtY+.35,c.z);paving.userData.phase2={stage:'architecture-courtyard-paving',start:.24,baseHeight:.8,groundY:courtY};paving.userData.cityObject={parcelId:parcel.id,kind:'courtyard',confidence:'inferred',semantic:true};group.add(paving);meshes.push(paving);return{typology:'courtyard-house',components:components+1}}
function streetHouse(group,meshes,materials,terrain,parcel,index){const mat=materials.inferred||materials.reconstructed,fp=shrink(parcel.geometry.polygon,.9),es=edges(fp).sort((a,b)=>b.length-a.length),front=es[0],c=centroid(fp),depth=.58,backA={x:front.a.x+(c.x-front.a.x)*depth,z:front.a.z+(c.z-front.a.z)*depth},backB={x:front.b.x+(c.x-front.b.x)*depth,z:front.b.z+(c.z-front.b.z)*depth},main=[front.a,front.b,backB,backA],rear=shrink(fp,.56),h=(13+(index%4)*2.5)*heightScale(parcel);add(group,meshes,mat,main,h,terrain,parcel,'street-frontage',.28);let components=1+facade(group,meshes,materials,terrain,parcel,front,h,index,.28);const upperH=h*.55;add(group,meshes,mat,rear,upperH,terrain,parcel,'upper-room',.34,h*.45);components++;components+=roof(group,meshes,mat,terrain,parcel,main,h,index,.37);components+=roof(group,meshes,mat,terrain,parcel,rear,upperH,index+1,.40,h*.45);return{typology:'street-house',components}}
function workshopHouse(group,meshes,materials,terrain,parcel,index){const mat=materials.inferred||materials.reconstructed,fp=shrink(parcel.geometry.polygon,.9),es=edges(fp).sort((a,b)=>b.length-a.length),front=es[0],c=centroid(fp),midA={x:front.a.x+(c.x-front.a.x)*.48,z:front.a.z+(c.z-front.a.z)*.48},midB={x:front.b.x+(c.x-front.b.x)*.48,z:front.b.z+(c.z-front.b.z)*.48},shop=[front.a,front.b,midB,midA],rear=shrink(fp,.62),h=(12+(index%4)*2.2)*heightScale(parcel),shopH=h*.58;add(group,meshes,mat,shop,shopH,terrain,parcel,'workshop-frontage',.27);let components=1+facade(group,meshes,materials,terrain,parcel,front,shopH,index,.27);add(group,meshes,mat,rear,h,terrain,parcel,'workshop-house',.32);components++;components+=roof(group,meshes,mat,terrain,parcel,shop,shopH,index,.36);components+=roof(group,meshes,mat,terrain,parcel,rear,h,index+2,.39);return{typology:'workshop-house',components}}
export function buildEraParcelArchitecture(group,core,materials,terrain,{phaseId='herodian-jesus',grammarId='shared-parcel-typology-v1',destroyedPhase=null,parcelBatch=null,indexOffset=0}={}){const parcels=parcelBatch??core.phase(phaseId).filter(o=>o.type==='parcel'&&o.geometry?.primitive==='polygon'),meshes=[],buildings=[];for(let localIndex=0;localIndex<parcels.length;localIndex++){const i=localIndex+indexOffset,parcel=parcels[localIndex],typology=chooseTypology(parcel,i);let result;if(typology==='street-house')result=streetHouse(group,meshes,materials,terrain,parcel,i);else if(typology==='workshop-house')result=workshopHouse(group,meshes,materials,terrain,parcel,i);else result=courtyardHouse(group,meshes,materials,terrain,parcel,i);const id=`${parcel.id}:building`;core.register({id,type:'building',phaseIds:destroyedPhase?[phaseId,destroyedPhase]:[phaseId],geometry:{primitive:'architectural-components',parcelId:parcel.id},typology:result.typology,source:{parcelId:parcel.id,grammar:grammarId},confidence:'inferred',lifecycle:{built:phaseId,...(destroyedPhase?{destroyed:destroyedPhase}:{})},metadata:{componentCount:result.components,finishedArchitectureFirst:true,parcelGeometryPreserved:true,terrainStepped:true,interiorFabric:!!parcel.metadata?.interiorFabric,roofGrammar:'stepped-flat-roof-parapet-v1',facadeGrammar:'temporal-facade-openings-v1'}});buildings.push(id)}return{version:grammarId,phaseId,parcels:parcels.length,buildings:buildings.length,meshes,buildingIds:buildings,semanticBoxes:0}}

export function buildHerodianParcelArchitecture(group,core,materials,terrain){return buildEraParcelArchitecture(group,core,materials,terrain,{phaseId:'herodian-jesus',grammarId:'herodian-typology-v5',destroyedPhase:'roman-destruction'});}

// Same typology and IDs as the synchronous builder, with an event-loop yield
// between bounded batches. No WebGL objects are built by the startup audit.
export async function buildEraParcelArchitectureAsync(group, core, materials, terrain, {
  phaseId, destroyedPhase = null, grammarId = 'bounded-shared-parcel-typology-v1',
  signal, budgetMs = 8, maxBatch = 4,
  yieldControl = () => new Promise(resolve => setTimeout(resolve, 0)),
  onProgress = () => {},
} = {}) {
  if (!(budgetMs > 0) || !Number.isInteger(maxBatch) || maxBatch < 1)
    throw new Error('Positive generation budget and batch size required');
  const parcels = core.phase(phaseId).filter(o => o.type === 'parcel' && o.geometry?.primitive === 'polygon');
  const meshes = [], buildingIds = [];
  const started = performance.now();
  let batchStart = performance.now(), batchCount = 0, yields = 0, maxBatchMs = 0;
  await yieldControl();
  for (let i = 0; i < parcels.length; i++) {
    if (signal?.aborted) throw new DOMException('Era generation cancelled', 'AbortError');
    const result = buildEraParcelArchitecture(group, core, materials, terrain, {
      phaseId, destroyedPhase, grammarId, parcelBatch: [parcels[i]], indexOffset: i,
    });
    meshes.push(...result.meshes); buildingIds.push(...result.buildingIds);
    onProgress({ completed: i + 1, total: parcels.length });
    if (++batchCount >= maxBatch || performance.now() - batchStart >= budgetMs) {
      maxBatchMs = Math.max(maxBatchMs, performance.now() - batchStart);
      yields++;
      await yieldControl();
      batchStart = performance.now(); batchCount = 0;
    }
  }
  if (signal?.aborted) throw new DOMException('Era generation cancelled', 'AbortError');
  return { version: grammarId, phaseId, parcels: parcels.length,
    buildings: buildingIds.length, meshes, buildingIds, semanticBoxes: 0, yields, maxBatchMs, elapsedMs: performance.now() - started };
}
