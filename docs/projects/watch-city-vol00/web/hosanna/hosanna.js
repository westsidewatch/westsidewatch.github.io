const root=document.querySelector('.hosanna');
const master=document.querySelector('[data-master]');
const montage=document.querySelector('[data-montage]');
const enter=document.querySelector('[data-enter]');
const soundNote=document.querySelector('[data-sound-note]');

let manifest={master:{},moments:[],timing:{}};
let timers=[];

function clearTimers(){timers.forEach(clearTimeout);timers=[]}
function later(fn,ms){const id=setTimeout(fn,ms);timers.push(id);return id}

async function loadManifest(){
  const r=await fetch('./sequence.json',{cache:'no-store'});
  if(!r.ok) throw new Error('Hosanna sequence unavailable');
  manifest=await r.json();
  if(manifest.master?.image){
    master.querySelector('.master-fallback').style.backgroundImage=`linear-gradient(180deg,rgba(8,8,7,.08),rgba(8,8,7,.42)),url("${manifest.master.image}")`;
    master.classList.add('has-image');
  }
}

function admittedMoment(moment){
  return moment?.rightsState==='publishable' &&
    Boolean(moment.asset) &&
    Boolean(moment.timestamp?.start) &&
    Boolean(moment.timestamp?.end);
}

function showStillMoment(moment){
  const el=document.createElement('div');
  el.className='shot';
  el.style.backgroundImage=`url("${moment.asset}")`;
  el.style.setProperty('--dur',`${moment.durationMs||1800}ms`);
  el.dataset.moment=moment.id;
  montage.append(el);
  later(()=>el.remove(),(moment.durationMs||1800)+120);
}

function showVideoMoment(moment){
  const el=document.createElement('video');
  el.className='shot shot-video';
  el.src=moment.asset;
  el.muted=true;
  el.playsInline=true;
  el.preload='metadata';
  el.dataset.moment=moment.id;
  el.style.setProperty('--dur',`${moment.durationMs||1800}ms`);

  const start=Number(moment.timestamp.start);
  const end=Number(moment.timestamp.end);
  const stop=()=>{try{el.pause()}catch{};el.remove()};

  el.addEventListener('loadedmetadata',()=>{
    if(Number.isFinite(start)) el.currentTime=start;
  },{once:true});
  el.addEventListener('seeked',()=>{el.play().catch(()=>{});},{once:true});
  el.addEventListener('timeupdate',()=>{if(Number.isFinite(end)&&el.currentTime>=end) stop()});
  montage.append(el);
  later(stop,(moment.durationMs||1800)+600);
}

function showMoment(moment){
  if(!admittedMoment(moment)) return;
  const type=moment.assetType || (/\.(mp4|webm|ogv)(\?|$)/i.test(moment.asset)?'video':'image');
  if(type==='video') showVideoMoment(moment); else showStillMoment(moment);
}

function loop(){
  clearTimers();
  root.dataset.state='approach';
  montage.replaceChildren();
  const t=manifest.timing||{};
  const montageStart=t.montageStartMs||2600;
  const arrival=t.arrivalMs||9200;
  const cycle=t.cycleMs||15000;

  manifest.moments.filter(admittedMoment).forEach((m,i)=>{
    later(()=>showMoment(m),montageStart+i*(m.offsetMs||900));
  });
  later(()=>{root.dataset.state='arrival'},arrival);
  later(loop,cycle);
}

enter.addEventListener('click',()=>{
  document.documentElement.classList.add('entered');
  window.dispatchEvent(new CustomEvent('westside:enter-city',{detail:{from:'hosanna-home'}}));
  location.hash='enter';
});

document.addEventListener('pointerdown',()=>{soundNote.hidden=true},{once:true});

loadManifest().then(loop).catch(()=>{
  root.dataset.state='arrival';
  soundNote.hidden=true;
});
