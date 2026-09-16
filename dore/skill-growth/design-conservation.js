import { evaluateConservation } from './capability-lifecycle.js';

export const DESIGN_CONSERVATION_CANARIES = Object.freeze([
  'design.visual-evidence',
  'design.taste',
  'design.beautiful-gate',
  'design.consumer-identity',
  'design.transfer'
]);

export function evaluateDesignConservation({
  canaries = {},
  transfer = {},
  antiForgetting = {},
  beauty = {},
  consumerIdentity = {}
} = {}) {
  const results = Object.fromEntries(
    DESIGN_CONSERVATION_CANARIES.map(id => [id, canaries[id] === true])
  );

  // Beauty is first authority: a technically valid concentration cannot PASS
  // if the real rendered result loses aesthetic quality.
  results['design.beautiful-gate'] =
    results['design.beautiful-gate'] &&
    beauty.realRender === true &&
    beauty.beautifulGate === true;

  // Consumer identity is conserved separately from transferable capability.
  results['design.consumer-identity'] =
    results['design.consumer-identity'] &&
    consumerIdentity.preserved === true;

  // Transfer means capability reuse on a materially different consumer,
  // never importing the source consumer's visual identity.
  const transferPassed =
    transfer.materiallyDifferentConsumer === true &&
    transfer.capabilityReused === true &&
    transfer.styleLeakage === false;

  const antiForgettingPassed =
    antiForgetting.previousCanariesPassed === true &&
    antiForgetting.regressions?.length === 0;

  const conservation = evaluateConservation({
    protectedCapabilities: DESIGN_CONSERVATION_CANARIES,
    results,
    transfer: transferPassed,
    antiForgetting: antiForgettingPassed
  });

  return Object.freeze({
    ...conservation,
    beautyFirst: results['design.beautiful-gate'],
    consumerIdentityPreserved: results['design.consumer-identity'],
    styleLeakage: transfer.styleLeakage ?? null,
    disposition: conservation.pass ? 'conserve' : 'block-concentration',
    authority: Object.freeze({
      canonical: false,
      maySelfPromote: false,
      requiresRealRender: true,
      requiresHumanOrIndependentTasteEvidence: true
    })
  });
}

export function preferenceDelta({ before, after, change, conditions = [], evidence = [] } = {}) {
  if (!before || !after || !change) throw new Error('preference delta requires before, after and causal change');
  if (!evidence.length) throw new Error('preference delta requires comparison evidence');
  return Object.freeze({
    kind: 'design.preference-delta',
    before,
    after,
    change,
    conditions: [...conditions],
    evidence: [...evidence],
    authority: Object.freeze({ canonical: false, maySelfPromote: false }),
    requiredNextStage: 'cross-context-validation'
  });
}
