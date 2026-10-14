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
 const preview=nav.querySelector('.ws-nav-hover-preview');
 const previewFrame=preview?.querySelector('iframe');
 const previewCaption=preview?.querySelector('.ws-nav-hover-preview__caption');
 const previewSources={church:'/first-look-editorial/church.html',magazine:'/first-look-editorial/magazine.html',bible:'/first-look-editorial/bible.html',sermon:'/first-look-editorial/sermon.html',book:'/first-look-editorial/book.html',cinema:'/first-look-editorial/cinema.html',life:'/first-look-editorial/life.html'};
 let previewKey='';
 const summary=menu?.querySelector('summary');
 const panel=menu?.querySelector('.sites-home-nav__panel');
 const reduced=window.matchMedia('(prefers-reduced-motion: reduce)');
 /* Sevenfold Dawn: one reversible timeline, with an unmodified Film iframe. */
 const root=document.documentElement;
 const hero=document.querySelector('.sites-home-hero');
 const plane=hero?.querySelector('.ws-dawn-brand-plane');
 // Keep the original slogan and both logos on ONE plane above the folds.
 if(plane&&nav&&!nav.contains(plane))nav.appendChild(plane);
 const slogan=plane?.querySelector('#sites-home-title');
 const largeLogo=plane?.querySelector('.ws-dawn-large-logo');
 const scripture=hero?.querySelector('.ws-dawn-scripture');
 // A fixed element inside the clipped Film hero may disappear behind the menu.
 // Keep the single canonical scripture node in the top-level navigation layer.
 if(scripture&&scripture.parentElement!==document.body)document.body.appendChild(scripture);
 const folds=panel?.querySelector('.ws-dawn-folds');
 const icon=summary?.querySelectorAll('.ws-dawn-stroke');
 const links=[...menu.querySelectorAll('.sites-home-nav__panel-links>a')];
 const colors=['--ws-water','--ws-first-light','--ws-pale-gold','--ws-olive','--ws-harvest','--ws-crimson','--ws-daylight-mauve'];
 const logoImage=largeLogo?.querySelector('img');
 const logoNames=['water','first-light','pale-gold','olive','harvest','crimson','daylight-mauve'];
 let timeline=null,opened=false,lastColor=-1,closing=false;
 const makeFolds=()=>{
  folds.replaceChildren();
  const order=colors.map((_,i)=>i);
  for(let i=order.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[order[i],order[j]]=[order[j],order[i]];}
  if(order[order.length-1]===lastColor){const j=order.findIndex(n=>n!==lastColor);[order[j],order[order.length-1]]=[order[order.length-1],order[j]];}
  lastColor=order[order.length-1];
  // The final curtain color selects the matching canonical SVG variant.
  if(logoImage)logoImage.src='/images/sevenfold/westside-watch-logo-'+logoNames[lastColor]+'.svg';
  order.forEach(i=>{const layer=document.createElement('div');layer.className='ws-dawn-fold';layer.style.setProperty('--fold-color','var('+colors[i]+')');folds.append(layer)});
 };
 const layout=()=>{
  if(!plane||!slogan||!largeLogo)return 0;
  // A single plane translation is constrained by the fixed relative positions.
  // Align slogan top-left in open state; large-logo alignment is verified separately.
  const rect=slogan.getBoundingClientRect();
  const current=Number(window.gsap?.getProperty(plane,'y'))||0;
  // Keep the slogan visible in the upper half after the menu reveals.
  const os=getComputedStyle(document.body);
  const target=window.innerHeight*(parseFloat(os.getPropertyValue('--ws-dawn-slogan-open-top'))||4.5)/100;
  const shift=Math.min(0,target-(rect.top-current));
  const clearance=parseFloat(os.getPropertyValue('--ws-dawn-slogan-menu-clearance'))||28;
  const minTop=window.innerHeight*(parseFloat(os.getPropertyValue('--ws-dawn-menu-min-top'))||25)/100;
  const linksTop=Math.ceil(Math.max(minTop,rect.bottom-current+shift+clearance));
  nav.style.setProperty('--ws-dawn-links-top',linksTop+'px');
  // Apply measured OS geometry to the actual grid; legacy CSS selectors must not win.
  const linkGrid=panel?.querySelector('.sites-home-nav__panel-links');
  if(linkGrid)linkGrid.style.setProperty('top',linksTop+'px','important');
  // Align the large logo to the centre of the visible lower Film half after translation.
  // This is one static plane geometry variable, not an independent animated transform.
  const image=largeLogo.querySelector('img');
  const logoHeight=largeLogo.getBoundingClientRect().height || image?.getBoundingClientRect().height || 0;
  const targetTop=window.innerHeight*.75-logoHeight*.5;
  plane.style.setProperty('--ws-dawn-large-top',Math.round(targetTop-shift)+'px');
  return shift;
 };
 const prepare=()=>{
  if(!window.gsap||!plane||!panel||!folds)return false;
  timeline?.kill();
  makeFolds();
  const gs=window.gsap;
  gs.set(plane,{y:0});
  gs.set(folds.children,{scaleY:0,transformOrigin:'top center'});
  gs.set(links,{opacity:0,y:20});
  timeline=gs.timeline({paused:true,onComplete:()=>{opened=true;root.classList.add('ws-dawn-open');summary?.setAttribute('aria-label','Close site contents');},onReverseComplete:()=>{opened=false;closing=false;menu.open=false;root.classList.remove('ws-dawn-active','ws-dawn-open');summary?.setAttribute('aria-label','Open site contents');}});
  timeline.to(plane,{y:layout(),duration:1.05,ease:'power3.inOut'},0);
  timeline.to(folds.children,{scaleY:1,duration:.72,stagger:.065,ease:'power3.inOut'},0);
  timeline.to(links,{opacity:1,y:0,duration:.4,stagger:.04,ease:'power2.out'},.6);
  if(icon?.length===3){
   timeline.to(icon[0],{attr:{x1:15,y1:3,x2:15,y2:27},duration:.5},.18);
   timeline.to(icon[1],{attr:{x1:3,y1:15,x2:27,y2:15},duration:.5},.18);
   timeline.to(icon[2],{attr:{x1:15,y1:15,x2:15,y2:15},opacity:0,duration:.3},.18);
  }
  return true;
 };
 const openCurtain=()=>{
  if(menu.open&&!closing)return;
  if(closing&&timeline){closing=false;timeline.play();return;}
  menu.open=true;root.classList.add('ws-dawn-active');nav.dataset.navHidden='false';
  if(!prepare()){menu.open=false;root.classList.remove('ws-dawn-active');summary?.setAttribute('aria-label','Open site contents');return;}
  if(reduced.matches){timeline.progress(1);timeline.pause();root.classList.add('ws-dawn-open');opened=true;}
  else timeline.play(0);
 };
 const closeCurtain=()=>{
  if(!menu.open)return;
  closing=true;root.classList.remove('ws-dawn-open');
  if(!timeline){menu.open=false;root.classList.remove('ws-dawn-active');opened=false;closing=false;return;}
  if(reduced.matches){timeline.progress(0);timeline.pause();menu.open=false;root.classList.remove('ws-dawn-active');opened=false;closing=false;}
  else timeline.reverse();
 };
 summary?.addEventListener('click',event=>{event.preventDefault();if(menu.open&&!closing)closeCurtain();else openCurtain()});
 window.addEventListener('resize',()=>{if(!timeline||!menu.open)return;const progress=timeline.progress();timeline.kill();prepare();timeline.progress(progress).pause();if(opened)root.classList.add('ws-dawn-open');},{passive:true});
 const showPreview=(link)=>{const match=link.getAttribute('href')?.match(/^#first-look-(church|magazine|bible|sermon|book|cinema|life)$/);if(!match||!previewFrame)return;const key=match[1];if(key!==previewKey){previewKey=key;previewFrame.src=previewSources[key];}if(previewCaption)previewCaption.textContent=link.textContent.trim();preview?.classList.add('is-visible');};
 const clearPreview=()=>{preview?.classList.remove('is-visible')};
 menu?.querySelectorAll('.sites-home-nav__panel-links>a').forEach(link=>{
  link.addEventListener('pointerenter',()=>showPreview(link));
  link.addEventListener('focus',()=>showPreview(link));
 });
 menu?.addEventListener('pointerleave',clearPreview);
 menu?.addEventListener('focusout',event=>{if(!menu.contains(event.relatedTarget))clearPreview()});
 menu?.querySelectorAll('a').forEach(a=>a.addEventListener('click',event=>{const hash=a.getAttribute('href');timeline?.pause(0);menu.open=false;opened=false;closing=false;root.classList.remove('ws-dawn-active','ws-dawn-open');nav.dataset.navHidden='false';if(hash?.startsWith('#')){const target=document.getElementById(hash.slice(1));if(target){event.preventDefault();history.pushState(null,'',hash);requestAnimationFrame(()=>target.scrollIntoView({behavior:reduced.matches?'instant':'smooth',block:'start'}));}}}));
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&menu?.open){closeCurtain();menu.querySelector('summary')?.focus()}});
 document.addEventListener('pointerdown',e=>{if(menu?.open&&!menu.contains(e.target))closeCurtain()});
 update();
})();

/* Keep the viewport behind the full-screen contents still while it is open. */
