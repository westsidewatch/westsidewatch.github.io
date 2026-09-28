import { assessReflexCandidate } from './reflex-candidate-contract.js';

export function compileExperienceTraces(events = [], options = {}) {
  const groups = new Map();
  for (const event of events) {
    if (!event?.recurrenceKey || !event?.decision || !event?.verification) continue;
    const key = [event.recurrenceKey, event.decision].join('::');
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(event);
  }

  return [...groups.entries()].map(([key, traces]) => {
    const verified = traces.filter(x => x.verification === 'PASS');
    const failed = traces.filter(x => x.verification === 'FAIL');
    const unknown = traces.filter(x => x.verification === 'UNKNOWN');
    const exemplar = traces[0];
    return assessReflexCandidate({
      id: `reflex-candidate:${key}`,
      evidence: traces.map(x => x.id).filter(Boolean),
      verifiedSuccesses: verified.length,
      bounded: traces.every(x => x.bounded === true),
      independentlyVerifiable: traces.every(x => x.independentVerifier === true),
      recoverable: traces.every(x => x.recoverable === true),
      authoritySafe: traces.every(x => x.authoritySafe === true),
      deterministic: exemplar.mode === 'deterministic',
      boundedChoice: exemplar.mode === 'bounded-choice',
      specialist: exemplar.mode === 'specialist',
      minimumRepeatedSuccesses: options.minimumRepeatedSuccesses ?? 2,
      traceSummary: { pass: verified.length, fail: failed.length, unknown: unknown.length }
    });
  });
}
