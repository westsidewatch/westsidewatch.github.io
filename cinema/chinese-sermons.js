(()=>{
  const grid=document.querySelector('#chinese-sermons-grid');
  if(!grid)return;
  const FALLBACK_URLS={
    'speaker:david-pawson':'https://www.youtube.com/channel/UCKkUuEC1rNnuQ1yZ-RCAHPQ',
    'speaker:jiang-xiuqin':'https://www.youtube.com/watch?v=pGeImHgQ2xo&list=PLZ76syLBohalXwTGd3yZfUsLVh0wezSst'
  };
  const LABELS={
    'whole-channel-admitted':'完整頻道',
    'whole-source-family-admitted':'完整中文頻道',
    'whole-series-family-admitted':'完整系列',
    'bulk-publication-families-admitted':'中文作品集',
    'teacher-corpus-admitted-from-official-channel':'講員館藏',
    'teacher-series-family-admitted':'完整系列族'
  };
  const preferredUrl=item=>item.url||FALLBACK_URLS[item.speakerId]||item.verifiedSourceFamilies?.find(source=>source.url)?.url||null;
  const render=item=>{
    const card=document.createElement('article');card.className='resource-card chinese-sermon-card';
    const meta=document.createElement('div');meta.className='resource-meta';meta.textContent=`中文講道 · ${LABELS[item.status]||'館藏'}`;
    const title=document.createElement('h4');title.textContent=item.speaker||item.sourceLabel||'中文講道';
    const series=document.createElement('p');series.textContent=item.sourceLabel||item.verifiedSourceFamilies?.[0]?.label||'';
    const topics=document.createElement('div');topics.className='resource-topics';
    const families=item.verifiedSeriesFamilies||item.knownSeriesFamilies||[];topics.textContent=families.slice(0,5).join(' · ');
    const url=preferredUrl(item);const action=document.createElement(url?'a':'span');action.className='resource-action';action.textContent=url?'進入館藏來源':'館藏整理中';if(url){action.href=url;action.target='_blank';action.rel='noopener noreferrer';}
    card.append(meta,title,series,topics,action);return card;
  };
  fetch('data/chinese-sermons-bulk-intake.v1.json',{cache:'no-store'}).then(response=>{if(!response.ok)throw new Error(`HTTP ${response.status}`);return response.json();}).then(payload=>{
    const admitted=(payload.intakes||[]).filter(item=>item.status&&item.status!=='candidate');
    grid.replaceChildren(...admitted.map(render));
    document.documentElement.dataset.cinemaChineseSermons=String(admitted.length);
    document.documentElement.dataset.cinemaChineseSermonsLive='true';
  }).catch(()=>{grid.innerHTML='<p class="resource-card">中文講道館藏暫時無法載入。</p>';document.documentElement.dataset.cinemaChineseSermonsLive='error';});
})();