/* R195 — one chapter-specific image field follows the lower-right interwoven square.
   The shared q is genuinely empty. The original illustration is retained for full viewing. */
(()=>{
"use strict";
let serial=0;
const ns="http://www.w3.org/2000/svg";
const el=(tag,cls)=>{const e=document.createElement(tag);e.className=cls;return e};
function mount(core){
 if(!core)return;
 core.querySelectorAll(".mother-art,.mother-art-dialog,.mother-art-open").forEach(e=>e.remove());
 const prelude=core.nextElementSibling?.classList.contains("chapter-prelude")?core.nextElementSibling:null;
 prelude?.querySelectorAll(".mother-art-credit-strip").forEach(e=>e.remove());
 core.classList.remove("mother-art-has-credit");
 core.classList.remove("mother-art-ready","mother-art-available");
 const field=core.querySelector(".core-field"),figure=core.querySelector(".illustration figure"),img=figure?.querySelector("img");
 if(!field)return;
 const lines=field.querySelector(".mother-art-outline");lines?.remove();
 const g=document.createElementNS(ns,"g");g.setAttribute("class","mother-art-outline");g.setAttribute("aria-hidden","true");
 // Two exposed L fields, with the central shared square not filled or covered.
 // Corner continuation remains aligned to the original 3q lattice.
 for(const [role,path] of [["a","M0 2V0H2V1 M0 2H1"],["b","M2 1H3V3H1V2"],["joint-a","M1 1V2H0"],["joint-b","M2 0V1H3"]]){
  const p=document.createElementNS(ns,"path");p.setAttribute("data-mother-edge",role);p.setAttribute("d",path);p.setAttribute("fill","none");g.append(p)
 }
 field.append(g);
 if(!img||!img.getAttribute("src"))return;
 const layer=el("div","mother-art");layer.setAttribute("aria-hidden","true");layer.dataset.artSource=img.getAttribute("src");
 const picture=el("div","mother-art-picture");layer.append(picture);core.insertBefore(layer,core.firstChild);
 // Initial focal offsets are explicit chapter-specific art-direction candidates.
 const parent=core.closest(".composition"),chapter=parent?.dataset.book?parent.dataset.book+":"+parent.dataset.chapter:"42:24";
 const focus={"42:24":"50% 0%","40:17":"50% 28%"}[chapter]||"50% 42%";
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
window.EMMAUS_MOTHER={mount};
})();