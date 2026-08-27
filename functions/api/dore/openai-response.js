const OPENAI_RESPONSES_URL='https://api.openai.com/v1/responses';
export const DEFAULT_OPENAI_MODEL='gpt-5.4';

const clean=(value,max=24000)=>String(value??'').normalize('NFKC').trim().slice(0,max);
const bounded=(value,fallback,min,max)=>{
  const n=Number(value);
  return Number.isFinite(n)?Math.max(min,Math.min(max,Math.trunc(n))):fallback;
};

function responseText(payload={}){
  const direct=clean(payload.output_text,24000);
  if(direct)return direct;
  const parts=[];
  for(const item of payload.output||[]){
    if(item?.type!=='message')continue;
    for(const content of item.content||[]){
      if(content?.type==='output_text'&&content.text)parts.push(content.text);
    }
  }
  return clean(parts.join('\n'),24000);
}

function metadata(input={}){
  const pairs={
    dore_project_id:clean(input.project_id,160),
    dore_conversation_id:clean(input.conversation_id,160)
  };
  return Object.fromEntries(Object.entries(pairs).filter(([,value])=>value));
}

export async function createOpenAIResponse(env,input={},fetchImpl=globalThis.fetch){
  const apiKey=clean(env?.OPENAI_API_KEY,512);
  if(!apiKey)throw new Error('openai_api_key_unbound');
  if(typeof fetchImpl!=='function')throw new Error('openai_fetch_unavailable');

  const prompt=clean(input.prompt??input.query,24000);
  if(!prompt)throw new Error('empty_query');
  const model=clean(env?.DORE_CHATGPT_MODEL||input.model||DEFAULT_OPENAI_MODEL,120);
  const previousResponseId=clean(input.previous_response_id,180);
  const body={
    model,
    instructions:clean(input.instructions,16000),
    input:prompt,
    max_output_tokens:bounded(input.max_output_tokens,900,128,2400),
    store:true,
    metadata:metadata(input)
  };
  if(/^resp_[A-Za-z0-9_-]+$/.test(previousResponseId))body.previous_response_id=previousResponseId;

  const headers={
    authorization:`Bearer ${apiKey}`,
    'content-type':'application/json',
    accept:'application/json'
  };
  const projectId=clean(env?.OPENAI_PROJECT_ID,160);
  if(projectId)headers['OpenAI-Project']=projectId;

  const controller=new AbortController();
  const timeout=setTimeout(()=>controller.abort('openai_timeout'),bounded(input.timeout_ms,45000,5000,90000));
  let response;
  try{
    response=await fetchImpl(OPENAI_RESPONSES_URL,{method:'POST',headers,body:JSON.stringify(body),signal:controller.signal});
  }catch(error){
    if(controller.signal.aborted)throw new Error('openai_request_timeout');
    throw new Error(`openai_request_failed:${clean(error?.message||error,240)}`);
  }finally{
    clearTimeout(timeout);
  }

  let payload={};
  try{payload=await response.json()}catch{throw new Error(`openai_invalid_json:${response.status}`)}
  if(!response.ok){
    const code=clean(payload?.error?.code||payload?.error?.type||'request_error',120);
    throw new Error(`openai_http_${response.status}:${code}`);
  }
  if(payload?.error){
    const code=clean(payload.error.code||payload.error.type||'response_error',120);
    throw new Error(`openai_response_error:${code}`);
  }
  const answer=responseText(payload);
  if(!answer)throw new Error('openai_response_empty');

  return{
    answer,
    provider:'openai',
    api:'responses',
    model:clean(payload.model||model,160),
    response_id:clean(payload.id,180),
    request_id:clean(response.headers?.get?.('x-request-id'),180),
    status:clean(payload.status||'completed',80)
  };
}

export const OPENAI_RESPONSE_CONTRACT={provider:'openai',api:'responses',url:OPENAI_RESPONSES_URL};
