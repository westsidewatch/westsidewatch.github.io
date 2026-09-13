import { relatedWorkIds, focusContext, clearFocus, serializeContext, restoreContext } from './relation-context.mjs';

const motionByKind = {
  flow: 'flow',
  shelf: 'settle',
  card: 'focus',
  spectrum: 'expand'
};

export function projectCollection({ overlay, context, kind }) {
  if (!['flow', 'shelf', 'card', 'spectrum'].includes(kind)) {
    throw new Error(`Unsupported projection kind: ${kind}`);
  }

  const related = relatedWorkIds(overlay, context);
  let items = related;

  if (kind === 'shelf') {
    items = [...related].sort((a, b) => a.workId.localeCompare(b.workId));
  }

  if (kind === 'card') {
    const focused = context.focusedWork;
    items = focused ? related.filter(item => item.workId === focused) : [];
  }

  if (kind === 'spectrum') {
    items = related.map((item, index) => ({
      ...item,
      radialOrder: index,
      anchor: item.relationCue
    }));
  }

  return {
    schema: 'dawn.projection.v1',
    kind,
    context: { ...context },
    items,
    motion: motionByKind[kind]
  };
}

export function transitionProjection({ overlay, context, from, to, workId = null }) {
  let nextContext = { ...context };

  if (workId) nextContext = focusContext(nextContext, workId);
  if (to === 'flow' || to === 'shelf') {
    if (from === 'card' || from === 'spectrum') nextContext = clearFocus(nextContext);
  }

  return {
    from: projectCollection({ overlay, context, kind: from }),
    to: projectCollection({ overlay, context: nextContext, kind: to }),
    serializedContext: serializeContext(nextContext)
  };
}

export function restoreProjection({ overlay, serializedContext, kind }) {
  const context = restoreContext(serializedContext);
  return projectCollection({ overlay, context, kind });
}
