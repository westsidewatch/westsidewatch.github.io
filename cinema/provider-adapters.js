(()=>{
  if(!document.querySelector('link[data-cinema-inline-player]')){
    const style=document.createElement('link');
    style.rel='stylesheet';
    style.href='inline-player.css';
    style.dataset.cinemaInlinePlayer='true';
    document.head.appendChild(style);
  }
})();

window.HolyLightProviders={
  resolve(item,startSeconds=0){
    const source=(item.providerSources||[])[0]||{};
    if(source.embed&&source.embedUrl){
      const url=new URL(source.embedUrl,window.location.href);
      if(startSeconds>0){
        if(source.provider==='youtube')url.searchParams.set('start',String(startSeconds));
        else if(source.startParam)url.searchParams.set(source.startParam,String(startSeconds));
      }
      if(source.provider==='youtube')url.searchParams.set('autoplay','1');if(source.provider==='jesus-film-project-arclight'){if(!url.searchParams.has('apiSessionId')){const seed=globalThis.crypto?.randomUUID?.()||`${Date.now().toString(16)}.${Math.floor(Math.random()*0x10000000).toString(16)}`;url.searchParams.set('apiSessionId',seed.replace(/-/g,''));}if(!url.searchParams.has('playerStyle'))url.searchParams.set('playerStyle','default');if(!url.searchParams.has('player'))url.searchParams.set('player','bc.vanilla5');}
      return{kind:'embed',provider:source.provider,url:url.toString(),official:!!source.official};
    }
    if(source.url){
      const url=new URL(source.url,window.location.href);
      if(startSeconds>0&&source.provider==='youtube')url.searchParams.set('t',`${startSeconds}s`);
      return{kind:'handoff',provider:source.provider,url:url.toString(),official:!!source.official};
    }
    return null;
  },
  mount(target,item,startSeconds=0){
    const resolved=this.resolve(item,startSeconds);
    if(!resolved||resolved.kind!=='embed')return null;
    target.replaceChildren();
    const frame=document.createElement('iframe');
    frame.src=resolved.url;
    frame.title=`${item.title} — official embedded player`;
    frame.loading='eager';
    frame.referrerPolicy='strict-origin-when-cross-origin';
    frame.allow='autoplay; fullscreen; picture-in-picture; encrypted-media';
    frame.allowFullscreen=true;
    frame.dataset.provider=resolved.provider||'unknown';
    target.appendChild(frame);
    return{frame,resolved};
  }
};
