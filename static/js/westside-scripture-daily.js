/* Westside Design OS: canonical Scripture identity and daily selection.
 * Daily pools are intentionally empty until text/translation review.
 * This module never invents verses or requests an external Bible API. */
(function(){
 'use strict';
 const theme={
  church:{text:'信我的人，就如經上所說：從他腹中要流出活水的江河來。',reference:'約翰福音 7:38'},
  magazine:{text:'黑夜已深，白晝將近。',reference:'羅馬書 13:12'},
  bible:{text:'於是耶穌開他們的心竅，使他們能明白聖經。',reference:'路加福音 24:45'},
  sermon:{text:'可見信道是從聽道來的，聽道是從基督的話來的。',reference:'羅馬書 10:17'},
  book:{text:'你的話是我腳前的燈，是我路上的光。',reference:'詩篇 119:105'},
  cinema:{text:'光照在黑暗裡，黑暗卻不接受光。',reference:'約翰福音 1:5'},
  life:{text:'一天的難處一天當就夠了。',reference:'馬太福音 6:34'}
 };
 const daily={church:[],magazine:[],bible:[],sermon:[],book:[],cinema:[],life:[]};
 function easternDay(){
  const parts=new Intl.DateTimeFormat('en-US',{timeZone:'America/Toronto',year:'numeric',month:'2-digit',day:'2-digit'}).formatToParts(new Date());
  const v=Object.fromEntries(parts.map(p=>[p.type,p.value]));
  return v.year+'-'+v.month+'-'+v.day;
 }
 function selection(realm,day=easternDay()){
  const base=theme[realm];if(!base)return null;
  const pool=daily[realm]||[];
  if(!pool.length)return {...base,day,isDaily:false};
  const n=Number(day.replace(/\D/g,''))%pool.length;
  return {...pool[n],day,isDaily:true};
 }
 function render(){
  document.querySelectorAll('[data-ws-scripture-realm]').forEach(el=>{
   const item=selection(el.getAttribute('data-ws-scripture-realm'));
   if(!item)return;
   el.querySelectorAll('[data-ws-scripture-text]').forEach(n=>{n.textContent=item.text});
   el.querySelectorAll('[data-ws-scripture-reference]').forEach(n=>{n.textContent=item.reference});
  });
 }
 window.WestsideScripture={theme,selection,easternDay,render};
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',render,{once:true});else render();
})();
