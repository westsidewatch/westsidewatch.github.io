/* 約翰福音 ONE：開卷註冊、母版資料與入口保護
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

  /* Doré-original audit is the first visual action for a new book.
   * Only exact Gustave Doré originals belonging to John are selected here.
   * Additional originals for the same chapter remain recorded in the immutable 241 library.
   */
  john.canonicalDoreMapping=Object.freeze({
    2:213,  // The Marriage in Cana
    4:215,  // Jesus and the Woman of Samaria
    6:216,  // Jesus Walking on the Sea
    8:217,  // Jesus and the Woman Taken in Adultery
    11:218, // Resurrection of Lazarus
    18:219, // St. Peter Denying Christ
    19:222, // Nailing Christ to the Cross
    21:223  // The Miraculous Draught of Fishes
  });
  john.doreOriginalLibrary=Object.freeze({
    2:Object.freeze([213,214]),
    4:Object.freeze([215]),
    6:Object.freeze([216]),
    8:Object.freeze([217]),
    11:Object.freeze([218]),
    18:Object.freeze([219]),
    19:Object.freeze([220,221,222]),
    21:Object.freeze([223])
  });
  john.missingPlateBacklog=Object.freeze([1,3,5,7,9,10,12,13,14,15,16,17,20]);
  john.doreAuditStatus="P1_ORIGINALS_AUDITED";

  /* 約翰福音沿用 ONE 共用聖光福音地圖。
   * 108：事奉初期（約 1–5）；109：加利利海／提比哩亞海（約 6、21）；
   * 110：住棚節後至伯大尼前後（約 7–11）；111：進入耶路撒冷與受難週（約 12–19）；
   * 106：主前四年至主後三十年間的巴勒斯坦總圖，用於復活顯現（約 20）。
   */
  const mapAssignments={1:108,2:108,3:108,4:108,5:108,6:109,7:110,8:110,9:110,10:110,11:110,12:111,13:111,14:111,15:111,16:111,17:111,18:111,19:111,20:106,21:109};
  for(const [chapter,mapId] of Object.entries(mapAssignments)){
    const study=studies[chapter];
    if(study?.map)study.map.mapId=mapId;
  }

  D.studyBooks={...(D.studyBooks||{}),43:john};

  const allReady=Array.from({length:expected},(_,index)=>Boolean(studies[String(index+1)])).every(Boolean);
  document.documentElement.dataset.johnReady=allReady?"true":"partial";
  document.documentElement.dataset.johnDore="8-original-locked-chapters";
  document.documentElement.dataset.johnMissingPlates=String(john.missingPlateBacklog.length);

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
