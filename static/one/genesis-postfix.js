/* 創世記：沒有可靠旅行地圖的章節不渲染地圖板塊。 */
(() => {
  "use strict";
  const studies=window.ONE_DATA?.genesis?.chapterStudies;
  if(!studies)return;
  ["1","5"].forEach(chapter=>{
    if(studies[chapter])studies[chapter].map=null;
  });
})();
