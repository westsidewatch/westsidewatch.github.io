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
  const theater=document.createElement('section');
  theater.className='olive-journey-section olive-journey-theater';
  theater.id='olive-sermon-experience';
  theater.setAttribute('aria-labelledby','olive-theater-title');
  theater.innerHTML='<div class="olive-journey-heading"><p>02 / THE SERMONS</p><h2 id="olive-theater-title">講道劇場</h2></div><div class="olive-journey-theater-grid"><div class="olive-journey-screen"><p>FEATURED SERMON</p><h3>大衛鮑森</h3><p>從上方主視覺播放精選講道，或選擇講員進入其系列與單集。</p><a href="#olive-speaker-experience">返回主視覺播放 ↑</a></div><div class="olive-journey-aside"><p>EXPLORE BY SPEAKER</p><div class="olive-journey-speaker-links"></div></div></div>';
  const list=theater.querySelector('.olive-journey-speaker-links');
  for(const card of cards){
    const label=card.dataset.person;
    if(!label)continue;
    const a=document.createElement('a');
    a.textContent=label+' ↗';
    const slug=card.dataset.doreSpeaker;
    a.href=slug?'/olive/'+slug+'/':'#olive-speaker-experience';
    list.append(a);
  }
  const archive=document.createElement('section');
  archive.className='olive-journey-section olive-journey-archive';
  archive.id='olive-archive-experience';
  archive.setAttribute('aria-labelledby','olive-archive-title');
  archive.innerHTML='<div class="olive-journey-heading"><p>03 / THE ARCHIVE</p><h2 id="olive-archive-title">講道檔案館</h2></div><p>按講員、系列與主題探索已收錄的講道資料。</p><a class="olive-journey-archive-link" href="#olive-sermon-experience">瀏覽講員與系列入口 ↗</a>';
  root.append(theater,archive);
})();