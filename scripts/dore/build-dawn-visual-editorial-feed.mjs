#!/usr/bin/env node
import { readFile, writeFile } from 'node:fs/promises';
import { selectEditorialVisualsFromGraph } from './visual-editorial-director-runtime.mjs';

const REQUESTS_URL = new URL('../../data/dawn_visual_editorial_queries.json', import.meta.url);
const OUTPUT_URL = new URL('../../data/dawn_visual_editorial.json', import.meta.url);

const requests = JSON.parse(await readFile(REQUESTS_URL, 'utf8'));
const selections = [];

for (const request of requests.selections || []) {
  const result = await selectEditorialVisualsFromGraph(request.input || {});
  selections.push({
    id: request.id,
    label: request.label || request.id,
    schema: result.schema,
    source: result.source,
    graphBound: result.graphBound === true,
    candidates: result.candidates.map(candidate => ({
      visualWorkId: candidate.visualWorkId,
      score: candidate.score,
      authorityClass: candidate.authorityClass,
      surfacePresetIds: candidate.surfacePresetIds,
    })),
  });
}

const feed = {
  schema: 'dawn.visual-editorial-feed.v1',
  source: 'dore.visual-editorial-director.v1',
  graph: 'dawn.visual-graph.v1',
  selections,
};

await writeFile(OUTPUT_URL, `${JSON.stringify(feed, null, 2)}\n`, 'utf8');
console.log(JSON.stringify({ status: 'PASS', selections: selections.length, output: 'data/dawn_visual_editorial.json' }));
