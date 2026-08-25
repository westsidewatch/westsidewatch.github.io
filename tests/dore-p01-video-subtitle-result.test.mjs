import assert from 'node:assert/strict';
import fs from 'node:fs/promises';

const source = await fs.readFile(new URL('../functions/api/dore/video-subtitle-result.js', import.meta.url), 'utf8');
const mod = await import(`data:text/javascript;base64,${Buffer.from(source).toString('base64')}`);

function envWithRow(row) {
  return {
    DORE_SENSORY: {
      prepare() {
        return {
          bind() {
            return { first: async () => row };
          }
        };
      }
    }
  };
}

function makeRow({ status='proofread-complete-result-ready', rights=null }={}) {
  const payload = {
    proofread_caption: {
      format: 'vtt',
      language_code: 'zh-Hant',
      text: 'WEBVTT\n\n00:00:00.000 --> 00:00:01.000\n耶和華',
      summary: { segments: 1, changed: 1 }
    }
  };
  if (rights) payload.rights = rights;
  return {
    id: 42,
    resource_id: 'resource-42',
    url: 'https://youtube.com/watch?v=test',
    canonical_url: 'https://youtube.com/watch?v=test',
    target_language: 'zh-Hant',
    mode: 'proofread',
    status,
    created_at: '2026-08-25T00:00:00Z',
    updated_at: '2026-08-25T00:00:01Z',
    payload_json: JSON.stringify(payload)
  };
}

async function get(url, row) {
  return mod.onRequestGet({ request: new Request(url), env: envWithRow(row) });
}

{
  const res = await get('https://example.test/api/dore/video-subtitle-result?job_id=42', makeRow());
  assert.equal(res.status, 200);
  const body = await res.json();
  assert.equal(body.ok, true);
  assert.equal(body.result.reader_state, 'result-ready-rights-restricted');
  assert.equal(body.result.rights.download_allowed, false);
  assert.deepEqual(body.result.download, { available: false });
  assert.equal(JSON.stringify(body).includes('耶和華'), false, 'raw subtitle text must not leak through public JSON');
}

{
  const res = await get('https://example.test/api/dore/video-subtitle-result?job_id=42&download=1', makeRow());
  assert.equal(res.status, 403);
  const body = await res.json();
  assert.equal(body.error, 'subtitle_download_not_authorized');
}

{
  const row = makeRow({ rights: { subtitle_download: true, basis: 'recorded-test-permission' } });
  const stateRes = await get('https://example.test/api/dore/video-subtitle-result?job_id=42', row);
  const stateBody = await stateRes.json();
  assert.equal(stateBody.result.reader_state, 'result-downloadable');
  assert.equal(stateBody.result.download.available, true);
  assert.equal(stateBody.result.rights.basis, 'recorded-test-permission');

  const downloadRes = await get('https://example.test/api/dore/video-subtitle-result?job_id=42&download=1', row);
  assert.equal(downloadRes.status, 200);
  assert.match(downloadRes.headers.get('content-type') || '', /^text\/vtt/);
  assert.equal(await downloadRes.text(), 'WEBVTT\n\n00:00:00.000 --> 00:00:01.000\n耶和華');
}

{
  const row = makeRow({ status: 'proofread-complete-needs-translation' });
  const res = await get('https://example.test/api/dore/video-subtitle-result?job_id=42', row);
  const body = await res.json();
  assert.equal(body.result.reader_state, 'translation-required');
  assert.equal(body.result.next_step, 'translation-executor');
}

{
  const res = await mod.onRequestGet({ request: new Request('https://example.test/api/dore/video-subtitle-result'), env: envWithRow(null) });
  assert.equal(res.status, 400);
}

console.log('P01 video-subtitle-result contract tests passed');
