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

  /* John 17–21 were originally authored in the older ONE_JOHN_CHAPTERS shape.
   * Convert them once at registration time into the canonical shared-renderer schema.
   * This preserves the authored content while removing the 16/21 registration gap.
   */
  const legacy=window.ONE_JOHN_CHAPTERS||{};
  const asRows=(items,mapper)=>Array.isArray(items)?items.map(mapper):[];
  for(const [chapter,raw] of Object.entries(legacy)){
    if(studies[chapter]||!raw||typeof raw!=="object")continue;
    const n=Number(chapter);
    studies[chapter]={
      title:String(raw.title||`第 ${n} 章`),
      passage:`約翰福音 ${n}`,
      movement:String(raw.subtitle||raw.theme||"受難、復活與見證"),
      story:String(raw.story||""),
      position:String(raw.subtitle||raw.theme||`約翰福音第 ${n} 章`),
      route:asRows(raw.storyPath,item=>[String(item?.ref||""),[item?.title,item?.note].filter(Boolean).join("：")]),
      background:asRows(raw.background,item=>["背景",String(item||""),""]),
      scout:asRows(raw.observations,item=>String(item||"")),
      connections:asRows(raw.crossReferences,item=>[String(item?.ref||""),"串珠",String(item?.note||"")]),
      harmony:asRows(raw.harmony,item=>[String(item?.ref||""),String(item?.note||""),""]),
      questions:asRows(raw.questions,item=>String(item||"")),
      prepare:Array.isArray(raw.prepare)?raw.prepare.map(String):raw.prepare?[String(raw.prepare)]:[],
      map:raw.map?{
        reference:`約翰福音 ${n}`,
        title:`約翰福音 ${n} 地理`,
        guide:"按經文明示辨認本章移動與地點；具體建築位置不作過度確定。",
        places:asRows(raw.map.places,item=>String(item||"")),
        routes:asRows(raw.map.routes,item=>[String(item?.from||""),String(item?.to||""),String(item?.note||"")])
      }:undefined
    };
  }

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
    2:213,
    4:215,
    6:216,
    8:217,
    11:218,
    18:219,
    19:222,
    21:223
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
