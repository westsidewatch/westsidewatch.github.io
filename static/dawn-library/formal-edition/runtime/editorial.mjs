import { updateDiscoveryContext } from './discovery.mjs';

export function validateEditorialArtifact(artifact, canonicalIds) {
  if (artifact?.schema !== 'dawn.editorial-world.v1') throw new Error('Invalid editorial schema');
  const allowedKinds = new Set(['morning-star','curated-collection','spectrum-editorial']);
  if (!allowedKinds.has(artifact.kind)) throw new Error(`Unsupported editorial kind: ${artifact.kind}`);
  const refs = artifact.canonicalRefs || [];
  if (!refs.length) throw new Error('Editorial artifact requires canonical refs');
  for (const ref of refs) if (!canonicalIds.has(ref)) throw new Error(`Unknown canonical ref: ${ref}`);
  for (const section of artifact.sections || []) {
    for (const ref of section.canonicalRefs || []) if (!canonicalIds.has(ref)) throw new Error(`Unknown section canonical ref: ${ref}`);
  }
  return true;
}

export function projectEditorialArtifact({ artifact, catalog, context }) {
  const byId = new Map(catalog.map(record => [record.workId, record]));
  const items = (artifact.canonicalRefs || []).map(id => byId.get(id)).filter(Boolean);
  const nextContext = updateDiscoveryContext(context, artifact.contextPatch || {});
  return {
    schema: 'dawn.editorial-projection.v1',
    editorialId: artifact.id,
    kind: artifact.kind,
    title: artifact.title || '',
    dek: artifact.dek || '',
    context: nextContext,
    items,
    sections: (artifact.sections || []).map(section => ({
      ...section,
      items: (section.canonicalRefs || []).map(id => byId.get(id)).filter(Boolean)
    }))
  };
}
