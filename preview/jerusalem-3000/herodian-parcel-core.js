import {housingFitsRing} from './housing-boundary.js';
import {metricParcelsForBlock} from './metric-residential-layout.js';
import {generateDistrictInfill,roadClearancePolygons} from './district-infill.js';
import {loadCityData} from './city-data-loader.js';
import {polygonsOverlap} from './urban-exclusion.js';
import {generateUrbanBlocks,subdivideBlockToParcels} from './herodian-urban-blocks-core.js';
import {CITY_OBJECT_TYPES,EVIDENCE_CONFIDENCE} from './temporal-city-core.js';
const load=()=>loadCityData('./data/urban/herodian-30ce.registration.json');
function collisionIndex(){const bins=new Map(),keys=p=>{const xs=p.map(v=>v.x),zs=p.map(v=>v.z),out=[];for(let x=Math.floor(Math.min(...xs)/40);x<=Math.floor(Math.max(...xs)/40);x++)for(let z=Math.floor(Math.min(...zs)/40);z<=Math.floor(Math.max(...zs)/40);z++)out.push(`${x},${z}`);return out;};return{add(p){for(const k of keys(p)){if(!bins.has(k))bins.set(k,[]);bins.get(k).push(p);}},overlaps(p){return [...new Set(keys(p).flatMap(k=>bins.get(k)||[]))].some(q=>polygonsOverlap(p,q));}};}
export function buildEraParcelCore(core,terrain,{phaseId,registration,districtId,exclusions=[],dataset='era-registration'}={}){
 if(!phaseId||!registration||!districtId)throw new Error('Era parcel core requires phaseId, registration and districtId');
 const data=registration,district=data.districts.find(d=>d.id===districtId);if(!district)return{parcels:[],blocks:[],withheld:true,reason:'lower-city-district-missing'};
 const generation=data.generation||{},infill=generation.infillMode==='district-constrained',metric=data.metricResidentialPolicy;
 const blockResult=infill?generateDistrictInfill({district,roads:data.roads,maxBlockArea:generation.maxBlockArea,roadClearance:generation.roadClearance}):generateUrbanBlocks({district,roads:data.roads,terrain,blockSize:generation.blockSize||96,roadClearance:generation.roadClearance||18});
 // Retain the existing street-front/block-edge parcels unchanged. Complete the
 // residual residential zone with separately identified, fixed-metre parcels.
 const additional=metric?generateDistrictInfill({district,roads:data.roads,maxBlockArea:12000,roadClearance:generation.roadClearance||6}).blocks.map(b=>({...b,id:`${b.id}:metric-infill`,metadata:{...b.metadata,metricInfill:true}})):[];
 const blocks=[...blockResult.blocks,...additional],reserved=infill?[...exclusions,...roadClearancePolygons(data.roads,generation.roadClearance)]:exclusions,metricReserved=[...exclusions,...roadClearancePolygons(data.roads,generation.roadClearance||6)],parcels=[],collisions=collisionIndex();
 for(const block of blocks){
  core.register({id:`${phaseId}:${block.id}`,type:CITY_OBJECT_TYPES.BLOCK,phaseIds:[phaseId],geometry:block.geometry,typology:'urban-block',source:{dataset,districtId:block.districtId,authority:infill?data.authority:'migration-scaffold'},confidence:EVIDENCE_CONFIDENCE.INFERRED,lifecycle:{built:phaseId},metadata:{...block.metadata,semanticRole:'block'}});
  const added=block.metadata.metricInfill,candidates=added?metricParcelsForBlock(block,terrain,metric):subdivideBlockToParcels(block,{terrain});
  for(const parcel of candidates){
   if(added&&data.metricHousingRings?.length&&!data.metricHousingRings.some(r=>housingFitsRing(parcel.geometry.polygon,r,2)))continue;
   if((added?metricReserved:reserved).some(zone=>polygonsOverlap(parcel.geometry.polygon,zone.polygon)))continue;
   if((infill||added)&&collisions.overlaps(parcel.geometry.polygon))continue;
   if(infill&&!added)parcel.orientation={...parcel.orientation,source:'inferred-district-block-edge'};
   parcels.push({...parcel,id:`${phaseId}:${parcel.id}`});collisions.add(parcel.geometry.polygon);
   core.register({id:`${phaseId}:${parcel.id}`,type:CITY_OBJECT_TYPES.PARCEL,phaseIds:[phaseId],geometry:parcel.geometry,typology:'urban-parcel',source:{dataset,districtId:parcel.districtId,blockId:parcel.blockId,authority:infill?data.authority:'migration-scaffold'},confidence:EVIDENCE_CONFIDENCE.INFERRED,lifecycle:{built:phaseId},metadata:{...parcel.metadata,orientation:parcel.orientation,typologyPool:parcel.typologyPool,architectureProfile:generation.architectureProfile||null}});
  }
 }
 return{parcels,roads:data.roads,exclusions,blocks,count:parcels.length,blockCount:blocks.length,withheld:blockResult.withheld,policy:'district→roads→terrain→blocks→parcels',generationScope:generation.scope||'unspecified',registrationAuthority:data.authority,validation:core.validate()};
}
export async function buildHerodianParcelCore(core,terrain,{exclusions=[],registration=null}={}){registration=registration||await load();return buildEraParcelCore(core,terrain,{phaseId:'herodian-jesus',registration,districtId:'j3k:district:western-lower-city',exclusions,dataset:'herodian-30ce.registration'});}
