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
import { buildHerodianParcelCore, buildEraParcelCore } from './herodian-parcel-core.js';
import { deriveEraRegistration } from './era-registration-adapter.js';
import { buildHerodianParcelArchitecture, buildEraParcelArchitecture } from './herodian-typology-grammar.js';
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
  return !isCorePhase(phaseId);
}
export function mountJerusalemThreeScene(mount, { onReady } = {}) {
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
  const eraCities = new Map();
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
  function ensureEraCity(phaseId) {
    if (isCorePhase(phaseId) || !ERA_FOOTPRINTS[phaseId] || !eraRegistrationReference || !cityCoreRuntime) return null;
    if (eraCities.has(phaseId)) return eraCities.get(phaseId);
    // Keep at most one generated non-core city in GPU memory.
    for (const [oldPhase, oldCity] of eraCities) {
      sharedEraLayer.remove(oldCity.group);
      oldCity.group.traverse((node) => {
        if (node.isMesh) node.geometry?.dispose?.();
      });
      eraCities.delete(oldPhase);
    }
    const registration = deriveEraRegistration(eraRegistrationReference, phaseId, ERA_FOOTPRINTS[phaseId]);
    const group = new THREE.Group();
    group.name = `j3k-shared-era-${phaseId}`;
    sharedEraLayer.add(group);
    const parcels = buildEraParcelCore(cityCoreRuntime.core, terrainRuntime, {
      phaseId, registration, districtId: registration.districts[0].id,
      dataset: 'provisional-era-registration',
    });
    const architecture = buildEraParcelArchitecture(group, cityCoreRuntime.core, temporalMaterials, terrainRuntime, {
      phaseId, grammarId: 'shared-era-parcel-typology-v1',
    });
    const roads = buildHerodianRoadGeometry(group, registration.roads, temporalMaterials, terrainRuntime);
    const result = { group, parcels, architecture, roads, phaseId };
    eraCities.set(phaseId, result);
    return result;
  }
  function updateCityCoreVisibility() {
    for (const [phaseId, city] of eraCities) {
      city.group.visible = phaseId === currentPhaseId && currentEvidenceMode !== 'disputed';
      if (city.group.visible) {
        const ruined = currentPhaseId.includes('destruction');
        for (const mesh of city.architecture.meshes) mesh.visible = !ruined || currentRuin < 1;
      }
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
    /* Every phase uses the same parcel-and-architecture pipeline. */
    if (isCorePhase(phaseId)) return;
    const sharedCity = ensureEraCity(phaseId);
    if (sharedCity?.architecture.buildings > 0) {
      eraFabricLayer.visible = false;
      updateCityCoreVisibility();
      needsFrame = true;
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
  function setTemporalCityState(objects = [], position = 0, phaseId = '') {
    const previousPhase = currentPhaseId,
      phaseChanged = previousPhase !== phaseId;
    currentPhaseId = phaseId;
    applyTemporalState();
    if (phaseChanged && terrainRuntime) {
      rebuildUrbanFabric(phaseId);
      applyTemporalState();
    }
    const activeIds = new Set();
    objects.forEach((object, index) => {
      if (
        !(object.visible || object.ruined) ||
        !legacyTemporalAllowed(object, phaseId)
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
    fetch('./data/objects/herodian-30ce.json', { cache: 'no-store' }).then(
      (r) => {
        if (!r.ok) throw new Error(`Herodian ledger unavailable (${r.status})`);
        return r.json();
      },
    ),
    loadTerrainAuthority(),
  ]).then(async ([ledger, { manifest }]) => {
    evidenceResolution = new EvidenceResolutionEngine(ledger.objects);
    terrainRuntime = await loadCanonicalTerrain(manifest, root);
    if (!terrainRuntime)
      throw new Error('Canonical Jerusalem DEM payload missing');
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
      const eraRegistrationResponse = await fetch('./data/urban/herodian-30ce.registration.json', { cache: 'no-store' });
      if (!eraRegistrationResponse.ok) throw new Error(`Era registration unavailable: ${eraRegistrationResponse.status}`);
      eraRegistrationReference = await eraRegistrationResponse.json();
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
    } catch (error) {
      throw new Error(`Canonical city construction failed: ${error.message}`, {
        cause: error,
      });
    }
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
        renderer.render(scene, camera);
        frameCount++;
        const state = window.__JERUSALEM3000__;
        if (state)
          state.renderDiagnostics = {
            frames: frameCount,
            canvasWidth: renderer.domElement.width,
            canvasHeight: renderer.domElement.height,
            webgl: !renderer.getContext().isContextLost(),
            sceneChildren: scene.children.length,
            cityProjection: cityProjection?.diagnostics(),
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
      terrainRuntime?.dispose?.();
      for (const mesh of cityCoreRuntime?.architecture?.meshes || [])
        mesh.geometry?.dispose?.();
      for (const city of eraCities.values())
        city.group.traverse(node => { if (node.isMesh) node.geometry?.dispose?.(); });
      renderer.dispose();
    },
  };
}
