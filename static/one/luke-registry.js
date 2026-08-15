/* 路加福音 ONE：開卷註冊與入口保護
 * 必須在所有 Luke 章資料載入完成後、one-map-catalog / one-app 之前執行。
 * 插圖配置由 mark-luke-illustrations.js 單一負責，避免舊映射覆蓋新資料。
 */
(() => {
  "use strict";
  const D=window.ONE_DATA;
  const luke=D?.luke;
  if(!D||!luke)return;

  const expected=D.books?.find(book=>book[0]===42)?.[3]||24;
  const studies=luke.chapterStudies||{};
  const chapters=Array.from({length:expected},(_,index)=>{
    const number=index+1;
    return studies[String(number)]?.title||`第 ${number} 章`;
  });

  luke.number=42;
  luke.code="LUK";
  luke.zhCode="LUK";
  luke.enCode="LUK";
  luke.name="路加福音";
  luke.nameEn="Luke";
  luke.chapters=chapters;
  luke.summary=luke.summary||"路加按次序見證耶穌是為萬民而來的救主；祂在聖靈中尋找失喪的人，定意走向耶路撒冷，並從復活開啟向萬邦的使命。";
  luke.meta=luke.meta||[["位置","新約第三卷 · 第42卷"],["文體","福音書 · 歷史敘事與旅程教導"],["章數","24章"],["核心線索","救恩 · 聖靈 · 禱告 · 失喪者 · 耶路撒冷 · 萬邦"]];

  D.studyBooks={...(D.studyBooks||{}),42:luke};

  const allReady=Array.from({length:expected},(_,index)=>Boolean(studies[String(index+1)])).every(Boolean);
  document.documentElement.dataset.lukeReady=allReady?"true":"partial";

  /* index.html 目前在 parser 階段載入本檔；在 ONE app 初始化前同步接入約翰福音
   * 全卷資料、註冊與逐章插圖。待 index.html 日後可安全改為直接 script 標籤時再移除此橋接。
   */
  if(!document.documentElement.dataset.johnLoader){
    document.documentElement.dataset.johnLoader="true";
    document.write([
      '<script src="./john-core.js?v=20260815a"><\\/script>',
      '<script src="./john-5-8.js?v=20260815a"><\\/script>',
      '<script src="./john-9-12.js?v=20260815a"><\\/script>',
      '<script src="./john-13-16.js?v=20260815a"><\\/script>',
      '<script src="./john-17-20.js?v=20260815a"><\\/script>',
      '<script src="./john-21.js?v=20260815a"><\\/script>',
      '<script src="./john-registry.js?v=20260815a"><\\/script>',
      '<script src="./john-illustrations.js?v=20260815b"><\\/script>'
    ].join(''));
  }

  /* index.html 目前在 parser 階段載入本檔；用 document.write 同步插入唯一的
   * 馬可／路加插圖配置，保證它在 one-map-catalog 與 one-app 初始化前完成。
   * 後續若 index.html 改為直接載入該檔，data 標記會阻止重複插入。
   */
  if(!document.documentElement.dataset.markLukeIllustrationsLoader){
    document.documentElement.dataset.markLukeIllustrationsLoader="true";
    document.write('<script src="./mark-luke-illustrations.js?v=20260815c"><\\/script>');
  }

  document.addEventListener("DOMContentLoaded",()=>{
    const item=document.querySelector('.cover-book[data-book="42"]');
    if(!item)return;
    item.classList.remove("forthcoming");
    item.classList.add("has-study");
    item.setAttribute("aria-label","第 42 卷，路加福音，可開始查考");
    item.addEventListener("click",()=>{
      if(!item.classList.contains("rail-current"))return;
      requestAnimationFrame(()=>{
        const dialog=document.getElementById("book-dialog");
        if(dialog&&!dialog.hidden)return;
        const url=new URL(location.href);
        url.searchParams.set("book","42");
        url.searchParams.set("chapter","1");
        location.assign(url.toString());
      });
    });
  });
})();
