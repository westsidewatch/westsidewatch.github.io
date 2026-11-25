/* Reader-facing P2 church ministry chapters. Architectural 3D remains
   the single source of camera geometry, lighting and the 251s route.
   No fictional room names, service schedules, personnel or facilities. */
(() => {
  const query=new URLSearchParams(location.search);
  if(query.get('entry')!=='p2')return;
  document.body.dataset.churchEntry='p2';
  const chapters=[
  {
    "at": 12,
    "boundary": 0,
    "name": "歡迎與連結",
    "en": "WELCOME",
    "title": "從一道門開始",
    "description": "由南門走進教會，從接待與認識彼此開始。",
    "reference": "約翰福音 7:38 · JOHN 7:38",
    "zh": "信我的人，就如經上所說：『從他腹中要流出活水的江河來。』",
    "kjv": "He that believeth on me, as the scripture hath said, out of his belly shall flow rivers of living water."
  },
  {
    "at": 43,
    "boundary": 38,
    "name": "團契生活",
    "en": "FELLOWSHIP",
    "title": "在四季裡相遇",
    "description": "中庭楓樹的季節轉變，見證教會的團契、同行與彼此扶持。",
    "reference": "使徒行傳 2:42 · ACTS 2:42",
    "zh": "都恆心遵守使徒的教訓，彼此交接、擘餅、祈禱。",
    "kjv": "And they continued stedfastly in the apostles' doctrine and fellowship, and in breaking of bread, and in prayers."
  },
  {
    "at": 94,
    "boundary": 70,
    "name": "主日崇拜",
    "en": "WORSHIP",
    "title": "一起來到神面前",
    "description": "停留在十字架的光中，與會眾一同等候、讚美、聆聽、回應和領受祝福。",
    "reference": "羅馬書 15:5–6 · ROMANS 15:5–6",
    "zh": "但願賜忍耐安慰的神，叫你們彼此同心，效法基督耶穌，一心一口榮耀神─我們主耶穌基督的父！",
    "kjv": "Now the God of patience and consolation grant you to be likeminded one toward another according to Christ Jesus: That ye may with one mind and one mouth glorify God, even the Father of our Lord Jesus Christ."
  },
  {
    "at": 95,
    "boundary": 98,
    "name": "禱告與牧養",
    "en": "PRAYER",
    "title": "十字架前的禱告",
    "description": "在十字架的亮光前安靜停留，記念教會裡的禱告、守望和牧養。",
    "reference": "腓立比書 4:6–7 · PHILIPPIANS 4:6–7",
    "zh": "應當一無掛慮，只要凡事藉著禱告、祈求，和感謝，將你們所要的告訴神。神所賜出人意外的平安，必在基督耶穌裡保守你們的心懷意念。",
    "kjv": "Be careful for nothing; but in every thing by prayer and supplication with thanksgiving let your requests be made known unto God. And the peace of God, which passeth all understanding, shall keep your hearts and minds through Christ Jesus."
  },
  {
    "at": 151,
    "boundary": 124,
    "name": "關懷與相交",
    "en": "CARE",
    "title": "在同一張桌邊",
    "description": "在下層共享空間停留，記念愛宴、問安、彼此照顧與社區關懷。",
    "reference": "約翰福音 13:34–35 · JOHN 13:34–35",
    "zh": "我賜給你們一條新命令，乃是叫你們彼此相愛；我怎樣愛你們，你們也要怎樣彼此相愛。你們若有彼此相愛的心，眾人因此就認出你們是我的門徒了。",
    "kjv": "A new commandment I give unto you, That ye love one another; as I have loved you, that ye also love one another. By this shall all men know that ye are my disciples, if ye have love one to another."
  },
  {
    "at": 211,
    "boundary": 176,
    "name": "查經與門訓",
    "en": "DISCIPLESHIP",
    "title": "在真道中成長",
    "description": "循著簡潔的階梯登上上層，俯看中庭，象徵查經、學習和實踐真道的成長。",
    "reference": "雅各書 1:22 · JAMES 1:22",
    "zh": "只是你們要行道，不要單單聽道，自己欺哄自己。",
    "kjv": "But be ye doers of the word, and not hearers only, deceiving your own selves."
  },
  {
    "at": 248,
    "boundary": 234,
    "name": "見證與差遣",
    "en": "WITNESS",
    "title": "把光帶向世界",
    "description": "傍晚的十字架從教會裡向外發光。鏡頭定格於整座建築，讓主日生活延伸至世界。",
    "reference": "馬太福音 5:14–16 · MATTHEW 5:14–16",
    "zh": "你們是世上的光。城造在山上是不能隱藏的。人點燈，不放在斗底下，是放在燈臺上，就照亮一家的人。你們的光也當這樣照在人前，叫他們看見你們的好行為，便將榮耀歸給你們在天上的父。",
    "kjv": "Ye are the light of the world. A city that is set on an hill cannot be hid. Neither do men light a candle, and put it under a bushel, but on a candlestick; and it giveth light unto all that are in the house. Let your light so shine before men, that they may see your good works, and glorify your Father which is in heaven."
  }
];

  const root=document.createElement('div');
  root.className='ws-ministry-story';root.dataset.wsSeal='water';
  root.setAttribute('aria-label','活水堂教會生活與事工導覽');
  root.innerHTML=`
    <div class="ws-ministry-story__rail">
      <div class="ws-ministry-story__identity"><span class="ws-name-seal" data-cut="small" aria-hidden="true"></span><div class="ws-ministry-story__eyebrow">LIVING WATER WEST · CHURCH LIFE</div></div>
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
    <div class="ws-ministry-story__final-identity" aria-label="教會正式名稱">
      <span class="ws-ministry-story__final-artwork" role="img" aria-label="神召會活水堂西區教會"></span>
      <span lang="en">P.A.O.C. Living Water Assembly West</span>
    </div>
    <div class="ws-ministry-story__final-stack">
    <section class="ws-ministry-story__panel" aria-live="polite" aria-atomic="true" aria-label="當前事工介紹">
      <div class="ws-ministry-story__meta"><span data-story-en>WELCOME</span>
        <span data-story-index>01 / 07</span></div>
      <h2 class="ws-ministry-story__title" data-story-title>從一道門開始</h2>
      <p class="ws-ministry-story__description" data-story-description></p>
      <div class="ws-ministry-story__scripture" aria-label="中英文完整主題經文">
        <div class="ws-ministry-story__verse-zh" lang="zh-Hant" data-story-zh></div>
        <div class="ws-ministry-story__verse-en" lang="en" data-story-kjv></div>
        <span class="ws-ministry-story__reference" data-story-reference></span>
        <a class="ws-ministry-story__content-link" data-story-link href="/church/visit/#ministries">了解教會生活</a>
      </div>
    </section>
    <section class="ws-ministry-story__sunday" aria-label="教會主日崇拜程序表" aria-hidden="true">
      <header class="ws-ministry-story__sunday-head">
        <span class="ws-ministry-story__eyebrow">SUNDAY WORSHIP · LIVING WATER WEST</span>
        <h2>主日崇拜<span lang="en">Sunday Worship</span></h2>
      </header>
      <div class="ws-ministry-story__sunday-rows">
        <div class="ws-ministry-story__sunday-row">
          <time>10:30–11:00</time><div><strong>以等候宣告敬拜神</strong><small>安靜等候主</small></div>
        </div><div class="ws-ministry-story__sunday-row">
          <time>11:00–11:30</time><div><strong>以揚聲讚美敬拜神</strong><small>詩歌、讚美與會眾敬拜</small></div>
        </div><div class="ws-ministry-story__sunday-row">
          <time>11:30–12:20</time><div><strong>以聆聽信息敬拜神</strong><small>證道與聆聽聖經信息</small></div>
        </div><div class="ws-ministry-story__sunday-row">
          <time>12:20–12:40</time><div><strong>以回應奉獻敬拜神</strong><small>回應、分享、奉獻</small></div>
        </div><div class="ws-ministry-story__sunday-row">
          <time>12:40</time><div><strong>以領受祝福敬拜神</strong><small>三一頌、祝福</small></div>
        </div><div class="ws-ministry-story__sunday-row">
          <time>12:45–13:00</time><div><strong>以關懷相交敬拜神</strong><small>歡迎新朋友、彼此問安</small></div>
        </div><div class="ws-ministry-story__sunday-row">
          <time>13:00–13:30</time><div><strong>以合一禱告敬拜神</strong><small>謝飯禱告、愛宴</small></div>
        </div>
      </div>
      <footer>205 Wilmington Ave. · North York, ON</footer>
    </section>
    <button class="ws-ministry-story__return-to-scene" type="button" data-action="return-scene">返回教會全景</button>
    </div>
    <button class="ws-ministry-story__scroll-invitation" type="button" data-action="read-finale"
      aria-label="向下滑動閱讀主日程序與你們是世上的光完整經文">
      <span>向下滑閱 · 主日程序與經文</span>
    </button>
    <button type="button" class="ws-ministry-story__minimal" data-action="show"
       aria-label="顯示教會事工章節">教會生活　01 — 07</button>
    <div class="ws-ministry-story__progress" aria-hidden="true">
      <div class="ws-ministry-story__progress-fill"></div>
    </div>`;
  document.body.append(root);
  // The same source powers P2 and this 3D finale; this page has no separate Sunday editor.
  window.WestsideSunday?.mountTour(root);
  const ministryAction=root.querySelector('[data-story-link]');
  let ministryItems=null;
  const syncMinistryAction=i=>{
    const item=ministryItems?.[i];
    ministryAction.href=item?.href||'/church/visit/#ministries';
    ministryAction.textContent=item?.action||'了解教會生活';
  };
  fetch('/data/church/ministries.json',{cache:'no-store'}).then(r=>r.ok?r.json():null)
    .then(d=>{if(d&&Array.isArray(d.items)&&d.items.length===7)ministryItems=d.items;syncMinistryAction(active>=0?active:0);})
    .catch(()=>{});

  const buttons=[...root.querySelectorAll('[data-chapter]')];
  const en=root.querySelector('[data-story-en]'),
    number=root.querySelector('[data-story-index]'),
    title=root.querySelector('[data-story-title]'),
    description=root.querySelector('[data-story-description]'),
    reference=root.querySelector('[data-story-reference]'),
    verseZh=root.querySelector('[data-story-zh]'),
    verseKjv=root.querySelector('[data-story-kjv]'),
    sunday=root.querySelector('.ws-ministry-story__sunday'),
    play=root.querySelector('[data-action="play"]'),
    progress=root.querySelector('.ws-ministry-story__progress-fill');
  let active=-1,manual=false,paused=false,queued=null;
  const mobileFinale=window.matchMedia('(max-width:680px)');
  // First settle on the whole church, then let the Sunday programme
  // emerge at reading pace. On phones it emerges only when the reader
  // actually scrolls to the lower content, never over the building.
  const sundayRows=[...root.querySelectorAll('.ws-ministry-story__sunday-row')];
  sundayRows.forEach((row,i)=>row.style.setProperty('--sunday-row-order',String(i)));
  const sundayObserver='IntersectionObserver' in window
    ?new IntersectionObserver(entries=>{
      if(entries.some(entry=>entry.isIntersecting)&&root.classList.contains('is-finale')){
        root.classList.add('is-sunday-visible');
      }
    },{threshold:0.12})
    :null;
  if(sundayObserver)sundayObserver.observe(sunday);
  function setFinaleMode(finale){
    const previouslyFinale=root.classList.contains('is-finale');
    root.classList.toggle('is-finale',finale);
    if(!finale){
      root.classList.remove('is-sunday-visible');
    }else if(!mobileFinale.matches||!sundayObserver){
      root.classList.add('is-sunday-visible');
    }else if(!previouslyFinale){
      // On mobile, a new finale starts with an unobstructed full-screen
      // scene. IntersectionObserver starts the stagger after scroll.
      root.classList.remove('is-sunday-visible');
    }
    const scrollFinale=finale&&mobileFinale.matches;
    document.documentElement.classList.toggle('church-finale-scroll',scrollFinale);
    document.body.classList.toggle('church-finale-scroll',scrollFinale);
    sunday.setAttribute('aria-hidden',String(!finale));
  }
  function render(index){
    if(index===active)return;
    const chapter=chapters[index];
    active=index;
    syncMinistryAction(index);
    en.textContent=chapter.en;
    number.textContent=String(index+1).padStart(2,'0')+' / 07';
    title.textContent=chapter.title;
    description.textContent=chapter.description;
    reference.textContent=chapter.reference+' · 和合本 / KJV';
    verseZh.textContent=chapter.zh;
    verseKjv.textContent=chapter.kjv;
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
    // The chapter click must render its final reading page immediately.
    // SwiftShader and slower devices can delay requestAnimationFrame for
    // seconds while drawing the 3D GLB; do not wait for the next frame.
    setFinaleMode(index===chapters.length-1);
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
  const readingStack=root.querySelector('.ws-ministry-story__final-stack');
  function jumpInDocument(top){
    const scrolling=document.scrollingElement;
    if(!scrolling)return;
    // An immediate native-document scroll does not depend on WebGL frame
    // delivery. Smooth-scroll animations can stall during heavy GLB draws.
    scrolling.style.scrollBehavior='auto';
    scrolling.scrollTop=Math.max(0,top);
    scrolling.style.removeProperty('scroll-behavior');
  }
  root.querySelector('[data-action="read-finale"]').addEventListener('click',()=>{
    const scrolling=document.scrollingElement;
    jumpInDocument(readingStack.getBoundingClientRect().top+(scrolling?.scrollTop||0));
  });
  root.querySelector('[data-action="return-scene"]').addEventListener('click',()=>{
    jumpInDocument(0);
  });
  let finalePinned=false;
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
        // The Sunday order appears ABOVE, not instead of, the complete
        // Matthew 5:14-16 scripture block. On narrow screens the original
        // church finale fills the first viewport; readers scroll down to
        // separate, stacked folios in document flow.
        const finale=t>=246;
        if(t<246)finalePinned=false;
        if(finale&&!manual&&!finalePinned&&t>=248){
          guide.pause();
          guide.seek(248);
          finalePinned=true;
          paused=true;
          play.textContent='繼續導覽';
        }
        setFinaleMode(finale);
        progress.style.width=(Math.min(1,t/251)*100).toFixed(3)+'%';
      }
    }
    requestAnimationFrame(tick);
  }
  render(0);
  window.__churchMinistryAudit=()=>({
    enabled:true,chapters:chapters.length,selected:active,
    chapterSeconds:chapters.map(c=>c.at),manual,paused,
    fullVerses:chapters.every(c=>c.zh.length>10&&c.kjv.length>20),
    scheduleRows:7,sundayVisible:root.classList.contains('is-finale'),
    sundayRevealStarted:root.classList.contains('is-sunday-visible'),
    scriptureVisible:root.classList.contains('is-finale') &&
      getComputedStyle(root.querySelector('.ws-ministry-story__panel')).display!=='none',
    scrollFinale:document.body.classList.contains('church-finale-scroll')
  });
  requestAnimationFrame(tick);
})();
