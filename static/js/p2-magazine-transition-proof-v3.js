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
const movements=[
 {name:'WATCH',number:'I',items:[['米斯巴','Mizpah'],['伯利恆一日','Bethlehem'],['門','The Gate'],['迦密','Carmel']],interlude:['細拉','Selah']},
 {name:'WALK',number:'II',items:[['以斯帖','Esther'],['亞杜蘭洞','Adullam'],['以馬忤斯','Emmaus']],interlude:['遠方無聲鴿','Jonath-elem-rechokim']},
 {name:'WITNESS',number:'III',items:[['以琳','Elim'],['別是巴','Beersheba'],['伯特利','Bethel'],['何烈山','Horeb']],interlude:['基尼烈','Kinneret']},
 {name:'WORSHIP',number:'IV',items:[['瑪拉拿','Maranatha']],interlude:null}
];
let serial=0;
const contents=movements.map(m=>{
 const entries=m.items.map(([zh,en])=>'<li class="mag3__entry"><span class="mag3__n">'+String(++serial).padStart(2,'0')+'</span><span class="mag3__zh" lang="zh-Hant">'+zh+'</span><i lang="en">'+en+'</i></li>').join('');
 const inter=m.interlude?'<p class="mag3__interlude"><b>INTERLUDE</b><span lang="zh-Hant">'+m.interlude[0]+'</span><i lang="en">'+m.interlude[1]+'</i></p>':'';
 return '<section class="mag3__movement" aria-label="'+m.name+'"><header class="mag3__movement-head"><span class="mag3__roman">'+m.number+'</span><h3 lang="en">'+m.name+'</h3></header><ol>'+entries+'</ol>'+inter+'</section>';
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
const glyph='<svg class="mag3__xiwang-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 255" role="img" aria-label="西望，極細豎排" preserveAspectRatio="xMidYMid meet"><title>西望</title>'+
 '<text class="mag3__svg-character" x="60" y="113" text-anchor="middle">西</text>'+
 '<text class="mag3__svg-character" x="60" y="232" text-anchor="middle">望</text></svg>';
// One master scene. Text composition exists ONCE, even when moving doors
// obscure it. The church's magazine fallback HTML is replaced only in proof.
magazine.innerHTML=
 '<div class="mag3__spread">'+
  '<aside class="mag3__left" aria-label="黎明與西望">' +
   '<div class="mag3__vertical-tag" lang="en">02 / WESTSIDE WATCH</div>'+
   '<div class="mag3__glyph-lift">'+glyph+'</div>'+
   '<span class="mag3__left-edition" lang="en">A WATCHFUL EDITION / 02</span>'+
  '</aside>'+
  '<main class="mag3__center" aria-label="西望雜誌正式目錄">'+
   '<header class="mag3__center-top"><span lang="en">WESTSIDE / ISSUE 02</span><span lang="en">2026 — THE EDITION</span></header>'+
   '<div class="mag3__brand"><img src="/images/westside-watch-masthead-landscape.svg" alt="LivingWater WestWatch 西望，官方雜誌 Logo SVG" loading="eager"></div>'+
   '<div class="mag3__contents-heading"><div><span class="mag3__section-marker" lang="en">02 / THE INDEX</span><h2 lang="en">Contents<span>.</span></h2></div><p lang="zh-Hant">目錄</p></div>'+
   '<div class="mag3__index" role="group" aria-label="四樂章、十二欄目、三間奏">'+contents+'</div>'+
   '<footer class="mag3__center-bottom"><div><span lang="en">FOUR MOVEMENTS</span><span lang="en">12 COLUMNS / 03 INTERLUDES</span></div><a href="/journal/" lang="en">ENTER WESTWATCH ↗</a></footer>'+
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
  '<p class="mag3__dayline" lang="en">the day is at hand:</p>'+
  '<div class="mag3__scripture-cn" lang="zh-Hant">黑夜已深，<br>白晝將近。</div>'+
  '<cite class="mag3__cite" lang="en">ROMANS 13:12 / KJV</cite>'+
 '</div>'+
 '<div class="mag3__star" aria-hidden="true"><iframe tabindex="-1" title="晨星 v5.3／加快播放" src="/experiments/morning-star-3d-lab.html?asset=1&amp;autoplay=1&amp;speed=1.7" loading="eager"></iframe></div>'+
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
// The live homepage P2 uses exactly: reveal*1.11 - i*.065, / .72,
// quartic foldEase and top-center scaleY on full-overlap planes.
function render(vh){
 const p=clamp((vh-2.85)/1);
 const change=smooth(p/.39);
 const door=smooth((p-.35)/.51);
 const rise=smooth((p-.11)/.69);
 const mobile=typeof matchMedia==='function'&&matchMedia('(max-width:700px)').matches;
 magazine.style.visibility=p>0.00001?'visible':'hidden';
 magazine.style.clipPath='none';
 magazine.style.pointerEvents=p>=.995?'auto':'none';
 magazine.setAttribute('aria-hidden',p>=.995?'false':'true');
 folding.forEach((el,i)=>{
  const phase=clamp((change*1.11-i*.065)/.72);
  const opened=foldEase(phase);
  el.style.transform='scale3d(1,'+opened.toFixed(6)+',1)';
  el.style.zIndex=String(i+1);
  el.style.visibility='visible';
 });
 // Expose the *gold* under the completed seven-color water curtain.
 const gold=smooth((change-.84)/.16);
 doors.style.setProperty('--mag3-gold',gold.toFixed(5));
 rightDoor.style.clipPath='inset(0 0 '+(100* (1-change)).toFixed(3)+'% 0)';
 leftDoor.style.clipPath='inset(0 0 '+(100*(1-change)).toFixed(3)+'% 0)';
 leftDoor.style.transform='translate3d('+(-100*door).toFixed(3)+'%,0,0)';
 rightDoor.style.transform='translate3d('+(100*door).toFixed(3)+'%,0,0)';
 spread.style.opacity=String(smooth((p-.28)/.28));
 // The star is always at the same x; it ONLY rises vertically on the
 // LEFT, never cutting diagonally across the middle column.
 star.style.left=mobile?'17%':'14%';
 star.style.top=(78-62*rise).toFixed(3)+'%';
 star.style.opacity=String(smooth((change-.17)/.37)*(mobile?(1-smooth((door-.52)/.38)):1));
 star.style.setProperty('--mag3-star-size',mobile?'min(31vw,128px)':'clamp(152px,13vw,216px)');
 // The glyph is pulled upward by the star within the same left column.
 glyphLift.style.transform='translate3d(0,'+((1-rise)*32).toFixed(3)+'svh,0)';
 glyphLift.style.opacity=String(smooth((rise-.63)/.37));
 // Type does not animate diagonally into the center; the right paragraph
 // only compresses horizontally into its own destination column.
 quote.style.left=mobile?'52%':(52+20*door).toFixed(3)+'%';
 quote.style.width=mobile?'45%':(44-18*door).toFixed(3)+'%';
 quote.style.opacity=String(smooth((change-.4)/.38)*(mobile?(1-smooth((door-.05)/.55)):1));
 // The two physical wall halves travel with their respective doors.
 // The complete panorama becomes visible as they uncover the stone.
 wallFinal.style.opacity=String(smooth((door-.22)/.64));
 magazine.style.setProperty('--mag3-door',door.toFixed(5));
 magazine.style.setProperty('--mag3-rise',rise.toFixed(5));
 magazine.style.setProperty('--mag3-change',change.toFixed(5));
 magazine.dataset.magazineStage=p<.36?'sevenfold':door<.999?'open-book':'contents';
}
window.wsP2MagazineProof={render};
render(Number(root.dataset.p2Progress)||0);
})();