import assert from 'node:assert/strict';
import { evidenceFromUniversalA2AResult } from './living-water-runtime-adapter.js';

const artifact={result:{provider:'dore-local',model:'real-local-model',canonical_workspace_mutated:false,production_promoted:false,candidates:[
 {id:'sacred-threshold',raster:{real_browser_render:true,sha256:'aaa'}},
 {id:'quiet-light',raster:{real_browser_render:true,sha256:'bbb'}}
],critic:{votes:[{judge:'blind-1'},{judge:'blind-2'}]}}};
const evidence=evidenceFromUniversalA2AResult(artifact,{visualEvidenceId:'visual-evidence:atlas'});
assert.equal(evidence.filter(x=>x.kind==='real-render').length,2);
assert.equal(evidence.find(x=>x.kind==='beautiful-gate').votes,2);
assert.ok(evidence.every(x=>x.kind!=='real-render'||x.sha256));

assert.throws(()=>evidenceFromUniversalA2AResult({result:{...artifact.result,candidates:[{id:'x',raster:{real_browser_render:true}}]}}),/proven browser raster/);
assert.throws(()=>evidenceFromUniversalA2AResult({result:{...artifact.result,critic:{votes:[{}]}}}),/two blind judge/);
assert.throws(()=>evidenceFromUniversalA2AResult({result:{...artifact.result,canonical_workspace_mutated:true}}),/immutable/);
assert.throws(()=>evidenceFromUniversalA2AResult({result:{...artifact.result,production_promoted:true}}),/production-promoted/);
console.log('DORE_LIVING_WATER_RUNTIME_ARTIFACT=PASS');
