/* 詩篇 ONE：完整性門檻與書卷註冊。
 * 僅當 150 篇研究資料與 150 篇插圖全部存在時，才把詩篇暴露給 ONE。
 * 不提供插圖 fallback，也不覆寫其他已註冊經卷。
 */
(() => {
  "use strict";
  const D=window.ONE_DATA,P=D?.psalms;if(!D||!P)return;
  const expected=D.books?.find(book=>book[0]===19)?.[3]||150;
  const studies=P.chapterStudies||{};
  const missingStudies=[],missingIllustrations=[];
  for(let number=1;number<=expected;number+=1){
    const study=studies[String(number)];
    if(!study)missingStudies.push(number);
    else if(!study.illustration?.src||!study.illustration?.source)missingIllustrations.push(number);
  }
  P.number=19;P.code="PSA";P.zhCode="PSA";P.enCode="PSA";P.name="詩篇";P.nameEn="Psalms";
  P.chapters=Array.from({length:expected},(_,index)=>studies[String(index+1)]?.title||`第 ${index+1} 篇`);
  P.summary=P.summary||"詩篇把讚美、哀歌、智慧、君王、聖所、錫安與信靠帶進神百姓的祈禱生活；五卷詩集從兩條道路與受膏君王開篇，最後匯聚成普世的哈利路亞。";
  P.meta=P.meta||[["位置","舊約詩歌智慧書 · 第19卷"],["文體","詩歌 · 禱告 · 智慧 · 君王詩"],["篇數","150篇"],["核心線索","耶和華作王 · 妥拉 · 受膏者 · 錫安 · 苦難 · 信靠 · 讚美"]];
  P.nowCards=P.nowCards||[["五卷","1–41 · 42–72 · 73–89 · 90–106 · 107–150"],["讀法","詩歌運動 · 題註 · 平行 · 轉折 · 禱告"]];
  const ready=missingStudies.length===0&&missingIllustrations.length===0;
  document.documentElement.dataset.psalmsReady=ready?"true":"partial";
  document.documentElement.dataset.psalmsStudyCount=String(Object.keys(studies).filter(key=>/^\d+$/.test(key)).length);
  document.documentElement.dataset.psalmsMissingStudies=missingStudies.join(",");
  document.documentElement.dataset.psalmsMissingIllustrations=missingIllustrations.join(",");
  if(ready){
    if(typeof D.registerStudyBook==="function")D.registerStudyBook(19,P,{source:"psalms-registry"});
    else D.studyBooks={...(D.studyBooks||{}),19:P};
  }else{
    console.info(`[ONE Psalms] work in progress: ${expected-missingStudies.length}/${expected} studies; ${expected-missingIllustrations.length}/${expected} illustrations.`);
  }
})();
