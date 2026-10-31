import {geographicToENU} from './terrain-runtime.js';
import {lifecycleStateAtPosition} from './construction-engine.js';
import {allowsEvidence} from './evidence-visibility.js';
const ORIGIN={lat:31.778,lon:35.235};
const IAA='https://publications.iaa.org.il/ha-esi/vol138/iss1/57/';
const SPRING={lat:31.773235,lon:35.2368303};
export const EASTERN_CORRIDOR_ID='j3k:place:eastern-cardo-corridor';
const CORRIDOR_PHASES=new Set(['aelia','byzantine','early-islamic','crusader','ayyubid-mamluk','ottoman','outside-walls','modern']);
const ROAD_IDS=new Map([...CORRIDOR_PHASES].map(phase=>[phase,['aelia','byzantine'].includes(phase)?'eastern-cardo-context':phase==='early-islamic'?'eastern-street-context':'eastern-valley-link-illustrative']));
// Existing Aelia design line becomes ONE corridor reference, not a measured road.
const CORRIDOR=[[-340,-610],[-300,-350],[-270,-100],[-240,200],[-220,380]];
export function commonCorridorFor(phase,id){
 if(!CORRIDOR_PHASES.has(phase)||ROAD_IDS.get(phase)!==id)return null;
 return {placeId:EASTERN_CORRIDOR_ID,points:CORRIDOR.map(([x,z])=>({x,z})),source:IAA,relation:'shared-route-corridor-not-surviving-pavement',modernScope:phase==='modern'?'historical-axis-context-not-complete-present-street':null};
}
export function sharedPlaceForObject(record){
 if(record.metadata?.placeId)return record.metadata.placeId;
 if(['j3k:object:first-temple','j3k:object:second-temple-early','j3k:object:temple-mount-enclosure-herodian','j3k:object:royal-stoa','j3k:object:antonia'].includes(record.id))return 'j3k:place:northern-sacred-hill';
 if(record.id==='j3k:object:gihon-spring')return 'j3k:place:gihon';
 return null;
}
export function createSharedUrbanPlaces({terrain,phases,core}){
 if(terrain?.grid?.origin?.lat!==ORIGIN.lat||terrain?.grid?.origin?.lon!==ORIGIN.lon||core.terrain!==terrain||!Array.isArray(phases)||phases.length!==18||phases.some((p,i)=>[...core.phases.keys()][i]!==p.id))throw new Error('Shared places require canonical terrain and complete ordered timeline');
 const spring=geographicToENU(SPRING.lat,SPRING.lon,ORIGIN);
 const definitions=[
  {id:'j3k:place:northern-sacred-hill',label:'北部高地／聖殿山區域',x:0,z:0,authority:'existing-platform-scale-context-not-exact-ancient-temple-location',source:'data/objects/herodian-30ce.json'},
  {id:'j3k:place:southeast-ridge',label:'大衛城／東南山脊',description:'大衛城所在的東南山脊；《撒母耳記下》5:7 的早期錫安。今天名為錫安山的西南丘是另一處；此標記不是古城界或宮殿定位。',historicalContextSource:'https://cityofdavid.org.il/wp-content/uploads/2023/03/Traveler_COD_Eng_2022_lowrez.pdf',x:spring.east-98,z:-spring.north+145,authority:'existing-illustrative-ridge-south-context',source:'data/settlement/david-solomon.v1.json'},
  {id:'j3k:place:gihon',label:'基訓泉附近',x:spring.east,z:-spring.north,authority:'approximate-modern-map-location-not-ancient-access',source:'https://api.openstreetmap.org/api/0.6/node/1608094098',attribution:'OpenStreetMap contributors, ODbL'}
 ];
 const anchors=definitions.map(p=>{const y=terrain.heightAtWorld(p.x,p.z);if(!Number.isFinite(y))throw new Error('Shared place outside terrain');return {...p,y,confidence:'inferred',geometryVerified:false,semanticCityObject:false};});
 const placeIds=new Set([...anchors.map(p=>p.id),EASTERN_CORRIDOR_ID,'j3k:place:holy-sepulchre-site','j3k:place:southern-haram','j3k:place:nea-site','j3k:place:roman-north-entry']);
 const timeline={phases},active=new Set(['build','rebuild','transform','expand','ruin']);
 function representations(phaseId,position,evidenceMode){
  return core.phase(phaseId).flatMap(record=>{
   const placeId=sharedPlaceForObject(record);if(!placeId||!placeIds.has(placeId)||!allowsEvidence(evidenceMode,record.confidence))return [];
   const state=record.lifecycle.events.length?lifecycleStateAtPosition({lifecycleEvents:record.lifecycle.events},timeline,position):'unresolved';
   return active.has(state)?[{placeId,objectId:record.id,type:record.type,state,physicalSurvivalVerified:false}]:[];
  });
 }
 const transitions=phases.slice(1).map((p,i)=>({from:phases[i].id,to:p.id,sharedGeographicPlaces:anchors.map(a=>a.id),corridorContextShared:CORRIDOR_PHASES.has(phases[i].id)&&CORRIDOR_PHASES.has(p.id),corridorSource:CORRIDOR_PHASES.has(phases[i].id)&&CORRIDOR_PHASES.has(p.id)?IAA:null,placeContinuity:'same-geographic-reference',physicalFabricContinuity:'unresolved',reuseLinksVerified:false}));
 return {
  anchors:()=>structuredClone(anchors),transitions:()=>structuredClone(transitions),
  snapshot({phaseId,position,evidenceMode='all'}){
   const index=phases.findIndex(p=>p.id===phaseId);if(index<0||Math.floor(position)!==index)throw new Error('Shared place phase mismatch');allowsEvidence(evidenceMode,'inferred');
   return {phaseId,anchors:allowsEvidence(evidenceMode,'inferred')?structuredClone(anchors):[],representations:representations(phaseId,position,evidenceMode),previousTransition:index?structuredClone(transitions[index-1]):null,samePlaceIsSameBuilding:false,historicalContinuityAccepted:false};
  }
 };
}
