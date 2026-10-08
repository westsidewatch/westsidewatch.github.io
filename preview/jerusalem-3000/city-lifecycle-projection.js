// One generated city, projected through time without replacing its objects.
// Aelia Capitolina is a replanned Roman city, not a surviving Herodian residential layer.
const CORE_PHASES = new Set(['herodian-jesus', 'roman-destruction']);
export function isCorePhase(phaseId) {
  return CORE_PHASES.has(phaseId);
}

export function createCityProjection(group, meshes, {
  phaseIds = [...CORE_PHASES], standingPhase = 'herodian-jesus',
} = {}) {
  const activePhases = new Set(phaseIds);
  const snapshots = meshes.map((mesh) => ({
    mesh,
    id:
      mesh.userData.cityObject.objectId ??
      `${mesh.userData.cityObject.parcelId}:building`,
    position: { x: mesh.position.x, y: mesh.position.y, z: mesh.position.z },
    scaleY: mesh.scale.y,
    ground:
      mesh.userData.cityObject.terrainGround ?? mesh.userData.phase2?.groundY,
    confidence: mesh.userData.cityObject.confidence,
    infrastructure: Boolean(mesh.userData.cityObject.infrastructure),
  }));
  let state = { phaseId: '', ruin: 0, visibleBuildings: 0 };
  return {
    apply({ phaseId, ruin = 0, evidenceAllowed = () => true }) {
      const active = activePhases.has(phaseId);
      const amount =
        phaseId === standingPhase ? 0 : Math.max(0, Math.min(1, ruin));
      const scale = 1 - 0.82 * amount;
      group.visible = active;
      const visible = new Set();
      for (const item of snapshots) {
        const { mesh, position, ground } = item;
        const objectScale = item.infrastructure ? 1 : scale;
        mesh.visible = active && evidenceAllowed(item.confidence);
        mesh.position.x = position.x;
        mesh.position.z = position.z;
        mesh.position.y = ground + (position.y - ground) * objectScale;
        mesh.scale.y = item.scaleY * objectScale;
        mesh.userData.cityObject.buildingId = item.id;
        mesh.userData.cityObject.lifecycleState =
          item.infrastructure
            ? 'street-continuity'
            : amount === 0 ? 'standing' : amount === 1 ? 'ruin' : 'destruction';
        if (mesh.visible && mesh.userData.cityObject.parcelId)
          visible.add(item.id);
      }
      state = { phaseId, ruin: amount, visibleBuildings: visible.size };
    },
    diagnostics() {
      const fingerprint = (fields) => {
        let hash = 2166136261;
        for (const item of snapshots) {
          const value = fields(item);
          for (const char of value)
            hash = Math.imul(hash ^ char.charCodeAt(0), 16777619) >>> 0;
        }
        return hash.toString(16);
      };
      return {
        ...state,
        objects: new Set(snapshots.map((item) => item.id)).size,
        components: snapshots.length,
        identityPolicy: 'same-objects-through-ruin',
        identityFingerprint: fingerprint((item) => item.id),
        transformFingerprint: fingerprint((item) =>
          JSON.stringify([
            item.mesh.position.x,
            item.mesh.position.y,
            item.mesh.position.z,
            item.mesh.scale.y,
          ]),
        ),
      };
    },
  };
}
