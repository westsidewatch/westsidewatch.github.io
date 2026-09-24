import {loadTerrainAuthority,terrainRuntimeState} from './terrain-runtime.js';
const timeline={
  "id": "jerusalem-continuous-build",
  "title": "Jerusalem — continuous urban biography",
  "range": {
    "from": "earliest-settlement",
    "to": "today"
  },
  "principle": "One terrain and coordinate system. Construction, expansion, destruction, abandonment, burial, reuse and rebuilding are all first-class temporal events. Never jump between isolated city models.",
  "phases": [
    {
      "id": "chalcolithic-early-bronze",
      "label": "最早聚落",
      "dateLabel": "c. 4th–3rd millennium BCE",
      "state": "settlement",
      "confidence": "reconstructed",
      "note": "Earliest occupation belongs to the southeastern ridge / spring landscape; do not invent monumental city fabric."
    },
    {
      "id": "middle-bronze",
      "label": "迦南城市",
      "dateLabel": "c. 19th–17th c. BCE onward",
      "state": "build",
      "confidence": "observed",
      "note": "Public architecture and fortified urban development emerge around the Gihon/eastern slope."
    },
    {
      "id": "late-bronze-iron1",
      "label": "晚青銅—鐵器早期",
      "dateLabel": "c. 16th–11th c. BCE",
      "state": "transform",
      "confidence": "reconstructed",
      "note": "Represent occupation intensity and debated urban form rather than a smooth growth curve."
    },
    {
      "id": "david-solomon",
      "label": "大衛—所羅門",
      "dateLabel": "10th c. BCE",
      "state": "build",
      "confidence": "disputed",
      "note": "Biblical royal-building coordinate; archaeological extent and specific monumental identifications remain debated."
    },
    {
      "id": "late-first-temple",
      "label": "第一聖殿晚期",
      "dateLabel": "8th–7th c. BCE",
      "state": "expand",
      "confidence": "observed",
      "note": "Major westward expansion and fortification become visible."
    },
    {
      "id": "babylonian-destruction",
      "label": "巴比倫毀城",
      "dateLabel": "586 BCE",
      "state": "ruin",
      "confidence": "observed",
      "note": "Destruction must be animated as loss/ruin, not skipped as a date marker."
    },
    {
      "id": "persian-nehemiah",
      "label": "波斯—尼希米",
      "dateLabel": "5th c. BCE",
      "state": "rebuild",
      "confidence": "reconstructed",
      "note": "Smaller post-exilic city and wall reconstruction layer."
    },
    {
      "id": "hellenistic-hasmonean",
      "label": "希臘化—哈斯蒙尼",
      "dateLabel": "4th–1st c. BCE",
      "state": "expand",
      "confidence": "reconstructed",
      "note": "Urban recovery and expansion toward the Second Temple city."
    },
    {
      "id": "herodian-jesus",
      "label": "大希律—耶穌",
      "dateLabel": "late 1st c. BCE–30s CE",
      "state": "build",
      "confidence": "reconstructed",
      "note": "Temple-platform and dense Second Temple city; hosts Biblical Route 01: Jesus Entry."
    },
    {
      "id": "roman-destruction",
      "label": "羅馬毀城",
      "dateLabel": "70 CE",
      "state": "ruin",
      "confidence": "observed",
      "note": "Destruction event alters walls, monumental fabric and occupation."
    },
    {
      "id": "aelia",
      "label": "Aelia Capitolina",
      "dateLabel": "2nd–4th c. CE",
      "state": "rebuild",
      "confidence": "reconstructed",
      "note": "Roman replanning is a new urban layer, not restoration of the Herodian city."
    },
    {
      "id": "byzantine",
      "label": "拜占庭",
      "dateLabel": "4th–7th c.",
      "state": "build",
      "confidence": "observed",
      "note": "Christian monumental city and street network."
    },
    {
      "id": "early-islamic",
      "label": "早期伊斯蘭",
      "dateLabel": "7th–11th c.",
      "state": "transform",
      "confidence": "observed",
      "note": "Haram/Temple Mount monumental transformation and changing southern urban fabric."
    },
    {
      "id": "crusader",
      "label": "十字軍",
      "dateLabel": "1099–1187",
      "state": "transform",
      "confidence": "observed",
      "note": "Reuse and reconstruction of existing city fabric."
    },
    {
      "id": "ayyubid-mamluk",
      "label": "阿尤布—馬穆魯克",
      "dateLabel": "12th–16th c.",
      "state": "transform",
      "confidence": "observed",
      "note": "Layered rebuilding, institutions, streets and reused fabric."
    },
    {
      "id": "ottoman",
      "label": "奧斯曼",
      "dateLabel": "1517–1917",
      "state": "build",
      "confidence": "observed",
      "note": "Present Old City wall/gate system becomes a major visible layer; Jaffa Gate belongs here."
    },
    {
      "id": "outside-walls",
      "label": "城外擴張",
      "dateLabel": "19th–early 20th c.",
      "state": "expand",
      "confidence": "observed",
      "note": "City breaks decisively beyond the Old City walls."
    },
    {
      "id": "modern",
      "label": "現代耶路撒冷",
      "dateLabel": "20th c.–today",
      "state": "expand",
      "confidence": "observed",
      "note": "Modern metropolitan fabric grows around the ancient topography; current political boundaries are not encoded as historical certainty."
    }
  ]
};
const phases=timeline.phases;
const city=document.querySelector('.j3k-city'),slider=document.querySelector('.j3k-scrubber'),stage=document.querySelector('.j3k-stage');
const markerButtons=[...document.querySelectorAll('.j3k-markers button')],eraEn=document.querySelector('.j3k-era-en'),eraZh=document.querySelector('.j3k-caption h2'),eraNote=document.querySelector('.j3k-era-note');
const evidenceToggle=document.querySelector('.j3k-evidence-toggle'),evidencePanel=document.querySelector('.j3k-evidence-panel'),routeToggle=document.querySelector('.j3k-route-toggle');
const play=document.querySelector('.j3k-play'),phaseDate=document.querySelector('.j3k-phase-date'),phaseStrip=document.querySelector('.j3k-phase-strip');
phases.forEach(()=>phaseStrip.append(document.createElement('i'))); const phaseTicks=[...phaseStrip.children];
const HERODIAN_LEDGER_URL='./data/objects/herodian-30ce.json';
const ENU_ORIGIN={lat:31.7780,lon:35.2350};const AOI={west:35.195,east:35.255,south:31.745,north:31.805};
function geographicPlacement(spatial){
 if(!spatial?.anchor)return null;
 const {lat,lon}=spatial.anchor;
 return {x:(lon-AOI.west)/(AOI.east-AOI.west)*100,y:(AOI.north-lat)/(AOI.north-AOI.south)*100};
}
let herodianObjects=[];
const objectLayer=document.createElement('div');objectLayer.className='j3k-object-layer';city.append(objectLayer);

async function loadHerodianLedger(){
 const ledger=await fetch(HERODIAN_LEDGER_URL).then(r=>{if(!r.ok)throw new Error('Herodian object ledger unavailable');return r.json()});
 herodianObjects=ledger.objects.map((object,i)=>{
   const el=document.createElement('div');el.className='j3k-historical-object';el.dataset.objectId=object.id;el.dataset.evidence=object.evidence;
   const pos=geographicPlacement(object.spatial);if(pos){el.style.left=pos.x+'%';el.style.top=pos.y+'%';el.dataset.registration=object.spatial.registration}else{el.dataset.registration='withheld';el.hidden=true}el.title=object.label;objectLayer.append(el);return {...object,el};
 });
 updateHistoricalObjects(Number(slider.value));
}
function updateHistoricalObjects(value){
 const phase=Math.round(value);
 herodianObjects.forEach((object,i)=>{
   let state='absent';
   if(phase===8) state='standing';
   else if(phase===9) state='ruin';
   else if(phase>9) state='buried-reused';
   object.el.dataset.lifecycle=state;
   object.el.style.setProperty('--life-opacity',state==='standing'?'1':state==='ruin'?'.42':state==='buried-reused'?'.12':'0');
 });
}

const blocks=[
[4,48,16,25,'observed'],[20,45,12,28,'observed'],[34,50,18,23,'reconstructed'],[54,42,12,31,'reconstructed'],[69,47,14,26,'inferred'],[82,52,10,20,'inferred'],[10,30,13,17,'observed'],[27,27,16,19,'reconstructed'],[48,29,19,18,'disputed'],[73,29,12,18,'inferred'],[6,65,21,12,'observed'],[30,66,16,10,'reconstructed'],[51,64,18,13,'inferred'],[72,67,20,10,'disputed'],[15,15,12,12,'reconstructed'],[39,13,16,13,'inferred'],[64,14,13,12,'disputed']];
blocks.forEach((b,i)=>{const el=document.createElement('div');el.className='j3k-block';el.dataset.status=b[4];el.style.left=b[0]+'%';el.style.top=b[1]+'%';el.style.width=b[2]+'%';el.style.height=b[3]+'%';el.dataset.birth=Math.floor(i/(blocks.length-1)*17);city.append(el)});
const blockEls=[...city.children];
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
const requested=new URL(location.href).searchParams.get('phase');const initial=Math.max(0,phases.findIndex(x=>x.id===requested));slider.value=initial;update(initial);

loadTerrainAuthority().then(({manifest})=>{
 const state=terrainRuntimeState(manifest);
 const badge=document.querySelector('.j3k-terrain-badge');
 const terrain=document.querySelector('.j3k-terrain');
 badge.textContent=state.label;
 terrain.dataset.terrainState=state.mode;
}).catch(()=>{document.querySelector('.j3k-terrain-badge').textContent='TERRAIN AUTHORITY ERROR'});

loadHerodianLedger().catch(()=>{stage.dataset.objectLedger='error'});
