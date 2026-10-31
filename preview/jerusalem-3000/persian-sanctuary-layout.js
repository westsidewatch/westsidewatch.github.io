import {compileSanctuaryComponents} from './sanctuary-component-layout.js';
const PHASE='persian-nehemiah';
export const SANCTUARY_GATE_ID='j3k:persian-nehemiah:gate:sanctuary-south';
export const SANCTUARY_ACCESS_ID='j3k:persian-nehemiah:road:sanctuary-access';
export function compilePersianSanctuary(data) {
  const phase=data.phases?.[PHASE],s=phase?.sanctuary;
  if(!s || s.objectId!=='j3k:object:second-temple-early' || s.geometryValidityPhases?.length!==1 || s.geometryValidityPhases[0]!==PHASE)throw new Error('Invalid Persian sanctuary authority');
  return compileSanctuaryComponents(phase,{phaseId:PHASE,gateId:SANCTUARY_GATE_ID,accessId:SANCTUARY_ACCESS_ID,approachId:'northern-rebuilding-access',approachObjectId:'j3k:persian-nehemiah:road:northern-rebuilding-access',reservationId:'second-temple-location-reservation'});
}
