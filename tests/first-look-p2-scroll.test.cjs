const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const html=fs.readFileSync('static/p2/living-water.html','utf8');
const scripts=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]);
function runtime(embedded){
 const events={},queue=[],parent={},nodes=new Map();
 const node=()=>({style:{setProperty(){}},dataset:{},classList:{toggle(){},remove(){}},setAttribute(){},querySelector(){return node()}});
 const root=node();root.getBoundingClientRect=()=>({top:0});
 root.querySelector=s=>{if(!nodes.has(s))nodes.set(s,node());return nodes.get(s)};
 root.querySelectorAll=()=>[];
 const document={documentElement:{dataset:embedded?{p2Embedded:'true'}:{}},visibilityState:'hidden',querySelector:()=>root};
 vm.runInNewContext(scripts[1],{document,window:{parent},location:{origin:'https://example.test'},innerHeight:800,performance:{now:()=>0},addEventListener:(name,fn)=>events[name]=fn,requestAnimationFrame:fn=>{queue.push(fn);return queue.length},cancelAnimationFrame(){}});
 return {root,parent,send(source,origin,progress){events.message({source,origin,data:{type:'westside-p2-scroll',progress}});while(queue.length)queue.shift()()}};
}
test('Embedded P2 follows only the hosting parent progress and reverses',()=>{
 const r=runtime(true);
 r.send({},'https://example.test',1);assert.equal(r.root.dataset.p2Phase,'identity');
 r.send(r.parent,'https://foreign.test',1);assert.equal(r.root.dataset.p2Phase,'identity');
 r.send(r.parent,'https://example.test',.35);assert.equal(r.root.dataset.p2Phase,'ocean-rise');
 r.send(r.parent,'https://example.test',.55);assert.equal(r.root.dataset.p2Phase,'red-sea');
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
