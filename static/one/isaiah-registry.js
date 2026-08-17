/* Isaiah ONE registry — use the same study-book registration path as existing books. */
(() => {
  "use strict";
  const D=window.ONE_DATA,I=D?.isaiah;if(!D||!I)return;
  const expected=66,studies=I.chapterStudies||{},missing=[];
  for(let n=1;n<=expected;n+=1){
    const s=studies[String(n)];
    if(!s||!s.title||!s.passage||!s.story||!Array.isArray(s.route)||!Array.isArray(s.background)||!Array.isArray(s.scout)||!Array.isArray(s.connections)||!Array.isArray(s.questions)||!Array.isArray(s.prepare))missing.push(n);
  }
  I.number=23;I.code="ISA";I.zhCode="ISA";I.enCode="ISA";I.name="以賽亞書";I.nameEn="Isaiah";I.chapters=Array.from({length:expected},(_,i)=>studies[String(i+1)]?.title||`第 ${i+1} 章`);
  I.summary="以賽亞書在聖潔之神的審判與安慰之間展開：從猶大與列國的罪、以馬內利與大衛苗裔，到耶和華僕人、錫安復興，最後指向新天新地與萬民敬拜。";
  I.meta=[["位置","舊約先知書 · 第23卷"],["文體","先知預言 · 詩歌 · 歷史敘事"],["章數","66章"],["核心線索","聖潔 · 餘民 · 以馬內利 · 僕人 · 錫安 · 新創造"]];
  I.nowCards=[["主線","審判 · 安慰 · 僕人 · 錫安 · 新創造"],["歷史","亞述危機 · 希西家 · 巴比倫 · 古列 · 歸回"]];
  const ready=missing.length===0;
  document.documentElement.dataset.isaiahReady=ready?"true":"partial";
  document.documentElement.dataset.isaiahMissingStudies=missing.join(",");
  if(ready){
    if(typeof D.registerStudyBook==="function")D.registerStudyBook(23,I,{source:"isaiah-registry"});
    else D.studyBooks={...(D.studyBooks||{}),23:I};
  }else console.error(`[ONE Isaiah] registration blocked: missing=${missing.join(",")||"none"}`);
})();
/* The Doré registry must execute after every completed book dataset and before one-app.js. */
document.write('<script src="./one-dore-cover-registry.js?v=20260817a"><\/script>');