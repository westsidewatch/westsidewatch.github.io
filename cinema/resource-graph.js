(()=>{
  const SCHEMA='dore.bible-media-graph.v0';
  const URLS={resources:'data/video-resource.v0.json',moments:'data/video-moment.v0.json',coordinates:'data/bible-media-coordinate.v0.json',journeys:'data/bible-journey.v0.json'};
  const special=()=>window.ParadiseCinemaSpecialResources;
  const state={graph:null};

  const fetchJson=async url=>{
    const response=await fetch(url,{cache:'no-store'});
    if(!response.ok)throw new Error(`Cinema graph source unavailable: ${url}`);
    return response.json();
  };

  const scriptureBook=value=>String(value||'').trim().split(/[\s.:]/)[0].toLowerCase();
  const stationMatchesWork=(station,work)=>{
    const c=work.coordinate?.coordinates||{};
    const textBooks=new Set((c.text||[]).filter(entry=>entry.type==='scripture').map(entry=>scriptureBook(entry.value)));
    const stationBooks=new Set((station.scripture||[]).map(scriptureBook));
    const textMatch=[...stationBooks].some(book=>textBooks.has(book));
    const worldValues=new Set((c.world||[]).map(entry=>String(entry.value||'').toLowerCase()));
    const worldMatch=(station.world||[]).some(value=>worldValues.has(String(value).toLowerCase()));
    return textMatch||worldMatch;
  };

  function compile(resourcePayload,momentPayload,coordinatePayload,journeyPayload){
    if(resourcePayload.schema!=='holy-light.video-resource.v0'||!Array.isArray(resourcePayload.items))throw new Error('Invalid Cinema resource schema');
    if(momentPayload.schema!=='holy-light.video-moment.v0'||!Array.isArray(momentPayload.items))throw new Error('Invalid Cinema moment schema');
    if(coordinatePayload.schema!=='dore.bible-media-coordinate.v0'||!Array.isArray(coordinatePayload.items))throw new Error('Invalid Cinema coordinate schema');
    if(journeyPayload.schema!=='dore.bible-journey.v0'||!Array.isArray(journeyPayload.journeys))throw new Error('Invalid Cinema journey schema');

    const admitted=(special()?.filter(resourcePayload.items))||resourcePayload.items;
    const admittedIds=new Set(admitted.map(item=>item.canonicalId));
    const coordinates=coordinatePayload.items.filter(item=>admittedIds.has(item.canonicalId));
    const coordinateById=new Map(coordinates.map(item=>[item.canonicalId,item]));
    const moments=momentPayload.items.filter(item=>admittedIds.has(item.canonicalId));
    const momentsByWork=new Map();
    for(const moment of moments){
      const list=momentsByWork.get(moment.canonicalId)||[];
      list.push(Object.freeze({...moment,mediaCoordinate:Object.freeze({workId:moment.canonicalId,startMs:moment.startMs,endMs:moment.endMs})}));
      momentsByWork.set(moment.canonicalId,list);
    }

    const works=admitted.map(resource=>{
      const coordinate=coordinateById.get(resource.canonicalId)||null;
      const workMoments=Object.freeze([...(momentsByWork.get(resource.canonicalId)||[])]);
      return Object.freeze({...resource,graphType:'work',coordinate,moments:workMoments,sources:Object.freeze([...(resource.providerSources||[])]),canonical:Object.freeze({id:resource.canonicalId,kind:'work'})});
    });
    const byId=new Map(works.map(work=>[work.canonicalId,work]));
    const collections=Object.freeze([...(coordinatePayload.collections||[])]);
    const journeys=Object.freeze(journeyPayload.journeys.map(journey=>Object.freeze({...journey,stations:Object.freeze([...journey.stations].sort((a,b)=>a.order-b.order).map(station=>{
      const relatedWorks=Object.freeze(works.filter(work=>stationMatchesWork(station,work)));
      return Object.freeze({...station,relatedWorks,mediaState:relatedWorks.length?'available':'unmapped'});
    }))})));
    const journeyById=new Map(journeys.map(journey=>[journey.journeyId,journey]));

    return Object.freeze({
      schema:SCHEMA,
      works:Object.freeze(works),
      moments:Object.freeze(moments.flatMap(moment=>momentsByWork.get(moment.canonicalId)?.filter(candidate=>candidate.momentId===moment.momentId)||[])),
      coordinates:Object.freeze(coordinates),
      collections,
      journeys,
      get(canonicalId){return byId.get(canonicalId)||null;},
      coordinate(canonicalId){return coordinateById.get(canonicalId)||null;},
      momentsFor(canonicalId){return byId.get(canonicalId)?.moments||Object.freeze([]);},
      journey(journeyId){return journeyById.get(journeyId)||null;},
      queryCoordinate(type,value){return works.filter(work=>{const c=work.coordinate?.coordinates||{};return [...(c.text||[]),...(c.world||[])].some(entry=>entry.type===type&&entry.value===value);});},
      queryStation(journeyId,stationId){const journey=journeyById.get(journeyId);return journey?.stations.find(station=>station.stationId===stationId)||null;}
    });
  }

  const ready=Promise.all([fetchJson(URLS.resources),fetchJson(URLS.moments),fetchJson(URLS.coordinates),fetchJson(URLS.journeys)])
    .then(parts=>{
      state.graph=compile(...parts);
      document.documentElement.dataset.cinemaGraphSchema='v0';
      document.documentElement.dataset.cinemaGraphWorks=String(state.graph.works.length);
      document.documentElement.dataset.cinemaGraphMoments=String(state.graph.moments.length);
      document.documentElement.dataset.cinemaGraphJourneys=String(state.graph.journeys.length);
      return state.graph;
    })
    .catch(error=>{document.documentElement.dataset.cinemaGraphError='load';throw error;});

  window.ParadiseCinemaGraph=Object.freeze({schema:SCHEMA,ready,current(){return state.graph;},get(canonicalId){return state.graph?.get(canonicalId)||null;}});
})();