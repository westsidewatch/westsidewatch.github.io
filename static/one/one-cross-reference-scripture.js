/* ONE canonical cross-reference Scripture layer.
 * Row shape: [reference, relationship, explanation, scripture].
 * Explicit batches only; commentary is never auto-promoted into a quotation.
 */
(()=>{
  "use strict";
  const D=window.ONE_DATA;if(!D?.studyBooks)return;
  const migrate=(book,chapter,index,explanation)=>{const row=D.studyBooks?.[book]?.chapterStudies?.[String(chapter)]?.connections?.[index];if(!Array.isArray(row)||!String(row[2]||'').trim())return false;if(!String(row[3]||'').trim())row[3]=String(row[2]).trim();row[2]=explanation;return true;};
  const batch=[
    [19,1,0,'與詩篇 1:2 同樣把蒙福的道路連於持續默想並遵行神的話。'],
    [19,1,1,'與詩篇 1:3 相同，以栽在水旁、持續結果的樹描寫倚靠耶和華的人。'],
    [19,1,2,'耶穌把兩條道路、兩種果子與兩種根基並置，呼應詩篇 1 的義人／惡人兩路。'],
    [19,2,0,'大衛之約提供「父／子」與永遠國位的背景，連到詩篇 2 的受膏君王。'],
    [19,2,1,'初代教會直接以詩篇 2 解釋希律、彼拉多、外邦人和以色列民敵擋耶穌。'],
    [19,2,2,'希伯來書把詩篇 2:7 的「你是我的兒子」用於基督。'],
    [19,2,3,'啟示錄沿用詩篇 2 的鐵杖治理圖像，指向基督所賜的王權。']
  ];
  const migrated=batch.reduce((n,args)=>n+(migrate(...args)?1:0),0);let total=0,verified=0;Object.values(D.studyBooks).forEach(book=>Object.values(book?.chapterStudies||{}).forEach(study=>(Array.isArray(study?.connections)?study.connections:[]).forEach(row=>{if(!Array.isArray(row))return;total++;if(String(row[3]||'').trim())verified++;})));window.ONE_CROSS_REFERENCE_SCRIPTURE_PROGRESS={batch:'psalms-1-2',migrated,total,verified,remaining:total-verified};document.documentElement.dataset.oneCrossReferenceScripture=`${verified}/${total}`;
})();
