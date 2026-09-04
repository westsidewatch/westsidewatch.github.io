(()=>{
  'use strict';

  const unlockSearch=()=>{
    const input=document.getElementById('search-input');
    const button=document.getElementById('search-button');
    if(input)input.disabled=false;
    if(button)button.disabled=false;
  };

  const placeSearchMeta=()=>{
    const shell=document.querySelector('.search-shell');
    const examples=shell?.querySelector('.examples');
    const status=shell?.querySelector('#search-status');
    if(!shell||(!examples&&!status))return;
    let meta=document.querySelector('.dore-search-meta');
    if(!meta){meta=document.createElement('div');meta.className='dore-search-meta';shell.insertAdjacentElement('afterend',meta)}
    if(examples)meta.appendChild(examples);
    if(status)meta.appendChild(status);
    if(!document.getElementById('dore-search-meta-style')){
      const style=document.createElement('style');style.id='dore-search-meta-style';style.textContent=`
        .dore-search-meta{width:min(68vw,1080px);margin:3.7vw auto 0;text-align:center;position:relative;z-index:4}
        .dore-search-meta .examples{margin:0;font-size:clamp(.7rem,.74vw,.82rem);line-height:2}
        .dore-search-meta #search-status{display:none!important}
        .cap span{white-space:nowrap}
        @media(max-width:820px){.dore-search-meta{width:calc(100% - 24px);margin-top:28px}.cap span{white-space:normal}}
      `;document.head.appendChild(style)
    }
  };

  const boot=()=>{unlockSearch();placeSearchMeta()};
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();

  const intelligenceRuntime=document.createElement('script');
  intelligenceRuntime.src='/dore/dore-bible-intelligence.js?v=search2-20260904a';
  intelligenceRuntime.async=false;
  intelligenceRuntime.onload=()=>{
    const openCrossrefs=document.createElement('script');
    openCrossrefs.src='/dore/dore-open-crossrefs.js?v=neuu-openbible-20260904a';
    openCrossrefs.async=false;
    document.head.appendChild(openCrossrefs);
  };
  document.head.appendChild(intelligenceRuntime);

  const brainRuntime=document.createElement('script');
  brainRuntime.src='/dore/dore-brain-bridge.js?v=brain-bridge-20260823a';
  brainRuntime.async=false;
  document.head.appendChild(brainRuntime);

  const parserRuntime=document.createElement('script');
  parserRuntime.src='/dore/dore-scripture-reference-parser.js?v=ssl1-20260823a';
  parserRuntime.onload=()=>{
    const inputLiteracyRuntime=document.createElement('script');
    inputLiteracyRuntime.src='/dore/dore-search-input-literacy.js?v=ssl1-20260823c';
    inputLiteracyRuntime.onload=()=>{
      const chapterReadingRuntime=document.createElement('script');
      chapterReadingRuntime.src='/dore/dore-chapter-reading.js?v=chapter-20260823b';
      document.head.appendChild(chapterReadingRuntime)
    };
    document.head.appendChild(inputLiteracyRuntime)
  };
  document.head.appendChild(parserRuntime);
  const entityRuntime=document.createElement('script');entityRuntime.src='/dore/dore-entity-search.js?v=bw1-20260822b';entityRuntime.defer=true;document.head.appendChild(entityRuntime);

  const R=window.ONE_DORE_COVER_REGISTRY;
  if(!R?.files)return;
  const front=document.getElementById('dore-plate-a'),back=document.getElementById('dore-plate-b'),credit=document.getElementById('dore-plate-credit');
  if(!front||!back)return;
  const ids=Array.from({length:241},(_,i)=>i+1).filter(id=>R.files[id]);
  if(!ids.length)return;
  const SCAN_MS=15000;
  let pos=0,active=front,inactive=back,timer=0,generation=0;
  const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
  const srcFor=id=>`https://commons.wikimedia.org/wiki/Special:Redirect/file/${encodeURIComponent(R.files[id])}?width=1600`;
  const titleFor=id=>R.titles?.[id]||String(R.files[id]).replace(/^\d+[A-Z]?\.?/,'').replace(/\.(?:jpg|jpeg|png|gif)$/i,'');
  const preload=id=>{const img=new Image();img.src=srcFor(id)};
  const showCredit=id=>{if(credit)credit.textContent=`Doré ${String(id).padStart(3,'0')} · ${titleFor(id)}`};

  const resetPlate=img=>{
    img.classList.remove('is-active');
    img.style.transition='none';
    img.style.objectPosition='center top';
    img.style.transformOrigin='center top';
    img.style.transform='translateY(0) scale(1.10)';
    void img.offsetHeight;
  };

  const beginScan=img=>{
    img.classList.add('is-active');
    if(reduced){img.style.transition='opacity .35s ease';img.style.transform='translateY(0) scale(1.04)';return}
    img.style.transition='opacity .9s ease, transform 15s linear';
    void img.offsetHeight;
    requestAnimationFrame(()=>requestAnimationFrame(()=>{
      img.style.transform='translateY(-9%) scale(1.10)';
    }));
  };

  const loadPlate=(img,id,token,done)=>{
    resetPlate(img);
    img.alt=`Gustave Doré — ${titleFor(id)}`;
    img.dataset.doreId=String(id).padStart(3,'0');
    let fired=false;
    const ready=()=>{
      if(fired||token!==generation)return;
      fired=true;
      img.onload=null;img.onerror=null;
      resetPlate(img);
      requestAnimationFrame(()=>done());
    };
    img.onload=ready;
    img.onerror=()=>{if(token!==generation)return;img.onload=null;img.onerror=null;setTimeout(ready,250)};
    img.src=srcFor(id);
    if(img.complete&&img.naturalWidth)queueMicrotask(ready);
  };

  const scheduleNext=()=>{clearTimeout(timer);timer=setTimeout(advance,SCAN_MS)};
  const advance=()=>{
    const token=++generation;
    pos=(pos+1)%ids.length;
    const id=ids[pos],next=ids[(pos+1)%ids.length];
    loadPlate(inactive,id,token,()=>{
      active.classList.remove('is-active');
      beginScan(inactive);
      [active,inactive]=[inactive,active];
      showCredit(id);
      preload(next);
      if(!reduced)scheduleNext();
    });
  };

  const firstToken=++generation;
  loadPlate(active,ids[0],firstToken,()=>{
    beginScan(active);
    showCredit(ids[0]);
    preload(ids[1%ids.length]);
    if(!reduced)scheduleNext();
  });
})();