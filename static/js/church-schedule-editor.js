/* Local export-only editor: no GitHub token, secret, or personal information. */
(() => {
'use strict';
const root=document.querySelector('#sunday-editor'),rows=document.querySelector('#sunday-rows'),verses=document.querySelector('#sunday-scriptures'),preview=document.querySelector('#preview');
let original=null;const f=name=>root.elements.namedItem(name);
const field=(parent,name,label,value)=>{const box=document.createElement('label');box.textContent=label;const inp=document.createElement('input');inp.name=name;inp.value=String(value||'');box.append(inp);parent.append(box);};
fetch('/data/church/current-sunday.json',{cache:'no-store'}).then(r=>{if(!r.ok)throw Error('missing data');return r.json();}).then(data=>{
 original=data;
 for(const name of ['date','status','theme','serviceTime','location','sermonTitle','pastor','chair','worshipLeader','speaker'])f(name).value=data[name]||'';
 data.schedule.forEach((row,i)=>{const el=document.createElement('div');el.className='schedule-row';field(el,'time'+i,'時間',row.time);field(el,'title'+i,'第 '+(i+1)+' 段名稱',row.title);field(el,'detail'+i,'內容',row.detail);rows.append(el);});
 (data.scriptures||[]).forEach((s,i)=>{const el=document.createElement('div');el.className='fields';el.style.marginBottom='15px';field(el,'ref'+i,'出處',s.reference);field(el,'verse'+i,'經文',s.text);verses.append(el);});
 const n=data.nextSunday||{};f('nextDate').value=n.date||'';f('nextSpeaker').value=n.speaker||'';f('nextChair').value=n.chair||'';f('nextWorship').value=n.worshipLeader||'';
 preview.textContent='已載入 '+data.date+' 的 '+(data.status==='archive'?'歷史日程':'現行日程')+'，共七段。';
}).catch(()=>preview.textContent='原始檔案未能載入，為避免覆蓋日程，本編輯器暫時停止匯出。');
function getData(){
 if(!original)throw Error('資料未載入');if(!root.reportValidity())throw Error('請補齊必填欄位');
 const pick=name=>String(f(name)?.value||'').trim();
 const copy={...original};
 for(const name of ['date','status','theme','serviceTime','location','sermonTitle','pastor','chair','worshipLeader','speaker'])copy[name]=pick(name);
 copy.dateLabel=copy.date;
 copy.schedule=original.schedule.map((_,i)=>({time:pick('time'+i),title:pick('title'+i),detail:pick('detail'+i)}));
 if(copy.schedule.some(r=>!r.time||!r.title))throw Error('七段程序的時間與標題均不可留空');
 copy.scriptures=(original.scriptures||[]).map((_,i)=>({reference:pick('ref'+i),text:pick('verse'+i)}));
 copy.nextSunday=pick('nextDate')?{date:pick('nextDate'),speaker:pick('nextSpeaker'),chair:pick('nextChair'),worshipLeader:pick('nextWorship')}:null;
 if(!copy.date)throw Error('請填寫崇拜日期');
 return JSON.stringify(copy,null,2)+'\n';
}
document.querySelector('#download-sunday').addEventListener('click',()=>{
 try{const text=getData(),blob=new Blob([text],{type:'application/json;charset=utf-8'}),url=URL.createObjectURL(blob);
 const a=document.createElement('a');a.href=url;a.download='current-sunday.json';document.body.append(a);a.click();a.remove();
 setTimeout(()=>URL.revokeObjectURL(url),5000);preview.textContent='已產生 current-sunday.json。請上傳到原 GitHub 的指定路徑。';
 }catch(e){preview.textContent=e.message;}
});
document.querySelector('#copy-sunday').addEventListener('click',async()=>{
 try{await navigator.clipboard.writeText(getData());preview.textContent='JSON 已複製。請貼入 GitHub 的指定資料檔並提交。';}
 catch(e){preview.textContent=e.message||'複製失敗，請使用下載 JSON。';}
});
})();
