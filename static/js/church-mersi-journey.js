/* Scroll-controlled church journey: progressive enhancement; no scroll hijack. */
(()=>{'use strict';
const journey=document.getElementById('church-journey');if(!journey)return;
const scenes=[...journey.querySelectorAll('.mc-scene')],steps=[...journey.querySelectorAll('.mc-progress li')];
const reduced=window.matchMedia('(prefers-reduced-motion: reduce)');
const gallery=document.getElementById('church-horizontal');const track=gallery?.querySelector('.church-horizontal__track');
let lastGalleryHeight=0;
function galleryUpdate(){if(!gallery||!track)return;const mobile=matchMedia('(max-width: 850px)').matches;if(reduced.matches||mobile){track.style.transform='';return}const distance=Math.max(0,track.scrollWidth-gallery.clientWidth);const length=Math.max(1,gallery.offsetHeight-innerHeight);const p=Math.max(0,Math.min(1,-gallery.getBoundingClientRect().top/length));track.style.transform='translate3d('+(-distance*p)+'px,0,0)'}
let frame=0;
function render(){
 frame=0;galleryUpdate();
 if(reduced.matches){scenes.forEach(s=>{s.classList.add('is-current');s.classList.remove('is-adjacent');s.style.removeProperty('--scene-p');s.style.removeProperty('--scene-out')});return}
 const max=Math.max(1,journey.offsetHeight-window.innerHeight);
 const progress=Math.max(0,Math.min(1,-journey.getBoundingClientRect().top/max));
 const scaled=progress*(scenes.length-1+0.999);
 const current=Math.min(scenes.length-1,Math.floor(scaled));
 scenes.forEach((s,i)=>{const local=Math.max(0,Math.min(1,scaled-i));s.classList.toggle('is-current',i===current);s.classList.toggle('is-adjacent',i===current+1);s.style.setProperty('--scene-p',String(local));s.style.setProperty('--scene-out',String(Math.max(0,Math.min(1,scaled-i-0.72))/0.28))});
 steps.forEach((s,i)=>s.classList.toggle('is-current',i===current));
 journey.style.setProperty('--journey-p',String(progress));
}
function schedule(){if(!frame)frame=requestAnimationFrame(render)}
function measureGallery(){if(!gallery||!track)return;const mobile=matchMedia('(max-width: 850px)').matches;if(reduced.matches||mobile){gallery.style.height='';lastGalleryHeight=0;track.style.transform='';return}const distance=Math.max(0,track.scrollWidth-gallery.clientWidth);const height=Math.round(innerHeight+distance+innerHeight*.15);if(height!==lastGalleryHeight){gallery.style.height=height+'px';lastGalleryHeight=height}schedule()}
addEventListener('scroll',schedule,{passive:true});addEventListener('resize',()=>{measureGallery();schedule()},{passive:true});reduced.addEventListener('change',()=>{measureGallery();schedule()});
if(document.fonts?.ready)document.fonts.ready.then(measureGallery);
if(typeof ResizeObserver!=='undefined'&&track){const observer=new ResizeObserver(()=>{if(!reduced.matches)measureGallery()});observer.observe(track)}
measureGallery();render();
})();
