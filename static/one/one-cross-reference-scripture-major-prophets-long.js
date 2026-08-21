/* ONE — long major-prophet Scripture references.
 * Loads only exact requested Public Domain Chinese Union Traditional (cut) passages.
 * Commentary is never promoted into Scripture.
 */
(()=>{
  "use strict";
  const D=window.ONE_DATA;if(!D?.studyBooks)return;
  const API='https://api.getbible.net/v2/cut';
  const chapter=async(book,ch)=>{
    const r=await fetch(`${API}/${book}/${ch}.json`,{mode:'cors'});
    if(!r.ok)throw new Error(`Scripture fetch ${book}/${ch}: ${r.status}`);
    const d=await r.json();
    return Array.isArray(d?.verses)?d.verses:[];
  };
  const text=verses=>verses.map(v=>String(v?.text||'').trim()).join('');
  const fillExact=(refs)=>{
    let filled=0;
    for(const bookNo of [24,25,26,27]){
      Object.values(D.studyBooks?.[bookNo]?.chapterStudies||{}).forEach(study=>{
        (Array.isArray(study?.connections)?study.connections:[]).forEach(row=>{
          if(!Array.isArray(row)||String(row[3]||'').trim())return;
          const scripture=refs[String(row[0]||'').trim()];
          if(scripture){row[3]=scripture;filled++;}
        });
      });
    }
    return filled;
  };
  window.ONE_MAJOR_PROPHETS_LONG_SCRIPTURE={status:'loading',filled:0,references:[]};
  Promise.all([
    chapter(12,22),chapter(12,23),chapter(12,24),chapter(12,25),
    chapter(24,52),chapter(66,13),chapter(66,21),chapter(66,22)
  ]).then(([k22,k23,k24,k25,jer52,rev13,rev21,rev22])=>{
    const refs={
      '列王紀下 22–25':text([...k22,...k23,...k24,...k25]),
      '列王紀下 25:1–21':text(k25.filter(v=>Number(v?.verse)<=21)),
      '耶利米書 52':text(jer52),
      '啟示錄 21–22':text([...rev21,...rev22]),
      '啟示錄 13':text(rev13)
    };
    const filled=fillExact(refs);
    window.ONE_MAJOR_PROPHETS_LONG_SCRIPTURE={status:'ready',filled,references:Object.keys(refs)};
    document.documentElement.dataset.oneMajorProphetsLongScripture=`PASS:${filled}`;
  }).catch(error=>{
    window.ONE_MAJOR_PROPHETS_LONG_SCRIPTURE={status:'error',filled:0,references:[],error:String(error)};
    document.documentElement.dataset.oneMajorProphetsLongScripture='FAIL';
    console.error('ONE long major-prophet Scripture load failed',error);
  });
})();
