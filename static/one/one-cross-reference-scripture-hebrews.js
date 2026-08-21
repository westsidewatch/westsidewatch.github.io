/* ONE — reviewed Scripture fill for Hebrews 1–13.
 * Public-domain Chinese Union Traditional text is loaded by exact reference only.
 * Explanation text in field 3 is never promoted into Scripture field 4.
 */
(()=>{
  "use strict";
  const D=window.ONE_DATA;if(!D?.studyBooks?.[58])return;
  const API='https://api.getbible.net/v2/cut';
  const bookNumbers={
    '創世記':1,'出埃及記':2,'利未記':3,'民數記':4,'申命記':5,'約書亞記':6,
    '撒母耳記下':10,'詩篇':19,'箴言':20,'以賽亞書':23,'耶利米書':24,'哈該書':37
  };
  const refs=[
    '詩篇 2:7','詩篇 110:1','撒母耳記下 7:14',
    '詩篇 8:4–6','詩篇 22:22','以賽亞書 8:18',
    '民數記 12:7','詩篇 95:7–11','出埃及記 17:1–7',
    '創世記 2:2','詩篇 95:7–11','約書亞記 21:43–45',
    '詩篇 2:7','詩篇 110:4','創世記 14:18–20',
    '創世記 22:16–18','利未記 16:2','詩篇 110:4',
    '創世記 14:18–20','詩篇 110:4','民數記 18:21',
    '耶利米書 31:31–34','出埃及記 24:7–8','出埃及記 25:8–9',
    '出埃及記 25–26','利未記 16','出埃及記 24:8',
    '詩篇 40:6–8','耶利米書 31:33–34','申命記 32:35–36',
    '創世記 12:1–4','創世記 22:1–18','出埃及記 2–14','約書亞記 2',
    '箴言 3:11–12','哈該書 2:6','申命記 4:24',
    '利未記 16:27','詩篇 118:6','申命記 31:6'
  ];
  const unique=[...new Set(refs)];
  const chapterCache=new Map();
  const fetchChapter=async(book,ch)=>{
    const key=`${book}/${ch}`;
    if(!chapterCache.has(key))chapterCache.set(key,fetch(`${API}/${book}/${ch}.json`,{mode:'cors'}).then(r=>{if(!r.ok)throw new Error(`CUV ${key} ${r.status}`);return r.json();}).then(d=>Array.isArray(d?.verses)?d.verses:[]));
    return chapterCache.get(key);
  };
  const verseText=verses=>verses.map(v=>String(v?.text||'').trim()).join('');
  const resolve=async ref=>{
    const m=ref.match(/^(.+?)\s+(\d+)(?:(:)(\d+)(?:[–-](\d+))?|[–-](\d+))?$/);
    if(!m)throw new Error(`Unsupported reference: ${ref}`);
    const [,bookName,startChapter,colon,startVerse,endVerse,endChapter]=m;
    const book=bookNumbers[bookName];if(!book)throw new Error(`Unknown book: ${bookName}`);
    const c1=Number(startChapter);
    if(colon){
      const verses=await fetchChapter(book,c1),v1=Number(startVerse),v2=endVerse?Number(endVerse):v1;
      return verseText(verses.filter(v=>Number(v?.verse)>=v1&&Number(v?.verse)<=v2));
    }
    if(endChapter){
      const parts=[];for(let ch=c1;ch<=Number(endChapter);ch++)parts.push(...await fetchChapter(book,ch));
      return verseText(parts);
    }
    return verseText(await fetchChapter(book,c1));
  };
  window.ONE_HEBREWS_CROSS_REFERENCE_SCRIPTURE={status:'loading',filled:0,references:unique.length,missing:[]};
  Promise.all(unique.map(async ref=>[ref,await resolve(ref)])).then(entries=>{
    const map=Object.fromEntries(entries);let filled=0;const missing=[];
    Object.values(D.studyBooks[58].chapterStudies||{}).forEach(study=>{
      (Array.isArray(study?.connections)?study.connections:[]).forEach(row=>{
        if(!Array.isArray(row))return;
        if(String(row[3]||'').trim())return;
        const ref=String(row[0]||'').trim(),scripture=map[ref];
        if(scripture){row[3]=scripture;filled++;}else if(ref)missing.push(ref);
      });
    });
    window.ONE_HEBREWS_CROSS_REFERENCE_SCRIPTURE={status:missing.length?'partial':'ready',filled,references:unique.length,missing:[...new Set(missing)]};
    document.documentElement.dataset.oneHebrewsScripture=missing.length?`PARTIAL:${filled}`:`PASS:${filled}`;
  }).catch(error=>{
    window.ONE_HEBREWS_CROSS_REFERENCE_SCRIPTURE={status:'error',filled:0,references:unique.length,missing:unique,error:String(error)};
    document.documentElement.dataset.oneHebrewsScripture='FAIL';
    console.error('ONE Hebrews Scripture load failed',error);
  });
})();
