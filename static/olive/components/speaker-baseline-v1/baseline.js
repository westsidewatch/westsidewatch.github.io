/* Olive speaker baseline v1: frozen typography; page CSS cannot cross its shadow boundary. */
(()=>{'use strict';
 const names=[{"slug": "david-pawson", "en": "DAVID PAWSON", "zh": "大衛鮑森", "image": "/images/olive/david-pawson-editorial.png", "typography": {"align": "right", "x": 96, "width": 100, "size": 10.35, "lines": ["DAVID", "PAWSON"], "thickness": 1, "opticalSize": 41.363}}, {"slug": "jiang-xiuqin", "en": "GRACE CHIANG", "zh": "江秀琴", "image": "/images/olive/jiang-xiuqin-editorial.png", "typography": {"align": "right", "x": 96, "width": 100, "size": 17.4, "lines": ["GRACE", "CHIANG"], "thickness": 1, "opticalSize": 69.537}}, {"slug": "derek-prince", "en": "DEREK PRINCE", "zh": "葉光明", "image": "/images/olive/derek-prince-editorial.png", "typography": {"align": "left", "x": 22.2805, "width": 100, "size": 18.19, "lines": ["DEREK", "PRINCE"], "thickness": 1, "opticalSize": 72.695}}, {"slug": "watchman-nee", "en": "WATCHMAN NEE", "zh": "倪柝聲", "image": "/images/olive/watchman-nee-editorial.png", "typography": {"align": "right", "x": 96, "width": 100, "size": 11, "lines": ["WATCHMAN", "NEE"], "thickness": 1, "opticalSize": 43.96}}, {"slug": "huang-shuhua", "en": "HUANG SHUHUA", "zh": "黃淑華", "image": "/images/olive/huang-shuhua-editorial.png", "typography": {"align": "left", "x": 20.4945, "width": 100, "size": 16.31, "lines": ["HUANG", "SHUHUA"], "thickness": 1, "opticalSize": 65.181}}, {"slug": "tong-liu", "en": "TONG LIU", "zh": "劉彤", "image": "/images/olive/tong-liu-editorial.png", "typography": {"align": "left", "x": 16.4, "width": 100, "size": 12, "lines": ["TONG", "LIU"], "thickness": 1, "opticalSize": 47.957}}, {"slug": "jerry-lai", "en": "JERRY LAI", "zh": "賴若瀚", "image": "/images/olive/jerry-lai-editorial.png", "typography": {"align": "right", "x": 96, "width": 100, "size": 26.24, "lines": ["JERRY", "LAI"], "thickness": 1, "opticalSize": 96}}, {"slug": "yu-hong-jie", "en": "YU HONGJIE", "zh": "于宏潔", "image": "/images/olive/yu-hong-jie-editorial.png", "typography": {"align": "right", "x": 96, "width": 100, "size": 14, "lines": ["YU", "HONG JIE"], "thickness": 1, "opticalSize": 55.95}}, {"slug": "stephen-tong", "en": "STEPHEN TONG", "zh": "唐崇榮", "image": "/images/olive/stephen-tong-editorial.png", "typography": {"align": "right", "x": 96, "width": 100, "size": 8.5, "lines": ["STEPHEN", "TONG"], "thickness": 1, "opticalSize": 33.969}}, {"slug": "rick-warren", "en": "RICK WARREN", "zh": "華理克", "image": "/images/olive/rick-warren-editorial.png", "typography": {"align": "right", "x": 96, "width": 100, "size": 10, "lines": ["RICK", "WARREN"], "thickness": 1, "opticalSize": 39.964}}, {"slug": "kang-lai-chang", "en": "KANG LAI-CHANG", "zh": "康來昌", "image": "/images/olive/kang-lai-chang-editorial.png", "typography": {"align": "right", "x": 99, "width": 100, "size": 7.2, "lines": ["KANG", "LAI CHANG"], "thickness": 1, "opticalSize": 28.774}}, {"slug": "kou-shao-en", "en": "KOU SHAO-EN", "zh": "寇紹恩", "image": "/images/olive/kou-shao-en-editorial.png", "typography": {"align": "left", "x": 15.45, "width": 100, "size": 11, "lines": ["KOU", "SHAO EN"], "thickness": 1, "opticalSize": 43.96}}];
 const bySlug=new Map(names.map(item=>[item.slug,item]));
 class OliveSpeakerBaseline extends HTMLElement{
  connectedCallback(){
   if(this.shadowRoot)return;
   const item=bySlug.get(this.dataset.speaker);if(!item)return;
   const parent=this.parentElement;
   const fit=()=>{const rect=parent.getBoundingClientRect(),width=Math.min(rect.width,rect.height*.75);this.style.width=width+'px';this.style.height=(width/0.75)+'px';this.style.left=((rect.width-width)/2)+'px';this.style.top=((rect.height-width/.75)/2)+'px';};
   this._observer=new ResizeObserver(fit);this._observer.observe(parent);fit();
   const shadow=this.attachShadow({mode:'open'});
   const style=document.createElement('link');style.rel='stylesheet';style.href='/olive/components/speaker-baseline-v1/baseline.css?v=07d89a2-recovered-v1';
   const frame=document.createElement('div');frame.className='speaker-card';frame.dataset.doreSpeaker=item.slug;frame.dataset.posterAlign=item.typography.align;frame.style.setProperty('--poster-x',item.typography.x+'%');frame.style.setProperty('--poster-width',item.typography.width+'%');frame.style.setProperty('--poster-size',item.typography.size+'cqw');frame.style.setProperty('--poster-optical-size',item.typography.opticalSize);
   const group=document.createElement('div');group.className='olive-speaker-typegroup';
   const en=document.createElement('span');en.className='olive-speaker-english';en.lang='en';en.textContent=item.en;
   const zh=document.createElement('h3');zh.lang='zh-Hant';zh.textContent=item.zh;
   group.append(en,zh);frame.append(group);shadow.append(style,frame);
  }
  disconnectedCallback(){this._observer?.disconnect()}
 }
 customElements.define('olive-speaker-baseline',OliveSpeakerBaseline);
 window.OliveSpeakerBaseline=Object.freeze({mount(card,slug){
  if(!bySlug.has(slug))return;
  if(card.querySelector('olive-speaker-baseline'))return;
  const element=document.createElement('olive-speaker-baseline');element.dataset.speaker=slug;
  element.setAttribute('aria-hidden','true');card.append(element);card.dataset.oliveProtectedBaseline='v1';
 }});
})();
