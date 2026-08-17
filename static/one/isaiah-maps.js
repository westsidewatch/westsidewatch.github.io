/* Isaiah maps: use ONE's registered study-book object and existing map renderer schema. */
(() => {
  "use strict";
  const I=window.ONE_DATA?.isaiah;if(!I?.chapterStudies)return;
  const holy=(id,title,reference,guide,places)=>({reference,title,guide,places,source:`https://biblegeography.holylight.org.tw/index/condensedbible_map_detail?m_id=${String(id).padStart(3,'0')}`,image:`https://biblegeography.holylight.org.tw/images/index/condensedbible/map/${String(id).padStart(3,'0')}.GIF`,imageTitle:title});
  const maps={
    israel:holy(95,"賽圖一（095）以賽亞書中的以色列地各地","以賽亞書 7–12","先定位耶路撒冷、猶大、撒馬利亞與大馬士革，再看亞述壓力如何進入先知的信息。",["耶路撒冷／錫安","猶大","撒馬利亞／以法蓮","大馬士革／亞蘭","亞述方向"]),
    outside:holy(96,"賽圖二（096）以賽亞書中的以色列地之外各地","以賽亞書 13–23；49–55；63","這些章節的視野跨出猶大。先辨認列國彼此位置，再理解審判、僕人使命與錫安盼望。",["亞述","巴比倫","埃及／古實","摩押／以東","推羅／西頓"]),
    assyria:holy(75,"王下圖七（075）亞述帝國","以賽亞書 28–35","把猶大放進亞述帝國擴張的大背景，理解為何先知反覆責備倚靠埃及與政治聯盟。",["亞述帝國","北國以色列","猶大","埃及","耶路撒冷"]),
    hezekiah:holy(73,"王下圖五（073）猶大國受亞述之欺壓","以賽亞書 36–39","這組歷史章的地理核心是拉吉與耶路撒冷。西拿基立先攻猶大城邑，再威脅耶路撒冷。",["拉吉","耶路撒冷","猶大諸城","亞述軍進路"]),
    babylon:holy(76,"王下圖八（076）巴比倫帝國","以賽亞書 40–48","從巴比倫使者事件轉入被擄與歸回視野；用地圖掌握耶路撒冷與巴比倫之間的帝國尺度。",["耶路撒冷","巴比倫","米所波大米","歸回方向"])
  };
  const assign=(chapters,map)=>chapters.forEach(n=>{const s=I.chapterStudies[String(n)];if(s)s.map={...map,places:[...map.places]};});
  assign([7,8,9,10,11,12],maps.israel);assign([13,14,15,16,17,18,19,20,21,22,23],maps.outside);assign([28,29,30,31,32,33,34,35],maps.assyria);assign([36,37,38,39],maps.hezekiah);assign([40,41,42,43,44,45,46,47,48],maps.babylon);assign([49,50,51,52,53,54,55,63],maps.outside);
})();