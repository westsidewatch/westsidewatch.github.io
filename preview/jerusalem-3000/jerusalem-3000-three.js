import {createDefenseTimelineView} from './defense-timeline-view.js';
import {advancePlayback} from './playback-clock.js';
import {isIndependentLaterPhase} from './independent-later-skeleton.js';
import {createSpatialSkeletonView} from './spatial-skeleton-view.js';
import { isEarliestPhase, isEarlyLandscapePhase } from './earliest-settlement.js';
import { isSharedSlicePhase, isSharedGenerationPhase, RETAINED_PHASE } from './shared-era-runtime.js';
import { isCorePhase } from './city-lifecycle-projection.js';
import { mountJerusalemThreeScene } from './three-scene.js';
import { HistoricalTimeEngine } from './historical-time-engine.js';
import { RuinTransformationEngine } from './ruin-transformation-engine.js';
import { loadTemporalCityIntegration } from './temporal-city-integration.js';
import { auditProductionReadiness } from './production-readiness.js';
import { auditProductionCompletion } from './production-completion-audit.js';
const stage = document.querySelector('.j3k-stage'),
  mount = document.querySelector('[data-three-stage]'),
  badge = document.querySelector('.j3k-terrain-badge');
window.__JERUSALEM3000__ = {
  status: 'booting',
  three: false,
  timeline: false,
  evidence: false,
  timeEngine: false,
  ruinEngine: false,
  temporalCity: false,
  inheritance: false,
  inheritanceError: null,
  productionReady: false,
  complete: false,
  error: null,
};
try {
  const response = await fetch('./data/continuous-build-timeline.json', {
    cache: 'no-store',
  });
  if (!response.ok) throw new Error(`timeline ${response.status}`);
  const timeline = await response.json(),
    phases = timeline.phases;
  if (!Array.isArray(phases) || phases.length !== 18)
    throw new Error('timeline must contain 18 canonical phases');
  const time = new HistoricalTimeEngine(phases),
    ruin = new RuinTransformationEngine(phases),
    temporalCity = await loadTemporalCityIntegration(phases);
  if (!time.reversibleCheck())
    throw new Error('historical time engine failed reversibility check');
  if (!ruin.reversibleCheck())
    throw new Error('ruin transformation engine failed reversibility check');
  window.__JERUSALEM3000__.timeline = true;
  window.__JERUSALEM3000__.timeEngine = true;
  window.__JERUSALEM3000__.ruinEngine = true;
  window.__JERUSALEM3000__.temporalCity = true;
  const slider = document.querySelector('.j3k-scrubber'),
    play = document.querySelector('.j3k-play'),
    date = document.querySelector('.j3k-phase-date'),
    eraEn = document.querySelector('.j3k-era-en'),
    eraZh = document.querySelector('.j3k-caption h2'),
    note = document.querySelector('.j3k-era-note');
  const markers = [...document.querySelectorAll('.j3k-markers button')],
    strip = document.querySelector('.j3k-phase-strip');
  phases.forEach(() => strip.append(document.createElement('i')));
  const ticks = [...strip.children];
  let districtAcceptance=null;
  function renderDistrictAcceptance(){
    const panel=document.querySelector('.j3k-evidence-panel');if(!panel)return;
    let section=panel.querySelector('[data-district-acceptance]');
    if(!districtAcceptance||districtAcceptance.phase!==stage.dataset.phase){section?.remove();return;}
    const key=JSON.stringify(districtAcceptance);if(section?.dataset.key===key)return;
    if(!section){section=document.createElement('section');section.dataset.districtAcceptance='';panel.append(section);}
    section.dataset.key=key;section.replaceChildren();
    const title=document.createElement('h4');title.textContent='住宅分區 · 推定示意';section.append(title);
    const note=document.createElement('p');note.textContent='以下是畫面模型數量，不代表古代人口或實際建築數；前代遺存與再利用關係仍未核定。';section.append(note);
    if(districtAcceptance.status!=='ready'){const pending=document.createElement('p');pending.textContent=districtAcceptance.status==='error'?'本期住宅生成失敗，尚無完整分區結果。':'本期住宅生成中，完成後顯示分區結果。';section.append(pending);return;}
    const labels={'eastern-ridge':'東南山脊','northern-precinct':'北部聖區周邊','western-hill':'西丘','ridge-rebuilding':'山脊重建區','northern-rebuilding':'北部重建區'};
    const table=document.createElement('table'),head=document.createElement('tr');
    for(const text of ['地區','街區','住宅','顯示','查看']){const th=document.createElement('th');th.textContent=text;head.append(th);}table.append(head);
    for(const d of districtAcceptance.districts){const row=document.createElement('tr');row.dataset.residentialDistrict=d.id;row.dataset.buildings=String(d.buildings);row.dataset.visibleBuildings=String(d.visibleBuildings);const name=(labels[d.id.split(':').at(-1)]||'推定地區')+(d.layerState==='retained-ruin'?' · 前代遺存':districtAcceptance.phase==='babylonian-destruction'?' · 毀城示意':'');for(const value of [name,d.blocks,d.buildings,d.visibleBuildings]){const cell=document.createElement('td');cell.textContent=String(value);row.append(cell);}const action=document.createElement('td'),button=document.createElement('button');button.type='button';button.textContent='近看';button.setAttribute('aria-label',name+'住宅近看');button.disabled=d.visibleBuildings===0;button.addEventListener('click',()=>{if((terrainOverview(false),three.focusResidentialDistrict(d.id))){panel.hidden=true;document.querySelector('.j3k-evidence-toggle').setAttribute('aria-expanded','false');}});action.append(button);row.append(action);table.append(row);}section.append(table);
  }
  let baselineInfo=null,baselinePhase='',baselineCompare=null,baselineGeneration='';
  function refreshBaseline(force=false){const key=stage.dataset.phase+'|'+stage.dataset.evidenceMode+'|'+Math.floor(Number(slider.value)*10);if(!baselineInfo||!stage.dataset.phase||(!force&&baselinePhase===key))return;const s=three.inspectSpatialSkeleton();if(!s)return;baselinePhase=key;baselineInfo.textContent='統一概覽基準 · 全時代共用公尺比例與原始高程；鏡頭縮放不改變建築尺寸。城市結構未完成，住宅仍含推定模組，不代表實測戶數。水防：'+(s.domains.waterDefense.spatialObjects?'已登記局部':'尚缺可定位表示')+'；宗教／公共核心：'+(s.domains.sacredCivic.spatialObjects?'已有局部表示（含推定量體）':'尚缺可定位表示')+'。缺口不表示歷史不存在；建造順序與跨期轉場為展示示意。';}
  let skeletonView=null,defenseView=null;
  const three = mountJerusalemThreeScene(mount, {
    onDistrictAcceptance(info){districtAcceptance=info;renderDistrictAcceptance();skeletonView?.refresh();defenseView?.refresh();const key=(info?.phase||'')+'|'+(info?.status||'');if(key!==baselineGeneration){baselineGeneration=key;refreshBaseline(true);}},
    onReady(info) {
      window.__JERUSALEM3000__.three = true;
      window.__JERUSALEM3000__.evidence = true;
      window.__JERUSALEM3000__.evidenceObjects = info;
      stage.dataset.threeRuntime = 'ready';
      badge.textContent = `THREE.JS · ORBIT READY · ${info.renderableObjects} EVIDENCE OBJECTS`;
    },
  });
  await three.ready;
  window.__JERUSALEM3000__.inspectCityObject=id=>three.inspectCityObject(id);
  window.__JERUSALEM3000__.inspectSourceLifecycleContext=id=>three.inspectSourceLifecycleContext(id);
  window.__JERUSALEM3000__.inspectCityFoundation=phase=>three.inspectCityFoundation(phase);
  window.__JERUSALEM3000__.inspectMetricResidentialPolicy=()=>three.inspectMetricResidentialPolicy();
  window.__JERUSALEM3000__.inspectHousingBoundary=options=>three.inspectHousingBoundary(options);
  window.__JERUSALEM3000__.inspectOverviewBaseline=()=>three.inspectOverviewBaseline();
  window.__JERUSALEM3000__.cityFoundationIndex=three.cityFoundationIndex();
  window.__JERUSALEM3000__.inspectHerodianDimensions=()=>three.inspectHerodianDimensions();
  window.__JERUSALEM3000__.inspectRegionalLandforms=()=>three.inspectRegionalLandforms();
  window.__JERUSALEM3000__.inspectSharedPlaces=()=>three.inspectSharedPlaces();
  window.__JERUSALEM3000__.sharedPlaceTransitions=()=>three.sharedPlaceTransitions();
  window.__JERUSALEM3000__.inspectPersistentCityPhase=phase=>three.inspectPersistentCityPhase(phase);
  window.__JERUSALEM3000__.inspectSpatialSkeleton=()=>three.inspectSpatialSkeleton();
  skeletonView=createSpatialSkeletonView({parent:document.querySelector('.j3k-shell'),controls:document.querySelector('.j3k-event-controls'),terrain:three.foundationContext().terrain,getSnapshot:()=>three.inspectSpatialSkeleton(),getPhaseLabel:id=>phases.find(p=>p.id===id)?.label||id});
  window.__JERUSALEM3000__.inspectDefenseTimeline=()=>three.inspectDefenseTimeline();
  window.__JERUSALEM3000__.defenseTimelineIndex=three.defenseTimelineIndex();
  window.__JERUSALEM3000__.defenseTransitionIndex=three.defenseTransitionIndex();
  defenseView=createDefenseTimelineView({parent:document.querySelector('.j3k-time'),controls:document.querySelector('.j3k-event-controls'),getSnapshot:()=>three.inspectDefenseTimeline(),index:three.defenseTimelineIndex(),transitions:three.defenseTransitionIndex()});
  const retainedToggle = document.querySelector('.j3k-retained-toggle');
  retainedToggle.addEventListener('click', () => {
    const enabled = retainedToggle.getAttribute('aria-pressed') !== 'true';
    retainedToggle.setAttribute('aria-pressed', String(enabled));
    three.setRetainedLayerVisible(enabled);
  });
  let inheritance = null,
    inheritedPhase = '';
  try {
    const module = await import('./phase2-inheritance-runtime.js');
    inheritance = module.createInheritanceLayer(three.root,{...three.foundationContext(),phases});
    window.__JERUSALEM3000__.inheritance = true;
    window.__JERUSALEM3000__.inheritanceTransitionIndex=inheritance.transitionIndex();
    stage.dataset.inheritance = 'ready';
  } catch (error) {
    console.error('[Jerusalem 3000 inheritance]', error);
    window.__JERUSALEM3000__.inheritance = false;
    window.__JERUSALEM3000__.inheritanceError = String(error?.stack || error);
    stage.dataset.inheritance = 'disabled';
  }
  function renderWaterDefense(position){
    const info=three.waterDefenseEvidence(position),panel=document.querySelector('.j3k-evidence-panel');let section=panel.querySelector('[data-water-defense]');
    if(!info){section?.remove();return;}
    const key=JSON.stringify([info.phase,info.selectedVariant,info.objects.map(o=>o.state)]);if(section?.dataset.key===key)return;
    if(!section){section=document.createElement('section');section.dataset.waterDefense='';panel.append(section);}section.dataset.key=key;section.replaceChildren();
    const title=document.createElement('h4');title.textContent='城防／取水 · 定位與缺口';section.append(title);
    if(info.phase==='middle-bronze'){const label=document.createElement('label');label.textContent='泉塔年代方案 ';const select=document.createElement('select');select.setAttribute('aria-label','泉塔年代方案');for(const v of info.variants){const option=document.createElement('option');option.value=v.id;option.textContent=v.label;select.append(option);}select.value=info.selectedVariant;select.addEventListener('change',()=>{three.setWaterDefenseVariant(select.value);renderWaterDefense(position);});label.append(select);section.append(label);}
    const note=document.createElement('p');note.textContent='定位圖使用現代近似位置點，不是古代城界、牆段平面或地下水道線。';section.append(note);
    const points=info.objects.filter(o=>o.point),ns='http://www.w3.org/2000/svg',svg=document.createElementNS(ns,'svg');svg.setAttribute('viewBox','0 0 320 190');svg.setAttribute('role','img');svg.setAttribute('aria-label','基訓泉與西丘寬牆的現代參考位置，沒有繪製古代牆線或水道');
    const xs=points.map(o=>o.point.x),zs=points.map(o=>o.point.z),xmin=Math.min(...xs)-80,xmax=Math.max(...xs)+80,zmin=Math.min(...zs)-70,zmax=Math.max(...zs)+70,scale=Math.min(300/(xmax-xmin),170/(zmax-zmin));
    const north=document.createElementNS(ns,'text');north.setAttribute('x','260');north.setAttribute('y','15');north.textContent='北 ↑';svg.append(north);
    for(const object of points){const x=10+(object.point.x-xmin)*scale,y=10+(object.point.z-zmin)*scale,circle=document.createElementNS(ns,'circle');circle.setAttribute('cx',String(x));circle.setAttribute('cy',String(y));circle.setAttribute('r','4');circle.setAttribute('fill',object.kind==='fortification'?'#95764d':'#537c83');svg.append(circle);const text=document.createElementNS(ns,'text');text.setAttribute('x',String(x>200?x-8:x+8));text.setAttribute('y',String(y+4));text.setAttribute('text-anchor',x>200?'end':'start');text.textContent=object.label;svg.append(text);}section.append(svg);const attribution=document.createElement('p');attribution.textContent='© OpenStreetMap contributors · ODbL（現代定位來源）';section.append(attribution);
    const admission=document.createElement('p');admission.textContent='局部幾何待核定：來源平面、尺度與方向、測量定位點、獨立核對點、高程基準及年代版本齊備後，才能接入牆段或地下路線。';admission.dataset.localPlanAdmission='';section.append(admission);
    const states={build:'時期來源支持',transform:'自然水源參考',unresolved:'具體年代／去向未核定',absent:'本期不指定此構件'};
    for(const object of info.objects){const entry=document.createElement('div');entry.dataset.waterDefenseObject=object.id;entry.dataset.state=object.state;const heading=document.createElement('h5');heading.textContent=object.label+' · '+(states[object.state]||'待核對');const text=document.createElement('p');text.textContent=object.gap;entry.append(heading,text);for(const url of [...object.sources,...(object.reference?[object.reference.source]:[])]){const link=document.createElement('a');link.href=url;link.target='_blank';link.rel='noopener';link.textContent=url===object.reference?.source?'現代定位來源':'研究／遺址來源';entry.append(link,document.createTextNode(' '));}section.append(entry);}
  }
  const earlyEvidencePanel=document.querySelector('.j3k-evidence-panel');
  const routeEvidenceNodes=[...earlyEvidencePanel.childNodes].map(n=>n.cloneNode(true));
  let evidencePanelPhase='';
  const templeFocusButton=document.createElement('button');templeFocusButton.textContent='聖殿近看';templeFocusButton.hidden=true;
  document.querySelector('.j3k-event-controls').append(templeFocusButton);
  const terrainButton=document.createElement('button');terrainButton.type='button';terrainButton.className='j3k-terrain-toggle';terrainButton.textContent='山城地形';terrainButton.setAttribute('aria-pressed','false');
  const terrainNote=document.createElement('span');terrainNote.className='j3k-terrain-note';terrainNote.hidden=true;terrainNote.textContent='GLO-30 現代地表 · 高度原比例 · 谷線非河水';
  document.querySelector('.j3k-event-controls').append(terrainButton,terrainNote);
  const geographyCredit=document.createElement('p');geographyCredit.className='j3k-geography-credit';geographyCredit.textContent='地形：Copernicus GLO-30 · © DLR／Airbus（歐盟及 ESA 提供）；現代地名與谷線：© OpenStreetMap contributors，ODbL。';stage.after(geographyCredit);
  function terrainOverview(enabled){const active=three.setTerrainOverview(enabled);terrainButton.setAttribute('aria-pressed',String(active));baselineCompare?.setAttribute('aria-pressed',String(active));terrainNote.hidden=!active;stage.classList.toggle('terrain-overview',active);}
  terrainButton.addEventListener('click',()=>terrainOverview(terrainButton.getAttribute('aria-pressed')!=='true'));
  templeFocusButton.addEventListener('click',()=>{terrainOverview(false);three.focusRoyalTemple();});
  const reliefButton=document.createElement('button');reliefButton.type='button';reliefButton.textContent='城內高差';reliefButton.hidden=true;
  document.querySelector('.j3k-event-controls').append(reliefButton);
  reliefButton.addEventListener('click',()=>{terrainOverview(false);three.focusRoyalRelief();});
  const reliefPanel=document.createElement('section');reliefPanel.className='j3k-royal-relief';reliefPanel.hidden=true;stage.after(reliefPanel);
  function updateRoyalRelief(phase,templeState){
    const active=phase==='david-solomon';reliefPanel.hidden=!active;reliefButton.hidden=!active;if(!active)return;
    const era=templeState==='absent'?'david':'solomon';if(reliefPanel.dataset.stage===era)return;reliefPanel.dataset.stage=era;reliefPanel.replaceChildren();
    const profile=three.royalReliefProfile();if(!profile)return;
    const heading=document.createElement('h3');heading.textContent='大衛城 → 北部高處：沿山脊上升';reliefPanel.append(heading);
    const names=['大衛城南段（示意點）','大衛城中段（示意點）',era==='david'?'禾場經文關聯區（位置示意）':'所羅門聖殿（位置示意）'];
    const ns='http://www.w3.org/2000/svg',svg=document.createElementNS(ns,'svg');svg.setAttribute('viewBox','0 0 760 185');svg.setAttribute('role','img');svg.setAttribute('aria-label','大衛城南段至北部高處的現代地形剖面，水平與垂直同一比例');
    const factor=620/profile.distance,base=profile.anchors[0].y-5,x=p=>70+p.distance*factor,y=p=>150-(p.y-base)*factor;
    const polyline=document.createElementNS(ns,'polyline');polyline.setAttribute('points',profile.samples.map(p=>`${x(p)},${y(p)}`).join(' '));polyline.setAttribute('fill','none');polyline.setAttribute('stroke','#8b422b');polyline.setAttribute('stroke-width','3');svg.append(polyline);
    profile.anchors.forEach((p,i)=>{const circle=document.createElementNS(ns,'circle');circle.setAttribute('cx',String(x(p)));circle.setAttribute('cy',String(y(p)));circle.setAttribute('r','4');circle.setAttribute('fill','#8b422b');svg.append(circle);const label=document.createElementNS(ns,'text');label.setAttribute('x',String(x(p)));label.setAttribute('y',String(y(p)-14));label.setAttribute('text-anchor',i===2?'end':'start');label.textContent=names[i];svg.append(label);});
    const axis=document.createElementNS(ns,'text');axis.setAttribute('x','70');axis.setAttribute('y','178');axis.textContent=`南 → 北 · 剖面水平距離約 ${Math.round(profile.distance)}m · 高程／水平同尺度（無誇大）`;svg.append(axis);reliefPanel.append(svg);
    const comparison=document.createElement('p');comparison.textContent=`目前示意點的現代地形：北部比南段高約 ${Math.round(profile.deltaSouth)}m，比中段高約 ${Math.round(profile.deltaMiddle)}m。`;reliefPanel.append(comparison);
    const caveat=document.createElement('p');caveat.className='j3k-relief-caveat';caveat.textContent='紅線為地形剖面參考線，非古道路。高差取自現代約30m DSM；示意點非考古定位，不能當作大衛／所羅門時代的實測高程。禾場與建殿關聯依代下3:1，精確位置與古地表尚未核定。';reliefPanel.append(caveat);
    const source=document.createElement('a');source.href='https://www.biblegateway.com/passage/?search=2+Chronicles+3%3A1&version=KJV';source.textContent='禾場與建殿的經文關聯：代下3:1';source.target='_blank';source.rel='noopener';reliefPanel.append(source);
  }
  function update(v) {
    const state = time.sample(v),
      p = state.phase,
      herodian = time.herodianVisibility(v),
      transformation = ruin.sample(v, p.id === 'babylonian-destruction' ? p.id : 'roman-destruction'),
      cityObjects = temporalCity.sample(state.position),
      citySummary = temporalCity.summary(state.position),
      localProgress = Math.max(0, Math.min(1, state.position - state.index));
    three.setBuildProgress(
      isCorePhase(p.id) ? 1 : localProgress,
    );
    three.setRuinProgress(transformation.ruin);
    three.setTemporalCityState?.(cityObjects, state.position, p.id);
    updateRoyalRelief(p.id,cityObjects.find(o=>o.id==='j3k:object:first-temple')?.state);
    if (inheritance) {
      try {
        inheritance.setVisible(!isCorePhase(p.id) && !isSharedGenerationPhase(p.id) && !isEarlyLandscapePhase(p.id) && !isIndependentLaterPhase(p.id));
        if (!isCorePhase(p.id) && !isSharedGenerationPhase(p.id) && !isEarlyLandscapePhase(p.id) && !isIndependentLaterPhase(p.id)) {
          if (inheritedPhase !== p.id) {
            inheritance.setPhase(p.id, localProgress);
            inheritedPhase = p.id;
          } else inheritance.setProgress(p.id, localProgress);
        }
      } catch (error) {
        console.error('[Jerusalem 3000 inheritance update]', error);
        window.__JERUSALEM3000__.inheritance = false;
        window.__JERUSALEM3000__.inheritanceError = String(
          error?.stack || error,
        );
        stage.dataset.inheritance = 'disabled';
        try {
          inheritance.dispose?.();
        } catch {}
        inheritance = null;
      }
    }
    window.__JERUSALEM3000__.historicalTime = {
      position: state.position,
      phase: p.id,
      continuity: state.cityContinuity,
      herodianVisibility: herodian,
      destruction: transformation.destruction,
      standing: transformation.standing,
      ruin: transformation.ruin,
      transformationPhase: transformation.phase,
    };
    window.__JERUSALEM3000__.temporalCityState = {
      phase: p.id,
      objects: cityObjects,
      summary: citySummary,
    };
    const inheritanceAudit=inheritance?.diagnostics(p.id)??null;
    window.__JERUSALEM3000__.inheritanceState = {
      audit:inheritanceAudit,
      terrainAuthority:inheritance?.terrainAuthority??null,
      phase: p.id,
      active: !isCorePhase(p.id) && !isSharedGenerationPhase(p.id) && !isEarlyLandscapePhase(p.id) && !isIndependentLaterPhase(p.id) && (inheritanceAudit?.visibleComponents??0)>0,
      progress: localProgress,
    };
    const productionInfo=window.__JERUSALEM3000__.production;
    badge.textContent=isEarliestPhase(p.id)
      ? '最早聚落 · 現代地形 · 推定住居／步徑'
      : p.id==='middle-bronze' ? '迦南城市 · 推定取水防禦 · 泉塔年代有爭議'
      : p.id==='late-bronze-iron1' ? '晚青銅—鐵器早期 · 住區推定 · 階梯石構年代有爭議'
      : p.id==='david-solomon' ? '大衛—所羅門 · 王室識別有爭議 · 建築平面未核定'
      : `JERUSALEM 3000 · TEMPORAL CITY · ${productionInfo?.evidenceObjects || 0} EVIDENCE OBJECTS · ${productionInfo?.constructionPieces || 0} PIECES`;
    date.textContent = p.dateLabel;
    eraEn.textContent = (p.state || '').toUpperCase() + ' · ' + p.dateLabel;
    const temple=cityObjects.find(o=>o.id===(p.id===RETAINED_PHASE?'j3k:object:second-temple-early':'j3k:object:first-temple'));
    templeFocusButton.hidden=!['david-solomon','late-first-temple','babylonian-destruction',RETAINED_PHASE].includes(p.id)||!(temple?.visible||temple?.ruined);
    eraZh.textContent=p.id==='david-solomon'?(temple?.state==='absent'?'大衛城 · 城防與王室':'所羅門城 · 第一聖殿'):p.label;
    retainedToggle.hidden = p.id !== RETAINED_PHASE;
    note.textContent = isEarliestPhase(p.id) ? '東南山脊與基訓泉周邊的小規模聚落。住居數量、位置、屋頂與步徑均為推定示意；地形使用現代 DEM。可拖動旋轉、滾輪縮放。' : p.id==='middle-bronze' ? '中青銅取水設施與防護通道示意。泉塔年代有爭議，粉褐色標示為爭議層；住居、位置與高度仍屬推定。鑿岩設施只顯示輪廓，完整城牆範圍尚未核定。' : p.id==='late-bronze-iron1' ? '此期城區範圍未核定；住居僅為示意，不代表人口增減或前代房屋留存。粉褐色階梯支撐體為年代與功能爭議層，不能直接認定為王宮基礎。前期防禦未預設延續，隱藏不表示毀壞。' : p.id==='david-solomon' ? '城防、王室院落與第一聖殿為推定復原，由共同帳本分段出現。聖殿主體採經文比例，牆線、位置與外觀未核定；可點「聖殿近看」。住宅仍為較晚鐵器時代類比。' : p.id === RETAINED_PHASE
      ? `${p.note} 可開啟「前代遺存」對照同一批第一聖殿廢墟；遺存範圍、埋藏深度及再利用關係尚未考古核定。重建住宅採獨立山脊／北部配置；早期第二聖殿主體、院落及入口為獨立推定示意，可點「聖殿近看」。城界、街網與人口未核定。`
      : isSharedSlicePhase(p.id) ? `${p.note} 東南山脊、北部聖區與西丘採獨立配置；西向擴張方向有文獻依據，具體邊界與道路仍為推定。毀城沿用同一批示意住居。` : isSharedGenerationPhase(p.id) ? `${p.note} 地塊、道路與住宅為推定示意，尚未完成該時代的考古定位。` : p.note;
    if(['byzantine','early-islamic','crusader','ayyubid-mamluk','ottoman','outside-walls','modern'].includes(p.id))note.textContent+=' 宗教核心亦為概略量體，非測繪復原。';
    if(p.id==='herodian-jesus')note.textContent+=' 比例校準：平台約300×480m；殿體高約52.5m（暫採每肘0.525m），位置與細節仍屬復原。';
    if(isIndependentLaterPhase(p.id))note.textContent+=' 地區、路網與住宅量體為示意；共同東側軸線不表示歷代路面相同。各期採階段概覽，非逐年完整復原。';
    if(window.__JERUSALEM3000__.inheritanceState.audit?.visibleComponents>0)note.textContent+=' 前代圖層按模型比例示意，留存構件與再利用關係尚未核定。';
    if(three.inspectDefenseTimeline()?.owner==='network')note.textContent+=' 赭色虛線牆為整體範圍的推定補足；低矮殘牆／候選帶保留毀壞及爭議狀態，並非測繪核定城廓；可看「城防年代」。';
    skeletonView?.refresh();defenseView?.refresh();
    if(evidencePanelPhase!==p.id) {
      evidencePanelPhase=p.id;
      const evidence=three.earlyLandscapeEvidence(p.id);
      if(evidence) {
        earlyEvidencePanel.replaceChildren();
        for(const [tag,text] of [['p','城市場景 · 資料來源'],['h3',p.label],['p',isEarlyLandscapePhase(p.id)?'住居與構件位置、形制仍為示意。現代 DEM 不等於古地表；粉褐色構件為爭議假說，沒有核定為完整建築。':'本期街區仍為推定示意。下列研究提供歷史背景，尚未核定畫面中的街網、建築平面與毀壞形態。']]) {
          const el=document.createElement(tag);el.textContent=text;earlyEvidencePanel.append(el);
        }
        const limits=document.createElement('ul');
        for(const text of evidence.limitations||[]) {
          const item=document.createElement('li');item.textContent=text;limits.append(item);
        }
        earlyEvidencePanel.append(limits);
        for(const [i,url] of [evidence.source,...evidence.references].entries()) {
          if(new URL(url).protocol!=='https:')continue;
          const link=document.createElement('a');link.href=url;link.target='_blank';link.rel='noopener noreferrer';link.textContent=i===0?'主要資料來源':`參考研究 ${i}`;
          const row=document.createElement('p');row.append(link);earlyEvidencePanel.append(row);
        }
      } else earlyEvidencePanel.replaceChildren(...routeEvidenceNodes.map(n=>n.cloneNode(true)));
    }
    let continuity=earlyEvidencePanel.querySelector('[data-city-continuity]');
    if(['david-solomon','late-first-temple','babylonian-destruction','persian-nehemiah'].includes(p.id)) {
      if(!continuity){continuity=document.createElement('section');continuity.dataset.cityContinuity='';earlyEvidencePanel.append(continuity);}
      continuity.replaceChildren();
      const title=document.createElement('h4');title.textContent='主體去向 · 資料狀態';continuity.append(title);
      const caveat=document.createElement('p');caveat.textContent='聖區承接不等於同一建築或地基。未知不表示已毀壞；資料狀態不等於已有復原幾何。';continuity.append(caveat);
      const states={absent:'尚未建造',withheld:'未核定',build:'建造',transform:'延續／改變',ruin:'毀壞',rebuild:'重新建造',unresolved:'去向未核定',buried:'埋藏',expand:'擴展',settlement:'聚落'};
      const list=document.createElement('ul');continuity.append(list);
      for(const object of cityObjects.filter(o=>['j3k:object:first-temple','j3k:object:second-temple-early','j3k:object:royal-city-wall-hypothesis','j3k:object:royal-monumental-zone-10c'].includes(o.id))) {
        const item=document.createElement('li');item.dataset.continuityObject=object.id;item.dataset.state=object.state;item.textContent=`${object.label}：${states[object.state]||object.state}`;list.append(item);
      }
    } else continuity?.remove();
    ticks.forEach((x, i) => {
      x.classList.toggle('is-past', i < state.index);
      x.classList.toggle('is-current', i === state.index);
    });
    markers.forEach((x) =>
      x.classList.toggle('is-active', Number(x.dataset.phase) === state.index),
    );
    stage.dataset.operation = p.state;
    stage.dataset.phase = p.id;
    renderDistrictAcceptance();
    renderWaterDefense(state.position);
    stage.dataset.transformation = transformation.phase;
    stage.dataset.temporalObjects = String(
      cityObjects.filter((object) => object.visible || object.ruined).length,
    );
    refreshBaseline();
    stage.dataset.inheritance =
      !isCorePhase(p.id) && !isSharedGenerationPhase(p.id) && !isEarlyLandscapePhase(p.id) && !isIndependentLaterPhase(p.id) && inheritance?.runtime
        ? 'active'
        : window.__JERUSALEM3000__.inheritance
          ? 'ready'
          : 'disabled';
  }
  const pace=document.createElement('label');pace.className='j3k-playback-pace';pace.textContent='播放速度 ';const speed=document.createElement('select');speed.setAttribute('aria-label','每期播放時間');for(const [seconds,label]of [[24,'慢速 · 24秒／期'],[12,'標準 · 12秒／期'],[6,'快速 · 6秒／期']]){const option=document.createElement('option');option.value=String(seconds);option.textContent=label;option.selected=seconds===12;speed.append(option);}pace.append(speed);play.before(pace);
  baselineInfo=document.createElement('p');baselineInfo.className='j3k-overview-baseline';document.querySelector('.j3k-time').append(baselineInfo);const compare=document.createElement('button');baselineCompare=compare;compare.type='button';compare.textContent='統一尺度比較';compare.setAttribute('aria-pressed','false');document.querySelector('.j3k-time-head').append(compare);compare.addEventListener('click',()=>{const active=terrainButton.getAttribute('aria-pressed')!=='true';terrainOverview(active);});
  let raf = 0,
    last = 0, waitingForCity=false,playbackPosition=Number(slider.value);
  function stop() {
    if (raf) cancelAnimationFrame(raf);
    raf = 0;
    last = 0;
    waitingForCity=false;
    play.textContent = '▶ 建城';
    play.setAttribute('aria-pressed', 'false');
    window.__JERUSALEM3000__.playback={status:'paused',position:Number(slider.value),presentationPosition:playbackPosition};
  }
  function frame(t) {
    if (!last) last = t;
    const readiness=three.playbackReadiness(),position=playbackPosition;
    const elapsed=(t-last)/1000;last=t;
    if(!readiness.ready){
      waitingForCity=true;
      window.__JERUSALEM3000__.playback={status:readiness.status==='error'?'error':'waiting',position,phase:readiness.phase};
      if(readiness.status==='error'){stop();window.__JERUSALEM3000__.playback={status:'error',position,phase:readiness.phase};}
      else {play.textContent='Ⅱ 等待城市 · 可暫停';if(raf)raf=requestAnimationFrame(frame);}
      return;
    }
    const wasWaiting=waitingForCity;waitingForCity=false;play.textContent='Ⅱ 暫停';
    let v=advancePlayback(position,wasWaiting?0:elapsed,time.max+1,{rate:1/Number(speed.value)});
    playbackPosition=v;
    window.__JERUSALEM3000__.playback={status:'playing',position:v,phase:readiness.phase};
    if (v >= time.max+1) {
      v = time.max+1;
      stop();
    }
    three.setPlaybackDisplayPosition(v);
    slider.value = Math.min(v,time.max);
    update(Math.min(v,time.max));
    if (raf) raf = requestAnimationFrame(frame);
  }
  function start() {
    if (raf) return;
    if(!(Number(slider.value)===time.max&&playbackPosition>time.max&&playbackPosition<time.max+1))playbackPosition=Number(slider.value);
    terrainOverview(true);
    three.setPlaybackPresentation(true);three.setPlaybackDisplayPosition(playbackPosition);
    play.textContent = 'Ⅱ 暫停';
    play.setAttribute('aria-pressed', 'true');
    raf = requestAnimationFrame(frame);
  }
  slider.addEventListener('input', () => {
    stop();playbackPosition=Number(slider.value);three.setPlaybackPresentation(false);
    update(Number(slider.value));
  });
  play.addEventListener('click', () => (raf ? stop() : start()));
  markers.forEach(b=>b.title='查看本期後段概覽；拖動時間軸可查看早段與建造過程');
  markers.forEach((b) =>
    b.addEventListener('click', () => {
      stop();three.setPlaybackPresentation(false);
      const index=Number(b.dataset.phase),inspection=index===phases.length-1?index:index+.9;
      slider.value = String(inspection);playbackPosition=inspection;
      update(inspection);
    }),
  );
  const evidenceToggle = document.querySelector('.j3k-evidence-toggle'),
    panel = document.querySelector('.j3k-evidence-panel');
  evidenceToggle.addEventListener('click', () => {
    const open = panel.hasAttribute('hidden');
    panel.toggleAttribute('hidden', !open);
    evidenceToggle.setAttribute('aria-expanded', String(open));
  });
  const evidenceModes = [...document.querySelectorAll('[data-evidence-mode]')];
  evidenceModes.forEach((button) =>
    button.addEventListener('click', () => {
      const mode = button.dataset.evidenceMode;
      three.setEvidenceMode(mode);
      stage.dataset.evidenceMode = mode;
      evidenceModes.forEach((item) =>
        item.classList.toggle('is-active', item === button),
      );
      window.__JERUSALEM3000__.evidenceMode = mode;
      inheritance?.setEvidenceMode(mode);
      update(Number(slider.value));
    }),
  );
  const route = document.querySelector('.j3k-route-toggle');
  route.addEventListener('click', () => {
    const on = !stage.classList.contains('route-on');
    stage.classList.toggle('route-on', on);
    route.setAttribute('aria-pressed', String(on));
    if (on) {
      stop();
      slider.value = 8;
      update(8);
    }
  });
  three.setEvidenceMode('all');
  stage.dataset.evidenceMode = 'all';
  window.__JERUSALEM3000__.evidenceMode = 'all';
  update(0);
  const phaseAudit = three.auditCityPhases(phases.map((phase) => phase.id));
  window.__JERUSALEM3000__.phaseAudit = phaseAudit;
  stage.dataset.phaseAudit = phaseAudit.complete ? 'pass' : phaseAudit.ok ? 'deferred' : 'fail';
  if (!phaseAudit.ok) console.error('[Jerusalem 3000 phase audit]', phaseAudit.emptyPhases);
  update(0);
  window.__JERUSALEM3000__.status = 'ready';
  const production = auditProductionReadiness(window.__JERUSALEM3000__);
  window.__JERUSALEM3000__.production = production;
  window.__JERUSALEM3000__.productionReady = production.ok && phaseAudit.complete;
  stage.dataset.productionReady = String(window.__JERUSALEM3000__.productionReady);
  const completion = auditProductionCompletion(
    window.__JERUSALEM3000__,
    timeline,
  );
  window.__JERUSALEM3000__.completion = completion;
  window.__JERUSALEM3000__.complete = completion.ok && phaseAudit.complete;
  stage.dataset.complete = String(window.__JERUSALEM3000__.complete);
  if(!isEarlyLandscapePhase(window.__JERUSALEM3000__.historicalTime.phase)) badge.textContent = `JERUSALEM 3000 · TEMPORAL CITY · ${production.evidenceObjects || 0} EVIDENCE OBJECTS · ${production.constructionPieces || 0} PIECES`;
  window.addEventListener(
    'pagehide',
    () => {
      try {
        inheritance?.dispose?.();
      } catch {}
    },
    { once: true },
  );
} catch (error) {
  console.error('[Jerusalem 3000 core runtime]', error);
  window.__JERUSALEM3000__.status = 'error';
  window.__JERUSALEM3000__.productionReady = false;
  window.__JERUSALEM3000__.complete = false;
  window.__JERUSALEM3000__.error = String(error?.stack || error);
  stage.dataset.threeRuntime = 'error';
  stage.dataset.productionReady = 'false';
  stage.dataset.complete = 'false';
  badge.textContent = '3D CORE RUNTIME ERROR';
  if (!window.__JERUSALEM3000__.three)
    mount.innerHTML =
      '<div class="j3k-runtime-error">Three.js core runtime failed to start. Check console.</div>';
}
