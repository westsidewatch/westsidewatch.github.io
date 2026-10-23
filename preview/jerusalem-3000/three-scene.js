import {createRoyalRelief} from './royal-relief.js';
import {createTerrainPresentation} from './terrain-presentation.js';
import {auditLocalPlanRegistry} from './local-plan-registration.js';
import {createWaterDefenseModelAdapter} from './water-defense-model-adapter.js';
import {compileWaterDefenseRegistration,bindWaterDefenseCore,waterDefenseState} from './water-defense-registration.js';
import {fitCityOverview} from './city-overview.js';
import {createPersianSanctuary} from './persian-sanctuary.js';
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
const ERA_FOOTPRINTS = {
  'chalcolithic-early-bronze': {
    cx: -430,
    cz: 360,
    sx: 0.38,
    sz: 0.52,
    density: 7,
  },
  'middle-bronze': { cx: -360, cz: 300, sx: 0.5, sz: 0.65, density: 10 },
  'late-bronze-iron1': { cx: -330, cz: 270, sx: 0.58, sz: 0.72, density: 12 },
  'david-solomon': { cx: -260, cz: 210, sx: 0.7, sz: 0.82, density: 18 },
  'late-first-temple': { cx: -100, cz: 120, sx: 1.05, sz: 1.05, density: 28 },
  'babylonian-destruction': {
    cx: -100,
    cz: 120,
    sx: 1.05,
    sz: 1.05,
    density: 18,
  },
  'persian-nehemiah': { cx: -220, cz: 170, sx: 0.72, sz: 0.82, density: 18 },
  'hellenistic-hasmonean': { cx: -40, cz: 80, sx: 1.05, sz: 1.02, density: 30 },
  'herodian-jesus': { cx: 80, cz: 0, sx: 1.25, sz: 1.15, density: 40 },
  'roman-destruction': { cx: 80, cz: 0, sx: 1.25, sz: 1.15, density: 24 },
  aelia: { cx: 40, cz: -40, sx: 1.02, sz: 1.02, density: 28 },
  byzantine: { cx: 20, cz: -30, sx: 1.14, sz: 1.1, density: 34 },
  'early-islamic': { cx: 10, cz: -20, sx: 1.08, sz: 1.06, density: 32 },
  crusader: { cx: 0, cz: -20, sx: 0.96, sz: 0.94, density: 30 },
  'ayyubid-mamluk': { cx: 0, cz: -10, sx: 1, sz: 0.98, density: 32 },
  ottoman: { cx: 0, cz: 0, sx: 1.02, sz: 1, density: 38 },
  'outside-walls': { cx: 55, cz: -35, sx: 1.28, sz: 1.18, density: 48 },
  modern: { cx: 120, cz: -80, sx: 1.65, sz: 1.5, density: 58 },
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
function temporalShape(object, index, phaseId) {
  const era = ERA_FOOTPRINTS[phaseId] || {
    cx: 0,
    cz: 0,
    sx: 1,
    sz: 1,
    density: 20,
  };
  const seed = [...object.id].reduce(
    (n, c) => (n * 31 + c.charCodeAt(0)) >>> 0,
    2166136261,
  );
  const angle = (seed % 6283) / 1000,
    radius = 220 + (seed % 780);
  const x = era.cx + Math.cos(angle) * radius * era.sx,
    z = era.cz + Math.sin(angle) * radius * era.sz,
    kind = object.kind || '';
  let w = 220 * era.sx,
    d = 170 * era.sz,
    h = 78;
  if (kind.includes('wall') || kind.includes('fortification')) {
    w = 760 * era.sx;
    d = 52;
    h = 120;
  }
  if (kind.includes('gate')) {
    w = 165;
    d = 105;
    h = 170;
  }
  if (kind.includes('sanctuary')) {
    w = 380 * era.sx;
    d = 285 * era.sz;
    h = 205;
  }
  if (kind.includes('urban-envelope')) {
    w = 1050 * era.sx;
    d = 780 * era.sz;
    h = 32;
  }
  if (kind.includes('urban-fabric')) {
    w = 820 * era.sx;
    d = 650 * era.sz;
    h = 48;
  }
  if (kind.includes('transport')) {
    w = 1150 * era.sx;
    d = 28;
    h = 10;
  }
  if (kind.includes('water')) {
    w = 340;
    d = 65;
    h = 55;
  }
  if (kind.includes('monumental')) {
    w = 420;
    d = 320;
    h = 155;
  }
  return {
    x: x + (index % 3) * 55,
    z: z + ((index * 83) % 230) - 115,
    w,
    d,
    h,
    rotation: angle * 0.3,
  };
}
function terrainY(terrain, x, z) {
  const y = terrain?.heightAtWorld?.(x, z);
  return Number.isFinite(y) ? y : 0;
}
function addEraFabric(
  group,
  phaseId,
  material,
  ruined = false,
  terrain = null,
) {
  const era = ERA_FOOTPRINTS[phaseId];
  if (!era) return [];
  const meshes = [];
  for (let i = 0; i < era.density; i++) {
    const col = i % 8,
      row = Math.floor(i / 8),
      jx = ((i * 47) % 71) - 35,
      jz = ((i * 29) % 59) - 29,
      x = era.cx + (col - 3.5) * 125 * era.sx + jx,
      z = era.cz + (row - 2.2) * 125 * era.sz + jz,
      w = (62 + ((i * 17) % 70)) * era.sx,
      d = (54 + ((i * 23) % 62)) * era.sz,
      h = ruined ? 12 + (i % 3) * 4 : 34 + ((i * 19) % 72);
    const mesh = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), material);
    mesh.position.set(x, terrainY(terrain, x, z) + h / 2 + 4, z);
    mesh.rotation.y = (((i * 13) % 17) - 8) * 0.018;
    mesh.receiveShadow = true;
    group.add(mesh);
    meshes.push(mesh);
  }
  return meshes;
}
function legacyTemporalAllowed(object, phaseId) {
  return object.rendererBinding!=='ledger-only-pending-adapter' && !isCorePhase(phaseId) && !isEarlyLandscapePhase(phaseId) && !isSharedGenerationPhase(phaseId);
}
export function mountJerusalemThreeScene(mount, { onReady, onDistrictAcceptance } = {}) {
  const scene = new THREE.Scene(),
    camera = new THREE.PerspectiveCamera(34, 1, 0.1, 18000),
    renderer = new THREE.WebGLRenderer({
      antialias: true,
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
  controls.autoRotate = !reducedMotion;
  controls.autoRotateSpeed = 0.32;
  const root = new THREE.Group(),
    historical = new THREE.Group(),
    temporalLayer = new THREE.Group(),
    eraFabricLayer = new THREE.Group(),
    cityCoreLayer = new THREE.Group(),
    sharedEraLayer = new THREE.Group();
  cityCoreLayer.name = 'j3k-canonical-herodian-city';
  scene.add(root);
  root.add(historical, temporalLayer, eraFabricLayer, cityCoreLayer, sharedEraLayer);
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
  let currentProgress = 0,
    currentRuin = 0,
    terrainRuntime = null,
    terrainPresentation = null,
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
  const temporalMeshes = new Map();
  let sharedEraRuntime = null;
  let earliestSettlement = null, middleBronzeSettlement = null, lateBronzeSettlement = null, davidSettlement = null, priorCamera = null;
  let retainedVisible = false, royalRelief=null, royalCity=null, persianSanctuary=null, periodSpatialData=null, waterDefense=null, waterDefenseModel=null, localPlanAudit=[], periodRegistrations=new Map(), overviewPriorCamera=null, overviewFrame='', overviewInfo=null, timelinePosition=0, royalCameraStage='', templePriorCamera=null;
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
    royalRelief?.apply({phaseId:currentPhaseId,stage:royalCity?.diagnostics().stage,evidenceAllowed});
    const sharedActive = sharedEraRuntime?.apply({ phaseId: currentPhaseId, ruin: currentRuin, evidenceAllowed, retainedVisible });
    if (sharedActive) {
      clearFabric(); eraFabricLayer.visible = false;
      for (const mesh of temporalMeshes.values()) mesh.visible = false;
    }
    if (cityProjection)
      cityProjection.apply({
        phaseId: currentPhaseId,
        ruin: currentRuin,
        evidenceAllowed,
      });
  }
  function applyTemporalState() {
    builder.setProgress(herodianPhaseActive() ? currentProgress : 0);
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
    updateCityCoreVisibility();
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
  function evidenceAllowed(level) {
    if (currentEvidenceMode === 'all') return true;
    if (currentEvidenceMode === 'observed') return level === 'observed';
    if (currentEvidenceMode === 'reconstructed')
      return level === 'observed' || level === 'reconstructed';
    if (currentEvidenceMode === 'inferred') return level !== 'disputed';
    return level === 'disputed';
  }
  function setEvidenceMode(mode = 'all') {
    currentEvidenceMode = mode;
    if (evidenceResolution)
      for (const mesh of builder.meshes) {
        const object = mesh.userData?.evidenceObject;
        mesh.visible =
          herodianPhaseActive() &&
          (!object || evidenceResolution.allows(object, mode));
      }
    for (const mesh of temporalMeshes.values())
      mesh.visible =
        mesh.userData.temporalActive &&
        evidenceAllowed(mesh.userData.evidenceLevel);
    eraFabricLayer.visible = mode !== 'disputed';
    applyTemporalState();
    needsFrame = true;
  }
  function clearFabric() {
    for (const mesh of fabricMeshes) {
      eraFabricLayer.remove(mesh);
      mesh.geometry.dispose();
    }
    fabricMeshes = [];
    phase2Morphology = null;
  }
  function rebuildUrbanFabric(phaseId) {
    clearFabric();
    // Request only this bounded slice; other eras retain their established morphology.
    sharedEraRuntime?.request(phaseId);
    if (isCorePhase(phaseId) || isEarlyLandscapePhase(phaseId)) return;
    if (isSharedGenerationPhase(phaseId)) {
      eraFabricLayer.visible = false;
      return;
    }
    eraFabricLayer.visible = currentEvidenceMode !== 'disputed';
    const ruined = phaseId.includes('destruction');
    if (phaseId === 'ottoman')
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
      return;
    }
    fabricMeshes = addEraFabric(
      eraFabricLayer,
      phaseId,
      temporalMaterials.reconstructed,
      ruined,
      terrainRuntime,
    );
  }
  function updatePeriodOverview(phaseId,force=false){
    if(terrainView)return;
    const framePhase=phaseId==='babylonian-destruction'?'late-first-temple':phaseId;
    const includesEarlier=phaseId==='persian-nehemiah'&&retainedVisible;
    const frameKey=framePhase+(includesEarlier?':retained':'');
    if(!periodRegistrations.has(framePhase)||(!force&&overviewFrame===frameKey))return;
    if(!overviewPriorCamera)overviewPriorCamera={position:camera.position.clone(),target:controls.target.clone(),minDistance:controls.minDistance};
    const registrations=[periodRegistrations.get(framePhase),...(includesEarlier?[periodRegistrations.get('late-first-temple')]:[])];
    const points=registrations.flatMap(r=>r.districts.flatMap(d=>d.geometry.polygon.flatMap(p=>{const y=terrainRuntime.heightAtWorld(p.x,p.z);return[new THREE.Vector3(p.x,y,p.z),new THREE.Vector3(p.x,y+32,p.z)];})));
    const framing=fitCityOverview({points,aspect:camera.aspect,fov:camera.fov});
    controls.minDistance=35;controls.target.copy(framing.target);camera.position.copy(framing.position);controls.update();overviewFrame=frameKey;
    overviewInfo={framePhase,includesEarlier,distance:framing.distance,bounds:framing.bounds,authority:framing.authority};
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
    currentPhaseId = phaseId;
    timelinePosition=position;
    if(!terrainView){
    if(phaseChanged&&templePriorCamera){camera.position.copy(templePriorCamera.position);controls.target.copy(templePriorCamera.target);controls.minDistance=templePriorCamera.minDistance;templePriorCamera=null;controls.update();}
    if(phaseChanged&&overviewPriorCamera&&!['late-first-temple','babylonian-destruction','persian-nehemiah'].includes(phaseId)){camera.position.copy(overviewPriorCamera.position);controls.target.copy(overviewPriorCamera.target);controls.minDistance=overviewPriorCamera.minDistance;overviewPriorCamera=null;overviewFrame='';overviewInfo=null;controls.update();}
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
    const activeIds = new Set();
    objects.forEach((object, index) => {
      if (
        !(object.visible || object.ruined) ||
        !legacyTemporalAllowed(object, phaseId) ||
        (isSharedGenerationPhase(phaseId) && sharedEraRuntime?.status === 'ready')
      )
        return;
      activeIds.add(object.id);
      let mesh = temporalMeshes.get(object.id);
      const shape = temporalShape(object, index, phaseId);
      if (!mesh) {
        const level = temporalEvidence(object);
        mesh = new THREE.Mesh(
          new THREE.BoxGeometry(shape.w, shape.h, shape.d),
          temporalMaterials[level],
        );
        mesh.rotation.y = shape.rotation;
        mesh.receiveShadow = true;
        mesh.userData = {
          evidenceLevel: level,
          baseHeight: shape.h,
          temporalActive: true,
        };
        temporalMeshes.set(object.id, mesh);
        temporalLayer.add(mesh);
      }
      mesh.userData.temporalActive = true;
      mesh.visible = evidenceAllowed(mesh.userData.evidenceLevel);
      mesh.scale.y = object.ruined ? 0.22 : 1;
      mesh.position.set(
        shape.x,
        terrainY(terrainRuntime, shape.x, shape.z) +
          (shape.h * mesh.scale.y) / 2 +
          5,
        shape.z,
      );
      mesh.rotation.z = object.ruined ? 0.035 : 0;
    });
    for (const [id, mesh] of temporalMeshes)
      if (!activeIds.has(id)) {
        mesh.userData.temporalActive = false;
        mesh.visible = false;
      }
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
          const w = object.kind === 'fortress' ? 156 : 540,
            d = object.kind === 'fortress' ? 136 : 360,
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
    for (const mesh of builder.meshes) {
      const object = mesh.userData.evidenceObject;
      const anchor = object.spatial.anchor;
      mesh.userData.cityObject = {
        objectId: object.id,
        confidence: temporalEvidence(object),
        terrainGround: terrainRuntime.sampleElevation(anchor.lat, anchor.lon),
      };
    }
    evidenceProjection = createCityProjection(historical, builder.meshes);
    historical.visible = false;
    const phaseSeed = Object.keys(ERA_FOOTPRINTS).map((id) => ({ id }));
    try {
      const loaded = await loadTemporalCityCore(phaseSeed, {
        terrain: terrainRuntime,
      });
      await registerHerodianUrbanCore(loaded.core);
      eraRegistrationReference = await loadCityData('./data/urban/herodian-30ce.registration.json');
      const parcels = await buildHerodianParcelCore(
        loaded.core,
        terrainRuntime,
        { exclusions },
      );
      const architecture = buildHerodianParcelArchitecture(
        cityCoreLayer,
        loaded.core,
        temporalMaterials,
        terrainRuntime,
      );
      cityCoreRuntime = {
        core: loaded.core,
        parcels,
        architecture,
        validation: loaded.core.validate(),
      };
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
      cityProjection = createCityProjection(cityCoreLayer, architecture.meshes);
      cityCoreRuntime.projection = cityProjection;
      periodSpatialData = await loadCityData('./data/urban/first-temple-persian.spatial.v1.json');
      for(const phase of ['late-first-temple','persian-nehemiah']){const registration=compilePeriodRegistration(periodSpatialData,phase,terrainRuntime.grid.origin);periodRegistrations.set(phase,registration);bindPeriodSpatialCore(loaded.core,registration);}
      sharedEraRuntime = createSharedEraRuntime(sharedEraLayer, {
        ledgerCore:loaded.core,
        getRegistration:phase => periodRegistrations.get(phase) ?? null,
        getExclusions:phase=>royalCity?.exclusionsFor(phase)||[],
        reference: eraRegistrationReference, footprint: ERA_FOOTPRINTS['late-first-temple'],
        successorFootprint: ERA_FOOTPRINTS['persian-nehemiah'],
        expansionFootprint: ERA_FOOTPRINTS['hellenistic-hasmonean'],
        terrain: terrainRuntime, materials: temporalMaterials,
        onChange: () => { applyTemporalState(); needsFrame = true; },
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
    earliestSettlement=createEarliestSettlement(root,{data:await settlementResponse.json(),terrain:terrainRuntime});
    const middleResponse=await fetch('./data/settlement/middle-bronze.v1.json',{cache:'no-store'});
    if(!middleResponse.ok) throw new Error('Middle Bronze settlement data unavailable');
    middleBronzeSettlement=createEarliestSettlement(root,{data:await middleResponse.json(),terrain:terrainRuntime});
    const lateResponse=await fetch('./data/settlement/late-bronze-iron1.v1.json',{cache:'no-store'});
    if(!lateResponse.ok) throw new Error('Late Bronze landscape data unavailable');
    lateBronzeSettlement=createEarliestSettlement(root,{data:await lateResponse.json(),terrain:terrainRuntime});
    const waterDefenseData=await loadCityData('./data/urban/water-defense.registration.v1.json');
    localPlanAudit=auditLocalPlanRegistry(await loadCityData('./data/urban/water-defense.local-plans.v1.json'),terrainRuntime.grid.origin);
    waterDefense=compileWaterDefenseRegistration(waterDefenseData,terrainRuntime.grid.origin);bindWaterDefenseCore(cityCoreRuntime.core,waterDefense);
    for(const admission of localPlanAudit){const record=cityCoreRuntime.core.get(admission.objectId);if(!record)throw new Error('Local plan target missing from shared ledger');cityCoreRuntime.core.register({...record,metadata:{...record.metadata,localPlanAdmission:admission}});}
    waterDefenseModel=createWaterDefenseModelAdapter({runtime:middleBronzeSettlement,core:cityCoreRuntime.core,registration:waterDefense});
    const davidData=await loadCityData('./data/settlement/david-solomon.v1.json');
    davidSettlement=createEarliestSettlement(root,{data:davidData,terrain:terrainRuntime});
    royalCity=createRoyalCity(root,{data:davidData,terrain:terrainRuntime,core:cityCoreRuntime.core});
    royalRelief=createRoyalRelief(root,mount,{data:davidData,terrain:terrainRuntime});
    persianSanctuary=createPersianSanctuary(root,{data:periodSpatialData,terrain:terrainRuntime,core:cityCoreRuntime.core});
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
  const resize = () => {
    const w = Math.max(1, mount.clientWidth),
      h = Math.max(1, mount.clientHeight);
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
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
    if (needsFrame || changed || controls.autoRotate) {
      try {
        royalRelief?.project(camera);
        renderer.render(scene, camera);
        frameCount++;
        const sharedState = sharedEraRuntime?.diagnostics();
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
            cityOverview:overviewInfo,
            terrainPresentation:{...terrainPresentation?.diagnostics,overviewActive:!!terrainView,camera:camera.position.toArray(),target:controls.target.toArray()},
            urbanFabric: {
              phase: currentPhaseId,
              coreVisible: cityCoreLayer.visible,
              fabricVisible: eraFabricLayer.visible,
              phase2Components: fabricMeshes.filter((mesh) => mesh.visible).length,
              blocks: cityCoreRuntime?.parcels?.blockCount || 0,
              parcels: cityCoreRuntime?.parcels?.count || 0,
              buildings: cityCoreRuntime?.architecture?.buildings || 0,
            },
            visibleLegacyTemporalMeshes: [...temporalMeshes.values()].filter(
              (m) => m.visible,
            ).length,
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
      if(phaseId==='persian-nehemiah')return {
        source:periodSpatialData.phases['persian-nehemiah'].sanctuary.sources[0],references:[],
        limitations:[...periodSpatialData.phases['persian-nehemiah'].sanctuary.limitations,'第一聖殿遺存、王室區與特定前代牆段的後續狀態尚未核定。']
      };
      return runtime?.evidence();
    },
    setWaterDefenseVariant(id){waterDefenseModel.setVariant(id);applyTemporalState();},
    waterDefenseEvidence(position){const state=waterDefenseState(waterDefense,{phases:[...cityCoreRuntime.core.phases.values()]},position);return state?{...state,selectedVariant:waterDefenseModel.selectedVariant,variants:waterDefense.towerVariants,localPlans:localPlanAudit}:null;},
    royalReliefProfile(){return royalRelief?structuredClone(royalRelief.profile):null;},
    focusRoyalRelief(){if(currentPhaseId!=='david-solomon')return false;frameRoyalRelief();return true;},
    setTerrainOverview(enabled){
      if(!terrainRuntime)return false;
      if(enabled&&!terrainView){
        terrainView={position:camera.position.clone(),target:controls.target.clone(),minDistance:controls.minDistance,maxDistance:controls.maxDistance,far:camera.far,fov:camera.fov,autoRotate:controls.autoRotate};
        // Shared urban landscape window, wide enough to keep surrounding relief
        // in frame. This camera envelope does not define a historical city extent.
        const points=[];
        for(const x of [-650,900])for(const z of [-700,1050])points.push(new THREE.Vector3(x,terrainRuntime.heightAtWorld(x,z),z));
        camera.fov=48;
        const frame=fitCityOverview({points,aspect:camera.aspect,fov:camera.fov});
        camera.far=Math.max(camera.far,frame.distance*3);camera.updateProjectionMatrix();controls.maxDistance=frame.distance*2;
        camera.position.copy(frame.position);controls.target.copy(frame.target);controls.minDistance=35;controls.autoRotate=false;
      }else if(!enabled&&terrainView){
        camera.position.copy(terrainView.position);controls.target.copy(terrainView.target);controls.minDistance=terrainView.minDistance;controls.maxDistance=terrainView.maxDistance;controls.autoRotate=terrainView.autoRotate;camera.far=terrainView.far;camera.fov=terrainView.fov;camera.updateProjectionMatrix();terrainView=null;
      }
      terrainPresentation.contours.visible=!!terrainView;controls.update();needsFrame=true;return !!terrainView;
    },
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
    focusRoyalTemple(){
      const templeRuntime=currentPhaseId==='persian-nehemiah'?persianSanctuary:royalCity;
      if(!templeRuntime?.diagnostics().visibleTemple)return;
      if(!templePriorCamera)templePriorCamera={position:camera.position.clone(),target:controls.target.clone(),minDistance:controls.minDistance};
      controls.minDistance=35;controls.target.copy(templeRuntime.templeFocus||templeRuntime.focus);camera.position.copy(templeRuntime.templeFocus||templeRuntime.focus).add(new THREE.Vector3(65,60,90));controls.update();needsFrame=true;
    },
    setRetainedLayerVisible(visible) {
      retainedVisible = Boolean(visible);
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
      builder.dispose();
      sharedEraRuntime?.dispose();
      earliestSettlement?.dispose();
      middleBronzeSettlement?.dispose();
      lateBronzeSettlement?.dispose();
      davidSettlement?.dispose();
      royalRelief?.dispose();
      royalCity?.dispose();
      persianSanctuary?.dispose();
      generationStatus.remove();
      terrainPresentation?.dispose();
      terrainRuntime?.dispose?.();
      for (const mesh of cityCoreRuntime?.architecture?.meshes || [])
        mesh.geometry?.dispose?.();
      renderer.dispose();
    },
  };
}
