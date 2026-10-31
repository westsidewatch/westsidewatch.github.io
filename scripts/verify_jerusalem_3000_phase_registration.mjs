import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import * as THREE from 'three';
import {TemporalCityCore} from '../preview/jerusalem-3000/temporal-city-core.js';
import {loadTemporalCityCore} from '../preview/jerusalem-3000/temporal-city-core-adapter.js';
import {loadTemporalCityIntegration} from '../preview/jerusalem-3000/temporal-city-integration.js';
import {loadAnchorCityLedger} from '../preview/jerusalem-3000/anchor-ledger-loader.js';
import {invalidateCityData} from '../preview/jerusalem-3000/city-data-loader.js';
import {lifecycleStateAt} from '../preview/jerusalem-3000/construction-engine.js';
import {createCityProjection} from '../preview/jerusalem-3000/city-lifecycle-projection.js';
const base=new URL('../preview/jerusalem-3000/',import.meta.url),read=async path=>JSON.parse(await readFile(new URL(path,base))),timeline=await read('data/continuous-build-timeline.json');
const test=new TemporalCityCore({phases:timeline.phases});
const input={id:'stable',type:'monument',phaseIds:['herodian-jesus'],lifecycle:{events:[]}};
test.register(input);test.register({...input,phaseIds:['roman-destruction']});
assert.equal(test.phase('herodian-jesus').length,0);assert.equal(test.byPhase.get('herodian-jesus').has(input.id),false);assert.equal(test.phase('roman-destruction')[0].id,input.id);
const record=test.register({...input,lifecycle:{events:[{phase:'herodian-jesus',state:'build'},{phase:'roman-destruction',state:'ruin'}]}});
assert.ok(record.phaseIds.includes('roman-destruction'),'event phases must be indexed');assert.throws(()=>record.phaseIds.push('modern'));
const before=()=>JSON.stringify({object:test.get(input.id),index:[...test.byPhase].map(([p,ids])=>[p,[...ids]])});
for(const events of [[{phase:'missing',state:'build'}],[{phase:'modern',state:'unsupported'}],[{phase:'modern',state:'build',offset:1}],[{phase:'modern',state:'build'},{phase:'modern',state:'unresolved',offset:0}]]){
 const snapshot=before();assert.throws(()=>test.register({...input,lifecycle:{events}}));assert.equal(before(),snapshot,'failed registration must not partially change an object or its indexes');
}
test.byPhase.set('modern',new Set(['stable']));assert.equal(test.validate().ok,false);assert.equal(test.phase('modern').length,0);test.register(record);assert.equal(test.validate().ok,true);
const previous=globalThis.fetch,calls=new Map();
try{
 invalidateCityData();globalThis.fetch=async url=>{const key=new URL(url).href;calls.set(key,(calls.get(key)||0)+1);return{ok:true,json:()=>read(key)};};
 const [{core,validation},integration,ledger]=await Promise.all([loadTemporalCityCore(timeline.phases),loadTemporalCityIntegration(timeline.phases),loadAnchorCityLedger()]);
 assert.equal(validation.ok,true);
 const pack=ledger.packs.packs.find(p=>p.phase==='herodian-jesus'),source=await read('data/objects/herodian-30ce.json');assert.equal(pack.objects.length,source.objects.length);
 const ids=source.objects.filter(o=>o.id!=='j3k:object:eastern-entry-unknown').map(o=>o.id);
 for(const id of ids){
  const r=core.get(id);assert.deepEqual(r.lifecycle.events,integration.lifecycle.get(id));assert.equal(r.metadata.lifecyclePack,'./lifecycle/herodian-30ce.lifecycle.json');
  assert.ok(core.phase('roman-destruction').some(o=>o.id===id));
  for(const [position,state] of [[8.9,'build'],[9.5,'ruin'],[10.9,'unresolved']])assert.equal(integration.sample(position).find(o=>o.id===id).state,state);
  assert.equal(lifecycleStateAt({lifecycleEvents:r.lifecycle.events},timeline,'aelia'),'unresolved');assert.deepEqual(core.lineage(id),{predecessors:[],successors:[]});
 }
 assert.equal(core.get(ids[0]).type,'monument');assert.equal(core.get('j3k:object:western-street').type,'road');assert.equal(core.get('j3k:object:eastern-entry-unknown').lifecycle.built,null);
 assert.equal(integration.sample(8.9).find(o=>o.id==='j3k:object:eastern-entry-unknown').state,'withheld','missing events and withheld geometry cannot become an invented construction');
 assert.equal(calls.get(new URL('data/lifecycle/herodian-30ce.lifecycle.json',base).href),1);assert.equal(calls.get(new URL('data/objects/herodian-30ce.json',base).href),1);
 const group=new THREE.Group(),geometry=new THREE.BoxGeometry(1,1,1),material=new THREE.MeshBasicMaterial(),meshes=ids.map(id=>{const m=new THREE.Mesh(geometry,material);m.position.y=20;m.userData.cityObject={objectId:id,confidence:'inferred',terrainGround:10};group.add(m);return m;});
 const projection=createCityProjection(group,meshes,{stateForObject:(id,phase)=>lifecycleStateAt({lifecycleEvents:core.get(id).lifecycle.events},timeline,phase)});
 projection.apply({phaseId:'herodian-jesus'});const fingerprint=projection.diagnostics().transformFingerprint;
 projection.apply({phaseId:'roman-destruction',ruin:1});assert.ok(meshes.every(m=>m.visible&&m.position.y<20));
 const old=core.get(ids[0]);core.register({...old,lifecycle:{...old.lifecycle,events:old.lifecycle.events.map(e=>e.phase==='roman-destruction'?{...e,state:'unresolved'}:e)}});
 projection.apply({phaseId:'roman-destruction',ruin:1});assert.equal(meshes[0].visible,false,'shared ledger changes must gate the renderer');assert.ok(meshes.slice(1).every(m=>m.visible));
 core.register(old);projection.apply({phaseId:'aelia'});assert.equal(group.visible,false);projection.apply({phaseId:'herodian-jesus'});assert.equal(projection.diagnostics().transformFingerprint,fingerprint);assert.ok(meshes.every(m=>m.visible));geometry.dispose();material.dispose();
 // Reject conflicting source authorities instead of overwriting events.
 invalidateCityData();globalThis.fetch=async url=>({ok:true,json:async()=>{const data=await read(new URL(url).href);if(String(url).endsWith('/anchor-era.lifecycle.json'))data.objects.push({id:ids[0],lifecycleEvents:[]});return data;}});
 await assert.rejects(loadAnchorCityLedger(),/declared lifecycle/);
}finally{globalThis.fetch=previous;invalidateCityData();}
console.log('PASS: atomic phase replacement, immutable event indexes, one declared source per consumer, six shared ruin/unknown fates, conflict rejection and exact reverse identity');
