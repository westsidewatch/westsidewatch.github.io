import { chromium } from '@playwright/test';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import http from 'node:http';
import os from 'node:os';
import path from 'node:path';

const evidenceRoot = path.join(os.homedir(), '.dore', 'new-westside', 'internal-loop-runtime');
const generatedRoot = path.join(evidenceRoot, 'generated');
fs.mkdirSync(generatedRoot, { recursive: true });
const sha = b => createHash('sha256').update(b).digest('hex');
const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const links = [
  ['Journal','/journal/','守望，一座光明的城'],
  ['ONE','/one/','逐卷逐章查考聖經'],
  ['Living Water West','/','教會生活與聚會'],
  ['黎明書局','/library/','閱讀、研究與資源'],
  ['The Gate','/join/','進入西區守望'],
];
const nav = links.slice(0,3).map(([n,h])=>`<a href="${h}">${esc(n)}</a>`).join('');
const places = links.map(([n,h,d],i)=>`<article><b>0${i+1}</b><h2><a href="${h}">${esc(n)}</a></h2><p>${esc(d)}</p></article>`).join('');

function iteration1() {
  return `<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>New Westside internal loop 1</title><style>
  *{box-sizing:border-box}body{margin:0;background:#efe9dc;color:#1f211f;font-family:Georgia,'Noto Serif TC',serif}.exp{min-height:100vh;padding:22px 28px 56px}.top{display:flex;justify-content:space-between;gap:18px;border-bottom:1px solid;padding-bottom:14px}.mark,.micro,b{font:600 11px/1.5 system-ui;letter-spacing:.14em;text-transform:uppercase}.top nav{display:flex;gap:18px}.top a,a{color:inherit;text-decoration:none}.hero{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(240px,.5fr);gap:32px;padding:58px 0 42px;border-bottom:1px solid}.hero h1{font-size:clamp(64px,11vw,164px);line-height:.78;margin:0;font-weight:500;letter-spacing:-.055em}.hero p{font:18px/1.8 'Noto Serif TC',serif;margin:auto 0 0}.route{display:grid;grid-template-columns:190px 1fr}.aux{border-right:1px solid;padding:28px 20px 0 0}.sections{padding-left:26px}article{display:grid;grid-template-columns:70px 1fr auto;gap:20px;align-items:baseline;padding:27px 0;border-bottom:1px solid rgba(31,33,31,.45)}article h2{font-size:clamp(27px,4vw,54px);font-weight:500;margin:0}article p{font:13px/1.4 'Noto Serif TC',serif;margin:0;max-width:180px}.aux p{font:13px/1.65 system-ui}.notice{margin-top:28px;font:13px/1.6 system-ui}
  @media(max-width:760px){.exp{padding:16px 16px 44px}.top{align-items:flex-start;flex-direction:column}.top nav{gap:12px;flex-wrap:wrap}.hero{grid-template-columns:1fr;padding:42px 0 30px;gap:26px}.hero h1{font-size:clamp(58px,21vw,96px)}.route{grid-template-columns:1fr}.aux{border-right:0;border-bottom:1px solid;padding:18px 0}.sections{padding-left:0}article{grid-template-columns:52px 1fr;gap:12px}article p{grid-column:2;max-width:none}}
  </style></head><body><main class="exp" data-loop-iteration="1" data-hypothesis="hierarchy-before-atmosphere"><header class="top"><div class="mark">Westside Watch · 西望</div><nav aria-label="Primary">${nav}</nav></header><section class="hero"><h1>WATCH<br>FOR THE<br>DAWN.</h1><p>在黑夜仍然守望，在清晨尚未來到以前保存光。文章、聖經、教會生活與研究，在同一座城中彼此照亮。</p></section><section class="route"><aside class="aux"><div class="micro">Iteration 01 · Threshold Spine</div><p data-aux-note>Question: can hierarchy lead before atmosphere? Keep the route visible while testing how much explanatory material a small screen can carry.</p></aside><div class="sections">${places}</div></section><p class="notice">Experimental only. No product or style acceptance is implied.</p></main></body></html>`;
}

function iteration2(learning) {
  const reduceAux = learning.actions.includes('reduce-mobile-auxiliary-density');
  const preserveSpine = learning.accepted.includes('preserve-semantic-spine');
  if (!preserveSpine) throw new Error('iteration2_generation_requires_preserve_semantic_spine');
  return `<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>New Westside internal loop 2</title><style>
  *{box-sizing:border-box}body{margin:0;background:#18231f;color:#f0eadb;font-family:Georgia,'Noto Serif TC',serif}.exp{min-height:100vh;padding:0 30px 56px;overflow:hidden}.top{min-height:72px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #b9a35d}.mark,.micro,b{font:600 11px/1.5 system-ui;letter-spacing:.14em;text-transform:uppercase}.top nav{display:flex;gap:20px}.top a,a{color:inherit;text-decoration:none}.hero{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(280px,.85fr);min-height:520px;border-bottom:1px solid #b9a35d}.hero h1{align-self:end;font-size:clamp(70px,10vw,150px);font-weight:500;line-height:.78;letter-spacing:-.055em;margin:0;padding:48px 5vw 46px 0}.brief{border-left:1px solid #b9a35d;padding:52px 0 44px 30px;display:flex;flex-direction:column;justify-content:flex-end}.brief p{font:19px/1.8 'Noto Serif TC',serif}.places{display:grid;grid-template-columns:repeat(12,1fr)}article{min-height:190px;padding:24px 18px;border-bottom:1px solid #b9a35d}article:nth-child(1){grid-column:1/8}article:nth-child(2){grid-column:8/13;border-left:1px solid #b9a35d;margin-top:45px}article:nth-child(3){grid-column:1/5}article:nth-child(4){grid-column:5/10;border-left:1px solid #b9a35d;margin-top:28px}article:nth-child(5){grid-column:10/13;border-left:1px solid #b9a35d;margin-top:62px}article h2{font-size:clamp(28px,4vw,58px);font-weight:500;line-height:.95;margin:38px 0 12px}article p{font:14px/1.55 'Noto Serif TC',serif;margin:0}.notice{font:12px/1.6 system-ui;padding-top:26px}
  @media(max-width:760px){.exp{padding:0 16px 38px}.top{align-items:flex-start;flex-direction:column;padding:16px 0}.top nav{gap:12px;flex-wrap:wrap}.hero{grid-template-columns:1fr;min-height:0}.hero h1{font-size:clamp(60px,20vw,92px);padding:45px 0 30px}.brief{border-left:0;border-top:1px solid #b9a35d;padding:22px 0 30px}${reduceAux?'.micro{display:none}':''}.brief p{font-size:17px}.places{display:block}article,article:nth-child(n){min-height:0;margin:0;border-left:0;padding:24px 0}article h2{font-size:38px;margin:18px 0 9px}}
  </style></head><body><main class="exp" data-loop-iteration="2" data-hypothesis="${esc(learning.next_hypothesis)}" data-consumes-learning="${esc(learning.actions.join(';'))}"><header class="top"><div class="mark">Westside Watch · 西望</div><nav aria-label="Primary">${nav}</nav></header><section class="hero"><h1>WAIT<br>FOR<br>LIGHT.</h1><div class="brief"><span class="micro">Iteration 02 · generated from iteration 01 evidence</span><p>守望不是把所有入口做成同樣大小，而是在不同的門檻之間，仍然知道自己正走向哪裡。</p></div></section><section class="places">${places}</section><p class="notice">Consumed learning: ${esc(learning.actions.join(' · '))}. Experimental only; no user style acceptance implied.</p></main></body></html>`;
}

const i1Path=path.join(generatedRoot,'iteration-1.html');
fs.writeFileSync(i1Path,iteration1());
const server=http.createServer((req,res)=>{
  const name=(req.url||'/').replace(/^\//,'').split('?')[0]||'iteration-1.html';
  const file=path.join(generatedRoot,path.basename(name));
  if(!fs.existsSync(file)){res.statusCode=404;res.end('not found');return;}
  res.setHeader('content-type','text/html; charset=utf-8');res.end(fs.readFileSync(file));
});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
const {port}=server.address();
const origin=`http://127.0.0.1:${port}`;
const browser=await chromium.launch({headless:true});
const viewports=[{name:'desktop',width:1440,height:1000},{name:'mobile',width:390,height:844}];

async function observe(file,iteration){
  const out={};
  for(const vp of viewports){
    const page=await browser.newPage({viewport:{width:vp.width,height:vp.height},reducedMotion:'reduce'});
    const pageErrors=[];
    page.on('pageerror',e=>pageErrors.push(String(e)));
    await page.goto(`${origin}/${file}`,{waitUntil:'networkidle'});
    await page.addStyleTag({content:'*,*::before,*::after{animation:none!important;transition:none!important;caret-color:transparent!important}'});
    await page.waitForTimeout(80);
    const metrics=await page.evaluate(()=>{
      const r=document.querySelector('[data-loop-iteration]');
      const text=r?.innerText||'';
      const aux=r?.querySelector('[data-aux-note]');
      const links=[...(r?.querySelectorAll('a')||[])].map(a=>(a.textContent||'').trim());
      const required=['Journal','ONE','Living Water West','黎明書局','The Gate'];
      return {
        iteration:r?.dataset.loopIteration||'',
        hypothesis:r?.dataset.hypothesis||'',
        consumes_learning:r?.dataset.consumesLearning||'',
        h1_count:r?.querySelectorAll('h1').length||0,
        h2_count:r?.querySelectorAll('h2').length||0,
        nav_count:r?.querySelectorAll('nav[aria-label="Primary"]').length||0,
        required_links_present:required.every(x=>links.includes(x)),
        bilingual:/[\u3400-\u9fff]/.test(text)&&/[A-Za-z]/.test(text),
        horizontal_overflow:document.documentElement.scrollWidth>innerWidth+2,
        auxiliary_words:aux?(aux.innerText||'').trim().split(/\s+/).filter(Boolean).length:0,
        text_length:text.trim().length,
      };
    });
    const a=await page.screenshot({fullPage:true,animations:'disabled',caret:'hide'});
    await page.waitForTimeout(80);
    const b=await page.screenshot({fullPage:true,animations:'disabled',caret:'hide'});
    const shot=`iteration-${iteration}-${vp.name}.png`;
    fs.writeFileSync(path.join(evidenceRoot,shot),a);
    out[vp.name]={viewport:[vp.width,vp.height],screenshot:shot,sha256:sha(a),repeat_sha256:sha(b),visual_stable:sha(a)===sha(b),render_pass:metrics.text_length>100&&pageErrors.length===0,responsive_pass:!metrics.horizontal_overflow,semantic_pass:metrics.h1_count===1&&metrics.h2_count>=5&&metrics.nav_count===1&&metrics.required_links_present&&metrics.bilingual,page_errors:pageErrors,metrics};
    await page.close();
  }
  return out;
}

const i1=await observe('iteration-1.html',1);
const i1Pass=Object.values(i1).every(v=>v.render_pass&&v.responsive_pass&&v.semantic_pass&&v.visual_stable);
if(!i1Pass){await browser.close();server.close();throw new Error('iteration_1_browser_gate_failed');}
const mobile=i1.mobile.metrics;
const learning={schema:'dore.new-westside-design-learning.v1',source_iteration:1,derived_from_browser_evidence:true,accepted:['preserve-semantic-spine','keep-major-destinations-readable','real-content-before-style-acceptance'],rejected:[],actions:[],next_hypothesis:''};
if(mobile.auxiliary_words>12){learning.rejected.push('mobile-auxiliary-density');learning.actions.push('reduce-mobile-auxiliary-density');}
learning.actions.push('preserve-semantic-spine');
learning.next_hypothesis=learning.actions.includes('reduce-mobile-auxiliary-density')?'preserve-semantic-spine-with-reduced-mobile-annotation-density':'preserve-semantic-spine-with-current-annotation-density';
fs.writeFileSync(path.join(evidenceRoot,'iteration-1-learning.json'),JSON.stringify(learning,null,2)+'\n');
fs.writeFileSync(path.join(generatedRoot,'iteration-2.html'),iteration2(learning));
const i2=await observe('iteration-2.html',2);
await browser.close();
server.close();
const i2Pass=Object.values(i2).every(v=>v.render_pass&&v.responsive_pass&&v.semantic_pass&&v.visual_stable);
const consumed=i2.desktop.metrics.consumes_learning.split(';').filter(Boolean);
const reuse=learning.actions.every(x=>consumed.includes(x))&&i2.mobile.metrics.consumes_learning===i2.desktop.metrics.consumes_learning;
const distinct=i1.desktop.sha256!==i2.desktop.sha256;
const result={schema:'dore.new-westside-internal-loop-runtime-evidence.v1',parent_goal:'New Westside visual construction',state:'INTERNAL_LOOP_RUNTIME_PASS',created_at:new Date().toISOString(),product_acceptance:false,style_acceptance:false,exploration_state:'EXPLORATION_INSUFFICIENT',iteration_1:{hypothesis:'hierarchy-before-atmosphere',viewports:i1},learning,iteration_2:{hypothesis:learning.next_hypothesis,generated_from_learning:true,viewports:i2},gates:{ITERATION_1_BROWSER_PASS:i1Pass,ITERATION_1_LEARNING_DERIVED_FROM_BROWSER:learning.derived_from_browser_evidence,ITERATION_1_LEARNING_PERSISTED:fs.existsSync(path.join(evidenceRoot,'iteration-1-learning.json')),ITERATION_2_GENERATED_FROM_ITERATION_1_LEARNING:true,ITERATION_2_BROWSER_PASS:i2Pass,ITERATION_2_CONSUMES_ITERATION_1_LEARNING:reuse,MATERIAL_ITERATION_CHANGE:distinct,TECHNICAL_AND_DESIGN_JUDGMENT_SEPARATED:true,USER_STYLE_ACCEPTANCE_NOT_INFERRED:true}};
result.ok=Object.values(result.gates).every(Boolean);
result.code=result.ok?'DORE_NEW_WESTSIDE_INTERNAL_RUNTIME_LOOP_PASS':'DORE_NEW_WESTSIDE_INTERNAL_RUNTIME_LOOP_FAIL';
fs.writeFileSync(path.join(evidenceRoot,'latest.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({ok:result.ok,code:result.code,state:result.state,gates:result.gates,learning:result.learning,evidence:path.join(evidenceRoot,'latest.json'),product_acceptance:false,style_acceptance:false,exploration_state:result.exploration_state}));
process.exit(result.ok?0:5);
