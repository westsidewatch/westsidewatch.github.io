(() => {
  'use strict';
  const root=document.querySelector('.olive-archive');
  if(!root)return;
  const rail=root.querySelector('.olive-speaker-rail');
  const cards=[...(rail?.querySelectorAll('.olive-speaker-card:not(.olive-speaker-card--clone)')||[])];
  // The gallery's editorial title is visible; IDs remain internal navigation anchors.
  const home=root.querySelector('.olive-home-stage');
  if(home)home.id='olive-speaker-experience';
  // The second layer is a readable gallery of the twelve approved editorial posters,
  // not a placeholder video rectangle or a repeated list of tiny names.
  const theater=document.createElement('section');
  theater.className='olive-journey-section olive-journey-theater';
  theater.id='olive-adullam';
  theater.setAttribute('aria-label','亞杜蘭洞 · 十二講員與當期論道');
  theater.innerHTML='<header class="olive-adullam-heading"><span class="olive-adullam-heading__en" lang="en">ADULLAM</span><h2 class="olive-adullam-heading__zh">亞杜蘭洞</h2></header><div class="olive-poster-gallery" aria-label="十二講員海報"></div><div class="olive-issue-sermons" aria-label="當期論道推薦" data-olive-issue-sermons></div>';
  const gallery=theater.querySelector('.olive-poster-gallery');
  const speakerSlugs={'大衛鮑森':'david-pawson','江秀琴':'jiang-xiuqin','賴若瀚':'jerry-lai','劉彤':'tong-liu','葉光明':'derek-prince','倪柝聲':'watchman-nee','康來昌':'kang-lai-chang','唐崇榮':'stephen-tong','寇紹恩':'kou-shao-en','華理克':'rick-warren','于宏潔':'yu-hong-jie','黃淑華':'huang-shuhua'};
  const englishNames={'大衛鮑森':'DAVID PAWSON','江秀琴':'GRACE CHIANG','賴若瀚':'JERRY LAI','劉彤':'TONG LIU','葉光明':'DEREK PRINCE','倪柝聲':'WATCHMAN NEE','康來昌':'KANG LAI CHANG','唐崇榮':'STEPHEN TONG','寇紹恩':'KOU SHAO EN','華理克':'RICK WARREN','于宏潔':'YU HONG JIE','黃淑華':'HUANG SHUHUA'};
  const addIdentity=(card,item)=>{
    const identity=document.createElement('span');identity.className='olive-gallery-card__identity';
    const en=document.createElement('span');en.className='olive-gallery-card__identity-en';en.lang='en';en.textContent=englishNames[item.name]||item.slug.replace(/-/g,' ').toUpperCase();
    const zh=document.createElement('span');zh.className='olive-gallery-card__identity-zh';zh.lang='zh-Hant';zh.textContent=item.name;
    identity.append(en,zh);card.append(identity);
  };
  const speakers=[...new Map(cards.map(card=>({slug:card.dataset.doreSpeaker||speakerSlugs[card.dataset.person],name:card.dataset.person})).filter(item=>item.slug&&item.name).map(item=>[item.slug,item])).values()];
  fetch('/dore-design/runtime/olive-editorial-covers.v1.json')
   .then(response=>{if(!response.ok)throw new Error('Poster manifest unavailable');return response.json();})
   .then(data=>{
    const assets=new Map((data.records||[]).filter(item=>typeof item.url==='string'&&item.url.startsWith('/images/olive/')&&item.url.endsWith('.png')&&/^[a-z0-9-]+$/.test(item.url.slice('/images/olive/'.length,-4))).map(item=>[item.speaker,item.url]));
    for(const item of speakers){
     const a=document.createElement('a');
     a.className='olive-gallery-card';
     a.href='/olive/'+encodeURIComponent(item.slug)+'/';
     a.setAttribute('aria-label','進入'+item.name+'講員頻道');
     const src=assets.get(item.slug);
     if(src){
      const img=document.createElement('img');
      img.src=src;img.alt=item.name+'講員海報';img.loading='lazy';img.decoding='async';
      a.append(img);
     }else{
      const label=document.createElement('span');label.textContent=item.name;a.append(label);
     }
     addIdentity(a,item);gallery.append(a);
    }
   })
   .catch(()=>{
    for(const item of speakers){
     const a=document.createElement('a');a.className='olive-gallery-card';
     a.href='/olive/'+encodeURIComponent(item.slug)+'/';addIdentity(a,item);gallery.append(a);
    }
   });
  const topics=document.createElement('section');
  topics.className='olive-journey-section olive-topic-index';
  topics.id='olive-discourse';
  topics.setAttribute('aria-label','橄欖山論道 · 主題索引');
  topics.innerHTML='<h2>橄欖山論道</h2><div class="olive-topic-index__links"><a href="#olive-discourse">聖經綜覽</a><a href="#olive-discourse">靈命成長</a><a href="#olive-discourse">教會與使命</a><a href="#olive-discourse">門徒生活</a></div>';
  // The issue feature is curated editorial content, independent of the twelve-person roster.
  const issue=theater.querySelector('[data-olive-issue-sermons]');
  if(issue){
    const heading=document.createElement('h2');heading.textContent='本期論道';issue.append(heading);
    const note=document.createElement('p');note.textContent='當期講道由雜誌選題策展，不限於十二位講員。';issue.append(note);
    const entry=document.createElement('a');entry.href='/journal/';entry.textContent='閱讀當期期刊 ↗';issue.append(entry);
  }
  root.append(theater,topics);
})();
