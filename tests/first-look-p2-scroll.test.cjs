const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const html=fs.readFileSync('static/p2/living-water.html','utf8');
const scripts=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]);
scripts[1]=fs.readFileSync('static/js/p2-living-water.js','utf8');
const css=fs.readFileSync('static/css/p2-living-water.css','utf8');
function runtime(embedded,visible=false){
 let now=0,waterPaints=0;
 const events={},queue=[],parent={},nodes=new Map();
 const node=()=>({style:{setProperty(){}},dataset:{},classList:{toggle(){},remove(){}},setAttribute(){},getAttribute(){return null},querySelector(){return null}});
 const planes=Array.from({length:7},()=>{const n=node();n.style.setProperty=(name,value)=>n.style[name]=value;return n});
 const root=node();root.getBoundingClientRect=()=>({top:0});
 root.querySelector=s=>{if(!nodes.has(s)){const n=node();if(s==='.index')n.querySelector=()=>({textContent:''});nodes.set(s,n)}return nodes.get(s)};
 root.querySelectorAll=selector=>selector==='.plane'?planes:[];
 const document={documentElement:{dataset:embedded?{p2Embedded:'true'}:{}},visibilityState:visible?'visible':'hidden',querySelector:()=>root};
 vm.runInNewContext(scripts[1],{document,window:{parent,wsP2Water:{paint(){waterPaints++}}},location:{origin:'https://example.test',search:''},URLSearchParams,innerHeight:800,performance:{now:()=>now},addEventListener:(name,fn)=>events[name]=fn,requestAnimationFrame:fn=>{queue.push(fn);return queue.length},cancelAnimationFrame(){}});
 return {root,parent,nodes,planes,get waterPaints(){return waterPaints},step(ms){now+=ms;const batch=queue.splice(0);for(const callback of batch)callback(now)},send(source,origin,progress,active=true){events.message({source,origin,data:{type:'westside-p2-scroll',progress,active}});if(!visible)while(queue.length)queue.shift()()}};
}
// Parent First Look devotes 75% of its scroll track to the first 2.9 P2 viewports.
// Keep assertions in physical P2 viewport units, independent of the parent fraction.
const progressAt=vh=>vh<=2.9?(vh/2.9)*.75:.75+(vh-2.9)/1.1*.25;
test('Embedded P2 follows only the hosting parent progress and reverses',()=>{
 const r=runtime(true);
 r.send({},'https://example.test',1);assert.equal(r.root.dataset.p2Phase,'identity');
 r.send(r.parent,'https://foreign.test',1);assert.equal(r.root.dataset.p2Phase,'identity');
 r.send(r.parent,'https://example.test',progressAt(1.2));assert.equal(r.root.dataset.p2Phase,'ocean-rise');
 r.send(r.parent,'https://example.test',progressAt(2.1));assert.equal(r.root.dataset.p2Phase,'red-sea');
 r.send(r.parent,'https://example.test',progressAt(2.5));assert.equal(r.root.dataset.p2Phase,'church');
 r.send(r.parent,'https://example.test',1);assert.equal(r.root.dataset.p2Phase,'magazine');
 r.send(r.parent,'https://example.test',0);assert.equal(r.root.dataset.p2Phase,'identity');
});
test('Standalone P2 ignores external progress',()=>{
 const r=runtime(false);r.send(r.parent,'https://example.test',1);assert.equal(r.root.dataset.p2Phase,'identity');
});
test('Only explicit iframe embedding disables the second scroll surface',()=>{
 for(const framed of [false,true])for(const search of ['', '?embed=1']){
  const window={};window.parent=framed?{}:window;
  const document={documentElement:{dataset:{}}};
  vm.runInNewContext(scripts[0],{window,document,location:{search},URLSearchParams});
  assert.equal(document.documentElement.dataset.p2Embedded==='true',framed&&search==='?embed=1');
 }
 assert.match(css,/html\[data-p2-embedded="true"\] \.showcase\{height:100svh\}/);
 assert.match(css,/html\[data-p2-embedded="true"\] body\{height:100%;overflow:clip\}/);
});

test('Scroll progress lands on the input position in one frame and stays there',()=>{
 for(const step of [1000/60,1000/120]){
  const r=runtime(true,true);
  for(const progress of [.05,.09,.15,.1,.02]){
   r.send(r.parent,'https://example.test',progress);
   assert.ok(Math.abs(Number(r.root.dataset.p2Progress)-progress*2.9/.75)<.0001,'input must apply without an extra child-frame wait');r.step(step);
   assert.ok(Math.abs(Number(r.root.dataset.p2Progress)-progress*2.9/.75)<.0001);
   const held=r.planes.map(p=>p.style.transform);
   for(let i=0;i<20;i++)r.step(step);
   assert.deepEqual(r.planes.map(p=>p.style.transform),held,'stopping input must stop every curtain');
  }
 }
});
test('Curtains retain navigation-like overlap and reverse to the same geometry',()=>{
 const r=runtime(true,true);
 const transforms=[];
 for(const reveal of [.1,.2,.3,.2,.1]){
  r.send(r.parent,'https://example.test',progressAt(reveal*.5));r.step(17);
  transforms.push(r.planes[0].style.transform);
 }
 assert.equal(transforms[0],transforms[4]);assert.equal(transforms[1],transforms[3]);
 const scalesAt=reveal=>{
  r.send(r.parent,'https://example.test',progressAt(reveal*.5));
  return r.planes.map(p=>Number(p.style.transform.match(/scale3d\(1,([^,]+)/)[1]));
 };
 const layers=scalesAt(.5);
 assert.equal(layers.length,7);
 for(let i=1;i<7;i++)assert.ok(layers[i-1]>layers[i], 'each later curtain must expose the preceding colour');
 assert.ok(layers[0]-layers[6]>.8,'overlap must span most of the upper half rather than a flat band');
 assert.ok(layers[0]-layers[1]!==layers[3]-layers[4],'fold edges need the navigation’s shaped progression');
 assert.deepEqual(scalesAt(1),Array(7).fill(1));
 assert.deepEqual(scalesAt(0),Array(7).fill(0));
});
test('Water travels from the bottom through mid-screen to the top before doors open',()=>{
 const r=runtime(true);
 for(const [vh,level] of [[.65,0],[1.125,.5],[1.6,1]]){
  r.send(r.parent,'https://example.test',progressAt(vh));
  assert.ok(Math.abs(Number(r.root.dataset.p2WaterLevel)-level)<.001);
  assert.equal(r.root.dataset.p2Phase,'ocean-rise');
 }
 r.send(r.parent,'https://example.test',progressAt(1.8));assert.equal(r.root.dataset.p2Phase,'red-sea');
});

test('Paper cover never masks the dynamic lower half at entry',()=>{
 const r=runtime(true);r.send(r.parent,'https://example.test',progressAt(.5));
 assert.match(r.nodes.get('.water-cover').style.clipPath,/50\.00%/);
 assert.doesNotMatch(r.nodes.get('.water-cover').style.clipPath,/% 100\.00%/);
});
test('The single animation clock stops offscreen and resumes on return',()=>{
 const r=runtime(true,true);r.send(r.parent,'https://example.test',.3);r.step(17);
 assert.equal(r.root.dataset.p2Animating,'true');
 r.send(r.parent,'https://example.test',.3,false);r.step(17);
 assert.equal(r.root.dataset.p2Animating,'false');
 const stopped=r.root.dataset.p2Progress,paints=r.waterPaints;r.step(500);assert.equal(r.root.dataset.p2Progress,stopped);assert.equal(r.waterPaints,paints);
 r.send(r.parent,'https://example.test',.3,true);r.step(17);assert.equal(r.root.dataset.p2Animating,'true');
});

test('Water door references the live source rather than a second renderer',()=>{
 assert.doesNotMatch(html,/<iframe/);
 assert.match(html,/<use href="#upper-lines"/);
 assert.match(html,/<use href="#p2-water-lower-lines"/);
 const water=fs.readFileSync('static/js/p2-water-surface.js','utf8');
 assert.doesNotMatch(water,/requestAnimationFrame/);
 assert.match(water,/window\.wsP2Water=\{paint:frame\}/);
});
test('Generic entrance motion does not target the dedicated P2 scroll host',()=>{
 const sections=fs.readFileSync('static/css/sites-home-sections.css','utf8');
 const composition=fs.readFileSync('static/css/westside-home-hero-composition.css','utf8');
 assert.match(sections,/\.candidate-focus-screen:not\(\.ws-p2-sevenfold-host\)\{view-timeline-name/);
 assert.doesNotMatch(composition,/\.candidate-focus-screen::before/);
});

test('Forward and reverse door handoff always cover the right half',()=>{
 const r=runtime(true);
 for(const vh of [1.70,1.7199,1.7201,1.73,2.4,1.73,1.7201,1.7199,1.70]){
  r.send(r.parent,'https://example.test',progressAt(vh));
  const sea=r.nodes.get('.ocean-rise'),doors=r.nodes.get('.water-doors');
  if(sea.style.clipPath==='inset(0 50% 0 0)'){
   assert.equal(doors.style.visibility,'visible','clipping the ocean requires an opaque shared door');
   assert.equal(r.nodes.get('.church-editorial').style.visibility,'visible');
  }else assert.equal(sea.style.clipPath,'none','full surface must cover both halves outside the door phase');
 }
});

test('Completed curtains remain until the rising water covers them, without a blank fade gap',()=>{
 const r=runtime(true);
 for(const vh of [.5,.95,1.125]){
  r.send(r.parent,'https://example.test',progressAt(vh));
  const wrap=r.nodes.get('.planes');
  assert.equal(wrap.style.visibility,'visible');assert.equal(wrap.style.opacity,'1');
  assert.match(wrap.style.clipPath,/polygon/);
 }
 r.send(r.parent,'https://example.test',progressAt(1.6));
 assert.equal(r.nodes.get('.planes').style.visibility,'hidden');
});
