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
    [19,1,0,'與詩篇 1:2 同樣把蒙福的道路連於持續默想並遵行神的話。'],
    [19,1,1,'與詩篇 1:3 相同，以栽在水旁、持續結果的樹描寫倚靠耶和華的人。'],
    [19,1,2,'耶穌把兩條道路、兩種果子與兩種根基並置，呼應詩篇 1 的義人／惡人兩路。'],
    [19,2,0,'大衛之約提供「父／子」與永遠國位的背景，連到詩篇 2 的受膏君王。'],
    [19,2,1,'初代教會直接以詩篇 2 解釋希律、彼拉多、外邦人和以色列民敵擋耶穌。'],
    [19,2,2,'希伯來書把詩篇 2:7 的「你是我的兒子」用於基督。'],
    [19,2,3,'啟示錄沿用詩篇 2 的鐵杖治理圖像，指向基督所賜的王權。'],

    [1,1,0,'詩篇以受造宇宙反問人的位置，並把人的尊榮直接連到治理神手所造的一切，呼應創世記 1:26–28。'],
    [1,1,1,'詩篇把創造歸因於耶和華的話語與氣息，呼應創世記 1 章反覆的「神說」。'],
    [1,1,2,'約翰以「太初」回應創世記的「起初」，並宣告萬物藉著道而被造。'],
    [1,1,3,'歌羅西書把基督放在萬有被造、萬有存在與萬有目的的中心，深化創世記 1 的創造主題。'],
    [1,2,0,'十誡把安息日直接建立在創造第七日的完成與神的安息之上。'],
    [1,2,1,'詩篇把受造物的生命、氣息、死亡與更新都歸於神，呼應創世記 2:7 的生命氣息。'],
    [1,2,2,'耶穌同時引用創世記 1 與 2 章，將婚姻的一體建立在創造秩序上。'],
    [1,2,3,'保羅引用創世記 2:24，並進一步把婚姻的一體指向基督與教會。'],
    [1,3,0,'保羅把亞當的悖逆、罪與死的進入，和基督的順服、稱義與生命作平行對照。'],
    [1,3,1,'保羅明確以蛇誘惑夏娃作為教會被詭詐引離基督的警戒。'],
    [1,3,2,'啟示錄把末世的大龍稱為「古蛇」，把創世記 3 的蛇放進整本聖經的屬靈爭戰脈絡。'],
    [1,3,3,'啟示錄末章再次出現生命水、生命樹、除去咒詛與見神的面，形成對伊甸失落的終末回應。'],
    [1,4,0,'希伯來書把亞伯蒙神悅納的獻祭與信心直接相連，補充創世記 4 對兩兄弟供物的敘述。'],
    [1,4,1,'約翰一書把該隱殺弟解讀為屬惡者、恨弟兄的反面例證，與彼此相愛形成對照。'],
    [1,4,2,'希伯來書把耶穌新約之血與亞伯的血並置，指出基督的血所宣告的更美。'],
    [1,4,3,'耶穌以七十個七次的饒恕回應報復的邏輯，與創世記 4 中拉麥七十七倍報復形成強烈反轉。']
  ];
  const migrated=batch.reduce((n,args)=>n+(migrate(...args)?1:0),0);
  /* Remove one known transcription artifact after its verse has been moved. */
  const psalm8=D.studyBooks?.[1]?.chapterStudies?.['1']?.connections?.[0];
  if(Array.isArray(psalm8)&&String(psalm8[3]||'').includes('aa耶和華'))psalm8[3]=String(psalm8[3]).replace('aa耶和華','耶和華');

  let total=0,verified=0;
  Object.values(D.studyBooks).forEach(book=>Object.values(book?.chapterStudies||{}).forEach(study=>(Array.isArray(study?.connections)?study.connections:[]).forEach(row=>{
    if(!Array.isArray(row))return;
    total++;
    if(String(row[3]||'').trim())verified++;
  })));
  window.ONE_CROSS_REFERENCE_SCRIPTURE_PROGRESS={batch:'psalms-1-2+genesis-1-4',migrated,total,verified,remaining:total-verified};
  document.documentElement.dataset.oneCrossReferenceScripture=`${verified}/${total}`;
})();
