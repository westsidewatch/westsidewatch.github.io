const fs = require('node:fs');
const { chromium } = require('playwright');
const origin = 'http://127.0.0.1:8765';
const routes = ['/', '/one/', '/olive/', '/dawn-library/', '/church/visit/', '/p2/living-water.html', '/p2/church-tour.html?quality=classic', '/journal/'];
(async () => {
  const browser = await chromium.launch({headless:true, args:['--enable-webgl','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
  const result = [];
  try {
    for (const path of routes) {
      const context = await browser.newContext({viewport:{width:1280,height:800},serviceWorkers:'block'});
      const rec = {path, external:[], failed:[], errors:[], status:0};
      await context.route('**/*', async route => {
        const req=route.request();
        const url=req.url();
        if (url.startsWith(origin+'/') || /^(data|blob|about):/.test(url)) return route.continue();
        rec.external.push({url,type:req.resourceType()});
        return route.abort('internetdisconnected');
      });
      const page=await context.newPage();
      page.on('pageerror', e=>rec.errors.push(String(e)));
      page.on('requestfailed', req=>{if(req.url().startsWith(origin+'/'))rec.failed.push({url:req.url(),type:req.resourceType(),error:req.failure()?.errorText})});
      page.on('response', res=>{if(res.status()>=400 && res.url().startsWith(origin+'/'))rec.failed.push({url:res.url(),type:res.request().resourceType(),status:res.status()})});
      try {
        const res=await page.goto(origin+path,{waitUntil:'domcontentloaded',timeout:25000});
        rec.status=res?.status()||0;
        await page.waitForTimeout(path.includes('church-tour')?5000:2500);
        rec.dom=await page.evaluate(()=>({title:document.title,fonts:document.fonts.status,canvas:document.querySelectorAll('canvas').length,bodyClass:document.body.className,gsap:typeof window.gsap}));
        if(path==='/') {
          await page.locator('#sites-first-layer').first().scrollIntoViewIfNeeded({timeout:5000}).catch(()=>{});
          await page.waitForTimeout(1500);
        }
      }catch(e){rec.errors.push(String(e))}
      result.push(rec);
      await context.close();
    }
  }finally{await browser.close()}
  fs.writeFileSync(process.env.DORE_BROWSER_REPORT,JSON.stringify(result,null,2));
  for(const r of result)console.log(JSON.stringify(r));
  const hard=result.filter(r=>r.status!==200||r.errors.length||r.failed.some(x=>['script','stylesheet','font'].includes(x.type))||r.external.some(x=>['script','stylesheet','font'].includes(x.type)));
  if(hard.length) {console.error('Offline route/runtime failures:',hard.map(x=>x.path));process.exitCode=1;}
})().catch(e=>{console.error(e);process.exitCode=1});
