import assert from 'node:assert/strict';
import { adaptLivingWaterBloomSpec, openLivingWaterTasteEpisode, admitLivingWaterRuntimeEvidence } from './living-water-runtime-adapter.js';

const spec={schema:'dore.living-water-bloom-armed.v2',consumer:'living-water',production_promoted:false,beauty_admission:{beautiful_is_floor:true,real_browser_raster_required:true,material_divergence_required:true},candidate_domains:[{id:'sacred-threshold'},{id:'quiet-light'},{id:'living-community'},{id:'architectural-bloom'}]};
const adapter=adaptLivingWaterBloomSpec(spec);
assert.equal(adapter.beautyFirst,true);assert.equal(adapter.requiresRealBrowserRaster,true);assert.equal(adapter.authority.visualEvidenceOnly,true);
const episode=openLivingWaterTasteEpisode(adapter,{id:'living-water:real-runtime:01'});assert.equal(episode.candidates.length,4);
const realRenders=adapter.candidateIds.map(candidate=>({id:`raster:${candidate}`,kind:'real-render',runtime:'browser-raster',candidate,sha256:`sha-${candidate}`}));
const envelope=admitLivingWaterRuntimeEvidence(adapter,episode,[...realRenders,{id:'visual-evidence:italian-editorial-atlas',kind:'visual-evidence'},{id:'beautiful-gate:living-water:01',kind:'beautiful-gate',votes:2}]);
assert.equal(envelope.readyForPairwiseTaste,true);assert.equal(envelope.candidates.length,4);
assert.throws(()=>admitLivingWaterRuntimeEvidence(adapter,episode,[...realRenders.slice(0,3),{id:'visual:e',kind:'visual-evidence'},{id:'beauty:e',kind:'beautiful-gate',votes:2}]),/real browser raster missing/);
assert.throws(()=>adaptLivingWaterBloomSpec({...spec,beauty_admission:{...spec.beauty_admission,beautiful_is_floor:false}}),/beauty admission/);
console.log('DORE_LIVING_WATER_RUNTIME_ADAPTER=PASS');
