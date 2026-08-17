/* Isaiah maps: geography where it materially aids reading; no forced map per chapter. */
(() => {
  "use strict";
  const I=window.ONE_DATA?.isaiah;if(!I?.chapterStudies)return;
  const holy=(id,title,note)=>({mapId:id,title,note,source:`https://biblegeography.holylight.org.tw/index/condensedbible_map_detail?m_id=${id}`,image:`https://biblegeography.holylight.org.tw/images/index/condensedbible/map/${id}.GIF`,imageTitle:title,routes:[]});
  const maps={
    israel:holy(95,"賽圖一（095）以賽亞書中的以色列地各地","以賽亞在猶大事奉約六十年；此圖直接整理本卷所涉及的以色列地、猶大、耶路撒冷與周邊城邑，適合閱讀亞蘭—以法蓮危機及猶大受亞述威脅的章節。"),
    outside:holy(96,"賽圖二（096）以賽亞書中的以色列地之外各地","本圖直接整理以賽亞書所涉及的亞述、巴比倫、埃及、古實、摩押、以東、推羅、西頓等以色列地之外地名，適合列國默示與後半卷帝國背景。"),
    assyriaEmpire:holy(75,"王下圖七（075）亞述帝國","用於理解主前八世紀亞述擴張，以及亞蘭、北國以色列、猶大與亞述之間的政治地理關係。"),
    hezekiah:holy(73,"王下圖五（073）猶大國受亞述之欺壓","此圖直接包含希西家、西拿基立、拉吉、耶路撒冷及以賽亞預言背景，最適合賽 36–39 的歷史插段。"),
    babylon:holy(76,"王下圖八（076）巴比倫帝國","此圖直接提及賽 39:1 與希西家接待巴比倫使者，並展示後來巴比倫帝國與猶大被擄的地理背景。")
  };
  const assign=(chapters,map)=>chapters.forEach(n=>{const s=I.chapterStudies[String(n)];if(s)s.map={...map};});
  assign([7,8,9,10,11,12],maps.israel);
  assign([13,14,15,16,17,18,19,20,21,22,23],maps.outside);
  assign([28,29,30,31,32,33,34,35],maps.assyriaEmpire);
  assign([36,37,38,39],maps.hezekiah);
  assign([40,41,42,43,44,45,46,47,48],maps.babylon);
  assign([49,50,51,52,53,54,55],maps.outside);
  assign([63],maps.outside);
  I.mapPolicy={source:"聖光聖經地理",rule:"優先使用以賽亞書直接地圖（賽圖一 095、賽圖二 096）；歷史敘事再使用與希西家、亞述、巴比倫直接相關的既有地圖。只在地理、帝國關係、戰爭或遷徙能實質幫助理解時配置，同一歷史單元共享地圖。",mappedChapters:[7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,63]};
})();