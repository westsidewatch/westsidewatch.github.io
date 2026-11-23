/* Real WebGL proof of permanently fixed bilingual South Wall identity and 248s finale.
   Uses the original GLB and camera; no replacement model or screenshot mock. */
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const base=process.env.CHURCH_TEST_ORIGIN||'http://127.0.0.1:4176';
(async()=>{
 fs.mkdirSync('artifacts/church-sign',{recursive:true});
 const browser=await chromium.launch({headless:true,args:['--no-sandbox','--enable-webgl','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 try{
  for(const cfg of [{name:'desktop',width:1440,height:900},{name:'phone',width:390,height:844}]){
   const page=await browser.newPage({viewport:{width:cfg.width,height:cfg.height},deviceScaleFactor:1});
   const messages=[];
   page.on('pageerror',e=>messages.push('PAGE_ERROR '+e.message));
   page.on('console',m=>{if(m.type()==='error')messages.push('CONSOLE '+m.text());});
   await page.goto(base+'/p2/church-tour.html?entry=p2&proofFrame=0',{waitUntil:'domcontentloaded',timeout:45000});
   await page.waitForFunction(()=>document.body.classList.contains('ready')&&typeof window.__churchRenderProofFrame==='function',null,{timeout:120000});
   const identity=await page.evaluate(()=>window.__churchSouthNameAudit);
   assert.equal(identity?.physicalMesh,true,'Native 3D mesh not mounted');
   assert.equal(identity?.wall,'south');
   assert.equal(identity?.exactChinese,'神召會活水堂西區教會');
   assert.equal(identity?.exactEnglish,'P.A.O.C. Living Water Assembly West');
   for(const t of [0,12,248]){
     const audit=await page.evaluate(time=>{
       window.__churchRenderProofFrame(time);
       return {frame:window.__churchFrameAudit,identity:window.__churchSouthNameAudit,
         canvasSize:[document.querySelector('#church-canvas')?.width,document.querySelector('#church-canvas')?.height]};
     },t);
     assert(Math.abs(audit.frame?.at-t)<0.001,'Wrong camera time: '+JSON.stringify(audit));
     assert(audit.canvasSize[0]>=cfg.width,'Missing GLB canvas');
     await page.waitForTimeout(260);
     await page.screenshot({path:'artifacts/church-sign/'+cfg.name+'-t'+t+'.png',animations:'disabled'});
     console.log('CHURCH_SOUTH_WALL_REAL_WEBGL_FRAME',cfg.name,t,JSON.stringify({identity:audit.identity,canvas:audit.canvasSize}));
   }
   console.log('BROWSER_MESSAGES',cfg.name,JSON.stringify(messages.slice(-8)));
   await page.close();
  }
 }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1});
