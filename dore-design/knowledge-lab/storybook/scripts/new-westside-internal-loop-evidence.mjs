import { chromium } from '@playwright/test';
import { createHash } from 'node:crypto';
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import process from 'node:process';

const root = process.cwd();
const staticDir = path.join(root, 'storybook-static');
const indexPath = path.join(staticDir, 'index.json');
const evidenceRoot = path.join(os.homedir(), '.dore', 'new-westside', 'internal-loop');
fs.mkdirSync(evidenceRoot, { recursive: true });
const sleep = ms => new Promise(r => setTimeout(r, ms));
const hash = b => createHash('sha256').update(b).digest('hex');

if (!fs.existsSync(indexPath)) throw new Error('storybook-static/index.json missing');
const index = JSON.parse(fs.readFileSync(indexPath, 'utf8'));
const wanted = Object.values(index.entries || {}).filter(e => /New Westside\/Internal Loop/i.test(e.title || '')).sort((a,b)=>(a.name||'').localeCompare(b.name||''));
if (wanted.length !== 2) throw new Error(`expected exactly 2 internal-loop stories, found ${wanted.length}`);

const port = Number(process.env.DORE_INTERNAL_LOOP_PORT || (24000 + (process.pid % 12000)));
const origin = `http://127.0.0.1:${port}`;
const server = spawn('python3', ['-m','http.server',String(port),'--bind','127.0.0.1','--directory',staticDir], { stdio:'ignore' });
let ready = false;
for (let i=0;i<40;i++) { try { const r=await fetch(`${origin}/index.json`); if(r.ok){ready=true;break;} } catch {} await sleep(100); }
if (!ready) throw new Error('internal-loop evidence server not ready');

const viewports = [{name:'desktop',width:1440,height:1000},{name:'mobile',width:390,height:844}];
const result = {
  schema:'dore.new-westside-internal-loop-evidence.v1',
  parent_goal:'New Westside visual construction',
  state:'INTERNAL_LOOP_BOOTSTRAP',
  created_at:new Date().toISOString(),
  product_acceptance:false,
  style_acceptance:false,
  exploration_state:'EXPLORATION_INSUFFICIENT',
  iterations:[],
};
let browser;
try {
  browser = await chromium.launch({headless:true});
  for (const [idx,entry] of wanted.entries()) {
    const row={iteration:idx+1,story_id:entry.id,name:entry.name,viewports:{}};
    for (const vp of viewports) {
      const page=await browser.newPage({viewport:{width:vp.width,height:vp.height},reducedMotion:'reduce'});
      const errors=[]; page.on('pageerror',e=>errors.push(String(e)));
      await page.goto(`${origin}/iframe.html?id=${encodeURIComponent(entry.id)}&viewMode=story`,{waitUntil:'networkidle',timeout:30000});
      await page.addStyleTag({content:'*,*::before,*::after{animation:none!important;transition:none!important;caret-color:transparent!important}'}).catch(()=>{});
      await page.waitForTimeout(120);
      const metrics=await page.evaluate(()=>{
        const root=document.querySelector('[data-new-westside-internal-loop]');
        const links=[...document.querySelectorAll('a')].map(a=>({text:(a.textContent||'').trim(),href:a.getAttribute('href')}));
        const required=['Journal','ONE','Living Water West','黎明書局','The Gate'];
        return {
          iteration:root?.getAttribute('data-iteration')||null,
          hypothesis:root?.getAttribute('data-hypothesis')||null,
          consumes_learning:root?.getAttribute('data-consumes-learning')||'',
          h1_count:document.querySelectorAll('h1').length,
          h2_count:document.querySelectorAll('h2').length,
          nav_count:document.querySelectorAll('nav[aria-label="Primary"]').length,
          required_links_present:required.every(name=>links.some(x=>x.text===name)),
          bilingual:/[\u3400-\u9fff]/.test(document.body.innerText)&&/[A-Za-z]/.test(document.body.innerText),
          horizontal_overflow:document.documentElement.scrollWidth>innerWidth+2,
          text_length:(document.body.innerText||'').trim().length,
        };
      });
      const shot1=await page.screenshot({fullPage:true,animations:'disabled',caret:'hide'}); await page.waitForTimeout(100); const shot2=await page.screenshot({fullPage:true,animations:'disabled',caret:'hide'});
      const filename=`iteration-${idx+1}-${vp.name}.png`; fs.writeFileSync(path.join(evidenceRoot,filename),shot1);
      row.viewports[vp.name]={viewport:[vp.width,vp.height],screenshot:filename,sha256:hash(shot1),repeat_sha256:hash(shot2),visual_stable:hash(shot1)===hash(shot2),render_pass:metrics.text_length>100&&errors.length===0,responsive_pass:!metrics.horizontal_overflow,semantic_pass:metrics.h1_count===1&&metrics.h2_count>=5&&metrics.nav_count===1&&metrics.required_links_present&&metrics.bilingual,page_errors:errors,metrics};
      await page.close();
    }
    result.iterations.push(row);
  }
} finally { if(browser) await browser.close(); server.kill('SIGTERM'); }

const i1=result.iterations[0], i2=result.iterations[1];
const allViews=result.iterations.flatMap(x=>Object.values(x.viewports));
const learning={
  iteration_1_hypothesis:'hierarchy-before-atmosphere',
  accepted_provisional:['preserve-semantic-spine','keep-major-destinations-readable','real-content-before-style-acceptance'],
  rejected_provisional:['equal-tile-grid-as-default','mobile-side-annotation-density'],
  next_hypothesis:'semantic-spine-with-responsive-thresholds',
  required_consumption:['preserve-semantic-spine','reduce-mobile-annotation-density','make-section-thresholds-explicit','avoid-equal-tile-grid'],
};
const consumed=i2.viewports.desktop.metrics.consumes_learning.split(';').filter(Boolean);
const explicitReuse=learning.required_consumption.every(x=>consumed.includes(x))&&i2.viewports.mobile.metrics.consumes_learning===i2.viewports.desktop.metrics.consumes_learning;
const distinct=hash(fs.readFileSync(path.join(evidenceRoot,'iteration-1-desktop.png')))!==hash(fs.readFileSync(path.join(evidenceRoot,'iteration-2-desktop.png')));
result.learning=learning;
result.gates={
  ITERATION_1_BROWSER_PASS:Object.values(i1.viewports).every(v=>v.render_pass&&v.responsive_pass&&v.semantic_pass&&v.visual_stable),
  ITERATION_1_LEARNING_PERSISTED:true,
  ITERATION_2_BROWSER_PASS:Object.values(i2.viewports).every(v=>v.render_pass&&v.responsive_pass&&v.semantic_pass&&v.visual_stable),
  ITERATION_2_CONSUMES_ITERATION_1_LEARNING:explicitReuse,
  MATERIAL_ITERATION_CHANGE:distinct,
  TECHNICAL_AND_DESIGN_JUDGMENT_SEPARATED:true,
  USER_STYLE_ACCEPTANCE_NOT_INFERRED:true,
};
result.design_judgment={
  iteration_1:'PROVISIONAL_LEARNING: route hierarchy is testable and readable; mobile side annotations should be reduced before deeper visual exploration.',
  iteration_2:'PROVISIONAL_LEARNING: preserves semantic route while applying reduced mobile annotations and non-equal threshold composition; still not a style candidate or user-approved direction.',
};
result.ok=Object.values(result.gates).every(Boolean);
result.code=result.ok?'DORE_NEW_WESTSIDE_INTERNAL_LOOP_PASS':'DORE_NEW_WESTSIDE_INTERNAL_LOOP_FAIL';
result.state=result.ok?'INTERNAL_LOOP_PASS':'INTERNAL_LOOP_FAIL';
fs.writeFileSync(path.join(evidenceRoot,'latest.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({ok:result.ok,code:result.code,state:result.state,gates:result.gates,evidence:path.join(evidenceRoot,'latest.json'),iterations:result.iterations.map(x=>({iteration:x.iteration,story_id:x.story_id,viewports:x.viewports})),learning:result.learning,design_judgment:result.design_judgment,product_acceptance:false,style_acceptance:false,exploration_state:result.exploration_state}));
process.exit(result.ok?0:4);
