import {firstTempleOuterCourt,earlyCourtPorticoes} from '../preview/jerusalem-3000/temple-context-layout.js';
import {HERODIAN_DIMENSIONS as D} from '../preview/jerusalem-3000/herodian-dimensions.js';
import assert from 'node:assert/strict';import fs from 'node:fs/promises';import * as THREE from 'three';
import {firstTempleCourt,courtEnvelopeDatum} from '../preview/jerusalem-3000/temple-court-envelopes.js';
import {compileRoyalSpatialLayout} from '../preview/jerusalem-3000/royal-spatial-layout.js';
import {sanctuaryAccessVertices} from '../preview/jerusalem-3000/sanctuary-access-geometry.js';
import {HeritageBuilder} from '../preview/jerusalem-3000/heritage-builder.js';import {addEvidenceArchitecture} from '../preview/jerusalem-3000/jerusalem-architecture.js';
import {PERIMETER_PORTICO_SEGMENTS} from '../preview/jerusalem-3000/temple-perimeter-porticoes.js';
const root=new URL('../preview/jerusalem-3000/',import.meta.url),read=async f=>JSON.parse(await fs.readFile(new URL(f,root))),royal=await read('data/settlement/david-solomon.v1.json'),court=firstTempleCourt(royal,compileRoyalSpatialLayout(royal));
assert.equal(court.gateX,-76);assert.ok(court.gateWidth>=royal.royalCity.spatial.roadWidth+1.4);
const outer=firstTempleOuterCourt(royal,compileRoyalSpatialLayout(royal));assert.ok(outer.length>60);
for(const seg of outer){assert.ok(seg.end-seg.start<=5.00001);for(const edge of compileRoyalSpatialLayout(royal).edges)for(let i=1;i<edge.points.length;i++){
 const a=edge.points[i-1],b=edge.points[i],ac=seg.axis==='x'?a[1]:a[0],bc=seg.axis==='x'?b[1]:b[0];if(ac===bc)continue;
 const f=(seg.fixed-ac)/(bc-ac);if(f<0||f>1)continue;const u=(seg.axis==='x'?a[0]:a[1])+f*((seg.axis==='x'?b[0]:b[1])-(seg.axis==='x'?a[0]:a[1]));
 assert.ok(u<=seg.start-2.49999||u>=seg.end+2.49999,'every registered crossing must retain5m clear outer gate');
}}
assert.equal(earlyCourtPorticoes([-158,-517,-40,-413]).length,3);
const peakGeometry=new THREE.BufferGeometry(),v=[];for(let z=0;z<=2;z++)for(let x=0;x<=2;x++)v.push(x,x===1&&z===1?9:0,z);peakGeometry.setAttribute('position',new THREE.Float32BufferAttribute(v,3));
const peak={grid:{width:3,height:3},mesh:{geometry:peakGeometry,position:{x:0,z:0}},heightAtWorld:(x,z)=>x===1&&z===1?9:0};assert.equal(courtEnvelopeDatum([0,0,2,2],{x:0,z:0},peak),9,'datum must include original interior DEM peaks, not only four corners');peakGeometry.dispose();
const vertices=sanctuaryAccessVertices([[0,0],[6,0]],2,()=>40,(x)=>40.1+x/6*3.9);
assert.ok(vertices.every(Number.isFinite));assert.ok(vertices.filter((_,i)=>i%3===1).every(y=>y>=40&&y<=44));assert.ok(vertices.some((v,i)=>i%3===1&&v===40),'raised ramp must have real ground-contact support vertices');assert.ok(vertices.some((v,i)=>i%3===1&&v===44),'ramp must reach its target floor');
const objects=(await read('data/objects/herodian-30ce.json')).objects,obj=objects.find(o=>o.kind==='perimeter-porticoes');assert.equal(obj.evidence,'inferred');assert.equal(obj.confidence,'inferred');
const mat=new THREE.MeshStandardMaterial(),builder=new HeritageBuilder({inferred:mat}),group=new THREE.Group();builder.currentObject=obj;addEvidenceArchitecture(builder,obj,{grid:{origin:{lat:31.778,lon:35.235}},sampleElevation:()=>200,heightAtWorld:()=>200});builder.finish(group);assert.equal(builder.meshes.length,1,'all colonnade segments must batch under their own evidence object');
const mesh=builder.meshes[0],p=mesh.geometry.attributes.position,bounds=new THREE.Box3().setFromObject(group);assert.ok(bounds.min.x>=-150&&bounds.max.x<=150&&bounds.min.z>=-240&&bounds.max.z<=240);
assert.ok(Math.abs(bounds.max.y-(200+.8+.12+25*.525+.8))<.001);
for(let i=0;i<p.count;i++){const x=p.getX(i),z=p.getZ(i);assert.ok(!(x>-138.71&&x<-12.71&&z>-275.64&&z<-169.64),'porticoes must not intersect the existing Antonia envelope');}
const east=PERIMETER_PORTICO_SEGMENTS.find(s=>s.id==='east'),north=PERIMETER_PORTICO_SEGMENTS.find(s=>s.id==='north');assert.equal(north.end,east.fixed-east.width/2,'roof segments must meet without coplanar overlapping corners');
const events=(await read('data/lifecycle/herodian-30ce.lifecycle.json')).objects.find(o=>o.id===obj.id).lifecycleEvents;assert.deepEqual(events.map(e=>e.state),['build','ruin','unresolved']);builder.dispose();
const stoa=objects.find(o=>o.kind==='portico-basilica'),basilicaBuilder=new HeritageBuilder({reconstructed:mat,inferred:mat}),basilicaGroup=new THREE.Group();basilicaBuilder.currentObject=stoa;addEvidenceArchitecture(basilicaBuilder,stoa,{grid:{origin:{lat:31.778,lon:35.235}},sampleElevation:()=>200,heightAtWorld:()=>200});basilicaBuilder.finish(basilicaGroup);basilicaGroup.updateMatrixWorld(true);const bb=new THREE.Box3().setFromObject(basilicaGroup),centre=bb.getCenter(new THREE.Vector3()),w=D.stoa.eastWest,d=D.stoa.depth,yy=200+.8+(D.stoa.sideHeight+D.stoa.centreHeight)/2;
for(const side of[-1,1]){
 const ray=(xx)=>new THREE.Raycaster(new THREE.Vector3(xx,yy,centre.z+side*(d*.2+2)),new THREE.Vector3(0,0,-side),0,3).intersectObjects(basilicaGroup.children,true);
 assert.equal(ray(centre.x-w/2+4+(w-8)/22).length,0,'clerestory bay must be genuinely open');assert.ok(ray(centre.x-w/2+4).length>0,'clerestory pier must support upper roof edge');
}
basilicaBuilder.dispose();
const fort=objects.find(o=>o.kind==='fortress'),fortBuilder=new HeritageBuilder({reconstructed:mat,inferred:mat,observed:mat,disputed:mat}),fortGroup=new THREE.Group();fortBuilder.currentObject=fort;addEvidenceArchitecture(fortBuilder,fort,{grid:{origin:{lat:31.778,lon:35.235}},sampleElevation:()=>200,heightAtWorld:()=>200});fortBuilder.finish(fortGroup);fortGroup.updateMatrixWorld(true);const fortBounds=new THREE.Box3().setFromObject(fortGroup),fc=fortBounds.getCenter(new THREE.Vector3());
const courtyard=new THREE.Raycaster(new THREE.Vector3(fc.x,300,fc.z),new THREE.Vector3(0,-1,0)).intersectObjects(fortGroup.children,true)[0];assert.ok(Math.abs(courtyard.point.y-202.12)<.001,'Antonia courtyard must really be open to the sky');
assert.equal(new THREE.Raycaster(new THREE.Vector3(fc.x,204,fc.z+43),new THREE.Vector3(0,0,-1),0,12).intersectObjects(fortGroup.children,true).length,0,'authored south portal must open into the court');
assert.ok(Math.abs(fortBounds.max.y-(200+2+70*.525))<.001,'SE tower must retain the selected70cubit height above inherited base');fortBuilder.dispose();mat.dispose();
console.log('PASS: existing-route-aligned court entrance, full-envelope DEM datum, physically supported approach, separately inferred/batched colonnades, no Antonia collision or roof overlap, and declared ruin/unknown fate');
