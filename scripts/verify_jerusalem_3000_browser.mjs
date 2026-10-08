import assert from 'node:assert/strict';
import { chromium } from 'playwright';
import { mkdir, writeFile } from 'node:fs/promises';
const output = process.env.J3K_OUTPUT || 'work/j3k-validation';
await mkdir(output, { recursive: true });
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({
  viewport: { width: 1440, height: 1000 },
  reducedMotion: 'reduce',
});
const errors = [];
page.on('pageerror', (e) => errors.push(String(e)));
page.on('console', (m) => {
  if (m.type() === 'error') errors.push(m.text());
});
const reports = [];
try {
  await page.goto(
    process.env.J3K_URL || 'http://127.0.0.1:8765/preview/jerusalem-3000/',
    { waitUntil: 'networkidle' },
  );
  await page.waitForFunction(() =>
    ['ready', 'error', 'render-error'].includes(
      window.__JERUSALEM3000__?.status,
    ),
  );
  const runtime = await page.evaluate(() => window.__JERUSALEM3000__);
  assert.equal(runtime.status, 'ready', JSON.stringify(runtime));
  assert.equal(
    runtime.production.ok,
    true,
    JSON.stringify(runtime.production),
  );
  assert.equal(runtime.productionReady, runtime.production.ok && runtime.phaseAudit.complete);
  assert.equal(
    runtime.complete,
    false,
    'a verified slice must not claim the whole timeline is complete',
  );
  for (const value of [8, 8.9, 9, 9.5, 9.9, 9.5, 8]) {
    await page.locator('.j3k-scrubber').evaluate((el, value) => {
      el.value = String(value);
      el.dispatchEvent(new Event('input', { bubbles: true }));
    }, value);
    await page.waitForFunction(
      (value) =>
        window.__JERUSALEM3000__?.historicalTime?.position === value &&
        window.__JERUSALEM3000__?.renderDiagnostics?.cityProjection?.phaseId ===
          window.__JERUSALEM3000__?.historicalTime?.phase &&
        window.__JERUSALEM3000__?.renderDiagnostics?.cityProjection?.ruin ===
          window.__JERUSALEM3000__?.historicalTime?.ruin,
      value,
    );
    const state = await page.evaluate(() => ({
      time: window.__JERUSALEM3000__.historicalTime,
      render: window.__JERUSALEM3000__.renderDiagnostics,
      inheritance: window.__JERUSALEM3000__.inheritanceState,
    }));
    assert.ok(state.render.webgl && state.render.frames > 0);
    assert.ok(state.render.cityProjection.visibleBuildings > 0);
    assert.equal(
      state.render.cityProjection.visibleBuildings,
      runtime.evidenceObjects.cityCoreAB.buildings,
    );
    assert.equal(state.render.visibleLegacyTemporalMeshes, 0);
    assert.equal(state.inheritance.active, false);
    reports.push({ value, ...state });
    if ([8, 9.5, 9.9].includes(value))
      await page.screenshot({
        path: `${output}/city-${value}.png`,
        fullPage: true,
      });
  }
  assert.equal(
    reports[0].render.cityProjection.transformFingerprint,
    reports.at(-1).render.cityProjection.transformFingerprint,
    'all actual mesh transforms must recover exactly',
  );
  assert.equal(
    new Set(reports.map((r) => r.render.cityProjection.identityFingerprint))
      .size,
    1,
    'actual building identities must persist',
  );
  assert.notEqual(
    reports[0].render.cityProjection.transformFingerprint,
    reports[3].render.cityProjection.transformFingerprint,
    'destruction must change rendered geometry',
  );
  await page.getByRole('button', { name: '實證', exact: true }).click();
  await page.waitForFunction(
    () =>
      window.__JERUSALEM3000__.renderDiagnostics?.cityProjection
        ?.visibleBuildings === 0,
  );
  await page.getByRole('button', { name: '全部', exact: true }).click();
  await page.waitForFunction(
    () =>
      window.__JERUSALEM3000__.renderDiagnostics?.cityProjection
        ?.visibleBuildings > 0,
  );
  // Render every era separately. Startup metadata is not proof of a visible city.
  const phaseReports = [];
  for (let phase = 0; phase < runtime.phaseAudit.records.length; phase++) {
    const value = phase + (phase === runtime.phaseAudit.records.length - 1 ? 0 : 0.9);
    const started = Date.now();
    await page.locator('.j3k-scrubber').evaluate((el, value) => {
      el.value = String(value);
      el.dispatchEvent(new Event('input', { bubbles: true }));
    }, value);
    await page.waitForFunction(value => {
      const s = window.__JERUSALEM3000__;
      return s?.historicalTime?.position === value &&
        s.renderDiagnostics?.phase === s.historicalTime.phase;
    }, value, { timeout: 15000 });
    const sample = await page.evaluate(() => ({
      time: window.__JERUSALEM3000__.historicalTime,
      render: window.__JERUSALEM3000__.renderDiagnostics,
    }));
    assert.ok(sample.render.webgl && sample.render.frames > 0);
    const visible = sample.render.visibleCoreMeshes +
      sample.render.urbanFabric.phase2Components + sample.render.visibleLegacyTemporalMeshes;
    assert.ok(visible > 0, `No urban geometry rendered for ${sample.time.phase}`);
    if (phase === 10) assert.equal(sample.render.visibleCoreMeshes, 0,
      'Aelia must not reuse standing Herodian architecture');
    phaseReports.push({ value, elapsedMs: Date.now() - started, visible, ...sample });
    await page.screenshot({ path: `${output}/phase-${phase}.png`, fullPage: true });
  }
  await writeFile(`${output}/phase-report.json`, JSON.stringify({
    scope: 'render-smoke-only; historical continuity remains unverified',
    phaseAudit: runtime.phaseAudit, phaseReports,
  }, null, 2));
  assert.deepEqual(errors, []);
  const mobile = await browser.newPage({
    viewport: { width: 390, height: 844 },
    isMobile: true,
    hasTouch: true,
    reducedMotion: 'reduce',
  });
  await mobile.goto(page.url(), { waitUntil: 'networkidle' });
  await mobile.waitForFunction(
    () => window.__JERUSALEM3000__?.status === 'ready',
  );
  await mobile.getByRole('button', { name: '耶穌時代', exact: false }).click();
  await mobile.waitForFunction(
    () =>
      window.__JERUSALEM3000__?.renderDiagnostics?.cityProjection
        ?.visibleBuildings > 0,
  );
  assert.equal(
    await mobile.evaluate(() => window.__JERUSALEM3000__.production.ok),
    true,
  );
  await mobile.screenshot({
    path: `${output}/city-mobile.png`,
    fullPage: true,
  });
  await mobile.close();
  const broken = await browser.newPage();
  await broken.route('**/data/urban/herodian-30ce.registration.json', (route) =>
    route.fulfill({ status: 503, body: 'unavailable' }),
  );
  await broken.goto(page.url(), { waitUntil: 'networkidle' });
  await broken.waitForFunction(
    () => window.__JERUSALEM3000__?.status === 'error',
  );
  const failed = await broken.evaluate(() => window.__JERUSALEM3000__);
  assert.equal(failed.productionReady, false);
  assert.match(failed.error, /Canonical city construction failed/);
  await broken.close();
  await writeFile(
    `${output}/report.json`,
    JSON.stringify(
      { ok: true, core: runtime.evidenceObjects.cityCoreAB, phaseReports, reports, errors },
      null,
      2,
    ),
  );
  console.log(
    JSON.stringify({
      ok: true,
      buildings: runtime.evidenceObjects.cityCoreAB.buildings,
      samples: reports.length,
      renderedPhases: phaseReports.length,
      fullTimelineReady: runtime.productionReady,
      errors,
    }),
  );
} catch (error) {
  await page
    .screenshot({ path: `${output}/failure.png`, fullPage: true })
    .catch(() => {});
  await writeFile(
    `${output}/report.json`,
    JSON.stringify(
      {
        ok: false,
        error: String(error),
        errors,
        runtime: await page
          .evaluate(() => window.__JERUSALEM3000__)
          .catch(() => null),
      },
      null,
      2,
    ),
  );
  throw error;
} finally {
  await browser.close();
}
