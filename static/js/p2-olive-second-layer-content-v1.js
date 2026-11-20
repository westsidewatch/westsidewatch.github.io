/* Content-only bridge: existing Westside Core speaker sources -> P2 inline folios.
 * No navigation or independent catalogue. All playback is on deliberate click.
 */
(()=>{'use strict';
  window.P2OliveSeries=window.P2OliveSeries||{};
  fetch('/experiments/olive-speaker-second-layer-data.json',{cache:'no-cache'})
    .then(response=>{if(!response.ok)throw Error('speaker catalogue unavailable');return response.json()})
    .then(payload=>{
      for(const [slug,speaker] of Object.entries(payload.speakers||{})){
        window.P2OliveSeries[slug]=(speaker.series||[]).map(group=>({
          titleZh:group.title,
          titleEn:'',
          indexKeys:group.keys||[],
          episodes:(group.items||[]).map(item=>({
            title:item.title,
            videoId:item.youtubeId,
            source:item.source||'YouTube',
            status:item.status||'existing'
          }))
        }));
      }
      document.documentElement.dataset.oliveCatalogue='ready';
    })
    .catch(error=>{
      document.documentElement.dataset.oliveCatalogue='unavailable';
      console.warn('[Olive catalogue]',error.message);
    });
})();
