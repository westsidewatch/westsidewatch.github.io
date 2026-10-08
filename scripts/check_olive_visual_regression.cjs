const { chromium } = require('playwright');
const fs = require('node:fs');
(async () => {
  const browser = await chromium.launch({headless:true});
  const sizes = [{name:'mobile',width:390,height:844},{name:'tablet',width:768,height:1024},{name:'desktop',width:1440,height:900}];
  fs.mkdirSync('/tmp/olive-visual',{recursive:true});
  try {
    for (const size of sizes) {
      const page = await browser.newPage({viewport:{width:size.width,height:size.height},deviceScaleFactor:1});
      await page.goto('http://127.0.0.1:8765/olive/',{waitUntil:'networkidle'});
      await page.screenshot({path:'/tmp/olive-visual/'+size.name+'.png',fullPage:true});
      const issues = await page.evaluate(() => {
        const errors = [];
        if(document.documentElement.scrollWidth>innerWidth+2) errors.push('horizontal page overflow');
        const cards=[...document.querySelectorAll('.speaker-card')];
        if(cards.length!==12) errors.push('expected 12 speaker cards, got '+cards.length);
        for(const card of cards) {
          const rect=card.getBoundingClientRect();
          const title=card.querySelector('h3')?.getBoundingClientRect();
          const meta=card.querySelector('p')?.getBoundingClientRect();
          if(title && (title.left<rect.left-2||title.right>rect.right+2||title.top<rect.top-2||title.bottom>rect.bottom+2)) errors.push(card.dataset.doreSpeaker+': title outside card');
          if(meta && (meta.left<rect.left-2||meta.right>rect.right+2||meta.top<rect.top-2||meta.bottom>rect.bottom+2)) errors.push(card.dataset.doreSpeaker+': meta outside card');
          if(title&&meta&&title.bottom>meta.top+2&&title.top<meta.bottom-2) errors.push(card.dataset.doreSpeaker+': title/meta overlap');
        }
        return errors;
      });
      console.log(size.name+': '+(issues.length?issues.join('; '):'PASS'));
      if(issues.length) process.exitCode=1;
      await page.close();
    }
  } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
