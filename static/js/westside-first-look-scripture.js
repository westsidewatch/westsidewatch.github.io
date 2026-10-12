/* Westside Design OS — deterministic local-date First Look scripture.
   Fixed identity verses are never replaced by daily selections. */
(() => {
  "use strict";
  const VERSES = {
    church: {
      identity: { text: "信我的人，就如經上所說：從他腹中要流出活水的江河來。", ref: "約翰福音 7:38" },
      daily: [{text:"我來了，是要叫羊得生命，並且得的更豐盛。",ref:"約翰福音 10:10"},{text:"你們要常在我裡面，我也常在你們裡面。",ref:"約翰福音 15:4"}]
    },
    magazine: { identity:{text:"黑夜已深，白晝將近。",ref:"羅馬書 13:12"}, daily:[{text:"你們是世上的光。",ref:"馬太福音 5:14"},{text:"你們的光也當這樣照在人前。",ref:"馬太福音 5:16"}] },
    bible: { identity:{text:"於是耶穌開他們的心竅，使他們能明白聖經。",ref:"路加福音 24:45"}, daily:[{text:"你的話是我腳前的燈，是我路上的光。",ref:"詩篇 119:105"},{text:"聖經都是神所默示的。",ref:"提摩太後書 3:16"}] },
    sermon: { identity:{text:"可見信道是從聽道來的，聽道是從基督的話來的。",ref:"羅馬書 10:17"}, daily:[{text:"有耳可聽的，就應當聽！",ref:"馬太福音 11:15"},{text:"你們往普天下去，傳福音給萬民聽。",ref:"馬可福音 16:15"}] },
    book: { identity:{text:"你的話是我腳前的燈，是我路上的光。",ref:"詩篇 119:105"}, daily:[{text:"求你開我的眼睛，使我看出你律法中的奇妙。",ref:"詩篇 119:18"},{text:"我將你的話藏在心裡，免得我得罪你。",ref:"詩篇 119:11"}] },
    cinema: { identity:{text:"光照在黑暗裡，黑暗卻不接受光。",ref:"約翰福音 1:5"}, daily:[{text:"那光是真光，照亮一切生在世上的人。",ref:"約翰福音 1:9"},{text:"我是世界的光。跟從我的，就不在黑暗裡走。",ref:"約翰福音 8:12"}] },
    life: { identity:{text:"一天的難處一天當就夠了。",ref:"馬太福音 6:34"}, daily:[{text:"所以，不要為明天憂慮。",ref:"馬太福音 6:34"},{text:"我們日用的飲食，今日賜給我們。",ref:"馬太福音 6:11"}] }
  };
  const ALIASES={olive:"sermon",journal:"magazine","dawn-library":"book","daylight-cafe":"life",one:"bible"};
  function verseFor(realm,date=new Date()){
    const key=ALIASES[realm]||realm,entry=VERSES[key];if(!entry)return null;
    const day=Math.floor(Date.UTC(date.getFullYear(),date.getMonth(),date.getDate())/86400000);
    return {identity:entry.identity,daily:entry.daily[((day%entry.daily.length)+entry.daily.length)%entry.daily.length]};
  }
  function appendText(parent,tag,className,text){const el=document.createElement(tag);el.className=className;el.textContent=text;parent.append(el);return el;}
  function render(root){
    const verse=verseFor(root.dataset.wsScriptureRealm);if(!verse)return;
    const mode=root.dataset.wsScriptureMode==="identity"?"identity":"daily";
    const current=verse[mode];root.replaceChildren();root.classList.add("ws-scripture-scroll");
    root.setAttribute("role","group");root.setAttribute("aria-label","每日經文");
    const track=appendText(root,"div","ws-scripture-scroll__track","");
    for(let i=0;i<2;i++){const group=appendText(track,"span","ws-scripture-scroll__group","");if(i)group.setAttribute("aria-hidden","true");
      appendText(group,"span","ws-scripture-scroll__text",current.text);
      appendText(group,"span","ws-scripture-scroll__reference",current.ref);
    }
  }
  window.WestsideFirstLookScripture=Object.freeze({verseFor,render});
  const boot=()=>document.querySelectorAll("[data-ws-scripture-realm]").forEach(render);
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",boot,{once:true});else boot();
})();
