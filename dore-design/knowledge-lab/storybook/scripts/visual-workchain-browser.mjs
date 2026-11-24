import {chromium} from '@playwright/test';
import assert from 'node:assert/strict';
import {readFileSync, mkdirSync, readdirSync, statSync} from 'node:fs';
import {resolve,join,relative} from 'node:path';
import {createServer} from 'node:http';
import {execFileSync} from 'node:child_process';
const root=resolve(new URL('../../../..',import.meta.url).pathname);
const staticRoot=join(root,'static');
const out=join(root,'visual-workchain-browser-evidence');
mkdirSync(out,{recursive:true});
const server=createServer((req,res)=>{
  try {
    const pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
    const p=resolve(staticRoot,'.'+pathname);
    if(!p.startsWith(staticRoot+'/'))throw Error('escape');
    const mime={'.html':'text/html; charset=utf-8','.css':'text/css','.js':'text/javascript','.woff2':'font/woff2','.ttf':'font/ttf','.svg':'image/svg+xml','.webp':'image/webp','.png':'image/png'};
    const ext=p.slice(p.lastIndexOf('.'));res.setHeader('Content-Type',mime[ext]||'application/octet-stream');res.end(readFileSync(p));
  }catch{res.statusCode=404;res.end('not found')}
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const origin='http://127.0.0.1:'+server.address().port;
const browser=await chromium.launch({headless:true});
const results=[];
function validatePair(m){
  assert(m.en.visible&&m.zh.visible,'paired titles must be visible');
  assert(m.en.size>m.zh.size,'English title must be larger than Chinese');
  assert(m.en.size>=1.7*m.zh.size,'English/Chinese scale ratio below 1.7');
  assert.equal(m.en.weight,400,'English title weight');
  assert.equal(m.zh.weight,600,'Chinese title weight');
  assert(m.en.family.includes('Bodoni Moda'),'English family');
  assert(m.zh.family.includes('Chiron Hei HK WS'),'Chinese family');
  assert(m.en.actual.length>0&&m.en.actual.every(f=>f.isCustomFont&&/bodoni/i.test(f.familyName+' '+f.postScriptName)),'English actual glyph font fallback');
  assert(m.zh.actual.length>0&&m.zh.actual.every(f=>f.isCustomFont&&/chiron/i.test(f.familyName+' '+f.postScriptName)),'Chinese actual glyph font fallback');
  assert(m.en.size>=72&&m.en.size<=160.1,'English realm role outside OS range');
  assert(m.zh.size>=36&&m.zh.size<=68.1,'Chinese realm role outside OS range');
}
const fake={en:{visible:true,size:100,weight:400,family:'Bodoni Moda',actual:[{isCustomFont:true,familyName:'Bodoni Moda'}]},zh:{visible:true,size:50,weight:600,family:'Chiron Hei HK WS',actual:[{isCustomFont:true,familyName:'Chiron Hei HK'}]}};
validatePair(fake);
for(const [name,mutate] of [
 ['reverse hierarchy',x=>x.en.size=30],['same hierarchy',x=>x.zh.size=100],
 ['wrong font',x=>x.en.family='Georgia'],['fallback glyphs',x=>x.zh.actual=[{isCustomFont:false,familyName:'Arial'}]],
 ['invisible title',x=>x.en.visible=false],['wrong weight',x=>x.zh.weight=900],
 ['out of OS range',x=>x.en.size=200]
]){const x=structuredClone(fake);mutate(x);assert.throws(()=>validatePair(x),undefined,name);console.log('NEGATIVE PASS',name)}
async function measure(page,selector,cdp){
 const node=page.locator(selector);assert.equal(await node.count(),1,'exactly one '+selector);
 const data=await node.evaluate(e=>{const s=getComputedStyle(e),r=e.getBoundingClientRect();return {text:e.textContent.trim(),size:parseFloat(s.fontSize),weight:Number(s.fontWeight),family:s.fontFamily,visible:r.width>0&&r.height>0&&s.visibility==='visible'&&s.display!=='none'&&Number(s.opacity)>0&&!!e.checkVisibility({checkOpacity:true,checkVisibilityCSS:true}),box:{x:r.x,y:r.y,w:r.width,h:r.height}}});
 const doc=await cdp.send('DOM.getDocument');const q=await cdp.send('DOM.querySelector',{nodeId:doc.root.nodeId,selector});const fonts=await cdp.send('CSS.getPlatformFontsForNode',{nodeId:q.nodeId});data.actual=fonts.fonts;return data;
}

async function findNavigationArrows(page){
 return page.evaluate(()=>{
   const arrows=/[\u2190-\u21ff\u27f0-\u27ff\u2900-\u297f\u2b05-\u2b07\u2b95\u2039\u203a\u00ab\u00bb\u276e-\u2771\u2794\u279c-\u27be]/u;
   const names=/(?:^|[\s_:\/#.-])(?:arrow(?:[-_](?:up|down|left|right|up-right|down-right|up-left|down-left))?|chevron(?:[-_](?:up|down|left|right|first|last))?|external[-_]link)(?:$|[\s_:\/#.-])/i;
   const visible=e=>e.checkVisibility({checkOpacity:true,checkVisibilityCSS:true})&&e.getClientRects().length>0;
   const failures=[];
   for(const a of document.querySelectorAll('a[href], [role="link"], button[data-href], button[onclick*="location"]')){
     if(!visible(a))continue;
     const id=(a.getAttribute('href')||a.getAttribute('aria-label')||a.outerHTML).slice(0,150);
     const nodes=[a,...a.querySelectorAll('*')].filter(visible);
     for(const el of nodes){
       const text=Array.from(el.childNodes).filter(n=>n.nodeType===3).map(n=>n.textContent).join('');
       if(arrows.test(text))failures.push({link:id,kind:'text',value:text.trim().slice(0,100)});
       for(const pseudo of ['::before','::after']){
         const style=getComputedStyle(el,pseudo);
         if(style.display!=='none'&&style.visibility!=='hidden'&&Number(style.opacity)>0&&arrows.test(style.content))failures.push({link:id,kind:pseudo,value:style.content});
       }
       if(el.matches('svg, use, i, span, img')) {
         const signature=['class','data-icon','data-lucide','aria-label','href','xlink:href','src'].map(k=>el.getAttribute(k)||'').join(' ');
         if(names.test(signature))failures.push({link:id,kind:'icon',value:signature.trim().slice(0,100)});
       }
     }
   }
   return failures;
 });
}
async function testNavigationArrowAudit(){
 const p=await browser.newPage();
 try{
   const fixtures=[
     ['inline arrow','<a href="/next">閱讀更多 ↗</a>',true],
     ['pseudo arrow','<style>a::after{content:"\\2192"}</style><a href="/next">閱讀更多</a>',true],
     ['svg named arrow','<a href="/next">閱讀更多<svg width="16" height="16" class="lucide-arrow-up-right"><path d="M2 14L14 2"/></svg></a>',true],
     ['hidden old mark','<a href="/next">閱讀更多<span hidden>↗</span></a>',false],
     ['non-navigation quoted arrow','<blockquote>A → B</blockquote><a href="/next">閱讀更多</a>',false],
     ['decorative battlement','<a href="/next">閱讀更多<span aria-hidden="true">▆▇▅▇▆▅</span></a>',false]
   ];
   for(const [name,html,bad] of fixtures){
     await p.setContent(html);const hits=await findNavigationArrows(p);assert.equal(hits.length>0,bad,name);console.log('NAVIGATION AUDIT PASS',name);
   }
 }finally{await p.close()}
}

async function audit(path,width){
 const page=await browser.newPage({viewport:{width,height:900}});const name=path.replaceAll('/','_')+'-'+width;let report={path,width,pass:false};
 try{
 await page.goto(origin+'/'+path,{waitUntil:'load',timeout:45000});await page.evaluate(()=>document.fonts.ready);
 const cdp=await page.context().newCDPSession(page);await cdp.send('DOM.enable');await cdp.send('CSS.enable');
 report.en=await measure(page,'[data-workchain-title="en"]',cdp);report.zh=await measure(page,'[data-workchain-title="zh"]',cdp);
 assert.match(report.en.text,/Living Water/i);assert.match(report.zh.text,/活水堂/);
 validatePair(report);
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'horizontal overflow');
 assert(await page.evaluate(()=>[...document.images].every(i=>i.complete&&i.naturalWidth>0)),'broken images');
 assert(await page.evaluate(()=>document.querySelectorAll('main h1').length===1),'one semantic main h1 required');
 // Immutable V01–V05 are historical comparison evidence, not current approval candidates.
 if(!/^experiments\/church-foundation-v0[1-5]\//.test(path)){
   report.navigationArrows=await findNavigationArrows(page);
   assert.equal(report.navigationArrows.length,0,'decorative navigation arrow: '+JSON.stringify(report.navigationArrows));
 }
 report.pass=true;
 }catch(e){report.error=String(e);console.error('REJECT',path,width,report.error)}
 finally{await page.screenshot({path:join(out,name+'.png'),fullPage:true,timeout:30000}).catch(()=>{});await page.close();results.push(report)}
}
try{
 await testNavigationArrowAudit();
 // Historical rejected releases are never promoted; run actual negative cases too.
 const old=['experiments/church-foundation-v01/index.html','experiments/church-foundation-v02/a.html','experiments/church-foundation-v02/b.html'];
 for(const path of old){await audit(path,1440);assert.equal(results.at(-1).pass,false,'rejected release admitted')}
 const walk=p=>readdirSync(p).flatMap(n=>{const f=join(p,n);return statSync(f).isDirectory()?walk(f):[f]});
 const candidates=walk(join(staticRoot,'experiments')).filter(p=>/\/church-foundation-v(?!01\/|02\/)\d+\/.*\.html$/.test(p));
 // All subsequent church candidate pages are audited, not just nominated files.
 for(const file of candidates){const p=relative(staticRoot,file);for(const width of [320,390,768,1440])await audit(p,width)}
 const bad=results.filter(r=>!old.includes(r.path)&&!r.pass);
 console.log('Candidates:',candidates.length,'failed:',bad.length);
 if(bad.length)process.exitCode=1;
}finally{
 const {writeFileSync}=await import('node:fs');writeFileSync(join(out,'report.json'),JSON.stringify({commit:execFileSync('git',['rev-parse','HEAD'],{cwd:root,encoding:'utf8'}).trim(),results},null,2));
 await browser.close();await new Promise(r=>server.close(r));
}
