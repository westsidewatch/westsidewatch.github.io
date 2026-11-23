// Chromium visual smoke QA for the Dawn Library first editorial issue.
const { chromium } = require("playwright");
const fs = require("node:fs");
const path = require("node:path");
const port = process.env.PORT || "4173";
const base = "http://127.0.0.1:" + port + "/dawn-library/reading-room/";
const names = ["index.html","gospel-essentials.html","inner-life.html","church-history.html","three-stars.html","spectrum-abiding.html","jerusalem-3000.html"];
const viewports = [{name:"desktop",width:1440,height:900},{name:"mobile",width:390,height:844}];
const out = path.join(process.cwd(),"artifacts","dawn-editorial-launch");
fs.mkdirSync(out,{recursive:true});
(async () => {
  const browser = await chromium.launch({headless:true});
  const results = [], failures = [];
  for (const viewport of viewports) {
    const context = await browser.newContext({viewport:{width:viewport.width,height:viewport.height},deviceScaleFactor:1,reducedMotion:"reduce"});
    for (const name of names) {
      const page = await context.newPage();
      try {
        const response = await page.goto(base + name,{waitUntil:"domcontentloaded",timeout:45000});
        await page.waitForTimeout(500);
        // Force offscreen book covers and exhibition plates to load before full-page screenshots.
        await page.evaluate(async () => {
          const images = [...document.querySelectorAll("main img")];
          images.forEach(im => { im.loading = "eager"; });
          await Promise.all(images.map(im => new Promise(resolve => {
            if(im.complete) return resolve();
            im.addEventListener("load",resolve,{once:true});
            im.addEventListener("error",resolve,{once:true});
            setTimeout(resolve,4500);
          })));
        });

        const data = await page.evaluate(() => {
          const imgs = [...document.querySelectorAll("main img")];
          return {
            width: innerWidth,
            scrollWidth: document.documentElement.scrollWidth,
            heading: document.querySelector("main h1")?.textContent || "",
            imageCount: imgs.length,
            brokenImages: imgs.filter(im=>im.complete&&im.naturalWidth===0).map(im=>({src:im.src,alt:im.alt})),
            aboveFold: imgs.filter(im=>{const r=im.getBoundingClientRect();return r.top<innerHeight&&r.bottom>0;})
              .map(im=>({src:im.src,loaded:im.complete && im.naturalWidth>0}))
          };
        });
        const status = response?.status();
        results.push({page:name,viewport:viewport.name,http:status,...data});
        if(status!==200)failures.push(viewport.name+" "+name+" HTTP "+status);
        if(data.scrollWidth>data.width+5)failures.push(viewport.name+" "+name+" horizontal overflow");
        if(!data.heading.trim())failures.push(viewport.name+" "+name+" no H1");
        for(const img of data.brokenImages)failures.push(viewport.name+" "+name+" broken book/exhibit image "+img.src+" — "+img.alt);
        for(const img of data.aboveFold)if(!img.loaded&&name!=="jerusalem-3000.html")failures.push(viewport.name+" "+name+" broken main image "+img.src);
        await page.screenshot({path:path.join(out,viewport.name+"-"+name.replace(".html",".png")),fullPage:["index.html","three-stars.html","spectrum-abiding.html","jerusalem-3000.html"].includes(name),animations:"disabled",timeout:30000});
      } catch(e) {
        failures.push(viewport.name+" "+name+" "+String(e).slice(0,280));
      } finally {await page.close();}
    }
    await context.close();
  }
  await browser.close();
  fs.writeFileSync(path.join(out,"report.json"),JSON.stringify({results,failures},null,2));
  console.log(JSON.stringify({tested:results.length,failures},null,2));
  if(failures.length)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
