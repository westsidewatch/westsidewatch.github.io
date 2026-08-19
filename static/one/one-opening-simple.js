/* ONE opening rail compatibility layer.
 * The actual wheel / pointer / keyboard rail interaction belongs to one-app.js.
 * This layer keeps presentation compatibility and guarantees that one deliberate
 * click is one selection: a click may first let the rail settle visually, then it
 * completes the same selection automatically. Pointer drags are never promoted
 * into selections.
 *
 * When the rail settles, keep the focused book name visible but let the temporary
 * enlargement ease back quickly to its resting size. Any new interaction cancels
 * that rebound immediately so stale focus styling cannot linger under the pointer.
 *
 * The Psalm 36:9 block on the cover is display-only. The former button and
 * full-screen scripture interaction are removed without touching the cover layout.
 *
 * YouVersion is a cross-origin application and can occasionally render its own
 * transient error page inside an otherwise valid chapter iframe. ONE therefore
 * gives every English chapter a fresh navigation and an explicit reload control,
 * while retaining the canonical "Open at YouVersion" link as the final fallback.
 */
(() => {
  "use strict";

  const scriptureTrigger=document.getElementById("open-scripture");
  if(scriptureTrigger){
    const staticScripture=document.createElement("div");
    staticScripture.className="cover-scripture-static";
    staticScripture.setAttribute("aria-label","詩篇 36:9");
    staticScripture.innerHTML=scriptureTrigger.innerHTML;
    scriptureTrigger.replaceWith(staticScripture);
    document.getElementById("light-reading")?.remove();
  }

  const scriptureStyle=document.createElement("style");
  scriptureStyle.textContent=`
    .one-scripture-reload{margin-left:.65rem;padding:0;border:0;color:inherit;background:transparent;font:inherit;text-decoration:underline;text-underline-offset:.18em;cursor:pointer}
    .one-scripture-reload:hover{opacity:.68}
    .one-scripture-reload:focus-visible{outline:1px solid currentColor;outline-offset:.2rem}
  `;
  document.head.append(scriptureStyle);

  const freshYouVersionUrl=source=>{
    try{const url=new URL(source,location.href);url.searchParams.set("one_embed",String(Date.now()));return url.toString()}
    catch(error){return source+(source.includes("?")?"&":"?")+"one_embed="+Date.now()}
  };

  const enhanceEnglishScripture=root=>{
    root.querySelectorAll?.('.scripture-reading__pages article[lang="en"]').forEach(article=>{
      if(article.dataset.oneEnglishReady==="true")return;
      const frame=article.querySelector("iframe"),head=article.querySelector(":scope > div"),canonical=head?.querySelector('a[href*="bible.com"]');
      const source=frame?.dataset.src||frame?.getAttribute("src")||canonical?.href;
      if(!frame||!head||!source)return;
      article.dataset.oneEnglishReady="true";frame.dataset.oneBaseSrc=source;frame.removeAttribute("data-src");frame.loading="eager";frame.src=freshYouVersionUrl(source);
      const reload=document.createElement("button");reload.type="button";reload.className="one-scripture-reload";reload.textContent="Reload English";reload.setAttribute("aria-label","重新載入本章英文 NIV 經文");
      reload.addEventListener("click",()=>{reload.disabled=true;const oldText=reload.textContent;reload.textContent="Reloading…";frame.src="about:blank";requestAnimationFrame(()=>requestAnimationFrame(()=>{frame.src=freshYouVersionUrl(frame.dataset.oneBaseSrc||source);setTimeout(()=>{reload.disabled=false;reload.textContent=oldText},900)}))});
      head.append(reload);
      frame.addEventListener("error",()=>{if(frame.dataset.oneNetworkRetry==="true")return;frame.dataset.oneNetworkRetry="true";frame.src=freshYouVersionUrl(frame.dataset.oneBaseSrc||source)});
    });
  };

  const chapterDetail=document.getElementById("chapter-detail");
  if(chapterDetail){enhanceEnglishScripture(chapterDetail);const scriptureObserver=new MutationObserver(()=>enhanceEnglishScripture(chapterDetail));scriptureObserver.observe(chapterDetail,{childList:true,subtree:true})}

  const list=document.getElementById("cover-books");
  if(!list)return;
  list.classList.add("one-rail-enabled");

  const reducedMotion=matchMedia("(prefers-reduced-motion: reduce)").matches;
  let reboundTimer=0,pointerStart=null,pointerDragged=false,autoSelectTimer=0;

  const clearRebound=()=>{clearTimeout(reboundTimer);reboundTimer=0;list.querySelectorAll(".cover-book").forEach(item=>item.style.removeProperty("transition"))};
  const scheduleRebound=()=>{clearTimeout(reboundTimer);if(!list.classList.contains("is-settled"))return;reboundTimer=setTimeout(()=>{const current=list.querySelector(".cover-book.rail-current");if(!current||!list.classList.contains("is-settled"))return;current.style.setProperty("transition",reducedMotion?"none":"transform .26s cubic-bezier(.22,.8,.3,1), color .14s ease, opacity .14s linear");current.style.setProperty("--rail-scale","1.12")},reducedMotion?0:140)};

  const observer=new MutationObserver(records=>{if(!records.some(record=>record.attributeName==="class"))return;if(list.classList.contains("is-settled"))scheduleRebound();else clearRebound()});
  observer.observe(list,{attributes:true,attributeFilter:["class"]});

  /* Single deliberate click = one book selection.
   * one-app owns rail motion. If the clicked book is not current, its normal click
   * first calls settleTo(). We then wait for that same book to become rail-current
   * and invoke one keyboard-style click (detail===0), which one-app treats as the
   * actual selection. A pointer movement beyond the rail's 5px drag threshold
   * cancels this continuation, preserving drag-to-browse on desktop and mobile.
   */
  const cancelAutoSelect=()=>{clearTimeout(autoSelectTimer);autoSelectTimer=0};
  const finishSelectionWhenSettled=item=>{
    cancelAutoSelect();
    const started=performance.now();
    const check=()=>{
      if(!item.isConnected)return;
      if(item.classList.contains("rail-current")&&list.classList.contains("is-settled")){item.click();return}
      if(performance.now()-started<1200)autoSelectTimer=setTimeout(check,reducedMotion?0:24);
    };
    autoSelectTimer=setTimeout(check,reducedMotion?0:24);
  };

  list.addEventListener("pointerdown",event=>{clearRebound();cancelAutoSelect();pointerStart={x:event.clientX,y:event.clientY,id:event.pointerId};pointerDragged=false},{passive:true});
  list.addEventListener("pointermove",event=>{if(!pointerStart||event.pointerId!==pointerStart.id)return;if(Math.hypot(event.clientX-pointerStart.x,event.clientY-pointerStart.y)>5){pointerDragged=true;cancelAutoSelect()}},{passive:true});
  list.addEventListener("pointerup",()=>{setTimeout(()=>{pointerStart=null;pointerDragged=false},0)},{passive:true});
  list.addEventListener("pointercancel",()=>{pointerStart=null;pointerDragged=false;cancelAutoSelect()},{passive:true});
  list.addEventListener("click",event=>{
    if(event.detail===0||pointerDragged)return;
    const item=event.target.closest(".cover-book");
    if(!item||item.classList.contains("rail-current"))return;
    finishSelectionWhenSettled(item);
  });
  list.addEventListener("wheel",()=>{clearRebound();cancelAutoSelect()},{passive:true});
  list.addEventListener("keydown",event=>{clearRebound();cancelAutoSelect();if((event.key==="Enter"||event.key===" ")&&event.target===list){const item=list.querySelector(".cover-book.rail-current");if(item)item.click()} });

  if(list.classList.contains("is-settled"))scheduleRebound();
})();
