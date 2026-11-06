'use strict';
/* P2 04 manuscript gallery — physical-frame 03→04, no 01–03 changes.
 * Browser checks actual geometry/mask states at every designed beat.
 * Never mistake an engineering PASS for final visual art direction.
 */
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {chromium}=require('playwright');
const root=path.resolve(__dirname,'..');
const read=p=>fs.readFileSync(path.join(root,p),'utf8');
const html=read('static/experiments/p2-0104-olive-continuation.html');
const js=read('static/js/p2-0104-olive-continuation.js');
const css=read('static/css/p2-0104-olive-continuation.css');
const frozenSource=read('static/olive/components/speaker-baseline-v1/baseline.js');
const frozenCSS=read('static/olive/components/speaker-baseline-v1/baseline.css');
assert.match(js,/window\.OliveSpeakerBaseline/,
 'P2 must use the previously approved speaker name component, NOT naked PNG posters');
assert.match(js,/frozen\.mount\(art,target\)/,
 'every original speaker image must mount the frozen typographic shadow component');
assert.match(css,/\.olive-stage__artwork>olive-speaker-baseline/,
 'approved English must stay registered above the same original 3:4 image');
assert.match(frozenCSS,/--poster-optical-size/,
 'original optical-sizing/variable font authority must remain unchanged');
assert.match(frozenSource,/olive-speaker-english/,
 'original frozen English text must be provided by its original component');
assert.match(html,/p2-0103-release\.html\?embed=1/,'use real approved 01–03 stage');
assert.match(html,/id="olive-first"/,'first speaker must originate in the actual Doré frame');
assert.match(html,/id="olive-first-invitation"/,
 'first physical object must be a proper printed card, not a plain matte');
assert.match(html,/id="olive-invitation-left"/,'left settled speaker requires own card');
assert.match(html,/id="olive-invitation-right"/,'right settled speaker requires own card');
assert.match(css,/\.olive-stage__invitation\{/,
 'invitation is a real distinct graphic object');
assert.match(css,/04-olive-mount-etching-v8\.svg/,
 'the invitation must contain its own actual Mount of Olives landscape engraving');
assert.doesNotMatch(html,/olive-invitation__imprint|olive-invitation__colophon/,
 'no three competing invitation titles or redundant colophons');
assert.equal((html.match(/OLIVE <i>MOUNTAIN<\/i>/g)||[]).length,1,
 'exactly one page-level Olive Mountain masthead');
assert.match(js,/function printInsideCard\(c\)/,
 'original poster is geometrically mounted inside, not resized to hide old frame');
assert.match(js,/position\(firstInvitation,cardGeometry\.x/,
 'invitation card travels from original Doré frame with its mounted print');
assert.match(html,/id="olive-pair-next-left"/,'opposed double-spread image masks');
assert.match(html,/id="olive-overview"/,'all twelve original posters must converge in one finished layout');
assert.match(js,/first:10\.08,spread:10\.95/,'separate artwork handoff and two-poster formation');
assert.match(js,/groundStart:11\.15,groundEnd:11\.73/,'background MUST wait until after settled two-poster spread');
assert.match(js,/pairStart:11\.95,pairStep:\.83,pairDuration:\.62/,'six coherent original double-spread gallery stages');
assert.match(js,/indexStart:16\.25,indexEnd:17\.25/,'twelve real posters recompose after all six pairs');
assert.match(js,/getBoundingClientRect\(\)/,'original Doré source coordinates measured live');
assert.match(js,/style\.clipPath=/,'physical cutout/masks under one scroll owner');
assert.match(js,/ground\.style\.opacity='1'/,'background is NOT faded over the entering speakers');
assert.doesNotMatch(js,/setInterval|setTimeout|new Promise|animate\(|transitionDelay/,
 'no secondary timeline or time-based lag in P2 scroll choreography');
assert.doesNotMatch(html,/olive-main-image|olive-next-image|olive-speaker-names/,
 'remove prior speaker-player layout and small-thumb corridor');
assert.doesNotMatch(css,/04-olive-invitation-foil-v5\.svg/,
 'no ornate giant full-scene foil frame');
assert.match(css,/04-olive-mount-etching-v8\.svg/,
 'engraved Olives ridge is LOCAL to invitation, not a full-window wallpaper');
assert.match(css,/\/one\/cover-texture-antique-green\.png/,'use the real Scripture-cover green cloth');
assert.doesNotMatch(css,/cover-golden-shoot-frame-transparent\.png/,
 'the 04 transition must NOT duplicate the old ONE book-cover gilt frame');
const oliveCSS=css.slice(
 css.indexOf('.olive-surround__half{\n background-color:var(--ws-structure)'),
 css.indexOf('.olive-proof{'));
assert(oliveCSS.startsWith('.olive-surround__half{'),
 'the 04-only surface must be independently selected from the shared 03 mask geometry');
const cardCSS=css.slice(css.indexOf('.olive-stage__invitation{'),css.indexOf('.olive-stage__first{z-index:2'));
assert(!cardCSS.includes('/one/'),'04 invitation cards must not reuse the Bible cover stock');
const firstCSS=css.slice(css.indexOf('/* The incoming print lives'),css.indexOf('.olive-stage__poster{'));
assert(!oliveCSS.includes('/one/')&&!firstCSS.includes('/one/'),
 '04 final domain MUST NOT inherit ONE cover texture or gilt assets');
assert.match(oliveCSS,/background-color:var\(--ws-structure\)/,
 '04 field MUST consume Design OS semantic role instead of invented green');
assert.match(css,/\.p2-olive-stage\{[^}]*--ws-branch:var\(--ws-olive\)/,
 '04 scoped identity MUST bind to the OS canonical olive token');
assert.match(css,/\.olive-stage__invitation\{[^}]*background:color-mix\(in oklab,var\(--ws-deep\)/,
 'invitation stock MUST derive from OS semantic olive depth, not hard-coded teal');
assert.doesNotMatch(css,/#193d2e|#163a2a|#173c2a|#204432/i,
 'no prior invented dark green literal may remain');
const osCSS=read('static/css/westside-design-os.css');
assert.match(osCSS,/--ws-olive:#738a5a/,'exact OS olive anchor: #738A5A');
assert.match(css,/\.olive-stage__index-card\{[^}]*overflow:hidden/,
 '12 artwork rectangles must clip overflow');
assert.match(css,/\.olive-stage__index-card span\{[^}]*display:none!important/,
 'no external caption strip or overshooting print at index');
assert.doesNotMatch(css,/#e5d9b8|#e7e5d9|#ded1af/,
 'NO invented yellow intermediate or gray poster mat');
assert.match(html,/id="p2-olive-bridge"/,'bridge 03 reading world before changing 04 pigment');
assert.match(html,/olive-surround__half/,'MERSI left and right background masks exist');
assert.match(js,/revealSplitField\(ground,bg\)/,'paired field masks share one scroll clock');
assert.match(js,/rightHalf\.style\.clipPath=isInvitation\?/,
 'separate single-direction 03 source takeover from reversible 04 scene mask');
assert.match(js,/leftReveal=isInvitation\?ease\(\(reveal-\.52\)\/\.48\)/,
 'left must remain green Scripture cover as the right invitation enters');
assert.match(html,/id="olive-rubric"/,'reserved editorial masthead identity');
assert.match(css,/\.olive-stage__overview\{[^}]*background:transparent/,
 'index preserves full olive green and gold field, no white jump');
assert(fs.existsSync(path.join(root,'static/images/p2-realms/v15/04-olive-engraving-v1-5.svg')),
 'keep approved V1.5 source intact as archive');
const reliefSVG=read('static/images/p2-realms/v15/04-olive-mount-etching-v8.svg');
assert.match(reliefSVG,/Original native SVG copperplate vignette/,
 'hillside with trees and distant Jerusalem, not a two-line doodle');
assert.match(reliefSVG,/Mount of Olives/, 'independent 04 identity');
assert(!reliefSVG.includes('<image'), 'relief stays editable native SVG');
const out=path.join(root,'artifacts/p2-0104-olive');fs.mkdirSync(out,{recursive:true});
(async()=>{
 const browser=await chromium.launch({headless:true});
 try{
  for(const [width,height] of [[1648,928],[390,844]]){
   const page=await browser.newPage({viewport:{width,height},reducedMotion:'no-preference'});
   const errors=[];page.on('pageerror',e=>errors.push(e.stack||String(e)));
   await page.goto('http://127.0.0.1:4173/experiments/p2-0104-olive-continuation.html?d=9.30',
    {waitUntil:'domcontentloaded',timeout:45000});
   await page.waitForFunction(()=>{
    const st=document.getElementById('p2-olive-stage');
    const d=document.getElementById('p2-0103-original')?.contentDocument;
    const source=d?.getElementById('proof-original')?.contentDocument;
    return st?.dataset.p2FolioReady==='true'&&source
      ?.querySelector('.p2-magazine iframe:not(.p2-magazine__home-film)')?.contentDocument
      ?.getElementById('dual-cover');
   },null,{timeout:35000});
   // Previous previews passed while OMITTING the approved two-day English.
   // This is now a nonnegotiable visual/technical requirement.
   await page.waitForFunction(()=>{
      const main=document.querySelector('#olive-first .olive-stage__artwork>olive-speaker-baseline');
      const cards=[...document.querySelectorAll('#olive-overview .olive-stage__index-card')];
      return main?.shadowRoot?.querySelector('.olive-speaker-english')?.textContent==='WATCHMAN NEE' &&
        cards.length===12 &&
        cards.every(card=>{
          const over=card.querySelector('.olive-stage__artwork>olive-speaker-baseline');
          return over?.shadowRoot?.querySelector('.olive-speaker-english')?.textContent?.length>2;
        }) &&
        !!main.shadowRoot.querySelector('link[href*="speaker-baseline-v1/baseline.css"]')?.sheet;
   },null,{timeout:18000});
   const state=()=>page.evaluate(()=>{
    const st=document.getElementById('p2-olive-stage');
    const shell=document.getElementById('olive-proof');
    const image=document.getElementById('olive-first');
    const invitation=document.getElementById('olive-first-invitation');
    const cardLeft=document.getElementById('olive-invitation-left');
    const cardRight=document.getElementById('olive-invitation-right');
    const source=document.getElementById('p2-0103-original').contentDocument;
    const origRight=source.querySelector('#emmaus .emmaus__right').getBoundingClientRect();
    const left=document.getElementById('olive-pair-left');
    const right=document.getElementById('olive-pair-right');
    const nl=document.getElementById('olive-pair-next-left');
    const nr=document.getElementById('olive-pair-next-right');
    const ground=document.getElementById('p2-olive-surround');
    const neutral=document.getElementById('p2-olive-bridge');
    const overview=document.getElementById('olive-overview');
    const box=el=>{const b=el.getBoundingClientRect();return {x:b.x,y:b.y,w:b.width,h:b.height}};
    const get=el=>({visibility:getComputedStyle(el).visibility,
      src:el.querySelector('img')?.getAttribute('src')||'',
      clip:el.style.clipPath,box:box(el)});
    return {distance:+st.dataset.p2Distance,
      scene:st.dataset.p2Scene,frameReady:st.dataset.p2FolioReady,
      underlying:source.body.dataset.proofScene,
      first:+st.dataset.p2Bridge,spread:+st.dataset.p2Spread,
      reading:+st.dataset.p2ReadingField,method:st.dataset.p2FieldMethod,
      ground:+st.dataset.p2Ground,index:+st.dataset.p2Index,
      pairIndex:st.dataset.p2PairIndex||'0',pairBlend:st.dataset.p2PairBlend||'0',
      pairOrientation:st.dataset.p2PairOrientation,
      main:box(shell),masthead:box(document.getElementById('olive-rubric')),
      source:{...box(source.querySelector('#emmaus .emmaus__right')),folio:box(source.querySelector('#emmaus'))},
      firstFrame:get(image),
      invitation:{visibility:getComputedStyle(invitation).visibility,
       color:getComputedStyle(invitation).backgroundColor,
       bg:getComputedStyle(invitation).backgroundImage,
       relief:getComputedStyle(invitation.querySelector('.olive-card__relief')).backgroundImage,
       caption:invitation.querySelector('.olive-card__caption')?.textContent?.trim(),
       clip:invitation.style.clipPath,box:box(invitation)},
      pairCardLeft:{visibility:getComputedStyle(cardLeft).visibility,box:box(cardLeft),
       caption:cardLeft.querySelector('.olive-card__caption')?.textContent?.trim(),
       relief:box(cardLeft.querySelector('.olive-card__relief'))},
      pairCardRight:{visibility:getComputedStyle(cardRight).visibility,box:box(cardRight),
       caption:cardRight.querySelector('.olive-card__caption')?.textContent?.trim(),
       relief:box(cardRight.querySelector('.olive-card__relief'))},
      pairLeft:get(left),pairRight:get(right),
      incomingLeft:get(nl),incomingRight:get(nr),
      neutralCSS:{visibility:getComputedStyle(neutral).visibility,reveal:+neutral.dataset.reveal,
       halves:[...neutral.querySelectorAll('[data-side]')].map(x=>x.style.clipPath),
       cloth:getComputedStyle(neutral.querySelector('[data-side="left"]')).backgroundImage},
      groundCSS:{visibility:getComputedStyle(ground).visibility,
       opacity:getComputedStyle(ground).opacity,
       halves:[...ground.querySelectorAll('[data-side]')].map(x=>x.style.clipPath),
       left:+ground.dataset.leftReveal,right:+ground.dataset.rightReveal,
       texture:getComputedStyle(ground.querySelector('[data-side="left"]')).backgroundImage,
       parts:ground.querySelectorAll('.olive-surround__half').length},
      cards:[...overview.querySelectorAll('.olive-stage__index-card')].map(el=>
       ({src:el.querySelector('img')?.getAttribute('src'),...box(el)})),
      grid:overview.dataset.columns,
      overviewVisibility:getComputedStyle(overview).visibility,
      overviewPaper:getComputedStyle(overview).backgroundColor,
       pairDisplay:getComputedStyle(document.getElementById('olive-pair')).display,
       firstDisplay:getComputedStyle(document.getElementById('olive-first')).display,
       indexIsolated:st.dataset.p2IndexIsolated,
      ctaVisibility:getComputedStyle(document.getElementById('olive-enter')).visibility
    };
   });
   const go=async(d,label)=>{
    await page.evaluate(v=>{
     const t=document.getElementById('p2-olive-track');
     window.scrollTo({top:t.getBoundingClientRect().top+scrollY+innerHeight*v,behavior:'instant'});
    },d);
    await page.waitForFunction(v=>Math.abs(
     Number(document.getElementById('p2-olive-stage')?.dataset.p2Distance)-v)<.035,
     d,{timeout:18000});
    await page.waitForTimeout(140);
    const result=await state();
    if(label)await page.screenshot({path:path.join(out,width+'-'+label+'.png'),animations:'allow'});
    assert.equal(result.underlying,'03','approved 01–03 must stay on its original 03');
    return result;
   };
   const at03=await go(9.30,'00-original-emmaus');
   assert.equal(at03.scene,'03-held');
   assert.equal(at03.firstFrame.visibility,'hidden','04 must not enter before the 03 hold');
   assert.equal(at03.groundCSS.visibility,'hidden','Olive exterior must wait until the posters settle');
   assert.equal(at03.invitation.visibility,'hidden',
    '03 Doré remains fully intact before the invitation enters');
   const bridge=await go(9.76,'01-dore-frame-first-poster-half');
   const protectedFirst=await page.evaluate(()=>{
    const art=document.querySelector('#olive-first .olive-stage__artwork');
    const overlay=art?.querySelector('olive-speaker-baseline');
    const root=overlay?.shadowRoot;
    const name=root?.querySelector('.olive-speaker-english');
    const frame=root?.querySelector('.speaker-card');
    const a=art?.getBoundingClientRect(),b=overlay?.getBoundingClientRect();
    return {text:name?.textContent,slug:overlay?.dataset.speaker,
      posterSize:frame?.style.getPropertyValue('--poster-size'),
      opticalSize:frame?.style.getPropertyValue('--poster-optical-size'),
      font:name?getComputedStyle(name).fontFamily:'',
      ratio:b?b.width/b.height:0,
      fits:!!a&&!!b&&b.width<=a.width+1&&b.height<=a.height+1};
   });
   assert.equal(protectedFirst.text,'WATCHMAN NEE',
    'original large English WATCHMAN NEE must remain layered on the FIRST image');
   assert.equal(protectedFirst.slug,'watchman-nee');
   assert.equal(protectedFirst.posterSize,'11cqw',
    'never silently replace the two-day approved original English font size');
   assert.equal(protectedFirst.opticalSize,'43.96');
   assert(protectedFirst.font.includes('Bodoni Moda'),
    'original display font must load, not a generic small caption');
   assert(Math.abs(protectedFirst.ratio-.75)<.01&&protectedFirst.fits,
    'English master must stay image-relative in original 3:4 proportions');
   assert(bridge.first>.45&&bridge.first<.55,'same-frame handoff should be at midpoint');
   assert.equal(bridge.scene,'04-dore-handoff');
   assert(Math.abs(bridge.invitation.box.x-bridge.source.x)<2 &&
     Math.abs(bridge.invitation.box.w-bridge.source.w)<2,
     'the CARD, not the portrait, assumes the original Doré frame');
   assert.equal(bridge.invitation.visibility,'visible');
   assert(bridge.invitation.relief.includes('04-olive-mount-etching-v8.svg'),
     'invitation uses actual original 04 Olives copperplate landscape engraving');
   assert.equal(bridge.invitation.caption,'WATCHMAN NEE · 倪柝聲');
   assert(Math.abs(bridge.firstFrame.box.w/bridge.firstFrame.box.h-.75)<.01,
     'the protected 3:4 poster must mount INSIDE the invitation');
   assert(bridge.firstFrame.box.w<bridge.invitation.box.w &&
     bridge.firstFrame.box.h<bridge.invitation.box.h,
     'the editorial print must have real green-card margins');
   assert(bridge.firstFrame.src.includes('watchman-nee-editorial.png'));
   assert.equal(bridge.groundCSS.visibility,'hidden');
   assert.equal(bridge.neutralCSS.visibility,'hidden');
   const sourceTakeover=await go(10.18,'01b-source-plate-no-old-engraving-exposure');
   assert.equal(sourceTakeover.invitation.visibility,'visible',
     'the old source is claimed by a complete foil invitation');
   assert.equal(sourceTakeover.invitation.clip,'none',
     'the FULL invitation replaces the Doré source before moving');
   assert.match(sourceTakeover.invitation.color,/^(?:oklab\(|color\(|rgb\()/,
     'source card must resolve to an OS-driven real CSS color');
   assert(sourceTakeover.invitation.color!== 'rgb(25, 61, 46)',
     'old arbitrary teal green is forbidden');
   assert(sourceTakeover.invitation.relief.includes('04-olive-mount-etching-v8.svg'));
   assert(sourceTakeover.neutralCSS.reveal>.999,
     'at 10.18 the outgoing 03 full page must already be replaced, not torn into exposed scripture fragments');
   const card=sourceTakeover.invitation.box,print=sourceTakeover.firstFrame.box;
   assert(print.x>card.x+5&&print.y>card.y+5&&
     print.x+print.w<card.x+card.w-5 &&
     print.y+print.h<card.y+card.h-5,
     'speaker print must be visibly inset on every side of its invitation');
   const atUserScreenshot=await go(10.26,'01c-clean-mersi-invitation-transition');
   assert(atUserScreenshot.reading>.999&&atUserScreenshot.neutralCSS.reveal>.999,
    'at EXACT 10.26 the old 03 scripture page must be fully covered without exposed fragments');
   assert(atUserScreenshot.neutralCSS.halves.every(x=>!/[1-9][0-9.]*%/.test(x)),
    'all original page material is replaced by a full-panel source field at 10.26');
   assert.equal(atUserScreenshot.invitation.visibility,'visible',
    'the 04 printed card leads the spatial handoff');
   assert(atUserScreenshot.invitation.relief.includes('04-olive-mount-etching-v8.svg'),
    'the entering card carries the substantive original Olives landscape engraving');
   assert(Math.abs(atUserScreenshot.firstFrame.box.w/atUserScreenshot.firstFrame.box.h-.75)<.01,
    'the verified first-speaker 3:4 print must not be resized');
   const forming=await go(10.38,'02-first-to-left-second-to-right');
   assert.equal(forming.scene,'04-two-poster-formation');
   assert(forming.spread>.25&&forming.spread<.45,'first speaker must visibly travel toward left folio');
   assert(forming.firstFrame.box.x<bridge.firstFrame.box.x,
    'first speaker moves from right Doré frame to the left half');
   assert.equal(forming.groundCSS.visibility,'hidden','04 pigment waits until both originals settle');
   assert(forming.reading>.8,'old ONE typography must be covered during the physical transit');
   assert.equal(forming.incomingRight.visibility,'hidden','second portrait waits for first');
   assert.equal(forming.invitation.visibility,'visible',
     'the printed invitation and its original poster must travel together');
   assert(forming.invitation.box.x<bridge.invitation.box.x,
     'the invitation carrier must translate left as the original print travels');
   const pair=await go(10.98,'03-two-poster-locked-original-background');
   assert.equal(pair.scene,'04-pair-hold');
   assert.equal(pair.pairLeft.visibility,'visible');
   assert.equal(pair.invitation.visibility,'hidden',
     'first traveling card is replaced by TWO identical settled invitation objects');
   assert.equal(pair.pairCardLeft.visibility,'visible');
   assert.equal(pair.pairCardRight.visibility,'visible');
   assert.equal(pair.pairCardLeft.caption,'WATCHMAN NEE · 倪柝聲');
   assert.equal(pair.pairCardRight.caption,'DEREK PRINCE · 葉光明');
   for(const [mount,poster] of [[pair.pairCardLeft,pair.pairLeft],
                                [pair.pairCardRight,pair.pairRight]]){
     assert(mount.box.y<poster.box.y&&
       mount.box.y+mount.box.h>poster.box.y+poster.box.h,
       'gallery cards must retain real margins beyond approved poster');
   }
   if(width>800){
     assert(pair.masthead.y+pair.masthead.h<
       Math.min(pair.pairCardLeft.box.y,pair.pairCardRight.box.y)+2,
       'single global masthead must remain outside mounted gallery works');
   }
   for(const [cardBox,printBox] of [[pair.pairCardLeft.box,pair.pairLeft.box],
                                    [pair.pairCardRight.box,pair.pairRight.box]]){
    assert(cardBox.x<=printBox.x&&cardBox.y<printBox.y&&
      cardBox.x+cardBox.w>=printBox.x+printBox.w &&
      cardBox.y+cardBox.h>printBox.y+printBox.h,
      'each original print mounts independently on a green/gold invitation');
   }
   assert.equal(pair.pairRight.visibility,'visible');
   assert.equal(pair.pairLeft.src,'/images/olive/watchman-nee-editorial.png');
   assert.equal(pair.pairRight.src,'/images/olive/derek-prince-editorial.png');
   const pairNames=await page.evaluate(()=>['#olive-pair-left','#olive-pair-right'].map(sel=>{
    const el=document.querySelector(sel+' olive-speaker-baseline');
    const frame=el?.shadowRoot?.querySelector('.speaker-card');
    return {name:el?.shadowRoot?.querySelector('.olive-speaker-english')?.textContent,
      slug:el?.dataset.speaker,size:frame?.style.getPropertyValue('--poster-size'),
      opsz:frame?.style.getPropertyValue('--poster-optical-size')};
   }));
   assert.deepEqual(pairNames,[
    {name:'WATCHMAN NEE',slug:'watchman-nee',size:'11cqw',opsz:'43.96'},
    {name:'DEREK PRINCE',slug:'derek-prince',size:'18.19cqw',opsz:'72.695'}
   ],'both poster originals MUST preserve unique English typographic masters');
   // Restore the original moderate print dimensions from 50370f07:
   // a settled speaker print is a 3:4 composite inside a dedicated
   // editorial frame, NOT an oversized half-viewport folio.
   assert(pair.pairLeft.box.y>=pair.masthead.y+pair.masthead.h-3,
    'poster must have separate vertical clearance for the chapter masthead');
   for(const frame of [pair.pairLeft,pair.pairRight]){
    assert(Math.abs(frame.box.w/frame.box.h-.75)<.008,
      'speaker print retains original registered 3:4 aspect');
    assert(frame.box.h<pair.main.h*.9,
      'speaker poster must not expand to fill the entire scene height');
   }
   assert(Math.abs(pair.pairLeft.box.w-pair.pairRight.box.w)<2,
     'two speaker posters have equal widths');
   if(width>800){
    assert.equal(pair.pairOrientation,'side-by-side');
    assert(pair.pairRight.box.x>=pair.pairLeft.box.x+pair.pairLeft.box.w+12,
      'poster pairing has a deliberate editorial gutter');
   }else{
    assert.equal(pair.pairOrientation,'stacked');
    assert(pair.pairLeft.box.w>pair.main.w*.44,
     'mobile posters remain readable');
    assert(pair.pairRight.box.y>=pair.pairLeft.box.y+pair.pairLeft.box.h+8,
      'mobile prints have a deliberate vertical gutter');
   }
   assert.match(js,/const firstTravel=ease\(form\/\.73\);/,
    'preserve the first-poster entrance travel from 50370f07');
   assert.equal(pair.groundCSS.visibility,'hidden','04 pigment follows, not accompanies, the double spread');
    assert(pair.neutralCSS.reveal>.999,'03 must be fully cleared behind both posters');
    assert(pair.neutralCSS.cloth.includes('cover-texture-antique-green.png'),
     'transition carrier MUST retain the true green Bible-cover cloth, not yellow');
   const material=await go(11.44,'04-only-now-olive-svg-background');
   assert.equal(material.scene,'04-ground-reveal');
   assert(material.ground>.45&&material.ground<.60,'engraved exterior changes on its own later beat');
   assert.equal(material.groundCSS.parts,2,'two halves are registered to one field');
    assert.equal(material.groundCSS.opacity,'1','no fade');
    assert.equal(material.method,'opposed-top-down-bottom-up');
    assert(material.groundCSS.right>.90&&material.groundCSS.left<.02,
      'at 50% only RIGHT may be new Olive invitation; LEFT retains the Bible cover');
    assert(/^inset\(0(?:px)? 0(?:px)? [0-9.]+%/.test(material.groundCSS.halves[0]),'left from TOP');
    assert(/^inset\([0-9.]+%/.test(material.groundCSS.halves[1]),'right from BOTTOM: '+material.groundCSS.halves[1]);
   assert.equal(material.pairLeft.src,pair.pairLeft.src);
   assert.equal(material.pairRight.src,pair.pairRight.src);
   for(const key of ['x','y','w','h'])assert(Math.abs(material.pairLeft.box[key]-pair.pairLeft.box[key])<1,
    'speakers must be FIXED as background changes: '+key);
   const backgroundReady=await go(11.75,'05-olive-material-fixed');
   assert(backgroundReady.ground>.999 &&
       backgroundReady.groundCSS.visibility==='visible' &&
       backgroundReady.groundCSS.left>.999 && backgroundReady.groundCSS.right>.999,
       'both halves must finish the gilt invitation before the next speakers');
   assert.equal(backgroundReady.neutralCSS.visibility,'hidden',
       '03 Bible cloth must retire when 04 field is complete');
    assert(!backgroundReady.groundCSS.texture.includes('/one/'),
       '04 realm must not load 03 book-cover texture');
    const pairTransition=await go(12.25,'06-opposed-double-poster-change');
   assert.equal(pairTransition.scene,'04-six-pair-gallery');
   assert(+pairTransition.pairBlend>.4&&+pairTransition.pairBlend<.7,'new pair is physically half revealed');
   assert(pairTransition.incomingLeft.clip.includes('inset(')&&
     pairTransition.incomingRight.clip.includes('inset('),'both half-spreads have spatial opposing masks');
   if(width<=800){
    assert(/^inset\(0(?:px)? 0(?:px)? [0-9.]+%/.test(pairTransition.incomingLeft.clip),
     'phone upper poster switches from TOP DOWN');
    assert(/^inset\([0-9.]+%/.test(pairTransition.incomingRight.clip),
     'phone lower poster switches from BOTTOM UP');
   }
   assert(/^inset\(0(?:px)? 0(?:px)? [0-9.]+%/.test(pairTransition.incomingLeft.clip),
     'left artwork uses MERSI top-to-bottom mask on desktop and phone');
    assert(/^inset\([0-9.]+% 0(?:px)? 0(?:px)?/.test(pairTransition.incomingRight.clip),
     'right artwork uses bottom-to-top mask on desktop and phone');
    assert(pairTransition.incomingLeft.src.includes('david-pawson-editorial.png'));
   assert(pairTransition.incomingRight.src.includes('stephen-tong-editorial.png'));
   const incomingTypography=await page.evaluate(()=>
    ['#olive-pair-next-left','#olive-pair-next-right'].map(sel=>{
      const x=document.querySelector(sel+' olive-speaker-baseline');
      return {slug:x?.dataset.speaker,name:x?.shadowRoot?.querySelector('.olive-speaker-english')?.textContent};
    }));
   assert.deepEqual(incomingTypography,[
    {slug:'david-pawson',name:'DAVID PAWSON'},
    {slug:'stephen-tong',name:'STEPHEN TONG'}
   ],'opposed masks must carry original English along with the art');
   for(const key of ['x','y','w','h'])assert(Math.abs(pairTransition.pairLeft.box[key]-pair.pairLeft.box[key])<1,
    'all six pairs keep exactly the same folio/anchor geometry');
   const last=await go(16.11,'07-final-pair-eleven-twelve');
   assert(last.pairLeft.src.includes('yu-hong-jie-editorial.png'));
   assert(last.pairRight.src.includes('kou-shao-en-editorial.png'));
   const indexHalf=await go(16.70,'08-twelve-works-recomposing');
   assert.equal(indexHalf.scene,'04-twelve-recomposition');
   assert.equal(indexHalf.overviewPaper,'rgba(0, 0, 0, 0)',
    'index must stay in the same olive-gold field; no white background');
   assert(indexHalf.index>.35&&indexHalf.index<.55,'twelve images must visibly recompose');
   assert.equal(indexHalf.cards.length,12,'must be original TWELVE works, not gallery thumb proxies');
   assert(indexHalf.cards[0].w<indexHalf.main.w*(width>800?.5:.82),
    'twelve cards must interpolate from their approved desktop HALF or mobile FULL-WIDTH stacked source to grid destinations');
   const indexFull=await go(17.55,'09-twelve-voices-final-overview');
   assert.equal(indexFull.scene,'04-twelve-index');
   assert.equal(indexFull.cards.length,12);
    assert.equal(indexFull.pairDisplay,'none',
      'no large source-pair artwork underneath the 12 prints');
    assert.equal(indexFull.firstDisplay,'none',
      'no entrance-frame source underneath final index');
    assert.equal(indexFull.indexIsolated,'true',
      'the final screen contains only the 12 gallery works');
   assert.equal(indexFull.grid,width>=800?'6':'3','6x2 desktop or 3x4 phone exhibition index');
   assert.equal(indexFull.ctaVisibility,'visible');
   const seen=new Set(indexFull.cards.map(x=>x.src));
   assert.equal(seen.size,12,'all original 12 unique approved speaker images must be present');
   const protectedTwelve=await page.evaluate(()=>
    [...document.querySelectorAll('#olive-overview .olive-stage__index-card')].map(card=>{
      const overlay=card.querySelector('.olive-stage__artwork>olive-speaker-baseline');
      const root=overlay?.shadowRoot;
      const frame=root?.querySelector('.speaker-card');
      return {image:card.querySelector('img')?.getAttribute('src'),
        slug:overlay?.dataset.speaker,
        name:root?.querySelector('.olive-speaker-english')?.textContent,
        size:frame?.style.getPropertyValue('--poster-size'),
        optical:frame?.style.getPropertyValue('--poster-optical-size'),
        cssLoaded:!!root?.querySelector('link[href*="baseline.css"]')?.sheet};
    }));
   assert.equal(protectedTwelve.length,12);
   for(const entry of protectedTwelve){
    assert.equal(entry.image,'/images/olive/'+entry.slug+'-editorial.png',
      'image and its approved English must share exact speaker identity');
    assert(entry.name&&entry.name.length>3&&entry.size.endsWith('cqw'),
      'every index work MUST retain protected English instead of a bare PNG');
    assert(entry.optical&&entry.cssLoaded,
      'frozen optical-size and original shadow CSS must load for all twelve');
   }
   for(const [i,c] of indexFull.cards.entries()){
     assert(Math.abs(c.w/c.h-.75)<.008,
      'all twelve original artwork composites must have exact 3:4 geometry');
    assert(c.src==='/images/olive/'+[
     'watchman-nee','derek-prince','david-pawson','stephen-tong',
     'huang-shuhua','kang-lai-chang','jerry-lai','tong-liu',
     'jiang-xiuqin','rick-warren','yu-hong-jie','kou-shao-en'][i]+'-editorial.png',
     'order must remain original approval order');
    assert(c.w>25&&c.h>25,'twelve original posters still visible, no zero-size index cards');
   }
   const backMid=await go(11.44,'10-reverse-return-to-ground-mid');
   assert(Math.abs(backMid.ground-material.ground)<.005,
    'reversing returns exact exterior mask position, no delayed animation');
   const backBeginning=await go(9.76,'11-reverse-restore-dore-frame');
   assert(Math.abs(backBeginning.first-bridge.first)<.005,
    'reverse restores exact first poster clip and Doré frame geometry');
   const restored=await go(9.30,'12-reverse-restored-emmaus');
   assert.equal(restored.firstFrame.visibility,'hidden');
   assert.equal(restored.groundCSS.visibility,'hidden');
    assert.equal(restored.neutralCSS.visibility,'hidden','return to original 03 without a bridge remnant');
   assert.equal(errors.length,0,'JavaScript browser errors: '+errors.join(' | '));
   console.log('P2 04 TWELVE VOICES PASS',width,
    JSON.stringify({stage:indexFull.scene,groundAfterHold:material.ground,
      finalColumns:indexFull.grid,photos:indexFull.cards.length,
      reversed:restored.scene}));
   await page.close();
  }
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
