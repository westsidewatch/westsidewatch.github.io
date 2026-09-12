export const visualSurfaceContextContract = Object.freeze({
  schema: 'dore.visual-surface-context.v1',
  upstream: ['dawn.visual-graph.v1', 'dore.visual-editorial-director.v1'],
  downstream: 'dore.visual-surface-orchestrator.v1',
  preservesEditorialRank: true,
});
