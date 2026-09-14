(()=>{
  const params=new URL(window.location.href).searchParams;
  const eventId=params.get('event');
  if(!eventId)return;
  window.ParadiseCinemaGraph?.ready.then(graph=>{
    const event=graph.event(eventId);
    if(!event)return;
    const exact=graph.momentsForEvent(event.eventId).filter(moment=>moment.kind==='official-episode');
    if(!exact.length){document.documentElement.dataset.cinemaEventEntry='no-exact-moment';return;}
    const target=graph.deepLink(exact[0].momentId);
    if(!target)return;
    document.documentElement.dataset.cinemaEventEntry='canonical-event';
    window.location.replace(target);
  }).catch(()=>{document.documentElement.dataset.cinemaEventEntry='error';});
})();
