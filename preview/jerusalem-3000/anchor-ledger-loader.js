import {appendPeriodSpatialLedger} from './period-spatial-ledger.js';
import {loadCityData} from './city-data-loader.js';
import {compileRoyalSpatialLayout} from './royal-spatial-layout.js';
// Spatial records are a derived projection, not a second editable ledger.
export async function loadAnchorCityLedger(){
 const [packs,lifecycle]=await Promise.all([loadCityData('./data/anchor-era-packs.json'),loadCityData('./data/lifecycle/anchor-era.lifecycle.json')]);
 if(!Array.isArray(packs.packs)||!Array.isArray(lifecycle.objects))throw new Error('Invalid shared anchor ledger');
 for(const pack of packs.packs||[]){
  if(!pack.spatialObjectPack)continue;
  pack.objects ||= [];
  const data=await loadCityData(pack.spatialObjectPack),layout=compileRoyalSpatialLayout(data);
  for(const [kind,items,type] of [['gate',layout.gates,'gate'],['road',layout.edges,'transport-network'],['region',layout.regions,'urban-envelope']])for(const item of items){
   const id=`j3k:object:royal-${kind}:${item.id}`,templateId=data.royalCity.spatial.lifecycleTemplates[item.stage],template=lifecycle.objects.find(o=>o.id===templateId);
   if(!template)throw new Error(`Missing spatial lifecycle template ${templateId}`);
   if((pack.objects||[]).some(o=>o.id===id)||lifecycle.objects.some(o=>o.id===id))throw new Error(`Duplicate derived spatial object ${id}`);
   pack.objects.push({id,label:item.label||`${item.id}（連接示意）`,kind:type,confidence:'inferred',evidence:'inferred',geometry:'withheld-pending-shared-spatial-adapter',rendererBinding:'ledger-only-pending-adapter',sources:data.royalCity.spatial.sources,limitations:['Illustrative spatial connectivity/envelope, not surveyed location or verified later survival.'],lifecycleTemplate:templateId});
   lifecycle.objects.push({id,lifecycleEvents:template.lifecycleEvents.map(event=>({...event,authority:'inferred-display-follows-spatial-template',templateId}))});
  }
 }
 for(const path of new Set(packs.packs.map(p=>p.periodSpatialObjectPack).filter(Boolean)))appendPeriodSpatialLedger(packs,lifecycle,await loadCityData(path));
 return {packs,lifecycle};
}
