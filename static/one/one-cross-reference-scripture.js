/* ONE canonical cross-reference Scripture layer.
 * Row shape: [reference, relationship, explanation, scripture].
 * Explicit batches only; commentary is never auto-promoted into a quotation.
 */
(()=>{
  "use strict";
  const D=window.ONE_DATA;if(!D?.studyBooks)return;
  const migrate=(book,chapter,index,explanation)=>{
    const row=D.studyBooks?.[book]?.chapterStudies?.[String(chapter)]?.connections?.[index];
    if(!Array.isArray(row)||!String(row[2]||'').trim())return false;
    if(!String(row[3]||'').trim())row[3]=String(row[2]).trim();
    row[2]=explanation;
    return true;
  };
  const batch=[
    [19,1,0,'與詩篇 1:2 同樣把蒙福的道路連於持續默想並遵行神的話。'],[19,1,1,'與詩篇 1:3 相同，以栽在水旁、持續結果的樹描寫倚靠耶和華的人。'],[19,1,2,'耶穌把兩條道路、兩種果子與兩種根基並置，呼應詩篇 1 的義人／惡人兩路。'],[19,2,0,'大衛之約提供父子與永遠國位的背景，連到詩篇 2 的受膏君王。'],[19,2,1,'初代教會直接以詩篇 2 解釋眾人敵擋耶穌。'],[19,2,2,'希伯來書把詩篇 2:7 用於基督。'],[19,2,3,'啟示錄沿用詩篇 2 的鐵杖治理圖像。'],
    [1,1,0,'詩篇把人的尊榮連到治理受造界，呼應創世記的神形像使命。'],[1,1,1,'詩篇把創造歸於耶和華的話語與氣息。'],[1,1,2,'約翰以太初回應創世記的起初。'],[1,1,3,'歌羅西書把基督放在萬有被造與存在的中心。'],[1,2,0,'十誡把安息日建立在創造第七日。'],[1,2,1,'詩篇把生命氣息與更新歸於神。'],[1,2,2,'耶穌引用創世記建立婚姻的一體。'],[1,2,3,'保羅把婚姻的一體指向基督與教會。'],[1,3,0,'保羅把亞當與基督作平行對照。'],[1,3,1,'保羅以蛇誘惑夏娃作警戒。'],[1,3,2,'啟示錄稱大龍為古蛇。'],[1,3,3,'生命樹與除去咒詛回應伊甸失落。'],[1,4,0,'希伯來書把亞伯獻祭與信心相連。'],[1,4,1,'約翰一書以該隱作恨弟兄的反例。'],[1,4,2,'基督的血與亞伯的血形成對照。'],[1,4,3,'耶穌以饒恕反轉拉麥的報復邏輯。']
  ];
  /* Genesis 5–50: the existing third field is already verbatim Scripture in the canonical chapter data.
   * Move it wholesale into the fourth field, while replacing field 3 with a neutral relationship explanation.
   * This is deliberately scoped to Genesis only; no heuristic promotion is allowed outside this explicit range.
   */
  const genesisExplanation=(row)=>`此處引用 ${String(row?.[0]||'相關經文')}，作為本章「${String(row?.[1]||'串珠關係')}」的直接經文依據。`;
  for(let chapter=5;chapter<=50;chapter++){
    const rows=D.studyBooks?.[1]?.chapterStudies?.[String(chapter)]?.connections;
    if(!Array.isArray(rows))continue;
    rows.forEach((row,index)=>{if(Array.isArray(row)&&String(row[2]||'').trim())batch.push([1,chapter,index,genesisExplanation(row)]);});
  }
  const migrated=batch.reduce((n,args)=>n+(migrate(...args)?1:0),0);
  const psalm8=D.studyBooks?.[1]?.chapterStudies?.['1']?.connections?.[0];
  if(Array.isArray(psalm8)&&String(psalm8[3]||'').includes('aa耶和華'))psalm8[3]=String(psalm8[3]).replace('aa耶和華','耶和華');
  let total=0,verified=0;
  Object.values(D.studyBooks).forEach(book=>Object.values(book?.chapterStudies||{}).forEach(study=>(Array.isArray(study?.connections)?study.connections:[]).forEach(row=>{if(!Array.isArray(row))return;total++;if(String(row[3]||'').trim())verified++;})));
  window.ONE_CROSS_REFERENCE_SCRIPTURE_PROGRESS={batch:'psalms-1-2+genesis-1-50',migrated,total,verified,remaining:total-verified};
  document.documentElement.dataset.oneCrossReferenceScripture=`${verified}/${total}`;
})();
