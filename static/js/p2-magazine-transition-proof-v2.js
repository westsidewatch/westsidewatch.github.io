/* P2 Magazine second visual-proof pass.
 * Reuses the homepage Sevenfold fold dynamics, real OS colors, approved
 * Morning Star v5.3 and one uninterrupted Jerusalem wall across both states.
 * Standalone proof only. All stage motion is scroll-owned by p2-living-water.js.
 */
(()=>{'use strict';
if(new URLSearchParams(location.search).get('magazineProof')!=='1')return;
const root=document.querySelector('.showcase'),magazine=root?.querySelector('.p2-magazine');
if(!root||!magazine)return;
root.dataset.magazineProof='true';
root.dataset.magazineDesign='dawn-night-v2';
const movements=[
 {name:'WATCH',number:'I',items:[['米斯巴','Mizpah'],['伯利恆一日','Bethlehem'],['門','The Gate'],['迦密','Carmel']],interlude:['細拉','Selah']},
 {name:'WALK',number:'II',items:[['以斯帖','Esther'],['亞杜蘭洞','Adullam'],['以馬忤斯','Emmaus']],interlude:['遠方無聲鴿','Jonath-elem-rechokim']},
 {name:'WITNESS',number:'III',items:[['以琳','Elim'],['別是巴','Beersheba'],['伯特利','Bethel'],['何烈山','Horeb']],interlude:['基尼烈','Kinneret']},
 {name:'WORSHIP',number:'IV',items:[['瑪拉拿','Maranatha']],interlude:null}
];
// All 12 official titles, three interludes and their order come from
// docs/MASTER_SITE_ARCHITECTURE.md §2. No invented individual URLs.
let index=0;
const toc=movements.map(m=>{
 const items=m.items.map(([zh,en])=>'<li class="mag2__entry"><span class="mag2__item-num">'+String(++index).padStart(2,'0')+'</span><span class="mag2__item-zh">'+zh+'</span><i lang="en">'+en+'</i></li>').join('');
 const inter=m.interlude?'<p class="mag2__interlude"><span>INTERLUDE</span><strong>'+m.interlude[0]+'</strong><i lang="en">'+m.interlude[1]+'</i></p>':'<p class="mag2__closing" lang="en">UNTIL THE MORNING</p>';
 return '<section class="mag2__movement" aria-label="'+m.name+'"><div class="mag2__mov-head"><span class="mag2__roman">'+m.number+'</span><h3>'+m.name+'</h3><span class="mag2__count">'+m.items.length+' COLUMNS</span></div><ol>'+items+'</ol>'+inter+'</section>';
}).join('');
const palettes=[
 ['water','var(--ws-water,#5b8fa8)'],
 ['pale-gold','var(--ws-pale-gold,#cfb881)'],
 ['olive','var(--ws-olive,#899783)'],
 ['harvest','var(--ws-harvest,#c6a889)'],
 ['crimson','var(--ws-crimson,#a06d78)'],
 ['daylight-mauve','var(--ws-daylight-mauve,#b08cac)'],
 ['first-light','var(--ws-first-light,#d6c7a5)']
];
magazine.innerHTML=
 '<div class="mag2__spread">'+
  '<aside class="mag2__dawn"><header class="mag2__side-mast"><span>WESTSIDE WATCH</span><span>02 / MAGAZINE</span></header>'+
   '<div class="mag2__dawn-body"><span class="mag2__section-mark">02 — THE JOURNAL</span>'+
     '<p class="mag2__cover-title" lang="en">Watch<br><em>for Dawn.</em></p>'+
     '<strong class="mag2__dawn-cn">西望雜誌</strong>'+
     '<div class="mag2__side-line"></div><p class="mag2__dawn-deck">從夜色中守望，直到晨光顯明。</p>'+
   '</div><div class="mag2__side-bottom"><span>AN EDITORIAL OF WATCHING</span><span>WESTSIDE / 02</span></div></aside>'+
  '<main class="mag2__stone" aria-label="西望雜誌完整編輯目錄">'+
   '<header class="mag2__stone-mast"><span>WESTSIDE WATCH / THE JOURNAL</span><span>VOLUME / 02</span></header>'+
   '<div class="mag2__stone-title"><span class="mag2__colophon">THE ORDER OF READING / 2026</span>'+
    '<h2 lang="en">The <em>Journal.</em></h2><p>西望雜誌 <span lang="en">— Contents</span></p></div>'+
   '<div class="mag2__index" role="group" aria-label="四個樂章、十二欄目、三段間奏">'+toc+'</div>'+
   '<div class="mag2__intro"><span>FOUR MOVEMENTS</span><p>觀看世界，與光同行；記錄生命，直到敬拜。</p><span>12 COLUMNS / 03 INTERLUDES</span></div>'+
   '<footer class="mag2__stone-footer"><span>WESTSIDE WATCH / 02—07</span><a href="/journal/" lang="en">ENTER THE JOURNAL ↗</a></footer>'+
  '</main>'+
  '<aside class="mag2__night"><header class="mag2__side-mast"><span>NOCTURNE</span><span>ROMANS / 13:12</span></header>'+
   '<div class="mag2__night-body"><span>OF THE NIGHT AND THE DAY</span>'+
    '<p class="mag2__night-type" lang="en">The night<br><em>is far spent.</em></p>'+
    '<div class="mag2__night-rule"></div>'+
    '<blockquote><p lang="en">The night is far spent, the day is at hand.</p>'+
     '<p lang="zh-Hant">黑夜已深，白晝將近。</p><cite lang="en">ROMANS 13:12 · KJV</cite></blockquote></div>'+
   '<div class="mag2__side-bottom"><span>THE DAY IS AT HAND</span><span>WESTSIDE / 02</span></div></aside>'+
 '</div>'+
 '<div class="mag2__curtains" aria-hidden="true">'+
  '<div class="mag2__curtain mag2__curtain--dawn">'+''+'</div>'+
  '<div class="mag2__curtain mag2__curtain--night"></div>'+
 '</div>'+
 '<div class="mag2__two-page" aria-hidden="true">'+
  '<div class="mag2__hero-dawn"><span class="mag2__hero-eyebrow">SEVENFOLD / FIRST LIGHT</span>'+
    '<p class="mag2__hero-word" lang="en">Dawn.</p><span class="mag2__hero-foot">02 / WATCH FOR THE MORNING</span></div>'+
  '<div class="mag2__hero-night"><span class="mag2__hero-eyebrow">ROMANS XIII / VERSE XII</span>'+
    '<div class="mag2__hero-scripture"><p lang="en">The night<br><em>is far spent.</em></p>'+
      '<div class="mag2__hero-rule"></div><strong lang="zh-Hant">黑夜已深，白晝將近。</strong>'+
      '<cite lang="en">THE DAY IS AT HAND · ROMANS 13:12 · KJV</cite></div>'+
    '<span class="mag2__hero-foot">NOCTURNE / WESTSIDE WATCH</span></div>'+
 '</div>'+
 '<div class="mag2__star" aria-hidden="true"><iframe tabindex="-1" title="晨星 v5.3 透明琉璃立體資產" src="/experiments/morning-star-3d-lab.html?asset=1&amp;autoplay=1" loading="lazy"></iframe></div>'+
 // One single physical image is fixed to the viewport, NEVER copied or
 // clipped into the moving doors: uninterrupted before and after opening.
 '<div class="mag2__wall" aria-hidden="true"><img src="/images/jerusalem-wall.png" alt="" loading="eager"></div>';
const container=magazine.querySelector('.mag2__curtain--dawn');
container.innerHTML=palettes.map(([name,color],i)=>'<div class="mag2__fold" data-color="'+name+'" data-layer="'+i+'" style="--fold-color:'+color+'"></div>').join('');
const left=magazine.querySelector('.mag2__curtain--dawn');
const right=magazine.querySelector('.mag2__curtain--night');
const folds=[...magazine.querySelectorAll('.mag2__fold')];
const spread=magazine.querySelector('.mag2__spread');
const twoPage=magazine.querySelector('.mag2__two-page');
const star=magazine.querySelector('.mag2__star');
const wall=magazine.querySelector('.mag2__wall');
const clamp=n=>Math.max(0,Math.min(1,n));
const smooth=n=>{n=clamp(n);return n*n*(3-2*n)};
// The same quartic acceleration as the protected Sevenfold P2 curtains.
const foldEase=v=>v<.5?8*v**4:1-(-2*v+2)**4/2;
const reduced=typeof matchMedia==='function'&&matchMedia('(prefers-reduced-motion: reduce)').matches;
function render(vh){
 const p=clamp((vh-2.85)/1);
 // A separate, scroll-owned chapter for changing color, opening and reading.
 const change=smooth(p/.44),door=smooth((p-.43)/.48),rise=smooth((p-.38)/.57);
 magazine.style.visibility=p>.00001?'visible':'hidden';
 magazine.style.clipPath='none';
 magazine.style.pointerEvents=p>=.995?'auto':'none';
 magazine.setAttribute('aria-hidden',p>=.995?'false':'true');
 for(let i=0;i<folds.length;i++){
  const phase=clamp((change*1.18-i*.067)/.70);
  const opened=foldEase(phase);
  folds[i].style.transform='scale3d(1,'+opened.toFixed(6)+',1)';
  folds[i].style.setProperty('--fold-progress',opened.toFixed(5));
  folds[i].style.zIndex=String(i+1);
 }
 right.style.clipPath='inset(0 0 '+(100-change*100).toFixed(3)+'% 0)';
 left.style.transform='translate3d('+(-50*door).toFixed(3)+'vw,0,0)';
 right.style.transform='translate3d('+(50*door).toFixed(3)+'vw,0,0)';
 spread.style.opacity=String(smooth((p-.42)/.23));
 const doubleOpacity=smooth((change-.22)/.50)*(1-smooth((door-.03)/.58));
 twoPage.style.opacity=String(doubleOpacity);
 // The same approved star moves from left dawn stage to the top-right of
 // the opened stone folio. It is not duplicated behind or over the TOC.
 const mobile=typeof matchMedia==='function'&&matchMedia('(max-width:700px)').matches;
 star.style.left=(25+(mobile?49:33)*door).toFixed(3)+'%';
 star.style.top=(42-(mobile?26:23)*door).toFixed(3)+'%';
 star.style.setProperty('--star-scale',(1-.48*door).toFixed(4));
 star.style.opacity=String(smooth((change-.27)/.48));
 star.style.transform='translate3d(-50%,calc(-50% + '+((1-rise)*28).toFixed(3)+'svh),0)';
 // Maintain the skyline in the same screen coordinates, not per column.
 wall.style.opacity=String(smooth((p-.17)/.18));
 magazine.style.setProperty('--mag2-door',door.toFixed(5));
 magazine.style.setProperty('--mag2-change',change.toFixed(5));
 magazine.dataset.magazineStage=p<.43?'sevenfold-night':door<.998?'opening':'contents';
}
window.wsP2MagazineProof={render};
render(Number(root.dataset.p2Progress)||0);
})();
