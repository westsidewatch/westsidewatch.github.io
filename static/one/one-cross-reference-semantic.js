/* ONE cross-reference semantic guard.
 * The historical connection tuple mixes real Scripture excerpts and editorial
 * study guidance in its third field. Only real Scripture may occupy the quoted
 * Scripture slot. Editorial guidance is removed from that slot entirely.
 */
(()=>{
  'use strict';

  const NOTE_PATTERNS=[
    /^把(?:本|這)(?:篇|章|段|節)/,
    /^(?:本|這)(?:篇|章|段|節|處)(?:經文)?(?:與|把|可|是|在|要|宜|應|需|提醒|幫助|提供|呼應|連到|指向|放在|放回|需要|可以)/,
    /^此處(?:與|把|可|是|在|要|宜|應|需|提醒|幫助|提供|呼應|連到|指向|放在|放回)/,
    /^這裡(?:的|把|與|可|用|是|在|要|宜|應|需|提醒|幫助|提供|呼應|連到|指向)/,
    /^(?:比較|參照|對照|留意|注意|觀察|閱讀|研讀|理解|思想|辨認|可見|可比較|可參照|可對照|幫助|提醒|說明)/,
    /放回.*(?:聖經|救贖|敬拜|歷史|脈絡|處境).*(?:閱讀|理解|研讀)/,
    /(?:與|和).*(?:形成|構成|互相|彼此)?(?:呼應|對照|串連|連結).*(?:閱讀|理解|主題|脈絡)?$/,
    /(?:提供|說明|幫助我們|提醒我們).*(?:背景|脈絡|理解|閱讀|研讀)/
  ];

  const isEditorialNote=text=>{
    const value=String(text||'').trim().replace(/^[「『“\"]|[」』”\"]$/g,'');
    return value!==''&&NOTE_PATTERNS.some(pattern=>pattern.test(value));
  };

  function normalizeConnectionSection(root=document){
    root.querySelectorAll('.connection-section .connection-grid article').forEach(article=>{
      const quote=article.querySelector('blockquote');
      if(!quote)return;
      const text=quote.textContent.trim();
      if(isEditorialNote(text)){
        /* A study note is useful metadata, but it must never masquerade as a
         * Bible quotation. The card already retains its reference and relation
         * label, so remove the non-Scripture third field from the verse slot. */
        quote.remove();
        article.classList.add('connection-without-scripture');
      }else{
        quote.classList.add('connection-scripture');
        article.classList.remove('connection-without-scripture');
      }
    });
  }

  normalizeConnectionSection();
  const target=document.querySelector('#chapter-detail');
  if(target){
    new MutationObserver(()=>normalizeConnectionSection(target)).observe(target,{childList:true,subtree:true});
  }
})();
