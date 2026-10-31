import {createTempleSectionView} from './temple-section-view.js';
import {housingBoundaryStages} from './housing-boundary-stages.js';
import {createArchitecturalTerrainOcclusion} from './architectural-terrain-occlusion.js';
import {compileNamedCityGates,publishNamedCityGates,registerNamedGateApproaches} from './named-city-gates.js';
import {createCityEnclosureAudit} from './city-enclosure-audit.js';
import {createUrbanGroundPresentation} from './urban-ground-presentation.js';
import {completeUrbanCoverage} from './urban-coverage.js';
import {coreStageAt} from './landmark-chronology.js';
import {residentialEraProfile} from './residential-era-profiles.js';
import {applyMetricResidentialRegistration,augmentMetricEarlySettlement,metricResidentialPolicy,METRIC_RESIDENTIAL_PHASES} from './metric-residential-layout.js';
import {createHousingBoundaryAdmission,housingBoundaryAt} from './housing-boundary.js';
import {createRegionalLandforms} from './regional-landforms.js';
import {HERODIAN_DIMENSIONS} from './herodian-dimensions.js';
import {createDefenseTimeline,compileDefenseProfile} from './defense-timeline.js';
import {roadClearancePolygons} from './district-infill.js';
import {createCityConstructionPresentation} from './city-construction-presentation.js';
import {createPhaseDissolveView} from './phase-dissolve-view.js';
import {compileWallReference,createWallReferenceModel} from './old-city-wall-reference.js';
import {createSharedUrbanPlaces} from './shared-urban-places.js';
import {createSharedPlaceView} from './shared-place-view.js';
import {createPersistentCityWorld} from './persistent-city-world.js';
import {compileIndependentLaterSkeleton,buildIndependentLaterSkeleton} from './independent-later-skeleton.js';
import {collectSpatialSkeleton,SKELETON_WINDOW} from './spatial-skeleton.js';
import {declareHerodianSourceScopes,inspectSourceLifecycleContext} from './source-lifecycle-scope.js';
import {publishHerodianGeneratedEvents} from './herodian-generated-events.js';
import {allowsEvidence} from './evidence-visibility.js';
import {ERA_FOOTPRINTS,addEraFabric} from './legacy-era-fabric.js';
import {createLaterMorphologyLedger} from './later-morphology-ledger.js';
import {lifecycleStateAtPosition} from './construction-engine.js';
import {createCityFoundationRuntime,foundationOwnerFor} from './city-foundation-runtime.js';
import {createRoyalRelief} from './royal-relief.js';
import {createTerrainPresentation} from './terrain-presentation.js';
import {auditLocalPlanRegistry} from './local-plan-registration.js';
import {createWaterDefenseModelAdapter} from './water-defense-model-adapter.js';
import {compileWaterDefenseRegistration,bindWaterDefenseCore,waterDefenseState} from './water-defense-registration.js';
import {fitCityOverview} from './city-overview.js';
import {createPersianSanctuary} from './persian-sanctuary.js';
import {compileHellenisticSanctuary,createHellenisticSanctuary} from './hellenistic-sanctuary.js';
import {bindPeriodSpatialCore} from './period-spatial-ledger.js';
import { compilePeriodRegistration } from './period-spatial-registration.js';
import {createRoyalCity} from './royal-city.js';
import {loadCityData} from './city-data-loader.js';
import { createEarliestSettlement, isEarliestPhase, isEarlyLandscapePhase } from './earliest-settlement.js';
import { createSharedEraRuntime, isSharedSlicePhase, isSharedGenerationPhase } from './shared-era-runtime.js';
import * as THREE from 'three';
import { buildHerodianRoadGeometry } from './herodian-road-geometry.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { HeritageBuilder } from './heritage-builder.js';
import { addEvidenceArchitecture } from './jerusalem-architecture.js';
import { EvidenceResolutionEngine } from './evidence-resolution-engine.js';
import { auditEvidenceResolution } from './evidence-resolution-audit.js';
import {
  loadTerrainAuthority,
  loadCanonicalTerrain,
} from './terrain-runtime.js';
import { auditSpatialRegistrations } from './spatial-registration-audit.js';
import {
  auditArchitecturalGrammar,
  auditArchitecturalPieceDensity,
} from './architectural-grammar-audit.js';
import {
  buildPhase2UrbanMorphology,
  setPhase2MorphologyProgress,
} from './phase2-urban-morphology.js';
import {
  buildOttomanUrbanMorphology,
  setOttomanMorphologyProgress,
} from './ottoman-urban-morphology.js';
import {
  buildEraUrbanMorphology,
  setEraMorphologyProgress,
} from './phase2-era-morphology.js';
import { loadTemporalCityCore } from './temporal-city-core-adapter.js';
import { registerHerodianUrbanCore } from './herodian-urban-core-adapter.js';
import { buildHerodianParcelCore } from './herodian-parcel-core.js';
import { buildHerodianParcelArchitecture } from './herodian-typology-grammar.js';
import {
  createCityProjection,
  isCorePhase,
} from './city-lifecycle-projection.js';
const EVIDENCE_COLORS = {
  observed: 0x78806b,
  reconstructed: 0xb49b70,
  inferred: 0x9d8e79,
  disputed: 0x8e665c,
};
const TEMPORAL_COLORS = {
  observed: 0x8d8069,
  reconstructed: 0xb49b70,
  inferred: 0xa99b84,
  disputed: 0x8e665c,
};
const PROPAGATED_ERAS = new Set([
  'chalcolithic-early-bronze',
  'middle-bronze',
  'late-bronze-iron1',
  'late-first-temple',
  'persian-nehemiah',
  'hellenistic-hasmonean',
  'aelia',
  'byzantine',
  'early-islamic',
  'ayyubid-mamluk',
  'outside-walls',
  'modern',
]);
function makeMaterials() {
  const out = {};
  for (const [name, color] of Object.entries(EVIDENCE_COLORS))
    out[name] = new THREE.MeshStandardMaterial({
      color,
      roughness: 0.9,
      metalness: 0,
      transparent: true,
      opacity: name === 'disputed' ? 0.66 : 1,
      vertexColors: true,
    });
  return out;
}
function temporalEvidence(object) {
  const e = String(object.evidence || '').toLowerCase();
  if (e.includes('disputed')) return 'disputed';
  if (e.includes('observed') || e.includes('archaeological')) return 'observed';
  if (e.includes('reconstructed') || e.includes('textual'))
    return 'reconstructed';
  return 'inferred';
}
export function mountJerusalemThreeScene(mount, { onReady, onDistrictAcceptance } = {}) {
  const scene = new THREE.Scene(),
    camera = new THREE.PerspectiveCamera(34, 1, 0.1, 18000),
    renderer = new THREE.WebGLRenderer({
      antialias: true,
      logarithmicDepthBuffer: true,
      alpha: true,
      powerPreference: 'high-performance',
    }),
    reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches,
    coarsePointer = matchMedia('(pointer: coarse)').matches,
    pixelRatio = Math.min(devicePixelRatio, coarsePointer ? 1.25 : 1.75);
  renderer.setPixelRatio(pixelRatio);
  renderer.setClearColor(0xf4f1e9, 0);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1;
  renderer.shadowMap.enabled = !coarsePointer;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.shadowMap.autoUpdate = false;
  mount.replaceChildren(renderer.domElement);
  camera.position.set(3800, 2250, 5700);
  scene.add(new THREE.HemisphereLight(0xfaf7ef, 0x706a5c, 0.72));
  const key = new THREE.DirectionalLight(0xfff2e2, 2.4);
  key.position.set(-2200, 3800, 3000);
  key.castShadow = !coarsePointer;
  scene.add(key);
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.target.set(0, 120, 0);
  controls.enableDamping = true;
  controls.dampingFactor = 0.075;
  controls.minDistance = 700;
  controls.maxDistance = 11000;
  controls.minPolarAngle = 0.35;
  controls.maxPolarAngle = Math.PI * 0.51;
  controls.autoRotate = false;
  controls.autoRotateSpeed = 0.32;
  const root = new THREE.Group(),
    historical = new THREE.Group(),
    eraFabricLayer = new THREE.Group(),
    cityCoreLayer = new THREE.Group(),
    sharedEraLayer = new THREE.Group();
  cityCoreLayer.name = 'j3k-canonical-herodian-city';
  const templeSection=createTempleSectionView();
  renderer.localClippingEnabled=true;
  scene.add(root);
  root.add(historical, eraFabricLayer, cityCoreLayer, sharedEraLayer);
  const materials = makeMaterials(),
    builder = new HeritageBuilder(materials),
    temporalMaterials = {};
  for (const [name, color] of Object.entries(TEMPORAL_COLORS))
    temporalMaterials[name] = new THREE.MeshStandardMaterial({
      color,
      roughness: 0.94,
      transparent: true,
      opacity: name === 'disputed' ? 0.5 : 0.82,
    });
  let playbackPresentation=false,playbackDisplayPosition=null,renderedPlaybackPhase=null,renderedPlaybackReady=false;
  const presentationProgress=()=>playbackPresentation?Math.min(1,Math.max(0,(playbackDisplayPosition??timelinePosition)-Math.floor(timelinePosition))/.8):1;
  let currentProgress = 0,
    currentRuin = 0,
    terrainRuntime = null,
    foundationRuntime = null, cityEnclosureAudit=null, architecturalTerrainOcclusion=null,
    terrainPresentation = null, urbanGround=null, urbanGroundKey=null,
    terrainView = null,
    evidenceResolution = null,
    currentEvidenceMode = 'all',
    currentPhaseId = '',
    fabricMeshes = [],
    needsFrame = true,
    raf = 0,
    lastNow = performance.now(),
    phase2Morphology = null,
    cityCoreRuntime = null,
    cityProjection = null,
    evidenceProjection = null;
  renderer.localClippingEnabled=true;
  const constructionPresentation=createCityConstructionPresentation({root,getRecord:id=>cityCoreRuntime?.core.get(id)}),phaseDissolve=createPhaseDissolveView(mount);
  let landmarkLabelsEnabled=true;
  const landmarkView=createSharedPlaceView(mount,{anchors:()=>[]},{credit:false,ariaLabel:'當期已顯示地標量體（示意）',className:'j3k-landmark-references'});
  let regionalLandforms=null,regionalData=null,herodianScaleReport=null;
  let metricHellenisticRegistration=null;
  let housingBoundaryAdmission=null;
  let namedGates=null;
  let defenseTimeline=null,defenseData=null,canonicalProtected=[],independentLaterRegistrations=new Map(),fabricMaterialDisposer=null,persistentCityWorld=null,activeWorldEntry=null,sharedPlaces=null,sharedPlaceView=null,wallReference=null,wallReferenceModel=null,wallGateView=null,wallCredit=null;
  let sharedEraRuntime = null, laterMorphologyLedger=null, laterMorphologyBinding=null;
  let earliestSettlement = null, middleBronzeSettlement = null, lateBronzeSettlement = null, davidSettlement = null, priorCamera = null;
  let royalDataForGround=null;
  let retainedVisible = false, royalRelief=null, royalCity=null, persianSanctuary=null, hellenisticSanctuary=null, hellenisticSanctuaryData=null, hellenisticSanctuaryLayout=null, periodSpatialData=null, waterDefense=null, waterDefenseModel=null, localPlanAudit=[], periodRegistrations=new Map(), overviewPriorCamera=null, overviewFrame='', overviewInfo=null, timelinePosition=0, royalCameraStage='', templePriorCamera=null;
  const generationStatus = document.createElement('p');
  generationStatus.className = 'j3k-generation-status';
  generationStatus.setAttribute('role', 'status');
  generationStatus.hidden = true;
  mount.parentElement.appendChild(generationStatus);
  let eraRegistrationReference = null;
  function herodianPhaseActive() {
    return (
      currentPhaseId === 'herodian-jesus' ||
      currentPhaseId === 'roman-destruction'
    );
  }
  function phase2BuildActive() {
    return (
      currentPhaseId === 'herodian-jesus' ||
      currentPhaseId === 'david-solomon' ||
      currentPhaseId === 'crusader' ||
      currentPhaseId === 'ottoman' ||
      PROPAGATED_ERAS.has(currentPhaseId)
    );
  }
  function updateCityCoreVisibility() {
    earliestSettlement?.apply({phaseId:currentPhaseId,evidenceAllowed});
    middleBronzeSettlement?.apply({phaseId:currentPhaseId,evidenceAllowed});
    waterDefenseModel?.apply({position:timelinePosition,evidenceAllowed});
    lateBronzeSettlement?.apply({phaseId:currentPhaseId,evidenceAllowed});
    davidSettlement?.apply({phaseId:currentPhaseId,evidenceAllowed});
    royalCity?.apply({position:timelinePosition,ruin:currentRuin,evidenceAllowed});
    persianSanctuary?.apply({position:timelinePosition,evidenceAllowed});
    hellenisticSanctuary?.apply({position:timelinePosition,evidenceAllowed});
    royalRelief?.apply({phaseId:currentPhaseId,stage:royalCity?.diagnostics().stage,evidenceAllowed});
    const sharedActive = sharedEraRuntime?.apply({ phaseId: currentPhaseId, ruin: currentRuin, evidenceAllowed, retainedVisible,constructionProgress:1 });
    if (sharedActive) {
      clearFabric(); eraFabricLayer.visible = false;
    }
    if (cityProjection)
      cityProjection.apply({
        phaseId: currentPhaseId,
        ruin: currentRuin,
        constructionProgress:1,
        evidenceAllowed,
      });
  }
  function updateUrbanGround(){
    if(!urbanGround||!currentPhaseId||!cityCoreRuntime||!defenseData)return;
    const fraction=timelinePosition-Math.floor(timelinePosition),profile=defenseData.phases.find(p=>p.id===currentPhaseId),stage=royalCity?.diagnostics().stage;
    const bands=[...(profile?.walls||[]),...(profile?.extentReconstructions||[])].filter(w=>fraction>=w.fromOffset&&fraction<w.toOffset).map(w=>w.family||w.key).join('|');
    const key=currentPhaseId+'|'+(currentPhaseId==='david-solomon'?stage:'')+'|'+bands+'|'+evidenceAllowed('inferred');if(key===urbanGroundKey)return;urbanGroundKey=key;
    const registration=independentLaterRegistrations.get(currentPhaseId)||periodRegistrations.get(currentPhaseId==='babylonian-destruction'?'late-first-temple':currentPhaseId)||(['herodian-jesus','roman-destruction'].includes(currentPhaseId)?eraRegistrationReference:currentPhaseId==='hellenistic-hasmonean'?metricHellenisticRegistration:null);
    const zones=[];
    if(registration){
      for(const d of registration.districts)zones.push({polygon:d.geometry.polygon,kind:'quarter',explicitExpansion:d.metadata?.layoutRole==='extra-mural-expansion'});
      for(const r of registration.reservations||[])zones.push({polygon:r.geometry?.polygon||r.polygon,kind:r.metadata?.groundRole==='public-context'?'public':'reserved'});
      for(const r of registration.cores||[])zones.push({polygon:r.geometry.polygon,kind:'public'});
    }else for(const r of cityCoreRuntime.core.phase(currentPhaseId)){
      if(r.metadata.generationPhase!==currentPhaseId&&currentPhaseId!=='david-solomon')continue;
      if(r.type==='district'&&r.geometry?.polygon&&r.geometry.role!=='residential-model-envelope'&&!(r.metadata.regionId==='northern'&&stage!=='solomon'))zones.push({polygon:r.geometry.polygon,kind:'quarter'});
      if(r.type==='building'&&r.geometry?.bounds){const b=r.geometry.bounds;zones.push({polygon:[{x:b.min[0],z:b.min[2]},{x:b.max[0],z:b.min[2]},{x:b.max[0],z:b.max[2]},{x:b.min[0],z:b.max[2]}],kind:'quarter'});}
    }
    const boundary=housingBoundaryAt({phaseId:currentPhaseId,offset:fraction,defenseData,wallReference,royalData:currentPhaseId==='david-solomon'?royalDataForGround:null,royalStage:stage,origin:terrainRuntime.grid.origin});
    urbanGround.apply({key,phase:currentPhaseId,zones,rings:boundary.rings,allowed:evidenceAllowed('inferred')});
  }
  function applyTemporalState() {
    housingBoundaryAdmission?.restore();
    wallReferenceModel?.apply({position:timelinePosition,evidenceAllowed});
    defenseTimeline?.apply({phaseId:currentPhaseId,position:timelinePosition,evidenceAllowed});
    if(wallCredit)wallCredit.hidden=Boolean(terrainView)||!['ottoman','outside-walls','modern'].includes(currentPhaseId)||!evidenceAllowed('inferred');
    wallGateView?.setVisible(Boolean(terrainView)&&['ottoman','outside-walls','modern'].includes(currentPhaseId)&&evidenceAllowed('inferred'));
    sharedPlaceView?.setVisible(Boolean(terrainView)&&evidenceAllowed('inferred'));
    builder.setProgress(herodianPhaseActive() ? (playbackPresentation&&currentPhaseId==='herodian-jesus'?presentationProgress():currentProgress) : 0);
    evidenceProjection?.apply({
      phaseId: currentPhaseId,
      ruin: currentRuin,
      evidenceAllowed,
    });

    if (phase2Morphology && phase2BuildActive()) {
      if (currentPhaseId === 'ottoman')
        setOttomanMorphologyProgress(phase2Morphology, currentProgress);
      else if (PROPAGATED_ERAS.has(currentPhaseId))
        setEraMorphologyProgress(phase2Morphology, currentProgress, {
          ruined: false,
        });
      else
        setPhase2MorphologyProgress(phase2Morphology, currentProgress, {
          ruined: false,
        });
    }
    if (phase2Morphology && currentPhaseId === 'babylonian-destruction')
      setEraMorphologyProgress(phase2Morphology, 1, { ruined: true });
    laterMorphologyBinding?.apply(evidenceAllowed,{constructionProgress:1,position:timelinePosition});
    updateCityCoreVisibility();
    housingBoundaryAdmission?.apply();
    updateUrbanGround();
    templeSection.update(root);
    onDistrictAcceptance?.(sharedEraRuntime?.acceptance()??null);
    needsFrame = true;
  }
  function setBuildProgress(v) {
    currentProgress = Math.max(0, Math.min(1, v));
    applyTemporalState();
  }
  function setRuinProgress(v) {
    currentRuin = Math.max(0, Math.min(1, v));
    applyTemporalState();
  }
  function evidenceAllowed(level) {return allowsEvidence(currentEvidenceMode,level);}
  function setEvidenceMode(mode = 'all') {
    allowsEvidence(mode,'inferred');
    currentEvidenceMode = mode;phaseDissolve.clear();
    if (evidenceResolution)
      for (const mesh of builder.meshes) {
        const object = mesh.userData?.evidenceObject;
        mesh.visible =
          herodianPhaseActive() &&
          (!object || evidenceResolution.allows(object, mode));
      }
    eraFabricLayer.visible = mode !== 'disputed';
    applyTemporalState();
    needsFrame = true;
  }
  function clearFabric() {
    if(activeWorldEntry){persistentCityWorld.activate(null);activeWorldEntry=null;fabricMeshes=[];phase2Morphology=null;laterMorphologyBinding=null;return;}
    for (const mesh of fabricMeshes) {
      eraFabricLayer.remove(mesh);
      mesh.geometry.dispose();
    }
    fabricMaterialDisposer?.();fabricMaterialDisposer=null;
    fabricMeshes = [];
    phase2Morphology = null;laterMorphologyBinding=null;
  }
  function rebuildUrbanFabric(phaseId) {
    clearFabric();
    // Request only this bounded slice; other eras retain their established morphology.
    sharedEraRuntime?.request(phaseId,{retainedVisible});
    const foundationOwner=foundationOwnerFor(phaseId);
    if (['canonical-city','early-landscape'].includes(foundationOwner)) return;
    if (foundationOwner==='shared-period') {
      eraFabricLayer.visible = false;
      return;
    }
    eraFabricLayer.visible = currentEvidenceMode !== 'disputed';
    if(foundationOwner==='independent-later-skeleton'){activeWorldEntry=persistentCityWorld.activate(phaseId);fabricMeshes=activeWorldEntry.runtime.meshes;laterMorphologyBinding=activeWorldEntry.binding;laterMorphologyBinding.apply(evidenceAllowed,{constructionProgress:1,position:timelinePosition});return;}
    const ruined = phaseId.includes('destruction');
    if (foundationOwner === 'ottoman-morphology')
      phase2Morphology = buildOttomanUrbanMorphology(
        eraFabricLayer,
        temporalMaterials,
        terrainRuntime,
        { progress: currentProgress },
      );
    else if (PROPAGATED_ERAS.has(phaseId))
      phase2Morphology = buildEraUrbanMorphology(
        eraFabricLayer,
        phaseId,
        temporalMaterials,
        terrainRuntime,
        { progress: currentProgress },
      );
    else if (phaseId === 'babylonian-destruction')
      phase2Morphology = buildEraUrbanMorphology(
        eraFabricLayer,
        'late-first-temple',
        temporalMaterials,
        terrainRuntime,
        { progress: 1 },
      );
    else
      phase2Morphology = buildPhase2UrbanMorphology(
        eraFabricLayer,
        phaseId,
        temporalMaterials,
        terrainRuntime,
        { ruined, progress: phase2BuildActive() ? currentProgress : 1 },
      );
    if (phase2Morphology) {
      fabricMeshes = phase2Morphology.meshes;
      if(['crusader','ottoman'].includes(phaseId)){laterMorphologyBinding=laterMorphologyLedger.bind(phase2Morphology);laterMorphologyBinding.apply(evidenceAllowed,{constructionProgress:1,position:timelinePosition});}
      return;
    }
    fabricMeshes = addEraFabric(
      eraFabricLayer,
      phaseId,
      temporalMaterials.reconstructed,
      ruined,
      terrainRuntime,
    );
    if(fabricMeshes.length){laterMorphologyBinding=laterMorphologyLedger.bind({phaseId,meshes:fabricMeshes,grammar:'legacy-era-footprint-masses',fixedVisibility:true});laterMorphologyBinding.apply(evidenceAllowed,{constructionProgress:1,position:timelinePosition});}
  }
  function updatePeriodOverview(phaseId,force=false){
    if(terrainView)return;
    const independent=independentLaterRegistrations.has(phaseId);
    const framePhase=phaseId==='babylonian-destruction'?'late-first-temple':phaseId;
    const includesEarlier=phaseId==='persian-nehemiah'&&retainedVisible;
    const expansion=['outside-walls','modern'].includes(phaseId);
    const independentFrame=expansion?'independent-expansion-shared-window':'independent-later-shared-window';
    const frameKey=independent?independentFrame:framePhase+(includesEarlier?':retained':'');
    if((!independent&&!periodRegistrations.has(framePhase))||(!force&&overviewFrame===frameKey))return;
    if(!overviewPriorCamera)overviewPriorCamera={position:camera.position.clone(),target:controls.target.clone(),minDistance:controls.minDistance};
    const registrations=independent?[...independentLaterRegistrations.values()].filter(r=>['outside-walls','modern'].includes(r.phase)===expansion):[periodRegistrations.get(framePhase),...(includesEarlier?[periodRegistrations.get('late-first-temple')]:[])];
    const points=registrations.flatMap(r=>r.districts.flatMap(d=>d.geometry.polygon.flatMap(p=>{const y=terrainRuntime.heightAtWorld(p.x,p.z);return[new THREE.Vector3(p.x,y,p.z),new THREE.Vector3(p.x,y+32,p.z)];})));
    if(independent&&wallReference&&registrations.some(r=>r.occupationEnvelope))for(const line of wallReference.lines)for(const p of line){const y=terrainRuntime.heightAtWorld(p.x,p.z);points.push(new THREE.Vector3(p.x,y,p.z),new THREE.Vector3(p.x,y+wallReference.height,p.z));}
    if(defenseTimeline)for(const r of registrations)for(const p of defenseTimeline.pointsFor(r.phase)){const y=terrainRuntime.heightAtWorld(p.x,p.z);points.push(new THREE.Vector3(p.x,y,p.z),new THREE.Vector3(p.x,y+10,p.z));}
    const framing=fitCityOverview({points,aspect:camera.aspect,fov:camera.fov});
    controls.minDistance=35;controls.target.copy(framing.target);camera.position.copy(framing.position);controls.update();overviewFrame=frameKey;
    overviewInfo={framePhase:independent?independentFrame:framePhase,includesEarlier,distance:framing.distance,bounds:framing.bounds,authority:framing.authority};
  }
  function frameRoyalRelief(){
    if(!royalRelief)return;
    const [south,,north]=royalRelief.profile.anchors;
    controls.minDistance=35;controls.target.set((south.x+north.x)/2,(south.y+north.y)/2+10,(south.z+north.z)/2);
    camera.position.copy(controls.target).add(camera.aspect<1?new THREE.Vector3(2400,800,400):new THREE.Vector3(900,300,150));controls.update();needsFrame=true;
  }
  function setTemporalCityState(objects = [], position = 0, phaseId = '') {
    const previousPhase = currentPhaseId,
      phaseChanged = previousPhase !== phaseId;
    if(phaseChanged)renderedPlaybackReady=false;
    currentPhaseId = phaseId;
    timelinePosition=position;
    if(!terrainView){
    if(phaseChanged&&templePriorCamera){camera.position.copy(templePriorCamera.position);controls.target.copy(templePriorCamera.target);controls.minDistance=templePriorCamera.minDistance;templePriorCamera=null;controls.update();}
    if(phaseChanged&&overviewPriorCamera&&!['late-first-temple','babylonian-destruction','persian-nehemiah'].includes(phaseId)&&!independentLaterRegistrations.has(phaseId)){camera.position.copy(overviewPriorCamera.position);controls.target.copy(overviewPriorCamera.target);controls.minDistance=overviewPriorCamera.minDistance;overviewPriorCamera=null;overviewFrame='';overviewInfo=null;controls.update();}
    if(phaseChanged && earliestSettlement) {
      if(isEarlyLandscapePhase(phaseId)) {
        if(!isEarlyLandscapePhase(previousPhase)) priorCamera={position:camera.position.clone(),target:controls.target.clone(),minDistance:controls.minDistance};
        controls.minDistance=35;
        const landscape=isEarliestPhase(phaseId)?earliestSettlement:phaseId==='middle-bronze'?middleBronzeSettlement:phaseId==='late-bronze-iron1'?lateBronzeSettlement:davidSettlement;
        controls.target.copy(landscape.focus);
        camera.position.copy(landscape.focus).add(isEarliestPhase(phaseId)?new THREE.Vector3(120,105,160):phaseId==='david-solomon'?(camera.aspect<1?new THREE.Vector3(275,285,400):new THREE.Vector3(180,190,270)):new THREE.Vector3(150,125,190));
        controls.update();
      } else if(priorCamera) {
        camera.position.copy(priorCamera.position);controls.target.copy(priorCamera.target);controls.minDistance=priorCamera.minDistance;priorCamera=null;controls.update();
      }
    }
    if(phaseId==='david-solomon'&&royalCity){
      const stage=objects.find(o=>o.id==='j3k:object:first-temple')?.state==='absent'?'david':'solomon';
      royalCameraStage=stage;
      if(phaseChanged)frameRoyalRelief();
    }
    if(phaseChanged)updatePeriodOverview(phaseId);
    }
    applyTemporalState();
    if (phaseChanged && terrainRuntime) {
      rebuildUrbanFabric(phaseId);
      applyTemporalState();
    }
    // Anchor metadata remains in the ledger. A source awaiting spatial
    // registration must not become a hash-positioned box or monument slab.
    needsFrame = true;
  }
  const ready = Promise.all([
    loadCityData('./data/objects/herodian-30ce.json'),
    loadTerrainAuthority(),
  ]).then(async ([ledger, { manifest }]) => {
    evidenceResolution = new EvidenceResolutionEngine(ledger.objects);
    terrainRuntime = await loadCanonicalTerrain(manifest, root);
    if (!terrainRuntime)
      throw new Error('Canonical Jerusalem DEM payload missing');
    terrainPresentation=createTerrainPresentation(terrainRuntime.mesh,{datum:terrainRuntime.grid.verticalDatumOffsetMetres});
    urbanGround=createUrbanGroundPresentation(terrainRuntime.mesh);
    regionalData=await loadCityData('./data/terrain/regional-landforms.v1.json');regionalLandforms=createRegionalLandforms(root,mount,regionalData,terrainRuntime);
    const evidenceResolutionAudit = auditEvidenceResolution(ledger.objects),
      registrationAudit = auditSpatialRegistrations(
        ledger.objects,
        terrainRuntime,
      ),
      architecturalGrammarAudit = auditArchitecturalGrammar(ledger.objects),
      piecesBefore = builder.pieces;
    let renderableObjects = 0;
    const exclusions = [];
    for (const object of ledger.objects) {
      builder.currentObject = object;
      const registered = addEvidenceArchitecture(
        builder,
        object,
        terrainRuntime,
      );
      builder.currentObject = null;
      if (registered) {
        renderableObjects++;
        if (['platform-enclosure', 'fortress'].includes(object.kind)) {
          const w = object.kind === 'fortress' ? 156 : HERODIAN_DIMENSIONS.platform.eastWest+20,
            d = object.kind === 'fortress' ? 136 : HERODIAN_DIMENSIONS.platform.northSouth+20,
            x = registered.east,
            z = -registered.north;
          exclusions.push({
            objectId: object.id,
            authority: 'rendered-reconstruction-footprint',
            polygon: [
              { x: x - w / 2, z: z - d / 2 },
              { x: x + w / 2, z: z - d / 2 },
              { x: x + w / 2, z: z + d / 2 },
              { x: x - w / 2, z: z + d / 2 },
            ],
          });
        }
      }
    }
    const architecturalPieceAudit = auditArchitecturalPieceDensity(
      ledger.objects,
      piecesBefore,
      builder.pieces,
    );
    builder.finish(historical);
    const sanctuaryMesh=builder.meshes.find(m=>m.userData.evidenceObject?.id==='j3k:object:inner-temple');if(sanctuaryMesh){const b=new THREE.Box3().setFromObject(sanctuaryMesh);sanctuaryMesh.userData.templeSectionHeight=terrainRuntime.sampleElevation(31.778,35.235)+HERODIAN_DIMENSIONS.platform.pavingThickness+HERODIAN_DIMENSIONS.relativeCourtLevels.priests+6*HERODIAN_DIMENSIONS.cubitMetres+4;sanctuaryMesh.userData.landmarkFocus={x:b.min.x+11*HERODIAN_DIMENSIONS.cubitMetres+(HERODIAN_DIMENSIONS.sanctuary.eastWest-10*HERODIAN_DIMENSIONS.cubitMetres)/2,y:b.max.y,z:(b.min.z+b.max.z)/2};}
    architecturalTerrainOcclusion=createArchitecturalTerrainOcclusion(terrainRuntime,{platform:builder.meshes.find(m=>m.userData.evidenceObject?.id==='j3k:object:temple-mount-enclosure-herodian'),progress:builder.progress});
    herodianScaleReport={dimensions:structuredClone(HERODIAN_DIMENSIONS),models:builder.meshes.map(mesh=>{const b=new THREE.Box3().setFromObject(mesh),size=b.getSize(new THREE.Vector3());return {id:mesh.userData.evidenceObject.id,bounds:{min:b.min.toArray(),max:b.max.toArray()},eastWest:size.x,northSouth:size.z,verticalEnvelope:size.y};}),measurementScope:'canonical-standing-mesh-not-current-ruin',precinctGround:terrainRuntime.sampleElevation(31.778,35.235),ancientPlacementVerified:false};
    for (const mesh of builder.meshes) {
      const object = mesh.userData.evidenceObject;
      const anchor = object.spatial.anchor;
      mesh.userData.cityObject = {
        objectId: object.id,
        confidence: temporalEvidence(object),
        terrainGround: terrainRuntime.sampleElevation(anchor.lat, anchor.lon),
      };
    }
    evidenceProjection = createCityProjection(historical, builder.meshes,{
      stateForObject(id){const core=cityCoreRuntime?.core,record=core?.get(id);return record?.lifecycle.events.length?lifecycleStateAtPosition({lifecycleEvents:record.lifecycle.events},{phases:[...core.phases.values()]},timelinePosition):'unresolved';}
    });
    historical.visible = false;
    const phaseSeed = Object.keys(ERA_FOOTPRINTS).map((id) => ({ id }));
    try {
      const loaded = await loadTemporalCityCore(phaseSeed, {
        terrain: terrainRuntime,
      });
      await registerHerodianUrbanCore(loaded.core);
      eraRegistrationReference = applyMetricResidentialRegistration(await loadCityData('./data/urban/herodian-30ce.registration.json'));
      metricHellenisticRegistration=applyMetricResidentialRegistration(await loadCityData('./data/urban/hellenistic-metric.registration.v1.json'));
      hellenisticSanctuaryData=await loadCityData('./data/urban/hellenistic-sanctuary.v1.json');
      hellenisticSanctuaryLayout=compileHellenisticSanctuary(hellenisticSanctuaryData,metricHellenisticRegistration,terrainRuntime.grid.origin);
      metricHellenisticRegistration.reservations=hellenisticSanctuaryLayout.reservations.map(r=>({...r,metadata:{...r.metadata,groundRole:'public-context'}}));
      for(const r of eraRegistrationReference.reservations||[])r.metadata={...r.metadata,groundRole:'public-context'};
      defenseData=await loadCityData('./data/urban/defense-timeline.v1.json');
      for(const registration of [eraRegistrationReference,metricHellenisticRegistration])completeUrbanCoverage(registration,{rings:housingBoundaryAt({phaseId:registration.phase,offset:.9,defenseData,origin:terrainRuntime.grid.origin}).rings});
      for(const d of eraRegistrationReference.districts.filter(d=>d.metadata?.coverageResidual))loaded.core.register({...d,phaseIds:['herodian-jesus'],source:{...d.source,dataset:'herodian-30ce.registration'}});
      eraRegistrationReference.metricHousingRings=housingBoundaryAt({phaseId:'herodian-jesus',offset:.9,defenseData,origin:terrainRuntime.grid.origin}).rings;
      canonicalProtected=[...exclusions];
      const defenseProfile=compileDefenseProfile(defenseData,'herodian-jesus',eraRegistrationReference.roads,terrainRuntime,{exclusions});
      exclusions.push(...roadClearancePolygons([...defenseProfile.roads,...defenseProfile.walls.map(w=>({geometry:{points:w.points}}))],10));
      const parcels = await buildHerodianParcelCore(
        loaded.core,
        terrainRuntime,
        { exclusions,registration:eraRegistrationReference },
      );
      const overviewMaterial=temporalMaterials.inferred.clone();overviewMaterial.transparent=false;overviewMaterial.opacity=1;overviewMaterial.color.setHex(0xb9a27e);
      const architecture = buildHerodianParcelArchitecture(
        cityCoreLayer,
        loaded.core,
        {...temporalMaterials,lowRise:overviewMaterial},
        terrainRuntime,{overview:true},
      );
      architecture.overviewMaterial=overviewMaterial;
      cityCoreRuntime = {
        core: loaded.core,
        parcels,
        architecture,
        validation: loaded.core.validate(),
      };
      laterMorphologyLedger=createLaterMorphologyLedger(loaded.core);
      const independentLaterData=await loadCityData('./data/urban/roman-byzantine-islamic.skeleton.v1.json');
      for(const phase of ['aelia','byzantine','early-islamic'])independentLaterRegistrations.set(phase,compileIndependentLaterSkeleton(independentLaterData,phase,terrainRuntime.grid.origin));
      wallReference=compileWallReference(await loadCityData('./data/urban/old-city-walls.reference.v1.json'),terrainRuntime);
      namedGates=compileNamedCityGates(await loadCityData('./data/urban/named-city-gates.v1.json'),wallReference,terrainRuntime);wallReference.namedGates=namedGates;publishNamedCityGates(loaded.core,namedGates);
      wallCredit=document.createElement('small');wallCredit.className='j3k-wall-reference-credit';wallCredit.textContent='城牆：現代地圖參照／高度示意 · © OpenStreetMap contributors · ODbL';wallCredit.hidden=true;mount.parentElement.after(wallCredit);
      const medievalData=await loadCityData('./data/urban/medieval-ottoman.skeleton.v1.json');
      for(const phase of ['crusader','ayyubid-mamluk','ottoman'])independentLaterRegistrations.set(phase,compileIndependentLaterSkeleton(medievalData,phase,terrainRuntime.grid.origin,{wallReference}));
      const expansionData=await loadCityData('./data/urban/expansion-modern.skeleton.v1.json');
      for(const phase of ['outside-walls','modern'])independentLaterRegistrations.set(phase,compileIndependentLaterSkeleton(expansionData,phase,terrainRuntime.grid.origin,{wallReference}));
      for(const registration of independentLaterRegistrations.values())registerNamedGateApproaches(registration,namedGates);
      wallReferenceModel=createWallReferenceModel(root,{reference:wallReference,terrain:terrainRuntime,core:loaded.core});
      wallGateView=createSharedPlaceView(mount,wallReferenceModel,{credit:false});
      for(const [phase,registration]of independentLaterRegistrations){const stages=housingBoundaryStages({phaseId:phase,defenseData,wallReference,origin:terrainRuntime.grid.origin});registration.boundaryStages=stages;completeUrbanCoverage(registration,{rings:stages.rings});}
      sharedPlaces=createSharedUrbanPlaces({terrain:terrainRuntime,phases:[...loaded.core.phases.values()],core:loaded.core});
      sharedPlaceView=createSharedPlaceView(mount,sharedPlaces,{credit:false});
      persistentCityWorld=createPersistentCityWorld({parent:eraFabricLayer,phases:[...independentLaterRegistrations.keys()],build:(group,phase)=>buildIndependentLaterSkeleton(group,independentLaterRegistrations.get(phase),temporalMaterials,terrainRuntime),publish:runtime=>laterMorphologyLedger.bind(runtime)});
      if (!parcels.blockCount || !parcels.count || !architecture.buildings || !cityCoreRuntime.validation.ok)
        throw new Error(`Canonical city incomplete: ${parcels.blockCount || 0} blocks, ${parcels.count || 0} parcels, ${architecture.buildings || 0} buildings`);
      architecture.meshes.push(
        ...buildHerodianRoadGeometry(
          cityCoreLayer,
          parcels.roads,
          temporalMaterials,
          terrainRuntime,
        ),
      );
      const generatedEvents=publishHerodianGeneratedEvents(loaded.core,{registration:eraRegistrationReference,buildingIds:architecture.buildingIds,meshes:architecture.meshes});
      cityCoreRuntime.generatedEvents=generatedEvents.summary;
      cityCoreRuntime.sourceScopes=declareHerodianSourceScopes(loaded.core);
      cityProjection = createCityProjection(cityCoreLayer, architecture.meshes,{stateForObject:(id,phase)=>generatedEvents.stateFor(id,phase),stateForInfrastructure:true});
      cityCoreRuntime.projection = cityProjection;
      periodSpatialData = await loadCityData('./data/urban/first-temple-persian.spatial.v1.json');
      for(const phase of ['late-first-temple','persian-nehemiah']){
        const registration=compilePeriodRegistration(periodSpatialData,phase,terrainRuntime.grid.origin),template=loaded.core.get(registration.districts[0].id);
        completeUrbanCoverage(registration,{rings:housingBoundaryAt({phaseId:phase,offset:.9,defenseData,origin:terrainRuntime.grid.origin}).rings});
        for(const d of registration.districts.filter(d=>d.metadata?.coverageResidual))loaded.core.register({...d,phaseIds:template.phaseIds,lifecycle:template.lifecycle});
        periodRegistrations.set(phase,registration);bindPeriodSpatialCore(loaded.core,registration);
      }
      sharedEraRuntime = createSharedEraRuntime(sharedEraLayer, {
        ledgerCore:loaded.core,overview:true,
        getRegistration:phase => {const registration=applyMetricResidentialRegistration(periodRegistrations.get(phase)||metricHellenisticRegistration,phase);registration.metricHousingRings=housingBoundaryAt({phaseId:phase,offset:.9,defenseData,origin:terrainRuntime.grid.origin}).rings;return registration;},
        getExclusions:phase=>[...(royalCity?.exclusionsFor(phase)||[]),
        ...(phase==='hellenistic-hasmonean'?hellenisticSanctuaryLayout.roadExclusions:[]),...(defenseTimeline?.exclusionsFor(phase)||[])],
        reference: eraRegistrationReference, footprint: ERA_FOOTPRINTS['late-first-temple'],
        successorFootprint: ERA_FOOTPRINTS['persian-nehemiah'],
        expansionFootprint: ERA_FOOTPRINTS['hellenistic-hasmonean'],
        terrain: terrainRuntime, materials: temporalMaterials,
        onChange: () => { renderedPlaybackReady=false;applyTemporalState(); needsFrame = true; },
        onProgress: ({ completed, total }) => {
          if (isSharedGenerationPhase(currentPhaseId) && completed % 4 === 0)
            generationStatus.textContent = `城市生成中 · ${completed}/${total}`;
        },
      });
    } catch (error) {
      throw new Error(`Canonical city construction failed: ${error.message}`, {
        cause: error,
      });
    }
    const settlementResponse=await fetch('./data/settlement/earliest.v1.json',{cache:'no-store'});
    if(!settlementResponse.ok) throw new Error('Earliest settlement data unavailable');
    earliestSettlement=createEarliestSettlement(root,{data:augmentMetricEarlySettlement(await settlementResponse.json(),terrainRuntime),terrain:terrainRuntime,ledgerCore:cityCoreRuntime.core,overview:true});
    const middleResponse=await fetch('./data/settlement/middle-bronze.v1.json',{cache:'no-store'});
    if(!middleResponse.ok) throw new Error('Middle Bronze settlement data unavailable');
    middleBronzeSettlement=createEarliestSettlement(root,{data:augmentMetricEarlySettlement(await middleResponse.json(),terrainRuntime),terrain:terrainRuntime,ledgerCore:cityCoreRuntime.core,overview:true});
    const lateResponse=await fetch('./data/settlement/late-bronze-iron1.v1.json',{cache:'no-store'});
    if(!lateResponse.ok) throw new Error('Late Bronze landscape data unavailable');
    lateBronzeSettlement=createEarliestSettlement(root,{data:augmentMetricEarlySettlement(await lateResponse.json(),terrainRuntime),terrain:terrainRuntime,ledgerCore:cityCoreRuntime.core,overview:true});
    const waterDefenseData=await loadCityData('./data/urban/water-defense.registration.v1.json');
    localPlanAudit=auditLocalPlanRegistry(await loadCityData('./data/urban/water-defense.local-plans.v1.json'),terrainRuntime.grid.origin);
    waterDefense=compileWaterDefenseRegistration(waterDefenseData,terrainRuntime.grid.origin);bindWaterDefenseCore(cityCoreRuntime.core,waterDefense);
    for(const admission of localPlanAudit){const record=cityCoreRuntime.core.get(admission.objectId);if(!record)throw new Error('Local plan target missing from shared ledger');cityCoreRuntime.core.register({...record,metadata:{...record.metadata,localPlanAdmission:admission}});}
    waterDefenseModel=createWaterDefenseModelAdapter({runtime:middleBronzeSettlement,core:cityCoreRuntime.core,registration:waterDefense});
    const davidData=await loadCityData('./data/settlement/david-solomon.v1.json');royalDataForGround=davidData;
    davidSettlement=createEarliestSettlement(root,{data:augmentMetricEarlySettlement(davidData,terrainRuntime),terrain:terrainRuntime,ledgerCore:cityCoreRuntime.core,overview:true});
    royalCity=createRoyalCity(root,{data:davidData,terrain:terrainRuntime,core:cityCoreRuntime.core});
    royalRelief=createRoyalRelief(root,mount,{data:davidData,terrain:terrainRuntime});
    persianSanctuary=createPersianSanctuary(root,{data:periodSpatialData,terrain:terrainRuntime,core:cityCoreRuntime.core});
    hellenisticSanctuary=createHellenisticSanctuary(root,{data:hellenisticSanctuaryData,layout:hellenisticSanctuaryLayout,terrain:terrainRuntime,core:cityCoreRuntime.core});
    const defenseRoadsForPhase=phase=>{
      if(independentLaterRegistrations.has(phase))return independentLaterRegistrations.get(phase).roads;
      if(periodRegistrations.has(phase))return periodRegistrations.get(phase).roads;
      if(phase==='babylonian-destruction')return periodRegistrations.get('late-first-temple').roads;
      if(phase==='herodian-jesus'||phase==='roman-destruction')return eraRegistrationReference.roads;
      if(phase==='hellenistic-hasmonean')return metricHellenisticRegistration.roads;
      return [];
    };
    defenseTimeline=createDefenseTimeline({data:defenseData,phases:[...cityCoreRuntime.core.phases.values()],core:cityCoreRuntime.core,terrain:terrainRuntime,parent:root,roadsForPhase:defenseRoadsForPhase,exclusionsForPhase:phase=>independentLaterRegistrations.has(phase)?[...independentLaterRegistrations.get(phase).cores.map(c=>({polygon:c.geometry.polygon})),...independentLaterRegistrations.get(phase).reservations.map(c=>({polygon:c.geometry.polygon}))]:phase==='herodian-jesus'||phase==='roman-destruction'?canonicalProtected:[...(royalCity?.exclusionsFor(phase)||[]),...(periodRegistrations.get(phase)?.reservations||[]),...(phase==='hellenistic-hasmonean'?hellenisticSanctuaryLayout.reservations:[])]});
    for(const [phase,registration]of independentLaterRegistrations){
      applyMetricResidentialRegistration(registration,phase);
      registration.defenseReservations=defenseTimeline.exclusionsFor(phase);
      const stages=registration.boundaryStages;
      // An unwalled interval must not inherit a future enclosure constraint.
      if(stages.allIntervalsClosed)registration.housingBoundaryRings=stages.rings;
    }
    housingBoundaryAdmission=createHousingBoundaryAdmission({root,core:cityCoreRuntime.core,boundaryFor:()=>housingBoundaryAt({phaseId:currentPhaseId,offset:timelinePosition-Math.floor(timelinePosition),defenseData,wallReference,royalData:davidData,royalStage:royalCity?.diagnostics().stage,origin:terrainRuntime.grid.origin})});
    cityEnclosureAudit=createCityEnclosureAudit({root,core:cityCoreRuntime.core,boundaryFor:()=>housingBoundaryAt({phaseId:currentPhaseId,offset:timelinePosition-Math.floor(timelinePosition),defenseData,wallReference,royalData:davidData,royalStage:royalCity?.diagnostics().stage,origin:terrainRuntime.grid.origin})});
    foundationRuntime=createCityFoundationRuntime({core:cityCoreRuntime.core,terrain:terrainRuntime,root,getCurrentPhase:()=>currentPhaseId,getPosition:()=>timelinePosition});
    const bounds = new THREE.Box3()
      .setFromObject(cityCoreLayer)
      .union(new THREE.Box3().setFromObject(historical));
    const centre = bounds.getCenter(new THREE.Vector3());
    controls.target.copy(centre);
    const size = bounds.getSize(new THREE.Vector3());
    const distance = Math.max(size.x, size.z) * 1.65;
    camera.position
      .copy(centre)
      .add(
        new THREE.Vector3(distance * 0.65, distance * 0.52, distance * 0.85),
      );
    controls.update();
    applyTemporalState();
    const info = {
      renderableObjects,
      ledgerObjects: ledger.objects.length,
      constructionPieces: builder.pieces,
      temporalRuntime: 'canonical-herodian-ruin-slice',
      objectContinuityPhases: ['herodian-jesus', 'roman-destruction'],
      transformationRuntime: 'reversible-standing-to-ruin',
      renderProfile: coarsePointer ? 'coarse-pointer' : 'desktop',
      terrain: 'canonical-dem',
      spatialRegistration: 'canonical-dem-enu',
      evidenceResolutionAudit,
      registrationAudit,
      architecturalGrammarAudit,
      architecturalPieceAudit,
      cityCoreAB: cityCoreRuntime?.error
        ? { ok: false, error: cityCoreRuntime.error }
        : {
            ok: true,
            blocks: cityCoreRuntime?.parcels?.blockCount || 0,
            parcels: cityCoreRuntime?.parcels?.count || 0,
            buildings: cityCoreRuntime?.architecture?.buildings || 0,
            semanticBoxes: cityCoreRuntime?.architecture?.semanticBoxes ?? null,
            validation: cityCoreRuntime?.validation,
          },
    };
    onReady?.(info);
    return info;
  });
  controls.addEventListener('change', () => (needsFrame = true));
  function frameRegionalOverview(){
    const window=regionalData.window,points=[];
    for(const x of [window.minX,window.maxX])for(const z of [window.minZ,window.maxZ])points.push(new THREE.Vector3(x,terrainRuntime.heightAtWorld(x,z),z));
    for(const a of regionalLandforms.snapshot().anchors)points.push(new THREE.Vector3(a.x,a.y,a.z));
    camera.fov=48;const frame=fitCityOverview({points,aspect:camera.aspect,fov:camera.fov,landscape:true,viewDirection:[.28,.72,1.8]});camera.far=Math.max(camera.far,frame.distance*3);camera.updateProjectionMatrix();controls.maxDistance=frame.distance*2;camera.position.copy(frame.position);controls.target.copy(frame.target);controls.minDistance=35;controls.autoRotate=false;
  }
  const resize = () => {
    const w = Math.max(1, mount.clientWidth),
      h = Math.max(1, mount.clientHeight);
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    if(terrainView&&regionalLandforms)frameRegionalOverview();else if(independentLaterRegistrations.has(currentPhaseId))updatePeriodOverview(currentPhaseId,true);
    needsFrame = true;
  };
  const ro = new ResizeObserver(resize);
  ro.observe(mount);
  resize();
  let frameCount = 0;
  function render(now) {
    const dt = Math.min((now - lastNow) / 1000, 0.1);
    lastNow = now;
    const changed = controls.update(dt);
    if(changed)phaseDissolve.clear();
    if (needsFrame || changed || controls.autoRotate) {
      try {
        housingBoundaryAdmission?.restore();
        housingBoundaryAdmission?.apply();
    updateUrbanGround();
        camera.updateMatrixWorld();
        const royalBoxes=royalRelief?.project(camera)||[];
        const placeBoxes=sharedPlaceView?.project(camera,royalBoxes)||royalBoxes;
        const geographyBoxes=regionalLandforms?.project(camera,placeBoxes)||placeBoxes;
        const gateBoxes=wallGateView?.project(camera,geographyBoxes)||geographyBoxes;
        const phaseIndex=Math.floor(timelinePosition),fraction=(playbackDisplayPosition??timelinePosition)-phaseIndex,phaseReady=!isSharedGenerationPhase(currentPhaseId)||sharedEraRuntime?.status==='ready';
        if(currentPhaseId)constructionPresentation.apply({phaseId:currentPhaseId,phaseIndex,position:playbackDisplayPosition??timelinePosition,active:playbackPresentation,ruin:['babylonian-destruction','roman-destruction'].includes(currentPhaseId)});
        landmarkView.setAnchors(constructionPresentation.landmarks());landmarkView.setVisible(landmarkLabelsEnabled);const labelBoxes=landmarkView.project(camera,gateBoxes);mount.parentElement.style.setProperty('--map-label-rail-height',`${Math.max(0,...labelBoxes.map(b=>b.bottom-mount.clientHeight+20))}px`);
        architecturalTerrainOcclusion?.apply(activeWorldEntry?.runtime.landmarkMeshes?.find(m=>m.visible&&m.userData.occupiedFoundation));
        phaseDissolve.before({phaseId:currentPhaseId,index:phaseIndex,fraction,active:playbackPresentation,ready:phaseReady});
        renderer.render(scene, camera);
        phaseDissolve.after(renderer.domElement,{phaseId:currentPhaseId,fraction,ready:phaseReady&&playbackPresentation});
        frameCount++;
        const sharedState = sharedEraRuntime?.diagnostics();
        renderedPlaybackPhase=currentPhaseId;renderedPlaybackReady=!isSharedGenerationPhase(currentPhaseId)||sharedState?.status==='ready';
        const activeSharedSlice = isSharedGenerationPhase(currentPhaseId);
        generationStatus.hidden = !activeSharedSlice || !['generating', 'error'].includes(sharedState?.status);
        generationStatus.textContent = sharedState?.status === 'error'
          ? '城市生成失敗，暫時顯示示意圖。請重新切換時代再試。'
          : `城市生成中 · ${sharedState?.completed || 0}/${sharedState?.total || 0}`;
        const state = window.__JERUSALEM3000__;
        if (state)
          state.renderDiagnostics = {
            frames: frameCount,
            canvasWidth: renderer.domElement.width,
            canvasHeight: renderer.domElement.height,
            webgl: !renderer.getContext().isContextLost(),
            sceneChildren: scene.children.length,
            cityProjection: cityProjection?.diagnostics(),
            evidenceProjection:evidenceProjection?.diagnostics(),
            sharedEra: sharedState,
            earliestSettlement: earliestSettlement?.diagnostics(),
            middleBronzeSettlement: middleBronzeSettlement?.diagnostics(),
            waterDefenseModel:waterDefenseModel?.diagnostics(),
            localPlanAudit,
            lateBronzeSettlement: lateBronzeSettlement?.diagnostics(),
            davidSettlement: davidSettlement?.diagnostics(),
            royalCity:royalCity?.diagnostics(),
            royalRelief:royalRelief?.profile,
            persianSanctuary:persianSanctuary?.diagnostics(),
            hellenisticSanctuary:hellenisticSanctuary?.diagnostics(),
            cityOverview:overviewInfo,
            foundation:currentPhaseId?foundationRuntime?.describe(currentPhaseId):null,
            terrainPresentation:{...terrainPresentation?.diagnostics,logarithmicDepthBuffer:renderer.capabilities.logarithmicDepthBuffer,architecturalOcclusion:architecturalTerrainOcclusion?.diagnostics(),occupation:urbanGround?.diagnostics(),precinctReservations:(independentLaterRegistrations.get(currentPhaseId)||periodRegistrations.get(currentPhaseId))?.precinctReservationAudit||null,surfaceId:terrainRuntime?.mesh.uuid,gridId:terrainRuntime?.grid.id,nominalResolutionMetres:terrainRuntime?.grid.nominalResolutionMetres,regionalLandforms:regionalLandforms?.diagnostics(),historicalObjectContinuityComplete:false,overviewActive:!!terrainView,camera:camera.position.toArray(),target:controls.target.toArray()},
            housingBoundary:housingBoundaryAdmission?.snapshot({includeIds:false}),
            wallReference:wallReferenceModel?.diagnostics(),
            defenseTimeline:defenseTimeline?.snapshot({includeSourceAudit:false}),
            cityWorld:persistentCityWorld?.diagnostics(),
            constructionPresentation:constructionPresentation.diagnostics(),
            landmarks:{phase:currentPhaseId,...landmarkView.diagnostics(),visibleModelAnchors:constructionPresentation.landmarks(),historicalGeometryAccepted:false},
            phaseDissolve:phaseDissolve.diagnostics(),
            geographicReferences:sharedPlaceView?.diagnostics(),
            urbanFabric: {
              phase: currentPhaseId,
              coreVisible: cityCoreLayer.visible,
              fabricVisible: eraFabricLayer.visible,
              phase2Components: fabricMeshes.filter((mesh) => mesh.visible).length,
              canonicalGeneratedEvents:cityCoreRuntime?.generatedEvents??null,
              sharedLedger:laterMorphologyBinding?.summary??{published:false},
              morphologyProgress:phase2Morphology?.progress??null,
              morphologyGrammar:phase2Morphology?.grammar??null,
              blocks: cityCoreRuntime?.parcels?.blockCount || 0,
              parcels: cityCoreRuntime?.parcels?.count || 0,
              buildings: cityCoreRuntime?.architecture?.buildings || 0,
            },
            visibleLegacyTemporalMeshes: 0,
            visibleCoreMeshes:
              cityCoreRuntime?.architecture?.meshes?.filter(
                (m) => m.visible && cityCoreLayer.visible,
              ).length || 0,
            phase: currentPhaseId,
          };
        needsFrame = false;
      } catch (error) {
        const state = window.__JERUSALEM3000__;
        if (state) {
          state.renderDiagnostics = {
            error: String(error?.stack || error),
            frames: frameCount,
          };
          state.status = 'render-error';
        }
        console.error('[Jerusalem 3000 first-frame render]', error);
        cancelAnimationFrame(raf);
        return;
      }
    }
    raf = requestAnimationFrame(render);
  }
  raf = requestAnimationFrame(render);
  return {
    scene,
    camera,
    renderer,
    controls,
    root,
    ready,
    setPlaybackDisplayPosition(value){playbackDisplayPosition=value;needsFrame=true;},
    setPlaybackPresentation(active){playbackPresentation=Boolean(active);playbackDisplayPosition=null;applyTemporalState();needsFrame=true;},
    playbackReadiness(){let status=isSharedGenerationPhase(currentPhaseId)?(sharedEraRuntime?.status||'idle'):'ready';if(status==='ready'&&(!renderedPlaybackReady||renderedPlaybackPhase!==currentPhaseId))status='rendering';return {phase:currentPhaseId,status,ready:status==='ready'};},
    setBuildProgress,
    setRuinProgress,
    setEvidenceMode,
    setTemporalCityState,
    earlyLandscapeEvidence(phaseId) {
      const runtime=phaseId==='chalcolithic-early-bronze'?earliestSettlement:phaseId==='middle-bronze'?middleBronzeSettlement:phaseId==='late-bronze-iron1'?lateBronzeSettlement:phaseId==='david-solomon'?davidSettlement:null;
      if (['late-first-temple','babylonian-destruction'].includes(phaseId)) return {
        source:'https://whitelevy.fas.harvard.edu/publications/jewish-quarter-excavations-old-city-jerusalem-vols-i-and-ii-finds-areas-w-and',
        references:['https://hadashot.iaa.org.il/Report_Detail_eng.aspx?id=25841&mag_id=128&print=all','https://cityofdavid.org.il/wp-content/uploads/2023/03/Traveler_COD_Eng_2022_lowrez.pdf'],
        limitations:[
          '寬牆等城防遺構支持研究西南山丘的城市發展；本畫面尚未加入經定位的寬牆平面。',
          '目前山脊、北部聖區與西丘使用獨立推定配置；住宅改採鐵器時代四室低層類比。地塊、屋頂、高度、數量和具體區界未經考古定位。',
          '毀壞階段沿用相同模型呈現變化；倒塌方式、留存比例與埋藏深度尚未考古核定。',
          '現代 DEM 不代表古代地表；完整城牆、王宮與第一聖殿形制尚未核定。'
        ]
      };
      if(independentLaterRegistrations.has(phaseId)){const data=independentLaterRegistrations.get(phaseId);return {source:data.sources[0],references:data.sources.slice(1),limitations:data.limitations};}
      if(phaseId==='hellenistic-hasmonean')return {source:hellenisticSanctuaryData.sanctuary.sources[0],references:[],limitations:hellenisticSanctuaryData.sanctuary.limitations};
      if(phaseId==='persian-nehemiah')return {
        source:periodSpatialData.phases['persian-nehemiah'].sanctuary.sources[0],references:[],
        limitations:[...periodSpatialData.phases['persian-nehemiah'].sanctuary.limitations,'第一聖殿遺存、王室區與特定前代牆段的後續狀態尚未核定。']
      };
      return runtime?.evidence();
    },
    setWaterDefenseVariant(id){waterDefenseModel.setVariant(id);applyTemporalState();},
    waterDefenseEvidence(position){const state=waterDefenseState(waterDefense,{phases:[...cityCoreRuntime.core.phases.values()]},position);return state?{...state,selectedVariant:waterDefenseModel.selectedVariant,variants:waterDefense.towerVariants,localPlans:localPlanAudit}:null;},
    foundationContext(){return {terrain:terrainRuntime};},
    inspectMetricResidentialPolicy(){return {phase:currentPhaseId,policy:metricResidentialPolicy(currentPhaseId),phaseCoverage:[...METRIC_RESIDENTIAL_PHASES],terrainOrigin:terrainRuntime.grid.origin,terrainScale:terrainRuntime.mesh.scale.toArray(),rootScale:root.scale.toArray(),densityHistoricallyVerified:false};},
    inspectHousingBoundary(options){return housingBoundaryAdmission?.snapshot(options);},
    inspectOverviewBaseline(){let meshes=0,modules=0,gridMeshes=0,maxVisualModuleSpanMetres=0,slenderSolidModules=0,omittedSliverAreaSquareMetres=0,projectedRoofAreaSquareMetres=0;const ids=new Set(),subdivisions=new Set(),planForms={};root.traverse(m=>{if(!m.isMesh||!m.userData.overview)return;for(let p=m;p;p=p.parent)if(!p.visible)return;meshes++;const form=m.geometry.userData.planForm||'unspecified';planForms[form]=(planForms[form]||0)+1;modules+=m.geometry.userData.visualModules||1;projectedRoofAreaSquareMetres+=m.geometry.userData.projectedRoofAreaSquareMetres||0;maxVisualModuleSpanMetres=Math.max(maxVisualModuleSpanMetres,m.geometry.userData.maxVisualModuleSpanMetres||0);slenderSolidModules+=m.geometry.userData.slenderSolidModules||0;omittedSliverAreaSquareMetres+=m.geometry.userData.omittedSliverAreaSquareMetres||0;if(m.geometry.userData.worldGrid===true)gridMeshes++;subdivisions.add(m.geometry.userData.subdivision||'unspecified');ids.add(m.userData.cityObject?.objectId||m.userData.cityObject?.parcelId);});return {phase:currentPhaseId,grammar:'terrain-courtyard-mass-v1',mode:'city-overview',residentialProfile:residentialEraProfile(currentPhaseId),planForms,meshes,registeredHousingObjects:ids.size,visualModules:modules,projectedRoofAreaSquareMetres,maxVisualModuleSpanMetres,slenderSolidModules,omittedSliverAreaSquareMetres,subdivisions:[...subdivisions].sort(),worldGridMeshes:gridMeshes,moduleCountsAreHistoricalBuildings:false,detailWork:'paused',historicalFoundationAccepted:false};},
    setLandmarkLabels(enabled){landmarkLabelsEnabled=Boolean(enabled);landmarkView.setVisible(landmarkLabelsEnabled);needsFrame=true;return landmarkLabelsEnabled;},
    inspectSharedPlaces(){return currentPhaseId?sharedPlaces?.snapshot({phaseId:currentPhaseId,position:timelinePosition,evidenceMode:currentEvidenceMode})??null:null;},
    sharedPlaceTransitions(){return sharedPlaces?.transitions()??[];},
    inspectPersistentCityPhase(phase){return persistentCityWorld?.inspectPhase(phase)??null;},
    inspectDefenseTimeline(){return defenseTimeline?.snapshot()??null;},
    defenseTimelineIndex(){return defenseTimeline?.index()??[];},
    defenseTransitionIndex(){return defenseTimeline?.transitionIndex()??[];},
    inspectSpatialSkeleton(){return currentPhaseId?collectSpatialSkeleton(cityCoreRuntime.core,terrainRuntime,{phaseId:currentPhaseId,position:timelinePosition,evidenceMode:currentEvidenceMode,includeRetained:retainedVisible}):null;},
    inspectHerodianDimensions(){return structuredClone(herodianScaleReport);},
    inspectRegionalLandforms(){return regionalLandforms?.snapshot()??null;},
    landmarkChronology(){return (activeWorldEntry?.runtime.registration?.cores||[]).filter(c=>c.metadata.landmarkChronology).map(c=>({id:c.id,...coreStageAt(cityCoreRuntime.core.get(c.id)||c,timelinePosition-Math.floor(timelinePosition)),projection:c.metadata.landmarkChronology.projection,visibleProfiles:(activeWorldEntry.runtime.landmarkMeshes||[]).filter(m=>m.visible&&m.userData.cityObject?.objectId===c.id).map(m=>m.userData.landmarkRepresentation.profile),geometryVerified:false}));},
    inspectCityEnclosure(){return cityEnclosureAudit?.snapshot()??null;},
    inspectCityFoundation(phaseId=currentPhaseId){return phaseId?foundationRuntime?.snapshot(phaseId)??null:null;},
    cityFoundationIndex(){return foundationRuntime?.index()??[];},
    royalReliefProfile(){return royalRelief?structuredClone(royalRelief.profile):null;},
    focusRoyalRelief(){if(currentPhaseId!=='david-solomon')return false;frameRoyalRelief();return true;},
    setTerrainOverview(enabled){
      if(!terrainRuntime)return false;
      if(enabled&&!terrainView){
        terrainView={phase:currentPhaseId,position:camera.position.clone(),target:controls.target.clone(),minDistance:controls.minDistance,maxDistance:controls.maxDistance,far:camera.far,fov:camera.fov,autoRotate:controls.autoRotate};
        // Shared urban landscape window, wide enough to keep surrounding relief
        // in frame. This camera envelope does not define a historical city extent.
        frameRegionalOverview();
      }else if(!enabled&&terrainView){
        camera.position.copy(terrainView.position);controls.target.copy(terrainView.target);controls.minDistance=terrainView.minDistance;controls.maxDistance=terrainView.maxDistance;controls.autoRotate=terrainView.autoRotate;camera.far=terrainView.far;camera.fov=terrainView.fov;camera.updateProjectionMatrix();const changedPhase=terrainView.phase!==currentPhaseId;terrainView=null;if(changedPhase){updatePeriodOverview(currentPhaseId,true);if(isEarlyLandscapePhase(currentPhaseId)){const landscape=isEarliestPhase(currentPhaseId)?earliestSettlement:currentPhaseId==='middle-bronze'?middleBronzeSettlement:currentPhaseId==='late-bronze-iron1'?lateBronzeSettlement:davidSettlement;controls.target.copy(landscape.focus);camera.position.copy(landscape.focus).add(new THREE.Vector3(180,190,270));}else if(isCorePhase(currentPhaseId)){const box=new THREE.Box3().setFromObject(cityCoreLayer),frame=fitCityOverview({points:[box.min,box.max],aspect:camera.aspect,fov:camera.fov});camera.position.copy(frame.position);controls.target.copy(frame.target);}}
      }
      regionalLandforms?.setVisible(Boolean(terrainView));
      if(wallCredit)wallCredit.hidden=Boolean(terrainView)||!['ottoman','outside-walls','modern'].includes(currentPhaseId)||!evidenceAllowed('inferred');wallGateView?.setVisible(Boolean(terrainView)&&['ottoman','outside-walls','modern'].includes(currentPhaseId)&&evidenceAllowed('inferred'));sharedPlaceView?.setVisible(Boolean(terrainView)&&evidenceAllowed('inferred'));terrainPresentation.contours.visible=true;controls.update();needsFrame=true;return !!terrainView;
    },
    inspectSourceLifecycleContext(id){return inspectSourceLifecycleContext(cityCoreRuntime.core,id,timelinePosition);},
    inspectCityObject(id){const record=cityCoreRuntime?.core.get(id);return record?structuredClone(record):null;},
    focusResidentialDistrict(id){
      if(!['late-first-temple','babylonian-destruction','persian-nehemiah'].includes(currentPhaseId)||!evidenceAllowed('inferred'))return false;
      const core=cityCoreRuntime.core,district=core.get(id),polygon=district?.geometry?.polygon;if(!polygon?.length)return false;
      const cx=polygon.reduce((s,p)=>s+p.x,0)/polygon.length,cz=polygon.reduce((s,p)=>s+p.z,0)/polygon.length;
      const records=core.phase(currentPhaseId).filter(r=>r.type==='building'&&r.source?.districtId===id&&r.metadata?.rendererBinding==='shared-residential-adapter-v1');
      if(!records.length)return false;
      records.sort((a,b)=>{const ca=a.geometry.bounds,cb=b.geometry.bounds;return Math.hypot((ca.min[0]+ca.max[0])/2-cx,(ca.min[2]+ca.max[2])/2-cz)-Math.hypot((cb.min[0]+cb.max[0])/2-cx,(cb.min[2]+cb.max[2])/2-cz);});
      const r=records[0],bounds=r.geometry.bounds,x=(bounds.min[0]+bounds.max[0])/2,z=(bounds.min[2]+bounds.max[2])/2,focus=new THREE.Vector3(x,terrainRuntime.heightAtWorld(x,z)+3,z);
      if(!templePriorCamera)templePriorCamera={position:camera.position.clone(),target:controls.target.clone(),minDistance:controls.minDistance};
      controls.minDistance=15;controls.target.copy(focus);camera.position.copy(focus).add(camera.aspect<1?new THREE.Vector3(65,60,90):new THREE.Vector3(42,40,60));controls.update();needsFrame=true;return true;
    },
    namedGateIndex(){return (namedGates||[]).map(g=>({id:g.id,label:g.label,profile:g.profile,sealed:g.sealed,available:!!wallReferenceModel?.diagnostics().visibleGateIds.includes(g.id)&&['ottoman','outside-walls','modern'].includes(currentPhaseId),geometryVerified:false}));},
    focusCityObject(id){
      const gate=namedGates?.find(g=>g.id===id),box=new THREE.Box3();root.updateMatrixWorld(true);let found=false;
      root.traverse(m=>{if(!m.isMesh||m.userData.cityObject?.objectId!==id)return;for(let p=m;p;p=p.parent)if(!p.visible)return;box.expandByObject(m);found=true;});if(!found)return false;
      const focus=box.getCenter(new THREE.Vector3()),size=box.getSize(new THREE.Vector3()),distance=Math.max(size.x,size.y,size.z)*(id==='j3k:object:inner-temple'?(camera.aspect<1?1.8:1.15):2.1);
      controls.minDistance=5;controls.target.copy(focus);camera.position.copy(focus).add(gate?new THREE.Vector3(-gate.normal.x*distance,.25*distance,-gate.normal.z*distance):new THREE.Vector3(.65*distance,.7*distance,distance));controls.update();needsFrame=true;return true;
    },
    setTempleSection(value){const enabled=templeSection.set(value,root);needsFrame=true;return enabled;},
    inspectTempleSection(){return templeSection.diagnostics();},
    focusRoyalTemple(){
      const court=activeWorldEntry?.runtime.registration?.cores.find(c=>c.metadata.precinctContext);if(court)return this.focusCityObject(court.id);
      if(isCorePhase(currentPhaseId))return this.focusCityObject('j3k:object:inner-temple');
      const templeRuntime=currentPhaseId==='persian-nehemiah'?persianSanctuary:currentPhaseId==='hellenistic-hasmonean'?hellenisticSanctuary:royalCity;
      if(!templeRuntime?.diagnostics().visibleTemple)return;
      if(!templePriorCamera)templePriorCamera={position:camera.position.clone(),target:controls.target.clone(),minDistance:controls.minDistance};
      controls.minDistance=35;controls.target.copy(templeRuntime.templeFocus||templeRuntime.focus);camera.position.copy(templeRuntime.templeFocus||templeRuntime.focus).add(new THREE.Vector3(65,60,90));controls.update();needsFrame=true;
    },
    setRetainedLayerVisible(visible) {
      retainedVisible = Boolean(visible);
      sharedEraRuntime?.request(currentPhaseId,{retainedVisible});
      updatePeriodOverview(currentPhaseId,true);
      applyTemporalState();
      needsFrame = true;
    },
    auditCityPhases(phaseIds) {
      // A startup audit must NEVER switch eras or build WebGL geometry.
      // Previously this synchronously generated all 18 city meshes and froze the UI.
      const records = phaseIds.map((phaseId) => {
        const canonicalPhase = isCorePhase(phaseId);
        const canonicalValid = !canonicalPhase || Boolean(
          cityCoreRuntime?.parcels?.blockCount > 0 &&
          cityCoreRuntime?.parcels?.count > 0 &&
          cityCoreRuntime?.architecture?.buildings > 0
        );
        return {
          phaseId,
          canonicalValid,
          status: canonicalPhase ? (canonicalValid ? 'validated' : 'failed') : 'deferred-render-check',
          hasVisibleCity: canonicalPhase ? canonicalValid : null,
          canonicalBlocks: canonicalPhase ? cityCoreRuntime?.parcels?.blockCount || 0 : null,
          canonicalParcels: canonicalPhase ? cityCoreRuntime?.parcels?.count || 0 : null,
        };
      });
      const deferredPhases = records.filter(record => record.status === 'deferred-render-check').map(record => record.phaseId);
      const canonicalFailures = records.filter(record => !record.canonicalValid).map(record => record.phaseId);
      return {
        ok: canonicalFailures.length === 0,
        complete: deferredPhases.length === 0 && canonicalFailures.length === 0,
        checked: records.length - deferredPhases.length,
        deferredPhases,
        records,
        emptyPhases: canonicalFailures,
        canonicalFailures,
      };
    },
    dispose() {
      cancelAnimationFrame(raf);
      ro.disconnect();
      controls.dispose();
      constructionPresentation.dispose();phaseDissolve.dispose();
      templeSection.dispose();
      builder.dispose();
      clearFabric();persistentCityWorld?.dispose();laterMorphologyLedger?.dispose();
      sharedEraRuntime?.dispose();
      earliestSettlement?.dispose();
      middleBronzeSettlement?.dispose();
      lateBronzeSettlement?.dispose();
      davidSettlement?.dispose();
      royalRelief?.dispose();
      royalCity?.dispose();
      persianSanctuary?.dispose();
      hellenisticSanctuary?.dispose();
      generationStatus.remove();
      wallCredit?.remove();
      wallGateView?.dispose();
      defenseTimeline?.dispose();wallReferenceModel?.dispose();
      sharedPlaceView?.dispose();landmarkView.dispose();
      regionalLandforms?.dispose();
      urbanGround?.dispose();
      architecturalTerrainOcclusion?.dispose();
      terrainPresentation?.dispose();
      terrainRuntime?.dispose?.();
      for (const mesh of cityCoreRuntime?.architecture?.meshes || [])
        mesh.geometry?.dispose?.();
      cityCoreRuntime?.architecture?.overviewMaterial?.dispose();
      renderer.dispose();
    },
  };
}
