/* Lazy First Look embeds share their actual realm homepage, not a second implementation. */
(()=>{const frames=[...document.querySelectorAll('[data-fl-realm-frame]')];
window.addEventListener('message',event=>{if(event.origin!==location.origin||event.data?.type!=='ws-first-look:height')return;const frame=frames.find(f=>f.contentWindow===event.source),height=Number(event.data.height);if(frame&&Number.isFinite(height)&&height>=350&&height<=6000)frame.style.height=Math.ceil(height)+'px'});
let raf;const update=()=>{for(const frame of frames){const rect=frame.getBoundingClientRect(),progress=Math.max(0,Math.min(1,-rect.top/(Math.max(rect.height,1)*.55)));frame.contentWindow?.postMessage({type:'ws-first-look:progress',progress},location.origin)}raf=null};const schedule=()=>{if(!raf)raf=requestAnimationFrame(update)};
window.addEventListener('scroll',schedule,{passive:true});window.addEventListener('resize',schedule);frames.forEach(f=>f.addEventListener('load',schedule));schedule();
})();
