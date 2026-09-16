const SCOPE_WEIGHT = Object.freeze({ local: 0, skill: 1, 'skill-family': 2, 'cross-capability': 3, 'core-principle': 4 });
const HIGH_SIGNAL = new Set(['capability-gap', 'transfer-signal']);

export function clusterObservations(observations = []) {
  const clusters = new Map();
  for (const observation of observations) {
    if (!observation || observation.status === 'dismissed' || observation.status === 'superseded') continue;
    const key = observation.recurrenceKey || `${observation.kind}:${observation.signal.trim().toLowerCase()}`;
    const cluster = clusters.get(key) || { key, observations: [], capabilities: new Set(), surfaces: new Set(), maxScope: 'local' };
    cluster.observations.push(observation);
    for (const capability of observation.relatedCapabilities || []) cluster.capabilities.add(capability);
    if (observation.source?.surface) cluster.surfaces.add(observation.source.surface);
    if ((SCOPE_WEIGHT[observation.scope] ?? 0) > (SCOPE_WEIGHT[cluster.maxScope] ?? 0)) cluster.maxScope = observation.scope;
    clusters.set(key, cluster);
  }
  return [...clusters.values()].map(classifyCluster);
}

export function classifyCluster(cluster) {
  const count = cluster.observations.length;
  const kinds = new Set(cluster.observations.map(o => o.kind));
  const crossSurface = cluster.surfaces.size > 1;
  const crossCapability = cluster.capabilities.size > 1 || SCOPE_WEIGHT[cluster.maxScope] >= SCOPE_WEIGHT['cross-capability'];
  const explicitPrinciple = cluster.maxScope === 'core-principle';
  const highSignal = [...kinds].some(kind => HIGH_SIGNAL.has(kind));

  let disposition = 'local-defect';
  if (explicitPrinciple) disposition = 'principle-candidate';
  else if (crossCapability || (crossSurface && count >= 2)) disposition = 'transfer-candidate';
  else if (highSignal || count >= 3) disposition = 'skill-candidate';
  else if (count >= 2) disposition = 'watch-pattern';

  return {
    key: cluster.key,
    disposition,
    observationCount: count,
    kinds: [...kinds].sort(),
    capabilities: [...cluster.capabilities].sort(),
    surfaces: [...cluster.surfaces].sort(),
    maxScope: cluster.maxScope,
    observationIds: cluster.observations.map(o => o.id),
    authority: { mayPromoteCanonical: false, requiresEvaluation: disposition !== 'local-defect' }
  };
}
