import React from 'react';

const concepts={
 index:{paper:'#eee9dc',ink:'#171714',accent:'#a23b27',label:'A · LUMINOUS INDEX',layout:'index'},
 dispatch:{paper:'#061722',ink:'#f4efe4',accent:'#f06f46',label:'B · MIDNIGHT DISPATCH',layout:'dispatch'},
 folio:{paper:'#e7b8a6',ink:'#241913',accent:'#d9503f',label:'C · INDEPENDENT FOLIO',layout:'folio'},
};
function HomepageConcept({concept='index'}){
 const c=concepts[concept];
 return <main style={{minHeight:'100vh',background:c.paper,color:c.ink,fontFamily:'"Cormorant Garamond","Noto Serif TC",Georgia,serif',padding:'clamp(24px,4vw,64px)'}}>
  <header style={{display:'flex',justifyContent:'space-between',borderBottom:`1px solid ${c.ink}`,paddingBottom:14,font:'11px ui-monospace',letterSpacing:'.12em'}}><b>WESTSIDE WATCH · 西望</b><span>{c.label}</span></header>
  <section style={{minHeight:'68vh',display:'grid',gridTemplateColumns:concept==='dispatch'?'.42fr .58fr':'1.15fr .85fr',gap:'5vw',alignItems:'end',background:concept==='folio'?c.accent:'transparent',margin:'0 -2vw',padding:'5vw 2vw'}}>
   <h1 style={{fontSize:'clamp(78px,12vw,190px)',lineHeight:.68,letterSpacing:'-.055em',fontWeight:400,margin:0}}>WATCH<br/>FOR THE<br/><i style={{color:concept==='folio'?'#f4e3b2':c.accent}}>DAWN.</i></h1>
   <div style={{background:concept==='folio'?'#f4e3b2':'transparent',color:c.ink,padding:concept==='folio'?30:0,transform:concept==='folio'?'rotate(-2deg)':'none',boxShadow:concept==='folio'?`12px 12px 0 ${c.ink}`:'none'}}><p style={{fontSize:'clamp(20px,2vw,30px)',lineHeight:1.4}}>在黑夜仍然守望，在清晨尚未來到以前保存光。文章、聖經、教會生活與研究，在同一座城中彼此照亮。</p><small style={{color:c.accent,letterSpacing:'.16em'}}>READ · STUDY · GATHER · REMEMBER</small></div>
  </section>
  <section style={{display:'grid',gridTemplateColumns:concept==='index'?'7fr 5fr':concept==='folio'?'repeat(3,1fr)':'repeat(2,1fr)',gap:concept==='folio'?18:1,background:concept==='folio'?'transparent':c.ink,paddingTop:24}}>{['JOURNAL','ONE','CHURCH','LIBRARY','THE GATE'].map((x,i)=><article key={x} style={{minHeight:240,padding:24,background:concept==='dispatch'&&i===2?c.ink:concept==='folio'?'#f4e3b2':c.paper,color:concept==='dispatch'&&i===2?c.paper:c.ink,border:concept==='folio'?`2px solid ${c.ink}`:'none',boxShadow:concept==='folio'?`6px 6px 0 ${c.ink}`:'none'}}><small style={{color:c.accent}}>{String(i+1).padStart(2,'0')}</small><h2 style={{fontSize:42,fontWeight:400}}>{x}</h2></article>)}</section>
 </main>;
}
export default {title:'New Westside/Homepage Concepts',component:HomepageConcept,parameters:{layout:'fullscreen'}};
export const LuminousIndex={args:{concept:'index'}};
export const MidnightDispatch={args:{concept:'dispatch'}};
export const IndependentFolio={args:{concept:'folio'}};
