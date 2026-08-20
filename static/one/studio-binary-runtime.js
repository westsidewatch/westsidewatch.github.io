/* ONE Studio compatibility stub.
 * Keep presentation-only compatibility here.
 * Do not mutate ONE_COVER_POLICY or chapter study data.
 * No MutationObserver, timer, DOM writer loop, or navigation listener.
 */
(()=>{
  "use strict";
  if(!document.getElementById("one-cover-no-divider")){
    const style=document.createElement("style");
    style.id="one-cover-no-divider";
    style.textContent=".chapter-cover-chapter::before{display:none!important;content:none!important;}";
    document.head.append(style);
  }
  document.documentElement.dataset.oneStudioBinaryRuntime="presentation-only";
})();
