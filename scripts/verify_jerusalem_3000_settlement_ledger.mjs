import assert from 'node:assert/strict';
import * as THREE from 'three';
import {readFileSync} from 'node:fs';
import {TemporalCityCore} from '../preview/jerusalem-3000/temporal-city-core.js';
import {createLandscapeSettlement} from '../preview/jerusalem-3000/earliest-settlement.js';
import {lifecycleStateAt} from '../preview/jerusalem-3000/construction-engine.js';
const json=p=>JSON.parse(readFileSync(new URL('../preview/jerusalem-3000/'+p,import.meta.url)));
const timeline=json('data/continuous-build-timeline.json'),terrain={grid:{origin:{lat:31.773235,lon:35.2368303}},heightAtWorld:(x,z)=>50+x*.02+z*.01};
const core=new TemporalCityCore({phases:timeline.phases,terrain}),parent=new THREE.Group();
core.register({id:'foreign',type:'water',confidence:'inferred',phaseIds:[timeline.phases[0].id]});
const runtimes=[];
for(const [index,name]of ['earliest','middle-bronze','late-bronze-iron1','david-solomon'].entries()){
 const data=json(`data/settlement/${name}.v1.json`),runtime=createLandscapeSettlement(parent,{data,terrain,ledgerCore:core});runtimes.push(runtime);
 runtime.apply({phaseId:data.phase,evidenceAllowed:()=>true});
 const report=runtime.diagnostics();assert.equal(report.sharedLedger.buildings,data.houseOffsets.length);assert.equal(report.visibleHouses,data.houseOffsets.length);
 const records=core.phase(data.phase).filter(r=>r.metadata.generationPhase===data.phase);
 assert.ok(records.length>=data.houseOffsets.length);
 for(const record of records){assert.equal(record.confidence,'inferred');assert.equal(record.source.geometryVerified,false);assert.notEqual(record.geometry.primitive,'box');assert.deepEqual(core.lineage(record.id),{predecessors:[],successors:[]});assert.equal(lifecycleStateAt({lifecycleEvents:record.lifecycle.events},timeline,timeline.phases[index+1].id),'unresolved');}
 const id=records.find(r=>r.type==='building').id,record=core.get(id),group=parent.children.at(-1),parts=group.children.filter(m=>m.userData.cityObject.objectId===id);
 assert.ok(parts.length>1);assert.equal(new Set(parts.map(m=>m.userData.cityObject.componentId)).size,parts.length);
 const positions=parts.map(m=>m.position.toArray()),geometries=parts.map(m=>m.geometry.uuid);
 core.register({...record,lifecycle:{events:[{phase:data.phase,state:'unresolved'}]}});runtime.apply({phaseId:data.phase,evidenceAllowed:()=>true});assert.equal(runtime.diagnostics().visibleHouses,data.houseOffsets.length-1);assert.ok(parts.every(m=>!m.visible));
 core.register(record);runtime.apply({phaseId:data.phase,evidenceAllowed:()=>true});assert.ok(parts.every(m=>m.visible));
 assert.deepEqual(parts.map(m=>m.position.toArray()),positions);assert.deepEqual(parts.map(m=>m.geometry.uuid),geometries);
 const road=records.find(r=>r.type==='road');
 if(road){core.register({...road,lifecycle:{events:[{phase:data.phase,state:'unresolved'}]}});runtime.apply({phaseId:data.phase,evidenceAllowed:()=>true});assert.ok(group.children.filter(m=>m.userData.cityObject.objectId===road.id).every(m=>!m.visible));core.register(road);runtime.apply({phaseId:data.phase,evidenceAllowed:()=>true});assert.ok(group.children.filter(m=>m.userData.cityObject.objectId===road.id).every(m=>m.visible));}
 const isolated=new TemporalCityCore({phases:timeline.phases,terrain}),last=records.at(-1);isolated.register(last);const failedParent=new THREE.Group();
 assert.throws(()=>createLandscapeSettlement(failedParent,{data,terrain,ledgerCore:isolated}),/collision/);assert.deepEqual([...isolated.objects.keys()],[last.id],'late collision must roll back earlier staged records');assert.equal(failedParent.children.length,0);
 const keys=[...core.objects.keys()],before=parent.children.length;
 assert.throws(()=>createLandscapeSettlement(parent,{data,terrain,ledgerCore:core}),/collision/);assert.equal(parent.children.length,before);assert.deepEqual([...core.objects.keys()],keys);
 runtime.apply({phaseId:'modern',evidenceAllowed:()=>true});assert.equal(runtime.diagnostics().visibleHouses,0);
 runtime.apply({phaseId:data.phase,evidenceAllowed:()=>false});assert.equal(runtime.diagnostics().visibleHouses,0);
 assert.ok(group.children.filter(m=>!m.userData.cityObject.objectId.includes(':house:')&&m.userData.cityObject.kind!=='inferred-footpath').every(m=>!core.get(m.userData.cityObject.objectId)),'symbols and defense must not be claimed by residential publisher');
}
assert.ok(core.validate().ok);runtimes.forEach(r=>r.dispose());assert.deepEqual([...core.objects.keys()],['foreign']);assert.equal(parent.children.length,0);assert.ok(core.validate().ok);
console.log('PASS: four early-era batches, composite house/road identity, explicit unknown fate, live event visibility, evidence filters, exact geometry return, atomic collision cleanup and foreign ownership');
