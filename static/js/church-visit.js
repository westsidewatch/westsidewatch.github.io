/* Static visitor-facing church guide: one content source per domain, no WebGL required. */
(() => {
 'use strict';
 const E=(tag,cls,text)=>{const e=document.createElement(tag);if(cls)e.className=cls;if(text!==undefined)e.textContent=String(text||'');return e;};
 const get=path=>fetch(path,{cache:'no-store'}).then(x=>{if(!x.ok)throw Error('content unavailable');return x.json();});
 const renderMeetings=data=>{
   const node=document.querySelector('#church-gathering-list');if(!node||!Array.isArray(data.items))return;
   node.replaceChildren();
   data.items.forEach(item=>{
     const art=E('article','church-visit__gathering');
     art.append(E('span','',(item.day||'')+' / '+(item.mode||'')),E('h3','',item.name),E('p','',(item.time||'')+(item.timeVerified?'':' · 詳細時間請確認')),E('small','',item.note||''));
     node.append(art);
   });
 };
 const renderMinistries=data=>{
   const node=document.querySelector('#church-ministry-list');if(!node||!Array.isArray(data.items))return;
   node.replaceChildren();
   data.items.forEach((item,i)=>{
     const a=E('article','church-visit__ministry');
     a.append(E('small','',String(i+1).padStart(2,'0')+' / '+(item.en||'')),E('h3','',item.name),E('p','',item.description));
     const link=E('a','',item.action||'了解更多');link.href=item.href||'/church/';a.append(link);node.append(a);
   });
 };
 const sunday=document.querySelector('#church-sunday-live');
 if(sunday&&window.WestsideSunday)window.WestsideSunday.mountStatic(sunday);
 get('/data/church/gatherings.json').then(renderMeetings).catch(()=>{const n=document.querySelector('#church-gathering-list');if(n)n.textContent='聚會資料暫時無法更新，請聯絡教會。';});
 get('/data/church/ministries.json').then(renderMinistries).catch(()=>{const n=document.querySelector('#church-ministry-list');if(n)n.replaceChildren(E('a','', '使用 ONE 查經'),E('a','','聯絡活水堂西區'));const a=n?.querySelectorAll('a');if(a?.[0])a[0].href='/one/';if(a?.[1])a[1].href='mailto:westsidewatchca@gmail.com';});
})();