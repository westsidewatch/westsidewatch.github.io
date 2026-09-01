#!/usr/bin/env python3
"""First real New Westside visual-learning loop for Doré Storybook.

This is not a synthetic demo. It uses the locked approved homepage as the control
specimen, extracts its real Westside tokens/hero grammar, writes a Storybook
research specimen, builds Storybook, and records evidence. The parent homepage
is read-only.
"""
from __future__ import annotations
import json, re, subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
HOME=ROOT/'dore-design/new-westside/homepage-v2-living-fortress.html'
SB=ROOT/'dore-design/knowledge-lab/storybook'
STORIES=SB/'src/stories'
EVID=ROOT/'dore-design/knowledge-lab/evidence/new-westside-storybook-loop-1.json'

src=HOME.read_text(encoding='utf-8')

def cssvar(name, fallback):
    m=re.search(r'--'+re.escape(name)+r':\s*([^;]+);',src)
    return m.group(1).strip() if m else fallback

tokens={k:cssvar(k,v) for k,v in {
    'paper':'#f2eee4','ink':'#1e211f','night':'#0b2639','night-2':'#071a28','gold':'#b39a47','gold-soft':'#d0bd78'
}.items()}

STORIES.mkdir(parents=True,exist_ok=True)
story=STORIES/'NewWestsideEditorialHero.stories.js'
story.write_text(f'''import React from 'react';

const t={json.dumps(tokens,ensure_ascii=False)};
const styles={{
  shell:{{fontFamily:'"Cormorant Garamond","Noto Serif TC",Georgia,serif',background:t.night,color:t.paper,minHeight:'720px',position:'relative',overflow:'hidden'}},
  glow:{{position:'absolute',inset:'0 0 0 42%',background:'radial-gradient(circle at 60% 42%, rgba(208,189,120,.22), transparent 42%), linear-gradient(135deg, rgba(242,238,228,.08), rgba(7,26,40,.55))'}},
  copy:{{position:'relative',zIndex:1,minHeight:'720px',padding:'56px clamp(24px,5vw,80px)',display:'flex',flexDirection:'column',justifyContent:'flex-end'}},
  kicker:{{fontSize:12,letterSpacing:'.18em',textTransform:'uppercase',color:t['gold-soft'],marginBottom:18}},
  title:{{margin:0,maxWidth:'6.6em',fontSize:'clamp(76px,10vw,166px)',fontWeight:400,lineHeight:.72,letterSpacing:'-.055em'}},
  bottom:{{marginTop:38,display:'grid',gridTemplateColumns:'minmax(260px,520px) 1fr',gap:40,alignItems:'end'}},
  body:{{fontSize:'clamp(18px,1.8vw,27px)',lineHeight:1.42,margin:0,maxWidth:'22em'}},
  verse:{{justifySelf:'end',textAlign:'right',color:t['gold-soft'],fontSize:16,lineHeight:1.45}}
}};

function Hero({variant='control'}){{
  const alternate=variant==='threshold-study';
  return <section style={{{{...styles.shell, minHeight:alternate?'660px':'720px'}}}}>
    <div style={{...styles.glow, inset: alternate ? '0 0 0 54%' : styles.glow.inset}} />
    <div style={styles.copy}>
      <div style={styles.kicker}>WESTSIDE WATCH · VISUAL RESEARCH / 01</div>
      <h1 style={styles.title}>Watch for <span style={{{{color:t['gold-soft']}}}}>the Dawn</span></h1>
      <div style={styles.bottom}>
        <p style={styles.body}>A real New Westside specimen: editorial scale, restrained metadata, dawn-gold emphasis, and a threshold between darkness and first light.</p>
        <div style={styles.verse}>THE NIGHT IS FAR SPENT,<br/>THE DAY IS AT HAND.</div>
      </div>
    </div>
  </section>
}}

export default {{title:'New Westside/Research/Editorial Hero',component:Hero,parameters:{{layout:'fullscreen'}}}};
export const LockedBaseline={{args:{{variant:'control'}}}};
export const ThresholdStudy={{args:{{variant:'threshold-study'}}}};
''',encoding='utf-8')

cp=subprocess.run(['npm','run','build-storybook'],cwd=SB,text=True,capture_output=True)
EVID.parent.mkdir(parents=True,exist_ok=True)
evidence={
  'loop':'new-westside-storybook-real-loop.v0.1',
  'parent_goal':'New Westside visual construction',
  'control_source':'dore-design/new-westside/homepage-v2-living-fortress.html',
  'control_modified':False,
  'specimen':str(story.relative_to(ROOT)),
  'tokens_extracted':tokens,
  'variants':['LockedBaseline','ThresholdStudy'],
  'build_returncode':cp.returncode,
  'build_ok':cp.returncode==0,
  'stdout':(cp.stdout or '')[-6000:],
  'stderr':(cp.stderr or '')[-6000:],
  'next_question':'Compare the threshold-study variant against the locked baseline and promote only evidence-backed Westside patterns.'
}
EVID.write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(evidence,ensure_ascii=False))
raise SystemExit(cp.returncode)
