(()=>{
  const ids=new Set(['cinema:video:goodtv:holy-spirit-power-workplace-testimony']);
  window.ParadiseCinemaSpecialResources=Object.freeze({
    schema:'dore.cinema-special-resource-policy.v0',
    has(canonicalId){return ids.has(canonicalId);},
    filter(items){return Array.isArray(items)?items.filter(item=>!ids.has(item?.canonicalId)):[];},
    ids:Object.freeze([...ids])
  });
})();
