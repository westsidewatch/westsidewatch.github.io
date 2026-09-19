const root=document.querySelector('.hosanna');
const master=document.querySelector('[data-master]');
const montage=document.querySelector('[data-montage]');
const enter=document.querySelector('[data-enter]');
const soundNote=document.querySelector('[data-sound-note]');

let manifest={master:{},moments:[],timing:{}};
let timers=[];
let entering=false;

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
    Number.isFinite(Number(moment.timestamp?.start)) &&
    Number.isFinite(Number(moment.timestamp?.end));
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
  el.preload='auto';
  el.dataset.moment=moment.id;

  const start=Number(moment.timestamp.start);
  const end=Number(moment.timestamp.end);
  let started=false;
  const stop=()=>{try{el.pause()}catch{};el.remove()};

  el.addEventListener('loadedmetadata',()=>{
    if(Number.isFinite(start)) el.currentTime=start;
  },{once:true});
  el.addEventListener('seeked',()=>{
    if(started) return;
    started=true;
    el.classList.add('is-playing');
    el.play().catch(()=>{});
    later(stop,Math.max(8000,((end-start)*1000)+1200));
  });
  el.addEventListener('timeupdate',()=>{if(started&&Number.isFinite(end)&&el.currentTime>=end) stop()});
  el.addEventListener('error',()=>{el.dataset.failed='true'});
  montage.append(el);
}
function showMoment(moment){
  if(!admittedMoment(moment)) return;
  const type=moment.assetType || (/\.(mp4|webm|ogv)(\?|$)/i.test(moment.asset)?'video':'image');
  if(type==='video') showVideoMoment(moment); else showStillMoment(moment);
}

function loop(){
  if(entering) return;
  clearTimers();
  root.dataset.state='approach';
  montage.replaceChildren();
  const t=manifest.timing||{};
  const montageStart=t.montageStartMs||2600;
  const moments=manifest.moments.filter(admittedMoment);
  let cursor=montageStart;

  moments.forEach(m=>{
    const start=Number(m.timestamp?.start);
    const end=Number(m.timestamp?.end);
    const clipMs=(m.assetType==='video' && Number.isFinite(start) && Number.isFinite(end))
      ? Math.max(8000,((end-start)*1000)+1200)
      : (m.durationMs||1800);
    later(()=>showMoment(m),cursor);
    cursor+=clipMs;
  });

  const arrival=Math.max(t.arrivalMs||9200,cursor-6000);
  const cycle=Math.max(t.cycleMs||15000,cursor+600);
  later(()=>{root.dataset.state='arrival'},arrival);
  later(loop,cycle);
}

enter.addEventListener('click',()=>{
  if(entering) return;
  entering=true;
  clearTimers();
  montage.replaceChildren();
  root.dataset.state='threshold';
  document.documentElement.classList.add('entering');
  document.querySelector('[data-city-entry]')?.setAttribute('aria-hidden','false');
  window.dispatchEvent(new CustomEvent('westside:enter-city',{
    detail:{from:'hosanna-home',coordinate:'city',next:'jerusalem-depth'}
  }));
  history.replaceState(null,'','#enter');
});

document.addEventListener('pointerdown',()=>{soundNote.hidden=true},{once:true});

loadManifest().then(loop).catch(()=>{
  root.dataset.state='arrival';
  soundNote.hidden=true;
});
