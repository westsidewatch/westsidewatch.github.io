import assert from 'node:assert/strict';
import { mergeBookIntelligence } from '../static/multiwrite/book-core-client.mjs';

const deterministic = {
  schema: 'dore.book-intelligence-report.v1',
  intent: {
    category: 'biblical-reflection',
    thesis: '作者原始論點',
    audience: '',
    readingMode: 'continuous',
    visualTone: '',
    illustrationDensity: 'low',
    scriptureDensity: 'high'
  },
  structure: { chapterCount: 5 },
  authority: {
    thesisSource: 'author-declared',
    mayRewriteThesis: false,
    substantiveInferenceRequiresReview: true
  }
};

const semantic = {
  schema: 'dore.book-intelligence-report.v2',
  category: 'theological-reflection',
  inferredThesis: '模型不同的推論',
  thesisRelationship: 'tension',
  confidence: 0.88,
  audience: '教會讀者',
  readingMode: 'continuous',
  chapterRoles: [{ id: 'c1', role: 'argument' }],
  argumentRelations: [],
  structuralGaps: ['缺少結語'],
  visualToneHints: ['solemn', 'ancient'],
  evidence: [],
  authority: { declaredThesis: 'author', mayRewriteThesis: false },
  runtime: { semantic: true, degraded: false, reason: '' }
};

const merged = mergeBookIntelligence(deterministic, semantic);
assert.equal(merged.intent.thesis, '作者原始論點', 'semantic inference must not rewrite author thesis');
assert.equal(merged.authority.mayRewriteThesis, false);
assert.equal(merged.semantic.inferredThesis, '模型不同的推論');
assert.equal(merged.semantic.thesisRelationship, 'tension');
assert.equal(merged.intent.audience, '教會讀者');
assert.equal(merged.intent.visualTone, 'solemn / ancient');
assert.equal(merged.semantic.runtime.degraded, false);

const degraded = mergeBookIntelligence(deterministic, {
  schema: 'dore.book-intelligence-report.v2',
  runtime: { semantic: false, degraded: true, reason: 'core-unavailable' }
});
assert.equal(degraded.intent.thesis, '作者原始論點');
assert.equal(degraded.semantic.runtime.degraded, true);
assert.equal(degraded.semantic.runtime.reason, 'core-unavailable');

console.log('multiwrite book Core intelligence merge: PASS');
