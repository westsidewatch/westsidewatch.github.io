import {createTemporalCityCore,EVIDENCE_CONFIDENCE,CITY_OBJECT_TYPES} from './temporal-city-core.js';

const TYPE_MAP={
 'urban-envelope':CITY_OBJECT_TYPES.DISTRICT,
 'urban-fabric':CITY_OBJECT_TYPES.DISTRICT,
 'fortification':CITY_OBJECT_TYPES.WALL,
 'water-fortification':CITY_OBJECT_TYPES.WATER,
 'monumental-zone':CITY_OBJECT_TYPES.MONUMENT,
 'sanctuary':CITY_OBJECT_TYPES.MONUMENT,
 'gate':CITY_OBJECT_TYPES.GATE,
 'transport-network':CITY_OBJECT_TYPES.ROAD
};
function evidenceConfidence(object){const e=String(object.evidence||'').toLowerCase(),c=String(object.confidence||'').toLowerCase();if(e.includes('disputed')||c.includes('disputed')||c.startsWith('low'))return EVIDENCE_CONFIDENCE.DISPUTED;if(e.includes('archaeological')||e==='observed'||c==='high'||c.startsWith('high-'))return EVIDENCE_CONFIDENCE.OBSERVED;if(e.includes('reconstructed')||e.includes('text')||e.includes('historical-mapping'))return EVIDENCE_CONFIDENCE.RECONSTRUCTED;return EVIDENCE_CONFIDENCE.INFERRED;}
function geometryDescriptor(object){const raw=object.geometry;if(raw&&typeof raw==='object')return raw;const value=String(raw||'withheld');return{status:value.includes('withheld')?'withheld':'declared',authority:value,primitive:null};}
function lifecycleFor(id,lifecycleMap,phaseId){const events=lifecycleMap.get(id)||[];let built=phaseId,destroyed=null,ruined=false,reused=false;for(const event of events){if(['build','rebuild','settlement','expand','transform'].includes(event.state)&&!built)built=event.phase;if(['ruin','buried'].includes(event.state)){destroyed=event.phase;ruined=true}if(event.state==='rebuild'||event.state==='transform')reused=true}return{built,destroyed,ruined,reused,events};}
async function json(url){const response=await fetch(url,{cache:'no-store'});if(!response.ok)throw new Error(`${url} unavailable (${response.status})`);return response.json();}
export async function loadTemporalCityCore(phases,{terrain=null}={}){
 const [packs,lifecycle]=await Promise.all([json('./data/anchor-era-packs.json'),json('./data/lifecycle/anchor-era.lifecycle.json')]);
 const core=createTemporalCityCore({phases,terrain});
 const lifecycleMap=new Map((lifecycle.objects||[]).map(item=>[item.id,item.lifecycleEvents||[]]));
 for(const pack of packs.packs||[]){
  let objects=pack.objects||[];
  if(pack.objectPack){try{const external=await json(`./data/${String(pack.objectPack).replace(/^\.\//,'')}`);objects=external.objects||external.features||[]}catch(error){console.warn('[J3K core adapter] object pack withheld',pack.objectPack,error)}}
  for(const object of objects){
   const id=object.id||object.properties?.id;if(!id)continue;const source=object.properties?{...object.properties,...object}:object;
   core.register({id,type:TYPE_MAP[source.kind]||CITY_OBJECT_TYPES.BUILDING,phaseIds:[pack.phase],geometry:geometryDescriptor(source),typology:source.kind||null,source:{evidence:source.evidence||null,label:source.label||null,anchorPack:pack.phase},confidence:evidenceConfidence(source),lifecycle:lifecycleFor(id,lifecycleMap,pack.phase),metadata:{label:source.label||id,legacyConfidence:source.confidence||null,adapter:'anchor-era-packs-v1'}});
  }
 }
 const validation=core.validate();
 return{core,validation,summary:Object.fromEntries(phases.map(phase=>[phase.id,core.summary(phase.id)]))};
}
