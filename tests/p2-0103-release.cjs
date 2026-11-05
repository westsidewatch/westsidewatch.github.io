/* P2 RELEASE GATE — 01 Church → 02 Magazine → 03 Emmaus.
 * Publishing MUST NOT import 04 Olive Mountain or 05–07.
 * Real Chromium verifies the book choreography, not only regexes.
 */
const fs=require('node:fs');
const assert=require('node:assert/strict');
const {chromium}=require('playwright');
const html=fs.readFileSync('static/experiments/p2-0103-release.html','utf8');
const js=fs.readFileSync('static/js/p2-0103-release.js','utf8');
const css=fs.readFileSync('static/css/p2-0103-release.css','utf8');
const vol=fs.readFileSync('static/experiments/p2-double-square-video-lab.html','utf8');
const bridge=fs.readFileSync('static/js/p2-magazine-live-bridge.js','utf8');
const poster=fs.readFileSync('static/js/p2-vol00-poster.js','utf8');
const posterCss=fs.readFileSync('static/css/p2-vol00-poster.css','utf8');
assert(!/id="olive-proof"|p2-five-v15|olive-speaker-baseline|data-jump="1[01]\./.test(html),'04–07 are excluded from the release HTML');
assert(!/\bconst olive\b|\boliveIn\b|\boliveShowing\b|galleryBorrowed|archiveForOlive/.test(js),'04–07 animation is excluded from release runtime');
assert(!/\.olive-proof|data-realm="sermon"|data-realm="cinema"|data-realm="book"/.test(css),'release CSS excludes future realm content');
assert.match(js,/const timelineMax=9\.34/,'release ends before Olive starts at 9.44');
assert.match(js,/const move=smooth\(\(distance-6\.50\)\/\.60\)/,
 'Magazine original cover opens across 0.60vh instead of flashing over 0.30vh');
assert.match(js,/const firstAngle=-86\*move;/,
 'Magazine first hinge has the same 86-degree opening as the original Emmaus green cover');
assert.match(js,/const greenAngle=-86\*archive;/,
 'the existing Emmaus second hinge must remain untouched');
assert.match(html,/p2-0103-release\.css/);
assert.match(html,/p2-0103-release\.js/);
assert.match(vol,/coverIn=stableLargeA\?\(reduce\?\(progress>=\.14\?1:0\):ease\(\(progress-\.04\)\/\.10\)\)/,'cover field reveals while contents arrive in four stages');
assert.match(vol,/posterIn=stableLargeA\?ease\(\(progress-\.28\)\/\.07\)/,'whole large poster follows');
assert.match(poster,/const u=clamp\(\(p-\.36\)\/\.41\)\*6/,'seven inks only begin after folios are visible');
assert.match(bridge,/magazine\.style\.background='transparent'/,'no early blank paper curtain');
assert.match(bridge,/filmReveal=easing\(\(progress-\.86\)\/\.065\)/,'original home film must reveal during uniform spread shrink before Contents');
assert.match(poster,/--xw-field-opacity/,'full field follows the same scroll position');
assert.match(posterCss,/data-p2-poster="a"\]::before/,'backing paper must replace Church water and schedule');
assert.match(html,/p2-emmaus-theme-verse\.css/,'ONE green cover scripture has separate scoped OS rule');
assert(!/\.olive-proof/.test(css),'no Olive Mountain CSS');
const out='artifacts/p2-0103-release';fs.mkdirSync(out,{recursive:true});
const u='http://127.0.0.1:4173/experiments/p2-0103-release.html';
const browserPromise=chromium.launch({headless:true});
(async()=>{
 const browser=await browserPromise;
 try{
  for(const [width,height] of [[1648,928],[390,844]]){
   const page=await browser.newPage({viewport:{width,height},reducedMotion:'no-preference'});
   const errors=[];
   page.on('pageerror',error=>errors.push(String(error)));
   try{
    await page.goto(u+'?d=0.12',{waitUntil:'domcontentloaded',timeout:45000});
    await page.waitForFunction(()=>document.querySelector('#proof-original')?.contentDocument
      ?.querySelector('.p2-magazine iframe:not(.p2-magazine__home-film)')?.contentDocument
      ?.getElementById('dual-stage'),{timeout:25000});
    const pose=async d=>{
      await page.evaluate(distance=>{
       const track=document.querySelector('#proof-track');
       scrollTo({top:track.getBoundingClientRect().top+scrollY+distance*innerHeight,behavior:'instant'});
      },d);
      // The real 01/02 artwork lives in three nested frames. The old
      // arbitrary 190ms sleep could inspect PREVIOUS cover poses on busy
      // CI runners, yielding false wall/masthead order regressions.
      // Wait for the original Church scroll progress to catch up, then
      // allow the approved child poster a fresh animation frame.
      await page.waitForFunction(d=>{
       const root=document.getElementById('proof-original')?.contentDocument?.querySelector('.showcase');
       if(!root)return false;
       const churchEnd=3.0775,magazineEnd=6.5,dist=Math.min(d,magazineEnd);
       // The release compositor forwards NORMALIZED progress, and
       // living-water's existing embeddedScene() maps that to vh.
       const raw=dist<=churchEnd
        ?((dist<=1.8?.1+dist*(.4/1.8):.5+(dist-1.8))/2.9)
        :(()=>{
          const vh=2.37+(dist-churchEnd)/(magazineEnd-churchEnd)*(4-2.37);
          return vh<=2.9?.75*vh/2.9:.75+.25*(vh-2.9)/1.1;
         })();
       const expected=raw<=.75?raw/.75*2.9:2.9+(raw-.75)/.25*1.1;
       return Math.abs(Number(root.dataset.p2Progress||0)-expected)<.045;
      },d,{timeout:16000});
      await page.waitForTimeout(140);
      return page.evaluate(()=>{
       const root=document.getElementById('proof-original')?.contentDocument;
       const mag=root?.querySelector('.p2-magazine');
       const f=mag?.querySelector('iframe:not(.p2-magazine__home-film)');
       const doc=f?.contentDocument,stage=doc?.getElementById('dual-stage');
       const cover=doc?.getElementById('dual-cover'),poster=doc?.getElementById('dual-contents');
       const clip=mag?.querySelector('.p2-magazine__home-film');
       const inScene=document.getElementById('emmaus');
       const b=e=>e?.getBoundingClientRect();
       // A hidden parent iframe retains styled child DOM. Test the
       // COMPOSITED visibility, not the child's standalone CSS visibility.
       const magazineComposited=!!mag&&getComputedStyle(mag).visibility==='visible'&&
        getComputedStyle(mag).opacity!=='0';
       return {scene:document.body.dataset.proofScene,phase:stage?.dataset.phase,
        magazineComposited,
        coverVisible:magazineComposited&&!!cover&&getComputedStyle(cover).visibility==='visible',
        posterVisible:magazineComposited&&!!poster&&getComputedStyle(poster).visibility==='visible',
        coverX:b(cover)?.x,coverW:b(cover)?.width,coverH:b(cover)?.height,
        posterX:b(poster)?.x,posterW:b(poster)?.width,posterH:b(poster)?.height,
        coverIn:+stage?.dataset.releaseCoverIn||0,
        posterIn:+stage?.dataset.releasePosterIn||0,
        coverClip:cover?.style.clipPath||'',
        coverTransform:cover?.style.transform||'',
        wallRise:+stage?.dataset.coverWallRise||0,
        mastReveal:+stage?.dataset.coverMastReveal||0,
        verseReveal:+stage?.dataset.coverVerseReveal||0,
        featureReveal:+stage?.dataset.coverFeatureReveal||0,
        spreadScale:+stage?.dataset.posterSpreadScale||1,
        fieldOpacity:+stage?.dataset.posterField||0,
        posterPageBackground:doc?.defaultView?.getComputedStyle(doc.getElementById('xw-poster'))?.backgroundColor||'',
        filmOpacity:clip?+getComputedStyle(clip).opacity:-1,
        sheetContents:doc?.getElementById('dual-stone-contents')?.inert,
        oneVisible:!!inScene&&getComputedStyle(inScene).visibility==='visible',
        trackHeight:document.querySelector('#proof-track')?.getBoundingClientRect().height,
        olivePresent:!!document.getElementById('olive-proof'),
        banner:document.getElementById('proof-phase')?.textContent};
      });
    };
    const church=await pose(1.6);
    assert.equal(church.olivePresent,false);
    assert(!church.coverVisible&&!church.posterVisible,'nothing from Magazine may cover church in phase 01');
    // Original cover frame is stationary while its 4 physical content
    // layers play sequentially on the SAME scroll progress.
    const wallFirst=await pose(3.55);
    assert(wallFirst.wallRise>.95&&wallFirst.mastReveal<.001&&
      wallFirst.verseReveal<.001&&wallFirst.featureReveal<.001,
      'wall must rise FIRST with masthead/scripture/title absent');
    await page.screenshot({path:out+'/cover-wall-rises-first-'+width+'.png'});
    const mastSecond=await pose(3.72);
    assert(mastSecond.wallRise>.999&&mastSecond.mastReveal>.80&&
      mastSecond.verseReveal<.001&&mastSecond.featureReveal<.001,
      'official full-width masthead must appear SECOND');
    await page.screenshot({path:out+'/cover-masthead-second-'+width+'.png'});
    const verseThird=await pose(3.86);
    assert(verseThird.mastReveal>.999&&verseThird.verseReveal>.80&&
      verseThird.featureReveal<.20,'Isaiah verse THIRD, title after verse');
    await page.screenshot({path:out+'/cover-isaiah-verse-third-'+width+'.png'});
    // RECOVERY: 03 must not overwrite 02's APPROVED cover motion.
    // The native cover progresses monotonically from right to its full
    // position; an independent 03 JS cache must never snap it backward.
    const enteringCover=await pose(3.50);
    assert(enteringCover.coverIn>.05&&enteringCover.coverIn<.95,
      'approved magazine cover must enter smoothly, not flash full-width');
    assert(!enteringCover.posterVisible,'the giant left A waits for the full right cover');
    assert(enteringCover.fieldOpacity<.001,
      'the Magazine cannot paint a premature navy field over the Church schedule');
    await page.screenshot({path:out+'/cover-entering-church-unobscured-'+width+'.png'});
    const cover=await pose(3.92);
    console.log('RECOVERED ORIGINAL COVER',width,JSON.stringify(cover));
    assert(cover.coverIn>.999&&cover.posterIn===0,
      'recover PR #1381: the entire original right cover settles before giant A');
    assert.equal(enteringCover.coverTransform,'none',
      'never fly the complete finished cover across the Church schedule');
    assert(enteringCover.coverClip.startsWith('inset('),
      'use a fixed page mask and internal rising architecture');
    assert(Math.abs(enteringCover.coverX-cover.coverX)<1,
      'cover must remain the exact same stationary Church-schedule frame');
    assert(!cover.posterVisible,'no empty left folio while the right cover settles');
    assert.equal(cover.filmOpacity,0,'the original film remains hidden during cover arrival');
    assert(cover.fieldOpacity<.001,'do not recolor the Church during the MERSI cover reveal');
    if(width>820){
      const sameFrame=await page.evaluate(()=>{
        const church=document.getElementById('proof-original')?.contentDocument;
        const schedule=church?.querySelector('.church-editorial__copy');
        const magazine=church?.querySelector('.p2-magazine iframe:not(.p2-magazine__home-film)')?.contentDocument;
        const cover=magazine?.getElementById('dual-cover');
        const stage=magazine?.getElementById('dual-stage');
        const a=schedule?.getBoundingClientRect(),b=cover?.getBoundingClientRect();
        return {schedule:a?{x:a.x,y:a.y,w:a.width,h:a.height}:null,
          magazine:b?{x:b.x,y:b.y,w:b.width,h:b.height}:null,
          match:+stage?.dataset.coverScheduleMatch||0};
      });
      assert(sameFrame.schedule&&sameFrame.magazine,'the actual Church schedule and incoming original cover must exist');
      const a=sameFrame.schedule,b=sameFrame.magazine;
      assert(Math.abs(a.x-b.x)<2&&Math.abs(a.y-b.y)<2&&
             Math.abs(a.w-b.w)<2&&Math.abs(a.h-b.h)<2,
        'the incoming Magazine must match the Church schedule EXACTLY in x/y/width/height: '+
        JSON.stringify(sameFrame));
      assert(sameFrame.match>.999,'original schedule-sized page must hold for the complete cover entrance');
    }
    const completeCover=await pose(4.04);
    assert(completeCover.wallRise>.999&&completeCover.mastReveal>.999&&
      completeCover.verseReveal>.999&&completeCover.featureReveal>.999,
      'city→masthead→scripture→bilingual title must all be complete before giant 西望');
    await page.screenshot({path:out+'/cover-four-layers-complete-'+width+'.png'});
    await page.screenshot({path:out+'/cover-same-frame-as-church-schedule-'+width+'.png'});
    const print=await pose(4.65);
    console.log('RELEASE GIANT PRINT',width,JSON.stringify(print));
    assert(print.posterVisible&&print.coverVisible,'full pair must be present for seven-color print');
    assert(Math.abs(print.posterW-print.posterH)<3,'giant 西望 stays 1:1');
    assert.equal(print.filmOpacity,0,'no film while ink colors still run');
    assert(print.fieldOpacity>.99,'Church water must not show around large 西望');
    assert.equal(print.posterPageBackground,'rgba(0, 0, 0, 0)',
      'large 西望 may not arrive inside an opaque beige square');
    const gold=await pose(5.99);
    console.log('RELEASE BLUE-GOLD',width,JSON.stringify(gold));
    assert(gold.coverVisible&&gold.posterVisible,'gold print has intact complete folios');
    assert(Math.abs(gold.spreadScale-1)<.002,'do not shrink before the Contents entry');
    await page.screenshot({path:out+'/blue-gold-fixed-'+width+'.png'});
    // The editor's crucial order: scaled blue/gold spread + original film
    // are visible BEFORE the original Contents is allowed to enter.
    const shrunk=await pose(6.22); // p≈.918, original folios scaled, no Contents
    console.log('RELEASE FILM-BEFORE-CONTENTS',width,JSON.stringify(shrunk));
    assert(shrunk.spreadScale<.87,'both original folios must scale uniformly after blue/gold hold');
    assert(shrunk.filmOpacity>.95,'original home film must reveal BEFORE Contents enters');
    assert(shrunk.sheetContents,'Contents must remain hidden while the blue/gold spread shrinks over film');
    assert(shrunk.fieldOpacity<.05,'full-stage paper must clear during shrink to show original film');
    await page.screenshot({path:out+'/blue-gold-shrunken-over-original-film-'+width+'.png'});
    const entering=await pose(6.34); // p≈.953, Contents enters AFTER film reveal
    assert(entering.spreadScale<.86&&entering.filmOpacity>.99,
      'Contents must enter into already-reduced folios over the already-visible film');
    const indexSeam=await page.evaluate(()=>{
      const origin=document.querySelector('#proof-original')?.contentDocument;
      const doc=origin?.querySelector('.p2-magazine iframe:not(.p2-magazine__home-film)')?.contentDocument;
      const poster=doc?.getElementById('xw-poster');
      const index=doc?.getElementById('dual-stone-contents');
      return {old:poster?.style.clipPath||'',incoming:index?.style.clipPath||'',
        alpha:index?+doc.defaultView.getComputedStyle(index).opacity:0};
    });
    assert(indexSeam.old.startsWith('inset(')&&indexSeam.incoming.startsWith('inset('),
      'giant A and original Contents must use opposing MERSI masks, not overlap as transparencies');
    assert.equal(indexSeam.alpha,1,'the incoming native Contents paper must be opaque, not a ghosted crossfade');
    await page.screenshot({path:out+'/contents-entering-after-film-'+width+'.png'});
    const contents=await pose(6.47); // p≈.991: native Contents is settled
    console.log('RELEASE CONTENTS',width,JSON.stringify(contents));
    assert(contents.spreadScale<.86,'Contents must arrive into the already-shrunken spread');
    assert(contents.filmOpacity>.99,'original film remains visible beneath completed Contents');
    assert(!contents.sheetContents,'native Contents reader must be active once settled');
    await page.screenshot({path:out+'/contents-settled-'+width+'.png'});
    const retreat=await pose(6.48);
    assert(retreat.spreadScale<.86,'both original folios retain the uniform final scale');
    assert(retreat.filmOpacity>.99,'original home film remains visible behind Contents');
    assert(retreat.fieldOpacity<.05,'the stage paper must not obscure the revealed film');
    const settled=await pose(6.50);
    assert(settled.fieldOpacity<.001&&settled.filmOpacity>.999,
      'the whole paper field must fully clear when the original film is revealed');
    await page.screenshot({path:out+'/film-after-spread-retreat-'+width+'.png'});
    // The ORIGINAL magazine cover must be visible across multiple scroll
    // positions, never rotate beyond the 86-degree Emmaus hinge or expose
    // the mirrored printed verso as in the reported production screenshot.
    const originalHinge=()=>page.evaluate(()=>{
      const origin=document.querySelector('#proof-original')?.contentDocument;
      const doc=origin?.querySelector('.p2-magazine iframe:not(.p2-magazine__home-film)')?.contentDocument;
      const cover=doc?.getElementById('dual-cover');
      return {transform:cover?.style.transform||'',
        backface:cover?.style.backfaceVisibility||'',
        visibility:cover?.style.visibility||'',
        mode:cover?.dataset.turnMode||''};
    });
    const hingeAngle=pose=>Number(pose.transform.match(/rotateY\((-?[\d.]+)deg\)/)?.[1]);
    await pose(6.67);
    const early=await originalHinge();
    assert(hingeAngle(early)<-8&&hingeAngle(early)>-28,
      'at 6.67vh the Magazine cover must JUST be beginning to open');
    assert.equal(early.backface,'hidden','the reverse print must never appear mirrored');
    await page.screenshot({path:out+'/magazine-first-turn-early-'+width+'.png'});
    const emmausTurn=await pose(6.82);
    const middle=await originalHinge();
    assert(hingeAngle(middle)<-35&&hingeAngle(middle)>-60,
      'at 6.82vh the full Magazine cover should remain halfway through its opening');
    assert.equal(middle.visibility,'visible','no flash-disappearing cover at mid turn');
    await page.screenshot({path:out+'/magazine-first-turn-middle-'+width+'.png'});
    await pose(7.04);
    const late=await originalHinge();
    assert(hingeAngle(late)<-75&&hingeAngle(late)>=-86.01,
      'the first hinge must stop at 86 degrees, not swing 172 degrees over Contents');
    await page.screenshot({path:out+'/magazine-first-turn-late-'+width+'.png'});
    await pose(7.17);
    const greenPause=await page.evaluate(()=>document.querySelector('#emmaus')?.dataset.coverState);
    assert.equal(greenPause,'green','the full green cover must HOLD before the second book turn');
    await page.screenshot({path:out+'/magazine-first-turn-green-hold-'+width+'.png'});
    await pose(6.82);
    const reverse=await originalHinge();
    assert(Math.abs(hingeAngle(reverse)-hingeAngle(middle))<2,
      'reversing scroll must restore exactly the same mid-turn pose');
    await page.screenshot({path:out+'/magazine-first-turn-reverse-'+width+'.png'});
    const backstage=await page.evaluate(()=>{
      const origin=document.querySelector('#proof-original')?.contentDocument;
      const magazine=origin?.querySelector('.p2-magazine iframe:not(.p2-magazine__home-film)')?.contentDocument;
      const stage=magazine?.querySelector('#dual-stage');
      const field=document.getElementById('p2-realm-background');
      return {emmausBackdrop:Number(stage?.dataset.emmausBackdrop||0),
        exteriorOpacity:Number(field?.style.opacity||0),
        exteriorMode:document.body.dataset.p2Surround};
    });
    assert(backstage.emmausBackdrop>.999,
      '73%: old film must be covered by the native Emmaus background, not show as a collage');
    assert(backstage.exteriorOpacity>.999,
      '73%: the ONE green book-cover backing must take over from the video outside the original book spread');
    assert.equal(backstage.exteriorMode,'cloth',
      '73%: use the canonical green cover cloth, not the retired pale engraving');
    const turns=await page.evaluate(()=>{
      const origin=document.querySelector('#proof-original')?.contentDocument;
      const source=origin?.querySelector('.p2-magazine iframe:not(.p2-magazine__home-film)')?.contentDocument;
      const cover=source?.getElementById('dual-cover');
      return {mode:cover?.dataset.turnMode,transform:cover?.style.transform||''};
    });
    assert.equal(turns.mode,'matched-emmaus-slow-book-flip',
      'first magazine hinge must use the slower, bounded Emmaus-style opening');
    assert(/perspective\(2800px\) rotateY\(/.test(turns.transform),
      'first page must hinge as the original complete 5:8 cover, not be replaced by a clipped strip');
    const greenHold=await pose(7.30); // green 5:8 cover must be complete
    const greenState=await page.evaluate(()=>document.getElementById('emmaus')?.dataset.coverState);
    assert.equal(greenState,'green','the green cover has to HOLD before the second turn');
    await page.screenshot({path:out+'/green-cover-hold-'+width+'.png'});
    await pose(7.68); // green-underleaf -> Doré, controlled page turnover
    await page.screenshot({path:out+'/emmaus-second-turn-82percent-'+width+'.png'});
    const secondTurn=await page.evaluate(()=>{
      const origin=document.querySelector('#proof-original')?.contentDocument;
      const source=origin?.querySelector('.p2-magazine iframe:not(.p2-magazine__home-film)')?.contentDocument;
      const underleaf=source?.getElementById('p2-emmaus-magazine-underleaf');
      const overlay=document.getElementById('em-entry-cover');
      return {leaf:underleaf?.style.transform||'',leafClip:underleaf?.style.clipPath||'',
        secondHinge:overlay?.style.transform||'',
        secondVisible:overlay?getComputedStyle(overlay).visibility!=='hidden':false};
    });
    assert(secondTurn.leaf==='none'&&secondTurn.leafClip==='none',
      'the original green underleaf must remain a full 5:8 book cover during the handoff');
    assert(secondTurn.secondVisible&&/perspective\(6400px\) rotateY\(/.test(secondTurn.secondHinge),
      'second full green cover must use the recovered PR #1381 physical flip over the Doré page');
    await pose(8.06); // complete engraving, before the ONE reading arrives
    const illustrationState=await page.evaluate(()=>document.getElementById('emmaus')?.dataset.coverState);
    assert.equal(illustrationState,'illustration',
      'the entire Doré illustration must HOLD before ONE reading comes forward');
    await page.screenshot({path:out+'/dore-illustration-hold-'+width+'.png'});
    await pose(8.475); // mid ONE entrance, MERSI coordinated mask
    const oneWipe=await page.evaluate(()=>{
      const origin=document.querySelector('#proof-original')?.contentDocument;
      const magazine=origin?.querySelector('.p2-magazine iframe:not(.p2-magazine__home-film)')?.contentDocument;
      const oldPage=magazine?.getElementById('dual-contents');
      const newPage=document.querySelector('#emmaus > .emmaus__left');
      const state=document.querySelector('#emmaus')?.dataset.coverState;
      return {oldClip:oldPage?.style.clipPath||'',
       incomingClip:newPage?.style.clipPath||'',state};
    });
    assert.equal(oneWipe.state,'illustration','Dore stays visible as ONE text enters');
    assert(oneWipe.oldClip.startsWith('inset(')&&oneWipe.incomingClip.startsWith('inset('),
      'MERSI-style original Contents and ONE text must be controlled by synchronized clip masks');
    assert(!oneWipe.oldClip.includes('inset(0 '),
      'old Contents must retract from the TOP rather than slide away sideways');
    assert(!oneWipe.incomingClip.includes('inset(0 0 0 '),
      'incoming ONE text must be revealed vertically, not by a horizontal fake book wipe');
    await page.screenshot({path:out+'/mersi-scripture-mid-reveal-'+width+'.png'});
    const greenBackground=await page.evaluate(()=>{
      const field=document.getElementById('p2-realm-background');
      const emmaus=document.getElementById('emmaus');
      return {surround:document.body.dataset.p2Surround,
        ground:document.body.dataset.fixedGround,
        fieldOpacity:Number(getComputedStyle(field).opacity),
        fieldImage:getComputedStyle(field).backgroundImage,
        emmausBackground:getComputedStyle(emmaus).backgroundColor};
    });
    assert.equal(greenBackground.surround,'cloth',
      'final 03 background must use the canonical antique-green cover cloth, not pale paper');
    assert.equal(greenBackground.ground,'on',
      'the 03 exterior background must be enabled by default');
    assert(greenBackground.fieldOpacity>.999&&
      greenBackground.fieldImage.includes('cover-texture-antique-green.png'),
      'final 03 field must visibly use the actual ONE green-cover texture: '+
      JSON.stringify(greenBackground));
    assert.equal(greenBackground.emmausBackground,'rgba(0, 0, 0, 0)',
      'Emmaus full-screen pale paper must NOT cover the dark green cloth exterior');
    await page.screenshot({path:out+'/emmaus-final-green-cover-texture-'+width+'.png'});
    const reading=await pose(9.30);
    assert.equal(reading.scene,'03','terminal release page must remain 03 Emmaus');
    assert(reading.oneVisible,'real ONE Bible reader remains visible at release end');
    assert(!reading.olivePresent,'Olive Mountain must never mount');
    assert.equal(await page.evaluate(()=>window.ONE_DATA?.books?.length),66,'all 66 canonical ONE books are available');
    const over=await pose(9.90);
    assert.equal(over.scene,'03','scrolling past 03 must clamp at the release ceiling');
    assert(!over.olivePresent);
    await page.screenshot({path:out+'/end-03-'+width+'.png'});
    await pose(4.65);
    await page.screenshot({path:out+'/giant-seven-color-'+width+'.png'});
    await pose(3.92);
    await page.screenshot({path:out+'/cover-first-'+width+'.png'});
    // Parent frame should never insert a blank opaque paper over the church.
    const rewind=await pose(1.6);
    assert(!rewind.coverVisible&&!rewind.posterVisible,'reverse scroll must restore Church only');
    assert(rewind.fieldOpacity<.001,'reverse scroll must clear entire magazine field');
    assert(!errors.some(x=>/ReferenceError|TypeError|SyntaxError/.test(x)),
      'JavaScript errors during release choreography: '+errors.join('; '));
    console.log('P2 RELEASE VERIFIED',width,{church,cover,print,gold,contents,reading,over,rewind});
   }finally{await page.close()}
  }
  console.log('01–03-only P2 release gate PASS. 04–07 excluded.');
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
