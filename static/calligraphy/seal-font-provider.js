(()=>{"use strict";
const GLYPH_BASE="https://cdn.jsdelivr.net/gh/frankslin/kaiyuan-small-seal-font@main/glyphs/";
const cache=new Map();
let converter;
function toSeal(ch){
 if(!window.OpenCCSeal)return null;
 converter||(converter=window.OpenCCSeal.Converter({from:"t",to:"seal"}));
 const out=converter(ch),cp=out.codePointAt(0);
 return cp>=0x3D000&&cp<=0x3FC3F?out:null;
}
async function resolve(ch){
 const seal=toSeal(ch);
 if(!seal)return null;
 const hex=seal.codePointAt(0).toString(16).toUpperCase();
 if(cache.has(hex))return cache.get(hex);
 const task=fetch(`${GLYPH_BASE}u${hex}.svg`).then(async r=>{
  if(!r.ok)return null;
  const doc=new DOMParser().parseFromString(await r.text(),"image/svg+xml");
  const svg=doc.documentElement,path=svg.querySelector("path"),vb=(svg.getAttribute("viewBox")||"0 -880 1000 1000").trim().split(/\s+/).map(Number);
  if(!path||vb.length!==4||vb.some(Number.isNaN))return null;
  let bounds=null;try{const probe=document.createElementNS("http://www.w3.org/2000/svg","svg"),p=document.createElementNS("http://www.w3.org/2000/svg","path");probe.setAttribute("width","0");probe.setAttribute("height","0");probe.style.cssText="position:absolute;visibility:hidden;pointer-events:none";p.setAttribute("d",path.getAttribute("d"));probe.appendChild(p);document.body.appendChild(probe);const b=p.getBBox();if(b.width>0&&b.height>0)bounds=[b.x,b.y,b.width,b.height];probe.remove()}catch(e){}
  return {path:path.getAttribute("d"),viewBox:vb,bounds,source:"Kaiyuan Small Seal / Shuowen",license:"OFL-1.1",unicode:hex};
 }).catch(()=>null);
 cache.set(hex,task);
 return task;
}
function register(){window.SEAL_LAB?.registerGlyphProvider({id:"kaiyuan-small-seal",resolve})}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",register,{once:true});else register();
})();