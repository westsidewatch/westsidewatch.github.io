import {sourceSpatialTopology} from './source-spatial-topology.js';
import {loadAnchorCityLedger} from './anchor-ledger-loader.js';
import {createTemporalCityCore,EVIDENCE_CONFIDENCE,CITY_OBJECT_TYPES} from './temporal-city-core.js';

const TYPE_MAP={
 'platform-enclosure':CITY_OBJECT_TYPES.MONUMENT,
 'portico-basilica':CITY_OBJECT_TYPES.MONUMENT,
 'fortress':CITY_OBJECT_TYPES.MONUMENT,
 'sacred-complex':CITY_OBJECT_TYPES.MONUMENT,
 'pilgrimage-access':CITY_OBJECT_TYPES.ROAD,
 'street':CITY_OBJECT_TYPES.ROAD,
 'uncertain-access':CITY_OBJECT_TYPES.GATE,
 'urban-envelope':CITY_OBJECT_TYPES.DISTRICT,
 'urban-fabric':CITY_OBJECT_TYPES.DISTRICT,
 'fortification':CITY_OBJECT_TYPES.WALL,
 'water-fortification':CITY_OBJECT_TYPES.WATER,
 'monumental-zone':CITY_OBJECT_TYPES.MONUMENT,
 'sanctuary':CITY_OBJECT_TYPES.MONUMENT,
 'gate':CITY_OBJECT_TYPES.GATE,
 'transport-network':CITY_OBJECT_TYPES.ROAD
};
function evidenceConfidence(object){if(Object.values(EVIDENCE_CONFIDENCE).includes(object.confidence))return object.confidence;const e=String(object.evidence||'').toLowerCase(),c=String(object.confidence||'').toLowerCase();if(e.includes('disputed')||c.includes('disputed')||c.startsWith('low'))return EVIDENCE_CONFIDENCE.DISPUTED;if(e.includes('archaeological')||e==='observed'||c==='high'||c.startsWith('high-'))return EVIDENCE_CONFIDENCE.OBSERVED;if(e.includes('reconstructed')||e.includes('text')||e.includes('historical-mapping'))return EVIDENCE_CONFIDENCE.RECONSTRUCTED;return EVIDENCE_CONFIDENCE.INFERRED;}
function geometryDescriptor(object){const raw=object.geometry;if(raw&&typeof raw==='object')return raw;const value=String(raw||'withheld');return{status:value.includes('withheld')?'withheld':'declared',authority:value,primitive:null};}
function lifecycleFor(id,lifecycleMap,phaseId){const events=lifecycleMap.get(id)||[];let built=null,destroyed=null,ruined=false,reused=false;for(const event of events){if(['build','rebuild','settlement','expand','transform'].includes(event.state)&&!built)built=event.phase;if(['ruin','buried'].includes(event.state)){destroyed=event.phase;ruined=true}if(event.reuseVerified===true)reused=true}return{built,destroyed,ruined,reused,events};}
export async function loadTemporalCityCore(phases,{terrain=null}={}){
 const {packs,lifecycle}=await loadAnchorCityLedger();
 const core=createTemporalCityCore({phases,terrain});
 const lifecycleMap=new Map((lifecycle.objects||[]).map(item=>[item.id,item.lifecycleEvents||[]]));
 for(const pack of packs.packs||[]){
  const objects=pack.objects||[];
  for(const object of objects){
   const id=object.id||object.properties?.id;if(!id)continue;const source=object.properties?{...object.properties,...object}:object;
   const topology=String(pack.objectPack).replace(/^\.\//,'')==='objects/herodian-30ce.json'?sourceSpatialTopology(source,terrain):null;
   core.register({id,type:TYPE_MAP[source.kind]||CITY_OBJECT_TYPES.BUILDING,phaseIds:[...new Set([pack.phase,...(lifecycleMap.get(id)||[]).map(event=>event.phase)])],geometry:geometryDescriptor(source),typology:source.kind||null,source:{evidence:source.evidence||null,label:source.label||null,anchorPack:pack.phase,urls:source.sources||[],limitations:source.limitations||[]},confidence:evidenceConfidence(source),lifecycle:lifecycleFor(id,lifecycleMap,pack.phase),metadata:{...(topology?{spatialTopology:topology}:{}),label:source.label||id,legacyConfidence:source.confidence||null,adapter:'anchor-era-packs-v1',lifecyclePack:pack.lifecyclePack||null,relatedObjects:source.relatedObjects||[],rendererBinding:source.rendererBinding||null,lifecycleTemplate:source.lifecycleTemplate||null}});
  }
 }
 const validation=core.validate();
 return{core,validation,summary:Object.fromEntries(phases.map(phase=>[phase.id,core.summary(phase.id)]))};
}
