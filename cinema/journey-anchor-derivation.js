(()=>{
  const MATCH_TYPES=new Set(['event','place','theme']);
  const normalize=value=>String(value||'').trim().toLowerCase();

  function relationFor(journey,station,moment){
    if(moment.kind!=='official-episode')return null;
    const stationWorld=new Set((station.world||[]).map(normalize));
    const anchors=(moment.anchors||[]).filter(anchor=>MATCH_TYPES.has(anchor.type)&&stationWorld.has(normalize(anchor.value)));
    if(!anchors.length)return null;
    return Object.freeze({journeyId:journey.journeyId,stationId:station.stationId,momentId:moment.momentId,relation:'depicts',derived:true,basis:Object.freeze({kind:'biblical-anchor-derivation',anchors:Object.freeze(anchors.map(anchor=>Object.freeze({type:anchor.type,value:anchor.value}))),scripture:(moment.anchors||[]).find(anchor=>anchor.type==='scripture')?.value||null}),moment});
  }

  function relationsForStation(graph,journey,station){
    return Object.freeze(graph.moments.map(moment=>relationFor(journey,station,moment)).filter(Boolean));
  }

  function renderDerived(graph){
    const journey=graph.journey('cinema:journey:creation-to-new-creation');
    if(!journey)return;
    let count=0;
    for(const station of journey.stations){
      const relations=relationsForStation(graph,journey,station);
      if(!relations.length)continue;
      const host=document.querySelector(`.journey-station[data-station="${station.stationId}"] .journey-media`);
      if(!host)continue;
      host.replaceChildren();
      const label=document.createElement('small');label.textContent=`精確影像 ${relations.length}`;host.appendChild(label);
      for(const relation of relations.slice(0,4)){
        const moment=relation.moment;
        const link=document.createElement('a');
        link.className='journey-resource journey-moment';
        link.dataset.momentId=moment.momentId;
        link.dataset.derived='biblical-anchor-v1';
        link.href=graph.deepLink(moment.momentId)||'#cinema-library';
        link.textContent=moment.label;
        link.setAttribute('aria-label',`精確影像：${moment.label}`);
        host.appendChild(link);
      }
      count+=relations.length;
    }
    document.documentElement.dataset.cinemaJourneyDerivation='biblical-anchor-v1';
    document.documentElement.dataset.cinemaJourneyDerivedExact=String(count);
  }

  const layer=Object.freeze({schema:'dore.bible-journey-anchor-derivation.v1',relationFor,relationsForStation});
  window.ParadiseCinemaJourneyAnchors=layer;
  window.ParadiseCinemaGraph?.ready.then(graph=>setTimeout(()=>renderDerived(graph),0));
})();
