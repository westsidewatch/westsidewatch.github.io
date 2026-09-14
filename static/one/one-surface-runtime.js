(()=>{
  'use strict';

  const CONTRACT=Object.freeze({
    schema:'one.visual-surface-runtime.v2',
    consumer:'dore.visual-surface-consumer.v1',
    resourceFabric:'dore.resource-fabric.surface-manifest.v0',
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

  const loadResourceFabric=async()=>{
    const rf=await import('/js/resource-fabric-client.mjs');
    const manifest=await rf.resourceManifest();
    if(manifest?.identityAuthority!=='Dawn'||manifest?.canonicalMonolithRequired!==false)throw new Error('Resource Fabric boundary mismatch');
    window.ONE_RESOURCE_FABRIC=Object.freeze({
      manifest:rf.resourceManifest,
      work:rf.resourceWork,
      works:rf.resourceWorks,
      search:rf.resourceSearch,
      featured:rf.resourceFeatured,
    });
    document.documentElement.dataset.oneResourceFabric=`PASS:${manifest.workCount}`;
    return window.ONE_RESOURCE_FABRIC;
  };

  Promise.all([loadConsumer(),loadResourceFabric()]).then(()=>attach()).catch(error=>console.warn('[ONE Surface Runtime]',error));
  window.ONE_SURFACE_RUNTIME=Object.freeze({CONTRACT,attach,loadResourceFabric});
})();
