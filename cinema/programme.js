(()=>{
  const URL='data/programme.v1.json';
  const pad=n=>String(n).padStart(2,'0');
  const key=d=>`${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}`;
  const matches=(rule,d)=>rule?.type==='annual'&&rule.month===d.getMonth()+1&&rule.day===d.getDate();
  const choose=(items,d)=>[...items].filter(x=>matches(x.dateRule,d)).sort((a,b)=>(b.priority||0)-(a.priority||0))[0]||items.find(x=>x.dateRule?.type==='fallback');
  const renderReason=item=>{
    const root=document.querySelector('#cinema-why-tonight'); if(!root||!item)return;
    root.replaceChildren();
    const meta=document.createElement('p');meta.className='programme-meta';meta.textContent=item.label;
    const body=document.createElement('p');body.className='programme-copy';body.textContent=item.why;
    const scripture=document.createElement('p');scripture.className='programme-scripture';scripture.textContent=(item.scripture||[]).join(' · ');
    root.append(meta,body,scripture);
  };
  const renderWeek=(items,start)=>{
    const root=document.querySelector('#cinema-week-programme');if(!root)return;const cards=[];
    for(let i=0;i<7;i++){const d=new Date(start);d.setDate(start.getDate()+i);const item=choose(items,d);const card=document.createElement('article');card.className='programme-card';card.dataset.workId=item?.workId||'';card.innerHTML=`<time datetime="${key(d)}">${d.toLocaleDateString('zh-Hant',{month:'short',day:'numeric',weekday:'short'})}</time><strong>${item?.label||'天堂電影院'}</strong><span>${(item?.scripture||[]).join(' · ')}</span>`;cards.push(card);}
    root.replaceChildren(...cards);
  };
  fetch(URL).then(r=>{if(!r.ok)throw new Error('programme');return r.json();}).then(data=>{const now=new Date();const selected=choose(data.occasions||[],now);renderReason(selected);renderWeek(data.occasions||[],now);window.ParadiseCinemaProgramme={data,selected};document.documentElement.dataset.cinemaProgramme='ready';}).catch(()=>{document.documentElement.dataset.cinemaProgramme='error';});
})();
