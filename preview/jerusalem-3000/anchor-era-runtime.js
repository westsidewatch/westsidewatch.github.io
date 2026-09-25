import {lifecycleStateAt} from './construction-engine.js';

const PACKS_URL='./data/anchor-era-packs.json';
const LIFE_URL='./data/lifecycle/anchor-era.lifecycle.json';

function syntheticPlacement(index,total,phaseIndex){
  // Publication-only placement for objects whose sourced ENU geometry is still withheld.
  // Never exported back into historical/geographic authority.
  const band=(phaseIndex%5)+1;
  return {left:10+((index*17+band*9)%76),top:22+((index*13+band*7)%48)};
}

export async function loadAnchorEraObjects(timeline,layer){
  const [packs,life]=await Promise.all([
    fetch(PACKS_URL).then(r=>{if(!r.ok)throw new Error('anchor era packs unavailable');return r.json()}),
    fetch(LIFE_URL).then(r=>{if(!r.ok)throw new Error('anchor lifecycle unavailable');return r.json()})
  ]);
  const lifeById=new Map(life.objects.map(o=>[o.id,o.lifecycleEvents]));
  const phaseIndex=new Map(timeline.phases.map((p,i)=>[p.id,i]));
  const objects=[];
  for(const pack of packs.packs){
    if(!pack.objects) continue; // Herodian pack is rendered by its evidence-backed geographic ledger.
    pack.objects.forEach((object,index)=>{
      const el=document.createElement('div');
      el.className='j3k-historical-object j3k-anchor-object';
      el.dataset.objectId=object.id;el.dataset.evidence=object.evidence;el.dataset.anchorEra=pack.phase;
      el.dataset.registration='publication-only';el.title=`${object.label} · ${object.confidence}`;
      const pos=syntheticPlacement(index,pack.objects.length,phaseIndex.get(pack.phase)||0);
      el.style.left=pos.left+'%';el.style.top=pos.top+'%';layer.append(el);
      objects.push({...object,anchorEra:pack.phase,lifecycleEvents:lifeById.get(object.id)||[],el});
    });
  }
  return objects;
}

export function updateAnchorEraObjects(objects,timeline,phaseId){
  const opacity={absent:'0',settlement:'.55',build:'1',expand:'1',transform:'.72',ruin:'.42',buried:'.12',rebuild:'.88'};
  for(const object of objects){
    const state=lifecycleStateAt(object,timeline,phaseId);
    object.el.dataset.lifecycle=state;
    object.el.style.setProperty('--life-opacity',opacity[state]||'0');
    object.el.hidden=state==='absent';
  }
}
