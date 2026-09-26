const STATE_CURVE={settlement:.08,build:.78,transform:.58,expand:.9,ruin:.16,rebuild:.62};
export class HistoricalTimeEngine{
 constructor(phases){if(!Array.isArray(phases)||phases.length<2)throw new Error('HistoricalTimeEngine requires canonical phases');this.phases=phases;this.max=phases.length-1;this.position=0;}
 sample(value){const v=Math.max(0,Math.min(this.max,Number(value)||0)),lo=Math.floor(v),hi=Math.min(this.max,lo+1),t=v-lo,a=this.phases[lo],b=this.phases[hi];return{position:v,index:Math.round(v),phase:this.phases[Math.round(v)],from:a,to:b,t,cityContinuity:this.interpolateState(a.state,b.state,t)};}
 interpolateState(a,b,t){const x=STATE_CURVE[a]??.5,y=STATE_CURVE[b]??x;return x+(y-x)*(t*t*(3-2*t));}
 herodianVisibility(value){const s=this.sample(value),herodian=this.phases.findIndex(p=>p.id==='herodian-jesus'),roman=this.phases.findIndex(p=>p.id==='roman-destruction');if(herodian<0||roman<0)return 0;if(s.position<=herodian)return Math.max(0,Math.min(1,(s.position-(herodian-1))));if(s.position<roman)return 1;return Math.max(0,1-(s.position-roman));}
 reversibleCheck(samples=256){for(let i=0;i<=samples;i++){const v=this.max*i/samples,a=this.sample(v),b=this.sample(this.max-(this.max-v));if(Math.abs(a.position-b.position)>1e-9||Math.abs(a.cityContinuity-b.cityContinuity)>1e-9)return false;}return true;}
}
