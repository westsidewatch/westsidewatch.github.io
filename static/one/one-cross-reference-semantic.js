/* ONE cross-reference Scripture renderer.
 * Scripture text is resolved from in-repository ONE_SCRIPTURE_LOCAL.
 * Historical third-field summaries/notes are never trusted as Scripture.
 */
(()=>{
  'use strict';

  let scriptureReady=null;
  const canonical=value=>String(value||'')
    .trim()
    .replace(/：/g,':')
    .replace(/[—－-]/g,'–')
    .replace(/\s+/g,' ')
    .replace(/\s*:\s*/g,':')
    .replace(/\s*–\s*/g,'–');

  function ensureLocalScripture(){
    if(window.ONE_SCRIPTURE_LOCAL)return Promise.resolve(window.ONE_SCRIPTURE_LOCAL);
    if(scriptureReady)return scriptureReady;
    scriptureReady=new Promise((resolve,reject)=>{
      const existing=document.querySelector('script[data-one-scripture-local],script[src*="one-scripture-local.js"]');
      if(existing){
        if(window.ONE_SCRIPTURE_LOCAL){resolve(window.ONE_SCRIPTURE_LOCAL);return;}
        existing.addEventListener('load',()=>resolve(window.ONE_SCRIPTURE_LOCAL||{}),{once:true});
        existing.addEventListener('error',reject,{once:true});
        setTimeout(()=>resolve(window.ONE_SCRIPTURE_LOCAL||{}),250);
        return;
      }
      const script=document.createElement('script');
      script.src='./one-scripture-local.js?v=20260816d';
      script.dataset.oneScriptureLocal='true';
      script.onload=()=>resolve(window.ONE_SCRIPTURE_LOCAL||{});
      script.onerror=reject;
      document.head.append(script);
    });
    return scriptureReady;
  }

  function localText(reference){
    const map=window.ONE_SCRIPTURE_LOCAL||{};
    const key=canonical(reference);
    const exact=Object.keys(map).find(item=>canonical(item)===key);
    return exact?String(map[exact]||'').trim():'';
  }

  function ensureQuote(article){
    let quote=article.querySelector('blockquote.connection-scripture, blockquote');
    if(!quote){quote=document.createElement('blockquote');article.append(quote);}
    quote.className='connection-scripture';
    return quote;
  }

  async function populate(root=document){
    try{await ensureLocalScripture();}catch(error){return;}
    root.querySelectorAll('.connection-section .connection-grid article').forEach(article=>{
      const reference=article.querySelector('header strong')?.textContent?.trim()||'';
      const text=localText(reference);
      const quote=ensureQuote(article);

      /* Never leave historical editorial copy in the Scripture position. */
      quote.textContent='';
      quote.hidden=true;
      article.classList.add('connection-scripture-pending');
      article.classList.remove('connection-scripture-ready');

      if(!text)return;

      quote.textContent=`「${text}」`;
      quote.hidden=false;
      quote.removeAttribute('aria-hidden');
      quote.style.removeProperty('display');
      quote.style.removeProperty('visibility');
      article.classList.remove('connection-scripture-pending','connection-without-scripture');
      article.classList.add('connection-scripture-ready');
      article.dataset.scriptureSource='ONE-local-CUV';
    });
  }

  const rerender=()=>populate(document.querySelector('#chapter-detail')||document);

  /* Render immediately and retry after the ONE app has had a chance to build
   * or replace the current chapter. This deliberately does not rely on one
   * observer timing edge. */
  [0,50,150,400,900,1800].forEach(delay=>setTimeout(rerender,delay));

  const target=document.querySelector('#chapter-detail');
  if(target){
    let timer=0;
    new MutationObserver(()=>{
      clearTimeout(timer);
      timer=setTimeout(rerender,0);
    }).observe(target,{childList:true,subtree:true});
  }

  document.addEventListener('click',event=>{
    if(event.target.closest('[data-turn-chapter],.chapter-grid button,[data-open-chapter]')){
      setTimeout(rerender,0);
      setTimeout(rerender,120);
    }
  },true);
  window.addEventListener('pageshow',rerender);
})();
