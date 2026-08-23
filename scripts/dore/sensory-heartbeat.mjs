import fs from 'node:fs/promises';
import path from 'node:path';

const base = (process.env.DORE_SENSORY_BASE_URL || 'https://westsidewatch-github-io.pages.dev').replace(/\/$/, '');
const token = process.env.DORE_HEARTBEAT_TOKEN;
const activePath = path.join('dore-core','memory','sensory-active.json');
const brainPath = path.join('static','dore','brain','knowledge-index.json');

if (!token) throw new Error('DORE_HEARTBEAT_TOKEN is required');

const headers = { authorization: `Bearer ${token}`, 'content-type': 'application/json' };
async function api(method, body) {
  const r = await fetch(`${base}/api/dore/sensory-admin`, { method, headers, body: body ? JSON.stringify(body) : undefined });
  const text = await r.text();
  let data; try { data = JSON.parse(text); } catch { throw new Error(`${method} sensory-admin HTTP ${r.status}: ${text.slice(0,300)}`); }
  if (!r.ok || !data.ok) throw new Error(`${method} sensory-admin failed: ${r.status} ${JSON.stringify(data)}`);
  return data;
}
async function readJson(file, fallback) { try { return JSON.parse(await fs.readFile(file,'utf8')); } catch { return fallback; } }
async function writeJson(file, value) { await fs.mkdir(path.dirname(file),{recursive:true}); await fs.writeFile(file, JSON.stringify(value,null,2)+'\n'); }

const active = await readJson(activePath, { version:1, signals:[] });
const brain = await readJson(brainPath, { nodes:[] });
let changed = false;

// Close signals only after Doré's product-readable brain contains the node explicitly linked by the heartbeat.
for (const item of active.signals || []) {
  if (item.state === 'CONSOLIDATED') continue;
  const node = (brain.nodes || []).find(n => n.id === item.brain_node && n.status === 'CONSOLIDATED');
  if (node) {
    await api('PATCH', { signal_id:item.signal_id, state:'CONSOLIDATED', brain_node:node.id });
    item.state = 'CONSOLIDATED'; item.consolidated_at = new Date().toISOString(); changed = true;
    console.log(`consolidated ${item.signal_id} -> ${node.id}`);
  }
}

// Claim at most one new signal per heartbeat. Research itself is performed by Doré's autonomous learning heartbeat,
// not by hard-coded question answers in this transport layer.
const next = await api('GET');
if (next.signal && !['RESEARCHING','WORKING','CANDIDATE_FOR_EXAM'].includes(next.signal.state)) {
  const s = next.signal;
  const task = `sensory:${s.id}`;
  await api('PATCH', { signal_id:s.id, state:'RESEARCHING', research_task:task });
  const exists = (active.signals || []).some(x => x.signal_id === s.id);
  if (!exists) active.signals.push({ signal_id:s.id, query:s.query, research_task:task, state:'RESEARCHING', claimed_at:new Date().toISOString(), brain_node:null });
  changed = true;
  console.log(`claimed ${s.id}: ${s.query}`);
}

if (changed) { active.updated_at = new Date().toISOString(); await writeJson(activePath, active); }
else console.log('no sensory state change');
