(()=>{
  'use strict';

  const CONTRACT=Object.freeze({
    schema:'one.visual-surface-runtime.v1',
    consumer:'dore.visual-surface-consumer.v1',
    product:'one',
  });

  const attach=()=>{
    const consumer=window.DoreVisualSurfaceConsumer;
    if(!consumer?.attachOne)return false;
    const attached=consumer.attachOne(document);
    if(attached){
      document.documentElement.dataset.oneSurfaceRuntime=CONTRACT.schema;
      document.documentElement.dataset.oneSurfaceConsumer=consumer.CONTRACT?.schema||CONTRACT.consumer;
    }
    return attached;
  };

  const loadConsumer=()=>new Promise((resolve,reject)=>{
    if(window.DoreVisualSurfaceConsumer){resolve(window.DoreVisualSurfaceConsumer);return}
    const existing=[...document.scripts].find(script=>script.src.includes('/js/dore-visual-surface-consumer.js'));
    if(existing){existing.addEventListener('load',()=>resolve(window.DoreVisualSurfaceConsumer),{once:true});existing.addEventListener('error',reject,{once:true});return}
    const script=document.createElement('script');
    script.src='/js/dore-visual-surface-consumer.js?v=20260911-cut08';
    script.onload=()=>resolve(window.DoreVisualSurfaceConsumer);
    script.onerror=reject;
    document.body.append(script);
  });

  loadConsumer().then(()=>attach()).catch(error=>console.warn('[ONE Surface Runtime]',error));
  window.ONE_SURFACE_RUNTIME=Object.freeze({CONTRACT,attach});
})();
