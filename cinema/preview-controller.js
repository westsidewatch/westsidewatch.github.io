(()=>{
  const HOVER_DELAY=420;
  const HOVER_EXIT_DELAY=120;
  const previewTimers=new WeakMap();
  const exitTimers=new WeakMap();

  function youtubeId(source){
    try{
      const url=new URL(source.embedUrl||source.url||'',window.location.href);
      if(url.hostname.includes('youtube.com')){
        if(url.pathname.startsWith('/embed/'))return url.pathname.split('/')[2]||'';
        return url.searchParams.get('v')||'';
      }
      if(url.hostname==='youtu.be')return url.pathname.slice(1);
    }catch(_error){}
    return '';
  }

  function sourceFor(item){return (item.providerSources||[])[0]||{};}

  function previewSpec(item){
    const source=sourceFor(item);
    const declared=source.preview||{};
    if(declared.posterUrl)return {...declared,provider:source.provider,source};
    if(source.provider==='youtube'){
      const id=youtubeId(source);
      if(!id)return null;
      return {
        provider:'youtube',
        source,
        posterUrl:`https://i.ytimg.com/vi/${id}/hqdefault.jpg`,
        hoverPreview:true,
        previewStartSeconds:0
      };
    }
    return null;
  }

  function previewIframe(spec){
    if(spec.provider!=='youtube')return null;
    const id=youtubeId(spec.source);
    if(!id)return null;
    const url=new URL(`https://www.youtube-nocookie.com/embed/${id}`);
    url.searchParams.set('autoplay','1');
    url.searchParams.set('mute','1');
    url.searchParams.set('controls','0');
    url.searchParams.set('playsinline','1');
    url.searchParams.set('rel','0');
    url.searchParams.set('modestbranding','1');
    const start=Math.max(0,Number(spec.previewStartSeconds||0));
    if(start)url.searchParams.set('start',String(Math.floor(start)));
    const frame=document.createElement('iframe');
    frame.src=url.toString();
    frame.title='Silent video preview';
    frame.loading='eager';
    frame.allow='autoplay; encrypted-media; picture-in-picture';
    frame.referrerPolicy='strict-origin-when-cross-origin';
    frame.tabIndex=-1;
    return frame;
  }

  function stopPreview(surface){
    clearTimeout(previewTimers.get(surface));
    clearTimeout(exitTimers.get(surface));
    exitTimers.set(surface,setTimeout(()=>{
      surface.querySelector('iframe')?.remove();
      surface.classList.remove('is-previewing');
    },HOVER_EXIT_DELAY));
  }

  function startPreview(surface,spec){
    clearTimeout(exitTimers.get(surface));
    if(!spec.hoverPreview||window.matchMedia('(hover: none)').matches||window.matchMedia('(prefers-reduced-motion: reduce)').matches)return;
    clearTimeout(previewTimers.get(surface));
    previewTimers.set(surface,setTimeout(()=>{
      if(surface.querySelector('iframe'))return;
      const frame=previewIframe(spec);
      if(!frame)return;
      surface.appendChild(frame);
      requestAnimationFrame(()=>surface.classList.add('is-previewing'));
    },HOVER_DELAY));
  }

  function activateSurface(surface){
    const card=surface.closest('.resource-card');
    const action=card?.querySelector('.resource-action');
    if(action)action.click();
  }

  function installResourcePreviews(resources){
    for(const item of resources){
      if(item.canonicalId==='cinema:video:jesus-film:jesus')continue;
      const card=document.querySelector(`.resource-card[data-canonical-id="${CSS.escape(item.canonicalId)}"]`);
      if(!card||card.querySelector('.resource-preview'))continue;
      const spec=previewSpec(item);
      if(!spec?.posterUrl)continue;
      const surface=document.createElement('div');
      surface.className='resource-preview';
      surface.tabIndex=0;
      surface.setAttribute('role','button');
      surface.setAttribute('aria-label',`播放 ${item.title}`);
      const image=document.createElement('img');
      image.src=spec.posterUrl;
      image.alt='';
      image.loading='lazy';
      image.referrerPolicy='no-referrer';
      surface.appendChild(image);
      surface.addEventListener('pointerenter',()=>startPreview(surface,spec));
      surface.addEventListener('pointerleave',()=>stopPreview(surface));
      surface.addEventListener('focus',()=>startPreview(surface,spec));
      surface.addEventListener('blur',()=>stopPreview(surface));
      surface.addEventListener('click',()=>activateSurface(surface));
      surface.addEventListener('keydown',event=>{
        if(event.key==='Enter'||event.key===' '){event.preventDefault();activateSurface(surface);}
      });
      card.prepend(surface);
    }
  }

  function installJesusPoster(item){
    const poster=document.querySelector('.living-poster__poster');
    if(!poster||poster.dataset.previewReady==='true')return;
    const spec=previewSpec(item);
    if(!spec?.posterUrl)return;
    poster.dataset.previewReady='true';
    poster.style.backgroundImage=`linear-gradient(180deg,rgba(8,8,7,.04),rgba(8,8,7,.20)),url("${spec.posterUrl}")`;
    poster.style.backgroundSize='cover';
    poster.style.backgroundPosition='center';
    poster.setAttribute('role','button');
    poster.setAttribute('tabindex','0');
    poster.setAttribute('aria-label','播放 JESUS');
    poster.removeAttribute('aria-hidden');
    poster.querySelector('.living-poster__play-mark')?.remove();
    poster.addEventListener('click',()=>poster.closest('.living-poster')?.querySelector('[data-action="watch"]')?.click());
    poster.addEventListener('keydown',event=>{
      if(event.key==='Enter'||event.key===' '){
        event.preventDefault();
        poster.closest('.living-poster')?.querySelector('[data-action="watch"]')?.click();
      }
    });
  }

  async function install(){
    try{
      const response=await fetch('data/video-resource.v0.json',{cache:'no-store'});
      if(!response.ok)return;
      const payload=await response.json();
      const resources=Array.isArray(payload.items)?payload.items:[];
      const jesus=resources.find(item=>item.canonicalId==='cinema:video:jesus-film:jesus');
      let tries=0;
      const waitForCards=()=>{
        const ready=document.querySelector('.living-poster')&&document.querySelector('.resource-card');
        if(ready){
          if(jesus)installJesusPoster(jesus);
          installResourcePreviews(resources);
          document.documentElement.dataset.cinemaPreviewLayer='v1';
          return;
        }
        if(tries++<80)requestAnimationFrame(waitForCards);
      };
      waitForCards();
    }catch(_error){}
  }

  install();
})();
