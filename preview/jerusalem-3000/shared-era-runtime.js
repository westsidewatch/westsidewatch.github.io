import * as THREE from 'three';
import { TemporalCityCore } from './temporal-city-core.js';
import { deriveEraRegistration } from './era-registration-adapter.js';
import { buildEraParcelCore } from './herodian-parcel-core.js';
import { buildEraParcelArchitectureAsync } from './herodian-typology-grammar.js';
import { buildHerodianRoadGeometry } from './herodian-road-geometry.js';
import { createCityProjection } from './city-lifecycle-projection.js';

export const SHARED_SLICE_PHASES = ['late-first-temple', 'babylonian-destruction'];
export const isSharedSlicePhase = id => SHARED_SLICE_PHASES.includes(id);

// One provisional first-temple fabric, inherited by destruction in place.
// Reuse is a schematic lifecycle, not evidence of surveyed period-specific parcels.
export function createSharedEraRuntime(parent, { reference, footprint, terrain, materials, onChange = () => {}, onProgress = () => {} }) {
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
    if (!isSharedSlicePhase(phaseId)) {
      pending?.controller.abort();
      if (city) city.group.visible = false;
      return;
    }
    if (disposed || city || pending) return;
    const group = new THREE.Group();
    group.name = 'shared-first-temple-city';
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
        const phaseId = SHARED_SLICE_PHASES[0];
        const core = new TemporalCityCore({ phases: SHARED_SLICE_PHASES.map(id => ({ id })), terrain });
        const registration = deriveEraRegistration(reference, phaseId, footprint);
        const parcels = buildEraParcelCore(core, terrain, {
          phaseId, registration, districtId: registration.districts[0].id,
          dataset: 'provisional-first-temple-footprint-not-surveyed',
        });
        const architecture = await buildEraParcelArchitectureAsync(group, core, sharedMaterials, terrain, {
          phaseId, destroyedPhase: SHARED_SLICE_PHASES[1], signal: controller.signal,
          onProgress: progress => { state = { status: 'generating', ...progress }; onProgress(progress); },
        });
        if (!architecture.buildings || !core.validate().ok) throw new Error('Shared era generated no valid architecture');
        const roads = buildHerodianRoadGeometry(group, registration.roads, sharedMaterials, terrain);
        const projection = createCityProjection(group, [...architecture.meshes, ...roads], {
          phaseIds: SHARED_SLICE_PHASES, standingPhase: phaseId,
        });
        city = { group, core, parcels, architecture, projection };
        state = { status: 'ready', completed: architecture.buildings, total: architecture.buildings,
          yields: architecture.yields, maxBatchMs: architecture.maxBatchMs, elapsedMs: architecture.elapsedMs, authority: registration.authority };
      } catch (error) {
        release(group);
        state = { status: error.name === 'AbortError' ? 'cancelled' : 'error', error: String(error) };
      } finally {
        if (pending === task) pending = null;
        if (!disposed) {
          // A rapid leave/return may request this slice while cancellation settles.
          if (state.status === 'cancelled' && isSharedSlicePhase(current)) request(current);
          onChange();
        }
      }
    })();
  }
  return {
    request,
    get status() { return state.status; },
    apply({ phaseId, ruin, evidenceAllowed }) {
      city?.projection.apply({ phaseId, ruin, evidenceAllowed });
      return Boolean(city && isSharedSlicePhase(phaseId));
    },
    diagnostics() { return { ...state, phase: current, projection: city?.projection.diagnostics() ?? null,
      identityPolicy: 'same-first-temple-objects-through-babylonian-destruction',
      historicalRegistrationVerified: false }; },
    dispose() { disposed = true; if (!materials.facadeOpening) openingMaterial.dispose(); pending?.controller.abort(); if (city) release(city.group); city = null; },
  };
}
