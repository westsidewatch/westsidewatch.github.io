const {chromium}=require('playwright');
const fs=require('node:fs');
const assert=require('node:assert/strict');
const data=JSON.parse(fs.readFileSync('data/church/bulletins/2026-10-11.json','utf8'));
const viewports=[{name:'mobile',width:390,height:844},{name:'tablet',width:768,height:1024},{name:'desktop',width:1440,height:900}];
(async()=>{
 const browser=await chromium.launch({headless:true});
 fs.mkdirSync('/tmp/church-bulletin',{recursive:true});
 try{
  for(const viewport of viewports){
   const page=await browser.newPage({viewport:{width:viewport.width,height:viewport.height}});
   const errors=[];
   page.on('pageerror',e=>errors.push(e.message));
   const response=await page.goto('http://127.0.0.1:8765/church/bulletin-2026-10-11/',{waitUntil:'domcontentloaded',timeout:20000});
   assert.ok(response?.ok(),'bulletin page must return HTTP 200');
   assert.equal(await page.locator('.church-bulletin__timeline > li').count(),7);
   assert.equal(await page.locator('.church-bulletin__timeline time').allTextContents().then(x=>x.map(y=>y.trim()).join('|')),data.schedule.map(x=>x.time).join('|'));
   assert.equal(await page.locator('.church-bulletin__timeline h3').allTextContents().then(x=>x.map(y=>y.trim()).join('|')),data.schedule.map(x=>x.title).join('|'));
   const actions=await page.locator('.church-bulletin__timeline li').evaluateAll(nodes=>nodes.map(n=>[...n.querySelectorAll('p')].map(p=>p.textContent.trim())));
   assert.deepEqual(actions.map(x=>x.length),data.schedule.map(x=>x.actions.length));
   for(let i=0;i<actions.length;i++)for(let j=0;j<actions[i].length;j++)assert.ok(actions[i][j].includes(data.schedule[i].actions[j].text));
   assert.equal((await page.locator('#sermon-title').textContent()).trim(),data.sermon_title);
   const overflow=await page.evaluate(()=>({page:document.documentElement.scrollWidth,viewport:innerWidth}));
   assert.ok(overflow.page<=overflow.viewport+3,'horizontal overflow: '+JSON.stringify(overflow));
   assert.deepEqual(errors,[]);
   await page.screenshot({path:'/tmp/church-bulletin/'+viewport.name+'.png',fullPage:true});
   console.log('PASS church bulletin',viewport.name);
   await page.close();
  }
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
