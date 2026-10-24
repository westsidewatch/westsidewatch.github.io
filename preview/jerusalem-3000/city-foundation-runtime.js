import {cityObjectIdForMesh} from './city-lifecycle-projection.js';
import {lifecycleStateAtPosition} from './construction-engine.js';
const OWNERS=Object.freeze({
 'chalcolithic-early-bronze':'early-landscape','middle-bronze':'early-landscape','late-bronze-iron1':'early-landscape','david-solomon':'early-landscape',
 'late-first-temple':'shared-period','babylonian-destruction':'shared-period','persian-nehemiah':'shared-period','hellenistic-hasmonean':'shared-period',
 'herodian-jesus':'canonical-city','roman-destruction':'canonical-city',
 aelia:'legacy-footprint',byzantine:'legacy-footprint','early-islamic':'legacy-footprint',crusader:'crusader-morphology','ayyubid-mamluk':'legacy-footprint',ottoman:'ottoman-morphology','outside-walls':'legacy-footprint',modern:'legacy-footprint'
});
export function foundationOwnerFor(phaseId){const owner=OWNERS[phaseId];if(!owner)throw new Error(`Unknown foundation phase ${phaseId}`);return owner;}
const DOMAIN_TYPES={districts:['district'],routes:['road','route'],waterDefense:['water','wall','gate'],sacredCivic:['monument'],occupation:['block','parcel','building']};
function effectiveVisible(object){for(let current=object;current;current=current.parent)if(current.visible===false)return false;return true;}
function inheritedComponent(object){for(let current=object;current;current=current.parent)if(current.name==='phase2-inherited-city')return true;return false;}
// A common observation interface, not another model or a generated lineage ledger.
// Inactive inspection never invokes a generator. Counts do not certify completeness.
export function createCityFoundationRuntime({core,terrain,root,getCurrentPhase,getPosition}){
 if(!core||!terrain?.mesh||!terrain?.grid||core.terrain!==terrain)throw new Error('Foundation requires the shared core and canonical DEM instance');
 const phases=[...core.phases.values()],ids=phases.map(p=>p.id);
 if(new Set(ids).size!==ids.length||ids.length!==Object.keys(OWNERS).length||ids.some((id,i)=>id!==Object.keys(OWNERS)[i]))throw new Error('Foundation phase coverage mismatch');
 ids.forEach(foundationOwnerFor);
 const terrainBasis=()=>({frame:'canonical-dem-enu',sampling:'rendered-dem-triangles',verticalScale:1,modernSurface:true,ancientGroundVerified:false});
 function describe(phaseId){const index=ids.indexOf(phaseId);if(index<0)throw new Error(`Unknown foundation phase ${phaseId}`);return {phaseId,owner:foundationOwnerFor(phaseId),previous:ids[index-1]??null,next:ids[index+1]??null,terrain:terrainBasis(),foundationAccepted:false};}
 function snapshot(phaseId=getCurrentPhase()){
  const entry=describe(phaseId),active=phaseId===getCurrentPhase(),records=core.phase(phaseId),position=active?getPosition():ids.indexOf(phaseId)+.999;
  const byId=new Map(records.map(r=>[r.id,r])),bound=new Set(),visibleBound=new Set(),outOfPhase=new Set();
  let components=0,boundComponents=0,unbound=0,inherited=0,tracedInherited=0;
  if(active)root.traverse(mesh=>{
   if(!mesh.isMesh||!effectiveVisible(mesh))return;
   const meta=mesh.userData?.cityObject;
   if(!meta&&!mesh.userData?.phase2&&!mesh.userData?.evidenceObject&&!mesh.userData?.foundation)return;
   components++;
   const provisional=inheritedComponent(mesh);if(provisional){inherited++;if(mesh.userData.provisionalInheritance?.survivalVerified===false)tracedInherited++;}
   const id=cityObjectIdForMesh(mesh),record=id&&core.get(id);
   if(!record||provisional){unbound++;return;}
   boundComponents++;bound.add(record.id);if(byId.has(record.id))visibleBound.add(record.id);else outOfPhase.add(record.id);
  });
  const domains={};
  for(const [domain,types]of Object.entries(DOMAIN_TYPES)){
   const objects=records.filter(r=>types.includes(r.type));
   domains[domain]={registeredObjects:objects.length,visibleBoundObjects:objects.filter(r=>visibleBound.has(r.id)).length,scope:'registered-objects-only-not-complete-city'};
  }
  const states={},withEvents=records.filter(r=>r.lifecycle.events.length);
  for(const record of withEvents){const state=lifecycleStateAtPosition({lifecycleEvents:record.lifecycle.events},{phases},position);states[state]=(states[state]||0)+1;}
  domains.lifecycle={registeredObjects:withEvents.length,withoutDeclaredEvents:records.length-withEvents.length,states,scope:'existing-events-only-no-new-reuse-links'};
  return {...entry,active,position,ledgerObjects:records.length,domains,
   renderer:{status:active?'active':'not-inspected-inactive',visibleComponents:active?components:null,visibleBoundObjects:active?bound.size:null,boundComponents:active?boundComponents:null,unboundComponents:active?unbound:null,provisionalInheritedComponents:active?inherited:null,provisionalTraceableComponents:active?tracedInherited:null,outOfPhaseBindingIds:active?[...outOfPhase].sort():[]},
   gapPolicy:'Visible unbound components and provisional retention are not certified city objects. Zero counts do not prove historical absence.'};
 }
 return {describe,snapshot,index:()=>ids.map(describe)};
}
