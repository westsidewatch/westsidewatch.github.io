(() => {
  'use strict';
  const root=document.querySelector('.olive-archive');
  if(!root)return;
  const rail=root.querySelector('.olive-speaker-rail');
  const cards=[...(rail?.querySelectorAll('.olive-speaker-card:not(.olive-speaker-card--clone)')||[])];
  // Keep original speaker routes and buttons: add one accessible archive/theater navigation.
  const nav=document.createElement('nav');
  nav.className='olive-journey-nav';
  nav.setAttribute('aria-label','橄欖山內容導航');
  nav.innerHTML='<a href="#olive-speaker-experience">01 <span lang="en">The Speakers</span><small>講員長廊</small></a><a href="#olive-sermon-experience">02 <span lang="en">The Sermons</span><small>講道劇場</small></a><a href="#olive-archive-experience">03 <span lang="en">The Archive</span><small>講道檔案</small></a>';
  root.prepend(nav);
  const home=root.querySelector('.olive-home-stage');
  if(home)home.id='olive-speaker-experience';
  // The second layer is a readable gallery of the twelve approved editorial posters,
  // not a placeholder video rectangle or a repeated list of tiny names.
  const theater=document.createElement('section');
  theater.className='olive-journey-section olive-journey-theater';
  theater.id='olive-sermon-experience';
  theater.setAttribute('aria-labelledby','olive-theater-title');
  theater.innerHTML='<div class="olive-journey-heading"><p>02 / THE SPEAKERS</p><h2 id="olive-theater-title">十二講員</h2></div><p class="olive-gallery-intro">選擇講員海報，進入講員頻道與系列講道。</p><div class="olive-poster-gallery" aria-label="十二講員海報"></div>';
  const gallery=theater.querySelector('.olive-poster-gallery');
  const speakers=[{slug:'david-pawson',name:'大衛鮑森'},...cards.map(card=>({slug:card.dataset.doreSpeaker,name:card.dataset.person}))].filter(item=>item.slug&&item.name);
  fetch('/dore-design/runtime/olive-editorial-covers.v1.json')
   .then(response=>{if(!response.ok)throw new Error('Poster manifest unavailable');return response.json();})
   .then(data=>{
    const assets=new Map((data.records||[]).filter(item=>/^\\/images\\/olive\\/[a-z0-9-]+\\.png$/.test(item.url||'')).map(item=>[item.speaker,item.url]));
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
     gallery.append(a);
    }
   })
   .catch(()=>{
    for(const item of speakers){
     const a=document.createElement('a');a.className='olive-gallery-card';
     a.href='/olive/'+encodeURIComponent(item.slug)+'/';a.textContent=item.name;gallery.append(a);
    }
   });
  const archive=document.createElement('section');
  archive.className='olive-journey-section olive-journey-archive';
  archive.id='olive-archive-experience';
  archive.setAttribute('aria-labelledby','olive-archive-title');
  archive.innerHTML='<div class="olive-journey-heading"><p>03 / THE ARCHIVE</p><h2 id="olive-archive-title">講道檔案館</h2></div><p>按講員、系列與主題探索已收錄的講道資料。</p><a class="olive-journey-archive-link" href="#olive-sermon-experience">瀏覽講員與系列入口 ↗</a>';
  root.append(theater,archive);
})();