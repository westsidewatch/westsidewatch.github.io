(() => {
  'use strict';
  // Birth chronology: dated records first; unknowns retain prior relative order.
  // User-provided approximate ranges use a provisional year key, not a proven exact birth order.
  // Year-only records do not imply a known month/day. Do not infer birth years from age or graduation.
  const speakerBirth = {
    'watchman-nee': {year:1903, date:'1903-11-04', source:'https://en.wikipedia.org/wiki/Watchman_Nee'},
    'derek-prince': {year:1915, date:'1915-08-14', source:'https://www.derekprince.com/en-ca/about/faq'},
    'david-pawson': {year:1930, date:'1930-02-25', source:'https://www.wikidata.org/wiki/Q2432479'},
    'stephen-tong': {year:1940, date:null, source:'https://goodtvnews.goodtv.tv/goodtvnews/2019taiwan10/'},
    'kang-lai-chang': {year:1949, date:null, source:'https://www.lynchburgconference.org/bio_kang_laichang'},
    'rick-warren': {year:1954, date:'1954-01-28', source:'https://en.wikipedia.org/wiki/Rick_Warren'},
    'kou-shao-en': {year:1957, date:'1957-08-19', source:'https://rockpedia.org/pastors/kou-shaoen'},
    'jiang-xiuqin': {year:1954, date:null, precision:'year', source:'user-provided', label:'1954年'},
    'tong-liu': {year:1952, date:null, birthRange:[1952,1954], precision:'approximate-range', source:'user-provided', label:'約1952–1954年'},
    'jerry-lai': {year:1951, date:null, birthRange:[1951,1952], precision:'approximate-range', source:'user-provided', label:'1951或1952年，香港'},
    'yu-hong-jie': {year:1955, date:null, precision:'approximate-year', source:'user-provided', label:'約1955年'},
    'huang-shuhua': {year:1944, date:null, birthRange:[1943,1944], precision:'approximate-range', source:'user-provided', label:'約1944年或1943年底'}
  };
  const people=[['david-pawson','大衛鮑森'],['jiang-xiuqin','江秀琴'],['derek-prince','葉光明'],['watchman-nee','倪柝聲'],['kang-lai-chang','康來昌'],['stephen-tong','唐崇榮'],['kou-shao-en','寇紹恩'],['rick-warren','華理克'],['tong-liu','劉彤'],['jerry-lai','賴若瀚'],['yu-hong-jie','于宏潔'],['huang-shuhua','黃淑華']];
  people.sort(([a],[b]) => {
    const first=speakerBirth[a], second=speakerBirth[b];
    if(first.year===null) return second.year===null ? 0 : 1;
    if(second.year===null) return -1;
    if(first.year!==second.year) return first.year-second.year;
    return first.date && second.date ? first.date.localeCompare(second.date) : 0;
  });
  // Editorial grid order approved for the existing twelve images (row-major).
  // Do not alter the shared speaker entity registry or image files.
  // Huang Shuhua remains row 2, column 2.
  const editorialOrder = [
    'david-pawson', 'jiang-xiuqin', 'derek-prince',
    'watchman-nee', 'huang-shuhua', 'tong-liu',
    'jerry-lai', 'yu-hong-jie', 'stephen-tong',
    'rick-warren', 'kang-lai-chang', 'kou-shao-en'
  ];
  people.sort(([a],[b]) => editorialOrder.indexOf(a)-editorialOrder.indexOf(b));
  // English display names belong to the editorial presentation layer, not image assets.
  const speakerEnglish = {
    'david-pawson': 'David Pawson',
    'jiang-xiuqin': 'Grace Chiang',
    'derek-prince': 'Derek Prince',
    'watchman-nee': 'Watchman Nee',
    'huang-shuhua': 'Huang Shuhua',
    'tong-liu': 'Tong Liu',
    'jerry-lai': 'Jerry Lai',
    'yu-hong-jie': 'Yu Hongjie',
    'stephen-tong': 'Stephen Tong',
    'rick-warren': 'Rick Warren',
    'kang-lai-chang': 'Kang Lai-chang',
    'kou-shao-en': 'Kou Shao-en'
  };
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
  let verifiedPortraits=new Map();
  let editorialCovers=new Map();
  const validPortrait=r=>r&&r.verified===true&&r.licenseVerified===true&&r.identityVerified===true&&typeof r.url==='string'&&r.url.startsWith('/')&&!r.url.startsWith('//')&&!r.url.includes('..')&&!r.url.includes('?')&&typeof r.source==='string'&&r.source.trim()&&typeof r.license==='string'&&r.license.trim()&&typeof r.identityEvidence==='string'&&r.identityEvidence.trim();
  const recordsOf=p=>Array.isArray(p)?p:Array.isArray(p?.records)?p.records:Array.isArray(p?.items)?p.items:Array.isArray(p?.resources)?p.resources:[];

  function linkCard(cls,title,meta,href){
    const a=document.createElement('a'); a.className=cls; a.href=href;
    if(cls==='speaker-card'){const slug=/^\/olive\/(watchman-nee|jiang-xiuqin|derek-prince|tong-liu|huang-shuhua|jerry-lai|stephen-tong|kang-lai-chang|yu-hong-jie|rick-warren|kou-shao-en)\/$/.test(href)?href.split('/')[2]:new URL(href,location.origin).searchParams.get('person');const birth=speakerBirth[slug];if(birth){a.dataset.birthPrecision=birth.precision||(birth.year===null?'unknown':birth.date?'date':'year');if(birth.label)a.dataset.birthLabel=birth.label;}const composition=doreCompositions.get(slug);a.dataset.doreSurface='speaker-card';a.dataset.doreSpeaker=slug||'';a.dataset.doreIndex=String(people.findIndex(([id])=>id===slug)+1).padStart(2,'0');if(composition?.family)a.dataset.doreFamily=composition.family;if(typeof composition?.cover==='string'&&/^\/dore-design\/runtime\/olive-covers\/[a-z0-9-]+\.svg$/.test(composition.cover)){const cover=document.createElement('img');cover.className='dore-generated-cover';cover.src=composition.cover;cover.alt='';cover.loading='lazy';cover.decoding='async';cover.addEventListener('error',()=>cover.remove(),{once:true});a.append(cover);a.dataset.doreCover='generated';}if(composition?.geometry?.type){const [x,y,w,h]=composition.geometry.type;a.style.setProperty('--dore-type-x',x+'%');a.style.setProperty('--dore-type-y',y+'%');a.style.setProperty('--dore-type-w',w+'%');a.style.setProperty('--dore-type-h',h+'%');a.dataset.doreGeometry='runtime';}if(composition?.geometry?.image){const [x,y,w,h]=composition.geometry.image;a.style.setProperty('--dore-image-x',x+'%');a.style.setProperty('--dore-image-y',y+'%');a.style.setProperty('--dore-image-w',w+'%');a.style.setProperty('--dore-image-h',h+'%');a.dataset.doreImage='unbound';const portrait=verifiedPortraits.get(slug);if(validPortrait(portrait)){const img=document.createElement('img');img.className='dore-verified-portrait';img.src=portrait.url;img.alt='';img.loading='lazy';img.decoding='async';img.addEventListener('error',()=>{img.remove();a.dataset.doreImage='unbound';},{once:true});a.append(img);a.dataset.doreImage='verified';}}a.dataset.doreIdentitySynthesis='false';if(slug===selectedPerson)a.setAttribute('aria-current','true');}
    if(cls==='speaker-card'){
      const slug=a.dataset.doreSpeaker, editorial=editorialCovers.get(slug);
      if(editorial && /^\/images\/olive\/[a-z0-9-]+\.png$/.test(editorial.url)){
        const img=document.createElement('img');
        img.className='dore-editorial-cover'; img.src=editorial.url;
        img.alt=editorial.alt||''; img.loading='lazy'; img.decoding='async';
        img.addEventListener('load',()=>{
          a.querySelector('.dore-generated-cover')?.remove();
          a.dataset.doreCover='editorial'; a.dataset.doreImage='editorial';
          a.dataset.doreIdentitySynthesis=String(editorial.identitySynthesis===true);
        },{once:true});
        img.addEventListener('error',()=>img.remove(),{once:true});
        a.append(img);
      }
    }
    if(cls==='speaker-card'){
      // One typographic unit: Chinese title / English name / entry cue.
      // Placement is handled by the Olive magazine composition layer.
      const group=document.createElement('div');
      group.className='olive-speaker-typegroup';
      const chinese=document.createElement('h3');
      chinese.textContent=title;
      group.append(chinese);
      const english=speakerEnglish[a.dataset.doreSpeaker];
      if(english){
        const label=document.createElement('span');
        label.className='olive-speaker-english';
        label.lang='en';
        label.textContent=english;
        group.append(label);
      }
      const cue=document.createElement('p');
      cue.className='olive-speaker-entry';
      cue.append(document.createTextNode(meta||'進入'));
      const arrow=document.createElement('b');
      arrow.setAttribute('aria-hidden','true');
      arrow.textContent='↗';
      cue.append(' ',arrow);
      group.append(cue);
      a.append(group);
    } else {
      a.insertAdjacentHTML('beforeend',`<h3>${title}</h3><p>${meta||'進入'} <b aria-hidden="true">↗</b></p>`);
    }
    return a;
  }
  async function renderPeople(){
    speakerStage.replaceChildren();
    for(const [slug,name] of people){
      let p={}; try{if(window.WestsideResources) p=await window.WestsideResources.index('by-speaker','speaker:'+slug)}catch(_){}
      const n=recordsOf(p).length||p.itemCount||0;
      speakerStage.append(linkCard('speaker-card',name,n?n+' 篇':'進入',['david-pawson','watchman-nee','jiang-xiuqin','derek-prince','tong-liu','huang-shuhua','jerry-lai','stephen-tong','kang-lai-chang','yu-hong-jie','rick-warren','kou-shao-en'].includes(slug)?'/olive/'+slug+'/':'/olive/?person='+slug));
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
    try{const r=await fetch('/dore-design/runtime/olive-editorial-covers.v1.json',{cache:'no-cache'});if(r.ok){const d=await r.json();editorialCovers=new Map((d.records||[]).map(x=>[x.speaker,x]));}}catch(_){}
    try{const r=await fetch('/dore-design/runtime/olive-verified-portraits.v1.json',{cache:'no-cache'});if(r.ok){const d=await r.json();verifiedPortraits=new Map((d.records||[]).filter(validPortrait).map(x=>[x.speaker,x]));}}catch(_){}
    await renderPeople();
    if(selectedPerson==='jiang-xiuqin'){
      if(selectedTopic) await renderTopic(selectedTopic); else await renderJiangTopics();
    } else {
      topicStage.replaceChildren();
    }
  }
  init();
})();
