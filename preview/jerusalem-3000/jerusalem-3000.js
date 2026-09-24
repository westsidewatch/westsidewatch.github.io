const eras=[
  {en:'TODAY',zh:'今天',note:'固定地形與鏡頭。之後改變的是城市的時間狀態，不是觀看座標.',density:1,profile:1},
  {en:'HERODIAN · c. 30 CE',zh:'大希律—耶穌',note:'同一座山城進入第二聖殿晚期閱讀座標；歷史幾何尚未聲稱完成。',density:.82,profile:.9},
  {en:'PERSIAN · 5TH C. BCE',zh:'尼希米',note:'城市量體收縮，城牆與聚落狀態回到波斯時期的閱讀層。',density:.48,profile:.68},
  {en:'IRON AGE · 10TH C. BCE',zh:'大衛—所羅門',note:'原型只保留「同地形、同鏡頭、較小城市核心」；實際復原需逐物件掛接證據。',density:.28,profile:.52}
];
const city=document.querySelector('.j3k-city');
const slider=document.querySelector('.j3k-scrubber');
const markerButtons=[...document.querySelectorAll('.j3k-markers button')];
const eraEn=document.querySelector('.j3k-era-en');
const eraZh=document.querySelector('.j3k-caption h2');
const eraNote=document.querySelector('.j3k-era-note');
const evidenceToggle=document.querySelector('.j3k-evidence-toggle');
const evidencePanel=document.querySelector('.j3k-evidence-panel');

const blocks=[
  [4,48,16,25,'observed'],[20,45,12,28,'observed'],[34,50,18,23,'reconstructed'],[54,42,12,31,'reconstructed'],
  [69,47,14,26,'inferred'],[82,52,10,20,'inferred'],[10,30,13,17,'observed'],[27,27,16,19,'reconstructed'],
  [48,29,19,18,'disputed'],[73,29,12,18,'inferred'],[6,65,21,12,'observed'],[30,66,16,10,'reconstructed'],
  [51,64,18,13,'inferred'],[72,67,20,10,'disputed'],[15,15,12,12,'reconstructed'],[39,13,16,13,'inferred'],
  [64,14,13,12,'disputed']
];
blocks.forEach((b,i)=>{
  const el=document.createElement('div');
  el.className='j3k-block';
  el.dataset.status=b[4];
  el.style.left=b[0]+'%';el.style.top=b[1]+'%';el.style.width=b[2]+'%';el.style.height=b[3]+'%';
  el.style.setProperty('--seed',i);
  city.append(el);
});
const blockEls=[...city.children];

function interpolate(a,b,t){return a+(b-a)*t}
function update(value){
  const lo=Math.floor(value), hi=Math.min(3,Math.ceil(value)), t=value-lo;
  const a=eras[lo],b=eras[hi];
  const density=interpolate(a.density,b.density,t);
  const profile=interpolate(a.profile,b.profile,t);
  city.style.transform=`scaleY(${.74+.26*profile}) translateY(${(1-profile)*8}%)`;
  blockEls.forEach((el,i)=>{
    const threshold=(i+1)/blockEls.length;
    const visible=Math.max(0,Math.min(1,(density-threshold+.18)/.18));
    el.style.opacity=visible;
    el.style.transform=`scaleY(${.15+.85*visible}) translateY(${(1-visible)*18}px)`;
    const status=el.dataset.status;
    el.style.outline=status==='disputed'&&visible>.3?'1px dashed rgba(85,48,42,.65)':'none';
  });
  const nearest=Math.round(value);
  markerButtons.forEach((x,i)=>x.classList.toggle('is-active',i===nearest));
  const display=t<.5?a:b;
  eraEn.textContent=display.en;eraZh.textContent=display.zh;eraNote.textContent=display.note;
  const url=new URL(location.href);url.searchParams.set('era',nearest);history.replaceState(null,'',url);
}
slider.addEventListener('input',()=>update(Number(slider.value)));
markerButtons.forEach((btn,i)=>btn.addEventListener('click',()=>{slider.value=i;update(i)}));
evidenceToggle.addEventListener('click',()=>{
  const open=evidencePanel.hasAttribute('hidden');
  evidencePanel.toggleAttribute('hidden',!open);
  evidenceToggle.setAttribute('aria-expanded',String(open));
});
const initial=Math.max(0,Math.min(3,Number(new URL(location.href).searchParams.get('era')||0)));
slider.value=initial;update(initial);
