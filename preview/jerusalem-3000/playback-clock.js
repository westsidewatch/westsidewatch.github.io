// Presentation time never catches up for work spent generating or in a background tab.
export function advancePlayback(position,elapsedSeconds,max,{ready=true,rate=1/12}={}){
 if(![position,elapsedSeconds,max,rate].every(Number.isFinite)||position<0||max<position||elapsedSeconds<0||rate<=0)throw new Error('Invalid playback clock');
 if(!ready)return position;
 return Math.min(max,Math.floor(position)+1,position+Math.min(elapsedSeconds,.1)*rate);
}
