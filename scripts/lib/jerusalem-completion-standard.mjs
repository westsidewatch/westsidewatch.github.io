import assert from 'node:assert/strict';
// Read the existing plan and captures. This is neither a second lifecycle ledger
// nor a way to promote render tests into historical acceptance.
export function completionStandardSummary({plan,timeline,qualityReports=null}){
 const ids=timeline.phases.map(p=>p.id),standard=plan.completionStandard;
 assert.equal(standard?.version,1);assert.deepEqual(standard.gates.map(g=>g.id),['spatial-relations','adjacent-changes','shared-generation']);
 assert.deepEqual(plan.phases.map(p=>p.id),ids);assert.equal(ids.length,18);assert.equal(plan.transitions.length,17);
 for(const g of standard.gates){assert.ok(g.criteria.length>=3);assert.ok(g.requiredEvidence.length>=2);}
 const unreviewedPhases=plan.phases.filter(p=>plan.domains.some(d=>p.domains[d]!=='accepted')||!p.acceptanceEvidence.length).map(p=>p.id);
 const unreviewedTransitions=plan.transitions.filter((t,i)=>{assert.equal(t.from,ids[i]);assert.equal(t.to,ids[i+1]);return t.status!=='accepted'||!t.acceptanceEvidence.length;}).map(t=>`${t.from}->${t.to}`);
 let selectedChecks=null;
 if(qualityReports){
  const {overview,enclosure,transition}=qualityReports;assert.ok(overview&&enclosure&&transition,'all three quality captures are required');
  for(const r of [overview,enclosure,transition]){assert.deepEqual(r.errors,[]);assert.equal(r.rows.length,18);}
  assert.deepEqual(overview.rows.map(r=>r.baseline.phase),ids);assert.deepEqual(enclosure.rows.map(r=>r.enclosure.phase),ids);
  const surface=overview.rows[0].terrain.surfaceId;assert.ok(surface);
  const phases=overview.rows.map((r,i)=>{const b=r.baseline,e=enclosure.rows[i].enclosure;
   assert.ok(b.meshes>0&&b.visualModules>0);assert.ok(Number.isFinite(b.maxVisualModuleSpanMetres)&&b.maxVisualModuleSpanMetres>0&&b.maxVisualModuleSpanMetres<=32.0001);
   assert.ok(Number.isFinite(b.projectedRoofAreaSquareMetres)&&b.projectedRoofAreaSquareMetres>0);assert.ok(Number.isFinite(b.omittedSliverAreaSquareMetres)&&b.omittedSliverAreaSquareMetres>=0);assert.ok(b.omittedSliverAreaSquareMetres/b.projectedRoofAreaSquareMetres<.01);
   assert.equal(r.terrain.surfaceId,surface);assert.equal(r.terrain.occupation.terrainPositionsChanged,false);assert.deepEqual(e.violations,[]);assert.ok(Number.isInteger(e.unresolved)&&e.unresolved>=0);
   return {id:ids[i],maxRoofModuleSpanMetres:b.maxVisualModuleSpanMetres,omittedSliverAreaSquareMetres:b.omittedSliverAreaSquareMetres,roofAreaSquareMetres:b.projectedRoofAreaSquareMetres,enclosureUnresolved:e.unresolved};
  });
  transition.rows.forEach((r,i)=>{assert.equal(r.index,i);assert.equal(r.full.presentation.phase,ids[i]);});
  const transitions=transition.rows.slice(1).map((r,i)=>{assert.equal(r.index,i+1);assert.equal(r.full.presentation.phase,ids[i+1]);assert.equal(r.full.presentation.waiting,0);assert.equal(r.full.presentation.growing,0);assert.equal(r.early.dissolve.visible,true);assert.equal(r.full.dissolve.visible,false);assert.equal(r.full.presentation.historicalSurvivalInferred,false);return {from:ids[i],to:ids[i+1],selectedPlaybackChecksPassed:true,physicalSurvivalVerified:false};});
  selectedChecks={status:'selected-captures-pass-not-whole-city-certification',phases,transitions,historicalAcceptanceInferred:false};
 }
 const gates=standard.gates.map(g=>{const pendingIds=g.id==='spatial-relations'?unreviewedPhases:g.id==='adjacent-changes'?unreviewedTransitions:[];
  const review=g.id==='shared-generation'?standard.sharedGenerationReview:null;
  const accepted=g.id==='shared-generation'?Boolean(selectedChecks&&review?.status==='accepted'&&review.evidence?.length):pendingIds.length===0;
  return {...structuredClone(g),accepted,reviewStatus:accepted?'reviewed-accepted':g.id==='shared-generation'?(selectedChecks?'selected-engineering-checks-pass-review-pending':'capture-evidence-missing'):g.id==='spatial-relations'?'phase-source-review-pending':'adjacent-source-review-pending',pendingIds,selectedEngineeringChecks:g.id==='shared-generation'?selectedChecks:null};});
 return {version:1,gates,foundationAccepted:gates.every(g=>g.accepted),policy:'Only explicit reviewed evidence can close a gate; counts, same IDs, same buffers and smooth animation cannot establish historical survival.'};
}
