import fs from 'node:fs/promises';
import path from 'node:path';

const base=(process.env.DORE_SENSORY_BASE_URL||'https://westsidewatch-github-io.pages.dev').replace(/\/$/,'');
const token=process.env.DORE_HEARTBEAT_TOKEN;
const activePath=path.join('dore-core','memory','sensory-active.json');
const diagPath=path.join('dore-core','memory','sensory-heartbeat-diagnostic.json');
const brainPath=path.join('static','dore','brain','knowledge-index.json');

async function writeJson(file,value){await fs.mkdir(path.dirname(file),{recursive:true});await fs.writeFile(file,JSON.stringify(value,null,2)+'\n')}
async function readJson(file,fallback){try{return JSON.parse(await fs.readFile(file,'utf8'))}catch{return fallback}}
async function fail(error){await writeJson(diagPath,{ok:false,at:new Date().toISOString(),base,error:String(error?.message||error)});throw error}

if(!token)await fail(new Error('DORE_HEARTBEAT_TOKEN is required'));
const headers={authorization:`Bearer ${token}`,'content-type':'application/json'};
async function api(method,body){
  const r=await fetch(`${base}/api/dore/sensory-admin`,{method,headers,body:body?JSON.stringify(body):undefined});
  const text=await r.text();let data;try{data=JSON.parse(text)}catch{throw new Error(`${method} sensory-admin HTTP ${r.status}: ${text.slice(0,300)}`)}
  if(!r.ok||!data.ok)throw new Error(`${method} sensory-admin failed: ${r.status} ${JSON.stringify(data)}`);
  return data;
}

try{
  const active=await readJson(activePath,{version:1,signals:[]});
  const brain=await readJson(brainPath,{nodes:[]});
  let changed=false;
  for(const item of active.signals||[]){
    if(item.state==='CONSOLIDATED')continue;
    const node=(brain.nodes||[]).find(n=>n.id===item.brain_node&&n.status==='CONSOLIDATED');
    if(node){await api('PATCH',{signal_id:item.signal_id,state:'CONSOLIDATED',brain_node:node.id});item.state='CONSOLIDATED';item.consolidated_at=new Date().toISOString();changed=true}
  }
  const next=await api('GET');
  if(next.signal&&!['RESEARCHING','WORKING','CANDIDATE_FOR_EXAM'].includes(next.signal.state)){
    const s=next.signal,task=`sensory:${s.id}`;
    await api('PATCH',{signal_id:s.id,state:'RESEARCHING',research_task:task});
    if(!(active.signals||[]).some(x=>x.signal_id===s.id))active.signals.push({signal_id:s.id,query:s.query,research_task:task,state:'RESEARCHING',claimed_at:new Date().toISOString(),brain_node:null});
    changed=true;
  }
  if(changed){active.updated_at=new Date().toISOString();await writeJson(activePath,active)}
  await writeJson(diagPath,{ok:true,at:new Date().toISOString(),base,signal:next.signal||null,changed});
}catch(e){await fail(e)}
