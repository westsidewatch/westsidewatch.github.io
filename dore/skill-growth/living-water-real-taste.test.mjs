import assert from 'node:assert/strict';
import { createTasteEpisode } from './design-taste-episode.js';
import { pairwiseComparisonFromA2A } from './living-water-real-taste.js';

const episode=createTasteEpisode({id:'lw:real:01',consumer:'living-water',context:'living-water-bloom',candidates:[{id:'sacred-threshold'},{id:'quiet-light'}]});
const artifact={result:{provider:'dore-local',model:'real-local-model',canonical_workspace_mutated:false,production_promoted:false,candidates:[
 {id:'sacred-threshold',raster:{real_browser_render:true,sha256:'sha-sacred'}},
 {id:'quiet-light',raster:{real_browser_render:true,sha256:'sha-quiet'}}
],critic:{votes:[{id:'judge:1',judge:'blind-1'},{id:'judge:2',judge:'blind-2'}]}}};
const learned=pairwiseComparisonFromA2A(episode,artifact,{preferred:'quiet-light',rejected:'sacred-threshold',change:'hierarchy-through-light',conditions:['church-identity-preserved','typography-carries-presence'],visualEvidenceId:'atlas:casabella-domus'});
assert.equal(learned.delta.kind,'design.preference-delta');
assert.equal(learned.delta.before,'sacred-threshold');
assert.equal(learned.delta.after,'quiet-light');
assert.equal(learned.blindJudgeEvidence.length,2);
assert.ok(learned.rasterEvidence.every(x=>x.startsWith('raster:sha-')));
assert.equal(learned.authority.maySelfPromote,false);
assert.equal('score' in learned.delta,false);
assert.throws(()=>pairwiseComparisonFromA2A(episode,{result:{...artifact.result,candidates:[artifact.result.candidates[0]]}},{preferred:'quiet-light',rejected:'sacred-threshold',change:'x'}),/proven A2A rasters/);
console.log('DORE_LIVING_WATER_REAL_TASTE=PASS');
