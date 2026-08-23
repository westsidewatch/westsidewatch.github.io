(()=>{
  'use strict';
  // Visible deployment probe. Remove after Pages propagation is confirmed.
  const deployProbe=()=>{
    if(document.getElementById('dore-deploy-probe'))return;
    const el=document.createElement('div');
    el.id='dore-deploy-probe';
    el.textContent='build: chapter-reading-v4';
    Object.assign(el.style,{position:'fixed',right:'10px',bottom:'10px',zIndex:'99999',padding:'5px 8px',background:'rgba(255,253,246,.92)',border:'1px solid rgba(140,104,24,.45)',color:'#8c6818',font:'12px monospace',borderRadius:'4px'});
    document.body.appendChild(el);
  };
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',deployProbe,{once:true});
  else deployProbe();

  // Keep the Search UI usable even while capability runtimes are loading.
  const unlockSearch=()=>{
    const input=document.getElementById('search-input');
    const button=document.getElementById('search-button');
    if(input)input.disabled=false;
    if(button)button.disabled=false;
  };
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',unlockSearch,{once:true});
  else unlockSearch();

  // Scripture Search Input Literacy is a learnable, maintainable input corpus.
  // Load the pure parser reflex first so it can be tested independently in CI.
  const parserRuntime=document.createElement('script');
  parserRuntime.src='/dore/dore-scripture-reference-parser.js?v=ssl1-20260823a';
  parserRuntime.onload=()=>{
    const inputLiteracyRuntime=document.createElement('script');
    inputLiteracyRuntime.src='/dore/dore-search-input-literacy.js?v=ssl1-20260823b';
    document.head.appendChild(inputLiteracyRuntime);
  };
  document.head.appendChild(parserRuntime);

  // Final presentation guard for whole-chapter searches. This runs after the
  // main Search renderer and collapses verse cards into one continuous chapter.
  const chapterReadingRuntime=document.createElement('script');
  chapterReadingRuntime.src='/dore/dore-chapter-reading.js?v=chapter-20260823a';
  chapterReadingRuntime.defer=true;
  document.head.appendChild(chapterReadingRuntime);

  // BW-1 entity intelligence is a separate runtime so it can evolve without
  // coupling the Scripture reader/search implementation to Biblical World.
  const entityRuntime=document.createElement('script');
  entityRuntime.src='/dore/dore-entity-search.js?v=bw1-20260822b';
  entityRuntime.defer=true;
  document.head.appendChild(entityRuntime);

  const R=window.ONE_DORE_COVER_REGISTRY;
  if(!R?.files)return;
  const front=document.getElementById('dore-plate-a');
  const back=document.getElementById('dore-plate-b');
  const credit=document.getElementById('dore-plate-credit');
  if(!front||!back)return;
  const ids=Array.from({length:241},(_,i)=>i+1).filter(id=>R.files[id]);
  if(!ids.length)return;
  const SCAN_MS=15000;
  let pos=0,active=front,inactive=back,timer=0;
  const srcFor=id=>`https://commons.wikimedia.org/wiki/Special:Redirect/file/${encodeURIComponent(R.files[id])}?width=1600`;
  const titleFor=id=>R.titles?.[id]||String(R.files[id]).replace(/^\d+[A-Z]?\.?/,'').replace(/\.(?:jpg|jpeg|png|gif)$/i,'');
  const preload=id=>{const img=new Image();img.src=srcFor(id)};
  const setPlate=(img,id)=>{
    img.classList.remove('is-active');
    img.style.objectPosition='center top';
    img.src=srcFor(id);
    img.alt=`Gustave Doré — ${titleFor(id)}`;
    img.dataset.doreId=String(id).padStart(3,'0');
  };
  const showCredit=id=>{if(credit)credit.textContent=`Doré ${String(id).padStart(3,'0')} · ${titleFor(id)}`};
  const startScan=img=>{
    img.classList.add('is-active');
    img.style.objectPosition='center top';
    requestAnimationFrame(()=>requestAnimationFrame(()=>{img.style.objectPosition='center bottom'}));
  };
  const advance=()=>{
    pos=(pos+1)%ids.length;
    const id=ids[pos],next=ids[(pos+1)%ids.length];
    setPlate(inactive,id);
    requestAnimationFrame(()=>{
      active.classList.remove('is-active');
      startScan(inactive);
      [active,inactive]=[inactive,active];
      showCredit(id);
      preload(next);
      timer=setTimeout(advance,SCAN_MS);
    });
  };
  setPlate(active,ids[0]);
  startScan(active);
  showCredit(ids[0]);
  preload(ids[1%ids.length]);
  if(matchMedia('(prefers-reduced-motion: reduce)').matches){active.style.objectPosition='center center';return;}
  timer=setTimeout(advance,SCAN_MS);
})();
