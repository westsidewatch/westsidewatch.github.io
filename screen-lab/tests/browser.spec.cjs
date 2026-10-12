const { test, expect, devices } = require('@playwright/test');
const url = 'http://127.0.0.1:8765/screen-lab/';
for (const [name, viewport] of [
  ['desktop', { width: 1440, height: 900 }],
  ['mobile', { width: 390, height: 844 }]
]) {
  test(name + ': curated catalog, layout, search and player lifecycle', async ({ browser }, testInfo) => {
    const context = await browser.newContext({ viewport, isMobile: name === 'mobile', hasTouch: name === 'mobile' });
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    await page.goto(url, { waitUntil: 'domcontentloaded' });
    await expect(page.locator('#count')).toHaveText('6 TITLES');
    await expect(page.locator('#grid .tile')).toHaveCount(6);
    await expect(page.locator('#catalog-status')).toContainText('6 部');
    const width = await page.evaluate(() => ({ scroll: document.documentElement.scrollWidth, client: document.documentElement.clientWidth }));
    expect(width.scroll, 'horizontal overflow').toBeLessThanOrEqual(width.client + 2);
    await page.screenshot({ path: testInfo.outputPath(name + '-catalog.png'), fullPage: true });
    await page.locator('#search').fill('Sintel');
    await expect(page.locator('#grid .tile')).toHaveCount(1);
    await page.locator('#search').fill('');
    await page.locator('#grid .tile').filter({ hasText: 'Big Buck Bunny' }).click();
    await expect(page.locator('#detail')).toBeVisible();
    await expect(page.getByText('海報來源 ↗')).toBeVisible();
    await page.getByRole('button', { name: /試播 Blender 官方影片/ }).click();
    const frame = page.locator('#detail iframe');
    await expect(frame).toHaveCount(1);
    await expect(frame).toHaveAttribute('src', /^https:\/\/video\.blender\.org\/videos\/embed\//);
    await page.screenshot({ path: testInfo.outputPath(name + '-player.png') });
    await page.getByRole('button', { name: '關閉 ×' }).click();
    await expect(frame).toHaveCount(0);
    await expect(page.locator('#detail')).not.toBeVisible();
    expect(errors, 'uncaught page JavaScript errors').toEqual([]);
    await context.close();
  });
}
test('remote poster load is observed but does not masquerade as a passing playback check', async ({ page }, testInfo) => {
  await page.goto(url, { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#grid .tile')).toHaveCount(6);
  const image = page.locator('.tile').filter({ hasText: 'Big Buck Bunny' }).locator('img');
  await image.scrollIntoViewIfNeeded().catch(() => {});
  await page.waitForTimeout(5000);
  const loaded = await image.count() && await image.evaluate(img => img.complete && img.naturalWidth > 0).catch(() => false);
  console.log('REMOTE_POSTER_LOAD=' + (loaded ? 'PASS' : 'UNVERIFIED_OR_FAILED'));
  await page.screenshot({ path: testInfo.outputPath('poster-status.png') });
});

test('Blender PeerTube playback readiness is independently reported', async ({ page }, testInfo) => {
  await page.goto(url, { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#grid .tile')).toHaveCount(6);
  await page.locator('#grid .tile').filter({ hasText: 'Big Buck Bunny' }).click();
  await page.getByRole('button', { name: /試播 Blender 官方影片/ }).click();
  const iframe = page.locator('#detail iframe');
  await expect(iframe).toBeVisible();
  let status = 'UNVERIFIED';
  try {
    const response = await page.request.get(await iframe.getAttribute('src'), { timeout: 12000 });
    status = response.ok() ? 'EMBED_ENDPOINT_OK_NOT_PLAYBACK' : 'EMBED_HTTP_' + response.status();
  } catch (err) { status = 'EMBED_REQUEST_ERROR'; }
  console.log('PEERTUBE_PLAYBACK_STATUS=' + status);
  await testInfo.attach('peertube-endpoint-status', { body: status + '\\n', contentType: 'text/plain' });
  let playback = 'NOT_CONFIRMED';
  try {
    const video = page.frameLocator('#detail iframe').locator('video').first();
    await video.waitFor({ state: 'attached', timeout: 8000 });
    const before = await video.evaluate(v => v.currentTime);
    await video.evaluate(v => v.play().catch(() => {}));
    await page.waitForTimeout(4500);
    const after = await video.evaluate(v => ({ time: v.currentTime, paused: v.paused, ready: v.readyState }));
    if (!after.paused && after.ready >= 2 && after.time > before + 0.5) playback = 'PLAYING_CONFIRMED';
    else playback = 'NOT_CONFIRMED paused=' + after.paused + ' ready=' + after.ready;
  } catch (err) { playback = 'NOT_CONFIRMED ' + String(err.message).slice(0,180); }
  console.log('PEERTUBE_REAL_PLAYBACK=' + playback);
  await testInfo.attach('peertube-real-playback', { body: playback, contentType: 'text/plain' });
  if (process.env.SCREEN_LAB_REQUIRE_PLAYBACK === '1') expect(playback, 'Real playback must advance video.currentTime').toBe('PLAYING_CONFIRMED');
  await page.screenshot({ path: testInfo.outputPath('peertube-embed.png') });
  await page.getByRole('button', { name: '關閉 ×' }).click();
  await expect(iframe).toHaveCount(0);
});
