/* P2 production handoff / church -> Vol.00 magazine.
 * The existing V75 water, church schedule and Red Sea door implementation
 * remain untouched. This additive bridge observes the same P2 scroll pose
 * after the old scene is drawn, then exposes the approved two-page folio.
 */
(()=>{'use strict';
 const query=new URLSearchParams(location.search);
 // An opt-in historical proof owns its magazine; never replace that laboratory.
 if(query.get('magazineProof')==='1')return;
 const root=document.querySelector('.showcase');
 const magazine=root?.querySelector('.p2-magazine');
 if(!root||!magazine)return;
 const church=root.querySelector('.church-editorial');
 const churchIndex=root.querySelector('.index');
 const embedded=document.documentElement.dataset.p2Embedded==='true';
 const handoffVh=2.37; // the approved Red Sea / church door is fully open
 const finalVh=embedded?4:5.2; // standalone also grants a full editorial scroll passage
 const clamp=n=>Math.min(1,Math.max(0,n));
 const easing=n=>{n=clamp(n);return n*n*(3-2*n)};
 // The background is the SAME six-clip moving film used by the homepage.
 // Reuse its cover-mode player and manifest; never create a second montage.
 const film=document.createElement('iframe');
 film.className='p2-magazine__home-film';
 film.title='首頁〈王進城〉影片，延續至西望雜誌背景';
 film.src='/preview/watch-city-vol00/hosanna/?cover=1&v=20261012-cover-palette-r1';
 film.tabIndex=-1;
 film.setAttribute('aria-hidden','true');
 film.loading='eager';
 film.setAttribute('allow','autoplay');
 film.style.cssText='display:block;position:absolute;inset:0;width:100%;height:100%;border:0;z-index:0;pointer-events:none;background:var(--paper);opacity:0';
 const frame=document.createElement('iframe');
 frame.title='西望 Vol.00：承接活水教會的封面、晨星與十二欄目目錄';
 frame.src='/experiments/p2-double-square-video-lab.html?embed=1&p=0&side=cover-right';
 frame.loading='eager';
 frame.setAttribute('allow','autoplay');
 frame.style.cssText='display:block;position:absolute;inset:0;width:100%;height:100%;border:0;z-index:1;background:transparent';
 magazine.replaceChildren(film,frame);
 root.dataset.p2MagazineDesign='vol00-continuous-church-handoff';
 let loaded=false,filmLoaded=false,filmPlaying=null,lastVh=NaN;
 function syncFilm(shouldPlay,force=false){
  if(!filmLoaded||(!force&&filmPlaying===shouldPlay))return;
  filmPlaying=shouldPlay;
  film.contentWindow?.postMessage({type:'watch-cover-playback',paused:!shouldPlay},location.origin);
 }
 function paint(vh){
  const progress=clamp((vh-handoffVh)/(finalVh-handoffVh));
  const active=progress>0;
  // The original P2 JS may still calculate its retired placeholder's mask.
  // Replace only that magazine layer; never alter the water/door elements.
  magazine.style.visibility=active?'visible':'hidden';
  magazine.style.clipPath='none';
  // Close the Church spread like a page turn: the Vol.00 paper gradually
  // becomes opaque so the completed folio cannot leave Sunday copy visible
  // around its edges. The Church remains intact underneath for reverse scroll.
  const paperCover=Math.round(easing(progress/.34)*100);
  magazine.style.background=`color-mix(in srgb, var(--paper) ${paperCover}%, transparent)`;
  film.style.opacity=String(easing(progress/.20));
  syncFilm(active&&document.visibilityState==='visible');
  magazine.style.opacity='1';
  magazine.style.pointerEvents=progress>=.995?'auto':'none';
  magazine.inert=progress<.995;
  magazine.setAttribute('aria-hidden',progress>=.995?'false':'true');
  magazine.dataset.magazineStage=progress<.20?'cover-arrival':progress<.53?'xiwang-impression':
   progress<.72?'morning-star-rise':progress<.865?'cover-and-star':
   progress<.995?'contents-handoff':'contents-final';
  root.dataset.p2MagazineProgress=progress.toFixed(4);
  if(active){
   root.dataset.p2Phase=progress>=.995?'magazine':'church-to-magazine';
   if(church){church.inert=true;church.setAttribute('aria-hidden','true')}
  }else if(church){
   church.inert=false;
   // drawScene remains the sole authority for Church visibility before handoff.
  }
  if(churchIndex){
   const exit=easing((progress-.72)/.20);
   churchIndex.style.opacity=active?String(1-exit):'';
   churchIndex.style.pointerEvents=exit>.5?'none':'';
   churchIndex.setAttribute('aria-hidden',exit>.99?'true':'false');
  }
  if(loaded)frame.contentWindow?.postMessage({
   type:'westside-p2-dual-progress',progress,side:'cover-right'
  },location.origin);
 }
 // The existing P2 scroll owner sets this attribute last in drawScene.
 // A MutationObserver runs in the same event turn, after that draw and before
 // paint: there is no new animation clock or free-running overlay timer.
 const watch=new MutationObserver(()=>{
  const vh=Number(root.dataset.p2Progress);
  if(!Number.isFinite(vh)||vh===lastVh)return;
  lastVh=vh;paint(vh);
 });
 watch.observe(root,{attributes:true,attributeFilter:['data-p2-progress']});
 film.addEventListener('load',()=>{
  filmLoaded=true;
  syncFilm(Number(root.dataset.p2MagazineProgress)>0&&document.visibilityState==='visible',true);
 });
 document.addEventListener('visibilitychange',()=>syncFilm(
  Number(root.dataset.p2MagazineProgress)>0&&document.visibilityState==='visible'));
 addEventListener('message',event=>{
  if(event.origin!==location.origin||event.source!==parent||event.data?.type!=='westside-p2-scroll')return;
  syncFilm(event.data.active!==false&&Number(root.dataset.p2MagazineProgress)>0&&document.visibilityState==='visible');
 });
 frame.addEventListener('load',()=>{loaded=true;paint(Number(root.dataset.p2Progress)||0)});
 paint(Number(root.dataset.p2Progress)||0);
})();
