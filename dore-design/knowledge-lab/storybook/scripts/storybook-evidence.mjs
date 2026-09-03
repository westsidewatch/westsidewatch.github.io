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
const benignConsole = text => /favicon|download the react devtools|failed to load resource.*404/i.test(text || '');

if (!fs.existsSync(indexPath)) {
  console.error(JSON.stringify({ ok: false, infrastructure_ok: false, error: 'storybook-static/index.json missing; build Storybook first' }));
  process.exit(2);
}

const index = JSON.parse(fs.readFileSync(indexPath, 'utf8'));
const entries = Object.values(index.entries || {}).filter(e => e.type === 'story');
let candidates = entries.filter(e => /new\s*westside|westside|editorial/i.test(`${e.title || ''} ${e.name || ''} ${e.id || ''}`));
if (!candidates.length) candidates = entries;

// Resident and canonical loops may overlap. A fixed port lets one run kill or
// replace another run's evidence server, producing a false infrastructure FAIL.
const evidencePort = Number(process.env.DORE_STORYBOOK_EVIDENCE_PORT || (16000 + (process.pid % 20000)));
const evidenceOrigin = `http://127.0.0.1:${evidencePort}`;
const server = spawn('python3', ['-m', 'http.server', String(evidencePort), '--bind', '127.0.0.1', '--directory', staticDir], { stdio: 'ignore' });
let serverReady = false;
for (let attempt = 0; attempt < 30; attempt += 1) {
  if (server.exitCode !== null) break;
  try {
    const response = await fetch(`${evidenceOrigin}/index.json`);
    if (response.ok) { serverReady = true; break; }
  } catch {}
  await sleep(100);
}

const result = {
  schema: 'dore.storybook-evidence.v1.3',
  created_at: new Date().toISOString(),
  source: 'Storybook static build + Playwright Chromium',
  purpose: 'Observation layer. Design-gate failures are learning signals, not evidence-infrastructure failures.',
  candidates: [],
  gates: {},
};

let browser;
try {
  if (!serverReady) throw new Error(`storybook_evidence_server_not_ready:exit=${server.exitCode}`);
  browser = await chromium.launch({ headless: true });
  for (const entry of candidates) {
    const story = { id: entry.id, title: entry.title, name: entry.name, westside_candidate: /new\s*westside|westside/i.test(`${entry.title || ''} ${entry.name || ''} ${entry.id || ''}`), viewports: {} };
    for (const vp of [
      { name: 'desktop', width: 1440, height: 1000 },
      { name: 'mobile', width: 390, height: 844 },
    ]) {
      const page = await browser.newPage({ viewport: { width: vp.width, height: vp.height }, reducedMotion: 'reduce' });
      const consoleErrors = [];
      const pageErrors = [];
      page.on('console', m => { if (m.type() === 'error' && !benignConsole(m.text())) consoleErrors.push(m.text()); });
      page.on('pageerror', e => pageErrors.push(String(e)));
      const url = `${evidenceOrigin}/iframe.html?id=${encodeURIComponent(entry.id)}&viewMode=story`;
      await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
      const freeze = '*,*::before,*::after{animation:none!important;transition:none!important;caret-color:transparent!important}html{scroll-behavior:auto!important}';
      for (const frame of page.frames()) await frame.addStyleTag({ content: freeze }).catch(() => {});
      await page.waitForTimeout(150);
      const contentFrame = page.frames().find(frame => frame !== page.mainFrame() && /^https?:\/\//.test(frame.url()));
      const observedFrame = contentFrame || page.mainFrame();
      const metrics = await observedFrame.evaluate(() => {
        const body = document.body;
        const all = [...document.querySelectorAll('*')];
        const colors = [...new Set(all.slice(0, 300).flatMap(el => {
          const s = getComputedStyle(el);
          return [s.color, s.backgroundColor, s.borderColor].filter(Boolean);
        }))];
        const text = body?.innerText || '';
        const iframes = [...document.querySelectorAll('iframe')];
        return {
          text_length: text.trim().length,
          headings: document.querySelectorAll('h1,h2,h3').length,
          links: document.querySelectorAll('a').length,
          buttons: document.querySelectorAll('button').length,
          images: document.querySelectorAll('img,svg').length,
          iframes: iframes.length,
          iframe_srcs: iframes.map(x => x.getAttribute('src')).filter(Boolean),
          observed_url: location.href,
          horizontal_overflow: body ? body.scrollWidth > innerWidth + 2 : false,
          westside_text_signal: /(西區|西望|守望|黎明|Westside|Watch|Dawn)/i.test(text),
          brand_color_signal: colors.some(c => /rgb\(179, 154, 71\)|rgb\(11, 38, 57\)|rgb\(30, 33, 31\)|rgb\(242, 238, 228\)/.test(c)),
          editorial_system_signal: Boolean(document.querySelector('h1,.display')) && Boolean(document.querySelector('.micro,h2')),
        };
      });
      const shot1 = await page.screenshot({ fullPage: true, animations: 'disabled', caret: 'hide' });
      await page.waitForTimeout(120);
      const shot2 = await page.screenshot({ fullPage: true, animations: 'disabled', caret: 'hide' });
      const file = `${entry.id}-${vp.name}.png`.replace(/[^a-zA-Z0-9._-]+/g, '-');
      fs.writeFileSync(path.join(evidenceDir, file), shot1);
      const renderedContent = metrics.text_length > 0 || (metrics.iframes > 0 && metrics.iframe_srcs.length > 0);
      story.viewports[vp.name] = {
        viewport: [vp.width, vp.height],
        screenshot: file,
        sha256: sha(shot1),
        repeat_sha256: sha(shot2),
        visual_stable: sha(shot1) === sha(shot2),
        render_pass: renderedContent && pageErrors.length === 0,
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
const allViews = result.candidates.flatMap(x => Object.entries(x.viewports || {}).map(([viewport, v]) => ({ story_id: x.id, viewport, ...v })));
const westsideCandidates = result.candidates.filter(x => x.westside_candidate);
const fitSignals = westsideCandidates.map(x => {
  const views = Object.values(x.viewports || {});
  return views.some(v => v.metrics?.westside_text_signal) && views.some(v => v.metrics?.brand_color_signal || v.metrics?.editorial_system_signal);
});
const failedRender = allViews.filter(v => !v.render_pass).map(v => ({ story_id: v.story_id, viewport: v.viewport, text_length: v.metrics?.text_length, iframes: v.metrics?.iframes, iframe_srcs: v.metrics?.iframe_srcs, page_errors: v.page_errors, console_errors: v.console_errors }));
const unstable = allViews.filter(v => !v.visual_stable).map(v => ({ story_id: v.story_id, viewport: v.viewport, sha256: v.sha256, repeat_sha256: v.repeat_sha256 }));
result.gates = {
  BUILD_PASS: true,
  RENDER_PASS: allViews.length > 0 && failedRender.length === 0,
  FUNCTION_PASS: 'authoritative_in_vitest',
  A11Y_PASS: 'authoritative_in_storybook_vitest_addon',
  VISUAL_STABLE: allViews.length > 0 && unstable.length === 0,
  RESPONSIVE_PASS: allViews.length > 0 && allViews.every(v => v.responsive_pass),
  DESIGN_DISTINCT: result.candidates.length >= 3 ? distinctCount >= 3 : 'INSUFFICIENT_CANDIDATES',
  WESTSIDE_FIT: fitSignals.length > 0 && fitSignals.every(Boolean),
};
result.summary = {
  candidate_count: result.candidates.length,
  westside_candidate_count: westsideCandidates.length,
  distinct_desktop_screenshots: distinctCount,
  stable_viewports: allViews.length - unstable.length,
  total_viewports: allViews.length,
  failed_render: failedRender,
  unstable_viewports: unstable,
  evidence_dir: evidenceDir,
  browser_ok: !result.browser_error,
};
// A failing design candidate is evidence for rejection, not an infrastructure
// outage. Keep the run alive so individually qualified candidates can graduate.
result.infrastructure_ok = !result.browser_error && result.gates.RENDER_PASS;
result.ok = result.infrastructure_ok;
const latest = path.join(evidenceDir, 'latest.json');
fs.writeFileSync(latest, JSON.stringify(result, null, 2));
console.log(JSON.stringify({ ok: result.ok, infrastructure_ok: result.infrastructure_ok, evidence: latest, gates: result.gates, summary: result.summary }));
process.exit(result.infrastructure_ok ? 0 : 3);
