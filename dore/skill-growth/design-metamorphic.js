const RELATIONS = Object.freeze({
  'content-density': ['hierarchy-preserved', 'beautiful-gate-pass', 'no-generic-card-collapse'],
  'image-aspect-ratio': ['composition-recomputed', 'subject-weight-preserved', 'beautiful-gate-pass'],
  'consumer-transfer': ['capability-reused', 'consumer-identity-preserved', 'no-style-leakage'],
  'motion-emergence': ['semantic-emergence-preserved', 'timing-may-change', 'beautiful-gate-pass']
});

export const DESIGN_METAMORPHIC_RELATIONS = Object.freeze(Object.keys(RELATIONS));

export function createMetamorphicProbe({ id, relation, source, transformed, evidence = [] } = {}) {
  if (!id || !RELATIONS[relation]) throw new Error('known metamorphic relation required');
  if (!source || !transformed) throw new Error('metamorphic probe requires source and transformed cases');
  if (!evidence.length) throw new Error('metamorphic probe requires real evidence');
  return Object.freeze({
    id,
    kind: 'design.metamorphic-probe',
    relation,
    source,
    transformed,
    invariants: [...RELATIONS[relation]],
    evidence: [...evidence],
    authority: Object.freeze({ canonical: false, maySelfPromote: false })
  });
}

export function evaluateMetamorphicProbe(probe, results = {}) {
  const failed = probe.invariants.filter(invariant => results[invariant] !== true);
  return Object.freeze({
    probeId: probe.id,
    relation: probe.relation,
    pass: failed.length === 0,
    failed,
    disposition: failed.length ? 'capability-regression' : 'relation-preserved',
    authority: Object.freeze({ canonical: false, maySelfPromote: false })
  });
}

export function evaluateMetamorphicSuite(cases = []) {
  const failed = cases.filter(x => x?.pass !== true);
  return Object.freeze({
    kind: 'design.metamorphic-suite',
    pass: cases.length > 0 && failed.length === 0,
    failed: failed.map(x => x.probeId),
    relationsCovered: [...new Set(cases.map(x => x.relation))].sort(),
    authority: Object.freeze({ canonical: false, maySelfPromote: false })
  });
}
