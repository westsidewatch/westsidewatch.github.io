const root=document.querySelector('.hosanna');
const master=document.querySelector('[data-master]');
const montage=document.querySelector('[data-montage]');
const enter=document.querySelector('[data-enter]');
const soundNote=document.querySelector('[data-sound-note]');

let manifest={master:{},moments:[],timing:{}};
let timers=[];
let entering=false;
const preparedVideos=new Map();

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
  preloadMoments();
}

function admittedMoment(moment){
  return moment?.rightsState==='publishable' &&
    Boolean(moment.asset) &&
    Number.isFinite(Number(moment.timestamp?.start)) &&
    Number.isFinite(Number(moment.timestamp?.end));
}

function showStillMoment(moment){
  const el=document.createElement('div');
  const presentation=moment.presentation || 'film-frame';
  el.className=`shot ${presentation} ${moment.motion || 'motion-push-in'}`;
  el.style.backgroundImage=`url("${moment.asset}")`;
  el.style.setProperty('--dur',`${moment.durationMs||1800}ms`);
  const edit=moment.edit||{};
  const camera=edit.camera||{};
  const opacity=edit.opacity||{};
  if(camera.fromScale!=null) el.style.setProperty('--from-scale',camera.fromScale);
  if(camera.toScale!=null) el.style.setProperty('--to-scale',camera.toScale);
  if(camera.fromX!=null) el.style.setProperty('--from-x',`${camera.fromX}%`);
  if(camera.toX!=null) el.style.setProperty('--to-x',`${camera.toX}%`);
  if(camera.fromY!=null) el.style.setProperty('--from-y',`${camera.fromY}%`);
  if(camera.toY!=null) el.style.setProperty('--to-y',`${camera.toY}%`);
  if(camera.focus) el.style.backgroundPosition=camera.focus;
  if(opacity.peak!=null) el.style.setProperty('--peak-opacity',opacity.peak);
  if(opacity.hold!=null) el.style.setProperty('--hold-opacity',opacity.hold);
  el.dataset.cut=edit.cut||'semantic-overlay';
  el.dataset.moment=moment.id;
  if(moment.year) el.dataset.era=String(moment.year);
  montage.append(el);
  later(()=>el.remove(),(moment.durationMs||1800)+120);
}

function prepareVideoMoment(moment){
  let el=preparedVideos.get(moment.id);
  if(el) return el;

  el=document.createElement('video');
  el.className='shot shot-video';
  el.src=moment.asset;
  el.muted=true;
  el.playsInline=true;
  el.preload='auto';
  el.dataset.moment=moment.id;
  const start=Number(moment.timestamp.start);
  el.addEventListener('loadedmetadata',()=>{
    if(Number.isFinite(start)) el.currentTime=start;
  },{once:true});
  el.addEventListener('seeked',()=>{el.dataset.ready='true'},{once:true});
  preparedVideos.set(moment.id,el);
  montage.append(el);
  return el;
}

function preloadMoments(){
  manifest.moments.filter(admittedMoment).forEach(moment=>{
    const type=moment.assetType || (/\.(mp4|webm|ogv)(\?|$)/i.test(moment.asset)?'video':'image');
    if(type==='video') prepareVideoMoment(moment);
  });
}

function showVideoMoment(moment){
  const el=prepareVideoMoment(moment);
  const start=Number(moment.timestamp.start);
  const end=Number(moment.timestamp.end);
  let started=false;
  const stop=()=>{
    try{el.pause()}catch{}
    el.classList.remove('is-playing');
  };
  const begin=()=>{
    if(started) return;
    started=true;
    el.classList.add('is-playing');
    el.play().catch(()=>{});
  };
  const seekAndBegin=()=>{
    if(!Number.isFinite(start)){begin();return}
    if(Math.abs(el.currentTime-start)<.12){begin();return}
    el.addEventListener('seeked',begin,{once:true});
    el.currentTime=start;
  };

  if(el.readyState>=1) seekAndBegin();
  else el.addEventListener('loadedmetadata',seekAndBegin,{once:true});

  el.ontimeupdate=()=>{
    if(started&&Number.isFinite(end)&&el.currentTime>=end){
      stop();
      el.ontimeupdate=null;
    }
  };
}

function showMoment(moment){
  if(!admittedMoment(moment)) return;
  const type=moment.assetType || (/\.(mp4|webm|ogv)(\?|$)/i.test(moment.asset)?'video':'image');
  if(type==='video') showVideoMoment(moment); else showStillMoment(moment);
}

function loop(){
  if(entering || coverPaused) return;
  clearTimers();
  root.dataset.state='approach';
  preparedVideos.forEach(el=>{
    try{el.pause()}catch{}
    el.classList.remove('is-playing');
  });
  const t=manifest.timing||{};
  const montageStart=t.montageStartMs||2600;
  const moments=manifest.moments.filter(m=>admittedMoment(m)&&m.assetType==='video');
  const overlays=manifest.moments.filter(m=>admittedMoment(m)&&m.assetType==='image');
  let cursor=montageStart;

  moments.forEach(m=>{
    const start=Number(m.timestamp?.start);
    const end=Number(m.timestamp?.end);
    const clipMs=Number.isFinite(start)&&Number.isFinite(end)
      ? Math.max(800,((end-start)*1000)+250)
      : 6000;
    later(()=>showMoment(m),cursor);
    overlays.filter(overlay=>overlay.overlayFor===m.id).forEach(overlay=>{
      later(()=>showMoment(overlay),cursor+Math.max(0,Number(overlay.overlayDelayMs)||0));
    });
    cursor+=Math.max(800,clipMs-450);
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

// The home cover embeds this exact sequence, never a separate single-clip cut.
let coverPaused=false;
window.addEventListener('message',event=>{
  if(event.origin!==location.origin||event.source!==parent||event.data?.type!=='watch-cover-playback')return;
  const pause=Boolean(event.data.paused);
  if(pause){coverPaused=true;clearTimers();preparedVideos.forEach(video=>video.pause());}
  else if(coverPaused){coverPaused=false;loop();}
});
