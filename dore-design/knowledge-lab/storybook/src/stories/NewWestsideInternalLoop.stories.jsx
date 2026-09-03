import React from 'react';

const realLinks = [
  ['Journal', '/journal/', '守望，一座光明的城'],
  ['ONE', '/one/', '逐卷逐章查考聖經'],
  ['Living Water West', '/', '教會生活與聚會'],
  ['黎明書局', '/library/', '閱讀、研究與資源'],
  ['The Gate', '/join/', '進入西區守望'],
];

const shared = {
  fontFamily: 'Cormorant Garamond, Noto Serif TC, Georgia, serif',
  minHeight: '100vh',
  boxSizing: 'border-box',
};

function Frame({ children, iteration, hypothesis, consumes }) {
  return <main data-new-westside-internal-loop data-iteration={iteration} data-hypothesis={hypothesis} data-consumes-learning={consumes || ''} style={shared}>{children}</main>;
}

function IterationOneView() {
  return <Frame iteration="1" hypothesis="hierarchy-before-atmosphere">
    <style>{`
      *{box-sizing:border-box} body{margin:0} .i1{min-height:100vh;background:#efe9dc;color:#1f211f;padding:22px 28px 56px}.i1 header{display:grid;grid-template-columns:1fr auto;gap:18px;border-bottom:1px solid #1f211f;padding-bottom:14px}.i1 .mark{font:600 13px/1.2 system-ui;letter-spacing:.14em;text-transform:uppercase}.i1 nav{display:flex;gap:18px;flex-wrap:wrap}.i1 nav a,.i1 a{color:inherit;text-decoration:none}.i1 .hero{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(240px,.5fr);gap:32px;padding:58px 0 42px;border-bottom:1px solid #1f211f}.i1 h1{font-size:clamp(64px,11vw,164px);line-height:.78;margin:0;font-weight:500;letter-spacing:-.055em}.i1 .hero p{font-family:'Noto Serif TC',serif;font-size:18px;line-height:1.8;margin:auto 0 0}.i1 .route{display:grid;grid-template-columns:180px 1fr}.i1 .axis{border-right:1px solid #1f211f;padding:28px 20px 0 0;font:600 11px/1.6 system-ui;letter-spacing:.15em;text-transform:uppercase}.i1 .sections{padding-left:26px}.i1 article{display:grid;grid-template-columns:90px 1fr auto;gap:20px;align-items:baseline;padding:27px 0;border-bottom:1px solid rgba(31,33,31,.45)}.i1 article b{font:600 11px/1 system-ui;letter-spacing:.14em}.i1 article h2{font-size:clamp(27px,4vw,54px);font-weight:500;margin:0}.i1 article small{font:13px/1.4 'Noto Serif TC',serif;max-width:180px}.i1 .note{margin-top:30px;max-width:640px;font:14px/1.7 system-ui}
      @media(max-width:760px){.i1{padding:16px 16px 44px}.i1 header{grid-template-columns:1fr}.i1 nav{gap:12px;font-size:14px}.i1 .hero{grid-template-columns:1fr;padding:42px 0 30px;gap:26px}.i1 h1{font-size:clamp(58px,21vw,96px)}.i1 .route{grid-template-columns:1fr}.i1 .axis{border-right:0;border-bottom:1px solid #1f211f;padding:18px 0}.i1 .sections{padding-left:0}.i1 article{grid-template-columns:52px 1fr;gap:12px}.i1 article small{grid-column:2;max-width:none}.i1 article h2{font-size:34px}}
    `}</style>
    <div className="i1">
      <header><div className="mark">Westside Watch · Vaughan / Toronto · 西望</div><nav aria-label="Primary">{realLinks.slice(0,3).map(([n,h])=><a key={n} href={h}>{n}</a>)}</nav></header>
      <section className="hero"><h1>WATCH<br/>FOR THE<br/>DAWN.</h1><p>在黑夜仍然守望，在清晨尚未來到以前保存光。文章、聖經、教會生活與研究，在同一座城中彼此照亮。</p></section>
      <section className="route" aria-label="Westside places"><aside className="axis">Iteration 01<br/>Threshold Spine<br/><br/>Question:<br/>Can hierarchy lead before atmosphere?</aside><div className="sections">{realLinks.map(([n,h,d],i)=><article key={n}><b>0{i+1}</b><h2><a href={h}>{n}</a></h2><small>{d}</small></article>)}</div></section>
      <p className="note">Experimental only. This investigates information hierarchy and route clarity; it is not an accepted Westside style.</p>
    </div>
  </Frame>;
}

const iterationOneLearning = 'preserve-semantic-spine;reduce-mobile-annotation-density;make-section-thresholds-explicit;avoid-equal-tile-grid';

function IterationTwoView() {
  return <Frame iteration="2" hypothesis="semantic-spine-with-responsive-thresholds" consumes={iterationOneLearning}>
    <style>{`
      *{box-sizing:border-box} body{margin:0}.i2{min-height:100vh;background:#18231f;color:#f0eadb;padding:0 30px 56px;overflow:hidden}.i2 a{color:inherit;text-decoration:none}.i2 header{height:72px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #b9a35d}.i2 .mark{font:600 12px/1 system-ui;letter-spacing:.16em;text-transform:uppercase}.i2 nav{display:flex;gap:20px}.i2 .threshold{position:relative;display:grid;grid-template-columns:minmax(0,1.15fr) minmax(280px,.85fr);min-height:540px;border-bottom:1px solid #b9a35d}.i2 .title{display:flex;align-items:flex-end;padding:48px 5vw 46px 0}.i2 h1{font-size:clamp(70px,10vw,150px);font-weight:500;line-height:.78;letter-spacing:-.055em;margin:0}.i2 .brief{border-left:1px solid #b9a35d;padding:52px 0 44px 30px;display:flex;flex-direction:column;justify-content:flex-end}.i2 .brief .micro{font:600 11px/1.5 system-ui;letter-spacing:.16em;text-transform:uppercase;color:#d6c684}.i2 .brief p{font:19px/1.8 'Noto Serif TC',serif;margin:22px 0 0;max-width:440px}.i2 .places{display:grid;grid-template-columns:repeat(12,1fr)}.i2 article{min-height:190px;padding:24px 18px;border-bottom:1px solid #b9a35d;position:relative}.i2 article:nth-child(1){grid-column:1/8}.i2 article:nth-child(2){grid-column:8/13;border-left:1px solid #b9a35d;margin-top:45px}.i2 article:nth-child(3){grid-column:1/5;margin-top:-1px}.i2 article:nth-child(4){grid-column:5/10;border-left:1px solid #b9a35d;margin-top:28px}.i2 article:nth-child(5){grid-column:10/13;border-left:1px solid #b9a35d;margin-top:62px}.i2 article b{font:600 10px/1 system-ui;letter-spacing:.16em;color:#d6c684}.i2 article h2{font-size:clamp(28px,4vw,58px);font-weight:500;line-height:.95;margin:38px 0 12px}.i2 article p{font:14px/1.55 'Noto Serif TC',serif;margin:0;max-width:280px}.i2 footer{font:12px/1.6 system-ui;padding-top:26px;max-width:720px}
      @media(max-width:760px){.i2{padding:0 16px 38px}.i2 header{height:auto;min-height:64px;align-items:flex-start;padding:16px 0;gap:12px;flex-direction:column}.i2 nav{gap:12px;font-size:14px;flex-wrap:wrap}.i2 .threshold{grid-template-columns:1fr;min-height:0}.i2 .title{padding:45px 0 30px}.i2 h1{font-size:clamp(60px,20vw,92px)}.i2 .brief{border-left:0;border-top:1px solid #b9a35d;padding:22px 0 30px}.i2 .brief .micro{display:none}.i2 .brief p{font-size:17px;margin:0}.i2 .places{display:block}.i2 article,.i2 article:nth-child(n){min-height:0;margin:0;border-left:0!important;padding:24px 0;border-bottom:1px solid #b9a35d}.i2 article h2{font-size:38px;margin:18px 0 9px}.i2 article p{max-width:none}.i2 footer{padding-top:22px}}
    `}</style>
    <div className="i2">
      <header><div className="mark">Westside Watch · 西望</div><nav aria-label="Primary">{realLinks.slice(0,3).map(([n,h])=><a key={n} href={h}>{n}</a>)}</nav></header>
      <section className="threshold"><div className="title"><h1>WAIT<br/>FOR<br/>LIGHT.</h1></div><div className="brief"><span className="micro">Iteration 02 · consumes Iteration 01 learning</span><p>守望不是把所有入口做成同樣大小，而是在不同的門檻之間，仍然知道自己正走向哪裡。</p></div></section>
      <section className="places" aria-label="Westside places">{realLinks.map(([n,h,d],i)=><article key={n}><b>0{i+1} · THRESHOLD</b><h2><a href={h}>{n}</a></h2><p>{d}</p></article>)}</section>
      <footer>Learning consumed: preserve semantic spine · reduce mobile annotation density · make section thresholds explicit · avoid equal tile grid. Experimental only; no user style acceptance implied.</footer>
    </div>
  </Frame>;
}

export default { title: 'New Westside/Internal Loop', parameters: { layout: 'fullscreen' } };
export const Iteration01ThresholdSpine = { render: () => <IterationOneView/> };
export const Iteration02ResponsiveThresholds = { render: () => <IterationTwoView/> };
