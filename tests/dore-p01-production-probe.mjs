import fs from 'node:fs';

const origin = (process.env.DORE_P01_ORIGIN || '').replace(/\/$/, '');
const suppliedJobId = process.env.DORE_P01_JOB_ID || '';
const sourceUrl = process.env.DORE_P01_SOURCE_URL || 'https://youtube.com/watch?v=ak06MSETeo4';
const evidenceFile = process.env.DORE_P01_EVIDENCE_FILE || '';

const evidence = {
  schema: 'dore.p01-production-probe-evidence.v2',
  started_at: new Date().toISOString(),
  origin,
  source_url: sourceUrl,
  supplied_job_id: suppliedJobId || null,
  stages: []
};

function persist(final = false) {
  evidence.updated_at = new Date().toISOString();
  if (final) evidence.completed_at = evidence.updated_at;
  if (evidenceFile) fs.writeFileSync(evidenceFile, `${JSON.stringify(evidence, null, 2)}\n`, 'utf8');
}

async function requestJson(url, options = {}, expected = null) {
  const res = await fetch(url, options);
  const text = await res.text();
  let body = null;
  try { body = JSON.parse(text); } catch {}
  if (expected && !expected.includes(res.status)) {
    throw new Error(`${options.method || 'GET'} ${url} returned ${res.status}: ${text.slice(0, 1000)}`);
  }
  return { res, body, text };
}

async function main() {
  if (!origin) throw new Error('DORE_P01_ORIGIN is required');

  let jobId = suppliedJobId;
  let currentStatus = null;

  if (!jobId) {
    const created = await requestJson(`${origin}/api/dore/video-subtitle`, {
      method: 'POST',
      headers: { 'content-type': 'application/json', accept: 'application/json' },
      body: JSON.stringify({
        url: sourceUrl,
        target_language: 'en',
        mode: 'proofread',
        resource_id: 'p01-production-probe-bibleproject-what-is-the-bible'
      })
    }, [200, 202]);
    if (!created.body?.ok || !created.body?.job_id) throw new Error(`production job creation did not return a real job_id: ${created.text.slice(0, 1000)}`);
    jobId = String(created.body.job_id);
    currentStatus = created.body.status || created.body.existing_job?.status || null;
    evidence.stages.push({ stage: 'create-or-deduplicate-job', ok: true, http: created.res.status, job_id: jobId, status: currentStatus, deduplicated: Boolean(created.body.deduplicated) });
    persist();
  }

  if (!currentStatus) {
    const lookup = await requestJson(`${origin}/api/dore/video-subtitle?job_id=${encodeURIComponent(jobId)}`, { headers: { accept: 'application/json' } }, [200]);
    if (!lookup.body?.ok || !lookup.body?.job) throw new Error(`job lookup failed for ${jobId}`);
    currentStatus = lookup.body.job.status;
    evidence.stages.push({ stage: 'lookup-job', ok: true, http: lookup.res.status, job_id: jobId, status: currentStatus });
    persist();
  }

  const resultReady = new Set(['proofread-complete-result-ready', 'translated-result-ready', 'completed']);
  const captionReady = new Set(['caption-acquired-awaiting-proofread', 'proofread-complete-needs-translation']);

  if (!resultReady.has(currentStatus) && !captionReady.has(currentStatus)) {
    const acquired = await requestJson(`${origin}/api/dore/video-subtitle`, {
      method: 'POST',
      headers: { 'content-type': 'application/json', accept: 'application/json' },
      body: JSON.stringify({ action: 'execute-caption-acquisition', job_id: Number(jobId) })
    }, [200, 202]);
    currentStatus = acquired.body?.execution?.status || acquired.body?.status || null;
    evidence.stages.push({
      stage: 'execute-caption-acquisition',
      ok: Boolean(acquired.body?.ok),
      http: acquired.res.status,
      job_id: jobId,
      status: currentStatus,
      reason: acquired.body?.execution?.reason || acquired.body?.error || null
    });
    persist();
    if (!acquired.body?.ok) throw new Error(`caption acquisition did not succeed: ${acquired.text.slice(0, 1000)}`);
  }

  if (currentStatus === 'caption-acquired-awaiting-proofread') {
    const proofread = await requestJson(`${origin}/api/dore/video-subtitle`, {
      method: 'POST',
      headers: { 'content-type': 'application/json', accept: 'application/json' },
      body: JSON.stringify({ action: 'execute-proofread', job_id: Number(jobId) })
    }, [200]);
    currentStatus = proofread.body?.execution?.status || null;
    evidence.stages.push({
      stage: 'execute-proofread',
      ok: Boolean(proofread.body?.ok),
      http: proofread.res.status,
      job_id: jobId,
      status: currentStatus,
      summary: proofread.body?.execution?.summary || null,
      translation_required: Boolean(proofread.body?.execution?.translation_required)
    });
    persist();
    if (!proofread.body?.ok) throw new Error(`proofread execution did not succeed: ${proofread.text.slice(0, 1000)}`);
  }

  const resultUrl = `${origin}/api/dore/video-subtitle-result?job_id=${encodeURIComponent(jobId)}`;
  const result = await requestJson(resultUrl, { headers: { accept: 'application/json' } }, [200]);
  const body = result.body;
  if (!body?.ok || body.schema !== 'dore.video-subtitle-result.v1') throw new Error(`reader result contract failed: ${result.text.slice(0, 1000)}`);
  if (String(body.result?.job_id) !== String(jobId)) throw new Error(`reader result job_id mismatch: expected ${jobId}`);
  if (!body.result?.reader_state) throw new Error('reader_state missing');
  if (!body.result?.rights || typeof body.result.rights.download_allowed !== 'boolean') throw new Error('rights contract missing');
  if (typeof body.result?.download?.available !== 'boolean') throw new Error('download availability contract missing');

  let rightsBoundary = null;
  if (body.result.download.available) {
    if (body.result.rights.download_allowed !== true) throw new Error('download surfaced without rights permission');
    const downloadUrl = new URL(body.result.download.url, origin);
    const download = await fetch(downloadUrl);
    if (!download.ok) throw new Error(`download returned ${download.status}`);
    if (!/^text\/vtt\b/i.test(download.headers.get('content-type') || '')) throw new Error('download content-type is not text/vtt');
    if (!/attachment/i.test(download.headers.get('content-disposition') || '')) throw new Error('download is missing attachment disposition');
    const text = await download.text();
    if (!/^WEBVTT(?:\r?\n|$)/.test(text)) throw new Error('download is not VTT');
    rightsBoundary = 'authorized-download-verified';
  } else {
    const denied = await requestJson(`${resultUrl}&download=1`, {}, [403]);
    if (denied.body?.error !== 'subtitle_download_not_authorized') throw new Error(`rights denial contract failed: ${denied.text.slice(0, 1000)}`);
    rightsBoundary = 'unauthorized-download-denied';
  }

  evidence.ok = true;
  evidence.job_id = String(jobId);
  evidence.reader_state = body.result.reader_state;
  evidence.status = body.result.status;
  evidence.download_available = body.result.download.available;
  evidence.rights_basis = body.result.rights.basis || null;
  evidence.rights_boundary = rightsBoundary;
  evidence.stages.push({ stage: 'reader-result-and-rights-boundary', ok: true, http: 200, reader_state: body.result.reader_state, status: body.result.status, rights_boundary: rightsBoundary });
  persist(true);
  console.log(JSON.stringify(evidence, null, 2));
}

main().catch(error => {
  evidence.ok = false;
  evidence.error = String(error?.stack || error?.message || error);
  persist(true);
  console.error(JSON.stringify(evidence, null, 2));
  process.exit(1);
});
