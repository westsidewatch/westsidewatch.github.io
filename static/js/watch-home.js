(() => {
  if(/^(#contents|#vol-00-proclamation|#movement-|#column-)/.test(location.hash)){location.replace("/vol-00/"+location.hash);return;}
  const current=document.querySelector('.watch-current'), confluence=document.querySelector('.watch-confluence');
  const tracks=[...document.querySelectorAll('.watch-stream__track')], panes=[...document.querySelectorAll('.watch-windows i')];
  const reduce=matchMedia('(prefers-reduced-motion: reduce)');
  const progress=el=>Math.max(0,Math.min(1,-el.getBoundingClientRect().top/Math.max(1,el.offsetHeight-innerHeight)));
  let queued=false;
  function draw(){queued=false;if(reduce.matches)return;const p=progress(current), q=Math.min(1,progress(confluence)*1.55);tracks.forEach((el,i)=>{const travel=Math.min(innerWidth*.32,Math.max(0,el.scrollWidth-innerWidth));el.style.setProperty('--flow',`${-travel*(i%2?1-p:p)}px`)});panes.forEach((el,i)=>{el.style.setProperty('--wx',`${(i-1.5)*innerWidth*.028*(1-q)}px`);el.style.setProperty('--wy',`${[1,-1,-.55,.7][i]*innerHeight*.065*(1-q)}px`)});}
  function schedule(){if(!queued){queued=true;requestAnimationFrame(draw)}}
  addEventListener('scroll',schedule,{passive:true});addEventListener('resize',schedule);reduce.addEventListener('change',schedule);draw();
  const frame=document.querySelector('.watch-film iframe'), button=document.querySelector('[data-film-toggle]');let paused=reduce.matches;
  function notify(){frame.contentWindow?.postMessage({type:'watch-cover-playback',paused},location.origin);button.setAttribute('aria-pressed',String(paused));button.textContent=paused?'Play film · 播放':'Pause film · 暫停';}
  button.addEventListener('click',()=>{paused=!paused;notify()});frame.addEventListener('load',notify);
  new IntersectionObserver(([entry])=>frame.contentWindow?.postMessage({type:'watch-cover-playback',paused:paused||!entry.isIntersecting},location.origin),{threshold:.05}).observe(document.querySelector('.watch-cover'));
})();
