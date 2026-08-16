/* ONE cross-reference Scripture loader.
 * Every cross-reference card must render real Bible text in the Scripture slot.
 * Historical third-field summaries/notes are never trusted as Scripture.
 * Text is loaded from the public-domain Traditional Chinese Union Version.
 */
(()=>{
  'use strict';

  const DATA_URL='https://cdn.jsdelivr.net/gh/m0ty/bible-io-json@main/Chinese/zho-cuv-trad-shen.json';
  let biblePromise=null;
  let runId=0;

  const normalize=value=>String(value||'').replace(/[\s　]/g,'').replace(/壹/g,'一').replace(/貳/g,'二').replace(/參/g,'三');

  function parseReference(label){
    const value=String(label||'').trim().replace(/：/g,':').replace(/[—－]/g,'–');
    const match=value.match(/^(.+?)\s+(\d+)(?:(?::(\d+)(?:[–-](\d+))?)|(?:[–-](\d+))章?|章)?$/);
    if(!match)return null;
    return {
      book:match[1].trim(),
      chapter:Number(match[2]),
      verseStart:match[3]?Number(match[3]):null,
      verseEnd:match[4]?Number(match[4]):null,
      chapterEnd:match[5]?Number(match[5]):null
    };
  }

  async function loadBible(){
    if(!biblePromise){
      biblePromise=fetch(DATA_URL,{cache:'force-cache'}).then(response=>{
        if(!response.ok)throw new Error(`CUV ${response.status}`);
        return response.json();
      });
    }
    return biblePromise;
  }

  function findBook(data,name){
    const target=normalize(name);
    return Object.values(data?.books||{}).find(book=>normalize(book?.name)===target)||null;
  }

  function verseText(chapter,verse){
    return String(chapter?.[String(verse)]||chapter?.[verse]||'').trim();
  }

  function selectVerses(book,ref){
    const chapters=book?.chapters||{};
    const first=chapters[String(ref.chapter)]||chapters[ref.chapter];
    if(!first)return [];

    /* Explicit verse reference: quote the exact range. Long ranges are excerpted
     * from both ends so the card stays readable while every displayed word is
     * still Scripture rather than an editorial summary. */
    if(ref.verseStart){
      const end=ref.verseEnd||ref.verseStart;
      const numbers=[];
      if(end-ref.verseStart<=5){
        for(let v=ref.verseStart;v<=end;v++)numbers.push(v);
      }else{
        numbers.push(ref.verseStart,ref.verseStart+1,end-1,end);
      }
      return numbers.map(v=>({chapter:ref.chapter,verse:v,text:verseText(first,v)})).filter(item=>item.text);
    }

    /* Chapter-level references are contextual references. Show the opening
     * verses as an actual Scripture excerpt instead of inventing a summary. */
    const lastChapter=ref.chapterEnd||ref.chapter;
    if(lastChapter!==ref.chapter){
      const last=chapters[String(lastChapter)]||chapters[lastChapter];
      return [
        {chapter:ref.chapter,verse:1,text:verseText(first,1)},
        {chapter:ref.chapter,verse:2,text:verseText(first,2)},
        {chapter:lastChapter,verse:1,text:verseText(last,1)},
        {chapter:lastChapter,verse:2,text:verseText(last,2)}
      ].filter(item=>item.text);
    }
    return [1,2,3].map(v=>({chapter:ref.chapter,verse:v,text:verseText(first,v)})).filter(item=>item.text);
  }

  function scriptureString(items){
    if(!items.length)return '';
    return items.map((item,index)=>{
      const previous=items[index-1];
      const gap=previous&&(item.chapter!==previous.chapter||item.verse>previous.verse+1);
      return `${gap?'… ':''}${item.text}`;
    }).join(' ');
  }

  function clearHistoricalText(root=document){
    root.querySelectorAll('.connection-section .connection-grid article').forEach(article=>{
      let quote=article.querySelector('blockquote');
      if(!quote){
        quote=document.createElement('blockquote');
        article.append(quote);
      }
      quote.className='connection-scripture';
      quote.textContent='';
      quote.hidden=true;
      article.classList.add('connection-scripture-pending');
      article.classList.remove('connection-without-scripture');
    });
  }

  async function populate(root=document){
    const id=++runId;
    clearHistoricalText(root);
    const cards=[...root.querySelectorAll('.connection-section .connection-grid article')];
    if(!cards.length)return;
    let data;
    try{data=await loadBible()}catch(error){return}
    if(id!==runId)return;

    cards.forEach(article=>{
      const reference=article.querySelector('header strong')?.textContent?.trim()||'';
      const parsed=parseReference(reference);
      const quote=article.querySelector('blockquote');
      if(!parsed||!quote)return;
      const book=findBook(data,parsed.book);
      const text=scriptureString(selectVerses(book,parsed));
      if(!text)return;
      quote.textContent=`「${text}」`;
      quote.hidden=false;
      article.classList.remove('connection-scripture-pending');
      article.dataset.scriptureSource='CUV-public-domain';
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
    }).observe(target,{childList:true});
  }
})();
