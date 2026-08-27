import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';

const root=new URL('../../',import.meta.url);
const read=path=>readFile(new URL(path,root),'utf8');
const source=await read('functions/api/dore/openai-response.js');
const moduleUrl=`data:text/javascript;base64,${Buffer.from(source).toString('base64')}`;
const {createOpenAIResponse,OPENAI_RESPONSE_CONTRACT}=await import(moduleUrl);

let captured=null;
const mockFetch=async(url,options)=>{
  captured={url,options,body:JSON.parse(options.body)};
  return new Response(JSON.stringify({
    id:'resp_dore_contract_test',
    status:'completed',
    model:'gpt-5.4-2026-08-01',
    output:[{type:'message',content:[{type:'output_text',text:'Doré bridge contract passed.'}]}]
  }),{status:200,headers:{'content-type':'application/json','x-request-id':'req_dore_contract_test'}});
};

const result=await createOpenAIResponse({
  OPENAI_API_KEY:'test-key-never-sent',
  OPENAI_PROJECT_ID:'proj_test',
  DORE_CHATGPT_MODEL:'gpt-5.4'
},{
  project_id:'dore-search',
  conversation_id:'conversation-test',
  previous_response_id:'resp_previous_test',
  instructions:'You are Doré.',
  prompt:'Continue this conversation.',
  max_output_tokens:512
},mockFetch);

assert.equal(captured.url,'https://api.openai.com/v1/responses');
assert.equal(captured.options.method,'POST');
assert.equal(captured.options.headers.authorization,'Bearer test-key-never-sent');
assert.equal(captured.options.headers['OpenAI-Project'],'proj_test');
assert.equal(captured.body.model,'gpt-5.4');
assert.equal(captured.body.previous_response_id,'resp_previous_test');
assert.equal(captured.body.store,true);
assert.equal(captured.body.metadata.dore_conversation_id,'conversation-test');
assert.equal(result.provider,'openai');
assert.equal(result.api,'responses');
assert.equal(result.response_id,'resp_dore_contract_test');
assert.equal(result.answer,'Doré bridge contract passed.');
assert.deepEqual(OPENAI_RESPONSE_CONTRACT,{provider:'openai',api:'responses',url:'https://api.openai.com/v1/responses'});

await assert.rejects(
  ()=>createOpenAIResponse({}, {prompt:'must fail'},mockFetch),
  /openai_api_key_unbound/
);

const [respond,conversation,runtime,page]=await Promise.all([
  read('functions/api/dore/respond.js'),
  read('functions/api/dore/conversation.js'),
  read('static/dore/dore-search-runtime.js'),
  read('static/dore/search/index.html')
]);

assert.match(respond,/createOpenAIResponse/);
assert.doesNotMatch(respond,/@cf\/meta\/llama/);
assert.match(conversation,/dore\.search-chatgpt-conversation\.v1/);
assert.match(conversation,/previous_response_id/);
assert.match(runtime,/provider\?\.name!=='openai'/);
assert.match(runtime,/previous_response_id:previousResponseId\(\)/);
assert.match(page,/id="conversation-log"/);
assert.match(page,/dore-search-runtime\.js\?v=chatgpt-bridge-1/);

console.log(JSON.stringify({
  ok:true,
  provider:result.provider,
  api:result.api,
  model:result.model,
  response_id:result.response_id,
  checks:['server-side-api-key','responses-endpoint','continued-response-id','provider-proof','search-page-render-target','no-llama-response-path']
}));
