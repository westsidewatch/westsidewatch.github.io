/* Reader-facing P2 church ministry chapters. Architectural 3D remains
   the single source of camera geometry, lighting and the 251s route.
   No fictional room names, service schedules, personnel or facilities. */
(() => {
  const query=new URLSearchParams(location.search);
  if(query.get('entry')!=='p2')return;
  document.body.dataset.churchEntry='p2';
  const chapters=[
    {at:12,boundary:0,name:'歡迎與連結',en:'WELCOME',title:'從一道門開始',
      description:'從南門走近教會。對第一次來訪的人，認識一個群體，始於一句問候與一次被接待。',
      reference:'約翰福音 7:38 · 活水的邀請'},
    {at:43,boundary:38,name:'團契生活',en:'FELLOWSHIP',title:'在四季裡相遇',
      description:'走進中庭，看見紅楓隨季節變換。團契不只是一場活動，而是彼此認識、陪伴與分享生命。',
      reference:'使徒行傳 2:42 · 彼此交接'},
    {at:83,boundary:70,name:'主日崇拜',en:'WORSHIP',title:'一起來到神面前',
      description:'進入主堂。等候、讚美、聆聽信息、回應與祝福，構成教會共同的主日敬拜。',
      reference:'羅馬書 15:5–6 · 同心榮耀神'},
    {at:95,boundary:93,name:'禱告與牧養',en:'PRAYER',title:'十字架前的禱告',
      description:'當鏡頭望向十字架，光從教會裡透出。禱告、守望與牧養，讓信仰進入每一個人的處境。',
      reference:'腓立比書 4:6–7 · 禱告、祈求與感謝'},
    {at:154,boundary:124,name:'關懷與相交',en:'CARE',title:'在同一張桌邊',
      description:'從庭院走向下層共享空間。問安、愛宴、彼此照顧與社區關懷，使敬拜延伸到日常生活。',
      reference:'約翰福音 13:35 · 彼此相愛'},
    {at:211,boundary:176,name:'查經與門訓',en:'DISCIPLESHIP',title:'在真道中成長',
      description:'沿著階梯登上較高的樓層。以查經、討論、學習與實踐，象徵門徒生命逐步成長。',
      reference:'雅各書 1:22 · 行道，不單聽道'},
    {at:241,boundary:234,name:'見證與差遣',en:'WITNESS',title:'把光帶向世界',
      description:'鏡頭升向天空，再望見整座教會。服事不限於建築之內，也指向身邊的人與更遠的世界。',
      reference:'馬太福音 5:14–16 · 世上的光'}
  ];
  const root=document.createElement('div');
  root.className='ws-ministry-story';
  root.setAttribute('aria-label','活水堂教會生活與事工導覽');
  root.innerHTML=`
    <div class="ws-ministry-story__rail">
      <div class="ws-ministry-story__eyebrow">LIVING WATER WEST · CHURCH LIFE</div>
      <h1 class="ws-ministry-story__heading">在教會裡，遇見生命</h1>
      <div class="ws-ministry-story__rule" aria-hidden="true"></div>
      <nav class="ws-ministry-story__index" aria-label="選擇教會事工章節">
        ${chapters.map((c,i)=>`<button class="ws-ministry-story__chapter" type="button"
           data-chapter="${i}" aria-label="前往第 ${i+1} 章：${c.name}" aria-current="${i===0?'step':'false'}">
            <span class="ws-ministry-story__chapter-number">${String(i+1).padStart(2,'0')}</span>
            <span class="ws-ministry-story__chapter-title">${c.name}</span>
            <span class="ws-ministry-story__chapter-mark" aria-hidden="true"></span>
        </button>`).join('')}
      </nav>
      <div class="ws-ministry-story__rail-footer">
        <button type="button" class="ws-ministry-story__control" data-action="play">暫停導覽</button>
        <button type="button" class="ws-ministry-story__control" data-action="hide">收起介紹</button>
        <a class="ws-ministry-story__back" href="/" aria-label="返回 Westside Watch 主站">返回</a>
      </div>
    </div>
    <section class="ws-ministry-story__panel" aria-live="polite" aria-atomic="true" aria-label="當前事工介紹">
      <div class="ws-ministry-story__meta"><span data-story-en>WELCOME</span>
        <span data-story-index>01 / 07</span></div>
      <h2 class="ws-ministry-story__title" data-story-title>從一道門開始</h2>
      <p class="ws-ministry-story__description" data-story-description></p>
      <span class="ws-ministry-story__reference" data-story-reference></span>
    </section>
    <button type="button" class="ws-ministry-story__minimal" data-action="show"
       aria-label="顯示教會事工章節">教會生活　01 — 07</button>
    <div class="ws-ministry-story__progress" aria-hidden="true">
      <div class="ws-ministry-story__progress-fill"></div>
    </div>`;
  document.body.append(root);
  const buttons=[...root.querySelectorAll('[data-chapter]')];
  const en=root.querySelector('[data-story-en]'),
    number=root.querySelector('[data-story-index]'),
    title=root.querySelector('[data-story-title]'),
    description=root.querySelector('[data-story-description]'),
    reference=root.querySelector('[data-story-reference]'),
    play=root.querySelector('[data-action="play"]'),
    progress=root.querySelector('.ws-ministry-story__progress-fill');
  let active=-1,manual=false,paused=false,queued=null;
  function render(index){
    if(index===active)return;
    const chapter=chapters[index];
    active=index;
    en.textContent=chapter.en;
    number.textContent=String(index+1).padStart(2,'0')+' / 07';
    title.textContent=chapter.title;
    description.textContent=chapter.description;
    reference.textContent=chapter.reference;
    for(let i=0;i<buttons.length;i++){
      if(i===index)buttons[i].setAttribute('aria-current','step');
      else buttons[i].removeAttribute('aria-current');
    }
  }
  function show(index){
    const guide=window.__churchGuide;
    if(!guide?.seek){queued=index;return;}
    manual=true;
    paused=true;
    guide.pause();
    guide.seek(chapters[index].at);
    play.textContent='繼續導覽';
    render(index);
  }
  buttons.forEach(button=>button.addEventListener('click',()=>{
    const index=Number(button.dataset.chapter);
    if(Number.isInteger(index)&&chapters[index])show(index);
  }));
  root.querySelector('[data-action="hide"]').addEventListener('click',()=>{
    root.classList.add('is-minimal');
  });
  root.querySelector('[data-action="show"]').addEventListener('click',()=>{
    root.classList.remove('is-minimal');
  });
  play.addEventListener('click',()=>{
    const guide=window.__churchGuide;
    if(!guide)return;
    paused=!paused;
    if(paused)guide.pause();else{guide.play();manual=false;}
    play.textContent=paused?'繼續導覽':'暫停導覽';
  });
  function tick(){
    const guide=window.__churchGuide;
    if(guide?.status){
      if(queued!==null){
        const next=queued;queued=null;show(next);
      }
      const state=guide.status();
      if(state.ready){
        const t=state.at;
        if(!manual){
          let idx=0;
          for(let i=0;i<chapters.length;i++)
            if(t>=chapters[i].boundary)idx=i;
          render(idx);
        }
        progress.style.width=(Math.min(1,t/251)*100).toFixed(3)+'%';
      }
    }
    requestAnimationFrame(tick);
  }
  render(0);
  window.__churchMinistryAudit=()=>({
    enabled:true,chapters:chapters.length,selected:active,
    chapterSeconds:chapters.map(c=>c.at),manual,paused
  });
  requestAnimationFrame(tick);
})();
