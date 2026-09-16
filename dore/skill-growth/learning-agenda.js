import { learningPressure } from './capability-lifecycle.js';

const SIGNAL_VALUE = Object.freeze({
  failure: 4,
  correction: 5,
  'transfer-failure': 7,
  'high-variance': 4,
  friction: 2,
  'external-capability': 2,
  regression: 7,
  'capability-loss': 9
});

function capabilityScore(signals) {
  const pressure = learningPressure(signals);
  const weighted = signals.reduce((sum, signal) =>
    sum + (SIGNAL_VALUE[signal.kind] || 1) * (signal.severity || 1) * (signal.confidence ?? 1), 0);
  const distinctKinds = new Set(signals.map(x => x.kind)).size;
  const evidenceBonus = Math.min(4, new Set(signals.flatMap(x => x.evidence || [])).size);
  return { pressure, score: weighted + distinctKinds + evidenceBonus };
}

export function buildLearningAgenda(signals = [], options = {}) {
  const maxActive = options.maxActive ?? 3;
  const minScore = options.minScore ?? 8;
  const grouped = new Map();

  for (const signal of signals) {
    if (!signal?.capability || !signal?.kind) continue;
    if (!grouped.has(signal.capability)) grouped.set(signal.capability, []);
    grouped.get(signal.capability).push(signal);
  }

  const ranked = [...grouped.entries()].map(([capability, items]) => {
    const { pressure, score } = capabilityScore(items);
    return Object.freeze({
      capability,
      score,
      pressure: pressure.score,
      signals: items.map(x => x.id).filter(Boolean).sort(),
      evidence: [...new Set(items.flatMap(x => x.evidence || []))].sort(),
      eligible: score >= minScore && pressure.openEvolutionEpisode
    });
  }).sort((a, b) => b.score - a.score || a.capability.localeCompare(b.capability));

  const active = ranked.filter(x => x.eligible).slice(0, maxActive);
  const activeIds = new Set(active.map(x => x.capability));
  const hold = ranked.filter(x => !activeIds.has(x.capability));

  return Object.freeze({
    kind: 'dore.learning-agenda',
    active,
    hold,
    maxActive,
    authority: Object.freeze({ canonical: false, maySelfPromote: false })
  });
}

export function allocateLearningBudget(agenda, budget = {}) {
  const total = budget.total ?? 12;
  const minimum = budget.minimumPerActive ?? 2;
  const active = agenda.active;
  if (!active.length) return Object.freeze({ allocations: [], unused: total });

  const floor = Math.min(minimum, Math.floor(total / active.length));
  let remaining = total - floor * active.length;
  const totalScore = active.reduce((sum, x) => sum + x.score, 0);
  const allocations = active.map((item, index) => {
    const isLast = index === active.length - 1;
    const extra = isLast ? remaining : Math.min(remaining, Math.floor((item.score / totalScore) * (total - floor * active.length)));
    remaining -= extra;
    return Object.freeze({
      capability: item.capability,
      units: floor + extra,
      mode: item.score >= (budget.fullExplorationScore ?? 20) ? 'full-exploration' : 'light-loop'
    });
  });

  return Object.freeze({ allocations, unused: remaining, authority: Object.freeze({ maySelfPromote: false }) });
}
