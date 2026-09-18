const root=document.querySelector('.hosanna');
const master=document.querySelector('[data-master]');
const montage=document.querySelector('[data-montage]');
const enter=document.querySelector('[data-enter]');
const soundNote=document.querySelector('[data-sound-note]');

let manifest={master:{},moments:[],timing:{}};
let timers=[];

const wait=ms=>new Promise(r=>setTimeout(r,ms));
function clearTimers(){timers.forEach(clearTimeout);timers=[]}
function later(fn,ms){const id=setTimeout(fn,ms);timers.push(id);return id}

async function loadManifest(){
  const r=await fetch('./sequence.json',{cache:'no-store'});
  manifest=await r.json();
  if(manifest.master?.image){
    master.querySelector('.master-fallback').style.backgroundImage=`linear-gradient(180deg,rgba(8,8,7,.08),rgba(8,8,7,.42)),url("${manifest.master.image}")`;
    master.classList.add('has-image');
  }
}

function showMoment(moment){
  if(!moment.asset || moment.rightsState!=='publishable') return;
  const el=document.createElement('div');
  el.className='shot';
  el.style.backgroundImage=`url("${moment.asset}")`;
  el.style.setProperty('--dur',`${moment.durationMs||1800}ms`);
  el.dataset.moment=moment.id;
  montage.append(el);
  later(()=>el.remove(),(moment.durationMs||1800)+120);
}

async function loop(){
  clearTimers();
  root.dataset.state='approach';
  montage.replaceChildren();
  const t=manifest.timing||{};
  const approach=t.approachMs||5000;
  const montageStart=t.montageStartMs||2600;
  const arrival=t.arrivalMs||9200;
  const cycle=t.cycleMs||15000;

  manifest.moments.filter(x=>x.rightsState==='publishable').forEach((m,i)=>{
    later(()=>showMoment(m),montageStart+i*(m.offsetMs||900));
  });
  later(()=>{root.dataset.state='arrival'},arrival);
  later(loop,cycle);
}

enter.addEventListener('click',()=>{
  document.documentElement.classList.add('entered');
  window.dispatchEvent(new CustomEvent('westside:enter-city',{detail:{from:'hosanna-home'}}));
  // The next production surface will replace this target with the first city-depth spread.
  location.hash='enter';
});

document.addEventListener('pointerdown',()=>{soundNote.hidden=true},{once:true});

loadManifest().then(loop).catch(()=>loop());
