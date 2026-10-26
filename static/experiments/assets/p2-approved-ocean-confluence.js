/* P2 Westside Watch: accepted Fixed Ocean 2.5 confluence bridge.
   Reuses the v10 620 engraved paths and its approved 1.5 / 2.0 / 6.0 / 2.5 motion field.
   Two colour planes share the SAME geometries; only their ink colours differ. */
(()=>{
'use strict';
const stage=document.getElementById('dual-stage');
const canvas=document.getElementById('dual-transition-confluence');
const leftClip=document.getElementById('dual-ocean-gold-clip');
const rightClip=document.getElementById('dual-ocean-blue-clip');
const goldGroup=document.getElementById('dual-ocean-gold-lines');
const blueGroup=document.getElementById('dual-ocean-blue-lines');
const gold=document.getElementById('dual-contents');
const cover=document.getElementById('dual-cover');
const range=document.getElementById('dual-progress');
if(!stage||!canvas||!leftClip||!rightClip||!goldGroup||!blueGroup||!range)return;
const NS='http://www.w3.org/2000/svg',clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
const smooth=v=>{v=clamp(v,0,1);return v*v*(3-2*v)};
const reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
let paths=[],t=0,last=0,ready=false;
fetch('/experiments/assets/living-water-contour-engraving-v10.svg').then(r=>{
 if(!r.ok)throw Error('ocean source '+r.status);return r.text();
}).then(raw=>{
 const doc=new DOMParser().parseFromString(raw,'image/svg+xml');
 if(doc.querySelector('parsererror'))throw Error('ocean source svg parse');
 const source=document.importNode(doc.documentElement,true);
 source.style.cssText='position:fixed;left:-99999px;top:0;width:1600px;height:900px;visibility:hidden;pointer-events:none';
 document.body.appendChild(source);
 const originals=[...source.querySelectorAll('path')];
 for(const original of originals){
  const len=original.getTotalLength();
  if(len<1)continue;
  const steps=clamp(Math.ceil(len/22),28,110),points=[];
  for(let j=0;j<=steps;j++){const q=original.getPointAtLength(len*j/steps);points.push([q.x,q.y]);}
  const goldPath=document.createElementNS(NS,'path'),bluePath=document.createElementNS(NS,'path');
  for(const p of [goldPath,bluePath]){
   p.setAttribute('fill','none');
   p.setAttribute('stroke-width',original.getAttribute('stroke-width')||'.85');
   p.setAttribute('stroke-linecap','round');
   p.setAttribute('opacity',original.getAttribute('opacity')||'.2');
  }
  goldGroup.appendChild(goldPath);blueGroup.appendChild(bluePath);
  paths.push({points,goldPath,bluePath,baseOpacity:Number(original.getAttribute('opacity')||1)});
 }
 source.remove();
 ready=paths.length===620;
 canvas.dataset.sourcePaths=String(paths.length);
 canvas.dataset.motionPreset='fixed-ocean-2.5';
 if(!ready)canvas.dataset.error='original-620-paths-missing';
}).catch(e=>{canvas.dataset.error=e.message;});
function frame(now){
 requestAnimationFrame(frame);
 const p=clamp(Number(range.value)/100,0,1);
 const inTime=smooth((p-.19)/.14),outTime=1-smooth((p-.575)/.13);
 const visibility=inTime*outTime;
 canvas.style.opacity=String(ready?visibility:0);
 const surface=stage.getBoundingClientRect();
 const goldBox=gold.getBoundingClientRect(),coverBox=cover.getBoundingClientRect();
 const sx=1600/surface.width,sy=900/surface.height;
 const rect=(node,b,topReveal)=>{
  const x=(b.left-surface.left)*sx,y=(b.top-surface.top)*sy;
  const w=b.width*sx,h=b.height*sy;
  const reveal=topReveal?clamp(Number(stage.dataset.blueReveal),0,1):clamp(Number(stage.dataset.dawnReveal),0,1);
  const inset=h*(1-reveal);
  node.setAttribute('x',Math.max(0,x).toFixed(2));
  node.setAttribute('width',Math.max(0,w).toFixed(2));
  node.setAttribute('y',(topReveal?y:y+inset).toFixed(2));
  node.setAttribute('height',Math.max(0,h-inset).toFixed(2));
 };
 rect(leftClip,goldBox,false);rect(rightClip,coverBox,true);
 if(!ready||visibility<.015||!paths.length){last=now;return;}
 if(!last)last=now;
 const dt=Math.min(.05,(now-last)/1000);last=now;
 if(!reduce)t+=dt;
 const travel=1.5,contrast=2,amp=6,breath=21*Math.sin(t*Math.PI/7)+5*Math.sin(t*Math.PI/13);
 const field=(x,y)=>{
  const layer=smooth((y-180)/610),speed=.78+contrast*.25*layer,warp=18*Math.sin(y*.0065+x*.0018);
  return {layer,phase:.012*(x+warp)-t*.9*travel*speed};
 };
 for(const item of paths){
  let d='';
  for(let i=0;i<item.points.length;i++){
   const [x,y]=item.points[i],{layer,phase}=field(x,y),envelope=.72+.28*layer;
   const carrier=Math.sin(phase),secondary=Math.sin(phase*2-.6);
   const verticalMask=Math.sin(Math.PI*clamp(y/900,0,1));
   const stationaryRidges=.68*Math.sin(x*.008-y*.004)+.32*Math.sin(x*.014+y*.002);
   const spacingShift=2.5*1.8*verticalMask*stationaryRidges*Math.sin(y*.046);
   const yy=y+breath*.65+amp*envelope*(.82*carrier+.12*secondary)+spacingShift;
   const xx=x+amp*(.35*carrier+.10*secondary);
   d+=(i?'L':'M')+xx.toFixed(1)+' '+yy.toFixed(1);
  }
  item.goldPath.setAttribute('d',d);
  item.bluePath.setAttribute('d',d);
 }
 canvas.dataset.frameReady='true';
}
requestAnimationFrame(frame);
})();