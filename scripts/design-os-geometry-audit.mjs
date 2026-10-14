#!/usr/bin/env node
/**
 * Westside Design OS — browser-grounded geometry gate.
 * Usage: node scripts/design-os-geometry-audit.mjs docs/design-os-geometry.targets.json
 * Dependency: playwright (install in your existing test environment).
 * Never writes to site CSS; reports actual rendered geometry and fails on contract violations.
 */
import fs from 'node:fs/promises';
import process from 'node:process';
import path from 'node:path';

const file = process.argv[2];
if (!file) { console.error('Usage: node scripts/design-os-geometry-audit.mjs <targets.json>'); process.exit(2); }
const config = JSON.parse(await fs.readFile(file, 'utf8'));
if (!Array.isArray(config.pages) || !config.pages.length) throw Error('pages[] is required');
const { chromium } = await import('playwright').catch(() => { throw Error('Playwright is required: npm install --no-save playwright'); });
const browser = await chromium.launch({ headless: true });
let failures = 0;
const output = [];
try {
  for (const spec of config.pages) {
    for (const viewport of (spec.viewports || [{ width: 1440, height: 900 }])) {
      const page = await browser.newPage({ viewport, deviceScaleFactor: 1, reducedMotion: 'reduce' });
      try {
        await page.goto(spec.url, { waitUntil: 'domcontentloaded', timeout: 30000 });
        await page.evaluate(() => document.fonts.ready);
        if (spec.waitFor) await page.locator(spec.waitFor).waitFor({ state: 'visible' });
        const items = [];
        if (spec.sevenfoldDawn) {
          const summary = page.locator('.sites-home-nav--floating summary');
          const film = page.locator('.sites-home-film iframe');
          const filmSrc = await film.getAttribute('src');
          const frames = [];
          const screenshotDir = spec.screenshotDir || 'design-os-screenshots';
          await fs.mkdir(screenshotDir, { recursive: true });
          const capture = async (state) => {
            const sample = await page.evaluate(() => {
              const box = selector => { const el = document.querySelector(selector); if (!el) return null; const r = el.getBoundingClientRect(); return { x:r.x,y:r.y,width:r.width,height:r.height,right:r.right,bottom:r.bottom }; };
              return { logo:box('.ws-dawn-large-logo'), scripture:box('.ws-dawn-scripture'), panel:box('.sites-home-nav--floating .sites-home-nav__panel'), folds:document.querySelectorAll('.ws-dawn-fold').length, open:document.documentElement.classList.contains('ws-dawn-open') };
            });
            const name = `dawn-${viewport.width}x${viewport.height}-${state}.png`;
            await page.screenshot({ path:path.join(screenshotDir,name), fullPage:false });
            frames.push({state,...sample,screenshot:name});
            return sample;
          };
          const closed = await capture('closed');
          await summary.click();
          await page.waitForFunction(() => document.documentElement.classList.contains('ws-dawn-open'), {timeout:7000});
          const opened = await capture('open');
          if (opened.folds !== 7) { failures++; items.push({error:'sevenfold layers: expected 7, got '+opened.folds}); }
          if (!opened.logo || !opened.scripture || !opened.panel) { failures++; items.push({error:'missing dawn geometry'}); }
          else {
            const center = opened.logo.y + opened.logo.height/2;
            if (Math.abs(center - viewport.height*.75) > 18) { failures++; items.push({error:'logo lower-half center mismatch',center,expected:viewport.height*.75}); }
            if (Math.abs(opened.scripture.y-closed.scripture.y)>3) { failures++; items.push({error:'scripture moved on menu open'}); }
          }
          if (await film.getAttribute('src') !== filmSrc) { failures++; items.push({error:'Film source changed during opening'}); }
          await summary.click();
          await page.waitForFunction(() => !document.documentElement.classList.contains('ws-dawn-active'), {timeout:7000});
          await capture('reversed');
          output.push({url:spec.url,viewport,sevenfoldFrames:frames});
        }
        for (const target of spec.targets || []) {
          const locator = page.locator(target.selector);
          const count = await locator.count();
          if (count !== 1) { failures++; items.push({ selector: target.selector, error: 'expected exactly one element, got ' + count }); continue; }
          const actual = await locator.evaluate(el => {
            const r = el.getBoundingClientRect(), s = getComputedStyle(el);
            const names = ['position','top','right','bottom','left','width','height','transform','display','visibility','zIndex','fontSize','fontFamily','marginTop','marginLeft'];
            return { box: { x:r.x,y:r.y,width:r.width,height:r.height,right:r.right,bottom:r.bottom }, computed: Object.fromEntries(names.map(n => [n,s[n]])), inline:el.getAttribute('style') || '' };
          });
          const errors = [];
          if (target.expected) for (const [axis, wanted] of Object.entries(target.expected)) {
            const tolerance = target.tolerancePx ?? 2;
            if (!(axis in actual.box) || Math.abs(actual.box[axis] - wanted) > tolerance)
              errors.push(axis + ': expected ' + wanted + ' +/- ' + tolerance + ', measured ' + actual.box[axis]);
          }
          if (target.withinViewport) {
            const b=actual.box;
            if (b.x < 0 || b.y < 0 || b.right > viewport.width || b.bottom > viewport.height)
              errors.push('outside viewport');
          }
          if (errors.length) failures += errors.length;
          items.push({ selector:target.selector, ...actual, errors });
        }
        for (const pair of spec.noOverlap || []) {
          const a=items.find(i=>i.selector===pair[0])?.box, b=items.find(i=>i.selector===pair[1])?.box;
          if (a && b && Math.min(a.right,b.right)>Math.max(a.x,b.x) && Math.min(a.bottom,b.bottom)>Math.max(a.y,b.y)) {
            failures++; items.push({ error:'overlap', pair });
          }
        }
        output.push({ url:spec.url, viewport, items });
      } catch (error) { failures++; output.push({url:spec.url,viewport,error:String(error)}); }
      finally { await page.close(); }
    }
  }
} finally { await browser.close(); }
const report = config.report || 'design-os-geometry-report.json';
await fs.writeFile(report, JSON.stringify({ failures, output }, null, 2) + '\n');
console.log('Design OS geometry: ' + (failures ? failures + ' failure(s)' : 'PASS') + '; report: ' + report);
process.exitCode = failures ? 1 : 0;
