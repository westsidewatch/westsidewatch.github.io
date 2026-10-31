import assert from 'node:assert/strict';import fs from 'node:fs/promises';import {chromium} from 'playwright';
const out=process.env.J3K_OUTPUT||'work/j3k-temple-sections';await fs.mkdir(out,{recursive:true});
const browser=await chromium.launch({headless:true});try{
 const p=await browser.newPage({viewport:{width:1350,height:950},reducedMotion:'reduce'}),errors=[],rows=[];
 p.on('pageerror',e=>errors.push(String(e)));p.on('console',m=>{if(m.type()==='error'&&/shader|WebGLProgram/i.test(m.text()))errors.push(m.text());});
 await p.goto(process.env.J3K_URL||'http://127.0.0.1:8765/preview/jerusalem-3000/',{waitUntil:'networkidle'});await p.waitForFunction(()=>window.__JERUSALEM3000__?.status==='ready');
 for(const v of[3.9,6.9,7.9,8.9]){
  await p.locator('.j3k-scrubber').evaluate((e,v)=>{e.value=String(v);e.dispatchEvent(new Event('input',{bubbles:true}));},v);
  await p.waitForFunction(v=>window.__JERUSALEM3000__.historicalTime.position===v,v);
  await p.getByRole('button',{name:'聖殿近看',exact:true}).click();await p.waitForTimeout(1000);
  const canvas=p.locator('.j3k-stage canvas').first(),capture=async()=>{const b=await canvas.boundingBox();return p.screenshot({clip:{x:b.x,y:b.y+110,width:b.width,height:b.height-110}});},before=await capture();
  await p.getByRole('button',{name:'聖殿剖視',exact:true}).click();await p.waitForTimeout(200);
  const info=await p.evaluate(()=>window.__JERUSALEM3000__.inspectTempleSection());assert.equal(info.enabled,true);assert.ok(info.clippedMeshes>0);
  const cut=await capture();assert.ok(!before.equals(cut),`GPU section must visibly change temple ${v}`);
  await p.screenshot({path:`${out}/temple-section-${v}.png`,fullPage:true});
  await p.getByRole('button',{name:'聖殿剖視',exact:true}).click();await p.waitForTimeout(200);
  assert.equal(await p.evaluate(()=>window.__JERUSALEM3000__.inspectTempleSection().clippedMeshes),0);
  const restored=await capture();await fs.writeFile(`${out}/canvas-before-${v}.png`,before);await fs.writeFile(`${out}/canvas-restored-${v}.png`,restored);assert.ok(before.equals(restored),`closing section must restore original GPU scene below the toolbar ${v}`);rows.push({position:v,section:info,exactCanvasRestore:true});
 }
 await p.setViewportSize({width:390,height:844});await p.getByRole('button',{name:'聖殿剖視',exact:true}).click();await p.waitForTimeout(200);await p.screenshot({path:`${out}/temple-section-mobile.png`,fullPage:true});assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
 assert.deepEqual(errors,[]);await fs.writeFile(`${out}/temple-sections-proof.json`,JSON.stringify({rows,errors,historicalGeometryAccepted:false},null,2));console.log('PASS: first/Persian/Hasmonean/Herodian GPU cutaway, exact canvas restore, shader safety and portrait');
}finally{await browser.close();}
