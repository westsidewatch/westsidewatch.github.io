import React from 'react';

export function EditorialHero({ eyebrow='WESTSIDE WATCH', title='Watch for the Dawn.', deck='在黑夜仍然守望，在清晨尚未來到以前保存光。' }) {
  return <main style={{minHeight:'100vh',padding:'8vw',background:'#171713',color:'#eee8d7',fontFamily:'Georgia, serif'}}>
    <p style={{letterSpacing:'.18em',fontSize:12}}>{eyebrow}</p>
    <h1 style={{maxWidth:900,fontSize:'clamp(64px,11vw,170px)',lineHeight:.78,fontWeight:400,margin:'12vh 0 6vh'}}>{title}</h1>
    <p style={{maxWidth:620,fontSize:'clamp(18px,2vw,28px)',lineHeight:1.5}}>{deck}</p>
  </main>;
}
