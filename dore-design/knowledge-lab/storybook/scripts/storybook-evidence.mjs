import { chromium } from '@playwright/test';
import { createHash } from 'node:crypto';
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';

const root = process.cwd();
const staticDir = path.join(root, 'storybook-static');
const indexPath = path.join(staticDir, 'index.json');
const evidenceDir = path.resolve(root, '..', 'evidence', 'storybook-autonomy');
fs.mkdirSync(evidenceDir, { recursive: true });

const sleep = ms => new Promise(r => setTimeout(r, ms));
const sha = b => createHash('sha256').update(b).digest('hex');

if (!fs.existsSync(indexPath)) {
  console.error(JSON.stringify({ ok: false, error: 'storybook-static/index.json missing; build Storybook first' }));
  process.exit(2);
}

const index = JSON.parse(fs.readFileSync(indexPath, 'utf8'));
const entries = Object.values(index.entries || {}).filter(e => e.type === 'story');
let candidates = entries.filter(e => /new\s*westside|westside|editorial/i.test(`${e.title || ''} ${e.name || ''} ${e.id || ''}`));
if (!candidates.length) candidates = entries;

const server = spawn('python3', ['-m', 'http.server', '6106', '--bind', '127.0.0.1', '--directory', staticDir], { stdio: 'ignore' });
await sleep(900);

const result = {
  schema: 'dore.storybook-evidence.v1',
  created_at: new Date().toISOString(),
  source: 'Storybook static build + Playwright Chromium',
  candidates: [],
  gates: {},
};

let browser;
try {
  browser = await chromium.launch({ headless: true });
  for (const entry of candidates) {
    const story = { id: entry.id, title: entry.title, name: entry.name, viewports: {} };
    for (const vp of [
      { name: 'desktop', width: 1440, height: 1000 },
      { name: 'mobile', width: 390, height: 844 },
    ]) {
      const page = await browser.newPage({ viewport: { width: vp.width, height: vp.height } });
      const consoleErrors = [];
      const pageErrors = [];
      page.on('console', m => { if (m.type() === 'error') consoleErrors.push(m.text()); });
      page.on('pageerror', e => pageErrors.push(String(e)));
      const url = `http://127.0.0.1:6106/iframe.html?id=${encodeURIComponent(entry.id)}&viewMode=story`;
      await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
      await page.waitForTimeout(300);
      const metrics = await page.evaluate(() => {
        const body = document.body;
        const all = [...document.querySelectorAll('*')];
        const colors = [...new Set(all.slice(0, 250).flatMap(el => {
          const s = getComputedStyle(el);
          return [s.color, s.backgroundColor, s.borderColor].filter(Boolean);
        }))];
        const text = body?.innerText || '';
        return {
          text_length: text.trim().length,
          headings: document.querySelectorAll('h1,h2,h3').length,
          links: document.querySelectorAll('a').length,
          buttons: document.querySelectorAll('button').length,
          images: document.querySelectorAll('img,svg').length,
          horizontal_overflow: body ? body.scrollWidth > innerWidth + 2 : false,
          westside_text_signal: /(西區|西望|守望|黎明|Westside|Watch|Dawn)/i.test(text),
          brand_color_signal: colors.some(c => /rgb\(179, 154, 71\)|rgb\(11, 38, 57\)|rgb\(30, 33, 31\)|rgb\(242, 238, 228\)/.test(c)),
        };
      });
      const shot1 = await page.screenshot({ fullPage: true });
      await page.waitForTimeout(250);
      const shot2 = await page.screenshot({ fullPage: true });
      const file = `${entry.id}-${vp.name}.png`.replace(/[^a-zA-Z0-9._-]+/g, '-');
      fs.writeFileSync(path.join(evidenceDir, file), shot1);
      story.viewports[vp.name] = {
        viewport: [vp.width, vp.height],
        screenshot: file,
        sha256: sha(shot1),
        repeat_sha256: sha(shot2),
        visual_stable: sha(shot1) === sha(shot2),
        function_pass: metrics.text_length > 0 && consoleErrors.length === 0 && pageErrors.length === 0,
        responsive_pass: !metrics.horizontal_overflow,
        console_errors: consoleErrors.slice(0, 10),
        page_errors: pageErrors.slice(0, 10),
        metrics,
      };
      await page.close();
    }
    result.candidates.push(story);
  }
} catch (error) {
  result.browser_error = String(error?.stack || error);
} finally {
  if (browser) await browser.close();
  server.kill('SIGTERM');
}

const desktopHashes = result.candidates.map(x => x.viewports?.desktop?.sha256).filter(Boolean);
const distinctCount = new Set(desktopHashes).size;
const allViews = result.candidates.flatMap(x => Object.values(x.viewports || {}));
const fitSignals = result.candidates.map(x => {
  const views = Object.values(x.viewports || {});
  return views.some(v => v.metrics?.westside_text_signal) && views.some(v => v.metrics?.brand_color_signal);
});
result.gates = {
  BUILD_PASS: true,
  FUNCTION_PASS: allViews.length > 0 && allViews.every(v => v.function_pass),
  A11Y_PASS: 'delegated_to_storybook_vitest_addon',
  VISUAL_STABLE: allViews.length > 0 && allViews.every(v => v.visual_stable),
  RESPONSIVE_PASS: allViews.length > 0 && allViews.every(v => v.responsive_pass),
  DESIGN_DISTINCT: result.candidates.length >= 3 ? distinctCount >= 3 : 'INSUFFICIENT_CANDIDATES',
  WESTSIDE_FIT: fitSignals.length > 0 && fitSignals.every(Boolean),
};
result.summary = {
  candidate_count: result.candidates.length,
  distinct_desktop_screenshots: distinctCount,
  evidence_dir: evidenceDir,
  browser_ok: !result.browser_error,
};
result.ok = !result.browser_error && result.gates.FUNCTION_PASS && result.gates.VISUAL_STABLE && result.gates.RESPONSIVE_PASS;
const latest = path.join(evidenceDir, 'latest.json');
fs.writeFileSync(latest, JSON.stringify(result, null, 2));
console.log(JSON.stringify({ ok: result.ok, evidence: latest, gates: result.gates, summary: result.summary }));
process.exit(result.ok ? 0 : 3);
