#!/usr/bin/env node
import assert from 'node:assert/strict';
import { deriveDawnEditorialRequests } from './dawn-editorial-context.mjs';

const resources = {
  weekly_theme: {
    title: '風浪中的信靠',
    title_en: 'Trust in the Storm',
    description: '從馬可福音第四章進入風浪中的信靠。',
    scripture_refs: ['Mark 4:35–41'],
    visual_context: ['Sea of Galilee', 'storm', 'boat'],
  },
  resources: [
    {
      name: '經文入口',
      name_en: 'Scripture Entry',
      description: '閱讀本週經文。',
      morning_star: true,
      use_cases: ['每日讀經'],
    },
    { name: 'Not selected', morning_star: false },
  ],
};

const requests = deriveDawnEditorialRequests(resources);
assert.equal(requests.length, 1);
assert.equal(requests[0].id, 'dawn-library-featured');
assert.equal(requests[0].contextSource, 'resources.weekly_theme+morning_stars');
assert.ok(requests[0].input.content.includes('Trust in the Storm'));
assert.ok(requests[0].input.content.includes('Scripture Entry'));
assert.deepEqual(requests[0].input.scriptureRefs, ['Mark 4:35–41']);
assert.deepEqual(requests[0].input.visual, ['Sea of Galilee', 'storm', 'boat']);
assert.equal(requests[0].input.surfacePreset, 'card-8x5');
assert.equal(requests[0].input.limit, 3);
console.log(JSON.stringify({ status: 'PASS', source: requests[0].contextSource }));
