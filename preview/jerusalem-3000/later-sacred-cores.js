import * as THREE from 'three';
import {geographicToENU} from './terrain-runtime.js';
import {coreLocationReference} from './core-location-reference.js';
// Author-selected context coordinates in the canonical metre frame. These are NOT
// surveyed footprints, heights, ancient platforms, or verified cross-era reuse.
const CHURCH_SOURCE='https://www.custodia.org/en/sanctuaries/basilica-of-the-holy-sepulchre/';
const ROCK_SOURCE='https://islamicart.museumwnf.org/database_item.php?id=monument%3Bisl%3Bpa%3Bmon01%3B4%3Ben';
const CHRISTIAN_PHASES=new Set(['byzantine','early-islamic','crusader','ayyubid-mamluk','ottoman','outside-walls','modern']);
const ISLAMIC_PHASES=new Set(['early-islamic','crusader','ayyubid-mamluk','ottoman','outside-walls','modern']);
const rectangle=(x,z,w,d)=>[{x:x-w/2,z:z-d/2},{x:x+w/2,z:z-d/2},{x:x+w/2,z:z+d/2},{x:x-w/2,z:z+d/2}];
export function laterSacredCores(phase){
 const cores=[];
 if(CHRISTIAN_PHASES.has(phase)){
  const constantinian=['byzantine','early-islamic'].includes(phase);
  cores.push({id:`j3k:${phase}:independent:monument:holy-sepulchre-context`,type:'monument',confidence:'inferred',
   geometry:{frame:'canonical-dem-enu',status:'authored-context-not-surveyed',primitive:'polygon',polygon:rectangle(-495,15,constantinian?145:115,95)},
   source:{urls:[CHURCH_SOURCE],authority:'historical form context; coordinates and dimensions authored for schematic display'},
   metadata:{placeId:'j3k:place:holy-sepulchre-site',placeRelation:'same-site-not-verified-original-fabric',name:'聖墓教堂群（概略量體）',coreProfile:constantinian?'constantinian-rotunda-east-basilica':'medieval-rotunda-church',
    referencePeriod:constantinian?'post-335, before 1009 destruction':'post-Crusader rebuilding; later changes not resolved',
    wholePhaseSimultaneity:false,geometryVerified:false,ancientGroundVerified:false}});
 }
 if(ISLAMIC_PHASES.has(phase))cores.push({id:`j3k:${phase}:independent:monument:rock-sanctuary-context`,type:'monument',confidence:'inferred',
  geometry:{frame:'canonical-dem-enu',status:'authored-context-not-surveyed',primitive:'polygon',polygon:rectangle(0,-180,80,80)},
  source:{urls:[ROCK_SOURCE],authority:'octagonal shrine and dome form context; coordinates and dimensions authored for schematic display'},
  metadata:{placeId:'j3k:place:northern-sacred-hill',placeRelation:'same-hill-not-same-ancient-building',name:phase==='crusader'?'岩石圓頂建築／Templum Domini（概略量體）':'岩石圓頂建築（概略量體）',coreProfile:'octagonal-rock-shrine',referencePeriod:'post-691/692; phase-specific alterations not resolved',wholePhaseSimultaneity:false,geometryVerified:false,ancientGroundVerified:false}});
 if(coreLocationReference.phases.includes(phase))for(const core of cores){
  const key=core.id.split(':').at(-1),reference=coreLocationReference.cores[key],q=geographicToENU(reference.point.lat,reference.point.lon,{lat:31.778,lon:35.235});
  const polygon=core.geometry.polygon,cx=polygon.reduce((s,p)=>s+p.x,0)/polygon.length,cz=polygon.reduce((s,p)=>s+p.z,0)/polygon.length;
  core.geometry.polygon=polygon.map(p=>({x:p.x-cx+q.east,z:p.z-cz-q.north}));
  core.geometry.status='modern-map-position-with-illustrative-massing';
  core.source.urls.push(coreLocationReference.source.url);core.source.positionReference={...reference,...coreLocationReference.source,authority:coreLocationReference.positionAuthority};
  core.metadata.modernPositionReference=true;
 }
 return cores;
}
// One aggregate mesh per registered core, not independently registered fragments.
export function sacredCoreGeometry(record,terrain){
 const vertices=[],polygon=record.geometry.polygon,cx=polygon.reduce((s,p)=>s+p.x,0)/polygon.length,cz=polygon.reduce((s,p)=>s+p.z,0)/polygon.length;
 const append=(g,x,z,y=0)=>{g.translate(x,y,z);const p=g.attributes.position,indices=g.index?.array||Array.from({length:p.count},(_,i)=>i);for(const i of indices){const px=p.getX(i),pz=p.getZ(i),ground=terrain.heightAtWorld(px,pz);if(!Number.isFinite(ground)){g.dispose();throw new Error('Sacred core outside canonical DEM');}vertices.push(px,ground+.2+p.getY(i),pz);}g.dispose();};
 const box=(x,z,w,d,h)=>append(new THREE.BoxGeometry(w,h,d),x,z,h/2);
 const dome=(x,z,r,base)=>append(new THREE.SphereGeometry(r,16,8,0,Math.PI*2,0,Math.PI/2),x,z,base);
 if(record.metadata.coreProfile==='octagonal-rock-shrine'){
  append(new THREE.CylinderGeometry(25,25,10,8),cx,cz,5);append(new THREE.CylinderGeometry(11,11,7,16),cx,cz,13.5);dome(cx,cz,11,17);
 }else{
  const old=record.metadata.coreProfile==='constantinian-rotunda-east-basilica',rx=cx-(old?45:25);
  append(new THREE.CylinderGeometry(20,20,15,16),rx,cz,7.5);dome(rx,cz,17,15);
  box(cx+(old?28:15),cz,old?70:50,old?45:50,16);
  if(!old)box(cx+20,cz+32,12,12,25);
 }
 const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(vertices,3));g.computeVertexNormals();g.userData={schematicSacredCore:true,geometryVerified:false};return g;
}
