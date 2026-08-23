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
    if(!meta){
      meta=document.createElement('div');
      meta.className='dore-search-meta';
      shell.insertAdjacentElement('afterend',meta);
    }
    if(examples)meta.appendChild(examples);
    if(status)meta.appendChild(status);
    if(!document.getElementById('dore-search-meta-style')){
      const style=document.createElement('style');
      style.id='dore-search-meta-style';
      style.textContent=`
        .dore-search-meta{width:min(68vw,1080px);margin:3.7vw auto 0;text-align:center;position:relative;z-index:4}
        .dore-search-meta .examples{margin:0;font-size:clamp(.7rem,.74vw,.82rem);line-height:2}
        .dore-search-meta #search-status{margin:.45vw 0 0;font-size:clamp(.62rem,.65vw,.74rem);opacity:.58}
        @media(max-width:820px){.dore-search-meta{width:calc(100% - 24px);margin-top:28px}.dore-search-meta #search-status{margin-top:6px}}
      `;
      document.head.appendChild(style);
    }
  };

  const boot=()=>{unlockSearch();placeSearchMeta();};
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});
  else boot();

  const parserRuntime=document.createElement('script');
  parserRuntime.src='/dore/dore-scripture-reference-parser.js?v=ssl1-20260823a';
  parserRuntime.onload=()=>{
    const inputLiteracyRuntime=document.createElement('script');
    inputLiteracyRuntime.src='/dore/dore-search-input-literacy.js?v=ssl1-20260823c';
    inputLiteracyRuntime.onload=()=>{
      const chapterReadingRuntime=document.createElement('script');
      chapterReadingRuntime.src='/dore/dore-chapter-reading.js?v=chapter-20260823b';
      document.head.appendChild(chapterReadingRuntime);
    };
    document.head.appendChild(inputLiteracyRuntime);
  };
  document.head.appendChild(parserRuntime);

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
