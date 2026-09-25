export const CONSTRUCTION_STATES=new Set(['settlement','build','expand','transform','ruin','buried','rebuild']);

export function phaseIndex(timeline,phaseId){
  const i=timeline.phases.findIndex(p=>p.id===phaseId);
  if(i<0) throw new Error(`unknown Jerusalem phase: ${phaseId}`);
  return i;
}

export function lifecycleStateAt(object,timeline,phaseId){
  const now=phaseIndex(timeline,phaseId);
  const events=(object.lifecycleEvents||[]).slice().sort((a,b)=>phaseIndex(timeline,a.phase)-phaseIndex(timeline,b.phase));
  let state='absent';
  for(const event of events){
    if(phaseIndex(timeline,event.phase)>now) break;
    if(!CONSTRUCTION_STATES.has(event.state)) throw new Error(`invalid construction state: ${event.state}`);
    state=event.state;
  }
  return state;
}

export function materializeCityState(objects,timeline,phaseId){
  return objects.map(object=>({...object,runtimeLifecycle:lifecycleStateAt(object,timeline,phaseId)}));
}

export function transitionClass(fromState,toState){
  if(fromState===toState) return 'hold';
  if(toState==='ruin') return 'collapse';
  if(toState==='buried') return 'submerge';
  if(toState==='rebuild') return 're-emerge';
  if(toState==='build'||toState==='settlement') return 'emerge';
  if(toState==='expand') return 'grow';
  if(toState==='transform') return 'morph';
  if(toState==='absent') return 'withdraw';
  return 'change';
}

export function cityTransition(objects,timeline,fromPhase,toPhase){
  const before=new Map(materializeCityState(objects,timeline,fromPhase).map(o=>[o.id,o.runtimeLifecycle]));
  return materializeCityState(objects,timeline,toPhase).map(o=>({...o,transition:transitionClass(before.get(o.id)||'absent',o.runtimeLifecycle)}));
}
