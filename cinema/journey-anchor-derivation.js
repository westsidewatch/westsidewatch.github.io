(()=>{
  const MATCH_TYPES=new Set(['event','place','theme']);
  const normalize=value=>String(value||'').trim().toLowerCase();

  function relationFor(journey,station,moment){
    if(moment.kind!=='official-episode')return null;
    const stationWorld=new Set((station.world||[]).map(normalize));
    const anchors=(moment.anchors||[]).filter(anchor=>MATCH_TYPES.has(anchor.type)&&stationWorld.has(normalize(anchor.value)));
    if(!anchors.length)return null;
    const scripture=(moment.anchors||[]).find(anchor=>anchor.type==='scripture')?.value||null;
    return Object.freeze({
      journeyId:journey.journeyId,
      stationId:station.stationId,
      momentId:moment.momentId,
      relation:'depicts',
      derived:true,
      basis:Object.freeze({
        kind:'biblical-anchor-derivation',
        anchors:Object.freeze(anchors.map(anchor=>Object.freeze({type:anchor.type,value:anchor.value}))),
        scripture
      }),
      moment
    });
  }

  function relationsForStation(graph,journey,station){
    const overrides=(station.exactMoments||[]).map(moment=>Object.freeze({
      journeyId:journey.journeyId,
      stationId:station.stationId,
      momentId:moment.momentId,
      relation:'depicts',
      derived:false,
      basis:Object.freeze({kind:'editorial-override'}),
      moment
    }));
    if(overrides.length)return Object.freeze(overrides);
    return Object.freeze(graph.moments.map(moment=>relationFor(journey,station,moment)).filter(Boolean));
  }

  window.ParadiseCinemaJourneyAnchors=Object.freeze({
    schema:'dore.bible-journey-anchor-derivation.v1',
    relationFor,
    relationsForStation,
    momentsForStation(graph,journey,station){return Object.freeze(relationsForStation(graph,journey,station).map(item=>item.moment));}
  });
})();
