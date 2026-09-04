/* ONE visible Doré cross-reference intelligence panel. */
(()=>{
  'use strict';
  const D=window.ONE_DATA||(window.ONE_DATA={});
  const CODES=['GEN','EXO','LEV','NUM','DEU','JOS','JDG','RUT','1SA','2SA','1KI','2KI','1CH','2CH','EZR','NEH','EST','JOB','PSA','PRO','ECC','SNG','ISA','JER','LAM','EZK','DAN','HOS','JOL','AMO','OBA','JON','MIC','NAM','HAB','ZEP','HAG','ZEC','MAL','MAT','MRK','LUK','JHN','ACT','ROM','1CO','2CO','GAL','EPH','PHP','COL','1TH','2TH','1TI','2TI','TIT','PHM','HEB','JAS','1PE','2PE','1JN','2JN','3JN','JUD','REV'];
  const byCode=new Map(CODES.map((code,index)=>[code,D.books?.[index]?.[1]||code]));
  const esc=value=>String(value??'').replace(/[&<>"']/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
  const canonical=(book,chapter,verse)=>`bible.ref.${book}.${Number(chapter)}.${Number(verse)}`;
  const parseRef=ref=>{const m=String(ref||'').match(/(?:bible\.ref\.)?([1-3]?[A-Z]{2,3})\.(\d+)\.(\d+)/i);return m?{book:m[1].toUpperCase(),chapter:Number(m[2]),verse:Number(m[3])}:null};
  const refLabel=ref=>{const p=parseRef(ref);return p?`${byCode.get(p.book)||p.book} ${p.chapter}:${p.verse}`:String(ref||'').replace('bible.ref.','')};
  const relationLabel=type=>({quotation:'直接引用',parallel:'平行經文',entity_history:'人物／事件歷史',event:'事件',person:'人物',place:'地點',allusion:'呼應／暗引',lexical_original_language:'原文關聯',topic:'主題',traditional_cross_reference:'傳統串珠','cross-reference':'串珠'})[type]||'串珠';
  const sourceLabel=item=>item.source_label||({'neuu-bible-crossrefs':'OpenBible / TSK','dore-curated-scripture':'Doré 經文關係'})[item.source_dataset]||item.source_dataset||'Doré';
  const scoreLabel=score=>`${Math.round(Math.max(0,Math.min(1,Number(score)||0))*100)}%`;
  let openRuntimePromise=null,renderToken=0;

  function ensureOpenRuntime(){
    const engine=window.DoreBibleIntelligence;
    if(engine?.openCrossrefs)return Promise.resolve(engine);
    if(openRuntimePromise)return openRuntimePromise;
    openRuntimePromise=new Promise((resolve,reject)=>{
      const finish=()=>window.DoreBibleIntelligence?.openCrossrefs?resolve(window.DoreBibleIntelligence):reject(new Error('Doré open-cross-reference runtime unavailable'));
      const existing=document.getElementById('dore-open-crossrefs-runtime');
      if(existing){existing.addEventListener('load',finish,{once:true});setTimeout(finish,1500);return;}
      const script=document.createElement('script');script.id='dore-open-crossrefs-runtime';script.src='/dore/dore-open-crossrefs.js?v=search2-20260904a';script.async=false;script.onload=finish;script.onerror=()=>reject(new Error('無法載入 Doré 百萬串珠圖'));document.head.appendChild(script);
    });
    return openRuntimePromise;
  }

  function panelMarkup(book,chapter){
    return `<section class="dore-crossref-intelligence" data-dore-crossref-ui="v1" aria-labelledby="dore-crossref-title">
      <header class="dore-crossref-head"><div><p>DORÉ BIBLE INTELLIGENCE</p><h4 id="dore-crossref-title">百萬串珠圖</h4><span>從本章任一節出發，查看來源、票數／權重與多跳路徑。</span></div><strong data-dore-crossref-stats>正在連接圖譜…</strong></header>
      <form class="dore-crossref-controls" data-dore-crossref-controls>
        <label>本章第 <input name="verse" type="number" min="1" max="200" value="1" inputmode="numeric" aria-label="選擇本章節數"> 節</label>
        <label>來源 <select name="source"><option value="all">全部</option><option value="openbible">OpenBible</option><option value="tsk">TSK</option></select></label>
        <label>路徑 <select name="depth"><option value="1">一跳</option><option value="2">兩跳</option><option value="3">三跳</option></select></label>
        <button type="submit">探索關係</button>
      </form>
      <div class="dore-crossref-context"><span>${esc(byCode.get(book)||book)} ${Number(chapter)}</span><i>來源可追溯 · CC BY 4.0 corpus · 經文正文沿用 ONE 現有來源</i></div>
      <div class="dore-crossref-results" data-dore-crossref-results aria-live="polite"><p class="dore-crossref-loading">選擇節數後，Doré 會沿串珠圖展開關係。</p></div>
    </section>`;
  }

  function resultMarkup(item,index){
    const path=(item.path||[]).map(refLabel),provenance=item.provenance||{},votes=Number(item.source_votes||0);
    return `<article class="dore-crossref-card">
      <header><span>${String(index+1).padStart(2,'0')}</span><div><strong>${esc(refLabel(item.reference))}</strong><small>${esc(relationLabel(item.relation_type))}</small></div><b>${esc(scoreLabel(item.score))}</b></header>
      <div class="dore-crossref-meta"><span>${esc(sourceLabel(item))}</span>${votes?`<span>${votes.toLocaleString()} votes</span>`:''}<span>${Number(item.depth||1)} hop${Number(item.depth||1)>1?'s':''}</span></div>
      <details><summary>查看關係路徑與來源</summary><ol>${path.map((label,i)=>`<li><span>${i}</span>${esc(label)}</li>`).join('')}</ol><p>${esc(provenance.license||'CC BY 4.0')} · ${esc(provenance.dataset||item.source_dataset||'Doré')}</p></details>
    </article>`;
  }

  async function queryPanel(panel){
    const token=++renderToken,detail=document.getElementById('chapter-detail');
    const bookNumber=Number(detail?.dataset.book),chapter=Number(detail?.dataset.chapter),book=CODES[bookNumber-1];
    if(!book||!chapter)return;
    const form=panel.querySelector('[data-dore-crossref-controls]'),results=panel.querySelector('[data-dore-crossref-results]');
    const verse=Math.max(1,Math.min(200,Number(form.elements.verse.value)||1));form.elements.verse.value=String(verse);
    const source=form.elements.source.value,depth=Number(form.elements.depth.value)||1,ref=canonical(book,chapter,verse);
    results.innerHTML='<p class="dore-crossref-loading">Doré 正在沿圖譜尋找關係…</p>';
    try{
      const engine=await ensureOpenRuntime();
      const links=source==='all'?await engine.relatedAsync(ref,{depth,limit:18}):await engine.openCrossrefs.graph(ref,{depth,limit:18,source});
      if(token!==renderToken||!panel.isConnected)return;
      if(!links.length){results.innerHTML=`<p class="dore-crossref-empty">${esc(refLabel(ref))} 暫未找到符合目前篩選條件的串珠。可切換來源或路徑深度。</p>`;return;}
      results.innerHTML=links.map(resultMarkup).join('');
    }catch(error){if(token!==renderToken)return;results.innerHTML=`<p class="dore-crossref-error">${esc(error?.message||'Doré 串珠圖暫時無法使用')}</p>`;}
  }

  async function hydrateStats(panel){
    const target=panel.querySelector('[data-dore-crossref-stats]');
    try{
      const engine=await ensureOpenRuntime(),stats=await engine.openCrossrefs.stats();
      if(!panel.isConnected)return;
      target.textContent=`${Number(stats.directed_edges||0).toLocaleString()} 關係 · ${Number(stats.unique_verses||0).toLocaleString()} 節 · ${Number(stats.books||66)} 卷`;
    }catch(error){target.textContent='OpenBible + TSK · 可追溯串珠';}
  }

  function mount(){
    const detail=document.getElementById('chapter-detail');if(!detail)return;
    const section=detail.querySelector('.connection-section');if(!section||section.querySelector('[data-dore-crossref-ui]'))return;
    const bookNumber=Number(detail.dataset.book),chapter=Number(detail.dataset.chapter),book=CODES[bookNumber-1];if(!book||!chapter)return;
    section.insertAdjacentHTML('beforeend',panelMarkup(book,chapter));
    const panel=section.querySelector('[data-dore-crossref-ui]'),form=panel.querySelector('[data-dore-crossref-controls]');
    form.addEventListener('submit',event=>{event.preventDefault();queryPanel(panel)});
    hydrateStats(panel);queryPanel(panel);
  }

  function boot(){
    const detail=document.getElementById('chapter-detail');if(!detail)return;
    const observer=new MutationObserver(()=>queueMicrotask(mount));observer.observe(detail,{childList:true,subtree:false});
    window.addEventListener('one:bible-intelligence-ready',mount);window.addEventListener('dore:open-crossrefs-ready',mount);mount();
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();
