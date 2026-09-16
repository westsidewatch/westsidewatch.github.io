import { consolidateExperiences } from './capability-lifecycle.js';

function normalizedEvidence(experiences) {
  return [...new Set(experiences.flatMap(x => x.evidence || []))].sort();
}

export function consolidateTasteExperiences(experiences = [], existingCapabilities = []) {
  const base = consolidateExperiences(experiences, existingCapabilities);
  const valid = experiences.filter(x => x?.state === 'experience');

  if (!['create', 'improve', 'merge'].includes(base.action)) {
    return Object.freeze({ ...base, pattern: null, authority: Object.freeze({ canonical: false, maySelfPromote: false }) });
  }

  const recurrenceKeys = [...new Set(valid.map(x => x.recurrenceKey).filter(Boolean))];
  if (recurrenceKeys.length !== 1) throw new Error('taste pattern requires one causal recurrence key');

  const pattern = Object.freeze({
    id: `pattern:${recurrenceKeys[0]}`,
    state: 'pattern',
    kind: 'design.taste-pattern',
    recurrenceKey: recurrenceKeys[0],
    signals: [...new Set(valid.map(x => x.signal).filter(Boolean))],
    experienceIds: valid.map(x => x.id).sort(),
    evidence: normalizedEvidence(valid),
    targetCapabilities: [...(base.targets || [])],
    disposition: base.action,
    authority: Object.freeze({ canonical: false, maySelfPromote: false }),
    requiredNextStage: 'sandbox-candidate'
  });

  return Object.freeze({ ...base, pattern, authority: Object.freeze({ canonical: false, maySelfPromote: false }) });
}

export function admitTastePatternCandidate(consolidation, { sandboxEvidence = [], conservation = null } = {}) {
  if (!consolidation?.pattern) throw new Error('candidate requires consolidated taste pattern');
  if (!sandboxEvidence.length) throw new Error('taste candidate requires sandbox evidence');
  if (conservation?.pass !== true) throw new Error('taste candidate requires capability conservation PASS');

  return Object.freeze({
    id: `candidate:${consolidation.pattern.id}`,
    state: 'candidate',
    kind: 'design.taste-skill-candidate',
    patternId: consolidation.pattern.id,
    disposition: consolidation.action,
    targetCapabilities: [...(consolidation.targets || [])],
    sandboxEvidence: [...sandboxEvidence],
    conservation,
    authority: Object.freeze({ canonical: false, maySelfPromote: false }),
    requiredNextStage: 'existing-skill-growth-promotion-gate'
  });
}
