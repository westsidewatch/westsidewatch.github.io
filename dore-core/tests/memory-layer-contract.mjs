import fs from 'node:fs';
import assert from 'node:assert/strict';

const api=fs.readFileSync('functions/api/dore/memory.js','utf8');
const sql=fs.readFileSync('cloudflare/d1/002_dore_conversation_memory.sql','utf8');
const doc=fs.readFileSync('dore-core/projects/DORÉ-CONVERSATION-MEMORY-LAYER-V1.md','utf8');

for(const table of ['dore_conversations','dore_messages','dore_memory_chunks'])assert.ok(sql.includes(table),`missing ${table}`);
assert.ok(sql.includes('conversation_id TEXT NOT NULL'));
assert.ok(sql.includes('project_id TEXT NOT NULL'));
assert.ok(sql.includes('idx_dore_messages_conversation_created'));
assert.ok(sql.includes('idx_dore_messages_project_created'));

assert.ok(api.includes("error:'scope_required'"),'GET must reject unscoped retrieval');
assert.ok(api.includes('WHERE conversation_id=?1 AND project_id=?2'),'strong scope query missing');
assert.ok(api.includes('WHERE conversation_id=?1 ORDER BY'),'conversation scope query missing');
assert.ok(api.includes('WHERE project_id=?1 ORDER BY'),'project scope query missing');
assert.ok(api.includes('DORE_MEMORY_ARCHIVE'),'optional R2 archive hook missing');
assert.ok(api.includes('DORE_MEMORY_VECTOR'),'Vectorize readiness hook missing');
assert.ok(api.includes('content_sha256'),'dedupe hash missing');
assert.ok(api.includes('conversation_id=?1 AND content_sha256=?2 AND role=?3'),'conversation-local dedupe missing');

assert.match(doc,/Never use vector similarity as the first\/only selector/i);
assert.match(doc,/current `conversation_id`/i);
assert.match(doc,/restrict first to the active `project_id`/i);
assert.match(doc,/public multi-user operation requires an authenticated user\/tenant boundary/i);
assert.match(doc,/free-first/i);

console.log('Doré Conversation Memory Layer v1 contract: PASS');
