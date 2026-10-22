#!/usr/bin/env node
/* Westside §6A / New Westside Editorial Web: rendered visual evidence.
   This is NOT a substitute for the award-level human art-direction review. */
'use strict';
const fs=require('node:fs');
const path=require('node:path');
const {chromium}=require('playwright');
const base='http://127.0.0.1:4173';
const out='artifacts/p2-magazine-visual';
const viewports=[['desktop',1648,928],['tablet',768,1024],['phone',390,844],['zoom-proxy',824,928]];
const shapes=['square','wide','full'];
fs.mkdirSync(out,{recursive:true});
function intersect(a,b){return a&&b?Math.max(0,Math.min(a.right,b.right)-Math.max(a.left,b.left))*Math.max(0,Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top)):0}
(async()=>{
  const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
  const results=[];const failures=[];
  try{
    for(const [name,width,height] of viewports)for(const shape of shapes){
      const page=await browser.newPage({viewport:{width,height},reducedMotion:'reduce'});
      const errs=[];page.on('pageerror',e=>errs.push(e.message));
      const id=name+'-'+shape;
      try{
        const response=await page.goto(base+'/experiments/p2-magazine-art-direction-studio.html?view=geometry&shape='+shape,{waitUntil:'load',timeout:45000});
        await page.locator('#stage.geo').waitFor({state:'visible'});
        await page.evaluate(()=>document.fonts.ready);
        const m=await page.evaluate(()=>{
          const box=s=>{const r=document.querySelector(s)?.getBoundingClientRect();return r?{left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width,height:r.height}:null};
          const photo=document.querySelector('.geo__media img'),logo=document.querySelector('.geo__mast img'),li=document.querySelector('.geo__toc li');
          const font=s=>getComputedStyle(document.querySelector(s)).fontFamily;
          return {
            width:innerWidth,scrollWidth:document.documentElement.scrollWidth,
            photoCount:document.querySelectorAll('.geo__media img').length,
            photoDecoded:!!photo?.complete&&photo.naturalWidth>0,
            logoDecoded:!!logo?.complete&&logo.naturalWidth>0,
            image:box('.geo__media'),hero:box('.geo__hero'),title:box('.geo__display'),
            contents:document.querySelectorAll('.geo__toc .issue-list li').length,
            movements:document.querySelectorAll('.geo__toc .movement-head').length,
            tocFontSize:li?parseFloat(getComputedStyle(li).fontSize):0,
            source:!!document.querySelector('.geo__source')?.textContent.includes('非考古實拍'),
            realCopy:!!document.querySelector('.geo__excerpt p')?.textContent.includes('人在曠野走了很久'),
            squareLink:!!document.querySelector('.geo__square-seal[href="#geo-contents"]'),
            englishFont:font('.geo__huge'),chineseFont:font('.geo__display h2')
          };
        });
        const defects=[];
        if(response.status()!==200)defects.push('HTTP_'+response.status());
        if(errs.length)defects.push('JS: '+errs.join(';'));
        if(m.scrollWidth>m.width+2)defects.push('HORIZONTAL_OVERFLOW');
        if(m.photoCount!==1||!m.photoDecoded||!m.logoDecoded)defects.push('ASSET_DECODE');
        if(m.contents!==12||m.movements!==4)defects.push('CANONICAL_CONTENTS');
        if(m.tocFontSize<14)defects.push('TOC_UNDER_14PX');
        if(!m.source||!m.realCopy)defects.push('PROVENANCE_OR_MANUSCRIPT');
        if(shape!=='full'&&intersect(m.image,m.title)>200)defects.push('IMAGE_TYPE_COLLISION');
        if(shape==='square'&&Math.abs(m.image.width/m.image.height-1)>.08)defects.push('SQUARE_RATIO');
        if(shape==='wide'&&Math.abs(m.image.width/m.image.height-1.95)>.1)defects.push('WIDE_RATIO');
        if(shape==='full'&&width>760&&((m.image.width/m.hero.width)<.98||(m.image.height/m.hero.height)<.98))defects.push('FULL_BLEED_NOT_FULL_WIDTH_HEIGHT');
        if(shape!=='square'&&!m.squareLink)defects.push('FOLIO_LINK');
        const screenshot=id+'.png';
        await page.screenshot({path:path.join(out,screenshot),fullPage:true,animations:'disabled'});
        results.push({id,shape,viewport:{width,height},metrics:m,screenshot,defects});
        if(defects.length)failures.push({id,defects});
        console.log(id+' '+(defects.length?'FAIL: '+defects.join(', '):'BROWSER-CONTRACT PASS'));
      }catch(e){console.error(id+' ERROR '+e.message);failures.push({id,defects:[e.message]})}
      finally{await page.close()}
    }

    // Real clean publication renders (not the studio-toolbar comparison).
    // This tests that the image-embedded square is an accessible link to real Contents.
    for(const [id,width,height] of [['publication-desktop-square',1648,928],['publication-phone-square',390,844]]){
      const page=await browser.newPage({viewport:{width,height},reducedMotion:'reduce'});
      const defects=[];
      try{
        const response=await page.goto(base+'/experiments/p2-magazine-art-direction-studio.html?view=geometry&shape=square&presentation=1',{waitUntil:'load',timeout:45000});
        await page.evaluate(()=>document.fonts.ready);
        const visible=await page.evaluate(()=>{
          const mast=document.querySelector('.geo__mast');
          const photo=document.querySelector('.geo__media img');
          const lab=document.querySelector('.toolbar');
          return {mast:!!mast&&getComputedStyle(mast).display!=='none',
            photo:!!photo&&photo.complete&&photo.naturalWidth>0,
            controlsHidden:!!lab&&getComputedStyle(lab).display==='none',
            toc:document.querySelectorAll('.geo__toc .issue-list li').length,
            width:document.documentElement.scrollWidth,windowWidth:innerWidth};
        });
        if(!response||response.status()!==200)defects.push('HTTP');
        if(!visible.mast||!visible.photo||!visible.controlsHidden)defects.push('CLEAN_PUBLICATION_STATE');
        if(visible.toc!==12||visible.width>visible.windowWidth+2)defects.push('CONTENTS_OR_OVERFLOW');
        const link=page.locator('.geo__square-seal');
        await link.focus();
        if(!(await link.evaluate(el=>el===document.activeElement)))defects.push('SQUARE_LINK_NOT_FOCUSABLE');
        const filename=id+'.png';
        await page.screenshot({path:path.join(out,filename),fullPage:true,animations:'disabled'});
        await link.click();
        if(!(await page.evaluate(()=>location.hash==='#geo-contents')))defects.push('SQUARE_LINK_NOT_NAVIGABLE');
        results.push({id,shape:'square',presentation:1,viewport:{width,height},screenshot:filename,metrics:visible,defects});
        if(defects.length)failures.push({id,defects});
        console.log(id+' '+(defects.length?'FAIL: '+defects.join(', '):'PUBLICATION-UX PASS'));
      }catch(e){failures.push({id,defects:[e.message]});console.error(id+' ERROR '+e.message)}
      finally{await page.close()}
    }

    // THRESHOLD is a distinct authored concept, not a shape override. Separate art-direction evidence.
    for(const [id,width,height] of [['threshold-desktop',1648,928],['threshold-phone',390,844]]){
      const page=await browser.newPage({viewport:{width,height},reducedMotion:'reduce'});
      const defects=[];
      try{
        const response=await page.goto(base+'/experiments/p2-magazine-art-direction-studio.html?view=issue&presentation=1',{waitUntil:'load',timeout:45000});
        await page.locator('#stage.th').waitFor({state:'visible'});
        await page.evaluate(()=>document.fonts.ready);
        const facts=await page.evaluate(()=>{
          const img=document.querySelector('.th__photo img');
          const r=document.querySelector('.th__photo')?.getBoundingClientRect();
          return {photoDecoded:!!img&&img.complete&&img.naturalWidth>0,
            originalLogo:!!document.querySelector('.th__mast .os-logo'),
            source:!!document.querySelector('.th__imgcredit')?.textContent.includes('非史實攝影'),
            contents:document.querySelectorAll('.th__contents .issue-list li').length,
            width:innerWidth,scrollWidth:document.documentElement.scrollWidth,
            ratio:r?r.width/r.height:0,
            clean:document.body.classList.contains('presentation-mode')&&getComputedStyle(document.querySelector('.toolbar')).display==='none'};
        });
        if(!response||response.status()!==200)defects.push('HTTP');
        if(!facts.photoDecoded||!facts.originalLogo||!facts.source)defects.push('IMAGE_OR_PROVENANCE');
        if(facts.contents!==12||facts.scrollWidth>facts.width+2)defects.push('CONTENTS_OR_OVERFLOW');
        if(Math.abs(facts.ratio-1)>.08)defects.push('SQUARE_SUBJECT_RATIO');
        if(!facts.clean)defects.push('PUBLICATION_NOT_CLEAN');
        const screenshot=id+'.png';
        await page.screenshot({path:path.join(out,screenshot),fullPage:true,animations:'disabled'});
        const link=page.locator('.th__folio');
        await link.focus();
        if(!(await link.evaluate(el=>el===document.activeElement)))defects.push('FOLIO_KEYBOARD');
        await link.click();
        if(!(await page.evaluate(()=>location.hash==='#th-contents')))defects.push('FOLIO_CONTENTS');
        results.push({id,shape:'independent-threshold',viewport:{width,height},metrics:facts,screenshot,defects});
        if(defects.length)failures.push({id,defects});
        console.log(id+' '+(defects.length?'FAIL: '+defects.join(', '):'CONCEPT-UX PASS'));
      }catch(e){failures.push({id,defects:[e.message]});console.error(id+' ERROR '+e.message)}
      finally{await page.close()}
    }

    // R9 authored issue: one continuous publication, not image crop ratio permutations.
    for(const [id,width,height] of [['identity-desktop',1648,928],['identity-tablet',768,1024],['identity-phone',390,844],['identity-small',320,720]]){
      const page=await browser.newPage({viewport:{width,height},reducedMotion:'reduce'});
      const defects=[];const jsErrors=[];page.on('pageerror',e=>jsErrors.push(e.message));
      try{
        const response=await page.goto(base+'/experiments/p2-magazine-art-direction-studio.html?view=identity&presentation=1',{waitUntil:'load',timeout:45000});
        await page.locator('#stage.id').waitFor({state:'visible'});
        await page.evaluate(()=>document.fonts.ready);
        const facts=await page.evaluate(()=>{
          const sel=s=>document.querySelector(s);
          const art=sel('.id__cover-art img'),logo=sel('.id__meta .os-logo'),toc=sel('.id__index');
          const tocLinks=[...document.querySelectorAll('.id__index-group ol a')];
          return {
            width:innerWidth,scrollWidth:document.documentElement.scrollWidth,
            decoded:!!art?.complete&&art.naturalWidth>0&&!!logo?.complete&&logo.naturalWidth>0,
            title:sel('.id__cover-title h1')?.textContent.trim(),
            tocCount:tocLinks.length,movements:document.querySelectorAll('.id__index-group').length,
            interludes:document.querySelectorAll('.id__interlude').length,
            chapters:['#id-gate','#id-carmel','#id-elim','#id-esther','#id-maranatha'].every(s=>!!sel(s)),
            allTargets:tocLinks.every(a=>!!sel(a.getAttribute('href'))),
            sourceGate:sel('#id-gate .id__body')?.textContent.includes('考古學家在古代近東'),
            sourceEsther:sel('#id-esther .id__body')?.textContent.includes('Nicholas Herman'),
            honestIncomplete:sel('#id-maranatha')?.textContent.includes('尚待編輯核定'),
            officialMastheads:document.querySelectorAll('.id .os-logo').length,
            noLinksToNonexistent:!tocLinks.some(a=>!sel(a.getAttribute('href'))),
            presentation:document.body.classList.contains('presentation-mode'),
            deepTextSize:parseFloat(getComputedStyle(sel('#id-gate .id__body p')).fontSize),
            chineseWeight:getComputedStyle(sel('.id__cover-title h1')).fontWeight,
            loadedBodoni:getComputedStyle(sel('.id__cover-word')).fontFamily,
            monumentalIntroFont:parseFloat(getComputedStyle(sel('.id__intro-statement')).fontSize),
            monumentalIntroFamily:getComputedStyle(sel('.id__intro-statement')).fontFamily,
            orphanPunctuation:[...document.querySelectorAll('.id__act-name')].filter(el=>{
              const txt=el.firstChild;
              if(!txt||txt.nodeType!==Node.TEXT_NODE||txt.length<2)return false;
              const before=document.createRange(),dot=document.createRange();
              before.setStart(txt,txt.length-2);before.setEnd(txt,txt.length-1);
              dot.setStart(txt,txt.length-1);dot.setEnd(txt,txt.length);
              return dot.getBoundingClientRect().top-before.getBoundingClientRect().top>2;
            }).map(el=>el.textContent.trim())
          };
        });
        if(!response||response.status()!==200)defects.push('HTTP');
        if(jsErrors.length)defects.push('JAVASCRIPT: '+jsErrors.join(';'));
        if(facts.scrollWidth>facts.width+2)defects.push('HORIZONTAL_OVERFLOW');
        if(!facts.decoded)defects.push('ORIGINAL_BRAND_OR_IMAGE');
        if(facts.tocCount!==12||facts.movements!==4||facts.interludes!==3)defects.push('CANON_12_4_3');
        if(!facts.chapters||!facts.allTargets)defects.push('DEAD_TOC_DESTINATION');
        if(!facts.sourceGate||!facts.sourceEsther||!facts.honestIncomplete)defects.push('SOURCE_INTEGRITY');
        if(facts.deepTextSize<16)defects.push('BODY_TOO_SMALL');
        if(facts.monumentalIntroFont<38||!facts.monumentalIntroFamily.includes('Bodoni'))defects.push('INTRO_MONUMENT_FONT_REGRESSED');
        if(facts.orphanPunctuation.length)defects.push('ORPHAN_DISPLAY_PUNCTUATION: '+facts.orphanPunctuation.join(','));
        if(facts.chineseWeight!=='900')defects.push('PRIMARY_CHINESE_WEIGHT');
        if(!facts.presentation)defects.push('NOT_CLEAN_PUBLICATION');
        const screenshot=id+'.png';
        await page.screenshot({path:path.join(out,screenshot),fullPage:true,animations:'disabled'});
        const toc=page.locator('.id__enter[href="#id-contents"]').first();await toc.focus();
        if(!(await toc.evaluate(el=>document.activeElement===el)))defects.push('KEYBOARD_FOCUS');
        await toc.click();
        if(!(await page.evaluate(()=>location.hash==='#id-contents')))defects.push('COVER_TO_CONTENTS');
        const story=page.locator('.id__index-group a[href="#id-esther"]').first();await story.click();
        if(!(await page.evaluate(()=>location.hash==='#id-esther')))defects.push('CONTENTS_TO_STORY');
        results.push({id,viewport:{width,height},screenshot,metrics:facts,defects,artDirection:'SUBJECTIVE_REVIEW_PENDING',realZoom200:'NOT_VERIFIED'});
        if(defects.length)failures.push({id,defects});
        console.log(id+' '+(defects.length?'FAIL: '+defects.join(', '):'FULL-ISSUE BROWSER CONTRACT PASS'));
      }catch(e){failures.push({id,defects:[e.message]});console.error(id+' ERROR '+e.message)}
      finally{await page.close()}
    }


    // R10 SECTION-SPECIFIC EDITORIAL EVIDENCE: screenshot what the reader
    // actually reads, not only 12k-pixel full-page thumbnails.
    for(const [screen,width,height] of [['desktop',1648,928],['tablet',768,1024],['phone',390,844],['small',320,720]]) {
      const page=await browser.newPage({viewport:{width,height},reducedMotion:'reduce'});
      const id='identity-editorial-'+screen;
      const defects=[], sections=[];
      try {
        await page.goto(base+'/experiments/p2-magazine-art-direction-studio.html?view=identity&presentation=1',{waitUntil:'load',timeout:45000});
        await page.evaluate(()=>document.fonts.ready);
        for(const [name,selector] of [
          ['cover','#id-cover'],['contents','#id-contents'],
          ['city-essay','#id-gate'],['city-feature','#id-carmel'],
          ['technical-history','#id-elim'],['human-witness','#id-esther'],
          ['closing','#id-maranatha']]) {
          const loc=page.locator(selector);
          if(await loc.count()!==1){defects.push('MISSING_SECTION_'+name);continue;}
          await loc.scrollIntoViewIfNeeded();
          const box=await loc.boundingBox();
          if(!box||box.width<width*.35||box.height<1)defects.push('INVALID_SECTION_BOX_'+name);
          const filename=id+'-'+name+'.png';
          await page.screenshot({path:path.join(out,filename),fullPage:false,animations:'disabled'});
          // The centered viewport crop is contextual, not a complete section proof.
          // Capture the complete semantic section separately so mobile headers and
          // closing paragraphs are not silently omitted from art-direction review.
          const fullSectionFilename=id+'-'+name+'-section.png';
          await loc.screenshot({path:path.join(out,fullSectionFilename),animations:'disabled',timeout:45000});
          sections.push({name,selector,screenshot:filename,fullSectionScreenshot:fullSectionFilename,bounds:box});
        }
        const metrics=await page.evaluate(()=>{
          const root=document.documentElement;
          const anchors=[...document.querySelectorAll('.id__index-group ol a')];
          const buttons=[...document.querySelectorAll('#stage a')];
          // Detect two-glyph cover teaser widows in the actual rendered lines.
          const teaser=document.querySelector('.id__cover-title p')?.firstChild;
          let coverTeaserLastLineGlyphs=null;
          if(teaser?.nodeType===Node.TEXT_NODE){
            const lines=new Map();
            for(let i=0;i<teaser.length;i++){
              const char=document.createRange();char.setStart(teaser,i);char.setEnd(teaser,i+1);
              const rect=char.getBoundingClientRect();if(!rect.height)continue;
              const top=Math.round(rect.top);
              lines.set(top,(lines.get(top)||'')+teaser.textContent[i]);
            }
            coverTeaserLastLineGlyphs=[...lines.values()].at(-1)?.trim().length??null;
          }
          return {
            cssWidth:innerWidth,scrollWidth:root.scrollWidth,
            sourceSectionCount:document.querySelectorAll('#stage .id__source').length,
            originalNarrativeHasFootnotes:document.querySelectorAll('#stage [role="doc-endnote"],#stage .footnotes').length>0,
            resolvedTOCRoutes:anchors.filter(a=>{try{return !!document.querySelector(a.getAttribute('href'));}catch{return false;}}).length,
            totalTOCRoutes:anchors.length,
            emptyLinks:buttons.filter(a=>!a.getAttribute('href')||a.getAttribute('href')==='#').length,
            hasUnreleasedInterludes:[...document.querySelectorAll('.id__interlude')].some(el=>el.textContent.includes('尚未接入')||el.textContent.includes('等候')),
            fontsLoaded:document.fonts.status,
            coverTeaserLastLineGlyphs
          };
        });
        if(metrics.scrollWidth>metrics.cssWidth+2)defects.push('EDITORIAL_HORIZONTAL_OVERFLOW');
        if(metrics.resolvedTOCRoutes!==12||metrics.totalTOCRoutes!==12)defects.push('EDITORIAL_TOC_ROUTE');
        if(metrics.emptyLinks)defects.push('EMPTY_EDITORIAL_LINK');
        if(metrics.fontsLoaded!=='loaded')defects.push('FONT_LOAD_INCOMPLETE');
        if(metrics.coverTeaserLastLineGlyphs!==null&&metrics.coverTeaserLastLineGlyphs<3)defects.push('COVER_TEASER_WIDOW');
        results.push({id,viewport:{width,height},sections,metrics,defects,
          editorialVisualDecision:'HUMAN REVIEW REQUIRED — screenshots per section',
          publicationAcceptance:'BLOCKED: full manuscripts/media/rights and actual browser 200% zoom open'});
        if(defects.length)failures.push({id,defects});
        console.log(id+' '+(defects.length?'FAIL '+defects.join(', '):'SECTION-SPECIFIC PROOF CAPTURED'));
      }catch(e){failures.push({id,defects:[e.message]});console.error(id+' ERROR '+e.message)}
      finally{await page.close()}
    }

  }finally{await browser.close()}
  fs.writeFileSync(path.join(out,'manifest.json'),JSON.stringify({
    schema:'westside.magazine.visual-evidence.v1',commit:process.env.GITHUB_SHA,
    source:'PR-local Hugo preview',cases:results,failures,
    humanVisualReview:'PENDING',awardScore:'NOT SCORED',
    realBrowserZoom200:'NOT VERIFIED (824px case is only an effective viewport proxy)',
    finalPromotion:'BLOCKED UNTIL VISUAL SIGNOFF'
  },null,2)+'\n');
  console.log('Captured '+results.length+' screenshots; objective defects '+failures.length+'; artistic verdict NOT VERIFIED');
  if(failures.length)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
