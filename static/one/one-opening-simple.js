/* ONE opening rail compatibility layer.
 * The actual wheel / pointer / keyboard rail interaction belongs to one-app.js.
 * Do not intercept it here: unvisited books stay as numbers and reveal their names
 * only when they reach the rail focus; visited books keep their status treatment.
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

  /* Cross-origin scripture resilience.
   * We cannot inspect YouVersion's iframe DOM, so an application-level error does
   * not surface as iframe.onerror. Instead each freshly rendered chapter receives
   * a unique navigation URL, plus a manual reload that rebuilds only that frame.
   */
  const scriptureStyle=document.createElement("style");
  scriptureStyle.textContent=`
    .one-scripture-reload{
      margin-left:.65rem;
      padding:0;
      border:0;
      color:inherit;
      background:transparent;
      font:inherit;
      text-decoration:underline;
      text-underline-offset:.18em;
      cursor:pointer;
    }
    .one-scripture-reload:hover{opacity:.68}
    .one-scripture-reload:focus-visible{outline:1px solid currentColor;outline-offset:.2rem}
  `;
  document.head.append(scriptureStyle);

  const freshYouVersionUrl=source=>{
    try{
      const url=new URL(source,location.href);
      url.searchParams.set("one_embed",String(Date.now()));
      return url.toString();
    }catch(error){
      return source+(source.includes("?")?"&":"?")+"one_embed="+Date.now();
    }
  };

  const enhanceEnglishScripture=root=>{
    root.querySelectorAll?.('.scripture-reading__pages article[lang="en"]').forEach(article=>{
      if(article.dataset.oneEnglishReady==="true")return;
      const frame=article.querySelector("iframe");
      const head=article.querySelector(":scope > div");
      const canonical=head?.querySelector('a[href*="bible.com"]');
      const source=frame?.dataset.src||frame?.getAttribute("src")||canonical?.href;
      if(!frame||!head||!source)return;

      article.dataset.oneEnglishReady="true";
      frame.dataset.oneBaseSrc=source;
      frame.removeAttribute("data-src");
      frame.loading="eager";
      frame.src=freshYouVersionUrl(source);

      const reload=document.createElement("button");
      reload.type="button";
      reload.className="one-scripture-reload";
      reload.textContent="Reload English";
      reload.setAttribute("aria-label","重新載入本章英文 NIV 經文");
      reload.addEventListener("click",()=>{
        reload.disabled=true;
        const oldText=reload.textContent;
        reload.textContent="Reloading…";
        frame.src="about:blank";
        requestAnimationFrame(()=>requestAnimationFrame(()=>{
          frame.src=freshYouVersionUrl(frame.dataset.oneBaseSrc||source);
          setTimeout(()=>{reload.disabled=false;reload.textContent=oldText},900);
        }));
      });
      head.append(reload);

      frame.addEventListener("error",()=>{
        if(frame.dataset.oneNetworkRetry==="true")return;
        frame.dataset.oneNetworkRetry="true";
        frame.src=freshYouVersionUrl(frame.dataset.oneBaseSrc||source);
      });
    });
  };

  const chapterDetail=document.getElementById("chapter-detail");
  if(chapterDetail){
    enhanceEnglishScripture(chapterDetail);
    const scriptureObserver=new MutationObserver(()=>enhanceEnglishScripture(chapterDetail));
    scriptureObserver.observe(chapterDetail,{childList:true,subtree:true});
  }

  /* Canonical 66-book illustration runtime.
   * This deliberately lives in the shared layer, never in a book-specific patch.
   * Data may identify an illustration as historical or generated, but either kind
   * receives exactly the same ONE cover/frame treatment. Missing or broken art is
   * presentation-only: it can never disable a book, a chapter, or chapter navigation.
   */
  const illustrationStyle=document.createElement("style");
  illustrationStyle.textContent=`
    .chapter-illustration.is-missing a{display:none}
    .chapter-illustration__fallback{
      display:block;
      width:100%;
      aspect-ratio:5/8;
      background:
        radial-gradient(ellipse at 50% 36%,rgba(206,189,116,.16),transparent 58%),
        linear-gradient(145deg,rgba(38,31,20,.96),rgba(13,15,14,.99));
    }
    .chapter-illustration.is-missing figcaption{display:none}
  `;
  document.head.append(illustrationStyle);

  const chapterContext=()=>{
    const data=window.ONE_DATA;
    const book=Number(document.body.dataset.book);
    const chapter=Number(chapterDetail?.dataset.chapter);
    const study=data?.studyBooks?.[book]?.chapterStudies?.[String(chapter)];
    return Number.isInteger(book)&&Number.isInteger(chapter)&&study?{book,chapter,study}:null;
  };

  const normalizeIllustration=illustration=>{
    if(!illustration||typeof illustration!=="object")return null;
    const src=typeof illustration.src==="string"?illustration.src.trim():"";
    if(!src)return null;
    const kind=illustration.kind==="generated"?"generated":"historical";
    const creator=String(illustration.creator||illustration.artist||(kind==="historical"?"Gustave Doré":"ONE")).trim();
    const title=String(illustration.title||"").trim();
    const source=typeof illustration.source==="string"?illustration.source.trim():"";
    const alt=String(illustration.alt||title||"本章插圖").trim();
    return {src,kind,creator,title,source,alt,morningStar:Boolean(illustration.morningStar)};
  };

  const clearCoverArt=()=>{
    const now=document.querySelector(".now");
    const intro=document.querySelector(".now__intro");
    const cover=document.getElementById("chapter-cover-art");
    const credit=document.getElementById("chapter-art-credit");
    now?.style.removeProperty("--chapter-engraving");
    document.documentElement.style.removeProperty("--one-chapter-engraving");
    intro?.classList.remove("has-morning-star");
    if(cover){cover.removeAttribute("src");cover.alt="";cover.hidden=true}
    if(credit){credit.removeAttribute("href");credit.textContent="";credit.hidden=true}
  };

  const applyIllustrationRuntime=()=>{
    const context=chapterContext();
    if(!context)return;
    const {study}=context;
    const art=normalizeIllustration(study.illustration);
    const now=document.querySelector(".now");
    const intro=document.querySelector(".now__intro");
    const cover=document.getElementById("chapter-cover-art");
    const credit=document.getElementById("chapter-art-credit");
    const figure=chapterDetail?.querySelector(".chapter-illustration");

    intro?.classList.toggle("has-morning-star",Boolean(study.morningStar||art?.morningStar));

    if(!art){
      clearCoverArt();
      return;
    }

    const engraving=`url("${art.src.replaceAll('"','%22')}")`;
    now?.style.setProperty("--chapter-engraving",engraving);
    document.documentElement.style.setProperty("--one-chapter-engraving",engraving);

    if(cover){
      cover.hidden=false;
      cover.alt=art.alt;
      if(cover.getAttribute("src")!==art.src)cover.src=art.src;
      cover.onerror=()=>clearCoverArt();
    }

    const creditText=[art.creator,art.title].filter(Boolean).join(" · ");
    if(credit){
      credit.textContent=creditText;
      if(art.source){credit.href=art.source;credit.hidden=false}
      else{credit.removeAttribute("href");credit.hidden=!creditText}
    }

    if(!figure)return;
    figure.dataset.illustrationKind=art.kind;
    const image=figure.querySelector("img");
    const link=figure.querySelector("a");
    const caption=figure.querySelector("figcaption");
    if(caption)caption.textContent=creditText;
    if(link){
      if(art.source){link.href=art.source;link.target="_blank";link.rel="noopener"}
      else{link.removeAttribute("href");link.removeAttribute("target");link.removeAttribute("rel")}
    }
    if(image){
      image.alt=art.alt;
      image.onerror=()=>{
        figure.classList.add("is-missing");
        if(!figure.querySelector(".chapter-illustration__fallback")){
          const fallback=document.createElement("span");
          fallback.className="chapter-illustration__fallback";
          fallback.setAttribute("aria-hidden","true");
          figure.insertBefore(fallback,figure.firstChild);
        }
        clearCoverArt();
      };
    }
  };

  if(chapterDetail){
    applyIllustrationRuntime();
    const illustrationObserver=new MutationObserver(()=>requestAnimationFrame(applyIllustrationRuntime));
    illustrationObserver.observe(chapterDetail,{childList:true,subtree:false,attributes:true,attributeFilter:["data-chapter","data-book"]});
  }

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
        reducedMotion?"none":"transform .26s cubic-bezier(.22,.8,.3,1), color .14s ease, opacity .14s linear"
      );
      current.style.setProperty("--rail-scale","1.12");
    },reducedMotion?0:140);
  };

  const observer=new MutationObserver(records=>{
    if(!records.some(record=>record.attributeName==="class"))return;
    if(list.classList.contains("is-settled"))scheduleRebound();
    else clearRebound();
  });
  observer.observe(list,{attributes:true,attributeFilter:["class"]});

  const cancelOnInteraction=()=>clearRebound();
  list.addEventListener("pointerdown",cancelOnInteraction,{passive:true});
  list.addEventListener("wheel",cancelOnInteraction,{passive:true});
  list.addEventListener("keydown",cancelOnInteraction);

  if(list.classList.contains("is-settled"))scheduleRebound();
})();
