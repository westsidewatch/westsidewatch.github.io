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
  // Load and decompress the architectural GLB ONCE. The tour's own animation
  // loop reads proofFrame from location.search on every frame; stepping the
  // URL with replaceState requires no reloading or lost WebGL state.
  const frames=[187,194,199,204,211,216,223,27,31,40,55,64,110,121,132,143,154,165,174,9,20,22,89,94,103,236,241,246,248,251];
  await send('Page.navigate',{
    url:'http://127.0.0.1:8765/p2/church-tour.html?proofFrame='+frames[0]
  });
  for(let index=0;index<frames.length;index++){
    const frame=frames[index];
    errors.length=0;
    if(index>0){
      await evaluate("history.replaceState(null,'','?proofFrame="+frame+"')");
      await evaluate("window.__churchRenderProofFrame("+frame+")");
    }

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
          crossLight:window.__churchLightAudit||null,
          spatial:window.__churchSpatialAudit||null,
          surface:window.__churchSurfaceAudit||null
        })`);
      }catch{continue;}
      if(state?.className==='ready')break;
      if(state?.className==='failed')throw Error('Architecture failed '+JSON.stringify(state)+' '+errors.join('; '));
    }
    // The ready class is set before the first RAF; force the requested 3D
    // frame before reading any per-frame spatial/lighting telemetry.
    if(state?.className==='ready' && !state.spatial){
      await evaluate("window.__churchRenderProofFrame("+frame+")");
      state.spatial=await evaluate('window.__churchSpatialAudit');
    }
    console.log('P2_BROWSER_FRAME_'+frame+'='+JSON.stringify({state,errors:errors.slice(0,7)}));
    if(state?.className!=='ready')throw Error('Church GLB not ready in browser '+frame+' '+JSON.stringify(state)+' '+errors.join('; '));
    if(!state.hardware || !Array.isArray(state.hardware.remaining) || state.hardware.remaining.length)
      throw Error('Door hardware still present at frame '+frame+' '+JSON.stringify(state.hardware));
    if(!state.spatial || state.spatial.ghostRoofs<2 || !state.surface || !state.surface.glassSinglePass || state.surface.planeThreshold!==.24 || !Array.isArray(state.surface.removed))
      throw Error('Spatial clearance mesh cleanup absent: '+JSON.stringify(state.spatial));
    if(frame>=40&&frame<=223&&state.spatial.ghostRoofVisible!==0)
      throw Error('Ghost roof still obscures inhabited spaces at frame '+frame);
    if(!state.hardware.removed?.some(name=>/moving.pull/i.test(name)))
      throw Error('Known V33 moving_pull geometry was not removed from live GLB scene: '+JSON.stringify(state.hardware));
    if(!state.crossLight?.aperture || !state.crossLight?.floor || state.crossLight.sheets!==3 || !state.crossLight.additive)
      throw Error('Cross illumination incomplete at frame '+frame);
    if(Math.abs((state.crossLight?.crossCenter?.[1]??0)-3.65)>.001)
      throw Error('Cross illumination not aligned to the original 3.65m aperture at frame '+frame);
    if(state.crossLight?.bounceSources!==2)
      throw Error('Cross light must illuminate actual surfaces with two real PBR light sources, not only planes: '+JSON.stringify(state.crossLight));
    if(!state.crossLight?.volumeShader)
      throw Error('Volumetric cross shaft GLSL renderer missing '+frame);
    if(!state.crossLight?.beamTracksSun)
      throw Error('Volumetric light must track the sunlit floor impact: '+frame);
    if(!state.crossLight?.adaptiveExposure)
      throw Error('Cross highlight exposure compensation missing at frame '+frame);

    await sleep(300);
    let clock=await evaluate('window.__churchFrameAudit');
    if(clock?.at!==frame){
      await evaluate("window.__churchRenderProofFrame("+frame+")");
      clock=await evaluate('window.__churchFrameAudit');
    }
    if(!clock||Math.abs(clock.at-frame)>0.01)
      throw Error('Actual rendered camera/time did not advance to proof frame '+frame+' '+JSON.stringify(clock));
    if((frame>=187&&frame<=223)||(frame>=22&&frame<=64)){
      const safety=await evaluate('window.__churchSafetyAudit');
      console.log('P2_UPPER_ENTRANCE_CAMERA_'+frame+'='+JSON.stringify(safety));
      if(!safety || safety.at!==frame)
        throw Error('Collision telemetry missing in entrance/stairs at '+frame);
      if(frame>=187 && (safety.cameraPenetrations||safety.forwardOcclusions))
        throw Error('Upper stair camera still intersects geometry at '+frame+' '+JSON.stringify(safety));
    }
    if([27,31,187,194,199,204,211,216,223].includes(frame)){
      const near=await evaluate('window.__churchMeshProbe?.(450,300,180)');
      console.log('P2_UNFINISHED_REGION_MESH_'+frame+'='+JSON.stringify(near));
    }
    if(frame>=132&&frame<=176){
      const safety=await evaluate('window.__churchSafetyAudit');
      const route=await evaluate('window.__churchRouteClearanceAudit');
      console.log('P2_FORUM_HEADROOM_'+frame+'='+JSON.stringify({safety,route}));
      if(!safety||safety.at!==frame||safety.boxes<1||!route)
        throw Error('No live mesh collision checks at frame '+frame);
      if(route.sampledFrames!==111||route.blockedFrames?.length)
        throw Error('Full C-forum camera sweep has blocked frames: '+JSON.stringify(route));
      if(route.maxCameraDisplacement>0.95)
        throw Error('Camera would need an unsafe corrective jump '+JSON.stringify(route));
      if(safety.cameraPenetrations||safety.forwardOcclusions)
        throw Error('Camera cuts into/looks through a near solid at frame '+frame+' '+JSON.stringify(safety));
    }
    if(Math.abs(clock.crossHeight-3.65)>0.001 || !Number.isFinite(clock.portalIntensity))
      throw Error('Cross daylight shader/real PBR bounce not active '+frame+' '+JSON.stringify(clock));
    if(!Number.isFinite(clock.beamAlignment) || clock.beamAlignment<0.99)
      throw Error('Cross beam diverged from true aperture-to-floor direction at frame '+frame+' '+JSON.stringify(clock));
    if(!Number.isFinite(clock.airStrength)||clock.airStrength>0.166
       || !Number.isFinite(clock.exposure)||clock.exposure<0.70||clock.exposure>1.05)
      throw Error('Cross optical energy/exposure out of calibrated range '+frame+' '+JSON.stringify(clock));
    if(frame>=236){
      const finale=await evaluate('window.__churchFinaleAudit');
      console.log('P2_OUTWARD_CROSS_FINALE_'+frame+'='+JSON.stringify(finale));
      if(!state.crossLight?.facadeWarmth)throw Error('Exterior warm facade reflection missing');
      if(!state.crossLight?.outwardFinale||!finale||!finale.skyGradient
         || finale.direction!=='inside-to-outside')
        throw Error('Finale lacks inside-out cross illumination at '+frame+' '+JSON.stringify(finale));
      if(frame===251&&(finale.twilight<.99||finale.crossCore<.35
        || finale.interiorLamp<11||finale.exteriorLamp<10||finale.outwardBeam<.14
        || finale.facadeBounce<18||finale.groundPool<.22))
        throw Error('Final dusk cross must glow from home into the world '+JSON.stringify(finale));
    }
    console.log('P2_CROSS_LIGHT_FRAME_'+frame+'='+JSON.stringify(clock));
    if([132,143,154,165].includes(frame)){
      const near=await evaluate('window.__churchMeshProbe?.(450,300,110)');
      console.log('P2_C_FORUM_CAMERA_PROBE_'+frame+'='+JSON.stringify(near));
    }
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
    if(frame===251){
      const proof=await send('Page.captureScreenshot',{
        format:'jpeg',quality:37,captureBeyondViewport:false,fromSurface:true
      });
      console.log('P2_FINAL_CROSS_IMAGE_BASE64='+proof.data);
    }
    const filename = `${proofDir}/frame-${String(frame).padStart(3,'0')}.jpg`;
    writeFileSync(filename, Buffer.from(shot.data, 'base64'));
    console.log('P2_FRAME_PROOF='+filename);
  }
  // Prove the public chapter URL starts *in the sanctuary* but continues
  // the original animation normally. No proofFrame freeze on this request.
  await send('Page.navigate',{
    url:'http://127.0.0.1:8765/p2/church-tour.html?startAt=89'
  });
  let chapelReady=false;
  for(let retry=0;retry<110;retry++){
    await sleep(220);
    try{
      chapelReady=await evaluate("document.body?.classList.contains('ready')===true");
      if(chapelReady)break;
    }catch{}
  }
  if(!chapelReady)throw Error('Direct 3D sanctuary preview did not load');
  await sleep(700);
  const chapelClock=await evaluate('window.__churchFrameAudit');
  if(!chapelClock || chapelClock.at<89 || chapelClock.at>94)
    throw Error('Sanctuary preview did not start at chapter 81: '+JSON.stringify(chapelClock));
  if(!Number.isFinite(chapelClock.portalIntensity) || chapelClock.portalIntensity<1)
    throw Error('Direct sanctuary preview must begin with illuminated cross, not at night: '+JSON.stringify(chapelClock));
  console.log('P2_DIRECT_CHAPEL_PREVIEW='+JSON.stringify(chapelClock));
  const chapelShot=await send('Page.captureScreenshot',{
    format:'jpeg',quality:65,captureBeyondViewport:false,fromSurface:true
  });
  if(!chapelShot.data)throw Error('Direct chapel preview returned no screenshot');
  writeFileSync(proofDir+'/chapel-direct-preview.jpg',Buffer.from(chapelShot.data,'base64'));
}finally{
  ws.close();
}
