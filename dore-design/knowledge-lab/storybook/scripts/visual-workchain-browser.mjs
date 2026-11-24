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
 report.pass=true;
 }catch(e){report.error=String(e);console.error('REJECT',path,width,report.error)}
 finally{await page.screenshot({path:join(out,name+'.png'),fullPage:true,timeout:30000}).catch(()=>{});await page.close();results.push(report)}
}
try{
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
