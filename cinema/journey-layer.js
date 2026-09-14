(()=>{
  const JOURNEY_ID='cinema:journey:creation-to-new-creation';
  const host=document.querySelector('#cinema-journey');
  if(!host||!window.ParadiseCinemaGraph)return;

  const scriptureLabel=station=>(station.scripture||[]).join(' · ');
  const resourceButton=work=>{
    const button=document.createElement('button');
    button.type='button';
    button.className='journey-resource';
    button.dataset.canonicalId=work.canonicalId;
    button.textContent=work.title;
    button.addEventListener('click',()=>document.querySelector(`.resource-card[data-canonical-id="${CSS.escape(work.canonicalId)}"]`)?.scrollIntoView({behavior:'smooth',block:'center'}));
    return button;
  };
  const momentLink=(graph,moment)=>{
    const link=document.createElement('a');
    link.className='journey-resource journey-moment';
    link.dataset.momentId=moment.momentId;
    link.href=graph.deepLink(moment.momentId)||'#cinema-library';
    link.textContent=moment.label;
    link.setAttribute('aria-label',`精確影像：${moment.label}`);
    return link;
  };

  function render(graph){
    const journey=graph.journey(JOURNEY_ID);if(!journey)return;
    const intro=document.createElement('div');intro.className='journey-intro';intro.innerHTML=`<p>FROM CREATION TO NEW CREATION</p><h3>${journey.title}</h3><small>不是片單，而是一條聖經世界的路。已有可靠影像座標時才顯示資源；沒有時保留空白，不虛構。</small>`;
    const rail=document.createElement('ol');rail.className='journey-rail';
    for(const station of journey.stations){
      const item=document.createElement('li');item.className='journey-station';item.dataset.station=station.stationId;item.dataset.mediaState=station.mediaState;
      if(station.terminal)item.dataset.terminal='true';
      const marker=document.createElement('span');marker.className='journey-marker';marker.textContent=String(station.order).padStart(2,'0');
      const copy=document.createElement('div');copy.className='journey-copy';
      const title=document.createElement('strong');title.textContent=station.label;
      const scripture=document.createElement('span');scripture.className='journey-scripture';scripture.textContent=scriptureLabel(station);
      const media=document.createElement('div');media.className='journey-media';
      if(station.exactMoments?.length){
        const count=document.createElement('small');count.textContent=`精確影像 ${station.exactMoments.length}`;media.appendChild(count);
        station.exactMoments.slice(0,4).forEach(moment=>media.appendChild(momentLink(graph,moment)));
      }else if(station.relatedWorks.length){
        const count=document.createElement('small');count.textContent=`相關影像 ${station.relatedWorks.length}`;media.appendChild(count);
        station.relatedWorks.slice(0,4).forEach(work=>media.appendChild(resourceButton(work)));
      }else{
        const empty=document.createElement('small');empty.textContent=station.terminal?'終點已建立；影像座標尚待可靠來源。':'影像座標尚未建立';media.appendChild(empty);
      }
      copy.append(title,scripture,media);item.append(marker,copy);rail.appendChild(item);
    }
    host.replaceChildren(intro,rail);
    document.documentElement.dataset.cinemaJourney='creation-to-new-creation-v1';
    document.documentElement.dataset.cinemaJourneyStations=String(journey.stations.length);
    document.documentElement.dataset.cinemaJourneyExact=String(journey.stations.reduce((sum,station)=>sum+(station.exactMoments?.length||0),0));
  }

  window.ParadiseCinemaGraph.ready.then(render).catch(()=>{document.documentElement.dataset.cinemaJourneyError='load';});
})();