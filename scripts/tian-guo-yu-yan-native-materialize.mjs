#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { spawnSync } from 'node:child_process';

const uploadDir = process.argv[2] || '.dore-upload/tian-guo-yu-yan';
const manifestPath = path.join(uploadDir, 'manifest.json');
const canonicalPath = 'data/publishing/manuscripts/tian-guo-yu-yan.md';
const receiptPath = 'data/publishing/tian-guo-yu-yan.materialization-receipt.v1.json';
const censusPath = 'data/publishing/tian-guo-yu-yan.manuscript-census.v1.json';

function fail(message, code = 1) {
  console.error(message);
  process.exit(code);
}

if (!fs.existsSync(manifestPath)) fail(`Missing upload manifest: ${manifestPath}`, 2);
const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));

if (manifest.schema !== 'dore.native-persist-manuscript.v1') fail('Invalid manuscript upload schema.', 3);
if (manifest.projectId !== 'book.tian-guo-yu-yan') fail('Project ID mismatch.', 4);
if (manifest.target !== canonicalPath) fail('Canonical target mismatch.', 5);
if (manifest.kind !== 'markdown') fail('Only markdown canonical source is admitted.', 6);
if (!Number.isInteger(manifest.parts) || manifest.parts < 1) fail('Invalid part count.', 7);
if (!Number.isInteger(manifest.bytes) || manifest.bytes < 1) fail('Invalid byte count.', 8);
if (!/^[a-f0-9]{64}$/i.test(String(manifest.sha256 || ''))) fail('Invalid SHA-256.', 9);
if (manifest.sourceIdentity?.fileId !== 'file_00000000ee2c822fbba5855796ec34b2') fail('Canonical File Library source identity mismatch.', 10);
if (manifest.sourceIdentity?.provider !== 'chatgpt-file-library') fail('Source provider mismatch.', 11);

const chunks = [];
for (let index = 0; index < manifest.parts; index += 1) {
  const part = path.join(uploadDir, `part-${String(index).padStart(3, '0')}.b64`);
  if (!fs.existsSync(part)) fail(`Missing upload part: ${part}`, 20 + index);
  const encoded = fs.readFileSync(part, 'utf8').replace(/\s+/g, '');
  if (!encoded) fail(`Empty upload part: ${part}`, 40 + index);
  chunks.push(encoded);
}

let reconstructed;
try {
  reconstructed = Buffer.from(chunks.join(''), 'base64');
} catch (error) {
  fail(`Base64 reconstruction failed: ${error.message}`, 60);
}

const reconstructedSha = crypto.createHash('sha256').update(reconstructed).digest('hex');
if (reconstructed.length !== manifest.bytes) fail(`Byte-length mismatch: expected ${manifest.bytes}, got ${reconstructed.length}.`, 61);
if (reconstructedSha !== manifest.sha256) fail(`SHA-256 mismatch: expected ${manifest.sha256}, got ${reconstructedSha}.`, 62);

const utf8RoundTrip = Buffer.from(reconstructed.toString('utf8'), 'utf8');
if (!reconstructed.equals(utf8RoundTrip)) fail('Canonical manuscript is not valid lossless UTF-8 markdown.', 63);

fs.mkdirSync(path.dirname(canonicalPath), { recursive: true });
fs.writeFileSync(canonicalPath, reconstructed);
const persisted = fs.readFileSync(canonicalPath);
const persistedSha = crypto.createHash('sha256').update(persisted).digest('hex');
if (!persisted.equals(reconstructed) || persistedSha !== reconstructedSha) fail('Persisted canonical manuscript differs from reconstructed source bytes.', 64);

const census = spawnSync(process.execPath, ['scripts/tian-guo-yu-yan-manuscript-census.mjs', canonicalPath, censusPath], {
  encoding: 'utf8',
  stdio: ['ignore', 'pipe', 'pipe']
});
if (census.status !== 0) fail(`Census failed after materialization:\n${census.stderr || census.stdout}`, 65);

const receipt = {
  schema: 'dore.manuscript-materialization-receipt.v1',
  projectId: 'book.tian-guo-yu-yan',
  status: 'PASS',
  sourceIdentity: manifest.sourceIdentity,
  transport: {
    protocol: 'dore-upload-chunked-base64',
    uploadDir,
    parts: manifest.parts
  },
  source: {
    bytes: manifest.bytes,
    sha256: manifest.sha256
  },
  canonical: {
    path: canonicalPath,
    bytes: persisted.length,
    sha256: persistedSha,
    byteIdentityVerified: true
  },
  census: {
    path: censusPath,
    generated: true
  },
  authority: {
    reconstructedFromRetrievalSnippets: false,
    sourceBytesModified: false,
    authorThesisAuthority: true,
    mayRewriteThesis: false
  }
};

fs.writeFileSync(receiptPath, `${JSON.stringify(receipt, null, 2)}\n`, 'utf8');
console.log(JSON.stringify(receipt, null, 2));
