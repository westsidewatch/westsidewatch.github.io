import { createTasteEpisode } from './design-taste-episode.js';

const REQUIRED_BEAUTY = Object.freeze(['beautiful_is_floor','real_browser_raster_required','material_divergence_required']);

export function adaptLivingWaterBloomSpec(spec = {}) {
  if (spec.consumer !== 'living-water') throw new Error('Living Water runtime adapter requires living-water consumer');
  for (const key of REQUIRED_BEAUTY) if (spec.beauty_admission?.[key] !== true) throw new Error(`Living Water runtime missing beauty admission: ${key}`);
  if (spec.production_promoted !== false) throw new Error('learning adapter refuses production-promoted experiment');
  const domains = spec.candidate_domains || [];
  if (domains.length < 2) throw new Error('Living Water taste learning requires divergent candidate domains');
  return Object.freeze({kind:'design.runtime-adapter',consumer:'living-water',sourceSchema:spec.schema,candidateIds:domains.map(x=>x.id),beautyFirst:true,requiresRealBrowserRaster:true,authority:Object.freeze({canonical:false,maySelfPromote:false,visualEvidenceOnly:true})});
}

export function openLivingWaterTasteEpisode(adapter,{id,context='living-water-bloom-armed-v2'}={}) {
  return createTasteEpisode({id,consumer:adapter.consumer,context,candidates:adapter.candidateIds.map(candidateId=>({id:candidateId,source:adapter.sourceSchema}))});
}

// Exact legacy Universal A2A Design artifact contract proven by PR #728:
// result.candidates[*].raster.real_browser_render + raster.sha256,
// result.critic.votes (two blind judges), canonical_workspace_mutated=false,
// production_promoted=false. This adapter consumes it; it does not redefine it.
export function evidenceFromUniversalA2AResult(result = {}, { visualEvidenceId } = {}) {
  const design = result.result || result;
  const candidates = design.candidates || [];
  if (design.canonical_workspace_mutated !== false) throw new Error('canonical workspace must remain immutable');
  if (design.production_promoted !== false) throw new Error('runtime evidence cannot already be production-promoted');
  if (design.provider !== 'dore-local') throw new Error('real Universal A2A design provider required');
  const votes = design.critic?.votes || [];
  if (votes.length !== 2) throw new Error('two blind judge votes required');
  const evidence = candidates.map((candidate,index)=>{
    const raster=candidate.raster||{};
    if (raster.real_browser_render !== true || !raster.sha256) throw new Error(`candidate ${index} lacks proven browser raster`);
    return {id:`raster:${raster.sha256}`,kind:'real-render',runtime:'browser-raster',candidate:candidate.id||candidate.candidate_id||String(index),sha256:raster.sha256};
  });
  if (visualEvidenceId) evidence.push({id:visualEvidenceId,kind:'visual-evidence'});
  evidence.push({id:`blind-judge:${votes.length}:${candidates.length}`,kind:'beautiful-gate',votes:2});
  return Object.freeze(evidence);
}

export function admitLivingWaterRuntimeEvidence(adapter,episode,evidence=[]) {
  const candidateIds=new Set(adapter.candidateIds);
  const rastered=new Set(evidence.filter(x=>x.kind==='real-render'&&x.runtime==='browser-raster'&&x.sha256).map(x=>x.candidate));
  const unknown=evidence.filter(x=>x.candidate&&!candidateIds.has(x.candidate));
  if(unknown.length) throw new Error('runtime evidence references unknown Living Water candidate');
  const missing=adapter.candidateIds.filter(id=>!rastered.has(id));
  if(missing.length) throw new Error(`real browser raster missing for: ${missing.join(',')}`);
  if(!evidence.some(x=>x.kind==='visual-evidence')) throw new Error('Living Water learning requires Visual Evidence authority');
  const beauty=evidence.find(x=>x.kind==='beautiful-gate');
  if(!beauty||beauty.votes!==2) throw new Error('Living Water learning requires two-judge Beautiful Gate evidence');
  return Object.freeze({kind:'design.runtime-evidence-envelope',episodeId:episode.id,consumer:adapter.consumer,candidates:[...adapter.candidateIds],evidence:evidence.map(x=>x.id),readyForPairwiseTaste:true,authority:Object.freeze({canonical:false,maySelfPromote:false})});
}
