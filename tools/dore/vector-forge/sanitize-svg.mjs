#!/usr/bin/env node
import fs from 'node:fs';

const [input, output] = process.argv.slice(2);
if (!input || !output) {
  console.error('usage: node sanitize-svg.mjs <input.svg> <output.svg>');
  process.exit(2);
}

let svg = fs.readFileSync(input, 'utf8');
if (!/<svg\b/i.test(svg)) throw new Error('missing SVG root');

// Fail closed for constructs that can execute code, load foreign content,
// hide raster data, or alter geometry in ways the canonical asset cannot audit.
const forbidden = [
  ['script', /<script\b/i],
  ['foreignObject', /<foreignObject\b/i],
  ['image', /<image\b/i],
  ['event-handler', /\bon\w+\s*=/i],
  ['external-reference', /\b(?:href|xlink:href)\s*=\s*["'](?:https?:|\/\/|data:)/i],
  ['external-css-reference', /url\(\s*["']?(?:https?:|\/\/|data:)/i]
];
for (const [name, re] of forbidden) {
  if (re.test(svg)) throw new Error(`refusing unsafe/non-canonical SVG: ${name}`);
}

// Remove metadata that is not part of rendered geometry. Do not rewrite paths,
// transforms, viewBox, clipPath, mask or group ordering: crop authority wins.
svg = svg
  .replace(/<\?xml[^>]*\?>\s*/gi, '')
  .replace(/<!DOCTYPE[^>]*>\s*/gi, '')
  .replace(/<!--([\s\S]*?)-->/g, '')
  .replace(/<metadata\b[^>]*>[\s\S]*?<\/metadata>/gi, '')
  .replace(/\s+xmlns:xlink=["'][^"']*["']/gi, '')
  .trim();

if (!/\bviewBox\s*=\s*["'][^"']+["']/i.test(svg)) {
  throw new Error('refusing SVG without explicit viewBox');
}
if (!/<(?:path|rect|circle|ellipse|line|polyline|polygon)\b/i.test(svg)) {
  throw new Error('refusing SVG without vector primitives');
}

fs.writeFileSync(output, `${svg}\n`);
console.log(JSON.stringify({ ok: true, input, output, geometryRewritten: false }, null, 2));
