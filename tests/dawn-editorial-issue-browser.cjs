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

    // The editorial room is a path through the existing bookstore, not a detached microsite.
    for(const route of ["/dawn-library/","/dawn-library/product/"]){
      const page=await context.newPage();
      const label=route==="/dawn-library/"?"book-root":"book-catalogue";
      try{
        const response=await page.goto("http://127.0.0.1:"+port+route,{waitUntil:"domcontentloaded",timeout:45000});
        const data=await page.evaluate(()=>{
          const links=[...document.querySelectorAll('a[href^="/dawn-library/reading-room/"]')];
          return {width:innerWidth,scrollWidth:document.documentElement.scrollWidth,
            heading:document.querySelector("main h1")?.textContent||"",
            threeLists:["gospel-essentials","inner-life","church-history"].every(slug=>links.some(a=>a.getAttribute("href").includes(slug+".html"))),
            listLinks:links.length,
            identityOverlap:(()=>{
              const nav=document.querySelector(".sites-layer-header")?.getBoundingClientRect();
              const title=document.querySelector(".sites-dawn-library .fl-header h1")?.getBoundingClientRect();
              return !!(nav&&title&&title.top<nav.bottom-2);
            })(),
            chineseOrphan:(()=>{
              const name=document.querySelector('.sites-dawn-library .fl-header h1 span[lang="zh-Hant"]');
              return !!(name&&getComputedStyle(name).whiteSpace!=="nowrap");
            })()};
        });
        results.push({page:label,viewport:viewport.name,http:response?.status(),...data});
        if(response?.status()!==200)failures.push(viewport.name+" "+label+" HTTP "+response?.status());
        if(data.scrollWidth>data.width+5){
          const offenders=await page.evaluate(()=>[...document.querySelectorAll("main *")].filter(el=>{
            const rect=el.getBoundingClientRect();return rect.width>0&&rect.right>innerWidth+5;
          }).slice(0,7).map(el=>({tag:el.tagName,className:String(el.className).slice(0,55),width:Math.round(el.getBoundingClientRect().width),right:Math.round(el.getBoundingClientRect().right)})));
          failures.push(viewport.name+" "+label+" horizontal overflow "+JSON.stringify(offenders));
        }
        if(!data.threeLists)failures.push(viewport.name+" "+label+" missing one of three reading lists");
        if(data.identityOverlap)failures.push(viewport.name+" "+label+" bookstore identity overlaps global navigation");
        if(data.chineseOrphan)failures.push(viewport.name+" "+label+" Chinese identity can wrap a single character");
        await page.screenshot({path:path.join(out,viewport.name+"-"+label+".png"),fullPage:true,animations:"disabled",timeout:30000});
        await page.locator('a[href="/dawn-library/reading-room/gospel-essentials.html"]').first().click({timeout:15000});
        await page.waitForURL("**/dawn-library/reading-room/gospel-essentials.html",{timeout:15000});
        const trail=await page.locator(".dl-trail a").count();
        if(trail<2)failures.push(viewport.name+" "+label+" did not open the guided reading journey");
      }catch(e){failures.push(viewport.name+" "+label+" "+String(e).slice(0,280))}
      finally{await page.close()}
    }
    await context.close();
  }
  await browser.close();
  fs.writeFileSync(path.join(out,"report.json"),JSON.stringify({results,failures},null,2));
  console.log(JSON.stringify({tested:results.length,failures},null,2));
  if(failures.length)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
