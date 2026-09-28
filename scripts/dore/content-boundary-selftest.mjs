#!/usr/bin/env node
import assert from 'node:assert/strict';
import { boundaryDecision, contentBoundary } from './content-boundary.mjs';

for (const context of contentBoundary.excludedContexts) {
  assert.equal(boundaryDecision({ contexts:[context] }), 'exclude');
}
assert.equal(boundaryDecision({ uncertain:true }), 'exclude');
for (const context of contentBoundary.allowedContexts) {
  assert.equal(boundaryDecision({ contexts:[context] }), 'continue-rights-and-theology-gates');
}
console.log('Content Boundary PASS', contentBoundary.excludedContexts.length, 'excluded contexts; uncertainty fail-closed');
