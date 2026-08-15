/* 約翰福音 ONE：開卷註冊與入口保護
 * 必須在所有 John 章資料載入完成後、one-map-catalog / one-app 之前執行。
 */
(() => {
  "use strict";
  const D=window.ONE_DATA;
  const john=D?.john;
  if(!D||!john)return;

  const expected=D.books?.find(book=>book[0]===43)?.[3]||21;
  const studies=john.chapterStudies||{};
  const chapters=Array.from({length:expected},(_,index)=>{
    const number=index+1;
    return studies[String(number)]?.title||`第 ${number} 章`;
  });

  john.number=43;
  john.code="JHN";
  john.zhCode="JHN";
  john.enCode="JHN";
  john.name="約翰福音";
  john.nameEn="John";
  john.chapters=chapters;
  john.summary=john.summary||"約翰以記號與見證引人看見道成肉身的耶穌是基督、神的兒子，使信的人因祂的名得生命；從光與生命、節期與『我是』宣告，直到十字架、復活與彼得再次蒙召。";
  john.meta=john.meta||[["位置","新約第四卷 · 第43卷"],["文體","福音書 · 記號、見證與神學敘事"],["章數","21章"],["核心線索","生命 · 光 · 記號 · 見證 · 我是 · 榮耀 · 相愛 · 信"]];

  /* 約翰福音沿用 ONE 共用聖光福音地圖。
   * 108：事奉初期（約 1–5）；109：加利利海／提比哩亞海（約 6）；
   * 110：住棚節後至伯大尼前後（約 7–11）；111：進入耶路撒冷與受難週（約 12 起）。
   */
  const mapAssignments={5:108,6:109,7:110,8:110,9:110,10:110,11:110,12:111};
  for(const [chapter,mapId] of Object.entries(mapAssignments)){
    const study=studies[chapter];
    if(study?.map)study.map.mapId=mapId;
  }

  D.studyBooks={...(D.studyBooks||{}),43:john};

  const allReady=Array.from({length:expected},(_,index)=>Boolean(studies[String(index+1)])).every(Boolean);
  document.documentElement.dataset.johnReady=allReady?"true":"partial";

  document.addEventListener("DOMContentLoaded",()=>{
    const item=document.querySelector('.cover-book[data-book="43"]');
    if(!item)return;
    item.classList.remove("forthcoming");
    item.classList.add("has-study");
    item.setAttribute("aria-label","第 43 卷，約翰福音，可開始查考");
    item.addEventListener("click",()=>{
      if(!item.classList.contains("rail-current"))return;
      requestAnimationFrame(()=>{
        const dialog=document.getElementById("book-dialog");
        if(dialog&&!dialog.hidden)return;
        const url=new URL(location.href);
        url.searchParams.set("book","43");
        url.searchParams.set("chapter","1");
        location.assign(url.toString());
      });
    });
  });
})();
