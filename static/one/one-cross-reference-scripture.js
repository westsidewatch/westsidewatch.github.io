/* ONE canonical cross-reference Scripture layer.
 * Row shape: [reference, relationship, explanation, scripture].
 * Only explicitly validated books may promote legacy field 3 into Scripture field 4.
 * Explanation-only books receive Scripture only from an explicit reviewed reference map.
 */
(()=>{
  "use strict";
  const D=window.ONE_DATA;if(!D?.studyBooks)return;
  const migrate=(book,chapter,index,explanation)=>{const row=D.studyBooks?.[book]?.chapterStudies?.[String(chapter)]?.connections?.[index];if(!Array.isArray(row)||!String(row[2]||'').trim()||String(row[3]||'').trim())return false;row[3]=String(row[2]).trim();row[2]=explanation;return true;};
  const explanationFor=(row)=>`此處引用 ${String(row?.[0]||'相關經文')}，作為本章「${String(row?.[1]||'串珠關係')}」的直接經文依據。`;
  const curated=[
    [19,1,0,'與詩篇 1:2 同樣把蒙福的道路連於持續默想並遵行神的話。'],[19,1,1,'與詩篇 1:3 相同，以栽在水旁、持續結果的樹描寫倚靠耶和華的人。'],[19,1,2,'耶穌把兩條道路、兩種果子與兩種根基並置，呼應詩篇 1 的義人／惡人兩路。'],[19,2,0,'大衛之約提供父子與永遠國位的背景，連到詩篇 2 的受膏君王。'],[19,2,1,'初代教會直接以詩篇 2 解釋眾人敵擋耶穌。'],[19,2,2,'希伯來書把詩篇 2:7 用於基督。'],[19,2,3,'啟示錄沿用詩篇 2 的鐵杖治理圖像。'],
    [1,1,0,'詩篇把人的尊榮連到治理受造界，呼應創世記的神形像使命。'],[1,1,1,'詩篇把創造歸於耶和華的話語與氣息。'],[1,1,2,'約翰以太初回應創世記的起初。'],[1,1,3,'歌羅西書把基督放在萬有被造與存在的中心。'],[1,2,0,'十誡把安息日建立在創造第七日。'],[1,2,1,'詩篇把生命氣息與更新歸於神。'],[1,2,2,'耶穌引用創世記建立婚姻的一體。'],[1,2,3,'保羅把婚姻的一體指向基督與教會。'],[1,3,0,'保羅把亞當與基督作平行對照。'],[1,3,1,'保羅以蛇誘惑夏娃作警戒。'],[1,3,2,'啟示錄稱大龍為古蛇。'],[1,3,3,'生命樹與除去咒詛回應伊甸失落。'],[1,4,0,'希伯來書把亞伯獻祭與信心相連。'],[1,4,1,'約翰一書以該隱作恨弟兄的反例。'],[1,4,2,'基督的血與亞伯的血形成對照。'],[1,4,3,'耶穌以饒恕反轉拉麥的報復邏輯。']
  ];
  let migrated=curated.reduce((n,args)=>n+(migrate(...args)?1:0),0);
  const validatedBooks=[[1,1,50],[9,1,31],[10,1,24],[19,1,150],[23,1,66],[40,1,28],[41,1,16],[42,1,24],[43,1,21],[44,1,28],[52,1,5],[53,1,3],[66,1,22]];
  const migratedByBook={};
  for(const [book,start,end] of validatedBooks){let bookCount=0;for(let chapter=start;chapter<=end;chapter++){const rows=D.studyBooks?.[book]?.chapterStudies?.[String(chapter)]?.connections;if(!Array.isArray(rows))continue;rows.forEach((row,index)=>{if(!Array.isArray(row)||!String(row[2]||'').trim()||String(row[3]||'').trim())return;if(migrate(book,chapter,index,explanationFor(row))){migrated++;bookCount++;}});}migratedByBook[book]=bookCount;}

  /* Reviewed public-domain Chinese Union Version passages for explanation-only books.
   * Exact-reference lookup only: no commentary-to-Scripture promotion and no fuzzy matching.
   */
  const scriptureByReference={
    '申命記 31:6–8':'你們當剛強壯膽，不要害怕，也不要畏懼他們，因為耶和華－你的神和你同去。他必不撇下你，也不丟棄你。摩西召了約書亞來，在以色列眾人眼前對他說：你當剛強壯膽！因為，你要和這百姓一同進入耶和華向他們列祖起誓應許所賜之地；你也要使他們承受那地為業。耶和華必在你前面行；他必與你同在，必不撇下你，也不丟棄你。不要懼怕，也不要驚惶。',
    '申命記 7:1–6':'耶和華－你神領你進入要得為業之地，從你面前趕出許多國民，就是赫人、革迦撒人、亞摩利人、迦南人、比利洗人、希未人、耶布斯人，共七國的民，都比你強大。耶和華－你神將他們交給你擊殺，那時你要把他們滅絕淨盡，不可與他們立約，也不可憐恤他們。不可與他們結親。不可將你的女兒嫁他們的兒子，也不可叫你的兒子娶他們的女兒；因為他必使你兒子轉離不跟從主，去事奉別神，以致耶和華的怒氣向你們發作，就速速地將你們滅絕。你們卻要這樣待他們：拆毀他們的祭壇，打碎他們的柱像，砍下他們的木偶，用火焚燒他們雕刻的偶像。因為你歸耶和華－你神為聖潔的民；耶和華－你神從地上的萬民中揀選你，特作自己的子民。',
    '詩篇 114:3–5':'滄海看見就奔逃；約旦河也倒流。大山踴躍，如公羊；小山跳舞，如羊羔。滄海啊，你為何奔逃？約旦哪，你為何倒流？',
    '撒母耳記上 8:4–7':'以色列的長老都聚集，來到拉瑪見撒母耳，對他說：你年紀老邁了，你兒子不行你的道。現在求你為我們立一個王治理我們，像列國一樣。撒母耳不喜悅他們說立一個王治理我們，他就禱告耶和華。耶和華對撒母耳說：百姓向你說的一切話，你只管依從；因為他們不是厭棄你，乃是厭棄我，不要我作他們的王。',
    '詩篇 106:34–46':'他們不照耶和華所吩咐的滅絕外邦人，反與他們混雜相合，學習他們的行為，事奉他們的偶像，這就成了自己的網羅，把自己的兒女祭祀鬼魔，流無辜人的血，就是自己兒女的血，把他們祭祀迦南的偶像，那地就被血污穢了。這樣，他們被自己所做的污穢了，在行為上犯了邪淫。所以，耶和華的怒氣向他的百姓發作，憎惡他的產業，將他們交在外邦人的手裡；恨他們的人就轄制他們。他們的仇敵也欺壓他們，他們就伏在敵人手下。他屢次搭救他們，他們卻設謀背逆，因自己的罪孽降為卑下。然而，他聽見他們哀告的時候，就眷顧他們的急難，為他們記念他的約，照他豐盛的慈愛後悔。他也使他們在凡擄掠他們的人面前蒙憐恤。',
    '利未記 19:9–10':'在你們的地收割莊稼，不可割盡田角，也不可拾取所遺落的。不可摘盡葡萄園的果子，也不可拾取葡萄園所掉的果子；要留給窮人和寄居的。我是耶和華－你們的神。',
    '申命記 25:5–10':'弟兄同居，若死了一個，沒有兒子，死人的妻不可出嫁外人，他丈夫的兄弟當盡弟兄的本分，娶他為妻，與他同房。婦人生的長子必歸死兄的名下，免得他的名在以色列中塗抹了。那人若不願意娶他哥哥的妻，他哥哥的妻就要到城門長老那裡，說：我丈夫的兄弟不肯在以色列中興起他哥哥的名字，不給我盡弟兄的本分。本城的長老就要召那人來問他，他若執意說：我不願意娶他，他哥哥的妻就要當著長老到那人的跟前，脫了他的鞋，吐唾沫在他臉上，說：凡不為哥哥建立家室的都要這樣待他。在以色列中，他的名必稱為脫鞋之家。',
    '馬太福音 1:5–6':'撒門從喇合氏生波阿斯；波阿斯從路得氏生俄備得；俄備得生耶西；耶西生大衛王。大衛從烏利亞的妻子生所羅門。'
  };
  const reviewedExplanationBooks=[6,7,8];
  let filledFromReference=0;
  const filledByBook={};
  for(const bookNo of reviewedExplanationBooks){let n=0;const book=D.studyBooks?.[bookNo];Object.values(book?.chapterStudies||{}).forEach(study=>(Array.isArray(study?.connections)?study.connections:[]).forEach(row=>{if(!Array.isArray(row)||String(row[3]||'').trim())return;const scripture=scriptureByReference[String(row[0]||'').trim()];if(!scripture)return;row[3]=scripture;n++;filledFromReference++;}));filledByBook[bookNo]=n;}

  const psalm8=D.studyBooks?.[1]?.chapterStudies?.['1']?.connections?.[0];if(Array.isArray(psalm8)&&String(psalm8[3]||'').includes('aa耶和華'))psalm8[3]=String(psalm8[3]).replace('aa耶和華','耶和華');
  let total=0,verified=0,commentaryOnly=0;Object.values(D.studyBooks).forEach(book=>Object.values(book?.chapterStudies||{}).forEach(study=>(Array.isArray(study?.connections)?study.connections:[]).forEach(row=>{if(!Array.isArray(row))return;total++;if(String(row[3]||'').trim())verified++;else if(String(row[2]||'').trim())commentaryOnly++;})));
  window.ONE_CROSS_REFERENCE_SCRIPTURE_PROGRESS={batch:'validated-major-books-plus-acts-plus-joshua-judges-ruth',migrated,migratedByBook,filledFromReference,filledByBook,total,verified,remaining:total-verified,commentaryOnly,validatedBooks:validatedBooks.map(([book,start,end])=>({book,start,end})),reviewedExplanationBooks};
  document.documentElement.dataset.oneCrossReferenceScripture=`${verified}/${total}`;
})();
