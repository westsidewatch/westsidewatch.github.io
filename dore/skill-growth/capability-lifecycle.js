const ACTIVE_STATES = new Set(['experience', 'pattern', 'candidate', 'skill', 'policy', 'compiled']);
const TERMINAL_STATES = new Set(['retired']);

export const LIFECYCLE_STATES = Object.freeze([
  'experience', 'pattern', 'candidate', 'skill', 'policy', 'compiled', 'retired'
]);

export const CONSOLIDATION_ACTIONS = Object.freeze([
  'discard', 'hold', 'improve', 'merge', 'create', 'reopen', 'supersede', 'retire'
]);

export function createExperience(observation, options = {}) {
  if (!observation?.id) throw new Error('experience requires observation id');
  return Object.freeze({
    id: options.id || `experience:${observation.id}`,
    state: 'experience',
    observationIds: [observation.id],
    recurrenceKey: observation.recurrenceKey || null,
    signal: observation.signal || '',
    relatedCapabilities: [...(observation.relatedCapabilities || [])].sort(),
    evidence: [...(observation.evidence || [])],
    authority: Object.freeze({ canonical: false, maySelfPromote: false })
  });
}

export function consolidateExperiences(experiences = [], existingCapabilities = []) {
  const valid = experiences.filter(item => item?.state === 'experience');
  if (!valid.length) return { action: 'discard', reason: 'no-experience-evidence', experiences: [] };

  const keys = new Set(valid.map(item => item.recurrenceKey).filter(Boolean));
  const capabilities = new Set(valid.flatMap(item => item.relatedCapabilities || []));
  const matching = existingCapabilities.filter(entry => capabilities.has(entry.id));

  if (keys.size > 1) return { action: 'hold', reason: 'unconsolidated-signals', experiences: valid.map(x => x.id) };
  if (matching.length > 1) return { action: 'merge', targets: matching.map(x => x.id).sort(), experiences: valid.map(x => x.id) };
  if (matching.length === 1) return { action: 'improve', targets: [matching[0].id], experiences: valid.map(x => x.id) };
  if (valid.length < 2) return { action: 'hold', reason: 'single-experience-is-not-a-skill', experiences: valid.map(x => x.id) };
  return { action: 'create', experiences: valid.map(x => x.id) };
}

export function assertLifecycleTransition(from, to, evidence = {}) {
  if (!LIFECYCLE_STATES.includes(from) || !LIFECYCLE_STATES.includes(to)) throw new Error('unknown lifecycle state');
  if (TERMINAL_STATES.has(from) && to !== 'experience') throw new Error('retired capability must reopen through new experience');
  if (to === 'retired' && !evidence.supersededBy && !evidence.retirementAuthority) throw new Error('retirement requires supersession or authority evidence');
  if (to === 'compiled' && !evidence.capabilityConservation) throw new Error('compile requires capability conservation evidence');
  if ((to === 'skill' || to === 'policy') && !evidence.promotionGate) throw new Error('canonical maturity requires promotion gate evidence');
  return true;
}

export function evaluateConservation({ protectedCapabilities = [], results = {}, transfer = null, antiForgetting = null } = {}) {
  const missing = protectedCapabilities.filter(id => results[id] !== true);
  const pass = missing.length === 0 && transfer !== false && antiForgetting !== false;
  return Object.freeze({
    pass,
    missing,
    transferPassed: transfer !== false,
    antiForgettingPassed: antiForgetting !== false,
    authority: Object.freeze({ maySelfPromote: false })
  });
}

export function learningPressure(signals = [], budget = {}) {
  const weights = { failure: 4, correction: 5, 'transfer-failure': 6, 'high-variance': 3, friction: 2, 'external-capability': 2 };
  const score = signals.reduce((sum, signal) => sum + (weights[signal.kind] || 1) * (signal.severity || 1), 0);
  const threshold = budget.threshold ?? 8;
  return Object.freeze({ score, threshold, openEvolutionEpisode: score >= threshold });
}

export function isActiveLifecycleState(state) {
  return ACTIVE_STATES.has(state);
}
