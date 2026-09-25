export function mountOrbitCamera(stage, city){
  stage.classList.add('j3k-oblique-view');
  const scene=document.createElement('div');
  scene.className='j3k-orbit-scene';
  city.parentNode.insertBefore(scene,city);
  scene.append(city);
  let yaw=-24,pitch=56,zoom=1,dragging=false,lastX=0,lastY=0,resumeAt=0;
  const apply=()=>{
    scene.style.setProperty('--j3k-yaw',`${yaw}deg`);
    scene.style.setProperty('--j3k-pitch',`${pitch}deg`);
    scene.style.setProperty('--j3k-zoom',zoom);
  };
  apply();
  stage.addEventListener('pointerdown',e=>{dragging=true;lastX=e.clientX;lastY=e.clientY;resumeAt=performance.now()+3500;stage.setPointerCapture?.(e.pointerId)});
  stage.addEventListener('pointermove',e=>{if(!dragging)return;const dx=e.clientX-lastX,dy=e.clientY-lastY;lastX=e.clientX;lastY=e.clientY;yaw+=dx*.28;pitch=Math.max(38,Math.min(68,pitch-dy*.16));apply()});
  const release=()=>{dragging=false;resumeAt=performance.now()+3500};
  stage.addEventListener('pointerup',release);stage.addEventListener('pointercancel',release);
  stage.addEventListener('wheel',e=>{e.preventDefault();zoom=Math.max(.78,Math.min(1.42,zoom-e.deltaY*.0007));resumeAt=performance.now()+3500;apply()},{passive:false});
  let last=performance.now();
  function orbit(now){const dt=Math.min(.05,(now-last)/1000);last=now;if(!dragging&&now>resumeAt){yaw+=dt*3.2;apply()}requestAnimationFrame(orbit)}
  requestAnimationFrame(orbit);
  return {setYaw(v){yaw=v;apply()},setPitch(v){pitch=Math.max(38,Math.min(68,v));apply()}};
}
