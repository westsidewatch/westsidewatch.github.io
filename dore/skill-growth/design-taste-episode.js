import { createExperience } from './capability-lifecycle.js';
import { preferenceDelta } from './design-conservation.js';

export function createTasteEpisode({ id, consumer, candidates = [], context } = {}) {
  if (!id || !consumer || !context) throw new Error('taste episode requires id, consumer and context');
  if (candidates.length < 2) throw new Error('taste episode requires divergent candidates');
  if (new Set(candidates.map(x => x.id)).size !== candidates.length) throw new Error('candidate ids must be unique');
  return Object.freeze({
    id,
    kind: 'design.taste-episode',
    consumer,
    context,
    candidates: candidates.map(candidate => Object.freeze({ ...candidate })),
    stage: 'awaiting-real-render',
    authority: Object.freeze({ canonical: false, maySelfPromote: false })
  });
}

export function admitPairwisePreference(episode, { preferred, rejected, change, conditions = [], evidence = [] } = {}) {
  const ids = new Set(episode.candidates.map(x => x.id));
  if (!ids.has(preferred) || !ids.has(rejected) || preferred === rejected) throw new Error('preference must compare two episode candidates');
  const rendered = new Set(evidence.filter(x => x.kind === 'real-render').map(x => x.candidate));
  if (!rendered.has(preferred) || !rendered.has(rejected)) throw new Error('pairwise taste requires real renders for both candidates');
  const comparison = evidence.filter(x => x.kind === 'pairwise-comparison');
  if (!comparison.length) throw new Error('pairwise taste requires comparison evidence');

  return preferenceDelta({
    before: rejected,
    after: preferred,
    change,
    conditions,
    evidence: evidence.map(x => x.id)
  });
}

export function validatePreferenceTransfer(delta, { sourceContext, targetContext, result, styleLeakage = null, evidence = [] } = {}) {
  if (!sourceContext || !targetContext || sourceContext === targetContext) throw new Error('cross-context validation requires a different target context');
  if (!['confirmed', 'contradicted', 'inconclusive'].includes(result)) throw new Error('unknown transfer result');
  if (!evidence.length) throw new Error('cross-context validation requires evidence');
  if (result === 'confirmed' && styleLeakage !== false) throw new Error('confirmed transfer requires explicit no-style-leakage evidence');
  return Object.freeze({
    kind: 'design.preference-transfer',
    delta,
    sourceContext,
    targetContext,
    result,
    styleLeakage,
    evidence: [...evidence],
    promotionEligible: result === 'confirmed' && styleLeakage === false,
    authority: Object.freeze({ canonical: false, maySelfPromote: false })
  });
}

export function preferenceTransferToExperience(transfer, observationId) {
  if (!transfer.promotionEligible) throw new Error('only confirmed no-leakage transfer can become Skill Growth experience');
  return createExperience({
    id: observationId,
    recurrenceKey: `design:taste:${transfer.delta.change}`,
    signal: transfer.delta.change,
    relatedCapabilities: ['design.taste'],
    evidence: [...transfer.delta.evidence, ...transfer.evidence]
  });
}
