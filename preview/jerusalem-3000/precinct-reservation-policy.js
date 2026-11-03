const area=p=>Math.abs(p.reduce((s,a,i)=>{const b=p[(i+1)%p.length];return s+a.x*b.z-b.x*a.z;},0))/2;
const polygon=r=>r.geometry?.polygon||r.polygon;
// An unlocated programme item is not evidence that a neighbourhood was empty.
// Preserve the authored source vector in a non-spatial planning list; keep actual
// sacred precincts and rendered core footprints as housing constraints.
export function reconcilePrecinctReservations(registration){
 const planning=[],active=[],rows=[];
 for(const r of registration.reservations||[]){const original=polygon(r),id=r.id.split(':').at(-1);let selected=original,reason='protected-sacred-court';
  if(['western-core-unfilled-not-measured','cotton-services-unfilled-not-footprint','administrative-core-unfilled'].includes(id)){
   planning.push({...r,metadata:{...r.metadata,planningOnly:true,spatialExclusionVerified:false,reason:'unlocated-programme-not-evidence-of-empty-land'}});rows.push({id,originalArea:area(original),activeArea:0,status:'non-spatial-programme'});continue;
  }
  const core=id==='eastern-precinct-unfilled'?registration.cores.find(c=>c.metadata.precinctContext):id==='southern-church-context-not-footprint'?registration.cores.find(c=>c.id.endsWith(':nea-context')):null;
  if(core){selected=core.geometry.polygon;reason='matched-rendered-precinct-envelope';}
  const next={...r,metadata:{...r.metadata,groundRole:'public-context',reservationReason:reason,sourcePlanningPolygon:original}};
  if(r.geometry)next.geometry={...r.geometry,polygon:selected};else next.polygon=selected;
  active.push(next);rows.push({id,originalArea:area(original),activeArea:area(selected),status:reason});
 }
 registration.reservations=active;registration.planningReservations=planning;registration.precinctReservationAudit={phase:registration.phase,rows,historicalLandUseVerified:false};return registration;
}
