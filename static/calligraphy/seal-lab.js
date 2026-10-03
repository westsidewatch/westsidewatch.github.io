(()=>{"use strict";
const NS="http://www.w3.org/2000/svg";
const GLYPH_PROVIDERS=[];
function registerGlyphProvider(provider){if(provider&&provider.id&&typeof provider.resolve==="function"){const i=GLYPH_PROVIDERS.findIndex(x=>x.id===provider.id);if(i>=0)GLYPH_PROVIDERS[i]=provider;else GLYPH_PROVIDERS.push(provider)}}
async function resolveGlyph(ch,ctx={}){for(const p of GLYPH_PROVIDERS){try{const g=await p.resolve(ch,ctx);if(g?.path)return {...g,provider:p.id}}catch(e){console.warn("seal glyph provider",p.id,e)}}return null}
function pathGlyph(g,x,y,size,fill,scaleX=1,scaleY=1){const box=g.viewBox||[0,0,1000,1000],bw=box[2]||1000,bh=box[3]||1000,s=size/Math.max(bw,bh),cx=box[0]+bw/2,cy=box[1]+bh/2;return svgEl("path",{d:g.path,fill,transform:`translate(${x} ${y}) scale(${s*scaleX} ${s*scaleY}) translate(${-cx} ${-cy})`,"data-glyph-source":g.source||g.provider||"unknown","data-glyph-provider":g.provider||""})}
const STYLES={
 genesis:{id:"genesis",label:"創世記",shape:"organic",yin:true,ink:"#9b4f3f"},
 matthew:{id:"matthew",label:"馬太福音",shape:"rect",yin:false,ink:"#7f2f2b"},
 psalms:{id:"psalms",label:"詩篇",shape:"round",yin:false,ink:"#8b3f35"}
};
const BOOK_STYLE={"創世記":"genesis","创世记":"genesis","馬太福音":"matthew","马太福音":"matthew","詩篇":"psalms","诗篇":"psalms"};
const NUM=["零","一","二","三","四","五","六","七","八","九"];
function cnNum(n){n=+n;if(n<10)return NUM[n];if(n<20)return"十"+(n%10?NUM[n%10]:"");if(n<100)return NUM[Math.floor(n/10)]+"十"+(n%10?NUM[n%10]:"");return String(n)}
function hash(s){let h=2166136261;for(const c of String(s)){h^=c.codePointAt(0);h=Math.imul(h,16777619)}return h>>>0}
function rng(seed){let x=seed||1;return()=>((x=Math.imul(x^x>>>15,1|x),x^=x+Math.imul(x^x>>>7,61|x),((x^x>>>14)>>>0)/4294967296))}
function refParts(ref){const m=String(ref||"").match(/^(.+?)(\d+):(\d+)$/);return m?{book:m[1],chapter:m[2],verse:m[3]}:{book:"",chapter:"",verse:""}}
function svgEl(n,a={}){const e=document.createElementNS(NS,n);for(const[k,v]of Object.entries(a))e.setAttribute(k,v);return e}
function layoutCandidate(chars,rows,pad=145){const n=chars.length,cols=Math.ceil(n/rows),w=1000-pad*2,h=1000-pad*2,cw=w/cols,ch=h/rows,slots=[];for(let i=0;i<n;i++){const col=Math.floor(i/rows),row=i%rows;slots.push({index:i,col,row,x:1000-pad-col*cw-cw/2,y:pad+row*ch+ch/2,size:Math.min(cw,ch)*.78,scaleX:1,scaleY:1,rotate:0})}return{id:`vrtl-${cols}x${rows}`,flow:"vertical-rtl",rows,cols,pad,slots,metrics:{occupancy:n/(rows*cols),cellAspect:cw/ch}}}
function fitGlyphTransforms(c,glyphs=[]){const target=Math.max(.01,c.metrics.cellAspect||1);c.slots.forEach((slot,i)=>{const b=glyphs[i]?.viewBox||[0,0,1000,1000],ratio=Math.max(.01,(b[2]||1000)/(b[3]||1000)),need=target/ratio,limit=1.28;if(need>=1){slot.scaleX=Math.min(limit,Math.sqrt(need));slot.scaleY=1/slot.scaleX}else{slot.scaleY=Math.min(limit,Math.sqrt(1/need));slot.scaleX=1/slot.scaleY}});return c}
const COMPOSITIONS={balanced:{pad:145,size:1,stagger:0},loose:{pad:175,size:.9,stagger:0},dense:{pad:105,size:1.08,stagger:0},staggered:{pad:135,size:.98,stagger:.13}};
function applyComposition(c,name){const p=COMPOSITIONS[name]||COMPOSITIONS.balanced;c.composition=name;c.id+=`-${name}`;c.slots.forEach((s,i)=>{s.size*=p.size;if(p.stagger){const dir=((s.col+s.row)%2?1:-1),step=(1000-c.pad*2)/Math.max(c.rows,c.cols);if(c.cols>1)s.y+=dir*step*p.stagger;else s.x+=dir*step*p.stagger}});c.metrics.compositionDensity=p.size;c.metrics.stagger=p.stagger;return c}
function sealLayoutCandidates(chars,glyphs=[]){const n=chars.length;if(!n)return[];const rows=new Set([n<=3?n:Math.ceil(n/2),Math.ceil(Math.sqrt(n)),Math.ceil(n/2)]),out=[];for(const r of [...rows].filter(r=>r>0&&r<=n))for(const [name,p] of Object.entries(COMPOSITIONS))out.push(fitGlyphTransforms(applyComposition(layoutCandidate(chars,r,p.pad),name),glyphs));return out}
function scoreSealLayout(c,glyphs=[]){const m=c.metrics||{},corpus=window.SEAL_CORPUS?.stats,sealAspect=(1000-c.pad*2)/(1000-c.pad*2),corpusAspect=corpus?.meanAspect||1,corpusPenalty=corpus?Math.abs(Math.log(Math.max(.01,sealAspect/corpusAspect))):0,empty=1-(m.occupancy||0),aspect=Math.abs(Math.log(Math.max(.01,m.cellAspect||1))),gridAspect=Math.abs(Math.log(Math.max(.01,c.cols/c.rows))),utilization=(m.occupancy||0)/(1+aspect),ratios=glyphs.map(g=>{const b=g?.viewBox||[0,0,1000,1000];return Math.max(.01,(b[2]||1000)/(b[3]||1000))}),glyphAspect=ratios.length?ratios.reduce((a,v)=>a+Math.abs(Math.log(v/Math.max(.01,m.cellAspect||1))),0)/ratios.length:0,glyphFill=ratios.length?ratios.reduce((a,v)=>a+Math.min(v/(m.cellAspect||1),(m.cellAspect||1)/v),0)/ratios.length:1,transformPenalty=c.slots.length?c.slots.reduce((a,s)=>a+Math.abs(Math.log(s.scaleX||1))+Math.abs(Math.log(s.scaleY||1)),0)/c.slots.length:0,density=Math.abs(Math.log(Math.max(.01,m.compositionDensity||1))),stagger=Math.abs(m.stagger||0);const score=utilization*100+glyphFill*28-empty*45-aspect*18-gridAspect*6-glyphAspect*20-transformPenalty*24-density*5-stagger*4-corpusPenalty*8;return{score,components:{utilization,glyphFill,emptyPenalty:empty,cellAspectPenalty:aspect,gridAspectPenalty:gridAspect,glyphAspectPenalty:glyphAspect,transformPenalty,densityPenalty:density,staggerPenalty:stagger,corpusAspectPenalty:corpusPenalty},corpus:window.SEAL_CORPUS?.id||null}}
function selectSealLayout(candidates,glyphs=[]){let best=null;for(const c of candidates){c.scoring=scoreSealLayout(c,glyphs);if(!best||c.scoring.score>best.scoring.score)best=c}return best}
async function make(text,opt={}){const style=STYLES[opt.style]||STYLES.genesis,seed=opt.seed??hash(text+style.id),r=rng(seed),yin=opt.yin??style.yin;
 const svg=svgEl("svg",{viewBox:"0 0 1000 1000",role:"img","aria-label":text,"data-seal-style":style.id,"data-seed":seed});
 const bg=svgEl(style.shape==="round"?"circle":"rect",style.shape==="round"?{cx:500,cy:500,r:455}:{x:55,y:55,width:890,height:890,rx:style.shape==="organic"?70:8});
 bg.setAttribute("fill",yin?style.ink:"none");bg.setAttribute("stroke",style.ink);bg.setAttribute("stroke-width","34");svg.appendChild(bg);
 const chars=[...String(text)].filter(x=>!/[\s:：]/.test(x)),glyphs=await Promise.all(chars.map(c=>resolveGlyph(c,{style:style.id,book:opt.book||"",role:opt.role||"seal"}))),layout=selectSealLayout(sealLayoutCandidates(chars,glyphs),glyphs),slots=layout?.slots||[];
 svg.setAttribute("data-layout",layout?.id||"none");svg.setAttribute("data-composition",layout?.composition||"");svg.setAttribute("data-layout-score",layout?.scoring?.score?.toFixed(3)||"");
 for(let i=0;i<chars.length;i++){const c=chars[i],{x,y,size:glyphSize,scaleX=1,scaleY=1}=slots[i],resolved=glyphs[i];
  const g=svgEl("g",{"data-char":c,"data-layout":layout?.id||"none",transform:`translate(${(r()-.5)*18} ${(r()-.5)*18}) rotate(${(r()-.5)*3} ${x} ${y})`});
  if(resolved){g.appendChild(pathGlyph(resolved,x,y,glyphSize,yin?"#f6efe1":style.ink,scaleX,scaleY));g.setAttribute("data-vector-glyph","1")}
  else{const t=svgEl("text",{x,y,"text-anchor":"middle","font-size":glyphSize*.9,"font-family":'"Noto Serif TC","STSong","Songti TC",serif',"font-weight":"700",fill:yin?"#f6efe1":style.ink});t.textContent=c;g.appendChild(t);g.setAttribute("data-glyph-fallback","text")}
  svg.appendChild(g)
 }
 return svg
}
function mount(){
 const variants=document.querySelector(".variants"),panel=document.querySelector(".panel");if(!variants||!panel||document.querySelector("#sealLab"))return;
 const variantTitle=variants.querySelector("#variantTitle"),variantGrid=variants.querySelector("#variantGrid"),empty=variants.querySelector("#empty");
 let glyphBox=panel.querySelector("#glyphCandidates");if(!glyphBox){glyphBox=document.createElement("section");glyphBox.id="glyphCandidates";glyphBox.innerHTML='<h2>字形候選</h2><div id="glyphCandidateMount"></div>';panel.appendChild(glyphBox);const mount=glyphBox.querySelector("#glyphCandidateMount");if(variantGrid)mount.appendChild(variantGrid);if(empty)mount.appendChild(empty);if(variantTitle)variantTitle.remove()}
 variants.classList.add("yifang-panel");
 const box=document.createElement("section");box.id="sealLab";box.innerHTML='<div class="seal-lab-head"><h2>一方</h2></div><div id="sealPair"><div><small>經卷</small><div id="bookSealPreview"></div></div><div><small>章節</small><div id="sealPreview"></div></div></div><label>風格</label><select id="sealStyle"><option value="genesis">創世記</option><option value="matthew">馬太福音</option><option value="psalms">詩篇</option></select><label>印文</label><input id="sealText" value="一章一節"><div class="seal-row"><button id="sealYang">陽文</button><button id="sealYin">陰文</button><button id="sealAgain">再生成</button></div>';
 variants.replaceChildren(box);
 const style=document.createElement("style");style.textContent='#glyphCandidates{margin-top:2rem;padding-top:1.4rem;border-top:1px solid #d8d1c2}#glyphCandidates h2{font-size:1rem;font-weight:400;letter-spacing:.08em;margin:0 0 1rem}.yifang-panel{display:block}#sealLab{margin:0;padding:0;border:0}#sealLab h2{margin:.45em 0 1em}#sealLab small{font:10px/1 Arial,sans-serif;letter-spacing:.16em;color:#8f7d38}#sealPair{display:grid;grid-template-columns:1.25fr .75fr;gap:.8rem;align-items:end;margin-bottom:1rem}#sealPair>div>small{display:block;margin-bottom:.4rem}#bookSealPreview,#sealPreview{width:100%;aspect-ratio:1}#bookSealPreview svg,#sealPreview svg{width:100%;height:100%;display:block}#sealLab select,#sealLab input{width:100%;border:1px solid #d8d1c2;background:rgba(255,255,255,.5);padding:.7em;color:#24231f}#sealLab .seal-row{display:grid;grid-template-columns:1fr 1fr 1.2fr;gap:.45rem;margin-top:1rem}#sealLab button{border:1px solid #d8d1c2;background:transparent;padding:.65em .35em;cursor:pointer}';document.head.appendChild(style);
 let yin=STYLES.genesis.yin,seed=0;
 const preview=box.querySelector("#sealPreview"),bookPreview=box.querySelector("#bookSealPreview"),txt=box.querySelector("#sealText"),sel=box.querySelector("#sealStyle");let bookText="創世記";
 async function draw(newSeed=false){if(newSeed)seed=(Date.now()&0xffffffff)>>>0;const s=seed||undefined;const [bookSvg,refSvg]=await Promise.all([make(bookText,{style:sel.value,yin:!yin,seed:s,book:bookText,role:"book"}),make(txt.value||"一章一節",{style:sel.value,yin,seed:s,book:bookText,role:"reference"})]);bookPreview.replaceChildren(bookSvg);preview.replaceChildren(refSvg)}
 sel.onchange=()=>{yin=STYLES[sel.value].yin;seed=0;draw()};txt.oninput=()=>{seed=0;draw()};box.querySelector("#sealYang").onclick=()=>{yin=false;draw()};box.querySelector("#sealYin").onclick=()=>{yin=true;draw()};box.querySelector("#sealAgain").onclick=()=>draw(true);
 draw();
 window.SEAL_CORPUS?.refresh?.().then(()=>draw()).catch(e=>console.warn("seal corpus",e));
 window.SEAL_LAB={make,styles:STYLES,registerGlyphProvider,resolveGlyph,compositions:COMPOSITIONS,layoutCandidates:sealLayoutCandidates,scoreLayout:scoreSealLayout,selectLayout:selectSealLayout,fromReference(ref){const p=refParts(ref);if(p.book){bookText=p.book;const sid=BOOK_STYLE[p.book];if(sid){sel.value=sid;yin=STYLES[sid].yin}}if(p.chapter&&p.verse)txt.value=cnNum(p.chapter)+"章"+cnNum(p.verse)+"節";seed=0;draw()}}
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",mount,{once:true});else mount();
})();