const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const html=fs.readFileSync('layouts/partials/watch-home-editorial.html','utf8');
const script=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]).find(s=>s.includes('westside-p2-scroll'));
function progress(top,height=800){
 let message;
 const frame={contentWindow:{postMessage(data){message=data}},addEventListener(){}};
 const host={offsetHeight:height*3.9,getBoundingClientRect:()=>({top}),querySelector:()=>frame};
 vm.runInNewContext(script,{document:{querySelector:()=>host},innerHeight:height,location:{origin:'https://example.test'},addEventListener(){},requestAnimationFrame(fn){fn()}});
 return message.progress*2.9;
}
test('Sevenfold runs during entry, finishing before the upper half is fully visible',()=>{
 assert.equal(progress(800),0);
 assert.equal(progress(600),.25);
 assert.equal(progress(400),.5);
 assert.equal(progress(200),.5);
 assert.equal(progress(0),.5);
});
test('Pinned rise and opening progress stay continuous through the existing host',()=>{
 const points=[800,600,400,200,0,-200,-800,-1600,-2320,-3000];
 const values=points.map(top=>progress(top));
 for(let i=1;i<values.length;i++)assert.ok(values[i]>=values[i-1]);
 assert.ok(Math.abs(progress(-2320)-2.9)<1e-9);
 assert.equal(progress(-3000),2.9);
 assert.ok(progress(-200)>.5);
});
test('Entry geometry scales with the viewport, including compact screens',()=>{
 for(const height of [480,720,1128,1692]){
  assert.equal(progress(height,height),0);
  assert.equal(progress(height*.75,height),.25);
  assert.equal(progress(height*.5,height),.5);
 }
});
