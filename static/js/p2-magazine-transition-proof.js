/* Magazine triptych proof, isolated from production by ?magazineProof=1.
 * Single scroll owner: static/p2/p2-living-water.js calls render(vh).
 * No timers, no independent progress, no modification of the Church V75 surface.
 */
(()=>{'use strict';
if(new URLSearchParams(location.search).get('magazineProof')!=='1')return;
const showcase=document.querySelector('.showcase'),magazine=showcase?.querySelector('.p2-magazine');
if(!showcase||!magazine)return;
showcase.dataset.magazineProof='true';
const movement=(title,items)=>'<section class="p2-magazine-toc__movement"><h3>'+title+'</h3><ol>'+items.map(item=>'<li>'+item+'</li>').join('')+'</ol></section>';
const interlude=(cn,en)=>'<p class="p2-magazine-toc__interlude"><span>'+cn+'</span><i lang="en">'+en+'</i></p>';
// Names and order exactly as docs/MASTER_SITE_ARCHITECTURE.md §2,
// without making up individual routes for columns not independently routed.
const toc=[
 movement('WATCH',['米斯巴 <i lang="en">Mizpah</i>','伯利恆一日 <i lang="en">Bethlehem</i>','門 <i lang="en">The Gate</i>','迦密 <i lang="en">Carmel</i>']),
 interlude('細拉','Selah'),
 movement('WALK',['以斯帖 <i lang="en">Esther</i>','亞杜蘭洞 <i lang="en">Adullam</i>','以馬忤斯 <i lang="en">Emmaus</i>']),
 interlude('遠方無聲鴿','Jonath-elem-rechokim'),
 movement('WITNESS',['以琳 <i lang="en">Elim</i>','別是巴 <i lang="en">Beersheba</i>','伯特利 <i lang="en">Bethel</i>','何烈山 <i lang="en">Horeb</i>']),
 interlude('基尼烈','Kinneret'),
 movement('WORSHIP',['瑪拉拿 <i lang="en">Maranatha</i>'])
].join('');
const layers=['#ae9461','#b9a16e','#c6af7f','#d0b989','#dcc69a','#e5d0aa','#dbc294'];
magazine.innerHTML=
 '<div class="mag-proof__spread">'+
  '<aside class="mag-proof__dawn"><div class="mag-proof__mast" lang="en">WESTSIDE WATCH / 02 — 07</div>'+
  '<div class="mag-proof__dawn-copy"><span class="mag-proof__eyebrow" lang="en">The independent journal</span>'+
  '<h2 lang="en">Watch <em>for Dawn.</em></h2>'+
  '<p>西望雜誌</p></div><span class="mag-proof__folio" lang="en">THE HOUR OF FIRST LIGHT</span></aside>'+
  '<main class="mag-proof__stone" aria-label="西望雜誌：十二欄目與三段間奏">'+
   '<div class="mag-proof__stone-header"><span lang="en">WESTSIDE / INDEX</span><span lang="en">VOLUME / 02</span></div>'+
   '<div class="mag-proof__star" aria-hidden="true"><iframe tabindex="-1" title="晨星 v5.3 透明琉璃立體資產" loading="lazy" src="/experiments/morning-star-3d-lab.html?asset=1&amp;autoplay=1"></iframe></div>'+
   '<div class="mag-proof__catalog"><p class="mag-proof__catalog-kicker" lang="en">THE JOURNAL / FOUR MOVEMENTS</p>'+
   '<h2>西望雜誌 <em lang="en">Contents</em></h2>'+
   '<div class="p2-magazine-toc">'+toc+'</div></div>'+
   '<img class="mag-proof__wall" src="/images/jerusalem-wall.png" alt="" loading="lazy">'+
   '<div class="mag-proof__stone-foot"><span lang="en">TWELVE COLUMNS / THREE INTERLUDES</span><a href="/journal/" lang="en">ENTER THE JOURNAL ↗</a></div>'+
  '</main>'+
  '<aside class="mag-proof__night"><div class="mag-proof__mast" lang="en">NOCTURNE / EDITORIAL</div>'+
  '<p class="mag-proof__night-title" lang="en">Still <em>watching.</em></p>'+
  '<div class="mag-proof__night-footer"><span lang="en">READ / REFLECT / REMAIN</span>'+
  '<p>在夜色與晨光之間，以編輯的秩序，學習觀看。</p>'+
  '<span lang="en">WESTSIDE WATCH</span></div></aside>'+
 '</div>'+
 '<div class="mag-proof__curtains" aria-hidden="true">'+
  '<div class="mag-proof__curtain mag-proof__curtain--left">'+layers.map((c,i)=>'<div class="mag-proof__gold" data-curtain="'+i+'" style="--gold:'+c+'"></div>').join('')+'</div>'+
  '<div class="mag-proof__curtain mag-proof__curtain--right"></div>'+
 '</div>';
const spread=magazine.querySelector('.mag-proof__spread');
const left=magazine.querySelector('.mag-proof__curtain--left'),right=magazine.querySelector('.mag-proof__curtain--right');
const golds=[...magazine.querySelectorAll('.mag-proof__gold')],star=magazine.querySelector('.mag-proof__star');
const clamp=n=>Math.min(1,Math.max(0,n));
const smooth=n=>{n=clamp(n);return n*n*(3-2*n)};
function render(vh){
 const p=clamp((vh-2.85)/(3.85-2.85));
 const recolor=smooth(p/.45);
 const door=smooth((p-.44)/.47);
 const rise=smooth((p-.54)/.44);
 magazine.style.visibility=p>0?'visible':'hidden';
 magazine.style.clipPath='none';
 magazine.style.pointerEvents=p>=.995?'auto':'none';
 magazine.setAttribute('aria-hidden',p>=.995?'false':'true');
 spread.style.opacity=String(smooth((p-.38)/.25));
 left.style.transform='translate3d('+(-50*door).toFixed(3)+'vw,0,0)';
 right.style.transform='translate3d('+(50*door).toFixed(3)+'vw,0,0)';
 for(let i=0;i<golds.length;i++){
  const amount=smooth((recolor*1.16-i*.055)/.77);
  golds[i].style.clipPath='inset('+(100-amount*100).toFixed(3)+'% 0 0 0)';
 }
 right.style.clipPath='inset(0 0 '+(100-100*recolor).toFixed(3)+'% 0)';
 star.style.opacity=String(rise);
 star.style.transform='translate3d(0,'+((1-rise)*33).toFixed(3)+'svh,0)';
 magazine.style.setProperty('--mag-proof-open',door.toFixed(5));
 magazine.dataset.magazineStage=p<.44?'recolour':door<.999?'doors':'contents';
}
window.wsP2MagazineProof={render};
render(Number(showcase.dataset.p2Progress)||0);
})();
