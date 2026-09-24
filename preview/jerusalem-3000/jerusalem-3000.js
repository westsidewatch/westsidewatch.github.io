import {loadTerrainAuthority,terrainRuntimeState} from './terrain-runtime.js';
import {lifecycleStateAt} from './construction-engine.js';
import {loadAnchorEraObjects,updateAnchorEraObjects} from './anchor-era-runtime.js';
const timeline=await fetch('./data/continuous-build-timeline.json').then(r=>{if(!r.ok)throw new Error('timeline unavailable');return r.json()});
const phases=timeline.phases;
const city=document.querySelector('.j3k-city'),slider=document.querySelector('.j3k-scrubber'),stage=document.querySelector('.j3k-stage');
const markerButtons=[...document.querySelectorAll('.j3k-markers button')],eraEn=document.querySelector('.j3k-era-en'),eraZh=document.querySelector('.j3k-caption h2'),eraNote=document.querySelector('.j3k-era-note');
const evidenceToggle=document.querySelector('.j3k-evidence-toggle'),evidencePanel=document.querySelector('.j3k-evidence-panel'),routeToggle=document.querySelector('.j3k-route-toggle');
const play=document.querySelector('.j3k-play'),phaseDate=document.querySelector('.j3k-phase-date'),phaseStrip=document.querySelector('.j3k-phase-strip');
phases.forEach(()=>phaseStrip.append(document.createElement('i'))); const phaseTicks=[...phaseStrip.children];
const HERODIAN_LEDGER_URL='./data/objects/herodian-30ce.json';
const HERODIAN_LIFECYCLE_URL='./data/lifecycle/herodian-30ce.lifecycle.json';
const ENU_ORIGIN={lat:31.7780,lon:35.2350};const AOI={west:35.195,east:35.255,south:31.745,north:31.805};
function geographicPlacement(spatial){
 if(!spatial?.enuMetres)return null;
 const metresPerDegLat=111319.4908,metresPerDegLon=metresPerDegLat*Math.cos(ENU_ORIGIN.lat*Math.PI/180);
 const west=(AOI.west-ENU_ORIGIN.lon)*metresPerDegLon,east=(AOI.east-ENU_ORIGIN.lon)*metresPerDegLon;
 const south=(AOI.south-ENU_ORIGIN.lat)*metresPerDegLat,north=(AOI.north-ENU_ORIGIN.lat)*metresPerDegLat;
 return {x:(spatial.enuMetres.east-west)/(east-west)*100,y:(north-spatial.enuMetres.north)/(north-south)*100};
}
let herodianObjects=[],anchorEraObjects=[];
const objectLayer=document.createElement('div');objectLayer.className='j3k-object-layer';city.append(objectLayer);

async function loadHerodianLedger(){
 const [ledger,lifecycle]=await Promise.all([
   fetch(HERODIAN_LEDGER_URL).then(r=>{if(!r.ok)throw new Error('Herodian object ledger unavailable');return r.json()}),
   fetch(HERODIAN_LIFECYCLE_URL).then(r=>{if(!r.ok)throw new Error('Herodian lifecycle ledger unavailable');return r.json()})
 ]);
 const lifeById=new Map(lifecycle.objects.map(o=>[o.id,o.lifecycleEvents]));
 herodianObjects=ledger.objects.map(object=>{
   const el=document.createElement('div');el.className='j3k-historical-object';el.dataset.objectId=object.id;el.dataset.evidence=object.evidence;
   const pos=geographicPlacement(object.spatial);if(pos){el.style.left=pos.x+'%';el.style.top=pos.y+'%';el.dataset.registration=object.spatial.registration}else{el.dataset.registration='withheld';el.hidden=true}
   el.title=object.label;objectLayer.append(el);return {...object,lifecycleEvents:lifeById.get(object.id)||[],el};
 });
 updateHistoricalObjects(Number(slider.value));
}
function updateHistoricalObjects(value){
 const phaseId=phases[Math.round(value)].id;
 herodianObjects.forEach(object=>{
   const state=lifecycleStateAt(object,timeline,phaseId);
   object.el.dataset.lifecycle=state;
   const opacity={absent:'0',settlement:'.55',build:'1',expand:'1',transform:'.72',ruin:'.42',buried:'.12',rebuild:'.88'}[state]||'0';
   object.el.style.setProperty('--life-opacity',opacity);
 });
 updateAnchorEraObjects(anchorEraObjects,timeline,phaseId);
}

const blocks=[
[4,48,16,25,'observed'],[20,45,12,28,'observed'],[34,50,18,23,'reconstructed'],[54,42,12,31,'reconstructed'],[69,47,14,26,'inferred'],[82,52,10,20,'inferred'],[10,30,13,17,'observed'],[27,27,16,19,'reconstructed'],[48,29,19,18,'disputed'],[73,29,12,18,'inferred'],[6,65,21,12,'observed'],[30,66,16,10,'reconstructed'],[51,64,18,13,'inferred'],[72,67,20,10,'disputed'],[15,15,12,12,'reconstructed'],[39,13,16,13,'inferred'],[64,14,13,12,'disputed']];
blocks.forEach((b,i)=>{const el=document.createElement('div');el.className='j3k-block';el.dataset.status=b[4];el.style.left=b[0]+'%';el.style.top=b[1]+'%';el.style.width=b[2]+'%';el.style.height=b[3]+'%';el.dataset.birth=Math.floor(i/(blocks.length-1)*17);city.append(el)});
const blockEls=[...city.querySelectorAll('.j3k-block')];
const density=[.08,.16,.22,.30,.48,.20,.25,.46,.78,.30,.43,.56,.62,.66,.72,.79,.90,1];
const profile=[.38,.43,.47,.53,.65,.48,.50,.66,.90,.55,.63,.72,.76,.78,.82,.88,.94,1];
const lerp=(a,b,t)=>a+(b-a)*t;
function update(value){
 const lo=Math.floor(value),hi=Math.min(17,Math.ceil(value)),t=value-lo,p=phases[Math.round(value)],d=lerp(density[lo],density[hi],t),prof=lerp(profile[lo],profile[hi],t);
 stage.dataset.operation=p.state; stage.classList.toggle('herodian',p.id==='herodian-jesus');
 city.style.transform=`scaleY(${.72+.28*prof}) translateY(${(1-prof)*9}%)`;
 blockEls.forEach((el,i)=>{const birth=Number(el.dataset.birth),base=Math.max(0,Math.min(1,(value-birth+1.1)/1.1));let visible=base;
   if(p.state==='ruin') visible*=.38+(i%3)*.12;
   visible*=Math.max(.12,Math.min(1,d*1.5));
   el.style.opacity=visible;el.style.transform=`scaleY(${.12+.88*visible}) translateY(${(1-visible)*22}px)`;
   el.style.outline=el.dataset.status==='disputed'&&visible>.25?'1px dashed rgba(85,48,42,.65)':'none';
 });
 eraEn.textContent=(p.state||'').toUpperCase()+' · '+p.dateLabel;eraZh.textContent=p.label;eraNote.textContent=p.note;phaseDate.textContent=p.dateLabel;
 phaseTicks.forEach((x,i)=>{x.classList.toggle('is-past',i<Math.round(value));x.classList.toggle('is-current',i===Math.round(value))});
 markerButtons.forEach(x=>x.classList.toggle('is-active',Number(x.dataset.phase)===Math.round(value)));updateHistoricalObjects(value);
 const url=new URL(location.href);url.searchParams.set('phase',p.id);history.replaceState(null,'',url);
}
slider.addEventListener('input',()=>{stop();update(Number(slider.value))});
markerButtons.forEach(btn=>btn.addEventListener('click',()=>{stop();slider.value=btn.dataset.phase;update(Number(btn.dataset.phase))}));
let raf=null,last=0;function frame(ts){if(!last)last=ts;const delta=(ts-last)/1000;last=ts;let v=Number(slider.value)+delta*.65;if(v>=17){v=17;stop()}slider.value=v;update(v);if(raf)raf=requestAnimationFrame(frame)}
function start(){if(raf)return;play.textContent='Ⅱ 暫停';play.setAttribute('aria-pressed','true');last=0;raf=requestAnimationFrame(frame)}
function stop(){if(raf)cancelAnimationFrame(raf);raf=null;last=0;play.textContent='▶ 建城';play.setAttribute('aria-pressed','false')}
play.addEventListener('click',()=>raf?stop():start());
routeToggle.addEventListener('click',()=>{const on=!stage.classList.contains('route-on');stage.classList.toggle('route-on',on);routeToggle.setAttribute('aria-pressed',String(on));if(on){stop();slider.value=8;update(8)}});
evidenceToggle.addEventListener('click',()=>{const open=evidencePanel.hasAttribute('hidden');evidencePanel.toggleAttribute('hidden',!open);evidenceToggle.setAttribute('aria-expanded',String(open))});
const requested=new URL(location.href).searchParams.get('phase');const found=phases.findIndex(x=>x.id===requested);const initial=found>=0?found:0;slider.value=initial;update(initial);

loadTerrainAuthority().then(({manifest})=>{
 const state=terrainRuntimeState(manifest);
 const badge=document.querySelector('.j3k-terrain-badge');
 const terrain=document.querySelector('.j3k-terrain');
 badge.textContent=state.label;
 terrain.dataset.terrainState=state.mode;
}).catch(()=>{document.querySelector('.j3k-terrain-badge').textContent='TERRAIN AUTHORITY ERROR'});

Promise.all([loadHerodianLedger(),loadAnchorEraObjects(timeline,objectLayer).then(objects=>{anchorEraObjects=objects;updateHistoricalObjects(Number(slider.value))})]).catch(()=>{stage.dataset.objectLedger='error'});