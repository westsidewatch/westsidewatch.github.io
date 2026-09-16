import { evidenceFromUniversalA2AResult } from './living-water-runtime-adapter.js';
import { admitPairwisePreference } from './design-taste-episode.js';

export function pairwiseComparisonFromA2A(episode, a2aResult, { preferred, rejected, change, conditions = [], visualEvidenceId } = {}) {
  const evidence = evidenceFromUniversalA2AResult(a2aResult, { visualEvidenceId });
  const renders = evidence.filter(x => x.kind === 'real-render');
  const ids = new Set(renders.map(x => x.candidate));
  if (!ids.has(preferred) || !ids.has(rejected)) throw new Error('preferred and rejected candidates require proven A2A rasters');
  const design = a2aResult.result || a2aResult;
  const votes = design.critic?.votes || [];
  const comparison = { id:`pairwise:${rejected}->${preferred}`, kind:'pairwise-comparison', preferred, rejected, judgeEvidence:votes.map((vote,i)=>vote.id||vote.judge||`blind-${i+1}`) };
  const delta = admitPairwisePreference(episode, { preferred, rejected, change, conditions, evidence:[...renders, comparison] });
  return Object.freeze({ kind:'living-water.real-taste-result', preferred, rejected, rasterEvidence:renders.map(x=>x.id), blindJudgeEvidence:comparison.judgeEvidence, delta, authority:Object.freeze({canonical:false,maySelfPromote:false}) });
}
