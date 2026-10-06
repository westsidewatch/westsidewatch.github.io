(() => {
  'use strict';

  const speakers = [
    ['speaker:david-pawson','大衛鮑森'],['speaker:jiang-xiuqin','江秀琴'],['speaker:derek-prince','葉光明'],
    ['speaker:watchman-nee','倪柝聲'],['speaker:kang-lai-chang','康來昌'],['speaker:stephen-tong','唐崇榮'],
    ['speaker:kou-shao-en','寇紹恩'],['speaker:rick-warren','華理克'],['speaker:tong-liu','劉彤'],
    ['speaker:jerry-lai','賴若瀚'],['speaker:yu-hong-jie','于宏潔'],['speaker:huang-shuhua','黃淑華']
  ];
  const speakerStage=document.querySelector('#olive-speakers');
  const seriesStage=document.querySelector('#olive-series');
  const slug=id=>id.replace(/^speaker:/,'').replace(/^series:/,'').replace(/:/g,'-');
  const recordsOf=p=>Array.isArray(p)?p:Array.isArray(p?.records)?p.records:Array.isArray(p?.items)?p.items:Array.isArray(p?.resources)?p.resources:[];
  const countOf=p=>recordsOf(p).length || p?.itemCount || (Array.isArray(p?.series)?p.series.length:0);

  function speakerCard(id,name,payload){
    const a=document.createElement('a');
    a.className='speaker-card';
    a.href='/olive/?speaker='+encodeURIComponent(slug(id));
    a.innerHTML=`<p class="olive-eyebrow">SPEAKER</p><h3>${name}</h3><p>${countOf(payload)} 項已索引內容 <b aria-hidden="true">↗</b></p>`;
    return a;
  }

  async function loadSpeakers(){
    if(!speakerStage) return;
    speakerStage.replaceChildren();
    for(const [id,name] of speakers){
      let payload={};
      try{ payload=await window.WestsideResources.index('by-speaker',id); }catch(_){}
      speakerStage.append(speakerCard(id,name,payload));
    }
  }

  async function loadSeries(){
    if(!seriesStage) return;
    const specs=[
      ['series:jiang-xiuqin:inner-life-45','SERIES','江秀琴 · 內在生活','45 集系列'],
      ['series:jiang-xiuqin:goodtv','GOOD TV','江秀琴 · GOOD TV','GOOD TV 系列館藏']
    ];
    seriesStage.replaceChildren();
    for(const [id,label,name,fallback] of specs){
      let payload={};
      try{ payload=await window.WestsideResources.index('by-series',id); }catch(_){}
      const a=document.createElement('a');
      a.className='series-card';
      a.href='/olive/?series='+encodeURIComponent(slug(id));
      const n=countOf(payload);
      a.innerHTML=`<p class="olive-eyebrow">${label}</p><h3>${name}</h3><p>${n?n+' 項已索引內容':fallback} <b aria-hidden="true">↗</b></p>`;
      seriesStage.append(a);
    }
  }
  if(window.WestsideResources) Promise.allSettled([loadSpeakers(),loadSeries()]);
})();
