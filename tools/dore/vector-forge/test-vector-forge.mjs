#!/usr/bin/env node
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const sanitizer = path.join(here, 'sanitize-svg.mjs');
const validator = path.join(here, 'validate-svg.mjs');
const fixture = path.join(here, 'fixtures', 'cropped-glyph-01.svg');
const malicious = path.join(here, 'fixtures', 'malicious-raster.svg');
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'dore-vector-forge-'));
const clean = path.join(tmp, 'cropped-glyph-01.clean.svg');

function run(script, args) {
  return spawnSync(process.execPath, [script, ...args], { encoding: 'utf8' });
}

function extractGeometry(svg) {
  const viewBox = svg.match(/\bviewBox\s*=\s*(["'])(.*?)\1/i)?.[2] ?? null;
  const protectedGroup = svg.match(/<g\b[^>]*\bid=["']protected-glyph["'][^>]*>[\s\S]*?<\/g>/i)?.[0] ?? null;
  const pathData = [...svg.matchAll(/<path\b[^>]*\bd=["']([^"']+)["']/gi)].map(m => m[1]);
  return { viewBox, protectedGroup, pathData };
}

const before = fs.readFileSync(fixture, 'utf8');
const sanitized = run(sanitizer, [fixture, clean]);
assert.equal(sanitized.status, 0, sanitized.stderr || sanitized.stdout);
const after = fs.readFileSync(clean, 'utf8');

assert.deepEqual(extractGeometry(after), extractGeometry(before), 'sanitizer changed crop/geometry authority');

const valid = run(validator, [clean]);
assert.equal(valid.status, 0, valid.stderr || valid.stdout);

const rejected = run(sanitizer, [malicious, path.join(tmp, 'must-not-exist.svg')]);
assert.notEqual(rejected.status, 0, 'malicious raster SVG was accepted');
assert.match(`${rejected.stderr}${rejected.stdout}`, /image|unsafe|non-canonical/i);

console.log(JSON.stringify({
  ok: true,
  gates: {
    cropAuthorityPreserved: true,
    protectedGroupPreserved: true,
    pathDataPreserved: true,
    sanitizedOutputValid: true,
    maliciousRasterRejected: true
  }
}, null, 2));
