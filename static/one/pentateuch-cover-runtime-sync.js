/* ONE Pentateuch cover runtime sync.
 * Guarantees audited Doré mappings for books 2–5 are visible to the canonical
 * registry and re-applied after all book data/app scripts have settled.
 */
(() => {
  "use strict";
  const D=window.ONE_DATA;
  const R=window.ONE_DORE_COVER_REGISTRY;
  if(!D||!R)return;

  const syncRegistry=()=>{
    R.maps=R.maps||{};
    [2,3,4,5].forEach(bookNumber=>{
      const mapping=D.studyBooks?.[bookNumber]?.canonicalDoreMapping;
      if(mapping&&typeof mapping==="object") R.maps[bookNumber]={...mapping};
    });
  };

  const refresh=()=>{
    syncRegistry();
    const policy=window.ONE_COVER_POLICY;
    if(!policy)return;
    [2,3,4,5].forEach(bookNumber=>policy.applyBook?.(bookNumber));
    policy.applyAll?.();

    /* If the current chapter is one of the newly loaded Pentateuch books,
     * force the visible cover element to the canonical resolver result now.
     */
    const currentBook=Number(D.current?.book);
    const currentChapter=Number(D.current?.nextChapter||1);
    if(currentBook>=2&&currentBook<=5){
      const art=policy.getCover?.(currentBook,currentChapter);
      const img=document.getElementById("chapter-cover-art");
      const credit=document.getElementById("chapter-art-credit");
      if(img){
        if(art?.src){img.src=art.src;img.alt=art.alt||"";img.hidden=false;}
        else{img.removeAttribute("src");img.alt="";img.hidden=true;}
      }
      if(credit){
        if(art?.source){credit.href=art.source;credit.textContent=art.title||"Gustave Doré";credit.hidden=false;}
        else credit.hidden=true;
      }
    }
    document.documentElement.dataset.pentateuchCoverSync="ready";
  };

  syncRegistry();
  if(document.readyState==="loading") document.addEventListener("DOMContentLoaded",()=>setTimeout(refresh,0),{once:true});
  else setTimeout(refresh,0);
  window.addEventListener("load",()=>setTimeout(refresh,0),{once:true});
})();

/* ONE exact-reference reader repair.
 * Keeps Scripture in row[3], never promotes explanation text, and repairs the
 * currently visible connection DOM after one-app.js has rendered.
 */
(()=>{
  "use strict";
  const D=window.ONE_DATA;if(!D?.studyBooks)return;
  const scriptureByReference={
    "申命記 31:6–8":"你們當剛強壯膽，不要害怕，也不要畏懼他們，因為耶和華－你的上帝和你同去。他必不撇下你，也不丟棄你。摩西召了約書亞來，在以色列眾人眼前對他說：你當剛強壯膽！因為，你要和這百姓一同進入耶和華向他們列祖起誓應許所賜之地；你也要使他們承受那地為業。耶和華必在你前面行；他必與你同在，必不撇下你，也不丟棄你。不要懼怕，也不要驚惶。",
    "申命記 7:1–6":"耶和華－你上帝領你進入要得為業之地，從你面前趕出許多國民，就是赫人、革迦撒人、亞摩利人、迦南人、比利洗人、希未人、耶布斯人，共七國的民，都比你強大。耶和華－你上帝將他們交給你擊殺，那時你要把他們滅絕淨盡，不可與他們立約，也不可憐恤他們。不可與他們結親。不可將你的女兒嫁他們的兒子，也不可叫你的兒子娶他們的女兒；因為他必使你兒子轉離不跟從主，去事奉別神，以致耶和華的怒氣向你們發作，就速速地將你們滅絕。你們卻要這樣待他們：拆毀他們的祭壇，打碎他們的柱像，砍下他們的木偶，用火焚燒他們雕刻的偶像。因為你歸耶和華－你上帝為聖潔的民；耶和華－你上帝從地上的萬民中揀選你，特作自己的子民。",
    "詩篇 114:3–5":"滄海看見就奔逃；約旦河也倒流。大山踴躍，如公羊；小山跳舞，如羊羔。滄海啊，你為何奔逃？約旦哪，你為何倒流？"
  };

  const applyData=()=>{
    let applied=0;
    for(const book of Object.values(D.studyBooks))for(const study of Object.values(book?.chapterStudies||{}))for(const row of (Array.isArray(study?.connections)?study.connections:[])){
      if(!Array.isArray(row))continue;
      const scripture=scriptureByReference[String(row[0]||'').trim()];
      if(scripture){row[3]=scripture;applied++;}
    }
    return applied;
  };

  const repairVisible=()=>{
    document.querySelectorAll('.connection-grid > article').forEach(article=>{
      const reference=article.querySelector('header strong')?.textContent?.trim();
      const scripture=scriptureByReference[reference];
      if(!scripture)return;
      article.querySelectorAll('*').forEach(node=>{
        const t=(node.textContent||'').trim();
        if(t.includes('SCRIPTURE PENDING')||t.includes('經文待補')||t.includes('本條目前只保留串珠關係與說明'))node.remove();
      });
      let quote=article.querySelector('blockquote[data-one-scripture="true"]');
      if(!quote){quote=document.createElement('blockquote');quote.dataset.oneScripture='true';const note=article.querySelector('.connection-note');article.insertBefore(quote,note||null);}
      quote.textContent=scripture;
    });
  };

  const applied=applyData();
  queueMicrotask(repairVisible);
  setTimeout(repairVisible,0);
  window.addEventListener('load',()=>setTimeout(repairVisible,0),{once:true});
  const detail=document.getElementById('chapter-detail');
  if(detail)new MutationObserver(()=>queueMicrotask(repairVisible)).observe(detail,{childList:true,subtree:true});
  window.ONE_EXACT_REFERENCE_READER_REPAIR={applied,references:Object.keys(scriptureByReference).length};
})();
