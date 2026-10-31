import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const root=new URL('../preview/jerusalem-3000/',import.meta.url);
const read=path=>JSON.parse(readFileSync(new URL(path,root)));
const timeline=read('data/continuous-build-timeline.json');
const plan=read('data/city-foundation-plan.v1.json');
export function auditFoundationPlan(plan,timeline){
 const domains=['districts','routes','waterDefense','sacredCivic','occupation','lifecycle'];
 const statuses=new Set(['partial','scaffold','unresolved','accepted']);
 assert.deepEqual(plan.domains,domains,'same city domains in every phase');
 assert.deepEqual(plan.phases.map(p=>p.id),timeline.phases.map(p=>p.id),'cover every phase once in canonical order');
 assert.equal(plan.transitions.length,timeline.phases.length-1,'cover every adjacent transition');
 for(const phase of plan.phases){
  assert.deepEqual(Object.keys(phase.domains),domains);
  assert.ok(phase.rendererFamily&&phase.gap&&Array.isArray(phase.acceptanceEvidence));
  for(const status of Object.values(phase.domains))assert.ok(statuses.has(status));
  if(Object.values(phase.domains).includes('accepted'))assert.ok(phase.acceptanceEvidence.length,'accepted foundation needs review evidence');
 }
 plan.transitions.forEach((t,i)=>{
  assert.equal(t.from,timeline.phases[i].id);assert.equal(t.to,timeline.phases[i+1].id);
  assert.ok(statuses.has(t.status)&&t.policy&&Array.isArray(t.acceptanceEvidence));
  if(t.status==='accepted')assert.ok(t.acceptanceEvidence.length,'accepted transition needs review evidence');
 });
 const phaseGaps=plan.phases.filter(p=>Object.values(p.domains).some(s=>s!=='accepted')).map(p=>p.id);
 const transitionGaps=plan.transitions.filter(t=>t.status!=='accepted').map(t=>`${t.from}->${t.to}`);
 return {inventoryValid:true,foundationAccepted:!phaseGaps.length&&!transitionGaps.length,phaseGaps,transitionGaps};
}
assert.deepEqual(plan.completionStandard.gates.map(g=>g.id),['spatial-relations','adjacent-changes','shared-generation']);
for(const g of plan.completionStandard.gates){assert.ok(g.criteria.length>=3&&g.requiredEvidence.length>=2);}
const report=auditFoundationPlan(plan,timeline);
assert.equal(report.foundationAccepted,false,'inventory validation must not certify unfinished foundation');
for(const mutation of [p=>p.phases.pop(),p=>p.transitions.reverse(),p=>delete p.phases[0].domains.routes,p=>p.phases[0].domains.routes='accepted']){
 const broken=structuredClone(plan);mutation(broken);assert.throws(()=>auditFoundationPlan(broken,timeline));
}
console.log(JSON.stringify(report));
console.log('PASS: complete 18-phase/17-transition inventory; foundation remains unaccepted, detail work paused');
