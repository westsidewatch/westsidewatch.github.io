import assert from 'node:assert/strict';
import fs from 'node:fs';
import * as THREE from 'three';
import {createPersistentCityWorld} from '../preview/jerusalem-3000/persistent-city-world.js';
import {compileIndependentLaterSkeleton,buildIndependentLaterSkeleton} from '../preview/jerusalem-3000/independent-later-skeleton.js';
import {createLaterMorphologyLedger} from '../preview/jerusalem-3000/later-morphology-ledger.js';
import {TemporalCityCore} from '../preview/jerusalem-3000/temporal-city-core.js';
const root=new URL('../preview/jerusalem-3000/',import.meta.url),read=p=>JSON.parse(fs.readFileSync(new URL(p,root)));
const phases=read('data/continuous-build-timeline.json').phases,registrations=new Map();
const terrain={heightAtWorld:(x,z)=>100+x*.02-z*.03},material=new THREE.MeshStandardMaterial(),parent=new THREE.Group();
for(const name of ['roman-byzantine-islamic','medieval-ottoman','expansion-modern']){const data=read(`data/urban/${name}.skeleton.v1.json`);for(const phase of Object.keys(data.phases))registrations.set(phase,compileIndependentLaterSkeleton(data,phase,data.origin));}
const core=new TemporalCityCore({phases,terrain}),publisher=createLaterMorphologyLedger(core),world=createPersistentCityWorld({parent,phases:[...registrations.keys()],build:(group,phase)=>buildIndependentLaterSkeleton(group,registrations.get(phase),{inferred:material},terrain),publish:r=>publisher.bind(r)}),snapshots=new Map(),entries=new Map();
for(const phase of registrations.keys()){
 const entry=world.activate(phase);entries.set(phase,entry);entry.binding.apply(()=>true);snapshots.set(phase,world.inspectPhase(phase));
 assert.equal(parent.children.filter(g=>g.visible).length,1);assert.equal(entry.group.visible,true);
}
for(const phase of [...registrations.keys()].reverse()){
 const entry=world.activate(phase);assert.deepEqual(world.inspectPhase(phase),snapshots.get(phase),'return must keep exact mesh AND geometry instances');
 entry.binding.apply(()=>false);assert.ok(entry.runtime.meshes.every(m=>!m.visible));entry.binding.apply(()=>true);assert.ok(entry.runtime.meshes.every(m=>m.visible));
}
const blockPolygons=phase=>entries.get(phase).runtime.ledgerRecords.filter(r=>r.type==='block'&&r.source.districtId.includes(':district:')&&!r.source.districtId.includes('outside')&&!r.source.districtId.includes('modern')).map(r=>JSON.stringify(r.geometry.polygon));
// Explicitly authored old-city background must not be re-randomised by new IDs.
const ottoman=new Set(blockPolygons('ottoman'));
for(const phase of ['outside-walls','modern']){
 const oldIds=new Set(registrations.get(phase).districts.filter(d=>d.metadata.layoutRole==='old-city-context').map(d=>d.id));
 const blocks=entries.get(phase).runtime.ledgerRecords.filter(r=>r.type==='block'&&oldIds.has(r.source.districtId));
 assert.equal(blocks.length,ottoman.size);assert.ok(blocks.every(b=>ottoman.has(JSON.stringify(b.geometry.polygon))),'same authored old city must have same block geometry across expansion pair');
}
const before=world.diagnostics();assert.equal(before.builds,8);assert.equal(before.cachedPhases.length,8);assert.ok(before.cacheHits>=8);assert.ok(before.uniqueGeometries<before.meshInstances);assert.ok(before.geometryBufferBytes>0);assert.equal(before.sameGeometryIsHistoricalReuse,false);
const active=before.activePhase;assert.throws(()=>world.activate('not-a-phase'));assert.equal(world.diagnostics().activePhase,active);
world.activate(null);assert.equal(parent.children.filter(g=>g.visible).length,0);assert.equal(core.validate().ok,true);
let released=0;const geometries=new Set([...entries.values()].flatMap(e=>e.runtime.meshes.map(m=>m.geometry)));for(const g of geometries)g.addEventListener('dispose',()=>released++);
world.dispose();world.dispose();assert.equal(released,geometries.size,'each pooled buffer disposed exactly once');assert.equal(parent.children.length,0);assert.throws(()=>world.activate('modern'));publisher.dispose();assert.equal(core.objects.size,0);material.dispose();
// Failed target publication leaves prior scene visible and cleans the candidate.
const host=new THREE.Group(),created=[];let disposed=0;
const fail=createPersistentCityWorld({parent:host,phases:['good','bad'],build(group,phase){const mesh=new THREE.Mesh(new THREE.BoxGeometry(),new THREE.MeshBasicMaterial());mesh.geometry.addEventListener('dispose',()=>disposed++);group.add(mesh);created.push(mesh);return{phaseId:phase,meshes:[mesh],disposeMaterials(){mesh.material.dispose();}};},publish(r){if(r.phaseId==='bad')throw new Error('rejected');return{};}});
const good=fail.activate('good');assert.throws(()=>fail.activate('bad'),/rejected/);assert.equal(good.group.visible,true);assert.equal(host.children.length,1);assert.equal(disposed,1);fail.dispose();assert.equal(disposed,2);
console.log(JSON.stringify({ok:true,...before,geometryBuffersMiB:Number((before.geometryBufferBytes/1048576).toFixed(2)),historicalContinuityAccepted:false}));
