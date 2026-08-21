/* ONE cross-reference Scripture integrity layer.
 * The canonical connection row is [reference, relationship, explanation, optional Scripture quotation].
 * Explanatory text must never be rendered as if it were a Bible quotation.
 */
(()=>{
  "use strict";

  window.ONE_SCRIPTURE_LOCAL=Object.assign(window.ONE_SCRIPTURE_LOCAL||{}, {
    '約書亞記 1:8':'這律法書不可離開你的口，總要晝夜思想，好使你謹守遵行這書上所寫的一切話。如此，你的道路就可以亨通，凡事順利。',
    '耶利米書 17:5–8':'耶和華如此說：倚靠人血肉的膀臂，心中離棄耶和華的，那人有禍了！因他必像沙漠的杜松，不見福樂來到，卻要住曠野乾旱之處，無人居住的鹼地。倚靠耶和華、以耶和華為可靠的，那人有福了！他必像樹栽於水旁，在河邊扎根，炎熱來到，並不懼怕，葉子仍必青翠，在乾旱之年毫無掛慮，而且結果不止。',
    '馬太福音 7:13–27':'你們要進窄門。因為引到滅亡，那門是寬的，路是大的，進去的人也多；引到永生，那門是窄的，路是小的，找着的人也少。你們要防備假先知。他們到你們這裏來，外面披着羊皮，裏面卻是殘暴的狼。憑着他們的果子，就可以認出他們來。凡稱呼我「主啊，主啊」的人不能都進天國；惟獨遵行我天父旨意的人才能進去。所以，凡聽見我這話就去行的，好比一個聰明人，把房子蓋在磐石上；凡聽見我這話不去行的，好比一個無知的人，把房子蓋在沙土上。'
  });

  const D=window.ONE_DATA;
  if(!D?.studyBooks)return;
  const text=value=>value==null?'':String(value).trim();
  const rows=[];
  Object.entries(D.studyBooks).forEach(([bookNumber,book])=>{
    Object.entries(book?.chapterStudies||{}).forEach(([chapterNumber,study])=>{
      (Array.isArray(study?.connections)?study.connections:[]).forEach((item,index)=>{
        if(!Array.isArray(item))return;
        const reference=text(item[0]),relationship=text(item[1]),explanation=text(item[2]);
        const scripture=text(item[3])||text(window.ONE_SCRIPTURE_LOCAL?.[reference]);
        rows.push({bookNumber:Number(bookNumber),book:book.name||'',chapter:Number(chapterNumber),index,reference,relationship,explanation,scripture});
      });
    });
  });

  const withoutScripture=rows.filter(row=>!row.scripture);
  window.ONE_CROSS_REFERENCE_AUDIT={
    total:rows.length,
    withVerifiedScripture:rows.length-withoutScripture.length,
    withoutVerifiedScripture:withoutScripture.length,
    affected:withoutScripture.map(({bookNumber,book,chapter,index,reference})=>({bookNumber,book,chapter,index:index+1,reference})),
    ok:withoutScripture.length===0
  };
  document.documentElement.dataset.oneCrossReferenceAudit=`${withoutScripture.length}/${rows.length}`;

  const bookByName=new Map((D.books||[]).map(row=>[text(row?.[1]),Number(row?.[0])]));
  const officialChapterUrl=reference=>{
    const match=text(reference).match(/^(.+?)\s+(\d+)(?::|$)/);
    if(!match)return '';
    const number=bookByName.get(match[1]);
    const code=D.studyBooks?.[number]?.zhCode;
    return code?`https://rcuv.hkbs.org.hk/CUNP1/${encodeURIComponent(code)}/${Number(match[2])}/`:'';
  };

  const style=document.createElement('style');
  style.textContent=`
    .connection-note{margin:.8rem 0 0;color:var(--ink);font-size:var(--one-body-size);line-height:1.8}
    .connection-note>span,.connection-scripture-missing>span{display:block;margin-bottom:.18rem;color:var(--gold);font-size:.62rem;letter-spacing:.12em;text-transform:uppercase}
    .connection-scripture-missing{margin:.8rem 0 0;padding-top:.7rem;border-top:1px solid var(--line);color:var(--muted);font-size:.82rem;line-height:1.65}
    .connection-scripture-missing a{color:var(--olive);text-decoration:none;border-bottom:1px solid currentColor}
    .connection-section blockquote[data-one-scripture=true]{margin:.85rem 0 0}
  `;
  document.head.append(style);

  const repairRenderedConnections=()=>{
    const detail=document.getElementById('chapter-detail');
    if(!detail)return;
    const bookNumber=Number(detail.dataset.book),chapter=Number(detail.dataset.chapter);
    const study=D.studyBooks?.[bookNumber]?.chapterStudies?.[String(chapter)];
    const data=Array.isArray(study?.connections)?study.connections:[];
    detail.querySelectorAll('.connection-section .connection-grid > article').forEach((article,index)=>{
      const item=data[index];
      if(!Array.isArray(item))return;
      const reference=text(item[0]),explanation=text(item[2]);
      const scripture=text(item[3])||text(window.ONE_SCRIPTURE_LOCAL?.[reference]);
      article.querySelectorAll('blockquote,.connection-note,.connection-scripture-missing').forEach(node=>node.remove());

      if(scripture){
        const quote=document.createElement('blockquote');
        quote.dataset.oneScripture='true';
        quote.textContent=scripture;
        article.append(quote);
      }
      if(explanation&&explanation!==scripture){
        const note=document.createElement('p');
        note.className='connection-note';
        const label=document.createElement('span');
        label.textContent='Cross-reference note · 串珠說明';
        note.append(label,document.createTextNode(explanation));
        article.append(note);
      }
      if(!scripture){
        const missing=document.createElement('p');
        missing.className='connection-scripture-missing';
        const label=document.createElement('span');
        label.textContent='Scripture · 經文';
        missing.append(label,document.createTextNode('尚未接入逐字經文；此處不再把串珠說明冒充經文引用。'));
        const url=officialChapterUrl(reference);
        if(url){
          missing.append(document.createTextNode(' '));
          const link=document.createElement('a');
          link.href=url;link.target='_blank';link.rel='noopener';link.textContent=`查看 ${reference} ↗`;
          missing.append(link);
        }
        article.append(missing);
      }
    });
  };

  const detail=document.getElementById('chapter-detail');
  if(detail){
    repairRenderedConnections();
    const observer=new MutationObserver(repairRenderedConnections);
    observer.observe(detail,{childList:true,subtree:true});
  }
  console.info('ONE cross-reference audit',window.ONE_CROSS_REFERENCE_AUDIT);
})();
