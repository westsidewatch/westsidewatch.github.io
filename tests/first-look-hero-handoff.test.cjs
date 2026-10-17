const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const source=fs.readFileSync('static/js/first-look-host.js','utf8');
const start=source.indexOf(' const update=()=>{',source.indexOf('/* First-layer floating navigation'));
const update=source.slice(start,source.indexOf(" window.addEventListener('scroll'",start));
function render(bottom,open=false){
 const plane={style:{},getBoundingClientRect:()=>({bottom:900})};
 const scripture={style:{},getBoundingClientRect:()=>({bottom:800})};
 const state={outside:false};
 const nav={dataset:{}};
 vm.runInNewContext(update+'update();',{window:{scrollY:900-bottom,innerHeight:900},menu:{open},nav,plane,scripture,previousY:0,scheduled:false,document:{querySelector:()=>({getBoundingClientRect:()=>({top:bottom-900,bottom})}),body:{classList:{toggle(name,value){state.outside=value}}}}});
 return {plane,scripture,state};
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
