/* ONE — global cross-reference Scripture audit.
 * Read-only: never repairs or promotes content. It reports missing Scripture,
 * explanation copied into Scripture, and conflicting Scripture for the same reference.
 */
(()=>{
  "use strict";
  const D=window.ONE_DATA;if(!D?.studyBooks)return;
  const settled=status=>!status||!['loading','loading-long-references'].includes(status);
  const normalize=value=>String(value||'').replace(/\s+/g,'').trim();
  const scan=()=>{
    let totalRows=0,filledRows=0,missingRows=0,chaptersWithConnections=0,completeChapters=0,incompleteChapters=0;
    const missing=[],explanationCopied=[],relationshipCopied=[],referenceTexts=new Map();
    Object.entries(D.studyBooks).sort((a,b)=>Number(a[0])-Number(b[0])).forEach(([bookNo,book])=>{
      Object.entries(book?.chapterStudies||{}).sort((a,b)=>Number(a[0])-Number(b[0])).forEach(([chapterNo,study])=>{
        const rows=Array.isArray(study?.connections)?study.connections:[];
        if(!rows.length)return;
        chaptersWithConnections++;
        let chapterMissing=0;
        rows.forEach((row,index)=>{
          if(!Array.isArray(row))return;
          totalRows++;
          const ref=String(row[0]||'').trim(),relationship=String(row[1]||'').trim(),explanation=String(row[2]||'').trim(),scripture=String(row[3]||'').trim();
          if(scripture){
            filledRows++;
            if(explanation&&normalize(scripture)===normalize(explanation))explanationCopied.push({book:Number(bookNo),bookName:book.name,chapter:Number(chapterNo),row:index+1,reference:ref});
            if(relationship&&normalize(scripture)===normalize(relationship))relationshipCopied.push({book:Number(bookNo),bookName:book.name,chapter:Number(chapterNo),row:index+1,reference:ref});
            if(ref){if(!referenceTexts.has(ref))referenceTexts.set(ref,new Set());referenceTexts.get(ref).add(normalize(scripture));}
          }else{
            missingRows++;chapterMissing++;
            missing.push({book:Number(bookNo),bookName:book.name,chapter:Number(chapterNo),row:index+1,reference:ref});
          }
        });
        if(chapterMissing){incompleteChapters++;}else completeChapters++;
      });
    });
    const conflicts=[...referenceTexts.entries()].filter(([,texts])=>texts.size>1).map(([reference,texts])=>({reference,versions:texts.size}));
    const ok=missingRows===0&&explanationCopied.length===0&&relationshipCopied.length===0&&conflicts.length===0;
    const result={
      status:ok?'PASS':'FAIL',books:Object.keys(D.studyBooks).length,totalChapters:Object.values(D.studyBooks).reduce((n,b)=>n+Object.keys(b?.chapterStudies||{}).length,0),
      chaptersWithConnections,completeChapters,incompleteChapters,totalRows,filledRows,missingRows,
      explanationCopied,relationshipCopied,conflicts,missing
    };
    window.ONE_CROSS_REFERENCE_SCRIPTURE_GLOBAL_AUDIT=result;
    document.documentElement.dataset.oneCrossReferenceScriptureAudit=ok?`PASS:${filledRows}/${totalRows}`:`FAIL:missing-${missingRows}:copied-${explanationCopied.length+relationshipCopied.length}:conflicts-${conflicts.length}`;
    if(!ok)console.error('ONE cross-reference Scripture global audit',result);else console.info('ONE cross-reference Scripture global audit',result);
    return result;
  };
  const started=Date.now();
  const wait=()=>{
    const major=window.ONE_MAJOR_PROPHETS_CROSS_REFERENCE_SCRIPTURE?.status;
    const hebrews=window.ONE_HEBREWS_CROSS_REFERENCE_SCRIPTURE?.status;
    if((settled(major)&&settled(hebrews))||Date.now()-started>15000)scan();
    else setTimeout(wait,100);
  };
  wait();
})();
