#!/usr/bin/env node
/**
 * Doré Studio Native Binary Publisher
 *
 * Purpose: persist approved Studio images as real binary files inside the repo without
 * chat/base64 staging, browser reconstruction, or runtime fetch bridges.
 *
 * Typical use:
 *   node scripts/dore/publish-studio-asset.mjs \
 *     --input /absolute/path/lam03.png \
 *     --book 25 --chapter 3 \
 *     --asset-id LAM-03-DORE-STUDIO-001 \
 *     --title "Lamentations III" \
 *     --scripture "Lamentations 3" \
 *     --filename lamentations-03-dore-studio-v2.png
 *
 * Batch use:
 *   node scripts/dore/publish-studio-asset.mjs --manifest path/to/jobs.json
 *
 * The tool only changes the working tree. Git/PR/merge stay outside this script so one
 * batch can contain many approved plates and still produce one commit / one PR.
 */
import { readFile, writeFile, mkdir, copyFile, rename, stat } from 'node:fs/promises';
import { dirname, extname, basename, resolve, relative, sep } from 'node:path';
import { createHash } from 'node:crypto';
import process from 'node:process';

const ROOT = resolve(new URL('../..', import.meta.url).pathname);
const STUDIO_DIR = resolve(ROOT, 'static/one/studio');
const REGISTRY = resolve(ROOT, 'static/one/one-studio-assets.js');
const RECEIPTS_DIR = resolve(ROOT, 'static/one/dore-publisher-receipts');
const MARKER = '  document.documentElement.dataset.oneStudioAssets="separate-versioned-library";';

function fail(message) { console.error(`[Doré Publisher] ${message}`); process.exitCode = 1; throw new Error(message); }
function q(value) { return JSON.stringify(String(value ?? '')); }
function sha256(buffer) { return createHash('sha256').update(buffer).digest('hex'); }
function repoPath(path) { return relative(ROOT, path).split(sep).join('/'); }

function parseArgs(argv) {
  const out = {};
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith('--')) continue;
    const key = token.slice(2);
    if (['replace','dry-run'].includes(key)) out[key] = true;
    else out[key] = argv[++i];
  }
  return out;
}

function detect(buffer, extension) {
  const ext = extension.toLowerCase();
  const ascii = (a,b) => buffer.subarray(a,b).toString('ascii');
  if (buffer.length >= 12 && ascii(0,4) === 'RIFF' && ascii(8,12) === 'WEBP') return {kind:'webp', mime:'image/webp'};
  if (buffer.length >= 12 && ascii(4,12).startsWith('ftypavi')) return {kind:'avif', mime:'image/avif'};
  if (buffer.length >= 8 && buffer.subarray(0,8).equals(Buffer.from([137,80,78,71,13,10,26,10]))) return {kind:'png', mime:'image/png'};
  if (buffer.length >= 3 && buffer[0] === 0xff && buffer[1] === 0xd8 && buffer[2] === 0xff) return {kind:'jpeg', mime:'image/jpeg'};
  fail(`unsupported or corrupt image (${ext || 'no extension'})`);
}

function pngSize(buffer) {
  if (buffer.length < 24) return null;
  return {width: buffer.readUInt32BE(16), height: buffer.readUInt32BE(20)};
}
function webpSize(buffer) {
  const chunk = buffer.subarray(12,16).toString('ascii');
  if (chunk === 'VP8X' && buffer.length >= 30) {
    const w = 1 + buffer.readUIntLE(24,3), h = 1 + buffer.readUIntLE(27,3);
    return {width:w,height:h};
  }
  return null;
}
function dimensions(buffer, kind) {
  if (kind === 'png') return pngSize(buffer);
  if (kind === 'webp') return webpSize(buffer);
  return null;
}

function normalizeJob(raw, defaults={}) {
  const job = {...defaults, ...raw};
  job.book = Number(job.book);
  job.chapter = Number(job.chapter);
  if (!Number.isInteger(job.book) || job.book < 1 || job.book > 66) fail(`invalid book: ${job.book}`);
  if (!Number.isInteger(job.chapter) || job.chapter < 1) fail(`invalid chapter: ${job.chapter}`);
  if (!job.input) fail('missing --input');
  if (!job['asset-id'] && !job.assetId) fail('missing --asset-id');
  job.assetId = String(job.assetId || job['asset-id']);
  job.input = resolve(String(job.input));
  job.filename = String(job.filename || basename(job.input));
  if (!/^[A-Za-z0-9._-]+$/.test(job.filename)) fail(`unsafe filename: ${job.filename}`);
  job.title = String(job.title || job.assetId);
  job.scripture = String(job.scripture || '');
  job.alt = String(job.alt || `${job.scripture || `Book ${job.book} chapter ${job.chapter}`} · ONE Studio engraving`);
  job.note = String(job.note || 'Editorially approved Doré-continuation Studio plate.');
  job.approvedAt = String(job.approvedAt || new Date().toISOString().slice(0,10));
  job.replace = Boolean(job.replace);
  return job;
}

async function atomicCopy(source, target) {
  await mkdir(dirname(target), {recursive:true});
  const temp = `${target}.tmp-${process.pid}`;
  await copyFile(source, temp);
  const [src, tmp] = await Promise.all([readFile(source), readFile(temp)]);
  if (sha256(src) !== sha256(tmp)) fail(`atomic copy verification failed: ${target}`);
  await rename(temp, target);
}

function registryLines(job, publicSrc, digest, bytes) {
  const asset = `  registerAsset(${q(job.assetId)},{src:${q(publicSrc)},alt:${q(job.alt)},title:${q(job.title)},source:${q(publicSrc)},artist:"Westside Watch Engraving Studio · Doré continuation",origin:"ONE_STUDIO_DORE_CONTINUATION",palette:"MONOCHROME_ENGRAVING",scripture:${q(job.scripture)},approvedAt:${q(job.approvedAt)},note:${q(`${job.note} SHA-256 ${digest}; ${bytes} bytes.`)}});`;
  const assign = `  registerChapter(${job.book},${job.chapter},${q(job.assetId)},{priority:"P7_ONE_STUDIO_FIXED",basis:"EDITORIAL_FINAL_NATIVE_BINARY"});`;
  return {asset, assign};
}

async function updateRegistry(job, publicSrc, digest, bytes, dryRun) {
  let text = await readFile(REGISTRY, 'utf8');
  if (!text.includes(MARKER)) fail('ONE Studio registry marker not found; aborting to avoid unsafe edit');
  const assetExists = text.includes(`registerAsset(${q(job.assetId)},`);
  const chapterPattern = new RegExp(`registerChapter\\(${job.book},${job.chapter},`);
  const chapterExists = chapterPattern.test(text);
  if ((assetExists || chapterExists) && !job.replace) {
    fail(`registry already contains ${job.assetId} or ${job.book}:${job.chapter}; use --replace only after editorial approval`);
  }
  if (job.replace) {
    if (assetExists) text = text.replace(new RegExp(`^\\s*registerAsset\\(${q(job.assetId).replace(/[.*+?^${}()|[\\]\\]/g,'\\$&')}.*$`, 'm'), '');
    if (chapterExists) text = text.replace(new RegExp(`^\\s*registerChapter\\(${job.book},${job.chapter},.*$`, 'm'), '');
  }
  const {asset, assign} = registryLines(job, publicSrc, digest, bytes);
  text = text.replace(MARKER, `${asset}\n${assign}\n${MARKER}`);
  if (!dryRun) await writeFile(REGISTRY, text, 'utf8');
}

async function publish(job, {dryRun=false}={}) {
  const sourceStat = await stat(job.input).catch(() => null);
  if (!sourceStat?.isFile()) fail(`input file not found: ${job.input}`);
  const buffer = await readFile(job.input);
  const format = detect(buffer, extname(job.input));
  const size = dimensions(buffer, format.kind);
  if (buffer.length < 25_000) fail(`image is only ${buffer.length} bytes; refusing likely over-compressed Studio master`);
  const digest = sha256(buffer);
  const target = resolve(STUDIO_DIR, job.filename);
  if (!target.startsWith(STUDIO_DIR + sep)) fail('target escaped Studio directory');
  const publicSrc = `/one/studio/${job.filename}?v=${digest.slice(0,12)}`;

  if (!dryRun) await atomicCopy(job.input, target);
  if (!dryRun) {
    const persisted = await readFile(target);
    if (persisted.length !== buffer.length || sha256(persisted) !== digest) fail('persisted binary does not match source');
    detect(persisted, extname(target));
  }
  await updateRegistry(job, publicSrc, digest, buffer.length, dryRun);

  const receipt = {
    schema:'ONE_DORE_NATIVE_PUBLISHER_RECEIPT_V1',
    chapterKey:`${String(job.book).padStart(3,'0')}-${String(job.chapter).padStart(3,'0')}`,
    book:job.book, chapter:job.chapter, assetId:job.assetId,
    file:repoPath(target), publicSrc, kind:format.kind, mime:format.mime,
    bytes:buffer.length, sha256:digest, dimensions:size,
    state:'PERSISTED_ASSIGNED_PENDING_DEPLOYMENT', approvedAt:job.approvedAt,
    createdAt:new Date().toISOString()
  };
  const receiptPath = resolve(RECEIPTS_DIR, `${receipt.chapterKey}-${job.assetId}.json`);
  if (!dryRun) { await mkdir(RECEIPTS_DIR,{recursive:true}); await writeFile(receiptPath, JSON.stringify(receipt,null,2)+'\n','utf8'); }
  console.log(JSON.stringify(receipt,null,2));
  return receipt;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const dryRun = Boolean(args['dry-run']);
  let jobs;
  if (args.manifest) {
    const parsed = JSON.parse(await readFile(resolve(args.manifest), 'utf8'));
    jobs = Array.isArray(parsed) ? parsed : parsed.jobs;
    if (!Array.isArray(jobs) || !jobs.length) fail('manifest must be an array or {jobs:[...]}');
    jobs = jobs.map(job => normalizeJob(job));
  } else jobs = [normalizeJob(args)];

  const receipts = [];
  for (const job of jobs) receipts.push(await publish(job,{dryRun}));
  console.error(`[Doré Publisher] ${dryRun?'dry-run ':' '}OK: ${receipts.length} asset(s). Commit the binary files, one-studio-assets.js and receipts together.`);
}

main().catch(error => { if (!process.exitCode) process.exitCode = 1; if (!String(error?.message||'').startsWith('[Doré Publisher]')) console.error(error); });
