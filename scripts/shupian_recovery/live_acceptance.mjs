/**
 * 数片 — real-browser release acceptance for the public cinema, not a source-code test.
 * Verify the published catalog, desktop playback and mobile layout.
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
    const title = await page.title();
    check(/數片|数片/.test(title), 'correct_live_site_title', {title});
    const catalog = await context.request.get(new URL('screenings.json',base).href,{timeout:15000});
    const works = catalog.ok() ? await catalog.json() : null;
    check(Array.isArray(works) && works.length > 0, 'public_screenings_available',
      {status:catalog.status(), count:Array.isArray(works) ? works.length : null});
    const cards = page.locator('#grid article.card');
    await cards.first().waitFor({timeout:15000});
    check(Array.isArray(works) && await cards.count() === works.length, 'published_catalog_consistent');
    const body = await page.locator('body').innerText();
    check(!denied.some(x => body.includes(x)), 'no_filler_classics_visible');
    check(!JSON.stringify(works).toLowerCase().includes('youtube'), 'no_youtube_sources');
    await cards.first().locator('button.poster').click();
    const player = page.locator('dialog#player[open] #video');
    await player.evaluate(async video => {
      video.muted = true;
      await video.play();
    });
    await page.waitForFunction(() => {
      const video = document.querySelector('dialog#player[open] #video');
      return video && !video.paused && video.currentTime >= 2 && video.videoWidth > 0;
    }, null, {timeout:30000});
    const time = await player.evaluate(video => video.currentTime);
    check(time >= 2, 'published_video_playing', {time});
    check(errors.length===0, 'no_uncaught_js_errors',{errors});
    await page.screenshot({path:out+'/desktop.png',fullPage:true});
    await context.close();
    const mobile=await browser.newContext({viewport:{width:390,height:844},deviceScaleFactor:1,isMobile:true,hasTouch:true});
    const mobilePage=await mobile.newPage();
    const mobileRes=await mobilePage.goto(base,{waitUntil:'domcontentloaded',timeout:30000});
    check(!!mobileRes&&mobileRes.status()===200,'mobile_html_200',{status:mobileRes?.status()});
    await mobilePage.locator('#grid article.card').first().waitFor({timeout:15000});
    check(await mobilePage.locator('#grid article.card').count()>0,'mobile_cards_rendered');
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
