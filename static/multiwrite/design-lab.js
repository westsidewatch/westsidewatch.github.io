const prototype = document.getElementById('prototype');
const colorRole = document.getElementById('colorRole');
const hierarchy = document.getElementById('hierarchy');
const axis = document.getElementById('axis');
const density = document.getElementById('density');
const lineStrength = document.getElementById('lineStrength');
const colorReason = document.getElementById('colorReason');
const cssText = document.getElementById('cssText');
const saveState = document.getElementById('saveState');
const KEY = 'dore-multiwrite-design-lab-v1';

const reasons = {
  paper: '紙承載正文；讓首屏的金保有稀缺性。',
  'first-light': '初光適合顯現、入口與高價值強調；不宜讓整頁都成為同一強度。',
  'watch-night': '守望夜提供戲劇性與高對比，但會把第二頁推成新的主角。',
  olive: '橄欖帶生命與安息語義；適合生長、群體與恢復相關內容。'
};

function state(){return {color:colorRole.value,hierarchy:hierarchy.value,axis:axis.value,density:density.value,lines:lineStrength.value}}
function generatedCSS(s){
  const backgrounds={paper:'#F5EEDB','first-light':'#CEBD74','watch-night':'#26241F',olive:'#7A7B57'};
  const titleSizes={quiet:'1.55rem',equal:'2rem',display:'3.35rem'};
  const align=s.axis==='center'?'center':'left';
  const pad={0:'38px 0 42px',1:'64px 0 72px',2:'92px 0 110px'}[s.density];
  const line={0:'transparent',1:'rgba(74,56,20,.18)',2:'rgba(74,56,20,.38)'}[s.lines];
  return `.product-story { background: ${backgrounds[s.color]}; padding: ${pad}; }\n.product-story .thesis-copy { text-align: ${align}; }\n.product-story .thesis-copy h2 { font-size: ${titleSizes[s.hierarchy]}; }\n.product-story .product-path article { text-align: ${align}; border-color: ${line}; }`;
}
function apply(s, persist=true){
  prototype.dataset.color=s.color;
  prototype.dataset.hierarchy=s.hierarchy;
  prototype.dataset.axis=s.axis;
  prototype.dataset.density=s.density;
  prototype.dataset.lines=s.lines;
  colorRole.value=s.color; hierarchy.value=s.hierarchy; axis.value=s.axis; density.value=s.density; lineStrength.value=s.lines;
  colorReason.textContent=reasons[s.color]; cssText.textContent=generatedCSS(s);
  if(persist){localStorage.setItem(KEY,JSON.stringify(s)); saveState.textContent='已保存試驗'; setTimeout(()=>saveState.textContent='本機試驗',1200)}
}
[colorRole,hierarchy,axis,density,lineStrength].forEach(el=>el.addEventListener('input',()=>apply(state())));
const recommended={color:'paper',hierarchy:'quiet',axis:'center',density:'1',lines:'1'};
document.getElementById('applyDore').addEventListener('click',()=>apply(recommended));
document.getElementById('resetDesign').addEventListener('click',()=>apply(recommended));
document.getElementById('copyState').addEventListener('click',async()=>{
  const payload={schema:'dore.design-decision.v1',surface:'multiwrite.home.product-story',decision:state(),reasoning:{color:reasons[colorRole.value],hierarchy:'首頁第二屏應低於首屏品牌宣言。',axis:axis.value==='center'?'延續 Gate 的中央軸傳統。':'採用編輯式偏置以增加雜誌感。'},generatedCSS:generatedCSS(state())};
  try{await navigator.clipboard.writeText(JSON.stringify(payload,null,2));saveState.textContent='已複製設計決策'}catch{saveState.textContent='瀏覽器未允許複製'}
});
let initial=recommended;try{const saved=JSON.parse(localStorage.getItem(KEY));if(saved)initial={...recommended,...saved}}catch{}
apply(initial,false);
