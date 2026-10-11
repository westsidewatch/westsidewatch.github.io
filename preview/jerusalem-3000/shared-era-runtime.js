import { trimCityCache } from './city-runtime-cache.js';
import * as THREE from 'three';
import { TemporalCityCore } from './temporal-city-core.js';
import { deriveEraRegistration } from './era-registration-adapter.js';
import { buildEraParcelCore } from './herodian-parcel-core.js';
import { buildEraParcelArchitectureAsync } from './herodian-typology-grammar.js';
import { buildHerodianRoadGeometry } from './herodian-road-geometry.js';
import { createCityProjection } from './city-lifecycle-projection.js';

export const SHARED_SLICE_PHASES = ['late-first-temple', 'babylonian-destruction'];
export const isSharedSlicePhase = id => SHARED_SLICE_PHASES.includes(id);
export const RETAINED_PHASE = 'persian-nehemiah';
export const EXPANSION_PHASE = 'hellenistic-hasmonean';
export const REPLACEMENT_PHASE = 'aelia';
export const isSharedGenerationPhase = id => isSharedSlicePhase(id) || [RETAINED_PHASE, EXPANSION_PHASE, REPLACEMENT_PHASE].includes(id);

// One provisional first-temple fabric, inherited by destruction in place.
// Reuse is a schematic lifecycle, not evidence of surveyed period-specific parcels.
function createParcelRuntime(parent, { reference, footprint, terrain, materials,
  generationPhase, phaseIds, destroyedPhase = null, retainedPhase = null,
  onChange = () => {}, onProgress = () => {} }) {
  const openingMaterial = materials.facadeOpening || new THREE.MeshStandardMaterial({ color: 0x3d3327, roughness: .94, metalness: 0 });
  const sharedMaterials = { ...materials, facadeOpening: openingMaterial };
  let current = '', pending = null, city = null, disposed = false;
  let state = { status: 'idle', completed: 0, total: 0 };
  function release(group) {
    group.traverse(object => object.geometry?.dispose?.());
    group.removeFromParent();
  }
  function request(phaseId) {
    current = phaseId;
    if (!phaseIds.includes(phaseId)) {
      pending?.controller.abort();
      if (city) city.group.visible = false;
      return;
    }
    if (disposed || city || pending) return;
    const group = new THREE.Group();
    group.name = `shared-${generationPhase}-city`;
    group.visible = false; // Never show a partially assembled replacement.
    parent.add(group);
    const controller = new AbortController();
    const task = { controller, group };
    pending = task;
    state = { status: 'generating', completed: 0, total: 0 };
    task.promise = (async () => {
      try {
        // Yield before parcel work too; request() always returns immediately.
        await new Promise(resolve => setTimeout(resolve, 0));
        if (controller.signal.aborted) throw new DOMException('Cancelled', 'AbortError');
        const phaseId = generationPhase;
        const core = new TemporalCityCore({ phases: phaseIds.map(id => ({ id })), terrain });
        const registration = deriveEraRegistration(reference, phaseId, footprint);
        const parcels = buildEraParcelCore(core, terrain, {
          phaseId, registration, districtId: registration.districts[0].id,
          dataset: `provisional-${generationPhase}-footprint-not-surveyed`,
        });
        const architecture = await buildEraParcelArchitectureAsync(group, core, sharedMaterials, terrain, {
          phaseId, destroyedPhase, signal: controller.signal,
          onProgress: progress => { state = { status: 'generating', ...progress }; onProgress(progress); },
        });
        if (!architecture.buildings || !core.validate().ok) throw new Error('Shared era generated no valid architecture');
        // Carry the SAME records into the successor period as hypothetical ruins.
        // Do not claim Persian road continuity, burial depths or rebuilding links.
        for (const id of retainedPhase ? architecture.buildingIds : []) {
          const record = core.get(id);
          core.register({ ...record, phaseIds: [...record.phaseIds, retainedPhase],
            metadata: { ...record.metadata, retainedPhase,
              retentionAuthority: 'schematic-not-surveyed', burialDepthVerified: false, reuseLinksVerified: false } });
        }
        const roads = buildHerodianRoadGeometry(group, registration.roads, sharedMaterials, terrain);
        const projection = createCityProjection(group, [...architecture.meshes, ...roads], {
          phaseIds, standingPhase: phaseId,
          phaseStates: retainedPhase ? { [retainedPhase]: { state: 'retained-ruin', ruin: 1 } } : {},
        });
        city = { group, core, parcels, architecture, projection, components: architecture.meshes.length + roads.length };
        state = { status: 'ready', completed: architecture.buildings, total: architecture.buildings,
          yields: architecture.yields, maxBatchMs: architecture.maxBatchMs, elapsedMs: architecture.elapsedMs, authority: registration.authority };
      } catch (error) {
        release(group);
        state = { status: error.name === 'AbortError' ? 'cancelled' : 'error', error: String(error) };
      } finally {
        if (pending === task) pending = null;
        if (!disposed) {
          // A rapid leave/return may request this slice while cancellation settles.
          if (state.status === 'cancelled' && phaseIds.includes(current)) request(current);
          onChange();
        }
      }
    })();
  }
  return {
    request,
    get status() { return state.status; },
    get cachedComponents() { return city?.components ?? 0; },
    apply({ phaseId, ruin, evidenceAllowed, retainedVisible }) {
      city?.projection.apply({ phaseId, ruin, evidenceAllowed, retainedVisible });
      return Boolean(city && phaseIds.includes(phaseId) && phaseId !== retainedPhase);
    },
    diagnostics() { return { ...state, phase: current, projection: city?.projection.diagnostics() ?? null,
      retainedObjects: city?.core.phase(retainedPhase).filter(object => object.type === 'building').length ?? 0,
      identityPolicy: retainedPhase ? 'same-first-temple-objects-through-destruction-and-persian-retention' : 'distinct-period-objects-without-unverified-reuse-links',
      historicalRegistrationVerified: false }; },
    evict() { if (city) { release(city.group); city = null; state = { status: 'idle', completed: 0, total: 0 }; } },
    dispose() { disposed = true; if (!materials.facadeOpening) openingMaterial.dispose(); pending?.controller.abort(); if (city) release(city.group); city = null; },
  };
}

// Both periods use the same bounded generator. The successor has distinct IDs;
// proximity does not create unsupported reuse links to the earlier ruins.
export function createSharedEraRuntime(parent, options) {
  const limit = options.maxCachedCities ?? 3;
  if (!Number.isInteger(limit) || limit < 2) throw new Error('City cache requires at least two slots');
  let current = '', entries = [], clock = 0, evictions = 0;
  const lastUsed = new Map();
  const protectedIds = () => new Set(current === RETAINED_PHASE
    ? [SHARED_SLICE_PHASES[0], RETAINED_PHASE]
    : isSharedSlicePhase(current) ? [SHARED_SLICE_PHASES[0]] : [current]);
  function trimCache() { evictions += trimCityCache(entries,{limit,protectedIds:protectedIds(),lastUsed}).length; }
  const callbacks = { ...options, onChange: () => { trimCache(); options.onChange?.(); } };
  const first = createParcelRuntime(parent, { ...callbacks,
    generationPhase: SHARED_SLICE_PHASES[0], destroyedPhase: SHARED_SLICE_PHASES[1],
    phaseIds: [...SHARED_SLICE_PHASES, RETAINED_PHASE], retainedPhase: RETAINED_PHASE });
  const successor = createParcelRuntime(parent, { ...callbacks, footprint: options.successorFootprint,
    generationPhase: RETAINED_PHASE, phaseIds: [RETAINED_PHASE] });
  const expansion = createParcelRuntime(parent, { ...callbacks, footprint: options.expansionFootprint,
    generationPhase: EXPANSION_PHASE, phaseIds: [EXPANSION_PHASE] });
  const replacement = createParcelRuntime(parent, { ...callbacks, footprint: options.replacementFootprint,
    generationPhase: REPLACEMENT_PHASE, phaseIds: [REPLACEMENT_PHASE] });
  entries = [{id:SHARED_SLICE_PHASES[0],runtime:first},{id:RETAINED_PHASE,runtime:successor},
    {id:EXPANSION_PHASE,runtime:expansion},{id:REPLACEMENT_PHASE,runtime:replacement}];
  const runtimes = entries.map(entry=>entry.runtime);
  const active = () => current === REPLACEMENT_PHASE ? replacement : current === EXPANSION_PHASE ? expansion : current === RETAINED_PHASE ? successor : first;
  return {
    request(phaseId) {
      current = phaseId; for (const id of protectedIds()) lastUsed.set(id,++clock);
      for (const runtime of runtimes) runtime.request(phaseId);
      trimCache();
    },
    get status() {
      if (current === RETAINED_PHASE && first.status === 'error') return 'error';
      if (current === RETAINED_PHASE && successor.status === 'ready' && first.status !== 'ready') return first.status;
      return active().status;
    },
    apply(args) { let owned = false; for (const runtime of runtimes) owned = runtime.apply(args) || owned; return owned; },
    diagnostics() {
      const earlier = first.diagnostics(), later = successor.diagnostics();
      const expanded = expansion.diagnostics(), replaced = replacement.diagnostics();
      const primary = current === REPLACEMENT_PHASE ? replaced : current === EXPANSION_PHASE ? expanded : current === RETAINED_PHASE ? later : earlier;
      return { ...earlier, status: this.status,
        completed: primary.completed, total: primary.total,
        error: primary.error || (current === RETAINED_PHASE ? earlier.error : undefined),
        successor: later,
        expansion: expanded,
        replacement: replaced,
        cache: { limit, evictions, residentCities: entries.filter(e=>e.runtime.status==='ready').length,
          residentComponents: entries.reduce((sum,e)=>sum+e.runtime.cachedComponents,0),
          stagingCities: entries.filter(e=>e.runtime.status==='generating').length },
        historicalRegistrationVerified: false };
    },
    dispose() { for (const runtime of runtimes) runtime.dispose(); },
  };
}
