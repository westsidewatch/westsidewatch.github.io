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
    a.innerHTML=`<h3>${name}</h3><p>${countOf(payload) ? countOf(payload)+" 篇" : "進入"} <b aria-hidden="true">↗</b></p>`;
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
    const topics=[
      ['內在生活','series:jiang-xiuqin:inner-life-45','45 篇'],
      ['讚美','series:jiang-xiuqin:goodtv:praise','進入'],
      ['進入神的安息美地','series:jiang-xiuqin:goodtv:rest','進入'],
      ['慕主先鋒信息','series:jiang-xiuqin:goodtv:forerunner-message','進入'],
      ['內在生活饗宴','series:jiang-xiuqin:goodtv:inner-life-feast','進入'],
      ['道在人間','series:jiang-xiuqin:goodtv:good-message','進入']
    ];
    seriesStage.replaceChildren();
    for(const [name,id,fallback] of topics){
      const a=document.createElement('a');
      a.className='series-card';
      a.href='/olive/?topic='+encodeURIComponent(slug(id));
      a.innerHTML=`<h3>${name}</h3><p>${fallback} <b aria-hidden="true">↗</b></p>`;
      seriesStage.append(a);
    }
  }
  if(window.WestsideResources) Promise.allSettled([loadSpeakers(),loadSeries()]);
})();
