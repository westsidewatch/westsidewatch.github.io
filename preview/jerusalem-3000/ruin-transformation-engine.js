export class RuinTransformationEngine{
  constructor(phases){this.phases=phases;this.roman=phases.findIndex(p=>p.id==='roman-destruction');if(this.roman<0)throw new Error('Roman destruction phase missing');}
  sample(position,destructionPhase='roman-destruction'){const boundary=this.phases.findIndex(phase=>phase.id===destructionPhase);if(boundary<0||this.phases[boundary].state!=='ruin')throw new Error(`Unknown destruction phase: ${destructionPhase}`);const p=Number(position)||0;const t=Math.max(0,Math.min(1,p-boundary));const eased=t*t*(3-2*t);return{position:p,destruction:eased,standing:1-eased,ruin:eased,phase:p<boundary?'pre-destruction':p<boundary+1?'transformation':'post-destruction'};}
  reversibleCheck(samples=512){for(let i=0;i<=samples;i++){const p=this.roman+i/samples,a=this.sample(p),b=this.sample(p);if(a.destruction!==b.destruction||Math.abs(a.standing+a.ruin-1)>1e-9)return false;}return true;}
}
