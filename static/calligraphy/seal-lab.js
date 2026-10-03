(()=>{"use strict";
const NS="http://www.w3.org/2000/svg";
const STYLES={
 genesis:{id:"genesis",label:"創世記",shape:"organic",yin:true,ink:"#9b4f3f"},
 matthew:{id:"matthew",label:"馬太福音",shape:"rect",yin:false,ink:"#7f2f2b"},
 psalms:{id:"psalms",label:"詩篇",shape:"round",yin:false,ink:"#8b3f35"}
};
function hash(s){let h=2166136261;for(const c of String(s)){h^=c.codePointAt(0);h=Math.imul(h,16777619)}return h>>>0}
function rng(seed){let x=seed||1;return()=>((x=Math.imul(x^x>>>15,1|x),x^=x+Math.imul(x^x>>>7,61|x),((x^x>>>14)>>>0)/4294967296))}
function refParts(ref){const m=String(ref||"").match(/^(.+?)(\d+):(\d+)$/);return m?{book:m[1],chapter:m[2],verse:m[3]}:{book:"",chapter:"",verse:""}}
function svgEl(n,a={}){const e=document.createElementNS(NS,n);for(const[k,v]of Object.entries(a))e.setAttribute(k,v);return e}
function make(text,opt={}){const style=STYLES[opt.style]||STYLES.genesis,seed=opt.seed??hash(text+style.id),r=rng(seed),yin=opt.yin??style.yin;
 const svg=svgEl("svg",{viewBox:"0 0 1000 1000",role:"img","aria-label":text,"data-seal-style":style.id,"data-seed":seed});
 const bg=svgEl(style.shape==="round"?"circle":"rect",style.shape==="round"?{cx:500,cy:500,r:455}:{x:55,y:55,width:890,height:890,rx:style.shape==="organic"?70:8});
 bg.setAttribute("fill",yin?style.ink:"none");bg.setAttribute("stroke",style.ink);bg.setAttribute("stroke-width","34");svg.appendChild(bg);
 const chars=[...String(text)].filter(x=>!/[\s:：]/.test(x)),cols=chars.length<=2?1:2,rows=Math.ceil(chars.length/cols),cw=760/cols,ch=760/rows;
 chars.forEach((c,i)=>{const col=i%cols,row=Math.floor(i/cols),x=120+col*cw+cw/2,y=120+row*ch+ch*.66;
  const g=svgEl("g",{"data-char":c,transform:`translate(${(r()-.5)*18} ${(r()-.5)*18}) rotate(${(r()-.5)*3} ${x} ${y})`});
  const t=svgEl("text",{x,y,"text-anchor":"middle","font-size":Math.min(cw,ch)*.66,"font-family":'"Noto Serif TC","STSong","Songti TC",serif',"font-weight":"700",fill:yin?"#f6efe1":style.ink});
  t.textContent=c;g.appendChild(t);svg.appendChild(g)
 });
 return svg
}
function mount(){
 const variants=document.querySelector(".variants");if(!variants||document.querySelector("#sealLab"))return;
 const box=document.createElement("section");box.id="sealLab";box.innerHTML='<div class="seal-lab-head"><small>3927 / SEAL LAB</small><h2>印章生成</h2></div><div id="sealPreview"></div><label>風格</label><select id="sealStyle"><option value="genesis">創世記</option><option value="matthew">馬太福音</option><option value="psalms">詩篇</option></select><label>印文</label><input id="sealText" value="一章一節"><div class="seal-row"><button id="sealYang">陽文</button><button id="sealYin">陰文</button><button id="sealAgain">再生成</button></div>';
 variants.appendChild(box);
 const style=document.createElement("style");style.textContent='#sealLab{margin-top:2rem;padding-top:1.4rem;border-top:1px solid #d8d1c2}#sealLab h2{margin:.45em 0 1em}#sealLab small{font:10px/1 Arial,sans-serif;letter-spacing:.16em;color:#8f7d38}#sealPreview{width:min(220px,100%);aspect-ratio:1;margin:0 auto 1rem}#sealPreview svg{width:100%;height:100%;display:block}#sealLab select,#sealLab input{width:100%;border:1px solid #d8d1c2;background:rgba(255,255,255,.5);padding:.7em;color:#24231f}#sealLab .seal-row{display:grid;grid-template-columns:1fr 1fr 1.2fr;gap:.45rem;margin-top:1rem}#sealLab button{border:1px solid #d8d1c2;background:transparent;padding:.65em .35em;cursor:pointer}';document.head.appendChild(style);
 let yin=STYLES.genesis.yin,seed=0;
 const preview=box.querySelector("#sealPreview"),txt=box.querySelector("#sealText"),sel=box.querySelector("#sealStyle");
 function draw(newSeed=false){if(newSeed)seed=(Date.now()&0xffffffff)>>>0;preview.replaceChildren(make(txt.value||"一章一節",{style:sel.value,yin,seed:seed||undefined}))}
 sel.onchange=()=>{yin=STYLES[sel.value].yin;seed=0;draw()};txt.oninput=()=>{seed=0;draw()};box.querySelector("#sealYang").onclick=()=>{yin=false;draw()};box.querySelector("#sealYin").onclick=()=>{yin=true;draw()};box.querySelector("#sealAgain").onclick=()=>draw(true);
 draw();
 window.SEAL_LAB={make,styles:STYLES,fromReference(ref){const p=refParts(ref);txt.value=p.chapter&&p.verse?`${p.chapter}章${p.verse}節`:txt.value;draw()}}
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",mount,{once:true});else mount();
})();