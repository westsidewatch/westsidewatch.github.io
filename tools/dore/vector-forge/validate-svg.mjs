#!/usr/bin/env node
import fs from 'node:fs';

const file = process.argv[2];
if (!file) {
  console.error('usage: node validate-svg.mjs <asset.svg>');
  process.exit(2);
}

const svg = fs.readFileSync(file, 'utf8');
const failures = [];

if (!/<svg\b/i.test(svg)) failures.push('missing-svg-root');
if (!/\bviewBox\s*=\s*["'][^"']+["']/i.test(svg)) failures.push('missing-viewBox');
if (/<script\b/i.test(svg)) failures.push('script');
if (/<foreignObject\b/i.test(svg)) failures.push('foreignObject');
if (/<image\b/i.test(svg)) failures.push('embedded-raster-or-image');
if (/\b(?:href|xlink:href)\s*=\s*["'](?:https?:|\/\/|data:)/i.test(svg)) failures.push('external-or-data-reference');
if (/url\(\s*["']?(?:https?:|\/\/|data:)/i.test(svg)) failures.push('external-css-reference');
if (/\bon\w+\s*=/i.test(svg)) failures.push('event-handler');

const primitiveCount = (svg.match(/<(?:path|rect|circle|ellipse|line|polyline|polygon)\b/gi) || []).length;
if (primitiveCount === 0) failures.push('no-vector-primitives');

const result = {
  file,
  ok: failures.length === 0,
  failures,
  metrics: {
    primitiveCount,
    pathCount: (svg.match(/<path\b/gi) || []).length,
    groupCount: (svg.match(/<g\b/gi) || []).length,
    embeddedRaster: (svg.match(/<image\b/gi) || []).length,
    scripts: (svg.match(/<script\b/gi) || []).length
  }
};

console.log(JSON.stringify(result, null, 2));
process.exit(result.ok ? 0 : 1);
