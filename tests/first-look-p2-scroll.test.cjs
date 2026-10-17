const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const html=fs.readFileSync('static/p2/living-water.html','utf8');
const scripts=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]);
function runtime(embedded,visible=false){
 let now=0;
 const events={},queue=[],parent={},nodes=new Map();
 const node=()=>({style:{setProperty(){}},dataset:{},classList:{toggle(){},remove(){}},setAttribute(){},getAttribute(){return null},querySelector(){return null}});
 const root=node();root.getBoundingClientRect=()=>({top:0});
 root.querySelector=s=>{if(!nodes.has(s)){const n=node();if(s==='.index')n.querySelector=()=>({textContent:''});nodes.set(s,n)}return nodes.get(s)};
 root.querySelectorAll=()=>[];
 const document={documentElement:{dataset:embedded?{p2Embedded:'true'}:{}},visibilityState:visible?'visible':'hidden',querySelector:()=>root};
 vm.runInNewContext(scripts[1],{document,window:{parent},location:{origin:'https://example.test'},innerHeight:800,performance:{now:()=>now},addEventListener:(name,fn)=>events[name]=fn,requestAnimationFrame:fn=>{queue.push(fn);return queue.length},cancelAnimationFrame(){}});
 return {root,parent,step(ms){now+=ms;const batch=queue.splice(0);for(const callback of batch)callback(now)},send(source,origin,progress){events.message({source,origin,data:{type:'westside-p2-scroll',progress}});if(!visible)while(queue.length)queue.shift()()}};
}
test('Embedded P2 follows only the hosting parent progress and reverses',()=>{
 const r=runtime(true);
 r.send({},'https://example.test',1);assert.equal(r.root.dataset.p2Phase,'identity');
 r.send(r.parent,'https://foreign.test',1);assert.equal(r.root.dataset.p2Phase,'identity');
 r.send(r.parent,'https://example.test',.35);assert.equal(r.root.dataset.p2Phase,'ocean-rise');
 r.send(r.parent,'https://example.test',.7);assert.equal(r.root.dataset.p2Phase,'red-sea');
 r.send(r.parent,'https://example.test',1);assert.equal(r.root.dataset.p2Phase,'church');
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
 assert.match(html,/html\[data-p2-embedded="true"\] \.showcase\{height:100svh\}/);
 assert.match(html,/html\[data-p2-embedded="true"\] body\{height:100%;overflow:clip\}/);
});

test('Discrete wheel jumps converge smoothly at both 60Hz and 120Hz',()=>{
 for(const step of [1000/60,1000/120]){
  const r=runtime(true,true);r.send(r.parent,'https://example.test',1);
  r.step(step);const first=Number(r.root.dataset.p2Progress);
  assert.ok(first>0&&first<1,'first frame must not jump to the scroll target');
  let previous=first;
  for(let time=step;time<600;time+=step){r.step(step);const next=Number(r.root.dataset.p2Progress);assert.ok(next>=previous);previous=next;}
  assert.ok(previous>2.89,'wheel smoothing must not add a long lag');
  r.send(r.parent,'https://example.test',0);r.step(step);
  assert.ok(Number(r.root.dataset.p2Progress)<previous,'reversal starts on the next frame');
 }
});
test('Water travels from the bottom through mid-screen to the top before doors open',()=>{
 const r=runtime(true);
 for(const [vh,level] of [[.65,0],[1.125,.5],[1.6,1]]){
  r.send(r.parent,'https://example.test',vh/2.9);
  assert.ok(Math.abs(Number(r.root.dataset.p2WaterLevel)-level)<.001);
  assert.equal(r.root.dataset.p2Phase,'ocean-rise');
 }
 r.send(r.parent,'https://example.test',1.8/2.9);assert.equal(r.root.dataset.p2Phase,'red-sea');
});
