/* ONE Luke entry guard.
 * Keeps Book 42 usable even if registration/cache/order drifts, and provides a
 * direct-entry fallback when the cover rail click does not open the book dialog.
 */
(() => {
  "use strict";
  const D=window.ONE_DATA;
  const luke=D?.luke;
  if(!D||!luke)return;

  const expected=D.books?.find(book=>book[0]===42)?.[3]||24;
  const studies=luke.chapterStudies||{};
  const titles=Array.from({length:expected},(_,index)=>studies[String(index+1)]?.title||`第 ${index+1} 章`);

  luke.number=42;
  luke.code="LUK";
  luke.zhCode="LUK";
  luke.enCode="LUK";
  luke.name="路加福音";
  luke.nameEn="Luke";
  luke.chapters=titles;
  luke.summary=luke.summary||"路加按次序見證耶穌是為萬民而來的救主；祂在聖靈中尋找失喪的人，定意走向耶路撒冷，並從復活開啟向萬邦的使命。";
  luke.meta=luke.meta||[["位置","新約第三卷 · 第42卷"],["文體","福音書 · 歷史敘事與旅程教導"],["章數","24章"],["核心線索","救恩 · 聖靈 · 禱告 · 失喪者 · 耶路撒冷 · 萬邦"]];

  D.studyBooks={...(D.studyBooks||{}),42:luke};

  const ready=Array.from({length:expected},(_,index)=>Boolean(studies[String(index+1)])).every(Boolean);
  document.documentElement.dataset.lukeReady=ready?"true":"partial";

  document.addEventListener("DOMContentLoaded",()=>{
    const item=document.querySelector('.cover-book[data-book="42"]');
    if(!item)return;

    // The book must never be presented as forthcoming once Luke data is loaded.
    item.classList.remove("forthcoming");
    item.classList.add("has-study");
    item.setAttribute("aria-label","第 42 卷，路加福音，可開始查考");

    // Normal ONE handling runs first. If it fails to open the dialog, use a
    // canonical deep-link reload; one-app will then select Book 42 itself.
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
