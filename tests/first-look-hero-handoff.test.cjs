const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const source=fs.readFileSync('static/js/first-look-host.js','utf8');
const start=source.indexOf(' const update=()=>{',source.indexOf('/* First-layer floating navigation'));
const update=source.slice(start,source.indexOf(" window.addEventListener('scroll'",start));
function render(bottom,open=false,withFilm=false,hidden=false){
 const messages=[],frame=withFilm?{dataset:{},contentWindow:{postMessage(message){messages.push(message)}}}:undefined;
 const plane={style:{},getBoundingClientRect:()=>({bottom:900})};
 const scripture={style:{},getBoundingClientRect:()=>({bottom:800})};
 const state={outside:false};
 const nav={dataset:{}};
 vm.runInNewContext(update+'update();',{window:{scrollY:900-bottom,innerHeight:900},menu:{open},nav,plane,scripture,previousY:0,scheduled:false,location:{origin:'https://example.test'},document:{visibilityState:hidden?'hidden':'visible',querySelector:()=>({getBoundingClientRect:()=>({top:bottom-900,bottom}),querySelector:()=>frame}),body:{classList:{toggle(name,value){state.outside=value}}}}});
 return {plane,scripture,state,messages};
}
test('Hero artwork is clipped at the moving boundary before the hero leaves',()=>{
 const r=render(200);assert.equal(r.plane.style.clipPath,'inset(0 0 700px 0)');assert.equal(r.scripture.style.clipPath,'inset(0 0 600px 0)');assert.equal(r.state.outside,false);
});
test('Reversing to the hero restores artwork without clipping',()=>{
 const r=render(900);assert.equal(r.plane.style.clipPath,'none');assert.equal(r.scripture.style.clipPath,'none');
});
test('Contents curtain remains usable when opened beyond the hero',()=>{
 const r=render(-100,true);assert.equal(r.plane.style.clipPath,'none');assert.equal(r.scripture.style.clipPath,'none');assert.equal(r.state.outside,false);
});

test('Cover decoding pauses away from the hero and prewarms before reverse entry',()=>{
 assert.equal(render(-500,false,true).messages[0].paused,true);
 assert.equal(render(-200,false,true).messages[0].paused,false);
 assert.equal(render(900,false,true,true).messages[0].paused,true);
});
