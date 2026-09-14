(()=>{
  const SCHEMA='dore.bible-media-graph.v0';
  const MOMENT_SCHEMA='dore.bible-media-moment.v1';
  const JOURNEY_MOMENT_SCHEMA='dore.bible-journey-moment.v0';
  const MATCH_TYPES=new Set(['event','place','theme']);
  const URLS={resources:'data/video-resource.v0.json',moments:'data/video-moment.v0.json',coordinates:'data/bible-media-coordinate.v0.json',journeys:'data/bible-journey.v0.json',journeyMoments:'data/bible-journey-moment.v0.json'};
  const special=()=>window.ParadiseCinemaSpecialResources;
  const state={graph:null};

  const fetchJson=async url=>{
    const response=await fetch(url,{cache:'no-store'});
    if(!response.ok)throw new Error(`Cinema graph source unavailable: ${url}`);
    return response.json();
  };

  const normalize=value=>String(value||'').trim().toLowerCase();
  const scriptureBook=value=>normalize(value).split(/[\s.:]/)[0];
  const stationMatchesWork=(station,work)=>{
    const c=work.coordinate?.coordinates||{};
    const textBooks=new Set((c.text||[]).filter(entry=>entry.type==='scripture').map(entry=>scriptureBook(entry.value)));
    const stationBooks=new Set((station.scripture||[]).map(scriptureBook));
    const textMatch=[...stationBooks].some(book=>textBooks.has(book));
    const worldValues=new Set((c.world||[]).map(entry=>normalize(entry.value)));
    const worldMatch=(station.world||[]).some(value=>worldValues.has(normalize(value)));
    return textMatch||worldMatch;
  };
  const stationMatchesMoment=(station,moment)=>{
    if(moment.kind!=='official-episode')return false;
    const stationWorld=new Set((station.world||[]).map(normalize));
    return (moment.anchors||[]).some(anchor=>MATCH_TYPES.has(anchor.type)&&stationWorld.has(normalize(anchor.value)));
  };

  const normalizeMoment=moment=>Object.freeze({
    ...moment,
    canonicalId:moment.workId,
    anchors:Object.freeze([...(moment.anchors||[])].map(anchor=>Object.freeze({...anchor}))),
    evidence:Object.freeze([...(moment.evidence||[])].map(item=>Object.freeze({...item}))),
    mediaCoordinate:Object.freeze({workId:moment.workId,startMs:moment.startMs,endMs:moment.endMs})
  });

  function compile(resourcePayload,momentPayload,coordinatePayload,journeyPayload,journeyMomentPayload){
    if(resourcePayload.schema!=='holy-light.video-resource.v0'||!Array.isArray(resourcePayload.items))throw new Error('Invalid Cinema resource schema');
    if(momentPayload.schema!==MOMENT_SCHEMA||!Array.isArray(momentPayload.items))throw new Error('Invalid Cinema moment schema');
    if(coordinatePayload.schema!=='dore.bible-media-coordinate.v0'||!Array.isArray(coordinatePayload.items))throw new Error('Invalid Cinema coordinate schema');
    if(journeyPayload.schema!=='dore.bible-journey.v0'||!Array.isArray(journeyPayload.journeys))throw new Error('Invalid Cinema journey schema');
    if(journeyMomentPayload.schema!==JOURNEY_MOMENT_SCHEMA||!Array.isArray(journeyMomentPayload.items))throw new Error('Invalid Cinema journey Moment schema');

    const admitted=(special()?.filter(resourcePayload.items))||resourcePayload.items;
    const admittedIds=new Set(admitted.map(item=>item.canonicalId));
    const coordinates=coordinatePayload.items.filter(item=>admittedIds.has(item.canonicalId));
    const coordinateById=new Map(coordinates.map(item=>[item.canonicalId,item]));
    const moments=momentPayload.items.filter(item=>admittedIds.has(item.workId)).map(normalizeMoment);
    const momentById=new Map();
    const momentsByWork=new Map();
    const momentsByAnchor=new Map();

    for(const moment of moments){
      if(momentById.has(moment.momentId))throw new Error(`Duplicate Cinema moment: ${moment.momentId}`);
      momentById.set(moment.momentId,moment);
      const list=momentsByWork.get(moment.workId)||[];
      list.push(moment);
      momentsByWork.set(moment.workId,list);
      for(const anchor of moment.anchors){
        const key=`${anchor.type}:${anchor.value}`;
        const anchored=momentsByAnchor.get(key)||[];
        anchored.push(moment);
        momentsByAnchor.set(key,anchored);
      }
    }

    const works=admitted.map(resource=>{
      const coordinate=coordinateById.get(resource.canonicalId)||null;
      const workMoments=Object.freeze([...(momentsByWork.get(resource.canonicalId)||[])]);
      return Object.freeze({...resource,graphType:'work',coordinate,moments:workMoments,sources:Object.freeze([...(resource.providerSources||[])]),canonical:Object.freeze({id:resource.canonicalId,kind:'work'})});
    });
    const byId=new Map(works.map(work=>[work.canonicalId,work]));
    const collections=Object.freeze([...(coordinatePayload.collections||[])]);

    const overrideByStation=new Map();
    for(const relation of journeyMomentPayload.items){
      const moment=momentById.get(relation.momentId);
      if(!moment)throw new Error(`Journey Moment override references unknown Moment: ${relation.momentId}`);
      if(moment.kind!=='official-episode')throw new Error(`Journey exact override requires official episode Moment: ${relation.momentId}`);
      const key=`${relation.journeyId}:${relation.stationId}`;
      const list=overrideByStation.get(key)||[];
      list.push(Object.freeze({...relation,moment}));
      overrideByStation.set(key,list);
    }

    const journeys=Object.freeze(journeyPayload.journeys.map(journey=>Object.freeze({...journey,stations:Object.freeze([...journey.stations].sort((a,b)=>a.order-b.order).map(station=>{
      const relatedWorks=Object.freeze(works.filter(work=>stationMatchesWork(station,work)));
      const derived=Object.freeze(moments.filter(moment=>stationMatchesMoment(station,moment)));
      const override=overrideByStation.get(`${journey.journeyId}:${station.stationId}`)||[];
      const exactMoments=Object.freeze(override.length?override.map(item=>item.moment):derived);
      const exactSource=override.length?'editorial-override':(derived.length?'biblical-anchor':'none');
      const mediaState=exactMoments.length?'exact':(relatedWorks.length?'available':'unmapped');
      return Object.freeze({...station,relatedWorks,exactMoments,exactSource,mediaState});
    }))})));
    const journeyById=new Map(journeys.map(journey=>[journey.journeyId,journey]));

    const queryMoments=({type=null,value=null,workId=null}={})=>moments.filter(moment=>{
      if(workId&&moment.workId!==workId)return false;
      if(!type&&!value)return true;
      return moment.anchors.some(anchor=>(!type||anchor.type===type)&&(!value||anchor.value===value));
    });
    const deepLink=momentId=>{
      const moment=momentById.get(momentId);
      if(!moment)return null;
      const url=new URL(window.location.href);
      url.searchParams.set('moment',momentId);
      url.hash='cinema-library';
      return url.toString();
    };

    return Object.freeze({
      schema:SCHEMA,momentSchema:MOMENT_SCHEMA,journeyMomentSchema:JOURNEY_MOMENT_SCHEMA,
      works:Object.freeze(works),moments:Object.freeze(moments),coordinates:Object.freeze(coordinates),collections,journeys,
      get(canonicalId){return byId.get(canonicalId)||null;},
      moment(momentId){return momentById.get(momentId)||null;},
      coordinate(canonicalId){return coordinateById.get(canonicalId)||null;},
      momentsFor(canonicalId){return byId.get(canonicalId)?.moments||Object.freeze([]);},
      queryMoments,
      momentsForAnchor(type,value){return Object.freeze([...(momentsByAnchor.get(`${type}:${value}`)||[])]);},
      deepLink,
      journey(journeyId){return journeyById.get(journeyId)||null;},
      queryCoordinate(type,value){return works.filter(work=>{const c=work.coordinate?.coordinates||{};return [...(c.text||[]),...(c.world||[])].some(entry=>entry.type===type&&entry.value===value);});},
      queryStation(journeyId,stationId){const journey=journeyById.get(journeyId);return journey?.stations.find(station=>station.stationId===stationId)||null;}
    });
  }

  const ready=Promise.all([fetchJson(URLS.resources),fetchJson(URLS.moments),fetchJson(URLS.coordinates),fetchJson(URLS.journeys),fetchJson(URLS.journeyMoments)])
    .then(parts=>{
      state.graph=compile(...parts);
      document.documentElement.dataset.cinemaGraphSchema='v0';
      document.documentElement.dataset.cinemaMomentSchema='v1';
      document.documentElement.dataset.cinemaJourneyDerivation='graph-biblical-anchor-v2';
      document.documentElement.dataset.cinemaGraphWorks=String(state.graph.works.length);
      document.documentElement.dataset.cinemaGraphMoments=String(state.graph.moments.length);
      document.documentElement.dataset.cinemaGraphJourneys=String(state.graph.journeys.length);
      return state.graph;
    })
    .catch(error=>{document.documentElement.dataset.cinemaGraphError='load';throw error;});

  window.ParadiseCinemaGraph=Object.freeze({schema:SCHEMA,ready,current(){return state.graph;},get(canonicalId){return state.graph?.get(canonicalId)||null;},moment(momentId){return state.graph?.moment(momentId)||null;}});
})();
