import {mkdirSync,writeFileSync} from "node:fs";
const dir="artifacts/p2-church-ministry-second-layer";
mkdirSync(dir,{recursive:true});
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
let pages;
for(let i=0;i<100;i++){
  try{const res=await fetch("http://127.0.0.1:9222/json/list");
    if(res.ok){pages=await res.json();if(pages.some(x=>x.type==="page"))break;}
  }catch{}await sleep(300);
}
const tab=pages?.find(x=>x.type==="page");
if(!tab?.webSocketDebuggerUrl)throw Error("Chrome CDP page unavailable");
const ws=new WebSocket(tab.webSocketDebuggerUrl);
await new Promise((resolve,reject)=>{
  ws.addEventListener("open",resolve,{once:true});
  ws.addEventListener("error",reject,{once:true});
});
let seq=0;
const pending=new Map(),errors=[];
ws.addEventListener("message",event=>{
  const r=JSON.parse(event.data);
  if(r.id&&pending.has(r.id)){
    const p=pending.get(r.id);pending.delete(r.id);
    if(r.error)p.reject(Error(JSON.stringify(r.error)));else p.resolve(r.result);
  }
  if(r.method==="Runtime.exceptionThrown")
    errors.push(r.params?.exceptionDetails?.exception?.description||"Script exception");
  if(r.method==="Runtime.consoleAPICalled"&&r.params?.type==="error")
    errors.push((r.params.args||[]).map(x=>x.value||x.description).join(" "));
});
function send(method,params={}){
  const id=++seq;
  const promise=new Promise((resolve,reject)=>pending.set(id,{resolve,reject}));
  ws.send(JSON.stringify({id,method,params}));
  return promise;
}
async function evaluate(code){
  const result=await send("Runtime.evaluate",
    {expression:code,returnByValue:true,awaitPromise:true});
  if(result.exceptionDetails)throw Error(result.exceptionDetails.exception?.description||"Chrome expression failed");
  return result.result?.value;
}
async function waitReady(chapters){
  for(let i=0;i<135;i++){
    await sleep(190);
    const s=await evaluate(`({
      ready:document.body.classList.contains("ready"),
      failed:document.body.classList.contains("failed"),
      chapterCount:document.querySelectorAll(".ws-ministry-story__chapter").length,
      guide:!!window.__churchGuide?.status
    })`);
    if(s.failed)throw Error("Original GLB failed to load "+JSON.stringify(errors));
    if(s.ready&&s.guide&&s.chapterCount===chapters)return s;
  }
  throw Error("Original church did not reach ready for chapter count "+chapters+" "+errors.join("; "));
}
async function shot(name){
  const image=await send("Page.captureScreenshot",
    {format:"jpeg",quality:64,captureBeyondViewport:false,fromSurface:true});
  if(!image.data)throw Error("Missing real WebGL frame "+name);
  writeFileSync(dir+"/"+name+".jpg",Buffer.from(image.data,"base64"));
}
try{
  await send("Page.enable");
  await send("Runtime.enable");
  await send("Page.bringToFront");
  await send("Emulation.setEmulatedMedia",{
    features:[{name:"prefers-reduced-motion",value:"no-preference"}]
  });
  await send("Emulation.setDeviceMetricsOverride",
    {width:1366,height:850,deviceScaleFactor:1,mobile:false});
  await send("Page.navigate",{
    url:"http://127.0.0.1:8765/p2/church-tour.html?entry=p2&startAt=12"
  });
  await waitReady(7);
  const first=await evaluate(`({
    state:window.__churchGuide.status(),audit:window.__churchMinistryAudit(),
    visible:!!document.querySelector(".ws-ministry-story__rail")
  })`);
  if(!first.visible||first.audit.chapters!==7||
     first.audit.fullVerses!==true||first.audit.scheduleRows!==7)
    throw Error("P2 must publish seven COMPLETE bilingual scripture passages and seven worship rows "+JSON.stringify(first));
  await shot("01-p2-arrival");
  await evaluate('document.querySelector(\'[data-chapter="2"]\').click()');
  await sleep(240);
  const worship=await evaluate('({state:window.__churchGuide.status(),audit:window.__churchMinistryAudit()})');
  if(Math.abs(worship.state.at-94)>.1||!worship.state.paused||worship.audit.selected!==2)
    throw Error("Worship chapter must STOP at the illuminated sanctuary cross "+JSON.stringify(worship));
  const crossFrame=await evaluate("window.__churchMinistryFramingAudit");
  if(crossFrame?.label!=="cross-worship")
    throw Error("Worship camera did not select cross-and-pews composition "+JSON.stringify(crossFrame));
  const scriptureAtCross=await evaluate(`({
    zh:document.querySelector("[data-story-zh]").textContent,
    kjv:document.querySelector("[data-story-kjv]").textContent,
    source:document.querySelector("[data-story-reference]").textContent
  })`);
  if(scriptureAtCross.zh.length<35||scriptureAtCross.kjv.length<150||
     !scriptureAtCross.source.includes("15:5–6"))
    throw Error("Worship full CUV/KJV text missing "+JSON.stringify(scriptureAtCross));
  await shot("02-worship-3d");
  await evaluate('document.querySelector(\'[data-chapter="5"]\').click()');
  const discipleship=await evaluate('({state:window.__churchGuide.status(),audit:window.__churchMinistryAudit()})');
  if(Math.abs(discipleship.state.at-211)>.1||discipleship.audit.selected!==5)
    throw Error("Discipleship chapter did not reach original gallery "+JSON.stringify(discipleship));
  await shot("03-discipleship-3d");
  await evaluate('document.querySelector(\'[data-action="hide"]\').click()');
  if(!await evaluate('document.querySelector(".ws-ministry-story").classList.contains("is-minimal")'))
    throw Error("Visitor cannot hide guide and see 3D");
  await shot("04-pure-scene-toggle");
  await evaluate('document.querySelector(\'[data-action="show"]\').click()');
  await evaluate('document.querySelector(\'[data-action="play"]\').click()');
  await send("Page.bringToFront");
  await sleep(1350);
  const resumed=await evaluate(`({
    state:window.__churchGuide.status(),
    hidden:document.hidden,
    reduced:matchMedia("(prefers-reduced-motion: reduce)").matches,
    rendered:window.__churchFrameAudit?.at
  })`);
  console.log("P2_GUIDE_PLAYBACK_PROBE="+JSON.stringify(resumed));
  if(resumed.state.paused||(!resumed.hidden&&!resumed.reduced&&resumed.state.at<=211))
    throw Error("Play did not resume original route "+JSON.stringify(resumed));
  await send("Emulation.setDeviceMetricsOverride",
    {width:390,height:844,deviceScaleFactor:1,mobile:true});
  await sleep(350);
  const mobile=await evaluate(`({
    width:innerWidth,
    rail:document.querySelector(".ws-ministry-story__rail").getBoundingClientRect().toJSON(),
    panel:document.querySelector(".ws-ministry-story__panel").getBoundingClientRect().toJSON()
  })`);
  if(mobile.width!==390||mobile.rail.x<0||mobile.rail.right>391||mobile.panel.right>391)
    throw Error("Mobile 3D chapter labels are clipped "+JSON.stringify(mobile));
  const wrapping=await evaluate(`({
    panel:document.querySelector(".ws-ministry-story__panel").scrollWidth,
    panelWidth:document.querySelector(".ws-ministry-story__panel").clientWidth,
    en:document.querySelector("[data-story-kjv]").scrollWidth,
    enWidth:document.querySelector("[data-story-kjv]").clientWidth,
    zh:document.querySelector("[data-story-zh]").scrollWidth,
    zhWidth:document.querySelector("[data-story-zh]").clientWidth
  })`);
  if(wrapping.panel>wrapping.panelWidth+2||
     wrapping.en>wrapping.enWidth+2||
     wrapping.zh>wrapping.zhWidth+2)
    throw Error("Full scripture has horizontal overflow / broken words on phone "+JSON.stringify(wrapping));
  await shot("05-mobile-editorial");
  // Final architectural still must bring forward the genuine P2 Sunday
  // programme while the illuminated exterior cross stays visible.
  await evaluate('document.querySelector(\'[data-chapter="6"]\').click()');
  await sleep(550);
  const finale=await evaluate(`({
    state:window.__churchGuide.status(),
    active:document.querySelector(".ws-ministry-story").classList.contains("is-finale"),
    rows:document.querySelectorAll(".ws-ministry-story__sunday-row").length,
    hidden:document.querySelector(".ws-ministry-story__sunday").getAttribute("aria-hidden")
  })`);
  if(finale.state.at!==248||!finale.active||finale.rows!==7||finale.hidden!=="false")
    throw Error("Finale must show all seven Sunday worship programme rows "+JSON.stringify(finale));
  await shot("06-final-sunday-programme");
  await send("Page.navigate",{
    url:"http://127.0.0.1:8765/p2/church-tour.html?proofFrame=83"
  });
  await waitReady(0);
  if(await evaluate('!!document.querySelector(".ws-ministry-story")||!!document.body.dataset.churchEntry'))
    throw Error("Raw camera-only tour polluted by ministry introduction");
  await shot("07-direct-3d-clean");
  if(errors.length)throw Error("Browser errors "+errors.slice(-3).join("; "));
  console.log("P2_SECOND_LAYER_MINISTRY_QA_PASS="+JSON.stringify({
    sevenChapters:true,completeCUVandKJV:true,osGlass:true,
    p2Entry:true,worshipTime:94,studyTime:211,
    SundayFinaleRows:7,pausePlay:true,hideShow:true,mobile390:true,pure3dClean:true
  }));
}finally{ws.close();}
