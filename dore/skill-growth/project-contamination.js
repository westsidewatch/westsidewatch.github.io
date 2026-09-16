const IDENTITY_CLASSES = new Set(['project-thesis','project-motif','symbolic-vocabulary','character-voice','chapter-inner-action','signature-phrase','project-theological-conclusion','surface-specific-style']);

export function contaminationBlock(items = [], { currentProject } = {}) {
  const admitted = [];
  const blocked = [];
  for (const item of items) {
    const identityBound = IDENTITY_CLASSES.has(item.kind) || item.projectId && item.projectId !== currentProject && item.transferable !== true;
    (identityBound ? blocked : admitted).push(item);
  }
  return Object.freeze({
    kind: 'dore.project-contamination-block',
    currentProject,
    admitted,
    blocked,
    pass: blocked.length === 0,
    authority: Object.freeze({ canonical: false, maySelfPromote: false })
  });
}

export function assertCrossProjectTransfer({ capability, sourceProject, targetProject, contamination, evidence = [] } = {}) {
  if (!capability || !sourceProject || !targetProject || sourceProject === targetProject) throw new Error('heterogeneous project transfer required');
  if (!evidence.length) throw new Error('cross-project transfer requires evidence');
  if (contamination?.blocked?.length) throw new Error('project identity contamination blocks transfer');
  return Object.freeze({
    kind: 'dore.cross-project-capability-transfer', capability, sourceProject, targetProject,
    evidence: [...evidence], promotionEligible: true,
    authority: Object.freeze({ canonical: false, maySelfPromote: false })
  });
}
