#!/usr/bin/env node

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';
import { spawnSync } from 'node:child_process';

const root = process.cwd();
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'tian-guo-yu-yan-upload-'));
const uploadDir = path.join(tmp, 'upload');
fs.mkdirSync(uploadDir, { recursive: true });

const fixture = Buffer.from('\ufeff# 序言\r\n\r\n原稿第一段。\r\n\r\n# 第一章　要有光\r\n\r\n神說：「要有光。」\r\n', 'utf8');
const sha256 = crypto.createHash('sha256').update(fixture).digest('hex');
const encoded = fixture.toString('base64');
const splitAt = Math.ceil(encoded.length / 2);
const parts = [encoded.slice(0, splitAt), encoded.slice(splitAt)];
parts.forEach((content, index) => fs.writeFileSync(path.join(uploadDir, `part-${String(index).padStart(3, '0')}.b64`), content, 'utf8'));

const manifest = {
  schema: 'dore.native-persist-manuscript.v1',
  projectId: 'book.tian-guo-yu-yan',
  target: 'data/publishing/manuscripts/tian-guo-yu-yan.md',
  kind: 'markdown',
  bytes: fixture.length,
  sha256,
  parts: parts.length,
  sourceIdentity: {
    provider: 'chatgpt-file-library',
    fileId: 'file_00000000ee2c822fbba5855796ec34b2'
  }
};
fs.writeFileSync(path.join(uploadDir, 'manifest.json'), `${JSON.stringify(manifest, null, 2)}\n`, 'utf8');

const canonicalPath = path.join(root, manifest.target);
const receiptPath = path.join(root, 'data/publishing/tian-guo-yu-yan.materialization-receipt.v1.json');
const censusPath = path.join(root, 'data/publishing/tian-guo-yu-yan.manuscript-census.v1.json');
const backups = new Map();
for (const target of [canonicalPath, receiptPath, censusPath]) {
  backups.set(target, fs.existsSync(target) ? fs.readFileSync(target) : null);
}

try {
  const run = spawnSync(process.execPath, ['scripts/tian-guo-yu-yan-native-materialize.mjs', uploadDir], {
    cwd: root,
    encoding: 'utf8'
  });
  if (run.status !== 0) throw new Error(run.stderr || run.stdout || `materializer exit ${run.status}`);

  const persisted = fs.readFileSync(canonicalPath);
  if (!persisted.equals(fixture)) throw new Error('byte identity failed');
  const persistedSha = crypto.createHash('sha256').update(persisted).digest('hex');
  if (persistedSha !== sha256) throw new Error('sha identity failed');

  const receipt = JSON.parse(fs.readFileSync(receiptPath, 'utf8'));
  if (receipt.status !== 'PASS') throw new Error('receipt not PASS');
  if (receipt.canonical.byteIdentityVerified !== true) throw new Error('receipt missing byte identity');
  if (receipt.authority.reconstructedFromRetrievalSnippets !== false) throw new Error('snippet reconstruction boundary lost');

  const census = JSON.parse(fs.readFileSync(censusPath, 'utf8'));
  if (census.source.sha256 !== sha256) throw new Error('census sha drift');
  if (census.source.sourceBytesModified !== false) throw new Error('census modified source');
  if (census.source.newlineNormalizationAppliedForAnalysisOnly !== true) throw new Error('analysis newline normalization expectation failed');
  if (census.exact.topLevelSections !== 2) throw new Error(`expected 2 sections, got ${census.exact.topLevelSections}`);

  console.log(JSON.stringify({
    schema: 'dore.manuscript-native-materialization-smoke.v1',
    status: 'PASS',
    bytes: fixture.length,
    sha256,
    parts: parts.length,
    checks: [
      'chunked-base64-reconstruction',
      'exact-byte-length',
      'sha256-source-to-canonical-identity',
      'utf8-lossless-roundtrip',
      'census-after-materialization',
      'analysis-only-newline-normalization',
      'no-retrieval-snippet-reconstruction'
    ]
  }, null, 2));
} finally {
  for (const [target, previous] of backups) {
    if (previous === null) {
      if (fs.existsSync(target)) fs.rmSync(target);
    } else {
      fs.mkdirSync(path.dirname(target), { recursive: true });
      fs.writeFileSync(target, previous);
    }
  }
  fs.rmSync(tmp, { recursive: true, force: true });
}
