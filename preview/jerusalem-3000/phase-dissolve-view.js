// One local canvas snapshot, never a second semantic city or historical layer.
export function createPhaseDissolveView(mount){
 const saved=document.createElement('canvas'),overlay=document.createElement('canvas');overlay.className='j3k-phase-dissolve';overlay.setAttribute('aria-hidden','true');Object.assign(overlay.style,{position:'absolute',inset:'0',width:'100%',height:'100%',pointerEvents:'none',zIndex:'1'});overlay.hidden=true;mount.append(overlay);
 let capturedPhase=null,currentPhase=null,lastIndex=null,show=false,opacity=0,enabled=false;
 const clear=()=>{show=false;opacity=0;overlay.hidden=true;capturedPhase=null;};
 return {
  before({phaseId,index,fraction,active,ready}){
   if(!active){clear();enabled=false;currentPhase=phaseId;lastIndex=index;return;}
   if(currentPhase!==phaseId){
    show=enabled&&lastIndex===index-1&&capturedPhase===currentPhase;
    if(show){overlay.width=saved.width;overlay.height=saved.height;overlay.getContext('2d').drawImage(saved,0,0);}
    currentPhase=phaseId;lastIndex=index;
   }
   enabled=true;opacity=show?(ready?Math.max(0,1-fraction/.3):1):0;overlay.hidden=opacity<=0;overlay.style.opacity=String(opacity);
  },
  after(canvas,{phaseId,fraction,ready}){if(!ready||fraction<.9)return;if(saved.width!==canvas.width||saved.height!==canvas.height){saved.width=canvas.width;saved.height=canvas.height;}saved.getContext('2d').drawImage(canvas,0,0);capturedPhase=phaseId;},
  clear,diagnostics:()=>({visible:!overlay.hidden,opacity,capturedPhase,snapshotLayers:capturedPhase?1:0,semanticCityObjects:0}),dispose(){overlay.remove();saved.width=saved.height=overlay.width=overlay.height=0;}
 };
}
