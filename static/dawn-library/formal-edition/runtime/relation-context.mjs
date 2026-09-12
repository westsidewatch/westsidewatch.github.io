export function relatedWorkIds(overlay, context) {
  const anchors = new Set(context.anchors || []);
  const allowedTypes = new Set(context.relations || []);
  const rows = new Map();
  for (const edge of overlay.edges || []) {
    if (!anchors.has(edge.to)) continue;
    if (allowedTypes.size && !allowedTypes.has(edge.type)) continue;
    if (!edge.from.startsWith('dawn:')) continue;
    const previous = rows.get(edge.from);
    if (!previous || (edge.weight ?? 0) > previous.weight) {
      rows.set(edge.from, { workId: edge.from, weight: edge.weight ?? 0, relationCue: edge.to });
    }
  }
  return [...rows.values()].sort((a, b) => b.weight - a.weight || a.workId.localeCompare(b.workId));
}

export function focusContext(context, workId) {
  return { ...context, focusedWork: workId };
}

export function clearFocus(context) {
  return { ...context, focusedWork: null };
}

export function serializeContext(context) {
  const stable = {
    schema: context.schema,
    anchors: context.anchors || [],
    query: context.query || '',
    semanticIntent: context.semanticIntent || '',
    relations: context.relations || [],
    facets: context.facets || {},
    ordering: context.ordering || '',
    discoveryDistance: context.discoveryDistance ?? 0,
    cursor: context.cursor ?? null,
    origin: context.origin || '',
    focusedWork: context.focusedWork ?? null
  };
  return encodeURIComponent(JSON.stringify(stable));
}

export function restoreContext(serialized) {
  return JSON.parse(decodeURIComponent(serialized));
}
