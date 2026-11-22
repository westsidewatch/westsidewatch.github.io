import { mkdirSync, writeFileSync } from 'node:fs';
// Zero-dependency Chrome DevTools Protocol visual audit.
// Launch Chrome headless on remote-debugging-port=9222 with a local static server.
// This audit requires a real WebGL scene; a loading/failed screenshot is a failure.
const proofDir = 'artifacts/p2-church-visual-qa';
mkdirSync(proofDir, { recursive: true });
const sleep = n => new Promise(resolve => setTimeout(resolve, n));
let tabs;
for(let attempt=0;attempt<110;attempt++){
  try{
    const res=await fetch('http://127.0.0.1:9222/json/list');
    if(res.ok){tabs=await res.json();if(tabs.some(x=>x.type==='page'))break;}
  }catch{}
  await sleep(450);
}
const tab=tabs?.find(x=>x.type==='page');
if(!tab?.webSocketDebuggerUrl)throw Error('Chrome debug page unavailable');
const ws=new WebSocket(tab.webSocketDebuggerUrl);
await new Promise((resolve,reject)=>{
  ws.addEventListener('open',resolve,{once:true});
  ws.addEventListener('error',reject,{once:true});
});
let sequence=0;
const pending=new Map(),errors=[];
ws.addEventListener('message',event=>{
  const r=JSON.parse(event.data);
  if(r.id&&pending.has(r.id)){
    const {resolve,reject}=pending.get(r.id);pending.delete(r.id);
    if(r.error)reject(new Error(JSON.stringify(r.error)));
    else resolve(r.result);
  }
  if(r.method==='Runtime.exceptionThrown'){
    const d=r.params?.exceptionDetails||{};
    errors.push(d.exception?.description||d.text||'Unknown JS exception');
  }
  if(r.method==='Runtime.consoleAPICalled'&&r.params?.type==='error'){
    errors.push((r.params.args||[]).map(x=>x.value||x.description).join(' '));
  }
  if(r.method==='Network.loadingFailed'&&r.params?.errorText){
    errors.push('Network: '+r.params.errorText);
  }
});
function send(method,params={}){
  const id=++sequence;
  const promise=new Promise((resolve,reject)=>{pending.set(id,{resolve,reject});});
  ws.send(JSON.stringify({id,method,params}));
  return promise;
}
await send('Page.enable');
await send('Runtime.enable');
await send('Network.enable');
await send('Emulation.setDeviceMetricsOverride',{
  width:900,height:600,deviceScaleFactor:1,mobile:false
});
async function evaluate(expression){
  const r=await send('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});
  if(r.exceptionDetails)throw Error(r.exceptionDetails.exception?.description||r.exceptionDetails.text);
  return r.result?.value;
}
try{
  for(const frame of [9,20,22,40,61,64,89,94,103,110,150,174,204,223,250]){
    errors.length=0;
    await send('Page.navigate',{
      url:'http://127.0.0.1:8765/p2/church-tour.html?proofFrame='+frame
    });
    let state=null;
    for(let retry=0;retry<100;retry++){
      await sleep(220);
      try{
        state=await evaluate(`({
          className:document.body?.className||null,
          hasCanvas:!!document.querySelector('#church-canvas'),
          glb:window.__tourStatus||null,
          error:window.__tourError||null,
          hardware:window.__churchHardwareAudit||null,
          crossLight:window.__churchLightAudit||null
        })`);
      }catch{continue;}
      if(state?.className==='ready')break;
      if(state?.className==='failed')throw Error('Architecture failed '+JSON.stringify(state)+' '+errors.join('; '));
    }
    console.log('P2_BROWSER_FRAME_'+frame+'='+JSON.stringify({state,errors:errors.slice(0,7)}));
    if(state?.className!=='ready')throw Error('Church GLB not ready in browser '+frame+' '+JSON.stringify(state)+' '+errors.join('; '));
    if(!state.hardware || !Array.isArray(state.hardware.remaining) || state.hardware.remaining.length)
      throw Error('Door hardware still present at frame '+frame+' '+JSON.stringify(state.hardware));
    if(!state.hardware.removed?.some(name=>/moving.pull/i.test(name)))
      throw Error('Known V33 moving_pull geometry was not removed from live GLB scene: '+JSON.stringify(state.hardware));
    if(!state.crossLight?.aperture || !state.crossLight?.floor || state.crossLight.sheets!==3 || !state.crossLight.additive)
      throw Error('Cross illumination incomplete at frame '+frame);

    await sleep(700);
    if(frame===103){
      const upper=await evaluate('window.__churchMeshProbe?.(495,230,140)');
      const lower=await evaluate('window.__churchMeshProbe?.(310,510,100)');
      console.log('P2_SUSPENDED_HARDWARE_UPPER_103='+JSON.stringify(upper));
      console.log('P2_SUSPENDED_HARDWARE_LOWER_103='+JSON.stringify(lower));
    }
    const shot=await send('Page.captureScreenshot',{
      format:'jpeg',quality:57,captureBeyondViewport:false,fromSurface:true
    });
    if(!shot.data)throw Error('Missing screenshot '+frame);
    const filename = `${proofDir}/frame-${String(frame).padStart(3,'0')}.jpg`;
    writeFileSync(filename, Buffer.from(shot.data, 'base64'));
    console.log('P2_FRAME_PROOF='+filename);
  }
}finally{
  ws.close();
}
