/* One verified Sunday source for P2, native tour finale and static church overview.
   No direct DOM HTML from JSON; historical bulletins never masquerade as current. */
(() => {
  'use strict';
  const source='/data/church/current-sunday.json';
  const $=(s,root=document)=>root.querySelector(s);
  const make=(tag,cls,text)=>{const e=document.createElement(tag);if(cls)e.className=cls;if(text!==undefined)e.textContent=String(text??'');return e;};
  const dateOfToronto=()=>{
    const parts=new Intl.DateTimeFormat('en-CA',{timeZone:'America/Toronto',year:'numeric',month:'2-digit',day:'2-digit'}).formatToParts(new Date());
    const p=Object.fromEntries(parts.map(x=>[x.type,x.value]));
    return p.year+'-'+p.month+'-'+p.day;
  };
  const label=d=>String(d.date||'').replace(/-/g,'/');
  const isArchived=d=>d.status!=='current'||!/^\d{4}-\d{2}-\d{2}$/.test(d.date||'')||d.date<dateOfToronto();
  const statusText=d=>isArchived(d)?'歷史主日程序 · '+label(d)+'（非本週，請向教會確認最新安排）':'本週主日 · '+label(d);
  const address=d=>d.location||'請聯絡教會確認聚會地點';
  const makeRow=(r,variant,i)=>{
    if(variant==='tour'){
      const row=make('div','ws-ministry-story__sunday-row');row.style.setProperty('--sunday-row-order',String(i));
      row.append(make('time','',r.time));
      const copy=make('div');copy.append(make('strong','',r.title),make('small','',r.detail));row.append(copy);return row;
    }
    const row=make('div','worship-row');row.append(make('time','',r.time));
    const copy=make('div');copy.append(make('strong','',r.title),make('p','',r.detail));row.append(copy);return row;
  };
  const valid=d=>d&&typeof d==='object'&&/^\d{4}-\d{2}-\d{2}$/.test(d.date||'')&&
    Array.isArray(d.schedule)&&d.schedule.length===7&&d.schedule.every(x=>x.time&&x.title&&typeof x.detail==='string')&&Array.isArray(d.scriptures);
  const ready=fetch(source,{cache:'no-store'}).then(async response=>{
    if(!response.ok)throw new Error('schedule HTTP '+response.status);
    const data=await response.json();if(!valid(data))throw new Error('invalid Sunday data');return data;
  });
  function updateP2(data,root=document){
    const section=$('.church-schedule-source',root);if(!section)return;
    section.setAttribute('aria-label',statusText(data));
    const folio=$('.sunday-schedule',section);
    if(!folio)return;
    let status=$('.ws-sunday-source-status',folio);
    if(!status){status=make('p','ws-sunday-source-status');folio.prepend(status);}
    status.textContent=statusText(data);
    const meta=$('.sunday-schedule__top',folio);
    if(meta){const spans=[...meta.querySelectorAll('span')];if(spans[0])spans[0].textContent='SUNDAY WORSHIP / '+label(data);if(spans[1])spans[1].textContent=data.serviceTime;}
    const heading=folio.querySelector('h3');if(heading){
      const en=make('span','','Sunday Worship');en.lang='en';const zh=make('span','church-p2-sunday-zh','主日崇拜 · '+(data.theme||''));zh.lang='zh-Hant';heading.replaceChildren(en,zh);
    }
    const team=$('.worship-ministry',folio);
    if(team){const p=team.querySelector('p');if(p){
      p.replaceChildren();
      ['主任牧師：'+(data.pastor||'待確認'),'司會主席：'+(data.chair||'待確認')+'　敬拜主領：'+(data.worshipLeader||'待確認'),
        '證道：'+(data.speaker||'待確認')].forEach((x,i)=>{if(i)p.append(document.createElement('br'));p.append(document.createTextNode(x));});
    }}
    const rows=$('.worship-program',folio);if(rows)rows.replaceChildren(...data.schedule.map((r,i)=>makeRow(r,'p2',i)));
    const next=$('.church-folio__meeting-meta .worship-next',root);
    if(next){const n=data.nextSunday;const span=next.querySelector('span'),p=next.querySelector('p');
      if(span)span.textContent=n&&n.date?'NEXT SUNDAY / '+n.date:'NEXT SUNDAY';
      if(p)p.textContent=n&&n.date?('證道：'+(n.speaker||'待定')+'　主席：'+(n.chair||'待定')+'　敬拜：'+(n.worshipLeader||'待定')):'下週事奉安排請向教會查詢';
    }
    const place=$('.sunday-schedule__place p',root);if(place)place.textContent=address(data);
    const grid=$('.church-folio__scripture-grid',root);
    if(grid){
      const first=make('div','church-folio__scripture-pair'),second=make('div','church-folio__scripture-final');
      data.scriptures.forEach((s,i)=>{
        const p=make('p',i===0?'schedule-theme-scripture__lead':'', '「'+s.text+'」');
        p.append(make('span','schedule-theme-scripture__ref',' '+s.reference));
        (i<2?first:second).append(p);
      });
      grid.replaceChildren(first,second);
    }
  }
  function updateTour(data,root){
    const section=$('.ws-ministry-story__sunday',root);if(!section)return;
    let status=$('.ws-sunday-source-status',section);
    if(!status){status=make('p','ws-sunday-source-status');section.prepend(status);}
    status.textContent=statusText(data);
    const head=$('.ws-ministry-story__sunday-head',section);
    if(head){const eyebrow=$('.ws-ministry-story__eyebrow',head);if(eyebrow)eyebrow.textContent='SUNDAY WORSHIP · '+label(data);
      const h=head.querySelector('h2');if(h){const en=make('span','','Sunday Worship');en.lang='en';h.replaceChildren(document.createTextNode('主日崇拜'),en);}
    }
    const rows=$('.ws-ministry-story__sunday-rows',section);
    if(rows)rows.replaceChildren(...data.schedule.map((r,i)=>makeRow(r,'tour',i)));
    const footer=section.querySelector('footer');if(footer)footer.textContent=address(data);
  }
  function updateStatic(data,root){
    if(!root)return;
    root.replaceChildren();
    root.append(make('p','ws-sunday-source-status',statusText(data)));
    const h=make('h3','',data.theme||'主日崇拜');root.append(h);
    root.append(make('p','ws-church-lead','證道：'+(data.speaker||'待確認')+'　·　'+data.serviceTime));
    const list=make('div','ws-church-sunday-rows');
    data.schedule.forEach(r=>{
      const row=make('div','ws-church-sunday-row');row.append(make('time','',r.time));
      const copy=make('div');copy.append(make('strong','',r.title),make('p','',r.detail));row.append(copy);list.append(row);
    });
    root.append(list);
    const foot=make('p','ws-church-muted',address(data));root.append(foot);
    const verses=make('div','ws-church-scriptures');
    data.scriptures.forEach(s=>{const p=make('p','',s.text);p.append(make('small','',s.reference));verses.append(p);});
    root.append(verses);
  }
  const fail=target=>{if(target){const p=make('p','ws-sunday-source-status','日程暫時無法更新，請直接向教會確認本週聚會。');target.prepend(p);}};
  function mountTour(root){ready.then(data=>updateTour(data,root)).catch(()=>fail($('.ws-ministry-story__sunday',root)));}
  function mountStatic(root){ready.then(data=>updateStatic(data,root)).catch(()=>{root.replaceChildren(make('p','ws-church-muted','暫時無法載入主日程序，請直接聯絡教會。'));});}
  function mountP2(){ready.then(data=>updateP2(data)).catch(()=>fail($('.church-schedule-source')));}
  window.WestsideSunday={ready,mountTour,mountStatic,mountP2};
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',mountP2,{once:true});else mountP2();
})();