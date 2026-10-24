// One generated city, projected through time without replacing its objects.
// Aelia Capitolina is a replanned Roman city, not a surviving Herodian residential layer.
const CORE_PHASES = new Set(['herodian-jesus', 'roman-destruction']);
export function isCorePhase(phaseId) {
  return CORE_PHASES.has(phaseId);
}

export function cityObjectIdForMesh(mesh){const meta=mesh.userData?.cityObject;return meta?.objectId??(meta?.parcelId?`${meta.parcelId}:building`:null);}

export function createCityProjection(group, meshes, {
  phaseIds = [...CORE_PHASES], standingPhase = 'herodian-jesus', phaseStates = {}, stateForObject = null,
} = {}) {
  const activePhases = new Set(phaseIds);
  const snapshots = meshes.map((mesh) => ({
    mesh,
    id:cityObjectIdForMesh(mesh),
    position: { x: mesh.position.x, y: mesh.position.y, z: mesh.position.z },
    scaleY: mesh.scale.y,
    ground:
      mesh.userData.cityObject.terrainGround ?? mesh.userData.phase2?.groundY,
    confidence: mesh.userData.cityObject.confidence,
    infrastructure: Boolean(mesh.userData.cityObject.infrastructure),
    districtId:mesh.userData.cityObject.districtId||null,
  }));
  let state = { phaseId: '', ruin: 0, visibleBuildings: 0 };
  return {
    apply({ phaseId, ruin = 0, evidenceAllowed = () => true, retainedVisible = false }) {
      const active = activePhases.has(phaseId);
      const policy = phaseStates[phaseId];
      const retained = policy?.state === 'retained-ruin';
      const amount =
        phaseId === standingPhase ? 0 : Math.max(0, Math.min(1, policy?.ruin ?? ruin));
      const scale = 1 - 0.82 * amount;
      group.visible = active && (!retained || retainedVisible);
      const visible = new Set(),districtVisible=new Map(),lifecycleStates=new Map();
      for (const item of snapshots) {
        const { mesh, position, ground } = item;
        if(stateForObject&&!item.infrastructure&&!lifecycleStates.has(item.id))lifecycleStates.set(item.id,stateForObject(item.id,phaseId));
        const ledgerState=lifecycleStates.get(item.id);
        const objectScale = item.infrastructure ? 1 : scale;
        mesh.visible = group.visible && evidenceAllowed(item.confidence) &&
          !(retained && item.infrastructure) && (!stateForObject||item.infrastructure||['build','rebuild','transform','ruin','expand'].includes(ledgerState));
        mesh.position.x = position.x;
        mesh.position.z = position.z;
        if(mesh.userData.restPositions&&mesh.userData.groundHeights){
          mesh.position.y=position.y;mesh.scale.y=item.scaleY;
          if(mesh.userData.cityRuinFactor!==objectScale){const p=mesh.geometry.attributes.position,rest=mesh.userData.restPositions,heights=mesh.userData.groundHeights;for(let i=0;i<p.count;i++)p.setY(i,objectScale===1?rest[i*3+1]:heights[i]+(rest[i*3+1]-heights[i])*objectScale);p.needsUpdate=true;mesh.geometry.computeVertexNormals();mesh.userData.cityRuinFactor=objectScale;}
        }else{mesh.position.y = ground + (position.y - ground) * objectScale;mesh.scale.y = item.scaleY * objectScale;}
        mesh.userData.cityObject.buildingId = item.id;
        mesh.userData.cityObject.lifecycleState =
          retained ? 'retained-ruin' : item.infrastructure
            ? 'street-continuity'
            : amount === 0 ? 'standing' : amount === 1 ? 'ruin' : 'destruction';
        if (mesh.visible && mesh.userData.cityObject.parcelId)
          {visible.add(item.id);if(item.districtId){if(!districtVisible.has(item.districtId))districtVisible.set(item.districtId,new Set());districtVisible.get(item.districtId).add(item.id);}}
        mesh.userData.cityObject.ledgerState=ledgerState||null;
      }
      state = { phaseId, ruin: amount, visibleBuildings: visible.size,
        districtVisible:Object.fromEntries([...districtVisible].map(([id,values])=>[id,values.size])),
        layerState: retained ? 'retained-ruin' : 'active-city',
        retainedVisible: retained && retainedVisible,
        burialDepthVerified: false, reuseLinksVerified: false };
    },
    visibility(){return {...state};},
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
            item.mesh.userData.cityRuinFactor??null,
          ]),
        ),
      };
    },
  };
}
