import {auditProductionReadiness} from './production-readiness.js';

const REQUIRED_PHASE_COUNT=18;
const REQUIRED_EVIDENCE_MODES=['all','observed','reconstructed','inferred','disputed'];

export function auditProductionCompletion(runtime={},timeline={}){
  const readiness=auditProductionReadiness(runtime);
  const failures=[...readiness.failures];
  const phases=Array.isArray(timeline.phases)?timeline.phases:[];
  if(phases.length!==REQUIRED_PHASE_COUNT)failures.push(`timeline-phases:${phases.length}/${REQUIRED_PHASE_COUNT}`);
  const covered=new Set(runtime.evidenceObjects?.objectContinuityPhases||[]);
  if(phases.some(phase=>!covered.has(phase.id)))failures.push('full-timeline-object-continuity-unverified');
  const ids=new Set(phases.map(phase=>phase.id));
  if(ids.size!==phases.length)failures.push('timeline-phase-ids-not-unique');
  const audit=runtime.evidenceObjects?.evidenceResolutionAudit;
  for(const mode of REQUIRED_EVIDENCE_MODES){if(audit?.visibleByMode?.[mode]===undefined)failures.push(`evidence-mode:${mode}`)}
  if(runtime.evidenceObjects?.terrain!=='canonical-dem')failures.push('terrain-authority');
  if(runtime.evidenceObjects?.spatialRegistration!=='canonical-dem-enu')failures.push('spatial-registration');
  if(runtime.evidenceObjects?.transformationRuntime!=='reversible-standing-to-ruin')failures.push('ruin-transformation');
  if(!runtime.evidenceObjects?.renderProfile)failures.push('render-profile');
  return{
    ok:failures.length===0,
    failures:[...new Set(failures)],
    readiness,
    phaseCount:phases.length,
    evidenceModes:REQUIRED_EVIDENCE_MODES,
    renderProfile:runtime.evidenceObjects?.renderProfile||null,
    completion:'Jerusalem 3000 / Steps 1–9'
  };
}
