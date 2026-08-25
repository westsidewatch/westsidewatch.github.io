import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

const sourcePath='static/dore/dore-search.js';
const indexPath='static/dore/search-index.json';
const source=fs.readFileSync(sourcePath,'utf8');
const marker='\ninit();\n})();';
assert.ok(source.includes(marker),'unable to instrument dore-search.js test seam');
const instrumented=source.replace(marker,"\nglobalThis.__doreSearchTest={state,buildAliases,search,interpret,textSearch,englishPhraseRelevant};\n})();");

const context={
  console,
  document:{querySelector(){return null}},
  URL,
  URLSearchParams,
  location:{href:'https://example.invalid/search/',search:''},
  history:{replaceState(){}},
  fetch:async()=>{throw new Error('network disabled in browser-search regression test')},
};
context.globalThis=context;
vm.createContext(context);
vm.runInContext(instrumented,context,{filename:sourcePath});

const api=context.__doreSearchTest;
assert.ok(api,'test API was not exposed');
api.state.data=JSON.parse(fs.readFileSync(indexPath,'utf8'));
api.buildAliases();

const run=q=>api.search(q,api.interpret(q));

assert.equal(run('Mortal Shell II').length,0,'unrelated game title must not fabricate Scripture results');
assert.equal(run('Grand Theft Auto').length,0,'unrelated multiword English phrase must not fabricate Scripture results');
assert.ok(run('John 3:16').length>0,'explicit English Scripture reference must still resolve');
assert.ok(run('約翰福音 3:16').length>0,'explicit Chinese Scripture reference must still resolve');
assert.ok(run('begining').length>0,'single-term fuzzy tolerance must remain available');

console.log('Doré browser Search negative-relevance regression: PASS');
