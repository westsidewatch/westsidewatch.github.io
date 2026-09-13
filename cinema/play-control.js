(()=>{
  const selector='.living-poster__play-mark';
  const enhance=()=>{
    document.querySelectorAll(selector).forEach(control=>{
      if(control.dataset.playControlReady==='true')return;
      control.dataset.playControlReady='true';
      control.setAttribute('role','button');
      control.setAttribute('tabindex','0');
      control.setAttribute('aria-label','在此播放 JESUS');
    });
  };
  const trigger=control=>{
    const shell=control.closest('.living-poster');
    const watch=shell?.querySelector('[data-action="watch"]');
    if(watch&&!shell.classList.contains('is-playing'))watch.click();
  };
  document.addEventListener('click',event=>{
    const control=event.target.closest?.(selector);
    if(control){event.preventDefault();trigger(control);}
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
