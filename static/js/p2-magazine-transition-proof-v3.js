/* Magazine v3: book-opening editorial composition.
 * OFFICIAL magazine SVG. Sevenfold motion is parameter-parity with homepage
 * P2, preserving OS colors and 7 full-overlap curtains (not 7 tile bands).
 * Every scene transform is a pure function of the P2 scroll clock.
 */
(()=>{'use strict';
if(new URLSearchParams(location.search).get('magazineProof')!=='1')return;
const root=document.querySelector('.showcase'),magazine=root?.querySelector('.p2-magazine');
if(!root||!magazine)return;
root.dataset.magazineProof='true';
root.dataset.magazineDesign='xiwang-v3';
// Canon: docs/projects/watch-city-vol00/EDITORIAL_MAP.md; preserve confirmed titles and 4–4–2–2.
const movements=[{"name":"WATCH","number":"I","items":[["米斯巴","Mizpah",["守望，一座光明的城"]],["伯利恆","Bethlehem",[]],["門","The Gate",["城門口的人","耶路撒冷：在黑暗中軟弱，在光明中剛強","大希律：這個人會建造"]],["迦密","Carmel",["一萬年的建城禮"]]],"interlude":["細拉","Selah"]},{"name":"WALK","number":"II","items":[["以馬忤斯","Emmaus",["吾珥：離開一座大的城"]],["以琳","Elim",["若不是耶和華看守城池——古代攻城技術史"]],["別是巴","Beersheba",[]],["伯特利","Bethel",[]]],"interlude":["遠方無聲鴿","Jonath-elem-rechokim"]},{"name":"WITNESS","number":"III","items":[["以斯帖","Esther",["廚房裡的人｜你當像飛鳥往你的山"]],["亞杜蘭洞","Adullam",[],["黃淑華","江秀琴"]]],"interlude":["基尼烈","Kinneret"]},{"name":"WORSHIP","number":"IV","items":[["何烈山","Horeb",["房角石：整座城由此對齊"]],["瑪拉拿","Maranatha",["冠冕"]]],"interlude":null}];
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let serial=0;
const contents=movements.map(m=>{
 const entries=m.items.map(([zh,en,works,subjects])=>{
  const num=String(++serial).padStart(2,'0');
  const titles=works.map(w=>'<span class="mag3__work" lang="zh-Hant">〈'+esc(w)+'〉</span>').join('');
  const people=subjects?.length?'<span class="mag3__subjects" lang="zh-Hant">'+subjects.map(esc).join(' · ')+'</span>':'';
  return '<li class="mag3__entry"><span class="mag3__n">'+num+'</span><div class="mag3__entry-text"><div class="mag3__column"><span class="mag3__zh" lang="zh-Hant">'+esc(zh)+'</span><i lang="en">'+esc(en)+'</i></div>'+titles+people+'</div></li>';
 }).join('');
 const inter=m.interlude?'<p class="mag3__interlude"><b>INTERLUDE</b><span lang="zh-Hant">'+esc(m.interlude[0])+'</span><i lang="en">'+esc(m.interlude[1])+'</i></p>':'';
 return '<section class="mag3__movement" aria-label="'+esc(m.name)+'"><header class="mag3__movement-head"><span class="mag3__roman">'+m.number+'</span><h3 lang="en">'+esc(m.name)+'</h3></header><ol>'+entries+'</ol>'+inter+'</section>';
}).join('');
// Exact official P2 Sevenfold order and finishing water blue as p6.
// AFTER the water finish, the left spread reveals the magazine dawn gold.
// This adds no invented eighth band and uses the original homepage ease.
const palette=[
 ['p0','var(--ws-water,#5b8fa8)'],
 ['p1','var(--ws-first-light,#a2872a)'],
 ['p2','var(--ws-pale-gold,#cebd74)'],
 ['p3','var(--ws-olive,#738a5a)'],
 ['p4','var(--ws-harvest,#b8944a)'],
 ['p5','var(--ws-crimson,#a14d57)'],
 ['p6','var(--ws-water,#5b8fa8)']
];
// The existing magazine logo's ORIGINAL Chinese outlines, not synthetic text.
const glyph='<img class="mag3__xiwang-art" src="/images/westside-watch-xiwang-vertical.svg" alt="西望" width="210" height="430">';
// One master scene. Text composition exists ONCE, even when moving doors
// obscure it. The church's magazine fallback HTML is replaced only in proof.
magazine.innerHTML=
 '<div class="mag3__spread">'+
  '<aside class="mag3__left" aria-label="黎明與西望">' +
   '<div class="mag3__vertical-tag" lang="en">02 / WESTSIDE WATCH</div>'+
   
   '<span class="mag3__left-edition" lang="en">A WATCHFUL EDITION / 02</span>'+
  '</aside>'+
  '<main class="mag3__center" aria-label="西望 Vol.00：封面與正式目錄">'+
   '<section class="mag3__cover-page" aria-label="Vol.00 封面">'+
    '<header class="mag3__center-top"><span lang="en">WESTSIDE WATCH / VOL.00</span><span lang="en">2026 — THE EDITION</span></header>'+
    '<div class="mag3__brand"><img src="/images/westside-watch-masthead-landscape.svg" alt="WESTSIDE WATCH 西望，正式雜誌 Logo SVG" loading="eager"></div>'+
    '<span class="mag3__cover-edition" lang="en">A CITY OF LIGHT / SPECIAL EDITION</span>'+
    '<div class="mag3__cover-identity"><span class="mag3__cover-number" lang="en" aria-hidden="true">00</span>'+
     '<h1 class="mag3__issue-title" lang="zh-Hant">守望，<span>一座光明的城</span></h1></div>'+
    '<div class="mag3__cover-stories"><span class="mag3__cover-stories-label" lang="en">IN THIS ISSUE</span>'+
      '<p lang="zh-Hant">一萬年的建城禮<span aria-hidden="true"> / </span>城門口的人</p></div>'+
   '</section>'+
   '<section class="mag3__contents-page" aria-label="Vol.00 正式目錄">'+
     '<div class="mag3__contents-heading"><span class="mag3__section-marker" lang="en">CONTENTS<span>.</span></span><span class="mag3__contents-count" lang="zh-Hant">四樂章 · 十二欄目 · 三間奏</span></div>'+
     '<div class="mag3__index" role="region" tabindex="0" aria-label="四樂章、十二欄目、三間奏，可使用方向鍵捲動目錄">'+contents+'</div>'+
     '<footer class="mag3__center-bottom"><span lang="en">VOL.00 / 2026</span><a href="/journal/" lang="en">ENTER WESTSIDE WATCH ↗</a></footer>'+
   '</section>'+
  '</main>'+
  '<aside class="mag3__right" aria-label="黑夜與羅馬書經文">' +
   '<span class="mag3__night-edition" lang="en">ROMANS / XIII:12</span>'+
  '</aside>'+
 '</div>'+
 '<div class="mag3__doors" aria-hidden="true">'+
  '<div class="mag3__door mag3__door--left"><div class="mag3__folds">'+
     palette.map(([id,color],i)=>'<div class="mag3__fold mag3__fold--'+id+'" data-layer="'+i+'" style="--fold-color:'+color+'"></div>').join('')+
   '</div><div class="mag3__door-wall mag3__door-wall--left"></div></div>'+
  '<div class="mag3__door mag3__door--right"><div class="mag3__door-wall mag3__door-wall--right"></div></div>'+
 '</div>'+
 '<div class="mag3__night-quote" aria-label="羅馬書第十三章十二節">'+
  '<span class="mag3__scripture-kicker" lang="en">NOCTURNE / THE COMING DAY</span>'+
  '<div class="mag3__night-type" lang="en"><span>The night</span><em>is far spent,</em></div>'+
  '<p class="mag3__dayline" lang="en">the day <span>is at hand:</span></p>'+
  '<div class="mag3__scripture-cn" lang="zh-Hant">黑夜已深，<br>白晝將近。</div>'+
  '<cite class="mag3__cite" lang="en">ROMANS 13:12 / KJV</cite>'+
 '</div>'+
 '<div class="mag3__glyph-lift">'+glyph+'</div>'+
 '<div class="mag3__star" aria-hidden="true"><iframe tabindex="-1" title="晨星 v5.3／加快播放" src="/experiments/morning-star-3d-lab.html?asset=1&amp;autoplay=1&amp;speed=2.1" loading="eager"></iframe></div>'+
 // Door-attached half panos above; at the final triptych, this SINGLE
 // uninterrupted backing panorama replaces them. No static fixed top strip.
 '<div class="mag3__wall-final" aria-hidden="true"></div>';
const leftDoor=magazine.querySelector('.mag3__door--left');
const rightDoor=magazine.querySelector('.mag3__door--right');
const folding=[...magazine.querySelectorAll('.mag3__fold')];
const doors=magazine.querySelector('.mag3__doors');
const quote=magazine.querySelector('.mag3__night-quote');
const star=magazine.querySelector('.mag3__star');
const glyphLift=magazine.querySelector('.mag3__glyph-lift');
const wallFinal=magazine.querySelector('.mag3__wall-final');
const spread=magazine.querySelector('.mag3__spread');
const clamp=x=>Math.max(0,Math.min(1,x));
const smooth=x=>{x=clamp(x);return x*x*(3-2*x)};
const foldEase=v=>v<.5?8*v**4:1-(-2*v+2)**4/2;
// Strictly sequential. A scroll reversal precisely undoes every stage.
const timeline=Object.freeze({night:[0,.23],folds:[.23,.44],star:[.44,.69],hold:[.69,.75],open:[.75,.99]});
const phase=(p,window)=>smooth((p-window[0])/(window[1]-window[0]));
const reducedMotion=typeof matchMedia==='function'&&matchMedia('(prefers-reduced-motion: reduce)').matches;
// For reduced-motion users we snap between complete editorial states,
// never leave partially travelled door planes, enlarged glyphs or text.
const reducedStage=p=>p<.23?0:p<.44?.23:p<.69?.44:p<.99?.69:1;
function render(vh){
 // Start when the Church's real open-door completes, not 0.48vh later.
 const inputProgress=clamp((vh-2.37)/(3.85-2.37));
 const p=reducedMotion?reducedStage(inputProgress):inputProgress;
 const night=phase(p,timeline.night);
 const fold=phase(p,timeline.folds);
 const rise=phase(p,timeline.star);
 const door=phase(p,timeline.open);
 const mobile=typeof matchMedia==='function'&&matchMedia('(max-width:700px)').matches;
 // On phones the opened issue is one full-width scrolling page; its
 // closing-cover artwork must clear the article text while opening.
 const mobileCover=mobile?1-phase(p,[.76,.93]):1;
 magazine.style.visibility=p>.00001?'visible':'hidden';
 magazine.style.clipPath='none';
 magazine.style.pointerEvents=p>=.995?'auto':'none';
 // Hidden/transitional links and the scrollable directory must NOT enter Tab order.
 magazine.inert=p<.995;
 magazine.setAttribute('aria-hidden',p>=.995?'false':'true');
 // Right completely descends before the left side can begin its ascent.
 rightDoor.style.clipPath='inset(0 0 '+(100*(1-night)).toFixed(3)+'% 0)';
 leftDoor.style.clipPath='inset('+(100*(1-fold)).toFixed(3)+'% 0 0 0)';
 // Seven real narrow strips (8svh each), not seven full-height color slabs.
 folding.forEach((el,i)=>{
  const opened=foldEase(clamp((fold*1.11-i*.065)/.72));
  el.style.transform='translate3d(0,'+(103-109*opened).toFixed(4)+'svh,0)';
  el.style.opacity=String(1-phase(p,[.4,.45]));
  el.style.zIndex=String(i+1);
  el.style.visibility=fold>0&&p<.46?'visible':'hidden';
 });
 doors.style.setProperty('--mag3-gold',phase(p,[.39,.45]).toFixed(5));
 // 50vw leaves remain as the OUTSIDE 28vw of the final triptych.
 // No complete exit off-screen and no floating center contents in advance.
 leftDoor.style.transform='translate3d('+(-22*door).toFixed(3)+'vw,0,0)';
 rightDoor.style.transform='translate3d('+(22*door).toFixed(3)+'vw,0,0)';
 spread.style.opacity=String(phase(p,[.75,.95]));
 // The star and 西望 travel at the SAME time, while both doors are locked.
 // Their lateral reposition happens only during opening.
 const starX=25-11*door,starY=78-65*rise;
 star.style.left=starX.toFixed(3)+'%';
 star.style.top=starY.toFixed(3)+'%';
 star.style.opacity=String(phase(p,[.44,.49])*mobileCover);
 star.style.setProperty('--mag3-star-size',mobile?'min(43vw,174px)':'clamp(220px,18vw,308px)');
 glyphLift.style.left=(12.5-8.5*door).toFixed(3)+'%';
 glyphLift.style.width=(25-5*door).toFixed(3)+'%';
 glyphLift.style.top=(starY+19).toFixed(3)+'svh';
 glyphLift.style.transform='none';
 glyphLift.style.opacity=String(phase(p,[.44,.49])*mobileCover);
 // The verse is already composed at its FINAL width before the leaves open.
 // Translate its block with the right leaf; never rescale / reflow its type.
 quote.style.left=mobile?'52%':(60+13*door).toFixed(3)+'%';
 quote.style.width=mobile?'46%':'26%';
 quote.style.opacity=String(phase(p,[.10,.22])*mobileCover);
 wallFinal.style.opacity=String(phase(p,[.87,.99]));
 magazine.style.setProperty('--mag3-door',door.toFixed(5));
 magazine.style.setProperty('--mag3-rise',rise.toFixed(5));
 magazine.style.setProperty('--mag3-change',night.toFixed(5));
 magazine.dataset.magazineStage=p<.23?'right-night':p<.44?'left-sevenfold':p<.69?'star-lifts-xiwang':p<.75?'two-page-hold':p<.99?'opening':'contents';
}
window.wsP2MagazineProof={render};
render(Number(root.dataset.p2Progress)||0);
})();