import {housingBoundaryAt,housingFitsRing} from './housing-boundary.js';
import {clipBlockToEnvelope,subtractPlanarZones} from './district-infill.js';
// The selected authored wall bands, not additional historical dates/circuits.
export function housingBoundaryStages(options){
 const profile=options.defenseData.phases.find(p=>p.id===options.phaseId),bands=[...(profile?.walls||[]),...(profile?.extentReconstructions||[])],cuts=[...new Set([0,1,...bands.flatMap(b=>[b.fromOffset,b.toOffset])])].sort((a,b)=>a-b),intervals=cuts.slice(1).map((to,i)=>({from:cuts[i],to,...housingBoundaryAt({...options,offset:(cuts[i]+to)/2})})),rings=[...new Map(intervals.flatMap(s=>s.rings).map(r=>[JSON.stringify(r),r])).values()];
 return {intervals,rings,allIntervalsClosed:intervals.every(s=>s.rings.length>0)};
}
const area=p=>Math.abs(p.reduce((s,a,i)=>{const b=p[(i+1)%p.length];return s+a.x*b.z-b.x*a.z;},0))/2;
// Split only when a phase has multiple circuits. A complete block must not be
// withdrawn merely because one of its modules lies beyond a later inner wall.
export function splitHousingBoundaryBands(polygon,rings=[]){
 if(rings.length<2)return [{polygon,requiredRings:rings}];
 const ordered=[...rings].sort((a,b)=>area(a)-area(b)),result=[];let remaining=[polygon];
 for(const ring of ordered){for(const p of remaining)for(const part of clipBlockToEnvelope(p,ring))result.push({polygon:part,requiredRings:[ring,...ordered.filter(r=>r!==ring&&housingFitsRing(part,r,0))]});remaining=subtractPlanarZones(remaining,[ring]);}
 return result;
}
