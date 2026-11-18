// Complete the planning scaffold, not a population target or excavated house map.
// Existing named districts remain unchanged. A separate residual district uses
// the already selected contemporary enclosure; all old districts and protected
// precincts are subtracted before its blocks are made.
export function completeUrbanCoverage(registration,{rings=[]}={}){
 if(!rings.length||registration.districts.some(d=>d.metadata?.coverageResidual))return registration;
 if(registration.phase==='ottoman')for(const r of registration.roads)r.metadata={...r.metadata,layoutRole:r.metadata?.layoutRole||'old-city-route-context'};
 const existing=registration.districts.filter(d=>d.metadata?.layoutRole!=='extra-mural-expansion').map(d=>d.geometry.polygon);
 const area=p=>Math.abs(p.reduce((s,a,i)=>{const b=p[(i+1)%p.length];return s+a.x*b.z-b.x*a.z;},0))/2,ordered=[...rings].sort((a,b)=>area(a)-area(b));
 for(const [i,polygon]of ordered.entries())registration.districts.push({id:`j3k:${registration.phase}:district:urban-coverage-residual-${i}`,type:'district',confidence:'inferred',geometry:{primitive:'polygon',frame:'canonical-dem-enu',status:'whole-city-planning-context-not-surveyed-built-extent',polygon:polygon.map(p=>({...p}))},source:{authority:'residual planning scaffold inside existing selected enclosure, not measured occupation or individual houses',urls:registration.sources||[]},metadata:{coverageResidual:true,coverageExclusions:[...existing,...ordered.slice(0,i)],layoutRole:['ottoman','outside-walls','modern'].includes(registration.phase)?'old-city-context':'urban-coverage-context',historicalOccupationVerified:false}});
 registration.urbanCoverage={policy:'preserve-existing-districts-and-fill-residual-planning-scaffold',authority:'illustrative-not-surveyed-occupation',densityTarget:null,knownDimensionsRescaled:false};return registration;
}
