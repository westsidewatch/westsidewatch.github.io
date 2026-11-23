import { mkdirSync, writeFileSync } from 'node:fs';
// Zero-dependency Chrome DevTools Protocol visual audit.
// Launch Chrome headless on remote-debugging-port=9222 with a local static server.
// This audit requires a real WebGL scene; a loading/failed screenshot is a failure.
const proofDir = 'artifacts/p2-church-visual-qa';
const doorOnly=process.env.P2_CHURCH_DOOR_ONLY==='1';
const northOnly=process.env.P2_CHURCH_NORTH_ONLY==='1';
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
  const frames=northOnly?[55,59,62,63,64,67,73]:doorOnly?[103,106,108,110]:[187,194,199,202,204,205,211,216,223,27,31,40,55,64,110,121,132,143,154,165,174,9,20,22,89,94,103,236,241,246,248,251];
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
          surface:window.__churchSurfaceAudit||null,
          upperStair:window.__churchUpperStairAudit||null,
          northDoorSteps:window.__churchNorthDoorStepAudit||null,
          topology:window.__churchTopologyAudit||null,
          doorCollision:window.__churchDoorCollisionAudit||null,
          depth:window.__churchDepthLayerAudit||null
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
    if(!state.upperStair||state.upperStair.treads<8||
       state.upperStair.stringers!==1||state.upperStair.risers!==0)
      throw Error('Original upper eight steps must use ONE continuous concealed simple support '+JSON.stringify(state.upperStair));
    if(!state.northDoorSteps||state.northDoorSteps.treads!==3||
       state.northDoorSteps.supports!==3||
       state.northDoorSteps.landingSupports!==2||
       state.northDoorSteps.landingFoundationGapsClosed?.length!==2||
       state.northDoorSteps.landingFoundationGapsClosed.some(h=>Math.abs(h-1.35)>.03)||
       !state.northDoorSteps.unchangedOriginals||
       Math.abs(state.northDoorSteps.baseHeight+1.5)>.015||
       Math.abs(state.northDoorSteps.landingHeight)>.015||
       state.northDoorSteps.gapsClosed?.length!==3||
       state.northDoorSteps.foundationGapsClosed?.length!==3||
       state.northDoorSteps.foundationGapsClosed.some((h,i)=>Math.abs(h-(1.7+i*.35))>.035)||
       state.northDoorSteps.heights?.some((h,i)=>Math.abs(h-.35*(i+1))>.035))
      throw Error('North public sanctuary door still has unsupported terrace slabs '+JSON.stringify(state.northDoorSteps));
    if(!state.topology||!state.topology.physicalUnion||
       state.topology.materialOffsets!==false||
       state.topology.sourceBoxCount<65||
       state.topology.componentCount<5||
       state.topology.mergedSourceCount<40||
       state.topology.originalOverlappingPairs<40)
      throw Error('GLB intersecting solids are not physically unioned: '+JSON.stringify(state.topology));
    if(!state.depth||state.depth.materialOffsets!==false||state.depth.count!==0)
      throw Error('Legacy polygon-offset painting is still active: '+JSON.stringify(state.depth));
    if(!state.doorCollision||state.doorCollision.excludedAnimatedLeaves?.length<6||
       state.doorCollision.staleStaticLeaves?.length)
      throw Error('Opened doors still leave stale static collision boxes: '+JSON.stringify(state.doorCollision));
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
      if([187,199].includes(frame) && safety.cameraPosition?.[2]>-16.55)
        throw Error('Camera left the original north stair aisle into low overhang '+frame+' '+JSON.stringify(safety));
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
    // Image-space QA, not another source-code assertion. R29/R30 falsely
    // passed even while the nocturnal stair rendered as a featureless grey
    // slab (measured image contrast 4.5 at 194s, versus 33.7 after R31).
    if([174,187,194,199,202,205].includes(frame)){
      const probe=`(async()=>{
        const image=new Image();
        image.src='data:image/jpeg;base64,${shot.data}';
        await image.decode();
        const c=document.createElement('canvas');
        c.width=128;c.height=80;
        const g=c.getContext('2d',{willReadFrequently:true});
        g.drawImage(image,0,0,128,80);
        const a=g.getImageData(0,0,128,80).data;
        let sum=0,sq=0;
        for(let i=0;i<a.length;i+=4){
          const lum=(a[i]+a[i+1]+a[i+2])/3;
          sum+=lum;sq+=lum*lum;
        }
        const mean=sum/(128*80);
        return {mean:+mean.toFixed(2),
          contrast:+Math.sqrt(Math.max(0,sq/(128*80)-mean*mean)).toFixed(2)};
      })()`;
      const visual=await evaluate(probe);
      console.log('P2_IMAGE_CONTRAST_'+frame+'='+JSON.stringify(visual));
      if([187,194].includes(frame)&&visual.contrast<20)
        throw Error('Stair is rendered as an unreadable flat wall at '+frame+
          's: '+JSON.stringify(visual));
    }
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

  // 101 exact camera poses, using the very same interpolation and
  // collision solver used by animate(). No unnecessary WebGL redraw per pose.
  const poses=await evaluate("(()=>Array.from({length:101},(_,i)=>window.__churchRoutePoseAudit(+(102+i*.1).toFixed(3))))()");
  if(!Array.isArray(poses)||poses.length!==101)
    throw Error('Cannot sample 101 actual south door route positions');
  let previous=null,maxStep=0,reverse=0,doorFrames=doorOnly?frames.length:0;
  for(const pose of poses){
    const t=pose.at,p=pose.cameraPosition;
    if(!p||p.length!==3||!p.every(Number.isFinite))
      throw Error('Door camera missing '+t);
    if(previous){
      const delta=Math.hypot(...p.map((v,j)=>v-previous[j]));
      maxStep=Math.max(maxStep,delta);
      if(delta>.14)throw Error('Door camera jumped '+delta.toFixed(3)+'m at '+t);
      if(t>=103&&t<=111&&p[0]>previous[0]+.01)reverse++;
    }
    if(pose.cameraPenetrations||pose.forwardOcclusions)
      throw Error('South exit has a false collision at '+t+' '+JSON.stringify(pose));
    previous=p;
  }
  if(reverse)throw Error('South exit went backwards '+reverse+' times');
  // Save a handful of actual rendered frames independently of the
  // 101-position CPU route proof, not 101 slow duplicate screen captures.
  if(!doorOnly&&!northOnly){
    for(const t of [103,106.1,108,110]){
      await evaluate("window.__churchRenderProofFrame("+t+")");
      const img=await send('Page.captureScreenshot',{
        format:'jpeg',quality:65,captureBeyondViewport:false,fromSurface:true
      });
      if(!img.data)throw Error('Missing rendered doorway photo '+t);
      writeFileSync(proofDir+'/south-exit-'+String(t).replace('.','_')+'.jpg',
        Buffer.from(img.data,'base64'));
      doorFrames++;
    }
  }
  console.log('P2_SOUTH_DOOR_EXIT_SWEEP='+JSON.stringify({
    from:102,to:112,samples:poses.length,maxStep:+maxStep.toFixed(4),
    backwardFrames:reverse,doorFrames,actualWebGLDoorShots:true
  }));

  if(!doorOnly&&!northOnly){
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
  }
}finally{
  ws.close();
}
