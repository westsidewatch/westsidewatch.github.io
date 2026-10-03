(()=>{"use strict";
const FONT_URL="https://cdn.jsdelivr.net/gh/lxgw/LxgwSeal@main/TTF/LXGWSeal-Regular.ttf";
let fontPromise;
function loadFont(){
 if(!window.opentype)return Promise.reject(new Error("opentype.js unavailable"));
 return fontPromise||(fontPromise=new Promise((resolve,reject)=>window.opentype.load(FONT_URL,(e,f)=>e?reject(e):resolve(f))));
}
function pathData(path){return path.commands.map(c=>{switch(c.type){case"M":return`M${c.x} ${-c.y}`;case"L":return`L${c.x} ${-c.y}`;case"C":return`C${c.x1} ${-c.y1} ${c.x2} ${-c.y2} ${c.x} ${-c.y}`;case"Q":return`Q${c.x1} ${-c.y1} ${c.x} ${-c.y}`;case"Z":return"Z";default:return""}}).join(" ")}
async function resolve(ch){
 const font=await loadFont(),glyph=font.charToGlyph(ch);
 if(!glyph||glyph.index===0)return null;
 const bb=glyph.getBoundingBox(),path=glyph.getPath(0,0,1000);
 return {path:pathData(path),viewBox:[bb.x1,-bb.y2,Math.max(1,bb.x2-bb.x1),Math.max(1,bb.y2-bb.y1)],source:"LXGW Seal / Shuowen-derived",license:"OFL-1.1",unicode:ch.codePointAt(0).toString(16).toUpperCase()}
}
function register(){window.SEAL_LAB?.registerGlyphProvider({id:"lxgw-seal",resolve})}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",register,{once:true});else register();
})();