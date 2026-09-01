import React from 'react';
import watchman from '../../../../new-westside/assets/retro-pack-01/watchman-dawn-engraving-v1.png';

const colors={paper:'#f3ecdd',ink:'#17212b',night:'#0c2b3e',gold:'#d4b655',rust:'#a64b35'};

function Foundation(){
  return <main style={{background:colors.paper,color:colors.ink,minHeight:'100vh',fontFamily:'Georgia,"Noto Serif TC",serif'}}>
    <header style={{padding:'28px 5vw',borderTop:`12px solid ${colors.gold}`,borderBottom:`1px solid ${colors.ink}`,display:'flex',justifyContent:'space-between'}}>
      <strong>DORÉ IMAGE STUDIO / 多雷製圖</strong><small>FOUNDATION · CANDIDATE REVIEW</small>
    </header>
    <section style={{display:'grid',gridTemplateColumns:'minmax(280px,.85fr) minmax(420px,1.15fr)',gap:'4vw',padding:'5vw'}}>
      <div><div style={{color:colors.rust,font:'600 12px Arial',letterSpacing:'.14em'}}>EDITORIAL ARTWORK / 001</div><h1 style={{fontSize:'clamp(54px,7vw,112px)',lineHeight:.82,margin:'28px 0'}}>守望<br/>黎明</h1><p style={{fontSize:20,lineHeight:1.55,maxWidth:440}}>不是城塔圖示，而是一個完整的視覺事件：人物、城牆、道路與第一道光共同承擔敘事。</p><dl style={{font:'12px/1.8 Arial',marginTop:48}}><dt>STATUS</dt><dd>Candidate</dd><dt>ROLE</dt><dd>Homepage / feature hero</dd><dt>NEXT</dt><dd>Two-plate separation · mobile crop · WebP</dd></dl></div>
      <figure style={{margin:0,background:colors.night,padding:18}}><img src={watchman} alt="A solitary watchman stands on a city wall as first light reaches a distant city." style={{display:'block',width:'100%',height:'auto',filter:'sepia(.15) contrast(1.06)'}}/><figcaption style={{color:colors.gold,font:'11px Arial',paddingTop:12}}>WATCHMAN DAWN ENGRAVING V1 · 1122×1402</figcaption></figure>
    </section>
    <section style={{padding:'0 5vw 6vw'}}><h2 style={{font:'600 14px Arial',letterSpacing:'.12em'}}>WEBSITE ELEMENT FAMILY / BACKLOG</h2><div style={{display:'grid',gridTemplateColumns:'repeat(5,1fr)',borderTop:`1px solid ${colors.ink}`}}>{['晨星','第一道光','城門','書卷','紙紋'].map((x,i)=><article key={x} style={{minHeight:180,padding:20,borderRight:`1px solid ${colors.ink}`,background:i===0?colors.gold:'transparent'}}><b style={{fontSize:28}}>{String(i+1).padStart(2,'0')}</b><h3 style={{fontSize:25,marginTop:56}}>{x}</h3><small style={{fontFamily:'Arial'}}>RESEARCH → 3 CANDIDATES → STORYBOOK → APPROVE</small></article>)}</div></section>
  </main>;
}

export default {title:'Doré Image Studio/Foundation',component:Foundation,parameters:{layout:'fullscreen'}};
export const AssetAndElementSystem={};
