(()=>{
  'use strict';
  const hero=document.querySelector('.product-hero');
  if(!hero)return;
  const assignment={product:'folio',role:'primary',weight:2,motion:'near-still',surface:'folio-home-hero',preset:'folio-hero'};
  const attach=()=>window.DoreVisualSurfaceConsumer?.apply(hero,assignment);
  if(window.DoreVisualSurfaceConsumer){attach();return;}
  const existing=[...document.scripts].find(script=>script.src.includes('/js/dore-visual-surface-consumer.js'));
  if(existing){existing.addEventListener('load',attach,{once:true});return;}
  const script=document.createElement('script');
  script.src='/js/dore-visual-surface-consumer.js?v=20260911-cut09';
  script.onload=attach;
  script.onerror=()=>console.warn('[DORÉ Surface Consumer] Folio bridge failed');
  document.body.append(script);
})();
