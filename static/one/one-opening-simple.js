/* ONE opening rail compatibility layer.
 * The actual wheel / pointer / keyboard rail interaction belongs to one-app.js.
 * Do not intercept it here: unvisited books stay as numbers and reveal their names
 * only when they reach the rail focus; visited books keep their status treatment.
 *
 * When the rail settles, keep the focused book name visible but let the temporary
 * enlargement ease back to its resting size. This restores the original
 * "focus, confirm, rebound" rhythm without changing rail order or selection.
 */
(() => {
  "use strict";
  const list=document.getElementById("cover-books");
  if(!list)return;
  list.classList.add("one-rail-enabled");

  const reducedMotion=matchMedia("(prefers-reduced-motion: reduce)").matches;
  let reboundTimer=0;

  const clearRebound=()=>{
    clearTimeout(reboundTimer);
    reboundTimer=0;
    list.querySelectorAll(".cover-book").forEach(item=>{
      item.style.removeProperty("transition");
    });
  };

  const scheduleRebound=()=>{
    clearTimeout(reboundTimer);
    if(!list.classList.contains("is-settled"))return;
    reboundTimer=setTimeout(()=>{
      const current=list.querySelector(".cover-book.rail-current");
      if(!current||!list.classList.contains("is-settled"))return;
      current.style.setProperty(
        "transition",
        reducedMotion?"none":"transform .52s cubic-bezier(.22,.8,.3,1), color .2s ease, opacity .18s linear"
      );
      current.style.setProperty("--rail-scale","1.12");
    },reducedMotion?0:420);
  };

  const observer=new MutationObserver(records=>{
    if(!records.some(record=>record.attributeName==="class"))return;
    if(list.classList.contains("is-settled"))scheduleRebound();
    else clearRebound();
  });
  observer.observe(list,{attributes:true,attributeFilter:["class"]});

  if(list.classList.contains("is-settled"))scheduleRebound();
})();
