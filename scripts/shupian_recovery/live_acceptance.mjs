/**
 * 数片 — real-browser release acceptance for the public cinema, not a source-code test.
 * Exit nonzero unless the published user-facing page, catalog, poster and UI load.
 *
 * npm install --no-save playwright@1.58.2
 * npx playwright install --with-deps chromium
 * SHUPIAN_SITE_URL=https://westsidewatch.github.io/shupian/ node scripts/shupian_recovery/live_acceptance.mjs
 */
import {chromium} from 'playwright';
import {mkdir, writeFile} from 'node:fs/promises';

const base = process.env.SHUPIAN_SITE_URL || 'https://westsidewatch.github.io/shupian/';
const out = process.env.SHUPIAN_PROOF_DIR || 'artifacts/shupian-live-proof';
const denied = ['將軍號', '活死人之夜', '從馬槽到十字架', '貝弗利山人', '寶蓮歷險記'];
const results = {url: base, generatedAt: new Date().toISOString(), checks: [], failures: [], browser: 'Chromium'};
let browser;
const check = (condition, name, details = {}) => {
  results.checks.push({name, ok: !!condition, ...details});
  if (!condition) results.failures.push(name);
};
try {
  await mkdir(out, {recursive: true});
  browser = await chromium.launch({headless: true});
  const context = await browser.newContext({viewport:{width:1440,height:1000},deviceScaleFactor:1});
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(String(e)));
  let response;
  try {
    response = await page.goto(base + (base.includes('?') ? '&' : '?') + 'proof=' + Date.now(), {
      waitUntil:'domcontentloaded',timeout:30000
    });
  } catch (e) { check(false, 'public_html_reachable', {error:String(e)}); }
  check(!!response && response.status() === 200, 'public_html_200', {status:response?.status() ?? null});
  if (response?.status() === 200) {
    await page.waitForTimeout(2200);
    const title = await page.title();
    check(title.includes('数片'), 'correct_live_site_title', {title});
    const cards = await page.locator('#grid article.card').count();
    check(cards >= 1, 'rendered_cards', {cards});
    check(await page.locator('#grid aside.feature-detail').count() === (cards === 1 ? 1 : 0),
      'one_title_editorial_layout_renders');
    const body = await page.locator('body').innerText();
    check(!denied.some(x => body.includes(x)), 'no_filler_classics_visible');
    const inline = await page.locator('script#catalog').textContent();
    let works = [];
    try { works=JSON.parse(inline||'[]'); } catch (e) {check(false,'valid_embedded_catalog',{error:String(e)});}
    check(works.length >= 14, 'restored_multititle_catalog',{count:works.length});
    check(works.some(x => x.id === 'the-institute-historical'), 'original_institute_present');
    check(works.every(x => !denied.some(b => x.title?.includes(b))), 'catalog_no_filler');
    check(!JSON.stringify(works).toLowerCase().includes('youtube'), 'no_youtube_sources');
    check(works.filter(x=>x.type==='film').length>=11&&works.filter(x=>x.type==='series').length>=3,'restored_films_and_series_present');
    check(works.every(x=>typeof x.posterUrl==='string'&&x.posterUrl.startsWith('https://')),'every_work_has_explicit_poster_url');
    if (cards >= 1) {
      try {
        await page.locator('#grid article.card button.poster').first().click();
        check(await page.locator('dialog#player').evaluate(el => el.open), 'player_dialog_opens');
        const episodes = await page.locator('#episodes button').count();
        check(episodes === 10, 'historical_episode_index_restored', {episodes});
        await page.locator('#close').click();
      } catch (error) { check(false, 'player_episode_navigation', {error:String(error)}); }
    }
    const poster = page.locator('#grid article.card img').first();
    let posterLoaded = false, src = null;
    try {
      await poster.waitFor({state:'attached',timeout:10000});
      await page.waitForFunction(() => {
        const img=document.querySelector('#grid article.card img');
        return img && img.complete && img.naturalWidth>0;
      }, null, {timeout:20000});
      src=await poster.getAttribute('src');
      posterLoaded=true;
    } catch (e) {src=await poster.getAttribute('src').catch(()=>null);}
    check(posterLoaded,'first_real_poster_rendered',{src});
    const posterResults=[];
    const cardsAll=page.locator('#grid article.card');
    for(let i=0;i<await cardsAll.count();i++){
      const card=cardsAll.nth(i);
      await card.scrollIntoViewIfNeeded();
      const info=await card.evaluate(async element=>{
        const image=element.querySelector('img');
        if(!image)return {ok:false,reason:'no poster element',name:element.querySelector('h3')?.textContent||''};
        if(!image.complete)await new Promise(resolve=>{
          const done=()=>resolve();
          image.addEventListener('load',done,{once:true});
          image.addEventListener('error',done,{once:true});
          setTimeout(done,8500);
        });
        return {ok:image.complete&&image.naturalWidth>0,width:image.naturalWidth,url:image.currentSrc||image.src,name:element.querySelector('h3')?.textContent||''};
      });
      posterResults.push(info);
    }
    check(posterResults.every(x=>x.ok),'all_public_posters_visually_decode',{
      total:posterResults.length,decoded:posterResults.filter(x=>x.ok).length,
      failed:posterResults.filter(x=>!x.ok)
    });
    let remote = null;
    try {
      const res = await context.request.get(new URL('catalog.json',base).href,{timeout:15000});
      remote = res.ok()? await res.json() : null;
      check(res.status()===200,'remote_json_200',{status:res.status()});
    } catch(e) {check(false,'remote_json_200',{error:String(e)});}
    if(remote){
      const published=remote.titles||[];
      check(JSON.stringify(published)===JSON.stringify(works),'published_catalog_consistent',{external:published.length,inline:works.length});
    }
    check(errors.length===0, 'no_uncaught_js_errors',{errors});
    await page.screenshot({path:out+'/desktop.png',fullPage:true});
    await context.close();
    const mobile=await browser.newContext({viewport:{width:390,height:844},deviceScaleFactor:1,isMobile:true,hasTouch:true});
    const mobilePage=await mobile.newPage();
    const mobileRes=await mobilePage.goto(base,{waitUntil:'domcontentloaded',timeout:30000});
    check(!!mobileRes&&mobileRes.status()===200,'mobile_html_200',{status:mobileRes?.status()});
    await mobilePage.waitForTimeout(1500);
    check(await mobilePage.locator('#grid article.card').count()>0,'mobile_cards_rendered');
    check(await mobilePage.locator('#grid aside.feature-detail').count()===(await mobilePage.locator('#grid article.card').count()===1?1:0),'mobile_feature_layout_adapts_to_inventory');
    const overflow = await mobilePage.evaluate(()=>document.documentElement.scrollWidth > innerWidth+2);
    check(!overflow,'no_mobile_horizontal_overflow');
    await mobilePage.screenshot({path:out+'/mobile.png',fullPage:true});
    await mobile.close();
  }
} catch (e) {
  check(false,'unexpected_browser_failure',{error:String(e)});
} finally {
  if(browser) await browser.close();
  await mkdir(out,{recursive:true});
  await writeFile(out+'/acceptance.json',JSON.stringify(results,null,2)+'\n','utf8');
}
console.log(JSON.stringify(results,null,2));
if (results.failures.length) process.exitCode=1;
