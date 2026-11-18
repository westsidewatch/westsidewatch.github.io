import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {loadTemporalCityCore} from '../preview/jerusalem-3000/temporal-city-core-adapter.js';
import {registerHerodianUrbanCore} from '../preview/jerusalem-3000/herodian-urban-core-adapter.js';
import {declareHerodianSourceScopes,declaredEventScope,inspectSourceLifecycleContext} from '../preview/jerusalem-3000/source-lifecycle-scope.js';
import {invalidateCityData} from '../preview/jerusalem-3000/city-data-loader.js';
const root=new URL('../preview/jerusalem-3000/',import.meta.url),json=async path=>JSON.parse(await readFile(new URL(path,root))),phases=(await json('data/continuous-build-timeline.json')).phases,original=globalThis.fetch;
try{
 globalThis.fetch=async url=>({ok:true,json:()=>json(url)});invalidateCityData();const {core}=await loadTemporalCityCore(phases,{terrain:{}});await registerHerodianUrbanCore(core);
 const source=core.get('j3k:object:inner-temple'),unknown=core.get('j3k:object:eastern-entry-unknown');
 core.register({...unknown,geometry:{status:'declared'}});const map=core.objects,phaseIndex=[...core.byPhase].map(([id,set])=>[id,[...set]]);
 assert.throws(()=>declareHerodianSourceScopes(core),/remain withheld/);assert.strictEqual(core.objects,map);assert.deepEqual([...core.byPhase].map(([id,set])=>[id,[...set]]),phaseIndex);assert.ok([...core.objects.values()].every(r=>!r.metadata.lifecycleDeclaration),'late failure publishes no partial scope');core.register(unknown);
 const result=declareHerodianSourceScopes(core);assert.deepEqual(result,{objects:7,sourceContextOnly:5,withheld:2,physicalEventsInvented:0});assert.strictEqual(core.get(source.id),source);
 const scoped=[...core.objects.values()].filter(r=>declaredEventScope(r));assert.equal(scoped.length,7);
 for(const record of scoped){assert.equal(record.lifecycle.events.length,0);assert.equal(record.lifecycle.built,null);assert.equal(record.lifecycle.destroyed,null);assert.deepEqual(core.lineage(record.id),{predecessors:[],successors:[]});}
 const context=inspectSourceLifecycleContext(core,'j3k:district:temple-mount',8.9);assert.equal(context.anchors.length,3);assert.ok(context.anchors.every(a=>a.state==='build'));assert.equal(context.ownPhysicalEventsDeclared,false);
 assert.ok(inspectSourceLifecycleContext(core,'j3k:district:temple-mount',9.9).anchors.every(a=>a.state==='ruin'));assert.ok(inspectSourceLifecycleContext(core,'j3k:district:temple-mount',10.9).anchors.every(a=>a.state==='unresolved'));
 core.register({...source,lifecycle:{events:[{phase:'herodian-jesus',state:'unresolved'}]}});assert.equal(inspectSourceLifecycleContext(core,'j3k:district:temple-mount',8.9).anchors.find(a=>a.id===source.id).state,'unresolved','context must read current anchor events without copying them');core.register(source);
 const withheld=inspectSourceLifecycleContext(core,'j3k:gate:eastern-access-unresolved',8.9);assert.equal(withheld.status,'withheld');assert.equal(withheld.anchors[0].state,'unresolved');assert.equal(core.get(unknown.id).geometry.status,'withheld');
 assert.equal(inspectSourceLifecycleContext(core,'j3k:object:inner-temple',8.9),null);context.anchors[0].state='wrong';assert.ok(inspectSourceLifecycleContext(core,'j3k:district:temple-mount',8.9).anchors.every(a=>a.state==='build'));
 declareHerodianSourceScopes(core);assert.equal([...core.objects.values()].filter(r=>declaredEventScope(r)).length,7);assert.ok(core.validate().ok);
 console.log('PASS: seven explicit non-event scopes, late validation rollback, no invented build dates/lineage, live source context, withheld geometry, defensive inspection and idempotent declaration');
}finally{globalThis.fetch=original;invalidateCityData();}
