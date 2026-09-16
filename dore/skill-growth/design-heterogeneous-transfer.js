import { contaminationBlock, assertCrossProjectTransfer } from './project-contamination.js';
import { validatePreferenceTransfer, preferenceTransferToExperience } from './design-taste-episode.js';

export function transferLivingWaterPreference(realTaste, { targetProject, targetContext, transferableItems = [], targetEvidence = [], styleLeakage = null } = {}) {
  if (!realTaste?.delta) throw new Error('Living Water real Preference Delta required');
  if (!targetProject || targetProject === 'living-water') throw new Error('materially different consumer required');
  const contamination = contaminationBlock(transferableItems, { currentProject: targetProject });
  if (contamination.blocked.length) throw new Error(`project contamination blocked: ${contamination.blocked.map(x=>x.id).join(',')}`);
  const capability = `design.taste:${realTaste.delta.change}`;
  const projectTransfer = assertCrossProjectTransfer({ capability, sourceProject:'living-water', targetProject, contamination, evidence:targetEvidence });
  const preferenceTransfer = validatePreferenceTransfer(realTaste.delta, { sourceContext:'living-water-bloom', targetContext, result:'confirmed', styleLeakage, evidence:targetEvidence });
  return Object.freeze({ kind:'design.heterogeneous-transfer', targetProject, capability, projectTransfer, preferenceTransfer, contamination, authority:Object.freeze({canonical:false,maySelfPromote:false}) });
}

export function heterogeneousTransferToExperience(transfer, observationId) {
  if (!transfer.projectTransfer.promotionEligible || !transfer.preferenceTransfer.promotionEligible) throw new Error('heterogeneous transfer is not promotion eligible');
  return preferenceTransferToExperience(transfer.preferenceTransfer, observationId);
}
