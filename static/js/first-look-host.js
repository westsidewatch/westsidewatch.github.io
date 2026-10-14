/* Reuse actual realm homepages; keep requested anchors stable while lazy frames size. */
(()=>{
 const frames=[...document.querySelectorAll('[data-fl-realm-frame]')];let anchor=null,raf;
 const requested=()=>{anchor=/^#first-look-(church|magazine|bible|sermon|book|cinema|life)$/.test(location.hash)||location.hash==='#sites-first-layer'?document.getElementById(location.hash.slice(1)):null;if(anchor)anchor.scrollIntoView({behavior:'instant',block:'start'});schedule()};
 const update=()=>{for(const frame of frames){const rect=frame.getBoundingClientRect(),progress=Math.max(0,Math.min(1,-rect.top/(Math.max(rect.height,1)*.55)));frame.contentWindow?.postMessage({type:'ws-first-look:progress',progress},location.origin)}raf=null};
 const schedule=()=>{if(!raf)raf=requestAnimationFrame(update)};
 window.addEventListener('message',event=>{if(event.origin!==location.origin||event.data?.type!=='ws-first-look:height')return;const frame=frames.find(f=>f.contentWindow===event.source),height=Number(event.data.height);if(frame&&Number.isFinite(height)&&height>=350&&height<=6000){const size=Math.ceil(height)+'px';if(frame.style.height!==size){if(anchor&&Math.abs(anchor.getBoundingClientRect().top)>3)anchor=null;frame.style.height=size;if(anchor)anchor.scrollIntoView({behavior:'instant',block:'start'});schedule()}}});
 for(const event of ['wheel','touchstart','pointerdown','keydown'])window.addEventListener(event,()=>{anchor=null},{passive:true});
 window.addEventListener('hashchange',requested);window.addEventListener('scroll',schedule,{passive:true});window.addEventListener('resize',schedule);frames.forEach(f=>f.addEventListener('load',schedule));requested();
})();

/* First-layer floating navigation: native scrolling, no scroll lock or snap. */
(()=>{
 const nav=typeof document.querySelector==='function'?document.querySelector('.sites-home-nav--floating'):null;
 if(!nav)return;
 const menu=nav.querySelector('details');
 let previousY=window.scrollY,scheduled=false;
 const update=()=>{
  const y=Math.max(0,window.scrollY),delta=y-previousY;
  const expanded=Boolean(menu?.open);
  if(Math.abs(delta)>5&&!expanded){
   nav.dataset.navHidden=String(y>120&&delta>0);
  }
  if(y<90||expanded)nav.dataset.navHidden='false';
  const film=document.querySelector('.sites-home-hero');
  const inFilm=film&&film.getBoundingClientRect().bottom>Math.min(120,window.innerHeight*.2);
  nav.dataset.navTone=inFilm?'dark':'light';
  previousY=y;scheduled=false;
 };
 window.addEventListener('scroll',()=>{if(!scheduled){scheduled=true;requestAnimationFrame(update)}},{passive:true});
 window.addEventListener('resize',update,{passive:true});
 menu?.addEventListener('toggle',()=>{if(menu.open)nav.dataset.navHidden='false';document.documentElement.classList.toggle('ws-home-menu-open',Boolean(menu.open));update()});
 const stage=document.getElementById('ws-home-stage');
 const stageFrame=stage?.querySelector('.ws-home-stage__frame');
 const stageClose=stage?.querySelector('.ws-home-stage__close');
 const chapters={church:'/first-look-editorial/church.html',magazine:'/first-look-editorial/magazine.html',bible:'/first-look-editorial/bible.html',sermon:'/first-look-editorial/sermon.html',book:'/first-look-editorial/book.html',cinema:'/first-look-editorial/cinema.html',life:'/first-look-editorial/life.html'};
 let stageReturnFocus=null;
 const closeStage=()=>{if(!stage?.classList.contains('is-active'))return;stage.classList.remove('is-active');stage.setAttribute('aria-hidden','true');document.documentElement.classList.remove('ws-home-stage-open');stageFrame?.removeAttribute('src');stageReturnFocus?.focus?.();};
 const openStage=(key)=>{if(!stage||!chapters[key])return;stageReturnFocus=document.activeElement;menu.open=false;nav.dataset.navHidden='false';stageFrame.src=chapters[key];stageFrame.title=key+' — Westside Watch';stage.setAttribute('aria-hidden','false');stage.classList.add('is-active');document.documentElement.classList.add('ws-home-stage-open');stageClose?.focus();};
 menu?.querySelectorAll('a').forEach(a=>a.addEventListener('click',event=>{
  const hash=a.getAttribute('href'),match=hash?.match(/^#first-look-(church|magazine|bible|sermon|book|cinema|life)$/);
  if(match){event.preventDefault();openStage(match[1]);return;}
  if(hash==='#sites-first-layer'){event.preventDefault();openStage('magazine');return;}
  menu.open=false;nav.dataset.navHidden='false';
 }));
 stageClose?.addEventListener('click',closeStage);
 stage?.addEventListener('keydown',event=>{if(event.key==='Tab'){const controls=[stageClose,stageFrame].filter(Boolean);const idx=controls.indexOf(document.activeElement);if(event.shiftKey&&idx===0){event.preventDefault();controls.at(-1)?.focus()}else if(!event.shiftKey&&idx===controls.length-1){event.preventDefault();controls[0]?.focus()}}});

 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&stage?.classList.contains('is-active')){closeStage();return}if(e.key==='Escape'&&menu?.open){menu.open=false;menu.querySelector('summary')?.focus()}});
 document.addEventListener('pointerdown',e=>{if(menu?.open&&!menu.contains(e.target))menu.open=false});
 update();
})();

/* Keep the viewport behind the full-screen contents still while it is open. */
