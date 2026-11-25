(()=>{if(!document.documentElement.classList.contains('art110'))return;
const M=Object.freeze({"id":"church","en":"Living Water","zh":"活水堂","depths":[1,2,1,3,1,2],"width":48,"height":8,"source":"historical","path":"M0 8V1H8V2H16V1H24V3H32V1H40V2H48V8Z"});
const $=s=>document.querySelector(s);
const round=n=>Math.round(n*1000)/1000;
const px=n=>round(n)+'px';
const pairs=(start,end,origin,unit)=>{
  const at=x=>M.depths[Math.max(0,Math.min(5,Math.floor((x-origin)/unit/8)))];
  const points=[[start,at(start+1e-5)]];
  for(let k=1;k<6;k++){const x=origin+k*8*unit;if(x>start+1e-5&&x<end-1e-5){points.push([x,M.depths[k-1]],[x,M.depths[k]])}}
  points.push([end,at(end-1e-5)]);
  return points;
};
const prayer=$('#prayer'),head=$('#prayer .church-visit__section-head'),glass=$('#prayer .church-visit__about-grid');
const response=$('.church-visit__intake-grid');
function update(){
 const pr=prayer.getBoundingClientRect(),hr=head.getBoundingClientRect(),gr=glass.getBoundingClientRect(),s=getComputedStyle(prayer);
 const left=pr.left+parseFloat(s.paddingLeft),width=pr.width-parseFloat(s.paddingLeft)-parseFloat(s.paddingRight),bay=width/12;
 // Scale the mother beyond the entire page: four columns per tooth on desktop,
 // six on smaller screens. Its deepest turn lies exactly on the centre axis.
 const u=bay*(innerWidth<=900?.75:.5),origin=left+6*bay-24*u;
 const curve=pairs(hr.left,hr.right,origin,u),baseY=4*u;
 head.style.clipPath='polygon(0 0, 100% 0, '+curve.slice().reverse().map(([x,d])=>px(x-hr.left)+' '+px(hr.height-baseY+d*u)).join(', ')+')';
 prayer.dataset.crestCrop=JSON.stringify({mother:M.id,source:'9d7f3e5557738e45749b2121918809efdec4cd9d',orientation:0,scale:round(u),origin:round(origin-left),sourceWindow:[round((hr.left-origin)/u),round((hr.right-origin)/u),0,4],negativeWindow:[round((gr.left-origin)/u),round((hr.right-origin)/u),0,4],axis:round(left+6*bay),vertices:curve.map(([x,d])=>[round(x-left),d])});
 const grid=response.getBoundingClientRect(),items=[...response.querySelectorAll('article')];
 if(innerWidth>900){
  // A second view of the same crest, rotated ninety degrees. Its centre tooth
  // is anchored to the division between the two actual response rows.
  const a=items[0].getBoundingClientRect(),seam=a.bottom;
  const u2=grid.height/32,origin2=seam-24*u2;
  const maxCut=3*u2;response.style.setProperty('--response-safe',px(maxCut+Math.max(16,bay*.18)));
  items.forEach((e,i)=>{if(i%2){e.style.clipPath='none';return}const r=e.getBoundingClientRect();const c=pairs(r.top,r.bottom,origin2,u2);e.style.clipPath='polygon(0 0, '+c.map(([y,d])=>px(r.width-d*u2)+' '+px(y-r.top)).join(', ')+', 0 100%)';e.dataset.crestCrop=JSON.stringify({mother:M.id,orientation:90,scale:round(u2),sourceWindow:[round((r.top-origin2)/u2),round((r.bottom-origin2)/u2)],vertices:c.map(([y,d])=>[round(y-grid.top),d])});});
  response.dataset.crestCrop=JSON.stringify({mother:M.id,orientation:90,scale:round(u2),axis:round(seam-grid.top),sourceWindow:[round((grid.top-origin2)/u2),round((grid.bottom-origin2)/u2)]});
 }else{
  items.forEach(e=>{e.style.removeProperty('clip-path');delete e.dataset.crestCrop});response.style.removeProperty('--response-safe');delete response.dataset.crestCrop;
 }
}
let raf=0;const schedule=()=>{cancelAnimationFrame(raf);raf=requestAnimationFrame(update)};
const ro=new ResizeObserver(schedule);[prayer,head,glass,response,...response.querySelectorAll('article')].forEach(e=>ro.observe(e));window.addEventListener('resize',schedule);document.fonts.ready.then(schedule);update();
})();