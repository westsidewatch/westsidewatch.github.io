/* Dawn P2 05 Design OS browser acceptance, not token-stub grep.
 * Run against the built static site on http://127.0.0.1:4173.
 */
'use strict';
const {chromium}=require('playwright'),assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path');
const out='artifacts/p2-dawn-os-repair';fs.mkdirSync(out,{recursive:true});
(async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 try{
  for(const [device,width,height] of [['desktop',1440,900],['phone',390,844]]){
   const page=await browser.newPage({viewport:{width,height},deviceScaleFactor:1});
   const errors=[];page.on('pageerror',error=>errors.push(error.message));
   await page.goto('http://127.0.0.1:4173/experiments/p2-0105-dawn-preview.html?layer=second&d=28.4&v=os-r57',
    {waitUntil:'domcontentloaded',timeout:45000});
   await page.locator('#dawn-second .dawn-wall__grid--curated').waitFor({state:'visible',timeout:20000});
   await page.evaluate(()=>document.fonts.ready);
   await page.waitForFunction(()=>document.querySelectorAll('#dawn-wall-grid button.dawn-cover').length>=12,
    null,{timeout:35000});
   const openingTitles=await page.locator('#dawn-wall-grid button.dawn-cover')
    .evaluateAll(tiles=>tiles.slice(0,4).map(tile=>tile.dataset.workTitle));
   assert(!openingTitles.some(title=>/Confessions of Zeno|The Duke of York’s Steps|A Fighting Man of Mars/.test(title)),
    device+': generic fiction unexpectedly dominates gospel library entrance');
   assert(openingTitles.some(title=>/Bible|history|church/i.test(title)),
    device+': no source-backed Biblical or church-history Works in opening selection');
   const result=await page.evaluate(()=>{
    const grab=s=>{const el=document.querySelector(s);if(!el)throw Error('Missing '+s);
      const st=getComputedStyle(el),r=el.getBoundingClientRect();
      return {font:st.fontFamily,size:parseFloat(st.fontSize),weight:parseInt(st.fontWeight,10),
       x:r.x,y:r.y,right:r.right,bottom:r.bottom,width:r.width,height:r.height,
       display:st.display,position:st.position}
    };
    return {
      typeRoles:(()=>{
       // Test the stylesheet with the exact second-layer selector contexts;
       // some roles appear only after a user opens book detail or personal.
       const host=document.querySelector('#dawn-second');
       const roles=[
        {id:'subject',markup:'<div class="dawn-classification__sleeve"><strong>聖經</strong></div>',selector:'strong'},
        {id:'resultTitle',markup:'<div class="dawn-classification__result-heading"><h4>教會歷史</h4></div>',selector:'h4'},
        {id:'personalTitle',markup:'<div class="dawn-personal__head"><h2>我的書房</h2></div>',selector:'h2'},
        {id:'catalogueTitle',markup:'<div class="dawn-catalogue__classification-head"><h3>神學</h3></div>',selector:'h3'},
        {id:'body',markup:'<div class="dawn-book-detail__text">這是正文的標準閱讀角色。</div>',selector:'.dawn-book-detail__text'},
        {id:'description',markup:'<div class="dawn-expander__description">這是正文說明。</div>',selector:'.dawn-expander__description'}
       ];
       return roles.map(role=>{
        const holder=document.createElement('div');holder.innerHTML=role.markup;
        host.append(holder);
        const cs=getComputedStyle(holder.querySelector(role.selector));
        const result={id:role.id,font:cs.fontFamily,weight:parseInt(cs.fontWeight,10),
          size:parseFloat(cs.fontSize),lineHeight:parseFloat(cs.lineHeight)};
        holder.remove();return result;
       });
      })(),
      nav:grab('.dawn-second__global-nav'),
      returnMark:grab('.dawn-second__return .dawn-second__return-mark'),
      returnZh:grab('.dawn-second__return .dawn-second__nav-zh'),
      personalEntry:grab('#dawn-personal-open'),
      catalogueEntry:grab('#dawn-open-catalogue'),
      oldTopCount:document.querySelectorAll('.dawn-second__nav-actions, #dawn-open-catalogue-top, .dawn-second__all-works').length,
      oldTopEnglish:[...document.querySelectorAll('.dawn-second__global-nav *')].filter(el=>/THE COLLECTION|MY LIBRARY/.test(el.textContent||'')).length,
      featureEn:grab('#dawn-wall-grid .dawn-feature__titles em'),
      featureZh:grab('#dawn-wall-grid .dawn-feature__titles strong'),
      missingCoverCSS:(()=>{
       const sheet=document.createElement('button');
       sheet.className='dawn-cover dawn-cover--missing';
       sheet.innerHTML='<span class="dawn-cover__meta"><strong>Real source title</strong></span>';
       sheet.style.cssText='position:absolute;width:210px;height:210px;visibility:hidden';
       document.querySelector('#dawn-wall-grid').append(sheet);
       const meta=sheet.querySelector('.dawn-cover__meta');
       const value={tileDisplay:getComputedStyle(sheet).display,opacity:getComputedStyle(meta).opacity,
        copy:getComputedStyle(meta).color};
       sheet.remove();return value;
      })(),
      loadedCoverCSS:(()=>{
       const cover=document.createElement('button');
       cover.className='dawn-wall__tile dawn-cover dawn-cover--ready';
       cover.style.cssText='position:absolute;width:210px;height:210px;visibility:hidden';
       const meta=document.createElement('span');meta.className='dawn-cover__meta';
       const title=document.createElement('strong');title.textContent='A genuine title';
       meta.append(title);cover.append(meta);
       document.querySelector('#dawn-wall-grid').append(cover);
       const cs=getComputedStyle(meta),ts=getComputedStyle(title);
       const value={opacity:cs.opacity,color:ts.color,font:ts.fontFamily};
       cover.remove();return value;
      })(),
      gallery:grab('#dawn-wall-grid'),
      source:grab('#dawn-second'),
      departmentZh:grab('.dawn-reading-room__departments-intro h3 > strong'),
      departmentEn:grab('.dawn-reading-room__departments-intro h3 > span'),
      editorialPanels:[...document.querySelectorAll('#dawn-wall-grid > .dawn-feature')].map(element=>({
        background:getComputedStyle(element).backgroundColor,
        identity:element.dataset.dawnPortal,
        title:getComputedStyle(element.querySelector('.dawn-feature__editorial')).backgroundColor,
        x:element.getBoundingClientRect().left,
        y:element.getBoundingClientRect().top,
        width:element.getBoundingClientRect().width
      })),
      harvested:getComputedStyle(document.querySelector('#dawn-second')).getPropertyValue('--ws-harvest').trim(),
      duplicateHeading:document.querySelectorAll('#dawn-room-heading, .dawn-reading-room__masthead').length,
      scripturePlates:document.querySelectorAll('.dawn-second__motherform').length,
      returnNavText:document.querySelector('.dawn-second__return .dawn-second__nav-zh').textContent.trim(),
      returnButton:grab('.dawn-second__return')
    };
   });
   for(const role of result.typeRoles){
    if(['body','description'].includes(role.id)){
      assert(/Noto Serif TC/i.test(role.font),
        device+': '+role.id+' must use the OS long-form Noto Serif TC role, got '+role.font);
      assert.equal(role.weight,400,device+': '+role.id+' must be normal OS reading weight 400');
      assert(role.lineHeight/role.size>1.7,device+': '+role.id+' needs the OS reading line-height');
    }else{
      assert(/Chiron/i.test(role.font),
        device+': '+role.id+' must use Chiron display family, got '+role.font);
      assert.equal(role.weight,200,device+': '+role.id+' is a secondary title, never 900');
    }
   }
   assert(result.featureEn.size>result.featureZh.size*1.18,
    device+': editorial cover portal still uses oversized Chinese and tiny English');
   assert.equal(result.featureZh.weight,200,
    device+': three feature portal Chinese labels must be 200');
   assert(result.missingCoverCSS.tileDisplay!=='none'&&result.missingCoverCSS.opacity==='1',
     device+': missing jackets still disappear or become blank grid swatches');
   assert(result.loadedCoverCSS.opacity==='1'&&
     !['rgb(255, 255, 255)','white'].includes(result.loadedCoverCSS.color),
     device+': loaded source cards hide their title or print it in white on paper');
   assert.equal(result.duplicateHeading,0,device+': L2 repeats the brand outside scripture plate');
   assert.equal(result.scripturePlates,1,device+': original scripture plate missing');
   assert.equal(result.returnNavText,'返回',device+': back affordance label changed');
   assert(result.returnZh.size>=14&&result.returnZh.size<=18,device+': back Chinese must use readable OS UI scale, not a headline or tiny caption');
   assert(result.returnMark.size<=21,device+': back arrow enlarged into a headline');
   assert(result.returnButton.width<115,device+': back control occupies headline-sized width');
   assert(result.returnButton.height<58,device+': back control occupies excessive height');
   for(const [label,zh] of [['back',result.returnZh]]){
    assert(zh.size>=14&&zh.size<=18,device+': '+label+' Chinese is not OS UI size');
    assert.equal(zh.weight,200,device+': '+label+' Chinese is not Chiron air');
   }
   assert.equal(result.editorialPanels.length,3,device+': three editorial departments absent');
   assert.deepEqual(result.editorialPanels.map(p=>p.identity),['三晨星','策展集','光譜']);
   const harvestRGB=await page.evaluate(()=>{
    const marker=document.createElement('span');marker.style.background='var(--ws-harvest)';
    document.querySelector('#dawn-second').append(marker);
    const color=getComputedStyle(marker).backgroundColor;marker.remove();return color;
   });
   for(const card of result.editorialPanels){
    assert.equal(card.background,harvestRGB,device+': '+card.identity+' portal background is not OS harvest');
    assert.equal(card.title,harvestRGB,device+': '+card.identity+' title panel is not OS harvest');
   }
   if(width>1100){
    assert(result.editorialPanels.every(p=>Math.abs(p.y-result.editorialPanels[0].y)<5),
      device+': three editorial entry points do not share a single opening row');
    assert(result.editorialPanels[0].x<result.editorialPanels[1].x&&
      result.editorialPanels[1].x<result.editorialPanels[2].x,
      device+': three sections not laid out in editorial reading order');
   }
   assert.equal(result.departmentZh.weight,200,device+': secondary Chinese heading must be air');
   assert(result.departmentEn.size>result.departmentZh.size,device+': department heading scale reversed');
   assert(result.nav.height<52&&result.nav.width<160&&result.nav.position==='absolute',
     device+': screenshot-rejected giant billboard still occupies the top '+JSON.stringify(result.nav));
   assert(result.oldTopCount===0&&result.oldTopEnglish===0,
     device+': THE COLLECTION / MY LIBRARY billboard returned');
   assert(result.personalEntry.height>20&&result.catalogueEntry.height>20,
     device+': Collection and My Library controls lost when moving out of top band');
   assert(result.gallery.width>width*.65,device+': gallery contracted off canvas');
   assert(result.gallery.height>120,device+': source image wall collapsed');
   const overWidth=await page.evaluate(()=>document.querySelector('#dawn-second').scrollWidth-document.querySelector('#dawn-second').clientWidth);
   assert(overWidth<18,device+': horizontal overflow '+overWidth);
   await page.locator('#dawn-personal-open').click();
   assert(await page.locator('#dawn-personal-dialog').isVisible(),
     device+': moving the personal library action broke its dialog');
   await page.locator('#dawn-personal-close').click();
   assert(!await page.locator('#dawn-personal-dialog').isVisible(),
     device+': personal library dialog no longer closes');
   // Screenshot the ACTUAL TOP of the second reading layer, not whichever
   // position the bookwall checks scrolled to. The rejected header was at top.
   await page.evaluate(()=>document.querySelector('#dawn-second')?.scrollTo({top:0,behavior:'instant'}));
   await page.waitForTimeout(150);
   const topLayout=await page.evaluate(()=>{
     const second=document.querySelector('#dawn-second');
     const nav=second.querySelector('.dawn-second__global-nav');
     const press=second.querySelector('.dawn-second__press');
     const nr=nav.getBoundingClientRect(),pr=press.getBoundingClientRect(),sr=second.getBoundingClientRect();
     return {scrollTop:second.scrollTop,navY:nr.top-sr.top,navH:nr.height,
       pressY:pr.top-sr.top,navBg:getComputedStyle(nav).backgroundColor,
       navBorder:getComputedStyle(nav).borderBottomWidth};
   });
   assert(topLayout.scrollTop<3&&topLayout.navY>=-2&&topLayout.navY<38&&
     topLayout.navH<52&&topLayout.pressY<35&&topLayout.navBorder==='0px',
     device+': rejected pale navigation band still sits above the real scripture '+JSON.stringify(topLayout));
   await page.screenshot({path:path.join(out,device+'-os-navigation-masthead.png'),fullPage:false});
   await page.locator('#dawn-wall-grid').scrollIntoViewIfNeeded();
   await page.screenshot({path:path.join(out,device+'-os-original-gallery.png'),fullPage:false});
   assert.equal(errors.length,0,device+': runtime errors '+errors.join('; '));
   console.log('DAWN_OS',device,'NO_DUPLICATE_BRAND_THREE_HARVEST_PORTALS_GALLERY_PASS',
    JSON.stringify({navHeight:result.nav.height,harvest:harvestRGB,columns:result.editorialPanels.length,overflow:overWidth}));
   await page.close();
  }
 }finally{await browser.close()}
})().catch(err=>{console.error(err);process.exitCode=1});
