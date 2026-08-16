/* ONE cross-reference semantic guard.
 * Existing study data historically stores the third connection field as either
 * a quoted scripture excerpt OR an editorial note.  Do not present editorial
 * guidance as if it were Scripture.
 */
(()=>{
  'use strict';

  const NOTE_PATTERNS=[
    /^把本篇/,
    /^把本章/,
    /^把這篇/,
    /^把這章/,
    /^把本段/,
    /^把這段/,
    /^本節/,
    /^本段/,
    /^本處/,
    /^這段經文/,
    /^此處/,
    /^這裡(?:的|把|與|可|用)/,
    /放回.*(?:聖經|救贖|敬拜|歷史|脈絡|處境).*(?:閱讀|理解|研讀)/
  ];

  const isEditorialNote=text=>{
    const value=String(text||'').trim();
    return value!==''&&NOTE_PATTERNS.some(pattern=>pattern.test(value));
  };

  function normalizeConnectionSection(root=document){
    root.querySelectorAll('.connection-section .connection-grid article').forEach(article=>{
      const quote=article.querySelector('blockquote');
      if(!quote)return;
      const text=quote.textContent.trim();
      if(isEditorialNote(text)){
        const note=document.createElement('p');
        note.className='connection-note';
        note.textContent=text;
        quote.replaceWith(note);
      }else{
        quote.classList.add('connection-scripture');
      }
    });
  }

  normalizeConnectionSection();
  const target=document.querySelector('#chapter-detail');
  if(target){
    new MutationObserver(()=>normalizeConnectionSection(target)).observe(target,{childList:true,subtree:true});
  }
})();
