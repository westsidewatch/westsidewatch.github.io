#!/usr/bin/env node
/**
 * Westside Design OS — browser-grounded geometry gate.
 * Usage: node scripts/design-os-geometry-audit.mjs docs/design-os-geometry.targets.json
 * Dependency: playwright (install in your existing test environment).
 * Never writes to site CSS; reports actual rendered geometry and fails on contract violations.
 */
import fs from 'node:fs/promises';
import process from 'node:process';

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
