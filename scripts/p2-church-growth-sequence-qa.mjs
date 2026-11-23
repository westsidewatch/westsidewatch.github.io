// Actual P2 first-layer browser acceptance: Red Sea FIRST, then
// original scroll-built WebGL church, then the approved Magazine handoff.
// These frames use the PRODUCTION P2 scripts and original maquette iframe.
import {mkdirSync,writeFileSync} from "node:fs";
const out="artifacts/p2-church-growth-sequence";
mkdirSync(out,{recursive:true});
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
let pages;
for(let i=0;i<110;i++){
  try{const r=await fetch("http://127.0.0.1:9222/json/list");
    if(r.ok){pages=await r.json();if(pages.some(p=>p.type==="page"))break;}
  }catch{}
  await sleep(300);
}
const page=pages?.find(p=>p.type==="page");
if(!page?.webSocketDebuggerUrl)throw Error("Chrome CDP unavailable");
const ws=new WebSocket(page.webSocketDebuggerUrl);
await new Promise((yes,no)=>{
  ws.addEventListener("open",yes,{once:true});
  ws.addEventListener("error",no,{once:true});
});
let seq=0;
const pending=new Map(),errors=[];
ws.addEventListener("message",e=>{
  const r=JSON.parse(e.data);
  if(r.id&&pending.has(r.id)){
    const p=pending.get(r.id);pending.delete(r.id);
    if(r.error)p.reject(Error(JSON.stringify(r.error)));
    else p.resolve(r.result);
  }
  if(r.method==="Runtime.exceptionThrown")
    errors.push(r.params?.exceptionDetails?.exception?.description||"Script exception");
});
const send=(method,params={})=>{
  const id=++seq;
  const promise=new Promise((resolve,reject)=>pending.set(id,{resolve,reject}));
  ws.send(JSON.stringify({id,method,params}));
  return promise;
};
async function evaluate(expression){
  const r=await send("Runtime.evaluate",{expression,returnByValue:true,awaitPromise:true});
  if(r.exceptionDetails)throw Error(r.exceptionDetails.exception?.description||"Script evaluation error");
  return r.result?.value;
}
async function capture(name){
  const r=await send("Page.captureScreenshot",
    {format:"jpeg",quality:73,captureBeyondViewport:false,fromSurface:true});
  if(!r.data)throw Error("WebGL image missing "+name);
  writeFileSync(out+"/"+name+".jpg",Buffer.from(r.data,"base64"));
}
async function at(vh){
  // The isolated P2 church preview maps scroll distance d to
  // scene pose 2.37 + d * .58. It uses the SAME live drawScene code.
  const y=Math.round((vh-2.37)/.58*850);
  await evaluate("window.scrollTo({top:"+Math.max(0,y)+",behavior:'instant'})");
  for(let i=0;i<70;i++){
    await sleep(90);
    const s=await evaluate(`(()=>{
      const root=document.querySelector(".showcase");
      const frame=document.querySelector(".church-editorial__maquette");
      const progress=Number(root?.dataset.p2ChurchGrowth);
      const pose=Number(root?.dataset.p2Progress);
      const magazine=Number(root?.dataset.p2MagazineProgress||0);
      const figure=frame?.parentElement;
      return {pose,progress,water:Number(root?.dataset.p2WaterLevel),
        opening:Number(root?.querySelector(".stage")?.style?.getPropertyValue("--p2-door-open")||0),
        phase:root?.dataset.p2ChurchBuildPhase,
        modelVisible:frame?.style.visibility,
        modelLoaded:!!figure?.classList.contains("maquette-geometry-ready"),
        magazine,iframeSrc:frame?.getAttribute("src")||null};
    })()`);
    if(Math.abs(s.pose-vh)<.018)return s;
  }
  throw Error("Original P2 scroll position did not settle near "+vh);
}
try{
  await send("Page.enable");
  await send("Runtime.enable");
  await send("Page.bringToFront");
  await send("Emulation.setEmulatedMedia",
    {features:[{name:"prefers-reduced-motion",value:"no-preference"}]});
  await send("Emulation.setDeviceMetricsOverride",
    {width:1366,height:850,deviceScaleFactor:1,mobile:false});
  await send("Page.navigate",
    {url:"http://127.0.0.1:8765/p2/living-water.html?churchPreview=1"});
  await sleep(1200);
  const opened=await at(2.37);
  if(opened.opening<.995||opened.progress>.005||
     opened.modelVisible!=="hidden"||opened.magazine>.001)
    throw Error("Red Sea must finish BEFORE any visible white construction "+JSON.stringify(opened));
  console.log("P2_SEA_OPEN_FIRST="+JSON.stringify(opened));
  await capture("01-red-sea-fully-open-no-model");
  const beginning=await at(2.42);
  if(beginning.progress>.015||beginning.modelVisible!=="visible"||
     beginning.opening<.995)
    throw Error("White GLB growth must start near zero after opening "+JSON.stringify(beginning));
  await capture("02-original-maquette-begins");
  const midpoint=await at(2.815);
  if(midpoint.progress<.40||midpoint.progress>.60||
     midpoint.phase!=="building"||midpoint.modelVisible!=="visible"||
     midpoint.opening<.995||midpoint.magazine>.001)
    throw Error("Model construction must be independently visible between water and Magazine "+JSON.stringify(midpoint));
  console.log("P2_WHITE_MODEL_MID_GROWTH="+JSON.stringify(midpoint));
  await sleep(600);
  await capture("03-original-maquette-half-grown");
  const finished=await at(3.22);
  if(finished.progress<.999||finished.phase!=="complete"||
     finished.magazine>.001||finished.modelVisible!=="visible")
    throw Error("Original model must complete and hold before magazine takes over "+JSON.stringify(finished));
  const links=await evaluate(`({
    identity:document.querySelector(".church-folio__identity-link")?.getAttribute("href"),
    english:document.querySelector(".church-folio__english-link")?.getAttribute("href"),
    model:document.querySelector(".church-folio__model-entry")?.getAttribute("href"),
    compact:document.querySelector(".index a")?.getAttribute("href"),
    modelFrame:document.querySelector(".church-editorial__maquette")?.getAttribute("src")
  })`);
  for(const key of ["identity","english","model","compact"])
    if(links[key]!=="/p2/church-tour.html?entry=p2")
      throw Error("P2 "+key+" entry does not go to full native second-layer church "+JSON.stringify(links));
  // Let the unchanged source GLB render its final assembly before saving.
  for(let n=0;n<65;n++){
    const ready=await evaluate('document.querySelector(".church-editorial__maquette")?.parentElement?.classList.contains("maquette-geometry-ready")');
    if(ready)break;
    await sleep(450);
  }
  await capture("04-original-maquette-complete");
  const back=await at(2.815),closed=await at(2.37);
  if(back.progress<.40||back.progress>.60||closed.progress>.005||
     closed.modelVisible!=="hidden")
    throw Error("Reverse scroll must reverse white construction and return to only water "+JSON.stringify({back,closed}));
  if(errors.length)throw Error("Actual browser script exceptions "+errors.slice(-3).join("; "));
  console.log("P2_SEA_THEN_REAL_WHITE_MODEL_PASS="+JSON.stringify({
    opened,middle:midpoint,finished,returnToOpenSea:closed,links,
    fixedMagazineHandoff:3.36
  }));
}finally{ws.close()}
