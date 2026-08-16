/* ONE cross-reference Scripture renderer.
 * Scripture text is resolved from in-repository ONE_SCRIPTURE_LOCAL first.
 * Historical third-field summaries/notes are never trusted as Scripture.
 */
(()=>{
  'use strict';
  let runId=0;
  const canonical=value=>String(value||'').trim().replace(/：/g,':').replace(/[—－-]/g,'–').replace(/\s+/g,' ');

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

  function populate(root=document){
    ++runId;
    root.querySelectorAll('.connection-section .connection-grid article').forEach(article=>{
      const reference=article.querySelector('header strong')?.textContent?.trim()||'';
      const text=localText(reference);
      const quote=ensureQuote(article);
      /* Never show historical editorial copy in the Scripture slot. */
      quote.textContent='';
      quote.hidden=true;
      article.classList.add('connection-scripture-pending');
      if(!text)return;
      quote.textContent=`「${text}」`;
      quote.hidden=false;
      article.classList.remove('connection-scripture-pending','connection-without-scripture');
      article.dataset.scriptureSource='ONE-local-CUV';
    });
  }

  populate();
  const target=document.querySelector('#chapter-detail');
  if(target){
    let scheduled=false;
    new MutationObserver(()=>{
      if(scheduled)return;
      scheduled=true;
      queueMicrotask(()=>{scheduled=false;populate(target)});
    }).observe(target,{childList:true,subtree:false});
  }
})();
