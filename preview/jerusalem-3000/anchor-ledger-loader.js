import {appendWaterDefenseLedger} from './water-defense-registration.js';
import {appendPeriodSpatialLedger} from './period-spatial-ledger.js';
import {loadCityData} from './city-data-loader.js';
import {compileRoyalSpatialLayout} from './royal-spatial-layout.js';
// Spatial records are a derived projection, not a second editable ledger.
export async function loadAnchorCityLedger(){
 const [packs,lifecycle]=await Promise.all([loadCityData('./data/anchor-era-packs.json'),loadCityData('./data/lifecycle/anchor-era.lifecycle.json')]);
 if(!Array.isArray(packs.packs)||!Array.isArray(lifecycle.objects))throw new Error('Invalid shared anchor ledger');
 const lifecycleIds=new Set(lifecycle.objects.map(o=>o.id));if(lifecycleIds.size!==lifecycle.objects.length)throw new Error('Duplicate shared lifecycle ID');
 // Resolve declared source bundles once for BOTH temporal integration and core.
 for(const pack of packs.packs){
  if(pack.objectPack){
   const external=await loadCityData(`./data/${String(pack.objectPack).replace(/^\.\//,'')}`),objects=external.objects||external.features;
   if(!Array.isArray(objects))throw new Error(`Invalid object pack ${pack.objectPack}`);
   pack.objects=[...(pack.objects||[]),...objects.map(o=>o.properties?{...o.properties,...o,id:o.id||o.properties.id}:o)];
  }
  const ids=new Set();for(const object of pack.objects||[]){if(typeof object.id!=='string'||!object.id||ids.has(object.id))throw new Error(`Invalid/duplicate object ID in ${pack.phase}`);ids.add(object.id);}
  if(pack.lifecyclePack){
   const external=await loadCityData(`./data/${String(pack.lifecyclePack).replace(/^\.\//,'')}`);
   if(!Array.isArray(external.objects))throw new Error(`Invalid lifecycle pack ${pack.lifecyclePack}`);
   for(const object of external.objects){
    if(!ids.has(object.id)||lifecycleIds.has(object.id)||!Array.isArray(object.lifecycleEvents))throw new Error(`Invalid/duplicate declared lifecycle ${object.id}`);
    lifecycle.objects.push(object);lifecycleIds.add(object.id);
   }
  }
 }

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
 for(const path of new Set(packs.packs.map(p=>p.waterDefenseObjectPack).filter(Boolean)))appendWaterDefenseLedger(packs,lifecycle,await loadCityData(path));
 return {packs,lifecycle};
}
