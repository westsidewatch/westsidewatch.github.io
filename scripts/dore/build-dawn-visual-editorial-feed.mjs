#!/usr/bin/env node
import { readFile, writeFile } from 'node:fs/promises';
import { deriveDawnEditorialRequests } from './dawn-editorial-context.mjs';
import { orchestrateDawnSurfaces } from './dawn-surface-orchestrator.mjs';
import { selectEditorialVisualsFromGraph } from './visual-editorial-director-runtime.mjs';

const resources = JSON.parse(await readFile(new URL('../../data/resources.json', import.meta.url), 'utf8'));
const requests = deriveDawnEditorialRequests(resources);
const selections = [];

for (const request of requests) {
  const result = await selectEditorialVisualsFromGraph(request.input || {});
  const selection = {
    id: request.id,
    label: request.label || request.id,
    contextSource: request.contextSource,
    schema: result.schema,
    source: result.source,
    graphBound: result.graphBound === true,
    candidates: result.candidates.map(candidate => ({
      visualWorkId: candidate.visualWorkId,
      score: candidate.score,
      authorityClass: candidate.authorityClass,
      surfacePresetIds: candidate.surfacePresetIds,
    })),
  };
  selection.surfaceOrchestration = orchestrateDawnSurfaces(selection);
  selections.push(selection);
}

const feed = {
  schema: 'dawn.visual-editorial-feed.v3',
  source: 'dore.visual-editorial-director.v1',
  context: 'dawn.library-live-content.v1',
  surfaceEngine: 'dore.visual-surface-orchestrator.v1',
  graph: 'dawn.visual-graph.v1',
  selections,
};

await writeFile(new URL('../../data/dawn_visual_editorial.json', import.meta.url), JSON.stringify(feed, null, 2) + '\n', 'utf8');
console.log(JSON.stringify({ status: 'PASS', selections: selections.length, context: feed.context, surfaceEngine: feed.surfaceEngine }));
