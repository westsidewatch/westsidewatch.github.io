/* R195 — one chapter-specific image field follows the lower-right interwoven square.
   The shared q is genuinely empty. The original illustration is retained for full viewing. */
(()=>{
"use strict";
let serial=0;
const ns="http://www.w3.org/2000/svg";
const el=(tag,cls)=>{const e=document.createElement(tag);e.className=cls;return e};
// R200 — nested square-fold families with real alternating underpasses.
const f=v=>Number(v.toFixed(5));
const A=Array.from({length:17},(_,i)=>{const u=i/16;return{x:f(1.18+.69*Math.pow(u,1.28)),y:f(2.055+.45*Math.pow(u,1.44)),start:f(1.018+.02*(1-u)),end:3}});
const B=Array.from({length:17},(_,i)=>{const u=i/16;return{x:f(1.045+.58*Math.pow(u,1.35)),y:f(2.35+.60*Math.pow(u,1.16)),start:f(2.018+.015*u),end:1.985}});
function segment(axis,constant,from,to,gaps){
 const cuts=gaps.filter(x=>x>from+.004&&x<to-.004).sort((a,b)=>a-b),parts=[];let p=from;
 const draw=(s,e)=>{if(e-s<.001)return;parts.push(axis==="h"?"M"+f(s)+" "+f(constant)+"H"+f(e):"M"+f(constant)+" "+f(s)+"V"+f(e))};
 for(const x of cuts){draw(p,x-.0027);p=Math.max(p,x+.0027)}draw(p,to);return parts.join(" ");
}
function route(family,i){
 const a=A[i],b=B[i];
 if(family==="a"){
  const h=B.filter((b,k)=>(i+k)%2===0&&b.x>a.start&&b.x<a.x&&a.y>b.start&&a.y<b.y).map(b=>b.x);
  const v=B.filter((b,k)=>(i+k)%2===1&&a.x>b.x&&a.x<b.end&&b.y>a.y&&b.y<a.end).map(b=>b.y);
  // R203: the three accent folds enter from the lower corner of the
  // upper-left mother. The shared aperture remains unmarked inside.
  const entry=i===0?"M1 2H"+a.start+"V"+a.y+" ":
   i===6||i===12?"M"+a.start+" "+f(2.018+(i/6)*.016)+"V"+a.y+" ":"";
  return entry+segment("h",a.y,a.start,a.x,h)+" "+segment("v",a.x,a.y,a.end,v)
 }
 const v=A.filter((a,k)=>(i+k)%2===1&&b.x>a.start&&b.x<a.x&&a.y>b.start&&a.y<b.y).map(a=>a.y);
 const h=A.filter((a,k)=>(i+k)%2===0&&a.x>b.x&&a.x<b.end&&b.y>a.y&&b.y<a.end).map(a=>a.x);
 // R203: the outline rail turns at the actual lower-right mother
 // junction. The two subordinate folds have registered open ends;
 // no stroke enters the shared aperture or the negative impression.
 const upper={0:[2.020,1.055,2],6:[2.046,1.080,1.965],12:[2.073,1.105,1.938]}[i];
 let margin="";
 if(upper){
  const [x,top,bottom]=upper;
  margin="M"+x+" "+top+"V"+bottom+"H"+(i===0?b.x:2.006)+" ";
  margin+=i===0?"M"+b.x+" 2V"+b.start+" ":"M"+f(1.98-(i/6)*.026)+" "+b.start+"H"+b.x+" ";
 }
 return margin+segment("v",b.x,b.start,b.y,v)+" "+segment("h",b.y,b.x,b.end,h)
}
function inkPaths(){return ["a","b"].flatMap(family=>Array.from({length:17},(_,i)=>'<path data-mother-route="'+family+i+'" data-weave-family="'+family+'" d="'+route(family,i)+'" fill="none" stroke="currentColor" stroke-width="'+(i===0?.0030:i%5===0?.0021:.0012)+'" opacity="'+f(.62-i*.019)+'"/>')).join("")}
function accentPaths(){return ["a","b"].flatMap(family=>[0,6,12].map((i,k)=>'<path data-junction-accent="'+family+i+'" d="'+route(family,i)+'" fill="none" stroke="currentColor" stroke-width="'+(k===0?.0042:.0026)+'" opacity="'+f(.98-k*.14)+'"/>')).join("")}
function connect(core,prelude){
 if(!prelude)return;
 prelude.querySelector(".mother-prelude-spine")?.remove();
 const s=document.createElementNS(ns,"svg");s.setAttribute("class","mother-prelude-spine");s.setAttribute("aria-hidden","true");s.setAttribute("preserveAspectRatio","none");prelude.prepend(s);
 const draw=()=>{if(!core.isConnected||!prelude.isConnected)return;const q=core.clientWidth/3,depth=prelude.clientHeight/q;if(!q||!depth||core.clientWidth<=850||!document.getElementById("extension")?.checked||document.getElementById("texture")?.value!=="candidate"){s.replaceChildren();return}
 s.setAttribute("viewBox","0 0 3 "+depth);
 // R205: six actual exits from the A-family; no duplicate 17+17
 // sources. Reverse turn heights keep the six folds parallel, then
 // register to the six long study-edge rails in the next reading band.
 const exits=[0,3,6,9,12,16];
 s.innerHTML=exits.map((sourceIndex,i)=>{
  const source=A[sourceIndex].x,x=f(2+.004+i*.0022),y=f(.105-i*.014);
  return '<path data-prelude-route="'+i+'" data-source-route="a'+sourceIndex+'" d="M'+source+' 0V'+y+'H'+x+'V'+depth+'" fill="none" stroke="'+(i===0?'var(--emmaus-guide)':'currentColor')+'" stroke-width="'+(i===0?.0038:i===3?.0022:.0012)+'" opacity="'+(i===0?.92:.54-i*.055)+'"/>';
 }).join("")};
 const observer=new ResizeObserver(()=>{if(!core.isConnected||!prelude.isConnected){observer.disconnect();return}draw()});observer.observe(core);observer.observe(prelude);
 for(const id of ["texture","extension"]){const control=document.getElementById(id);const onChange=()=>{if(!core.isConnected){control.removeEventListener("change",onChange);return}draw()};control?.addEventListener("change",onChange)}
 requestAnimationFrame(draw)
}
function mount(core){
 if(!core)return;
 core.querySelectorAll(".mother-art,.mother-art-dialog,.mother-art-open").forEach(e=>e.remove());
 const prelude=core.nextElementSibling?.classList.contains("chapter-prelude")?core.nextElementSibling:null;
 prelude?.querySelectorAll(".mother-art-credit-strip").forEach(e=>e.remove());
 core.classList.remove("mother-art-has-credit");core.classList.add("mother-left");
 core.classList.remove("mother-art-ready","mother-art-available");
 const field=core.querySelector(".core-field"),figure=core.querySelector(".illustration figure"),img=figure?.querySelector("img");
 if(!field)return;
 const lines=field.querySelector(".mother-art-outline");lines?.remove();
 const g=document.createElementNS(ns,"g");g.setAttribute("class","mother-art-outline");g.setAttribute("aria-hidden","true");
 // Two exposed L fields, with the central shared square not filled or covered.
 // Corner continuation remains aligned to the original 3q lattice.
 for(const [role,path] of [["a","M.008 1.992V.008H1.992V1"],["b","M2.008 1.008H2.992V2.992H1.008V2"],["joint-a","M.008 1.992H1"],["joint-b","M2 1H1V2"]]){
  const p=document.createElementNS(ns,"path");p.setAttribute("data-mother-edge",role);p.setAttribute("d",path);p.setAttribute("fill","none");g.append(p)
 }
 // R206 isolated material proof: reuse the existing engraving, reflected
 // across the shared square's diagonal. No new line family or raster asset.
 field.querySelector(".mother-paper-echo")?.remove();
 const echo=document.createElementNS(ns,"g");
 echo.setAttribute("class","mother-paper-echo");
 echo.setAttribute("aria-hidden","true");
 echo.setAttribute("transform","matrix(0 -1 -1 0 3 3)");
 echo.innerHTML=inkPaths().replaceAll("data-mother-route=","data-paper-route=").replaceAll("data-weave-family=","data-paper-family=");
 field.append(echo);
 field.append(g);connect(core,prelude);
 const gold=document.createElementNS(ns,"g");gold.setAttribute("class","mother-gold-engraving");gold.setAttribute("aria-hidden","true");
 // Open folds at both exchange corners, rather than seven nested frames.
 // The primary strokes share the exact start coordinates of A0 and B0.
 const folds=[
  "M.018 .04V1.982H1V2",
  "M.046 .34V1.954H.982V1.985",
  "M.076 .78V1.924H.955V1.965",
  "M.46 .018H1.982V1H2.02V1.055",
  "M.75 .046H1.954V.985",
  "M1.06 .076H1.924V.965",
  "M1.35 .108H1.892V.93"
 ];
 for(let i=0;i<folds.length;i++){const p=document.createElementNS(ns,"path");p.setAttribute("d",folds[i]);p.setAttribute("fill","none");p.setAttribute("stroke-width",i===0||i===3?".0038":i===1||i===4?".0026":".0015");p.setAttribute("opacity",i===0||i===3?".96":i===1||i===4?".74":".46");gold.append(p)}
 field.querySelector(".mother-gold-engraving")?.remove();field.append(gold);
 if(!img||!img.getAttribute("src"))return;
 const layer=el("div","mother-art");layer.setAttribute("aria-hidden","true");layer.dataset.artSource=img.getAttribute("src");
 const picture=el("div","mother-art-picture");layer.append(picture);core.insertBefore(layer,core.firstChild);
 // Initial focal offsets are explicit chapter-specific art-direction candidates.
 const parent=core.closest(".composition"),chapter=parent?.dataset.book?parent.dataset.book+":"+parent.dataset.chapter:"42:24";
 const focus={"42:24":"50% 18%","40:17":"50% 14%"}[chapter]||"50% 35%";
 picture.style.setProperty("--mother-art-focus",focus);layer.dataset.focus=focus;
 const caption=figure.querySelector("figcaption");const open=el("button","mother-art-open");open.type="button";open.textContent="觀看完整圖版";open.setAttribute("aria-label","觀看完整圖版："+(img.alt||caption?.textContent||""));if(prelude){const strip=el("div","mother-art-credit-strip"),copy=el("div","mother-art-caption-copy");if(caption){for(const node of caption.childNodes){if(node.nodeName==="BR")copy.append(document.createTextNode(" · "));else copy.append(node.cloneNode(true))}}else copy.textContent=img.alt;strip.append(copy,open);prelude.prepend(strip);core.classList.add("mother-art-has-credit")}else figure.append(open);
 const dialog=el("dialog","mother-art-dialog");dialog.id="mother-art-"+(++serial);dialog.setAttribute("aria-label",img.alt||"完整圖版");open.setAttribute("aria-controls",dialog.id);
 const close=el("button","mother-art-close");close.type="button";close.textContent="關閉";
 const full=el("img","mother-art-full");full.alt=img.alt;const credit=el("p","mother-art-credit");credit.textContent=caption?.textContent||img.alt;
 dialog.append(close,full,credit);core.append(dialog);
 open.addEventListener("click",()=>{full.src=img.currentSrc||img.src;dialog.showModal()});
 close.addEventListener("click",()=>dialog.close());dialog.addEventListener("click",e=>{if(e.target===dialog)dialog.close()});
 const ready=()=>{if(!img.naturalWidth)return;if(!core.isConnected){requestAnimationFrame(()=>{if(core.isConnected)ready()});return;}picture.style.backgroundImage="url("+JSON.stringify(img.currentSrc||img.src)+")";core.classList.add("mother-art-ready");open.disabled=false};
 const fail=()=>{core.classList.remove("mother-art-ready");open.disabled=true};
 core.classList.add("mother-art-available");open.disabled=true;img.addEventListener("load",ready,{once:true});img.addEventListener("error",fail,{once:true});
 if(img.complete){if(img.naturalWidth)requestAnimationFrame(ready);else fail()}
}
window.EMMAUS_MOTHER={mount,inkPaths,accentPaths};
})();