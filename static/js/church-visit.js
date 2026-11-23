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

 // Fixed QR matrices for the four official HTTPS destinations.
 // Self-hosted, no visitor data, third-party QR API or tracking.
 const qrMatrix={"join":"AAAAAAAAAAAAAAAAAAAAAAAAAAAA/i4qP4BBVCMQQC6yoeugF1571dALpn+66AQRigEEA/qqqv4AAddnAACCnlJnAA4v+4cANuXKusAMiKJP8AMq0ZMYBUBB2QwDfMc5zAFLKQSNACKlU1yAcAP8s0Ak3EdNoAiI1TXwCzmSrdgGR1PI8ALcuLs8AUuzF88A+9wR+IAASe/FQD+X02qAEEydMeALpEgv2AXRYd7cAunNY3YBBPxG/AD+3UPxAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==","decision":"AAAAAAAAAAAAAAAAAAAAAAAAAAAA/nM/P4BBLPDQQC6W0CugF0GEJdALpI566AQW8+UEA/qqqv4AAMSYAACWx4VQAEqcJHjAJ6odpqAJDEXRgAPljMZIAK8u5fwDXuolvABYvftyAB5rTy0ALlJiyoAomIoY4A2JbcYwA/xo3BgBiWU3DAOausr6ALF1bigAm8tE/AAATTxGQD+YKquAEFZu0RALpRXvwAXWJDlAAuhYNiIBBP+JwAD+tYTtAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==","newcomer":"AAAAAAAAAAAAAAAAAAAAAAAAAAAA/jM/P4BBbrnQQC6aQmugF0iEJdALrcVa6AQSoa0EA/qqqv4AAK2cAACqVdwJAEqcJHjAFvMxNOANngz1EAplDMZIA08Kd7QDDKMBLgBajPtyAFZe3WQAOBlmWMA7kBoY4B2pP48QCP1ETlAAKCQ3DAK+aIPeANhj/GEAm8pE/AAAXVVGwD+dMOqgEEKu0RALq3zP0AXSZnBkAuoYNiIBBLetUgD+t83JgAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==","prayer":"AAAAAAAAAAAAAAAAAAAAAAAAAAAA/kixP4BBELEQQC6qqeugF1MLFdALrH+66AQXwiEEA/qqqv4AAdVPAAC+NkI+ACLGHJtAL9nKusAFGYLN8Au4vKXABchI+YwAX0c5zAASQhj8ABa7U1yAQMJ+u0A0gmmWwBo58bfwCSu0rdgH45+5NAKZgLs8AUFtH+4Au9TK/IAAX03FQD+UQ2qAEFug8fALr0Qv2AXVuP5cAuokDsABBChO3AD+rUPxAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=="};
 const qrSide=41;
 document.querySelectorAll('[data-church-qr]').forEach(slot=>{
   const value=qrMatrix[slot.dataset.churchQr];if(!value)return;
   const bytes=Uint8Array.from(atob(value),x=>x.charCodeAt(0));
   const canvas=document.createElement('canvas');canvas.width=canvas.height=qrSide*4;
   const g=canvas.getContext('2d');g.imageSmoothingEnabled=false;
   g.fillStyle='#fff';g.fillRect(0,0,canvas.width,canvas.height);g.fillStyle='#1c333a';
   for(let y=0;y<qrSide;y++)for(let x=0;x<qrSide;x++){
     const i=y*qrSide+x;
     if(bytes[i>>3]&(128>>(i&7)))g.fillRect(x*4,y*4,4,4);
   }
   slot.replaceChildren(canvas);
 });
})();
