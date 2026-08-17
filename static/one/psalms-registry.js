/* 詩篇 ONE：完整性門檻與書卷註冊。
 * 只以 150 篇研究資料完整性作為書卷註冊條件。
 * 插圖由中央 ONE_COVER_POLICY 在書卷註冊後統一注入，
 * 因此本 registry 不再以 local study.illustration 作為入口門檻。
 */
(() => {
  "use strict";
  const D=window.ONE_DATA,P=D?.psalms;if(!D||!P)return;
  const expected=D.books?.find(book=>book[0]===19)?.[3]||150;
  const studies=P.chapterStudies||{};
  const missingStudies=[],incompleteStudies=[];
  const nonEmptyString=value=>typeof value==="string"&&value.trim().length>0;
  const nonEmptyArray=value=>Array.isArray(value)&&value.length>0;

  for(let number=1;number<=expected;number+=1){
    const study=studies[String(number)];
    if(!study){missingStudies.push(number);continue;}
    const complete=
      nonEmptyString(study.title)&&
      nonEmptyString(study.passage)&&
      nonEmptyString(study.movement)&&
      nonEmptyString(study.story)&&
      nonEmptyString(study.position)&&
      nonEmptyArray(study.route)&&
      nonEmptyArray(study.background)&&
      nonEmptyArray(study.scout)&&
      nonEmptyArray(study.connections)&&
      nonEmptyArray(study.questions)&&
      nonEmptyArray(study.prepare);
    if(!complete)incompleteStudies.push(number);
  }

  P.number=19;P.code="PSA";P.zhCode="PSA";P.enCode="PSA";P.name="詩篇";P.nameEn="Psalms";
  P.chapters=Array.from({length:expected},(_,index)=>studies[String(index+1)]?.title||`第 ${index+1} 篇`);
  P.summary=P.summary||"詩篇把讚美、哀歌、智慧、君王、聖所、錫安與信靠帶進神百姓的祈禱生活；五卷詩集從兩條道路與受膏君王開篇，最後匯聚成普世的哈利路亞。";
  P.meta=P.meta||[["位置","舊約詩歌智慧書 · 第19卷"],["文體","詩歌 · 禱告 · 智慧 · 君王詩"],["篇數","150篇"],["核心線索","耶和華作王 · 妥拉 · 受膏者 · 錫安 · 苦難 · 信靠 · 讚美"]];
  P.nowCards=P.nowCards||[["五卷","1–41 · 42–72 · 73–89 · 90–106 · 107–150"],["讀法","詩歌運動 · 題註 · 平行 · 轉折 · 禱告"]];

  const ready=missingStudies.length===0&&incompleteStudies.length===0;
  document.documentElement.dataset.psalmsReady=ready?"true":"partial";
  document.documentElement.dataset.psalmsStudyCount=String(Object.keys(studies).filter(key=>/^\d+$/.test(key)).length);
  document.documentElement.dataset.psalmsMissingStudies=missingStudies.join(",");
  document.documentElement.dataset.psalmsIncompleteStudies=incompleteStudies.join(",");

  if(ready){
    if(typeof D.registerStudyBook==="function")D.registerStudyBook(19,P,{source:"psalms-registry"});
    else D.studyBooks={...(D.studyBooks||{}),19:P};
  }else{
    console.error(`[ONE Psalms] registration blocked: missing=${missingStudies.join(",")||"none"}; incomplete=${incompleteStudies.join(",")||"none"}.`);
  }
})();
