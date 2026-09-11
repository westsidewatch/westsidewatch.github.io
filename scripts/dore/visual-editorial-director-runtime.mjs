#!/usr/bin/env node
import { readFile } from 'node:fs/promises';
import { selectEditorialVisuals } from './visual-editorial-director-adapter.mjs';

const GRAPH_URL = new URL('../../data/visual_graph.json', import.meta.url);
const arr = value => Array.isArray(value) ? value : value == null ? [] : [value];

export async function loadVisualGraph(url = GRAPH_URL) {
  return JSON.parse(await readFile(url, 'utf8'));
}

function hydrateCandidate(candidate, graph) {
  const work = arr(graph?.visual_works).find(item => item.id === candidate.visualWorkId);
  if (!work) return null;

  const eligibleIds = new Set(candidate.representationIds || []);
  const representations = arr(work.representations)
    .filter(rep => eligibleIds.has(rep.id))
    .map(rep => ({
      id: rep.id,
      imageUrl: rep.image_url,
      provider: rep.provider || null,
      delivery: rep.delivery || null,
      rights: rep.rights || null,
    }));

  const wantedPresets = new Set(candidate.surfacePresetIds || []);
  const surfacePresets = arr(work.surface_presets)
    .filter(preset => !wantedPresets.size || wantedPresets.has(preset.id))
    .map(preset => ({
      id: preset.id,
      aspectRatio: preset.aspect_ratio || null,
      focalRegionId: preset.focal_region_id || null,
    }));

  return {
    ...candidate,
    title: work.canonical_title || null,
    slug: work.slug || null,
    creator: work.creator || null,
    type: work.type || null,
    scriptureRefs: arr(work.scripture_refs),
    representations,
    surfacePresets,
  };
}

export async function selectEditorialVisualsFromGraph(input, { graph, graphUrl } = {}) {
  const sourceGraph = graph || await loadVisualGraph(graphUrl || GRAPH_URL);
  const selection = selectEditorialVisuals(input, sourceGraph);
  const candidates = selection.candidates
    .map(candidate => hydrateCandidate(candidate, sourceGraph))
    .filter(Boolean);

  return {
    ...selection,
    source: 'dawn.visual-graph.v1',
    graphBound: true,
    candidateCount: candidates.length,
    candidates,
  };
}
