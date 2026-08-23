(()=>{
  'use strict';
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
