/* Scroll-controlled church journey: progressive enhancement; no scroll hijack. */
(()=>{'use strict';
const journey=document.getElementById('church-journey');if(!journey)return;
const scenes=[...journey.querySelectorAll('.mc-scene')],steps=[...journey.querySelectorAll('.mc-progress li')];
const reduced=window.matchMedia('(prefers-reduced-motion: reduce)');
let frame=0;
function render(){
 frame=0;
 if(reduced.matches){scenes.forEach(s=>{s.classList.add('is-current');s.style.removeProperty('--scene-p');s.style.removeProperty('--scene-out')});return}
 const max=Math.max(1,journey.offsetHeight-window.innerHeight);
 const progress=Math.max(0,Math.min(1,-journey.getBoundingClientRect().top/max));
 const scaled=progress*scenes.length;
 const current=Math.min(scenes.length-1,Math.floor(scaled));
 scenes.forEach((s,i)=>{const local=Math.max(0,Math.min(1,scaled-i));s.classList.toggle('is-current',i===current);s.classList.toggle('is-adjacent',i===current+1);s.style.setProperty('--scene-p',String(local));s.style.setProperty('--scene-out',String(Math.max(0,Math.min(1,scaled-i-0.72))/0.28))});
 steps.forEach((s,i)=>s.classList.toggle('is-current',i===current));
 journey.style.setProperty('--journey-p',String(progress));
}
function schedule(){if(!frame)frame=requestAnimationFrame(render)}
addEventListener('scroll',schedule,{passive:true});addEventListener('resize',schedule,{passive:true});reduced.addEventListener('change',schedule);render();
})();
