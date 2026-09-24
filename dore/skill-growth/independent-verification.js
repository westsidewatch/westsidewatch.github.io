export const VERIFICATION_STATES = Object.freeze(['PASS','FAIL','UNKNOWN']);

export function verifyOutcome({ action, observableDelta, expectedState, consumerVerification } = {}) {
  if (!action) throw new Error('verification requires action');
  if (!expectedState) throw new Error('verification requires expected state');

  const raw = consumerVerification?.status || 'UNKNOWN';
  const status = VERIFICATION_STATES.includes(raw) ? raw : 'UNKNOWN';
  const independent = consumerVerification?.independent === true;
  const evidence = [...new Set(consumerVerification?.evidence || [])];

  // A model/action claiming success is never verification.
  const verifiedStatus = independent ? status : 'UNKNOWN';

  return Object.freeze({
    action,
    observableDelta: observableDelta ?? null,
    expectedState,
    status: verifiedStatus,
    independent,
    evidence,
    authority: Object.freeze({
      consumerOwnsVerdict: true,
      reflexMayOverrideConsumer: false,
      unknownMayPass: false
    })
  });
}

export function verifyDesignOutcome(input = {}) {
  const functional = verifyOutcome(input.functional || {});
  const beautiful = verifyOutcome(input.beautiful || {});

  // Beautiful Gate is a separate prerequisite for design acceptance.
  const status = functional.status === 'FAIL' || beautiful.status === 'FAIL' ? 'FAIL'
    : functional.status === 'PASS' && beautiful.status === 'PASS' ? 'PASS'
    : 'UNKNOWN';

  return Object.freeze({
    status,
    functional,
    beautiful,
    gates: Object.freeze({
      functionalPassIsBeautifulPass: false,
      beautifulRequired: true
    })
  });
}
