(() => {
  'use strict';
  const people=[['david-pawson','大衛鮑森'],['jiang-xiuqin','江秀琴'],['derek-prince','葉光明'],['watchman-nee','倪柝聲'],['kang-lai-chang','康來昌'],['stephen-tong','唐崇榮'],['kou-shao-en','寇紹恩'],['rick-warren','華理克'],['tong-liu','劉彤'],['jerry-lai','賴若瀚'],['yu-hong-jie','于宏潔'],['huang-shuhua','黃淑華']];
  const jiangTopics=[
    ['內在生活','jiang-xiuqin-inner-life-45','45 篇'],
    ['讚美','jiang-xiuqin-goodtv-praise',''],
    ['進入神的安息美地','jiang-xiuqin-goodtv-rest',''],
    ['慕主先鋒信息','jiang-xiuqin-goodtv-forerunner-message',''],
    ['內在生活饗宴','jiang-xiuqin-goodtv-inner-life-feast',''],
    ['道在人間','jiang-xiuqin-goodtv-good-message','']
  ];
  const speakerStage=document.querySelector('#olive-speakers');
  const topicStage=document.querySelector('#olive-series');
  const q=new URLSearchParams(location.search);
  const selectedPerson=q.get('person');
  const selectedTopic=q.get('topic');
  let doreCompositions=new Map();
  const recordsOf=p=>Array.isArray(p)?p:Array.isArray(p?.records)?p.records:Array.isArray(p?.items)?p.items:Array.isArray(p?.resources)?p.resources:[];

  function linkCard(cls,title,meta,href){
    const a=document.createElement('a'); a.className=cls; a.href=href;
    if(cls==='speaker-card'){const slug=new URL(href,location.origin).searchParams.get('person');const composition=doreCompositions.get(slug);a.dataset.doreSurface='speaker-card';a.dataset.doreSpeaker=slug||'';if(composition?.family)a.dataset.doreFamily=composition.family;if(composition?.geometry?.type){const [x,y,w,h]=composition.geometry.type;a.style.setProperty('--dore-type-x',x+'%');a.style.setProperty('--dore-type-y',y+'%');a.style.setProperty('--dore-type-w',w+'%');a.style.setProperty('--dore-type-h',h+'%');a.dataset.doreGeometry='runtime';}if(composition?.geometry?.image){const [x,y,w,h]=composition.geometry.image;a.style.setProperty('--dore-image-x',x+'%');a.style.setProperty('--dore-image-y',y+'%');a.style.setProperty('--dore-image-w',w+'%');a.style.setProperty('--dore-image-h',h+'%');a.dataset.doreImage='unbound';}a.dataset.doreIdentitySynthesis='false';if(slug===selectedPerson)a.setAttribute('aria-current','true');}
    a.innerHTML=`<h3>${title}</h3><p>${meta||'進入'} <b aria-hidden="true">↗</b></p>`; return a;
  }
  async function renderPeople(){
    speakerStage.replaceChildren();
    for(const [slug,name] of people){
      let p={}; try{if(window.WestsideResources) p=await window.WestsideResources.index('by-speaker','speaker:'+slug)}catch(_){}
      const n=recordsOf(p).length||p.itemCount||0;
      speakerStage.append(linkCard('speaker-card',name,n?n+' 篇':'進入','/olive/?person='+slug));
    }
  }
  async function renderJiangTopics(){
    topicStage.replaceChildren();
    for(const [name,key,fallback] of jiangTopics) topicStage.append(linkCard('series-card',name,fallback,'/olive/?person=jiang-xiuqin&topic='+key));
  }
  async function renderTopic(key){
    topicStage.replaceChildren();
    let payload={}; try{if(window.WestsideResources) payload=await window.WestsideResources.index('by-series','series:'+key.replace(/-/g,':'))}catch(_){}
    let rows=recordsOf(payload);
    if(!rows.length && key==='jiang-xiuqin-goodtv-good-message') rows=[
      {title:'興起發光 迎接復興浪潮',url:'https://www.youtube.com/watch?v=4l-MLiv3Kto'},
      {title:'承受美地為業的祕訣',url:'https://www.youtube.com/watch?v=SeWck245iSE'},
      {title:'追求認識神',url:'https://www.youtube.com/watch?v=nelt0FmxwiA'}
    ];
    if(!rows.length){ await renderJiangTopics(); return; }
    for(const r of rows){
      const title=r.title||r.name||r.id||'講道';
      const href=r.url||r.sourcePointer||r.providerSources?.[0]?.url||'#';
      topicStage.append(linkCard('series-card',title,'觀看',href));
    }
  }
  async function init(){
    try{const r=await fetch('/dore-design/runtime/olive-speaker-compositions.v1.json',{cache:'no-cache'});if(r.ok){const d=await r.json();doreCompositions=new Map((d.records||[]).map(x=>[x.speaker,x]));}}catch(_){}
    await renderPeople();
    if(selectedPerson==='jiang-xiuqin'){
      if(selectedTopic) await renderTopic(selectedTopic); else await renderJiangTopics();
    } else {
      topicStage.replaceChildren();
    }
  }
  init();
})();
