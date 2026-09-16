import { evaluateDesignConservation, DESIGN_CONSERVATION_CANARIES } from './design-conservation.js';

export function runDesignCapabilityMutationProbe(baseline, capability) {
  if (!DESIGN_CONSERVATION_CANARIES.includes(capability)) throw new Error(`unknown protected Design capability: ${capability}`);
  const canaries = { ...(baseline.canaries || {}), [capability]: false };
  const mutated = evaluateDesignConservation({ ...baseline, canaries });
  return Object.freeze({
    kind: 'design.capability-mutation-probe',
    capability,
    detected: mutated.pass === false && mutated.missing.includes(capability),
    conservation: mutated,
    authority: Object.freeze({ canonical: false, maySelfPromote: false })
  });
}

export function runDesignMutationSuite(baseline) {
  const probes = DESIGN_CONSERVATION_CANARIES.map(capability => runDesignCapabilityMutationProbe(baseline, capability));
  const escaped = probes.filter(probe => !probe.detected).map(probe => probe.capability);
  return Object.freeze({
    kind: 'design.capability-mutation-suite',
    pass: escaped.length === 0,
    probes,
    escaped,
    requiredAction: escaped.length ? 'grow-conservation-test-capability' : 'none',
    authority: Object.freeze({ canonical: false, maySelfPromote: false })
  });
}

export function antiForgettingGate({ previousProtected = [], currentResults = {}, newCapabilityPassed = false, transferPassed = false } = {}) {
  const regressions = previousProtected.filter(id => currentResults[id] !== true);
  return Object.freeze({
    kind: 'dore.anti-forgetting-gate',
    pass: newCapabilityPassed === true && transferPassed === true && regressions.length === 0,
    newCapabilityPassed: newCapabilityPassed === true,
    transferPassed: transferPassed === true,
    regressions,
    disposition: regressions.length ? 'block-promotion' : (newCapabilityPassed && transferPassed ? 'admit-to-next-gate' : 'hold'),
    authority: Object.freeze({ canonical: false, maySelfPromote: false })
  });
}
