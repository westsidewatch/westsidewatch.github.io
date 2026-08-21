/* ONE — reviewed Scripture fill for explanation-only major prophets.
 * Exact-reference only. Existing verified Scripture may be reused; commentary never is.
 */
(()=>{
  "use strict";
  const D=window.ONE_DATA;if(!D?.studyBooks)return;
  const known={};
  Object.values(D.studyBooks).forEach(book=>Object.values(book?.chapterStudies||{}).forEach(study=>(Array.isArray(study?.connections)?study.connections:[]).forEach(row=>{
    if(Array.isArray(row)&&String(row[0]||'').trim()&&String(row[3]||'').trim())known[String(row[0]).trim()]=String(row[3]).trim();
  })));
  const reviewed={
    '申命記 30:1–6':'我所陳明在你面前的這一切咒詛都臨到你身上；你在耶和華－你上帝追趕你到的萬國中必心裏追念祝福的話；你和你的子孫若盡心盡性歸向耶和華－你的上帝，照着我今日一切所吩咐的聽從他的話；那時，耶和華－你的上帝必憐恤你，救回你這被擄的子民；耶和華－你的上帝要回轉過來，從分散你到的萬民中將你招聚回來。你被趕散的人，就是在天涯的，耶和華－你的上帝也必從那裏將你招聚回來。耶和華－你的上帝必領你進入你列祖所得的地，使你可以得着；又必善待你，使你的人數比你列祖眾多。耶和華－你上帝必將你心裏和你後裔心裏的污穢除掉，好叫你盡心盡性愛耶和華－你的上帝，使你可以存活。',
    '希伯來書 8:8–12':'所以主指責他的百姓說：日子將到，我要與以色列家和猶大家另立新約，不像我拉着他們祖宗的手，領他們出埃及的時候，與他們所立的約。因為他們不恆心守我的約，我也不理他們。這是主說的。主又說：那些日子以後，我與以色列家所立的約乃是這樣：我要將我的律法放在他們裏面，寫在他們心上；我要作他們的上帝；他們要作我的子民。他們不用各人教導自己的鄉鄰和自己的弟兄，說：你該認識主；因為他們從最小的到至大的，都必認識我。我要寬恕他們的不義，不再記念他們的罪愆。',
    '哥林多後書 4:8–9':'我們四面受敵，卻不被困住；心裏作難，卻不至失望；遭逼迫，卻不被丟棄；打倒了，卻不至死亡。',
    '耶利米書 31:31–34':'耶和華說：「日子將到，我要與以色列家和猶大家另立新約，不像我拉着他們祖宗的手，領他們出埃及地的時候，與他們所立的約。我雖作他們的丈夫，他們卻背了我的約。」這是耶和華說的。耶和華說：「那些日子以後，我與以色列家所立的約乃是這樣：我要將我的律法放在他們裏面，寫在他們心上。我要作他們的上帝，他們要作我的子民。他們各人不再教導自己的鄰舍和自己的弟兄說：『你該認識耶和華』，因為他們從最小的到至大的都必認識我。我要赦免他們的罪孽，不再記念他們的罪惡。」這是耶和華說的。',
    '約翰福音 10:11':'我是好牧人；好牧人為羊捨命。',
    '耶利米書 25:11–12':'這全地必然荒涼，令人驚駭。這些國民要服事巴比倫王七十年。七十年滿了以後，我必刑罰巴比倫王和那國民，並迦勒底人之地，因他們的罪孽使那地永遠荒涼。這是耶和華說的。',
    '馬太福音 24:15':'你們看見先知但以理所說的「那行毀壞可憎的」站在聖地（讀這經的人須要會意）。'
  };
  Object.assign(known,reviewed);
  const books=[24,25,26,27];
  const fillFrom=(map)=>{
    let filled=0;
    for(const bookNo of books){
      Object.values(D.studyBooks?.[bookNo]?.chapterStudies||{}).forEach(study=>{
        (Array.isArray(study?.connections)?study.connections:[]).forEach(row=>{
          if(!Array.isArray(row)||String(row[3]||'').trim())return;
          const scripture=map[String(row[0]||'').trim()];
          if(scripture){row[3]=scripture;filled++;}
        });
      });
    }
    return filled;
  };
  let filled=fillFrom(known);
  const missing=()=>{
    const result={};
    for(const bookNo of books){const set=new Set();Object.values(D.studyBooks?.[bookNo]?.chapterStudies||{}).forEach(study=>(Array.isArray(study?.connections)?study.connections:[]).forEach(row=>{if(Array.isArray(row)&&!String(row[3]||'').trim()&&String(row[0]||'').trim())set.add(String(row[0]).trim());}));result[bookNo]=[...set];}
    return result;
  };
  window.ONE_MAJOR_PROPHETS_CROSS_REFERENCE_SCRIPTURE={status:'loading-long-references',filled,books,missing:missing()};

  /* Five long passages are loaded from the Public Domain Chinese Union Traditional
   * getBible endpoint. Exact references only; failures leave field 4 empty. */
  const API='https://api.getbible.net/v2/cut';
  const chapter=async(book,ch)=>{
    const response=await fetch(`${API}/${book}/${ch}.json`,{mode:'cors'});
    if(!response.ok)throw new Error(`CUV ${book}/${ch} ${response.status}`);
    const data=await response.json();
    return Array.isArray(data?.verses)?data.verses:[];
  };
  const text=verses=>verses.map(v=>String(v?.text||'').trim()).join('');
  Promise.all([chapter(12,22),chapter(12,23),chapter(12,24),chapter(12,25),chapter(24,52),chapter(66,13),chapter(66,21),chapter(66,22)])
    .then(([k22,k23,k24,k25,jer52,rev13,rev21,rev22])=>{
      const longRefs={
        '列王紀下 22–25':text([...k22,...k23,...k24,...k25]),
        '列王紀下 25:1–21':text(k25.filter(v=>Number(v?.verse)<=21)),
        '耶利米書 52':text(jer52),
        '啟示錄 21–22':text([...rev21,...rev22]),
        '啟示錄 13':text(rev13)
      };
      if(Object.values(longRefs).some(v=>!v))throw new Error('empty long-reference Scripture payload');
      const longFilled=fillFrom(longRefs);filled+=longFilled;
      window.ONE_MAJOR_PROPHETS_CROSS_REFERENCE_SCRIPTURE={status:'ready',filled,longFilled,books,missing:missing(),longReferences:Object.keys(longRefs)};
      document.documentElement.dataset.oneMajorProphetsScripture=`PASS:${filled}`;
    })
    .catch(error=>{
      window.ONE_MAJOR_PROPHETS_CROSS_REFERENCE_SCRIPTURE={status:'long-reference-error',filled,books,missing:missing(),error:String(error)};
      document.documentElement.dataset.oneMajorProphetsScripture='PARTIAL';
      console.error('ONE major-prophet long Scripture load failed',error);
    });
})();

/* ONE — Hebrews 1–13 exact Scripture fill.
 * Public-domain Chinese Union Traditional text only; field 3 commentary is untouched.
 */
(()=>{
  "use strict";
  const D=window.ONE_DATA;if(!D?.studyBooks?.[58])return;
  const API='https://api.getbible.net/v2/cut';
  const bookNumbers={'創世記':1,'出埃及記':2,'利未記':3,'民數記':4,'申命記':5,'約書亞記':6,'撒母耳記下':10,'詩篇':19,'箴言':20,'以賽亞書':23,'耶利米書':24,'哈該書':37};
  const refs=[
    '詩篇 2:7','詩篇 110:1','撒母耳記下 7:14','詩篇 8:4–6','詩篇 22:22','以賽亞書 8:18','民數記 12:7','詩篇 95:7–11','出埃及記 17:1–7','創世記 2:2','約書亞記 21:43–45','詩篇 110:4','創世記 14:18–20','創世記 22:16–18','利未記 16:2','民數記 18:21','耶利米書 31:31–34','出埃及記 24:7–8','出埃及記 25:8–9','出埃及記 25–26','利未記 16','出埃及記 24:8','詩篇 40:6–8','耶利米書 31:33–34','申命記 32:35–36','創世記 12:1–4','創世記 22:1–18','出埃及記 2–14','約書亞記 2','箴言 3:11–12','哈該書 2:6','申命記 4:24','利未記 16:27','詩篇 118:6','申命記 31:6'
  ];
  const cache=new Map();
  const fetchChapter=async(book,ch)=>{
    const key=`${book}/${ch}`;
    if(!cache.has(key))cache.set(key,fetch(`${API}/${book}/${ch}.json`,{mode:'cors'}).then(r=>{if(!r.ok)throw new Error(`CUV ${key} ${r.status}`);return r.json();}).then(d=>Array.isArray(d?.verses)?d.verses:[]));
    return cache.get(key);
  };
  const verseText=verses=>verses.map(v=>String(v?.text||'').trim()).join('');
  const resolve=async ref=>{
    const m=ref.match(/^(.+?)\s+(\d+)(?:(:)(\d+)(?:[–-](\d+))?|[–-](\d+))?$/);
    if(!m)throw new Error(`Unsupported reference: ${ref}`);
    const [,bookName,startChapter,colon,startVerse,endVerse,endChapter]=m,book=bookNumbers[bookName],c1=Number(startChapter);
    if(!book)throw new Error(`Unknown book: ${bookName}`);
    if(colon){const verses=await fetchChapter(book,c1),v1=Number(startVerse),v2=endVerse?Number(endVerse):v1;return verseText(verses.filter(v=>Number(v?.verse)>=v1&&Number(v?.verse)<=v2));}
    if(endChapter){const parts=[];for(let ch=c1;ch<=Number(endChapter);ch++)parts.push(...await fetchChapter(book,ch));return verseText(parts);}
    return verseText(await fetchChapter(book,c1));
  };
  const unique=[...new Set(refs)];
  window.ONE_HEBREWS_CROSS_REFERENCE_SCRIPTURE={status:'loading',filled:0,references:unique.length,missing:[]};
  Promise.all(unique.map(async ref=>[ref,await resolve(ref)])).then(entries=>{
    const map=Object.fromEntries(entries);let filled=0;const missing=[];
    Object.values(D.studyBooks[58].chapterStudies||{}).forEach(study=>(Array.isArray(study?.connections)?study.connections:[]).forEach(row=>{
      if(!Array.isArray(row)||String(row[3]||'').trim())return;
      const ref=String(row[0]||'').trim(),scripture=map[ref];if(scripture){row[3]=scripture;filled++;}else if(ref)missing.push(ref);
    }));
    window.ONE_HEBREWS_CROSS_REFERENCE_SCRIPTURE={status:missing.length?'partial':'ready',filled,references:unique.length,missing:[...new Set(missing)]};
    document.documentElement.dataset.oneHebrewsScripture=missing.length?`PARTIAL:${filled}`:`PASS:${filled}`;
  }).catch(error=>{
    window.ONE_HEBREWS_CROSS_REFERENCE_SCRIPTURE={status:'error',filled:0,references:unique.length,missing:unique,error:String(error)};
    document.documentElement.dataset.oneHebrewsScripture='FAIL';
    console.error('ONE Hebrews Scripture load failed',error);
  });
})();

/* ONE — final global cross-reference Scripture audit. Read-only. */
(()=>{
  "use strict";
  const D=window.ONE_DATA;if(!D?.studyBooks)return;
  const settled=status=>!status||!['loading','loading-long-references'].includes(status);
  const norm=value=>String(value||'').replace(/\s+/g,'').trim();
  const scan=()=>{
    let totalRows=0,filledRows=0,missingRows=0,chaptersWithConnections=0,completeChapters=0,incompleteChapters=0;
    const missing=[],explanationCopied=[],relationshipCopied=[],referenceTexts=new Map();
    Object.entries(D.studyBooks).sort((a,b)=>Number(a[0])-Number(b[0])).forEach(([bookNo,book])=>Object.entries(book?.chapterStudies||{}).sort((a,b)=>Number(a[0])-Number(b[0])).forEach(([chapterNo,study])=>{
      const rows=Array.isArray(study?.connections)?study.connections:[];if(!rows.length)return;chaptersWithConnections++;let chapterMissing=0;
      rows.forEach((row,index)=>{
        if(!Array.isArray(row))return;totalRows++;
        const ref=String(row[0]||'').trim(),relationship=String(row[1]||'').trim(),explanation=String(row[2]||'').trim(),scripture=String(row[3]||'').trim();
        if(scripture){
          filledRows++;
          if(explanation&&norm(scripture)===norm(explanation))explanationCopied.push({book:Number(bookNo),bookName:book.name,chapter:Number(chapterNo),row:index+1,reference:ref});
          if(relationship&&norm(scripture)===norm(relationship))relationshipCopied.push({book:Number(bookNo),bookName:book.name,chapter:Number(chapterNo),row:index+1,reference:ref});
          if(ref){if(!referenceTexts.has(ref))referenceTexts.set(ref,new Set());referenceTexts.get(ref).add(norm(scripture));}
        }else{missingRows++;chapterMissing++;missing.push({book:Number(bookNo),bookName:book.name,chapter:Number(chapterNo),row:index+1,reference:ref});}
      });
      if(chapterMissing)incompleteChapters++;else completeChapters++;
    }));
    const conflicts=[...referenceTexts.entries()].filter(([,texts])=>texts.size>1).map(([reference,texts])=>({reference,versions:texts.size}));
    const ok=missingRows===0&&explanationCopied.length===0&&relationshipCopied.length===0&&conflicts.length===0;
    const result={status:ok?'PASS':'FAIL',books:Object.keys(D.studyBooks).length,totalChapters:Object.values(D.studyBooks).reduce((n,b)=>n+Object.keys(b?.chapterStudies||{}).length,0),chaptersWithConnections,completeChapters,incompleteChapters,totalRows,filledRows,missingRows,explanationCopied,relationshipCopied,conflicts,missing};
    window.ONE_CROSS_REFERENCE_SCRIPTURE_GLOBAL_AUDIT=result;
    document.documentElement.dataset.oneCrossReferenceScriptureAudit=ok?`PASS:${filledRows}/${totalRows}`:`FAIL:missing-${missingRows}:copied-${explanationCopied.length+relationshipCopied.length}:conflicts-${conflicts.length}`;
    if(!ok)console.error('ONE cross-reference Scripture global audit',result);else console.info('ONE cross-reference Scripture global audit',result);
  };
  const started=Date.now();
  const wait=()=>{
    const major=window.ONE_MAJOR_PROPHETS_CROSS_REFERENCE_SCRIPTURE?.status,hebrews=window.ONE_HEBREWS_CROSS_REFERENCE_SCRIPTURE?.status;
    if((settled(major)&&settled(hebrews))||Date.now()-started>15000)scan();else setTimeout(wait,100);
  };
  wait();
})();
