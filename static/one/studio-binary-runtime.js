/* ONE Studio binary runtime — retired compatibility stub.
 * Doré Studio assets are resolved by ONE_COVER_POLICY directly.
 * No MutationObserver, timer, DOM writer, or navigation listener.
 * This compatibility stub only installs a cross-browser cover typography guard.
 */
(()=>{
  "use strict";
  document.documentElement.dataset.oneStudioBinaryRuntime="retired-static-policy";
  if(document.getElementById("one-cover-type-guard")) return;
  const style=document.createElement("style");
  style.id="one-cover-type-guard";
  style.textContent=`
    .chapter-cover-book{top:61.5%!important;left:11%!important;right:11%!important;}
    .chapter-cover-book h2{font-size:clamp(1.75rem,8.6cqw,3.55rem)!important;line-height:1.06!important;gap:clamp(.16rem,.75cqw,.3rem)!important;letter-spacing:.025em!important;}
    .chapter-cover-book h2 i{font-size:clamp(.66rem,2.35cqw,.92rem)!important;line-height:1.08!important;letter-spacing:.27em!important;}
    .chapter-cover-chapter{top:76.8%!important;bottom:10.5%!important;left:12%!important;right:12%!important;}
    .chapter-cover-chapter::before{width:72%!important;margin:0 auto clamp(.38rem,1.8cqw,.68rem)!important;}
    .chapter-cover-chapter>strong{font-size:clamp(.78rem,3.45cqw,1.12rem)!important;line-height:1.12!important;}
    .chapter-cover-chapter>p{max-width:94%!important;margin:clamp(.12rem,.55cqw,.22rem) auto 0!important;font-size:clamp(.58rem,2.25cqw,.78rem)!important;line-height:1.22!important;overflow-wrap:normal!important;word-break:keep-all!important;}
    @media(max-width:650px){
      .chapter-cover-book{top:61%!important;left:10%!important;right:10%!important;}
      .chapter-cover-book h2{font-size:clamp(1.55rem,8.5cqw,2.8rem)!important;}
      .chapter-cover-chapter{top:76.5%!important;left:11%!important;right:11%!important;}
    }
    @container (max-width:360px){
      .chapter-cover-book{top:60.5%!important;}
      .chapter-cover-book h2{font-size:clamp(1.42rem,8.25cqw,2.35rem)!important;}
      .chapter-cover-chapter{top:76.2%!important;}
      .chapter-cover-chapter>p{font-size:clamp(.55rem,2.2cqw,.72rem)!important;}
    }
  `;
  document.head.append(style);
})();
