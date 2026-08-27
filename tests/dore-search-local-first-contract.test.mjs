import assert from 'node:assert/strict';
import fs from 'node:fs';

const runtime=fs.readFileSync('static/dore/dore-search-runtime.js','utf8');
const local=fs.readFileSync('local/dore-local/dore_local.py','utf8');

assert.match(runtime,/LOCAL_HEALTH='http:\/\/127\.0\.0\.1:8788\/health'/);
assert.match(runtime,/LOCAL_CHAT='http:\/\/127\.0\.0\.1:8788\/chat'/);
assert.ok(runtime.indexOf('converseLocal(detail)') < runtime.indexOf('converseCloud(detail'), 'local route must precede cloud fallback');
assert.match(runtime,/if\(!d\)d=await converseCloud\(detail,true\)/);
assert.match(runtime,/Search mode is the default\. No keyword, including 多雷\/Doré, can trigger AI here\./);
assert.match(runtime,/isOpenCommand\(raw\)/);
assert.match(runtime,/isCloseCommand\(raw\)/);
assert.match(local,/ALLOWED_ORIGINS=.*westsidewatch\.github\.io/);
assert.match(local,/Access-Control-Allow-Private-Network/);
assert.match(local,/def do_OPTIONS\(self\)/);
assert.match(local,/HOST=os\.environ\.get\('DORE_LOCAL_HOST','127\.0\.0\.1'\)/);
assert.match(local,/'workers_ai_used':False/);

console.log('DORE_SEARCH_LOCAL_FIRST_CONTRACT_PASS');
