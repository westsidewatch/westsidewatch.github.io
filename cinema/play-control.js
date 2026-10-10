(()=>{
  const selector='.living-poster__play-mark';
  const style=document.createElement('style');
  style.textContent=`
    .living-poster__play-mark{cursor:pointer;user-select:none;pointer-events:auto}
    .living-poster__play-mark:hover,.living-poster__play-mark:focus-visible{transform:translate(-50%,-50%) scale(1.12);background:rgba(206,189,116,.28);opacity:1;outline:2px solid rgba(240,234,220,.9);outline-offset:5px}
    .living-poster__poster{cursor:pointer}
  `;
  document.head.appendChild(style);
  const enhance=()=>{
    document.querySelectorAll(selector).forEach(control=>{
      if(control.dataset.playControlReady==='true')return;
      control.dataset.playControlReady='true';
      control.setAttribute('role','button');
      control.setAttribute('tabindex','0');
      control.setAttribute('aria-label','在此播放 JESUS');
      control.setAttribute('title','在此播放 JESUS');
    });
  };
  const trigger=control=>{
    const shell=control.closest('.living-poster');
    const watch=shell?.querySelector('[data-action="watch"]');
    if(watch&&!shell.classList.contains('is-playing'))watch.click();
  };
  document.addEventListener('click',event=>{
    const control=event.target.closest?.(selector);
    if(control){event.preventDefault();trigger(control);return;}
    const poster=event.target.closest?.('.living-poster__poster');
    if(poster){
      // The poster's own keyboard/click handler already delegates to watch.
      // Do not intercept it here: synthetic clicks on the nested control can double-trigger playback.
      if(poster.dataset.previewReady==='true')return;
      const controlInPoster=poster.querySelector(selector);
      if(controlInPoster){event.preventDefault();trigger(controlInPoster);}
    }
  });
  document.addEventListener('keydown',event=>{
    const control=event.target.closest?.(selector);
    if(control&&(event.key==='Enter'||event.key===' ')){
      event.preventDefault();
      trigger(control);
    }
  });
  new MutationObserver(enhance).observe(document.documentElement,{childList:true,subtree:true});
  enhance();
})();
