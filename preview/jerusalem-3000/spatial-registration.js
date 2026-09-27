import {geographicToENU} from './terrain-runtime.js';

const PHASE2_BOUNDED_REGISTRATIONS=Object.freeze({
  'j3k:object:inner-temple':{
    source:'platform-bounded-reconstruction',
    accuracy:'platform-only',
    note:'Phase 2 visualization is constrained to the Herodian platform anchor; exact sanctuary placement remains reconstructed and must not be presented as surveyed.'
  }
});

export function resolveSpatialRegistration(object,terrain){
  const spatial=object?.spatial||{};
  const registration=String(spatial.registration||'');
  const bounded=PHASE2_BOUNDED_REGISTRATIONS[object?.id];
  if((registration.startsWith('withheld')||object?.geometry?.status==='withheld')&&!bounded)return{renderable:false,reason:'withheld'};
  const anchor=spatial.anchor;
  if(!anchor||!Number.isFinite(anchor.lat)||!Number.isFinite(anchor.lon))return{renderable:false,reason:'missing-anchor'};
  const origin=terrain?.grid?.origin;
  if(!origin||!Number.isFinite(origin.lat)||!Number.isFinite(origin.lon))throw new Error('Canonical DEM origin missing for spatial registration');
  const enu=geographicToENU(anchor.lat,anchor.lon,origin);
  const elevation=terrain.sampleElevation(anchor.lat,anchor.lon);
  if(!Number.isFinite(elevation))return{renderable:false,reason:'outside-dem'};
  return{
    renderable:true,
    frame:'canonical-dem-enu',
    east:enu.east,
    north:enu.north,
    up:elevation,
    anchor:{lat:anchor.lat,lon:anchor.lon},
    sourceRegistration:bounded?.source||registration,
    accuracy:bounded?.accuracy||spatial.accuracy||'unspecified',
    reconstructionConstraint:bounded?.note||null
  };
}
