'use strict';
/* V4.3: prove static design uses the TWELVE actual approved 3:4 artworks
 * and their exact frozen English master, while historic SVG stays
 * OUTSIDE the protected artwork even at mobile widths. No motion edits. */
const fs=require('node:fs');
const path=require('node:path');
const assert=require('node:assert/strict');
const {chromium}=require('playwright');
const root=path.resolve(__dirname,'..');
const source=fs.readFileSync(path.join(root,'static/experiments/olive-mountain-art-foundation-v43.html'),'utf8');
const out=path.join(root,'artifacts/p2-0104-olive');
fs.mkdirSync(out,{recursive:true});
for(const text of ['OliveSpeakerBaseline.mount(art,slug)',
 '04-olive-woodward-cousen-desktop-intaglio-v43.svg',
 '04-olive-woodward-cousen-mobile-intaglio-v43.svg',
 'data-mode="archive"','data-mode="folio"']){
 assert(source.includes(text),'V4 must preserve original posters and mount new panoramic SVG: '+text);
}
assert(!source.includes('requestAnimationFrame'),'V4.3 is STATIC ART FIRST, not another animation attempt');
assert(!source.includes('requestAnimationFrame'), 'static art study cannot add a new scroll clock');
assert(!source.includes('04-olive-botanical-gallery-v12.svg'),
 'V4.3 must not reintroduce previously rejected full-height V12 artwork');

const slugCount=(source.match(/'watchman-nee'|'derek-prince'|'david-pawson'|'stephen-tong'|'huang-shuhua'|'kang-lai-chang'|'jerry-lai'|'tong-liu'|'jiang-xiuqin'|'rick-warren'|'yu-hong-jie'|'kou-shao-en'/g)||[]).length;
assert.equal(slugCount,12,'original lineup must be exactly twelve unique speaker assets');
const eqRect=(a,b)=>({left:a.left,right:a.right,top:a.top,bottom:a.bottom,width:a.width,height:a.height});
const overlap=(a,b)=>Math.max(0,Math.min(a.right,b.right)-Math.max(a.left,b.left))*
 Math.max(0,Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top));
(async()=>{
 const browser=await chromium.launch({headless:true});
 try{
  for(const [width,height,colCount] of [[1648,928,6],[1440,900,6],[800,900,4],[390,844,3]]){
   const page=await browser.newPage({viewport:{width,height},deviceScaleFactor:1,reducedMotion:'reduce'});
   const errors=[];page.on('pageerror',e=>errors.push(String(e)));
   await page.goto('http://127.0.0.1:4173/experiments/olive-mountain-art-foundation-v43.html',
    {waitUntil:'domcontentloaded',timeout:45000});
   await page.waitForFunction(()=>document.querySelectorAll('.protected-card olive-speaker-baseline').length===12,null,{timeout:15000});
   await page.waitForFunction(()=>[...document.querySelectorAll('.protected-card img')].every(i=>i.complete&&i.naturalWidth>10),null,{timeout:30000});
   await page.evaluate(()=>document.fonts.ready);
   for(const mode of ['archive','folio']){
    await page.locator('[data-mode="'+mode+'"]').click();
    const metrics=await page.evaluate(()=>{
     const r=el=>{const b=el.getBoundingClientRect();return {left:b.left,right:b.right,top:b.top,bottom:b.bottom,width:b.width,height:b.height}};
     const stage=document.querySelector('.site-preview');
     return {
      art:[...document.querySelectorAll('.protected-card')].map(el=>({
       rect:r(el),name:el.dataset.speaker,
       shadowName:el.querySelector('olive-speaker-baseline')?.shadowRoot?.querySelector('.olive-speaker-english')?.textContent,
       shadowExists:!!el.querySelector('olive-speaker-baseline')?.shadowRoot
      })),
      heading:r(document.querySelector('.paper-register')),
      engraving:r(document.querySelector('.woodward-master')),
      credit:r(document.querySelector('.olive-art-credit')),
      creditLabelBackground:getComputedStyle(document.querySelector('.olive-art-credit__chapter')).backgroundColor,
      stage:r(stage),
      mode:stage.dataset.direction,
      fullyVector:performance.getEntriesByType('resource').filter(x=>x.name.includes('04-olive-')).map(x=>x.name),
      scenicMask:getComputedStyle(document.querySelector('.woodward-master__'+(innerWidth<=600?'mobile':'desktop'))).maskImage
     };
    });
    assert.equal(metrics.mode,mode);
    assert(metrics.scenicMask.includes('04-olive-woodward-cousen-'+(width<=600?'mobile':'desktop')+'-intaglio-v43.svg'),'correct desktop/mobile historic artmaster must be mounted');
    assert.equal(metrics.art.length,12);
    const svgPath=path.join(root,'static/images/p2-realms/v15',
     '04-olive-woodward-cousen-'+(width<=600?'mobile':'desktop')+'-intaglio-v43.svg');
    const svg=fs.readFileSync(svgPath,'utf8');
    assert(svg.includes('historical-steel-engraving')&&svg.includes('Sha1: 8097a8aa1e5c1ee4ef0bcd126578b73d89229f04'),
     'Plate must be traceable to real Woodward/Cousen source');
    assert(!/<image\\b|data:image|<script\\b/.test(svg),'SVG must be native paths without bitmap or runtime script');
    assert((svg.match(/<path\\b/g)||[]).length>250,'historic artwork must contain complex engraved contours');

    assert(metrics.credit.height>0&&metrics.credit.height<50,
      'isolated V4 folio footer must remain a small editorial element, not a global full-screen colophon');
    assert.equal(metrics.creditLabelBackground,'rgba(0, 0, 0, 0)',
      'footer text must not inherit the global white chapter background');
    assert(metrics.credit.top>=Math.max(...metrics.art.map(x=>x.rect.bottom)),
      'folio/footer must remain BELOW all twelve original posters');

    assert(metrics.art.every(x=>x.shadowExists&&x.shadowName),'all original English typography is mounted');
    const seenNames=new Set(metrics.art.map(x=>x.name));
    assert.equal(seenNames.size,12,'no duplicated speaker image');
    for(const poster of metrics.art){
     const ratio=poster.rect.width/poster.rect.height;
     assert(Math.abs(ratio-.75)<.01,'poster must remain genuine 3:4, no distortion');
     assert.equal(overlap(poster.rect,metrics.engraving),0,'ARCHIVAL horizon overlaps a poster: '+mode+' '+width+' '+poster.name);
     assert.equal(overlap(poster.rect,metrics.heading),0,'masthead overlaps a poster: '+mode+' '+width+' '+poster.name);
    }
    const topRow=metrics.art.slice(0,colCount);
    const nextRow=metrics.art.slice(colCount,2*colCount);
    assert(nextRow[0].rect.top>topRow[0].rect.top,'responsive real poster grid must wrap normally');
    const jsErrors=errors.join(' | ');
    assert.equal(errors.length,0,'V4 browser errors: '+jsErrors);
    const fname=width+'-olive-v43-static-'+mode+'.png';
    await page.locator('.site-preview').screenshot({path:path.join(out,fname),animations:'disabled'});

    console.log('OLIVE V4.3 GEOMETRY PASS — NOT ART APPROVAL',width,mode,JSON.stringify({
     posters:12,gridCols:colCount,first:metrics.art[0].rect,
     masthead:metrics.heading,engravedArt:metrics.engraving
    }));
    if((width===1648||width===390)){
     const image=await page.locator('.site-preview').screenshot({type:'jpeg',quality:51,animations:'disabled'});
     const base64=image.toString('base64');
     console.log('OLIVE_V43_ART_JPEG_BEGIN '+width);
     for(let i=0;i<base64.length;i+=3200)
      console.log('OLIVE_V43_ART_JPEG_PART '+width+' '+base64.slice(i,i+3200));
     console.log('OLIVE_V43_ART_JPEG_END '+width);
    }
   }
   await page.close();
  }
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
