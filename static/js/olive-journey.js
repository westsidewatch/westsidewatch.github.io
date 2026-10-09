(() => {
  'use strict';
  const root=document.querySelector('.olive-archive');
  if(!root)return;
  const rail=root.querySelector('.olive-speaker-rail');
  const cards=[...(rail?.querySelectorAll('.olive-speaker-card:not(.olive-speaker-card--clone)')||[])];
  // Internal journey IDs are implementation details, not visible editorial headings.
  const home=root.querySelector('.olive-home-stage');
  if(home)home.id='olive-speaker-experience';
  // The second layer is a readable gallery of the twelve approved editorial posters,
  // not a placeholder video rectangle or a repeated list of tiny names.
  const theater=document.createElement('section');
  theater.className='olive-journey-section olive-journey-theater';
  theater.id='olive-sermon-experience';
  theater.setAttribute('aria-label','十二講員全員展示');
  theater.innerHTML='<div class="olive-poster-gallery" aria-label="十二講員海報"></div>';
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
  root.append(theater);
})();
