/* R195 — one chapter-specific image field follows the lower-right interwoven square.
   The shared q is genuinely empty. The original illustration is retained for full viewing. */
(()=>{
"use strict";
let serial=0;
const ns="http://www.w3.org/2000/svg";
const el=(tag,cls)=>{const e=document.createElement(tag);e.className=cls;return e};
const junctionPath=i=>{const n=.018+i*.011,x=2+.004+i*.0016,y=1.99-i*.0009;return "M"+x+" 1.025V"+y+"H2V"+(2+n)+"H"+(1+n)+"V3"};
function inkPaths(){return Array.from({length:34},(_,i)=>'<path data-mother-route="'+i+'" d="'+junctionPath(i)+'" fill="none" stroke="currentColor" stroke-width="'+(i%6===0?.0022:.0012)+'" opacity="'+(.46-i*.008)+'"/>').join("")}
function accentPaths(){return Array.from({length:6},(_,i)=>'<path data-junction-accent="'+i+'" d="'+junctionPath(i)+'" fill="none" stroke="currentColor" stroke-width="'+(i===0?.0038:.0017)+'" opacity="'+(.92-i*.085)+'"/>').join("")}
function connect(core,prelude){
 if(!prelude)return;
 prelude.querySelector(".mother-prelude-spine")?.remove();
 const s=document.createElementNS(ns,"svg");s.setAttribute("class","mother-prelude-spine");s.setAttribute("aria-hidden","true");s.setAttribute("preserveAspectRatio","none");prelude.prepend(s);
 const draw=()=>{if(!core.isConnected||!prelude.isConnected)return;const q=core.clientWidth/3,depth=prelude.clientHeight/q;if(!q||!depth||core.clientWidth<=850||!document.getElementById("extension")?.checked||document.getElementById("texture")?.value!=="candidate"){s.replaceChildren();return}
 s.setAttribute("viewBox","0 0 3 "+depth);
 s.innerHTML=Array.from({length:34},(_,i)=>{const n=.018+i*.011,x=2+.004+i*.0022,y=.014+i*.00125;return '<path data-prelude-route="'+i+'" d="M'+(1+n)+' 0V'+y+'H'+x+'V'+depth+'" fill="none" stroke="'+(i<6?'var(--emmaus-guide)':'currentColor')+'" stroke-width="'+(i===0?.0038:i%6===0?.0022:.0012)+'" opacity="'+(i<6?.9-i*.08:.46-i*.008)+'"/>'}).join("")};
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
 field.append(g);connect(core,prelude);
 const gold=document.createElementNS(ns,"g");gold.setAttribute("class","mother-gold-engraving");gold.setAttribute("aria-hidden","true");
 for(let i=0;i<7;i++){const inset=.018+i*.008,p=document.createElementNS(ns,"path");p.setAttribute("d","M"+inset+" 1.94 V"+inset+" H"+(2-inset)+" V"+(.92-i*.008));p.setAttribute("fill","none");p.setAttribute("stroke-width",i===0?".0038":".0017");p.setAttribute("opacity",String(1-i*.075));gold.append(p)}field.querySelector(".mother-gold-engraving")?.remove();field.append(gold);
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