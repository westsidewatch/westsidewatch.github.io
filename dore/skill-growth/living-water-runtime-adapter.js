import { createTasteEpisode } from './design-taste-episode.js';

const REQUIRED_BEAUTY = Object.freeze([
  'beautiful_is_floor',
  'real_browser_raster_required',
  'material_divergence_required'
]);

export function adaptLivingWaterBloomSpec(spec = {}) {
  if (spec.consumer !== 'living-water') throw new Error('Living Water runtime adapter requires living-water consumer');
  for (const key of REQUIRED_BEAUTY) {
    if (spec.beauty_admission?.[key] !== true) throw new Error(`Living Water runtime missing beauty admission: ${key}`);
  }
  if (spec.production_promoted !== false) throw new Error('learning adapter refuses production-promoted experiment');
  const domains = spec.candidate_domains || [];
  if (domains.length < 2) throw new Error('Living Water taste learning requires divergent candidate domains');

  return Object.freeze({
    kind: 'design.runtime-adapter',
    consumer: 'living-water',
    sourceSchema: spec.schema,
    candidateIds: domains.map(x => x.id),
    beautyFirst: true,
    requiresRealBrowserRaster: true,
    authority: Object.freeze({ canonical: false, maySelfPromote: false, visualEvidenceOnly: true })
  });
}

export function openLivingWaterTasteEpisode(adapter, { id, context = 'living-water-bloom-armed-v2' } = {}) {
  return createTasteEpisode({
    id,
    consumer: adapter.consumer,
    context,
    candidates: adapter.candidateIds.map(candidateId => ({ id: candidateId, source: adapter.sourceSchema }))
  });
}

export function admitLivingWaterRuntimeEvidence(adapter, episode, evidence = []) {
  const candidateIds = new Set(adapter.candidateIds);
  const rastered = new Set(evidence.filter(x => x.kind === 'real-render' && x.runtime === 'browser-raster').map(x => x.candidate));
  const unknown = evidence.filter(x => x.candidate && !candidateIds.has(x.candidate));
  if (unknown.length) throw new Error('runtime evidence references unknown Living Water candidate');
  const missing = adapter.candidateIds.filter(id => !rastered.has(id));
  if (missing.length) throw new Error(`real browser raster missing for: ${missing.join(',')}`);
  if (!evidence.some(x => x.kind === 'visual-evidence')) throw new Error('Living Water learning requires Visual Evidence authority');
  if (!evidence.some(x => x.kind === 'beautiful-gate')) throw new Error('Living Water learning requires Beautiful Gate evidence');

  return Object.freeze({
    kind: 'design.runtime-evidence-envelope',
    episodeId: episode.id,
    consumer: adapter.consumer,
    candidates: [...adapter.candidateIds],
    evidence: evidence.map(x => x.id),
    readyForPairwiseTaste: true,
    authority: Object.freeze({ canonical: false, maySelfPromote: false })
  });
}
