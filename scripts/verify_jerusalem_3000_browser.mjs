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
const dataRequests=new Map();
page.on('request',r=>{const path=new URL(r.url()).pathname;dataRequests.set(path,(dataRequests.get(path)||0)+1);});
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
  assert.equal(runtime.cityFoundationIndex.length,18);
  assert.ok(runtime.cityFoundationIndex.every(p=>p.terrain.sampling==='rendered-dem-triangles'&&p.foundationAccepted===false));
  const inactiveFoundation=await page.evaluate(()=>window.__JERUSALEM3000__.inspectCityFoundation('modern'));
  assert.equal(inactiveFoundation.renderer.visibleComponents,null,'inactive inspection must not generate a future city');

  for(const path of ['anchor-era-packs.json','lifecycle/anchor-era.lifecycle.json','lifecycle/herodian-30ce.lifecycle.json','objects/herodian-30ce.json','urban/herodian-30ce.registration.json','settlement/david-solomon.v1.json','urban/first-temple-persian.spatial.v1.json','urban/water-defense.registration.v1.json','urban/water-defense.local-plans.v1.json','urban/roman-byzantine-islamic.skeleton.v1.json']) {
    assert.equal(dataRequests.get(`/preview/jerusalem-3000/data/${path}`),1,`one shared request for ${path}`);
  }
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
  const terrainButton=page.getByRole('button',{name:'山城地形',exact:true});
  await terrainButton.click();
  await page.waitForFunction(()=>window.__JERUSALEM3000__.renderDiagnostics?.terrainPresentation?.overviewActive);
  const terrainView=await page.evaluate(()=>window.__JERUSALEM3000__.renderDiagnostics.terrainPresentation);
  assert.equal(terrainView.verticalScale,1);assert.ok(terrainView.contourSegments>100);
  for(const value of [3.9,4.9,8,10,17]){
    await page.locator('.j3k-scrubber').evaluate((el,v)=>{el.value=String(v);el.dispatchEvent(new Event('input',{bubbles:true}));},value);
    await page.waitForFunction(v=>window.__JERUSALEM3000__.historicalTime.position===v,value);
    await page.waitForTimeout(150);
    const current=await page.evaluate(()=>window.__JERUSALEM3000__.renderDiagnostics.terrainPresentation);
    assert.equal(current.overviewActive,true);current.camera.forEach((v,i)=>assert.ok(Math.abs(v-terrainView.camera[i])<.01,'terrain comparison camera must persist across phases'));
    if(value===4.9){await page.waitForFunction(()=>window.__JERUSALEM3000__.renderDiagnostics.sharedEra?.status==='ready',null,{timeout:60000});await page.screenshot({path:`${output}/mountain-city-overview.png`,fullPage:true});}
  }
  await terrainButton.click();
  await page.waitForFunction(()=>!window.__JERUSALEM3000__.renderDiagnostics.terrainPresentation.overviewActive);
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
    assert.equal(state.render.evidenceProjection.objects,6);
    const fate=await page.evaluate(()=>window.__JERUSALEM3000__.temporalCityState.objects.find(o=>o.id==='j3k:object:inner-temple')?.state);assert.equal(fate,value<9?'build':'ruin');
    assert.equal(await page.evaluate(()=>window.__JERUSALEM3000__.temporalCityState.objects.find(o=>o.id==='j3k:object:eastern-entry-unknown')?.state),'withheld');
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
  assert.equal(new Set(reports.map(r=>r.render.evidenceProjection.identityFingerprint)).size,1);
  assert.equal(reports[0].render.evidenceProjection.transformFingerprint,reports.at(-1).render.evidenceProjection.transformFingerprint);
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
  // The earliest phase is a geographically anchored small settlement, not a
  // scaled Herodian street/parcel city.
  await page.locator('.j3k-scrubber').evaluate(el=>{el.value='0.9';el.dispatchEvent(new Event('input',{bubbles:true}));});
  await page.waitForFunction(()=>window.__JERUSALEM3000__.renderDiagnostics.earliestSettlement?.visibleHouses===14);
  assert.match(await page.locator('.j3k-terrain-badge').textContent(),/推定/);
  const early=await page.evaluate(()=>({render:window.__JERUSALEM3000__.renderDiagnostics,inheritance:window.__JERUSALEM3000__.inheritanceState}));
  assert.equal(early.render.urbanFabric.phase2Components,0);
  assert.equal(early.render.visibleLegacyTemporalMeshes,0);
  assert.equal(early.inheritance.active,false);
  assert.equal(early.render.earliestSettlement.historicalFootprintsVerified,false);
  await page.screenshot({path:`${output}/earliest-settlement.png`,fullPage:true});
  await page.getByRole('button',{name:'實證',exact:true}).click();
  await page.waitForFunction(()=>window.__JERUSALEM3000__.renderDiagnostics.earliestSettlement.visibleHouses===0);
  await page.getByRole('button',{name:'全部',exact:true}).click();
  await page.waitForFunction(()=>window.__JERUSALEM3000__.renderDiagnostics.earliestSettlement.visibleHouses===14);
  await writeFile(`${output}/earliest-report.json`,JSON.stringify(early,null,2));
  await page.locator('.j3k-scrubber').evaluate(el=>{el.value='1.9';el.dispatchEvent(new Event('input',{bubbles:true}));});
  await page.waitForFunction(()=>window.__JERUSALEM3000__.renderDiagnostics.middleBronzeSettlement?.visibleHouses===24);
  const bronze=await page.evaluate(()=>window.__JERUSALEM3000__.renderDiagnostics);
  assert.equal(bronze.earliestSettlement.visibleHouses,0);
  assert.equal(bronze.urbanFabric.phase2Components,0);
  assert.equal(bronze.visibleLegacyTemporalMeshes,0);
  assert.ok(bronze.middleBronzeSettlement.visibleTowerComponents>0);
  assert.equal(await page.evaluate(()=>window.__JERUSALEM3000__.inheritanceState.active),false);
  await page.screenshot({path:`${output}/middle-bronze.png`,fullPage:true});
  await page.getByRole('button',{name:'Evidence',exact:true}).click();
  const towerSelect=page.getByLabel('泉塔年代方案',{exact:true});
  await towerSelect.selectOption('iron-age-dating');
  await page.waitForFunction(()=>window.__JERUSALEM3000__.renderDiagnostics.waterDefenseModel.visibleTowerComponents===0);
  await towerSelect.selectOption('middle-bronze-hypothesis');
  await page.waitForFunction(()=>window.__JERUSALEM3000__.renderDiagnostics.waterDefenseModel.visibleTowerComponents>0);
  await page.locator('[data-water-defense]').evaluate(el=>el.scrollIntoView({block:'start'}));
  await page.screenshot({path:`${output}/water-defense-variant.png`,fullPage:true});
  await page.getByRole('button',{name:'Evidence',exact:true}).click();

  await page.getByRole('button',{name:'推定',exact:true}).click();
  await page.waitForFunction(()=>window.__JERUSALEM3000__.renderDiagnostics.middleBronzeSettlement.visibleTowerComponents===0);
  assert.ok(await page.evaluate(()=>window.__JERUSALEM3000__.renderDiagnostics.middleBronzeSettlement.visibleDefenseComponents>0));
  await page.getByRole('button',{name:'實證',exact:true}).click();
  await page.waitForFunction(()=>window.__JERUSALEM3000__.renderDiagnostics.middleBronzeSettlement.visibleDefenseComponents===0);
  await page.getByRole('button',{name:'全部',exact:true}).click();
  await page.waitForFunction(()=>window.__JERUSALEM3000__.renderDiagnostics.middleBronzeSettlement.visibleTowerComponents>0);
  await page.locator('.j3k-scrubber').evaluate(el=>{el.value='0.9';el.dispatchEvent(new Event('input',{bubbles:true}));});
  await page.waitForFunction(()=>window.__JERUSALEM3000__.renderDiagnostics.earliestSettlement.visibleHouses===14);
  assert.equal(await page.evaluate(()=>window.__JERUSALEM3000__.renderDiagnostics.middleBronzeSettlement.visibleDefenseComponents),0);
  await writeFile(`${output}/middle-bronze-report.json`,JSON.stringify(bronze,null,2));
  await page.locator('.j3k-scrubber').evaluate(el=>{el.value='2.9';el.dispatchEvent(new Event('input',{bubbles:true}));});
  await page.waitForFunction(()=>window.__JERUSALEM3000__.renderDiagnostics.lateBronzeSettlement?.visibleSupportComponents===8);
  const late=await page.evaluate(()=>window.__JERUSALEM3000__.renderDiagnostics);
  assert.equal(late.earliestSettlement.visibleHouses,0);
  assert.equal(late.middleBronzeSettlement.visibleDefenseComponents,0);
  assert.equal(late.urbanFabric.phase2Components,0);
  assert.equal(late.visibleLegacyTemporalMeshes,0);
  assert.equal(late.lateBronzeSettlement.populationComparisonVerified,false);
  assert.equal(late.lateBronzeSettlement.houses,bronze.middleBronzeSettlement.houses);
  assert.equal(await page.evaluate(()=>window.__JERUSALEM3000__.inheritanceState.active),false);
  await page.screenshot({path:`${output}/late-bronze.png`,fullPage:true});
  await page.getByRole('button',{name:'爭議',exact:true}).click();
  await page.waitForFunction(()=>window.__JERUSALEM3000__.renderDiagnostics.lateBronzeSettlement.visibleHouses===0);
  assert.equal(await page.evaluate(()=>window.__JERUSALEM3000__.renderDiagnostics.lateBronzeSettlement.visibleSupportComponents),8);
  await page.getByRole('button',{name:'推定',exact:true}).click();
  await page.waitForFunction(()=>window.__JERUSALEM3000__.renderDiagnostics.lateBronzeSettlement.visibleSupportComponents===0);
  await page.getByRole('button',{name:'全部',exact:true}).click();
  await page.locator('.j3k-scrubber').evaluate(el=>{el.value='1.9';el.dispatchEvent(new Event('input',{bubbles:true}));});
  await page.waitForFunction(()=>window.__JERUSALEM3000__.renderDiagnostics.middleBronzeSettlement.visibleTowerComponents>0);
  assert.equal(await page.evaluate(()=>window.__JERUSALEM3000__.renderDiagnostics.lateBronzeSettlement.visibleSupportComponents),0);
  await writeFile(`${output}/late-bronze-report.json`,JSON.stringify(late,null,2));
  await page.locator('.j3k-scrubber').evaluate(el=>{el.value='3.9';el.dispatchEvent(new Event('input',{bubbles:true}));});
  await page.waitForFunction(()=>window.__JERUSALEM3000__.renderDiagnostics.davidSettlement?.visibleRoyalMarkers===1);
  const royal=await page.evaluate(()=>window.__JERUSALEM3000__.renderDiagnostics);
  assert.equal(royal.urbanFabric.phase2Components,0);
  assert.equal(royal.visibleLegacyTemporalMeshes,0);
  assert.equal(royal.lateBronzeSettlement.visibleHouses,0);
  assert.equal(royal.davidSettlement.royalBuildingGeometryVerified,false);
  assert.equal(await page.evaluate(()=>window.__JERUSALEM3000__.inheritanceState.active),false);
  await page.waitForFunction(()=>window.__JERUSALEM3000__.renderDiagnostics.royalCity?.visibleTemple>0);
  assert.equal(await page.evaluate(()=>window.__JERUSALEM3000__.renderDiagnostics.royalCity.visibleGates),9);
  assert.ok((await page.evaluate(()=>window.__JERUSALEM3000__.renderDiagnostics.royalCity.reachableDestinations)).includes('temple-entry'));
  const royalIdentity=await page.evaluate(()=>window.__JERUSALEM3000__.renderDiagnostics.royalCity.componentIdentity);
  await page.getByRole('button',{name:'城內高差',exact:true}).click();
  assert.equal(await page.locator('.j3k-royal-relief').getAttribute('data-stage'),'solomon');
  const relief=await page.evaluate(()=>window.__JERUSALEM3000__.renderDiagnostics.royalRelief);
  assert.ok(relief.deltaSouth>65&&relief.deltaMiddle>40);assert.equal(relief.verticalScale,1);assert.equal(relief.threshingFloorLocationVerified,false);
  await page.screenshot({path:`${output}/david-landscape.png`,fullPage:true});
  await page.getByRole('button',{name:'聖殿近看',exact:true}).click();
  await page.screenshot({path:`${output}/solomon-temple.png`,fullPage:true});

  await page.getByRole('button',{name:'Evidence',exact:true}).click();
  assert.equal(await page.locator('.j3k-evidence-panel a').first().getAttribute('href'),'https://cityofdavid.org.il/en/king-davids-palace-eng/');
  assert.ok(await page.locator('.j3k-evidence-panel li').count()>0,'scene-specific limitations are visible');
  await page.screenshot({path:`${output}/david-evidence.png`,fullPage:true});
  await page.getByRole('button',{name:'Evidence',exact:true}).click();
  await page.getByRole('button',{name:'推定',exact:true}).click();
  await page.waitForFunction(()=>window.__JERUSALEM3000__.renderDiagnostics.davidSettlement.visibleRoyalMarkers===0);
  await page.getByRole('button',{name:'全部',exact:true}).click();
  await page.locator('.j3k-scrubber').evaluate(el=>{el.value='2.9';el.dispatchEvent(new Event('input',{bubbles:true}));});
  await page.waitForFunction(()=>window.__JERUSALEM3000__.renderDiagnostics.lateBronzeSettlement.visibleSupportComponents===8);
  assert.equal(await page.evaluate(()=>window.__JERUSALEM3000__.renderDiagnostics.davidSettlement.visibleRoyalMarkers),0);
  await writeFile(`${output}/david-report.json`,JSON.stringify(royal,null,2));


  // Leave immediately while generation is pending: switching must not wait
  // for thousands of architectural components, and stale work must be cancelled.
  await page.locator('.j3k-scrubber').evaluate(el => {
    for (const value of [4, 17]) {
      el.value = String(value); el.dispatchEvent(new Event('input', { bubbles: true }));
    }
  });
  await page.waitForFunction(() => window.__JERUSALEM3000__.renderDiagnostics?.phase === 'modern');
  const sharedReports = [];
  await page.locator('.j3k-scrubber').evaluate(el=>{el.value='4.9';el.dispatchEvent(new Event('input',{bubbles:true}));});
  await page.getByRole('button',{name:'Evidence',exact:true}).click();
  assert.ok((await page.locator('.j3k-evidence-panel a').first().getAttribute('href')).includes('whitelevy.fas.harvard.edu'));
  assert.ok((await page.locator('.j3k-evidence-panel').textContent()).includes('獨立推定配置'));
  await page.screenshot({path:`${output}/first-temple-evidence.png`,fullPage:true});
  await page.getByRole('button',{name:'Evidence',exact:true}).click();
  for(const [value,expected] of [[3.2,'absent'],[3.9,'build'],[4.9,'transform'],[5.5,'ruin'],[6.5,'unresolved'],[3.2,'absent']]) {
    await page.locator('.j3k-scrubber').evaluate((el,v)=>{el.value=String(v);el.dispatchEvent(new Event('input',{bubbles:true}));},value);
    assert.equal(await page.locator('[data-continuity-object="j3k:object:first-temple"]').getAttribute('data-state'),expected);
    const objects=await page.evaluate(()=>window.__JERUSALEM3000__.temporalCityState.objects);
    assert.equal(objects.find(o=>o.id==='j3k:object:first-temple').state,expected);
    if(value===6.5)assert.equal(objects.find(o=>o.id==='j3k:object:second-temple-early').state,'rebuild');
    await page.waitForFunction(expected=>window.__JERUSALEM3000__.renderDiagnostics.royalCity?.templeState===expected,expected);
    const geometry=await page.evaluate(()=>window.__JERUSALEM3000__.renderDiagnostics.royalCity);
    assert.equal(geometry.componentIdentity,royalIdentity,'cross-era projection retains component identities');
    assert.equal(geometry.visibleTemple>0,['build','transform','ruin'].includes(expected));
    if(value===4.9)assert.equal(geometry.visibleWalls,0,'do not invent wall-segment continuity');
    if(value===5.5){assert.ok(geometry.templeCompressionFactor<1&&geometry.templeCompressionFactor>0);await page.waitForFunction(()=>window.__JERUSALEM3000__.renderDiagnostics.sharedEra?.status==='ready');await page.getByRole('button',{name:'聖殿近看',exact:true}).click();await page.screenshot({path:`${output}/temple-ruin.png`,fullPage:true});}

    if(value===3.2){assert.equal(await page.locator('.j3k-royal-relief').getAttribute('data-stage'),'david');assert.ok(await page.locator('.j3k-relief-labels').textContent().then(t=>t.includes('禾場關聯區')));await page.screenshot({path:`${output}/david-threshing-floor-relief.png`,fullPage:true});}
    if(value===4.9)assert.ok(await page.locator('.j3k-royal-relief').isHidden());
  }
  await page.locator('.j3k-scrubber').evaluate(el=>{el.value='6.5';el.dispatchEvent(new Event('input',{bubbles:true}));});
  await page.getByRole('button',{name:'Evidence',exact:true}).click();
  await page.waitForFunction(()=>window.__JERUSALEM3000__.renderDiagnostics.sharedEra?.successor?.status==='ready'&&window.__JERUSALEM3000__.renderDiagnostics.sharedEra?.status==='ready');
  await page.screenshot({path:`${output}/continuity-evidence.png`,fullPage:true});
  await page.getByRole('button',{name:'Evidence',exact:true}).click();
  for (const value of [4.9, 5, 5.5, 5.9, 4.9]) {
    await page.locator('.j3k-scrubber').evaluate((el, value) => {
      el.value = String(value); el.dispatchEvent(new Event('input', { bubbles: true }));
    }, value);
    await page.waitForFunction(value => {
      const s = window.__JERUSALEM3000__;
      return s?.historicalTime?.position === value &&
        s.renderDiagnostics?.sharedEra?.status === 'ready' &&
        s.renderDiagnostics.sharedEra.projection.phaseId === s.historicalTime.phase &&
        s.renderDiagnostics.sharedEra.projection.ruin === s.historicalTime.ruin;
    }, value, { timeout: 60000 });
    const sample = await page.evaluate(() => ({
      time: window.__JERUSALEM3000__.historicalTime,
      shared: window.__JERUSALEM3000__.renderDiagnostics.sharedEra,
      fabric: window.__JERUSALEM3000__.renderDiagnostics.urbanFabric,
      legacy: window.__JERUSALEM3000__.renderDiagnostics.visibleLegacyTemporalMeshes,
      inheritance: window.__JERUSALEM3000__.inheritanceState,
    }));
    assert.ok(sample.shared.projection.visibleBuildings > 0);
    assert.equal(sample.fabric.phase2Components, 0, 'legacy fabric must be removed after shared generation');
    assert.equal(sample.inheritance.active, false, 'do not rebuild a second inherited city');
    assert.equal(sample.legacy, 0, 'legacy temporal boxes must not overlap the shared city');
    assert.equal(sample.shared.historicalRegistrationVerified, false);
    assert.equal(sample.shared.residentialLedger.published,true);
    const chain=await page.evaluate(id=>{const inspect=window.__JERUSALEM3000__.inspectCityObject,building=inspect(id),parcel=inspect(building.source.parcelId),block=inspect(parcel.source.blockId),district=inspect(block.source.districtId);return {building,parcel,block,district};},sample.shared.residentialLedger.sampleBuildingIds[0]);
    assert.equal(chain.parcel.type,'parcel');assert.equal(chain.block.type,'block');assert.equal(chain.district.type,'district');
    assert.equal(chain.building.metadata.geometryVerified,false);
    assert.equal(chain.building.typology,'iron-age-four-room-analogy');
    assert.equal(chain.building.metadata.roofGrammar,'low-rise-open-court-flat-roof-v1');
    assert.ok(chain.building.lifecycle.events.some(e=>e.phase==='babylonian-destruction'&&e.state==='ruin'));
    assert.equal(sample.shared.projection.visibleBuildings,Object.values(sample.shared.projection.districtVisible).reduce((s,n)=>s+n,0));
    assert.equal(await page.evaluate(()=>window.__JERUSALEM3000__.renderDiagnostics.cityOverview.framePhase),'late-first-temple');
    assert.ok(sample.shared.yields > 0);
    sharedReports.push({ value, ...sample });
    await page.screenshot({ path: `${output}/shared-${value}.png`, fullPage: true });
  }
  assert.equal(new Set(sharedReports.map(r => r.shared.projection.identityFingerprint)).size, 1);
  assert.equal(sharedReports[0].shared.projection.transformFingerprint, sharedReports.at(-1).shared.projection.transformFingerprint);
  assert.notEqual(sharedReports[0].shared.projection.transformFingerprint, sharedReports[2].shared.projection.transformFingerprint);
  await page.getByRole('button', { name: '實證', exact: true }).click();
  await page.waitForFunction(() => window.__JERUSALEM3000__.renderDiagnostics.sharedEra.projection.visibleBuildings === 0);
  await page.getByRole('button', { name: '全部', exact: true }).click();
  await page.waitForFunction(() => window.__JERUSALEM3000__.renderDiagnostics.sharedEra.projection.visibleBuildings > 0);
  await writeFile(`${output}/shared-report.json`, JSON.stringify({ sharedReports }, null, 2));
  await page.getByRole('button',{name:'Evidence',exact:true}).click();
  const residentialClose=page.getByRole('button',{name:'西丘住宅近看',exact:true});
  await residentialClose.click();
  assert.equal(await page.locator('.j3k-evidence-panel').getAttribute('hidden'),'');
  await page.screenshot({path:`${output}/iron-age-residential-close.png`,fullPage:true});

  // Persian rebuilding retains the same earlier fabric as an opt-in ruin layer.
  await page.locator('.j3k-scrubber').evaluate(el => {
    for(const value of [6,17,6.5]) {el.value=String(value);el.dispatchEvent(new Event('input',{bubbles:true}));}
  });
  await page.locator('.j3k-scrubber').evaluate(el => {
    el.value = '6.5'; el.dispatchEvent(new Event('input', { bubbles: true }));
  });
  await page.waitForFunction(() => {const s=window.__JERUSALEM3000__.renderDiagnostics.sharedEra;return s.status==='ready'&&s.successor.projection?.visibleBuildings>0;},null,{timeout:60000});
  const retainedButton = page.getByRole('button', {name:'前代遺存 · 推定', exact:true});
  assert.equal(await retainedButton.getAttribute('aria-pressed'),'false');
  await retainedButton.click();
  await page.waitForFunction(() => window.__JERUSALEM3000__.renderDiagnostics.sharedEra.projection.visibleBuildings > 0);
  const retained = await page.evaluate(() => window.__JERUSALEM3000__.renderDiagnostics);
  assert.equal(retained.sharedEra.successor.residentialLedger.published,true);
  assert.equal(await page.locator('[data-district-acceptance] [data-residential-district]').count(),5);
  await page.getByRole('button',{name:'Evidence',exact:true}).click();
  await page.locator('.j3k-evidence-panel').evaluate(el=>{el.scrollTop=el.scrollHeight;});
  await page.screenshot({path:`${output}/district-ledger.png`,fullPage:true});
  await page.locator('.j3k-evidence-panel').evaluate(el=>{el.scrollTop=0;});
  await page.getByRole('button',{name:'Evidence',exact:true}).click();
  assert.equal(await page.locator('[data-water-defense-object]').count(),6);
  assert.equal(await page.locator('[data-water-defense-object="j3k:object:gihon-spring"]').getAttribute('data-state'),'transform');
  assert.ok(retained.localPlanAudit.every(entry=>entry.renderable===false));
  assert.equal(await page.locator('[data-local-plan-admission]').count(),1);
  assert.equal(retained.cityOverview.framePhase,'persian-nehemiah');
  assert.equal(retained.cityOverview.includesEarlier,true,'retained ruins must be included in overview framing');
  assert.ok(retained.persianSanctuary.visibleTemple>0);
  assert.equal(retained.persianSanctuary.visibleGate,2);
  assert.equal(retained.persianSanctuary.visibleAccess,true);
  assert.equal(retained.royalCity.visibleTemple,0);
  assert.equal(retained.sharedEra.successor.independentLayout,true);
  assert.equal(retained.sharedEra.projection.identityFingerprint, sharedReports[0].shared.projection.identityFingerprint);
  assert.equal(retained.sharedEra.projection.ruin,1);
  assert.equal(retained.sharedEra.projection.layerState,'retained-ruin');
  assert.equal(retained.sharedEra.retainedObjects, retained.sharedEra.projection.visibleBuildings);
  assert.equal(retained.urbanFabric.phase2Components,0,'legacy Persian morphology must be removed');
  assert.equal(retained.visibleLegacyTemporalMeshes,0);
  assert.ok(retained.sharedEra.successor.projection.visibleBuildings>0);
  assert.notEqual(retained.sharedEra.successor.projection.identityFingerprint,retained.sharedEra.projection.identityFingerprint);
  assert.equal(retained.sharedEra.successor.projection.ruin,0);
  assert.ok(retained.sharedEra.successor.yields>0);
  assert.equal(await page.evaluate(()=>window.__JERUSALEM3000__.inheritanceState.active),false);
  assert.equal(retained.sharedEra.projection.burialDepthVerified,false);
  assert.equal(retained.sharedEra.projection.reuseLinksVerified,false);
  await page.screenshot({path:`${output}/persian-retained.png`,fullPage:true});
  await page.getByRole('button', {name:'實證',exact:true}).click();
  await page.waitForFunction(() => window.__JERUSALEM3000__.renderDiagnostics.sharedEra.projection.visibleBuildings === 0);
  assert.equal(await page.evaluate(()=>window.__JERUSALEM3000__.renderDiagnostics.persianSanctuary.visibleTemple),0);
  await page.getByRole('button', {name:'全部',exact:true}).click();
  await page.waitForFunction(() => window.__JERUSALEM3000__.renderDiagnostics.sharedEra.projection.visibleBuildings > 0);
  await retainedButton.click();
  await page.waitForFunction(() => window.__JERUSALEM3000__.renderDiagnostics.sharedEra.projection.visibleBuildings === 0);
  const successorFingerprint=retained.sharedEra.successor.projection.transformFingerprint;
  for(const value of [4.9,6.5]) {
    await page.locator('.j3k-scrubber').evaluate((el,value)=>{el.value=String(value);el.dispatchEvent(new Event('input',{bubbles:true}));},value);
    await page.waitForFunction(value=>window.__JERUSALEM3000__.historicalTime.position===value&&window.__JERUSALEM3000__.renderDiagnostics.sharedEra.status==='ready',value);
  }
  assert.equal(await page.evaluate(()=>window.__JERUSALEM3000__.renderDiagnostics.sharedEra.successor.projection.transformFingerprint),successorFingerprint);
  assert.equal(await page.evaluate(()=>window.__JERUSALEM3000__.renderDiagnostics.cityOverview.includesEarlier),false);
  await page.screenshot({path:`${output}/persian-city.png`,fullPage:true});
  assert.equal(await page.evaluate(()=>window.__JERUSALEM3000__.renderDiagnostics.persianSanctuary.componentIdentity),retained.persianSanctuary.componentIdentity);
  await page.getByRole('button',{name:'聖殿近看',exact:true}).click();
  await page.screenshot({path:`${output}/persian-temple.png`,fullPage:true});
  await writeFile(`${output}/persian-sanctuary-report.json`,JSON.stringify(retained.persianSanctuary,null,2));
  await writeFile(`${output}/persian-retained-report.json`,JSON.stringify(retained,null,2));
  // Hellenistic expansion uses the same generator and preserves cached identity.
  const expansionReports=[];
  await page.locator('.j3k-scrubber').evaluate(el=>{
    for(const value of [7,17,7.5]) {el.value=String(value);el.dispatchEvent(new Event('input',{bubbles:true}));}
  });
  for(const value of [7.5,6.5,7.5]) {
    await page.locator('.j3k-scrubber').evaluate((el,value)=>{el.value=String(value);el.dispatchEvent(new Event('input',{bubbles:true}));},value);
    await page.waitForFunction(value=>{
      const s=window.__JERUSALEM3000__; const d=s.renderDiagnostics;
      const city=value===7.5?d.sharedEra.expansion:d.sharedEra.successor;
      return s.historicalTime.position===value&&d.sharedEra.status==='ready'&&city.projection?.visibleBuildings>0;
    },value,{timeout:60000});
    const d=await page.evaluate(()=>window.__JERUSALEM3000__.renderDiagnostics);
    assert.equal(d.urbanFabric.phase2Components,0);
    assert.equal(d.visibleLegacyTemporalMeshes,0);
    assert.equal(await page.evaluate(()=>window.__JERUSALEM3000__.inheritanceState.active),false);
    if(value===7.5) {
      assert.equal(d.cityOverview,null,'leaving period overview must release camera state');
      assert.equal(d.persianSanctuary.visibleTemple,0,'later institutional continuity must not retain Persian geometry');
      assert.equal(d.sharedEra.successor.projection.visibleBuildings,0);
      assert.equal(d.sharedEra.expansion.historicalRegistrationVerified,false);
      assert.equal(d.sharedEra.expansion.residentialLedger.published,true);
      assert.equal(d.sharedEra.expansion.residentialLedger.referenceLayoutDerived,true);
      assert.ok(d.sharedEra.expansion.residentialLedger.registrationObjects>0);
      expansionReports.push(d.sharedEra.expansion);
    } else assert.equal(d.sharedEra.expansion.projection.visibleBuildings,0);
  }
  assert.equal(expansionReports[0].projection.identityFingerprint,expansionReports[1].projection.identityFingerprint);
  assert.equal(expansionReports[0].projection.transformFingerprint,expansionReports[1].projection.transformFingerprint);
  assert.notEqual(expansionReports[0].projection.identityFingerprint,retained.sharedEra.successor.projection.identityFingerprint);
  await page.screenshot({path:`${output}/hellenistic-city.png`,fullPage:true});
  await page.getByRole('button',{name:'實證',exact:true}).click();
  await page.waitForFunction(()=>window.__JERUSALEM3000__.renderDiagnostics.sharedEra.expansion.projection.visibleBuildings===0);
  await page.getByRole('button',{name:'全部',exact:true}).click();
  await page.waitForFunction(()=>window.__JERUSALEM3000__.renderDiagnostics.sharedEra.expansion.projection.visibleBuildings>0);
  await writeFile(`${output}/hellenistic-report.json`,JSON.stringify({expansionReports},null,2));
  // Render every era separately. Startup metadata is not proof of a visible city.
  const phaseReports = [];
  await page.getByRole('button',{name:'空間骨架對照',exact:true}).click();
  await page.locator('.j3k-skeleton-panel').waitFor({state:'visible'});
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
    assert.equal(sample.render.visibleLegacyTemporalMeshes,0,'unregistered hash-positioned anchor solids must remain withdrawn in every era');
    if([13,15].includes(phase)){assert.ok(sample.render.urbanFabric.phase2Components>0,'Crusader/Ottoman construction must use their own phase progress after the Roman destruction');assert.ok(Math.abs(sample.render.urbanFabric.morphologyProgress-.9)<1e-6);}
    const foundation=await page.evaluate(()=>window.__JERUSALEM3000__.inspectCityFoundation());
    assert.equal(foundation.phaseId,sample.time.phase);assert.equal(foundation.owner,sample.render.foundation.owner);
    assert.equal(foundation.terrain.sampling,'rendered-dem-triangles');assert.equal(foundation.terrain.verticalScale,1);
    assert.equal(foundation.registrationAccounting.visibleScopeAccounted,true,'every visible unbound component must be explicitly scoped');
    assert.equal(foundation.domains.lifecycle.unclassifiedWithoutDeclaredEvents,0,'missing events require an explicit supported scope');
    if(phase===8){assert.equal(foundation.domains.lifecycle.explicitEventScopes,7);const context=await page.evaluate(()=>window.__JERUSALEM3000__.inspectSourceLifecycleContext('j3k:district:temple-mount'));assert.ok(context.anchors.every(a=>a.state==='build'));assert.equal(context.ownPhysicalEventsDeclared,false);}
    assert.equal(foundation.foundationAccepted,false);assert.equal(Object.keys(foundation.domains).length,6);
    assert.deepEqual(foundation.renderer.outOfPhaseBindingIds,[],'visible registered objects must have a matching phase index');
    if(phase===10){const unknown=await page.evaluate(()=>window.__JERUSALEM3000__.inspectCityObject('j3k:object:inner-temple'));assert.ok(unknown.lifecycle.events.some(e=>e.phase==='aelia'&&e.state==='unresolved'));}
    assert.ok(foundation.renderer.visibleComponents>0);
    if([13,15].includes(phase)){assert.equal(sample.render.urbanFabric.sharedLedger.published,true);assert.ok(foundation.domains.occupation.visibleBoundObjects>0);assert.equal(sample.render.urbanFabric.sharedLedger.semanticBuildings,0);assert.equal(foundation.renderer.unboundComponents,0,'later morphology components must bind to shared IDs');}
    if([10,11,12,14,16,17].includes(phase)){assert.equal(sample.render.urbanFabric.sharedLedger.published,true);assert.ok(foundation.domains.occupation.visibleBoundObjects>0);assert.equal(sample.render.urbanFabric.sharedLedger.semanticBuildings,0);assert.equal(foundation.renderer.unboundComponents,foundation.renderer.provisionalInheritedComponents,'only explicitly provisional inheritance may remain unbound in later footprint eras');}
    assert.equal(foundation.renderer.provisionalTraceableComponents,foundation.renderer.provisionalInheritedComponents,'every displayed provisional inherited component needs a separate trace');
    const inheritanceAudit=await page.evaluate(()=>({index:window.__JERUSALEM3000__.inheritanceTransitionIndex,state:window.__JERUSALEM3000__.inheritanceState}));
    assert.equal(inheritanceAudit.index.length,17);assert.ok(inheritanceAudit.index.every(t=>t.survivalVerified===false&&t.historicalFate==='unresolved'));
    if(foundation.renderer.provisionalInheritedComponents>0){assert.equal(inheritanceAudit.state.audit.tracedComponents,foundation.renderer.provisionalInheritedComponents);assert.equal(inheritanceAudit.state.audit.survivalVerified,false);}
    if([10,14,16].includes(phase)){
      const count=foundation.renderer.provisionalInheritedComponents;
      await page.getByRole('button',{name:'實證',exact:true}).click();
      await page.waitForFunction(()=>window.__JERUSALEM3000__.inheritanceState.audit.visibleComponents===0);
      assert.equal(await page.evaluate(()=>window.__JERUSALEM3000__.inspectCityFoundation().renderer.provisionalInheritedComponents),0);
      await page.getByRole('button',{name:'全部',exact:true}).click();
      await page.waitForFunction(count=>window.__JERUSALEM3000__.inheritanceState.audit.visibleComponents===count,count);
      assert.equal(await page.evaluate(()=>window.__JERUSALEM3000__.historicalTime.position),value);
    }
    if(phase<=3)assert.equal(foundation.renderer.displayAnnotationComponents,[1,1,9,10][phase]);
    if(phase<=3)assert.ok(foundation.domains.occupation.visibleBoundObjects>0,'early houses must bind to shared identities');
    if(phase===7){assert.ok(foundation.domains.occupation.visibleBoundObjects>0);assert.equal(foundation.renderer.unboundComponents,0,'finished Hellenistic geometry must share canonical IDs');}
    if([8,9].includes(phase)){assert.equal(foundation.renderer.unboundComponents,0,'all canonical roads and houses must bind to shared events');assert.ok(sample.render.urbanFabric.canonicalGeneratedEvents.buildings>0);}
    if([8,9].includes(phase))assert.ok(foundation.domains.occupation.visibleBoundObjects>0,'canonical parcel bindings must be recognized by the common foundation interface');
    assert.equal(foundation.renderer.boundComponents+foundation.renderer.unboundComponents,foundation.renderer.visibleComponents);

    const visible = sample.render.visibleCoreMeshes +
      sample.render.urbanFabric.phase2Components + sample.render.visibleLegacyTemporalMeshes +
      (sample.render.sharedEra?.projection?.visibleBuildings || 0) +
      (sample.render.sharedEra?.successor?.projection?.visibleBuildings || 0) +
      (sample.render.sharedEra?.expansion?.projection?.visibleBuildings || 0) +
      (sample.render.earliestSettlement?.visibleHouses || 0) +
      (sample.render.middleBronzeSettlement?.visibleHouses || 0) +
      (sample.render.lateBronzeSettlement?.visibleHouses || 0) +
      (sample.render.davidSettlement?.visibleHouses || 0);
    assert.ok(visible > 0, `No urban geometry rendered for ${sample.time.phase}`);
    if(phase===10)assert.equal(await page.evaluate(()=>window.__JERUSALEM3000__.inheritanceState.terrainAuthority),'canonical-dem-rendered-triangles');
    if (phase === 10) assert.equal(sample.render.visibleCoreMeshes, 0,
      'Aelia must not reuse standing Herodian architecture');
    const spatialSkeleton=await page.evaluate(()=>window.__JERUSALEM3000__.inspectSpatialSkeleton());
    assert.equal(spatialSkeleton.phaseId,sample.time.phase);assert.equal(spatialSkeleton.historicalFoundationAccepted,false);assert.equal(spatialSkeleton.terrain,'modern-dem-rendered-triangles');
    assert.equal(await page.locator('.j3k-skeleton-panel').getAttribute('data-phase'),sample.time.phase);
    if([10,11,12].includes(phase)){assert.ok(spatialSkeleton.domains.districts.spatialObjects>=2);assert.equal(spatialSkeleton.domains.routes.spatialObjects,3);assert.equal(foundation.renderer.unboundComponents,0);assert.equal(inheritanceAudit.state.active,false,'independent layouts must not retain arbitrary Herodian overlays');assert.equal(sample.render.cityOverview.framePhase,'independent-later-shared-window');}
    if(phase<=2)assert.ok(spatialSkeleton.domains.routes.spatialObjects>0,'existing early footpath linework must be available');
    phaseReports.push({ spatialSkeleton, inheritanceAudit, value, elapsedMs: Date.now() - started, visible, foundation, ...sample });
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
  await mobile.waitForFunction(()=>window.__JERUSALEM3000__.renderDiagnostics.earliestSettlement?.visibleHouses===14);
  await mobile.screenshot({path:`${output}/earliest-mobile.png`,fullPage:true});
  await mobile.getByRole('button',{name:'山城地形',exact:true}).click();
  await mobile.waitForFunction(()=>window.__JERUSALEM3000__.renderDiagnostics.terrainPresentation.overviewActive);
  await mobile.screenshot({path:`${output}/mountain-city-mobile.png`,fullPage:true});
  assert.equal(await mobile.getByRole('button',{name:'山城地形',exact:true}).getAttribute('aria-pressed'),'true');
  await mobile.getByRole('button',{name:'山城地形',exact:true}).click();
  await mobile.waitForFunction(()=>!window.__JERUSALEM3000__.renderDiagnostics.terrainPresentation.overviewActive);

  await mobile.locator('.j3k-scrubber').evaluate(el=>{el.value='1.9';el.dispatchEvent(new Event('input',{bubbles:true}));});
  await mobile.waitForFunction(()=>window.__JERUSALEM3000__.renderDiagnostics.middleBronzeSettlement?.visibleHouses===24);
  await mobile.screenshot({path:`${output}/middle-bronze-mobile.png`,fullPage:true});
  await mobile.locator('.j3k-scrubber').evaluate(el=>{el.value='2.9';el.dispatchEvent(new Event('input',{bubbles:true}));});
  await mobile.waitForFunction(()=>window.__JERUSALEM3000__.renderDiagnostics.lateBronzeSettlement?.visibleSupportComponents===8);
  await mobile.screenshot({path:`${output}/late-bronze-mobile.png`,fullPage:true});
  await mobile.locator('.j3k-scrubber').evaluate(el=>{el.value='3.9';el.dispatchEvent(new Event('input',{bubbles:true}));});
  await mobile.waitForFunction(()=>window.__JERUSALEM3000__.renderDiagnostics.davidSettlement?.visibleRoyalMarkers===1);
  const mobileReliefLabels=await mobile.locator('.j3k-relief-labels').evaluate(el=>{const box=el.getBoundingClientRect();return [...el.children].filter(c=>!c.hidden).map(c=>{const r=c.getBoundingClientRect();return {left:r.left-box.left,right:r.right-box.left,width:box.width};});});
  assert.equal(mobileReliefLabels.length,3);assert.ok(mobileReliefLabels.every(r=>r.left>=-1&&r.right<=r.width+1),'all royal relief labels fit portrait view');
  await mobile.screenshot({path:`${output}/david-mobile.png`,fullPage:true});
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
  await mobile.locator('.j3k-scrubber').evaluate(el=>{el.value='7.5';el.dispatchEvent(new Event('input',{bubbles:true}));});
  await mobile.waitForFunction(()=>window.__JERUSALEM3000__.renderDiagnostics.sharedEra.expansion.projection?.visibleBuildings>0,null,{timeout:60000});
  const mobileExpansion=await mobile.evaluate(()=>window.__JERUSALEM3000__.renderDiagnostics.sharedEra);
  assert.equal(mobileExpansion.successor.status,'idle','direct expansion entry must not generate Persian architecture');
  assert.equal(mobileExpansion.projection,null,'direct expansion entry must not generate first-temple architecture');
  await mobile.screenshot({path:`${output}/hellenistic-mobile.png`,fullPage:true});
  await mobile.locator('.j3k-scrubber').evaluate(el => {
    el.value = '6.5'; el.dispatchEvent(new Event('input', { bubbles: true }));
  });
  await mobile.getByRole('button', {name:'前代遺存 · 推定',exact:true}).click();
  await mobile.waitForFunction(() => window.__JERUSALEM3000__.renderDiagnostics?.sharedEra?.status === 'ready', null, {timeout:60000});
  const mobileShared = await mobile.evaluate(() => window.__JERUSALEM3000__.renderDiagnostics.sharedEra);
  assert.ok(mobileShared.projection.visibleBuildings > 0);
  assert.equal(mobileShared.projection.layerState,'retained-ruin');
  assert.equal(mobileShared.retainedObjects,mobileShared.projection.visibleBuildings);
  assert.ok(mobileShared.successor.projection.visibleBuildings>0);
  await mobile.screenshot({path:`${output}/shared-mobile.png`,fullPage:true});
  await mobile.getByRole('button',{name:'空間骨架對照',exact:true}).click();
  await mobile.locator('.j3k-skeleton-panel').waitFor({state:'visible'});
  const skeletonBox=await mobile.locator('.j3k-skeleton-panel canvas').boundingBox();assert.ok(skeletonBox.x>=0&&skeletonBox.x+skeletonBox.width<=390,'skeleton map must fit portrait width');
  await mobile.screenshot({path:`${output}/spatial-skeleton-mobile.png`,fullPage:true});
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
      { ok: true, core: runtime.evidenceObjects.cityCoreAB, phaseReports, sharedReports, reports, errors },
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
