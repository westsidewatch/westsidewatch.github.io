const ACTIVE_STATES=new Set(['build','rebuild','settlement','expand','transform']);
const RUIN_STATES=new Set(['ruin','buried']);

export class TemporalCityIntegration{
  constructor(phases=[],anchorPacks={packs:[]},lifecycle={objects:[]}){
    this.phases=phases;
    this.phaseIndex=new Map(phases.map((phase,index)=>[phase.id,index]));
    this.objects=new Map();
    for(const pack of anchorPacks.packs||[]){
      for(const object of pack.objects||[])this.objects.set(object.id,{...object,anchorPhase:pack.phase,anchorLabel:pack.label});
    }
    this.lifecycle=new Map((lifecycle.objects||[]).map(item=>[item.id,item.lifecycleEvents||[]]));
  }
  stateFor(id,position){
    const events=this.lifecycle.get(id)||[];
    let state='withheld',eventPhase=null;
    for(const event of events){
      const index=this.phaseIndex.get(event.phase);
      if(index===undefined||index>position)break;
      state=event.state;eventPhase=event.phase;
    }
    return{state,eventPhase,visible:ACTIVE_STATES.has(state),ruined:RUIN_STATES.has(state)};
  }
  sample(position){
    const objects=[];
    for(const object of this.objects.values())objects.push({...object,...this.stateFor(object.id,position)});
    return objects;
  }
  summary(position){
    const sampled=this.sample(position);
    return sampled.reduce((out,item)=>{out[item.state]=(out[item.state]||0)+1;return out},{total:sampled.length});
  }
}

export async function loadTemporalCityIntegration(phases){
  const [packsResponse,lifecycleResponse]=await Promise.all([
    fetch('./data/anchor-era-packs.json',{cache:'no-store'}),
    fetch('./data/lifecycle/anchor-era.lifecycle.json',{cache:'no-store'})
  ]);
  if(!packsResponse.ok)throw new Error(`anchor era packs unavailable (${packsResponse.status})`);
  if(!lifecycleResponse.ok)throw new Error(`anchor lifecycle unavailable (${lifecycleResponse.status})`);
  const [packs,lifecycle]=await Promise.all([packsResponse.json(),lifecycleResponse.json()]);
  return new TemporalCityIntegration(phases,packs,lifecycle);
}
