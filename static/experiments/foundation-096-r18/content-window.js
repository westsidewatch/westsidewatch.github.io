
/* Actual content is the geometric authority. Observe its box, not an invented
   x/y square. R13.5 source profile is still read from the R14 runtime. */
(()=>{
const attr=(el,values)=>Object.entries(values).forEach(([k,v])=>el.setAttribute(k,String(v)));
for(const plane of document.querySelectorAll("[data-window-realm]")){
 const id=plane.dataset.windowRealm,field=plane.parentElement,anchor=field.querySelector(id==="church"?".model iframe":".cover img"),cover=field.querySelector(".cover");
 const profile=rhythms.find(r=>r.id===id).depths;
 if(!anchor)continue;
 function draw(){
  const b=field.getBoundingClientRect(),a=anchor.getBoundingClientRect();
  if(b.width<1||b.height<1||a.width<1||getComputedStyle(plane).display==="none")return;
  const w=b.width,h=b.height,mobile=matchMedia("(max-width:760px)").matches;
  const pad=Math.max(5,Math.min(12,w*.009));
  const size=Math.min(a.width,a.height)+pad*2;
  const x=a.left-b.left+(a.width-size)/2,y=a.top-b.top+(a.height-size)/2;
  attr(plane,{viewBox:`0 0 ${w} ${h}`});
  attr(plane.querySelector("mask"),{x:0,y:0,width:w,height:h});
  attr(plane.querySelector(".mask-field"),{x:0,y:0,width:w,height:h});
  attr(plane.querySelector(".mask-opening"),{x,y,width:size,height:size});
  attr(plane.querySelector(".plane-stock"),{x:0,y:0,width:w,height:h});
  attr(plane.querySelector(".plane-engraving"),{x:0,y:0,width:w,height:h});
  const n=profile.length;let d="",artW,artX,artY;
  if(id==="church"){
   const depth=Math.min(12,w*.012);
   d=`M0 ${profile[0]*depth}`;
   profile.forEach((v,i)=>{if(i)d+=`V${v*depth}`;d+=`H${w*(i+1)/n}`});
   d+=`V${h}H0Z`;
   artW=w;artX=0;artY=(h-w)/2;
  }else if(mobile){
   const bottom=cover.getBoundingClientRect().bottom-b.top;
   const depth=Math.min(7,w*.01);
   d=`M0 ${profile[0]*depth}`;
   profile.forEach((v,i)=>{if(i)d+=`V${v*depth}`;d+=`H${w*(i+1)/n}`});
   d+=`V${bottom}H0Z`;artW=w;artX=0;artY=(bottom-w)/2;
  }else{
   const edge=w*.56,depth=Math.min(13,w*.012);
   d=`M0 0H${edge-profile[0]*depth}`;
   profile.forEach((v,i)=>{if(i)d+=`H${edge-v*depth}`;d+=`V${h*(i+1)/n}`});
   d+="H0Z";artW=edge;artX=0;artY=(h-edge)/2;
  }
  attr(plane.querySelector(".profile-edge"),{d});
  attr(plane.querySelector(".plane-art"),{x:artX,y:artY,width:artW,height:artW});
  plane.dataset.aperture=JSON.stringify({x,y,size,anchorWidth:a.width,anchorHeight:a.height});
 }
 const ro=new ResizeObserver(draw);ro.observe(field);ro.observe(anchor);
 new MutationObserver(draw).observe(document.body,{attributes:true,attributeFilter:["class"]});
 anchor.addEventListener("load",draw);window.addEventListener("resize",draw,{passive:true});
 document.fonts?.ready.then(draw);requestAnimationFrame(draw);
}
})();
