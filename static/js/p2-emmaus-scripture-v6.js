/* P2 / 03 Emmaus V6 — real bilingual verse text, NOT study summaries.
 * Source: Traditional Chinese Union Version (1919) and English KJV,
 * pinned to midvash/bible-data revision d9fe1779447717bbfcb578e505b893125cad581c.
 * Both Gospels are hosted locally; the other 64 books are read as pinned
 * per-book JSON when selected. A missing text is disclosed, never invented.
 */
(()=>{'use strict';
 const root=document.getElementById('emmaus'),
  output=document.getElementById('em-scripture-verses'),
  label=document.getElementById('em-scripture-location'),
  status=document.getElementById('em-scripture-source'),
  D=window.ONE_DATA;
 if(!root||!output||!label||!status||D?.books?.length!==66)return;
 const revision='d9fe1779447717bbfcb578e505b893125cad581c';
 const slug=[
  'Gen','Exod','Lev','Num','Deut','Josh','Judg','Ruth','1Sam','2Sam',
  '1Kgs','2Kgs','1Chr','2Chr','Ezra','Neh','Esth','Job','Ps','Prov',
  'Eccl','Song','Isa','Jer','Lam','Ezek','Dan','Hos','Joel','Amos',
  'Obad','Jonah','Mic','Nah','Hab','Zeph','Hag','Zech','Mal','Matt',
  'Mark','Luke','John','Acts','Rom','1Cor','2Cor','Gal','Eph','Phil',
  'Col','1Thess','2Thess','1Tim','2Tim','Titus','Phlm','Heb','Jas','1Pet',
  '2Pet','1John','2John','3John','Jude','Rev'
 ];
 const cache=new Map();
 let version=0;
 const sourceBase='https://raw.githubusercontent.com/midvash/bible-data/'+revision+'/versions/';
 const num=n=>String(n).padStart(2,'0');
 const notify=text=>{const p=document.createElement('p');p.className='emmaus__scripture-status';p.textContent=text;output.replaceChildren(p)};
 const fetchJSON=async url=>{
  const res=await fetch(url,{mode:'cors',credentials:'omit'});
  if(!res.ok)throw new Error('Source unavailable: '+res.status);
  return res.json();
 };
 const remote=async(index)=>{
  const name=slug[index-1];
  const [cuv,kjv]=await Promise.all([
   fetchJSON(sourceBase+'zh/cuv/books/'+name+'.json'),
   fetchJSON(sourceBase+'en/kjv/books/'+name+'.json')
  ]);
  return {translations:{cuv,kjv}};
 };
 function getBook(index){
  if(!cache.has(index)){
   const p=(index===42||index===43?
    fetchJSON('/data/p2-emmaus-scripture-v6/'+slug[index-1]+'.json')
     .catch(()=>remote(index)):
    remote(index)
   ).then(data=>{
    const c=data?.translations?.cuv,k=data?.translations?.kjv;
    if(c?.bookId!==index||k?.bookId!==index||!Array.isArray(c.chapters)||!Array.isArray(k.chapters))
     throw new Error('Book source mismatch');
    return data;
   }).catch(err=>{cache.delete(index);throw err});
   cache.set(index,p);
  }
  return cache.get(index);
 }
 function makeVerse(n,zh,en){
  const li=document.createElement('li');
  li.className='emmaus__scripture-verse';
  li.dataset.verse=String(n);
  const number=document.createElement('button');
  number.type='button';number.className='emmaus__scripture-verse-number';
  number.textContent=num(n);number.setAttribute('aria-label','第 '+n+' 節，標記重點');
  number.setAttribute('aria-pressed','false');
  const pair=document.createElement('div');pair.className='emmaus__scripture-pair';
  const chinese=document.createElement('p');
  chinese.className='emmaus__scripture-zh';chinese.lang='zh-Hant';
  chinese.textContent=zh||'〔此版本未提供本節經文〕';
  const english=document.createElement('p');
  english.className='emmaus__scripture-en';english.lang='en';
  english.textContent=en||'[This verse is unavailable in the pinned KJV source.]';
  pair.append(chinese,english);li.append(number,pair);
  number.addEventListener('click',()=>{
   const active=li.dataset.emphasis==='on';
   for(const el of output.querySelectorAll('.emmaus__scripture-verse[data-emphasis="on"]')){
    delete el.dataset.emphasis;
    el.querySelector('button')?.setAttribute('aria-pressed','false');
   }
   if(!active){li.dataset.emphasis='on';number.setAttribute('aria-pressed','true')}
  });
  return li;
 }
 async function render(book,chapter){
  const n=Number(book),ch=Number(chapter);
  if(!Number.isInteger(n)||n<1||n>66||!Number.isInteger(ch)||ch<1||ch>D.books[n-1][3])return;
  const ticket=++version,item=D.books[n-1];
  label.textContent=item[1]+' · 第 '+ch+' 章';
  status.textContent='CUV（1919） / KING JAMES VERSION · 逐節對照';
  notify('載入 '+item[1]+' 第 '+ch+' 章，中英文經文…');
  try{
   const source=await getBook(n);if(ticket!==version)return;
   const cuv=source.translations.cuv.chapters.find(x=>Number(x.chapter)===ch);
   const kjv=source.translations.kjv.chapters.find(x=>Number(x.chapter)===ch);
   if(!cuv||!kjv)throw new Error('Missing chapter');
   const zh=new Map(cuv.verses.map(v=>[Number(v.number),String(v.text||'').trim()]));
   const en=new Map(kjv.verses.map(v=>[Number(v.number),String(v.text||'').trim()]));
   const numbers=[...new Set([...zh.keys(),...en.keys()])].filter(x=>Number.isInteger(x)&&x>0).sort((a,b)=>a-b);
   if(!numbers.length)throw new Error('Missing verses');
   const list=document.createElement('ol');list.className='emmaus__scripture-lines';
   for(const verse of numbers)list.append(makeVerse(verse,zh.get(verse),en.get(verse)));
   output.replaceChildren(list);output.scrollTop=0;
   status.textContent='和合本（繁體）1919  /  KJV · '+numbers.length+' VERSES · '+item[1]+' '+ch;
   root.dataset.scriptureBook=String(n);root.dataset.scriptureChapter=String(ch);
   root.dataset.scriptureState='ready';
  }catch(error){
   if(ticket!==version)return;
   root.dataset.scriptureState='unavailable';
   status.textContent='CUV / KJV · 暫時無法讀取原文';
   notify('本章逐節經文暫時無法載入。可使用「開啟 ONE 完整研讀」；此處不以摘要冒充經文。');
  }
 }
 root.addEventListener('p2:one-selection',e=>{
  render(e.detail?.book,e.detail?.chapter);
 });
 render(Number(root.dataset.selectedBook)||42,Number(root.dataset.selectedChapter)||24);
})();
