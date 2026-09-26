import {geographicToENU} from './terrain-runtime.js';

export function resolveSpatialRegistration(object,terrain){
  const spatial=object?.spatial||{};
  const registration=String(spatial.registration||'');
  if(registration.startsWith('withheld')||object?.geometry?.status==='withheld')return{renderable:false,reason:'withheld'};
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
    sourceRegistration:registration,
    accuracy:spatial.accuracy||'unspecified'
  };
}
