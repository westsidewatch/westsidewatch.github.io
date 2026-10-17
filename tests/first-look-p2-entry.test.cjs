const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const html=fs.readFileSync('layouts/partials/watch-home-editorial.html','utf8');
const script=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]).find(s=>s.includes('westside-p2-scroll'));
function progress(top,height=800){
 let message;
 const frame={contentWindow:{postMessage(data){message=data}},addEventListener(){}};
 const host={offsetHeight:height*5.2,getBoundingClientRect:()=>({top}),querySelector:()=>frame};
 vm.runInNewContext(script,{document:{querySelector:()=>host},innerHeight:height,location:{origin:'https://example.test'},addEventListener(){},requestAnimationFrame(fn){fn()}});
 return message.progress*2.9;
}
test('Entry pre-roll cannot consume the seven-layer reveal offscreen',()=>{
 assert.equal(progress(800),0);
 assert.ok(Math.abs(progress(400)-.05)<1e-9);
 assert.ok(Math.abs(progress(0)-.1)<1e-9);
});
test('Sevenfold gets 1.8 pinned viewports before water choreography continues',()=>{
 assert.ok(Math.abs(progress(-720)-.3)<1e-9);
 assert.ok(Math.abs(progress(-1440)-.5)<1e-9);
 assert.ok(Math.abs(progress(-1560)-.65)<1e-9);
 assert.ok(Math.abs(progress(-3360)-2.9)<1e-9);
 assert.equal(progress(-4000),2.9);
 const values=[800,400,0,-360,-720,-1080,-1440,-1600,-2400,-3360].map(top=>progress(top));
 for(let i=1;i<values.length;i++)assert.ok(values[i]>=values[i-1]);
});
test('Scroll distance scales with viewport height rather than input device speed',()=>{
 for(const height of [480,720,1128,1692]){
  assert.equal(progress(height,height),0);
  assert.ok(Math.abs(progress(0,height)-.1)<1e-9);
  assert.ok(Math.abs(progress(-height*.9,height)-.3)<1e-9);
  assert.ok(Math.abs(progress(-height*1.8,height)-.5)<1e-9);
 }
});
