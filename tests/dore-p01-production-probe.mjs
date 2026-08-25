import assert from 'node:assert/strict';

const origin = process.env.DORE_P01_ORIGIN;
const jobId = process.env.DORE_P01_JOB_ID;

if (!origin || !jobId) {
  console.error('Set DORE_P01_ORIGIN and DORE_P01_JOB_ID to a deployed Pages origin and a real subtitle job id.');
  process.exit(2);
}

const base = origin.replace(/\/$/, '');
const resultUrl = `${base}/api/dore/video-subtitle-result?job_id=${encodeURIComponent(jobId)}`;
const res = await fetch(resultUrl, { headers: { accept: 'application/json' } });
assert.equal(res.ok, true, `result endpoint returned ${res.status}`);
const body = await res.json();
assert.equal(body.ok, true);
assert.equal(body.schema, 'dore.video-subtitle-result.v1');
assert.equal(String(body.result?.job_id), String(jobId));
assert.ok(body.result?.reader_state, 'reader_state missing');
assert.ok(body.result?.rights && typeof body.result.rights.download_allowed === 'boolean', 'rights contract missing');
assert.equal(typeof body.result?.download?.available, 'boolean');

if (body.result.download.available) {
  assert.equal(body.result.rights.download_allowed, true);
  const downloadUrl = new URL(body.result.download.url, base);
  const download = await fetch(downloadUrl);
  assert.equal(download.ok, true, `download returned ${download.status}`);
  assert.match(download.headers.get('content-type') || '', /^text\/vtt\b/i);
  assert.match(download.headers.get('content-disposition') || '', /attachment/i);
  const text = await download.text();
  assert.match(text, /^WEBVTT(?:\r?\n|$)/, 'download is not VTT');
} else {
  const denied = await fetch(`${resultUrl}&download=1`);
  assert.equal(denied.status, 403, `non-downloadable result exposed derivative with ${denied.status}`);
  const deniedBody = await denied.json();
  assert.equal(deniedBody.error, 'subtitle_download_not_authorized');
}

console.log(JSON.stringify({
  ok: true,
  origin: base,
  job_id: String(jobId),
  reader_state: body.result.reader_state,
  download_available: body.result.download.available,
  rights_basis: body.result.rights.basis || null
}, null, 2));
