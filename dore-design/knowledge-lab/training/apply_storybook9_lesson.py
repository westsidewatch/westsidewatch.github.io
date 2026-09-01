#!/usr/bin/env python3
from pathlib import Path
import json

lab = Path(__file__).resolve().parents[1] / "storybook"
lab.mkdir(parents=True, exist_ok=True)
(lab / ".storybook").mkdir(exist_ok=True)
(lab / "src").mkdir(exist_ok=True)

package = {
    "name": "dore-design-knowledge-lab-storybook",
    "private": True,
    "version": "0.1.0",
    "type": "module",
    "scripts": {
        "storybook": "storybook dev -p 6006",
        "build-storybook": "storybook build"
    },
    "dependencies": {
        "react": "^19.1.1",
        "react-dom": "^19.1.1"
    },
    "devDependencies": {
        "@storybook/react-vite": "^9.1.3",
        "storybook": "^9.1.3",
        "vite": "^7.1.3"
    }
}
(lab / "package.json").write_text(json.dumps(package, indent=2) + "\n", encoding="utf-8")

(lab / ".storybook" / "main.js").write_text("""export default {
  stories: ['../src/**/*.stories.@(js|jsx,mjs,ts,tsx)', '../src/**/*.stories.@(js|jsx|mjs|ts|tsx)'],
  addons: [],
  framework: { name: '@storybook/react-vite', options: {} },
};
""", encoding="utf-8")

# Correct the glob to one simple supported expression.
(lab / ".storybook" / "main.js").write_text("""export default {
  stories: ['../src/**/*.stories.@(js|jsx|mjs|ts|tsx)'],
  addons: [],
  framework: { name: '@storybook/react-vite', options: {} },
};
""", encoding="utf-8")

(lab / ".storybook" / "preview.js").write_text("""export default {
  parameters: { layout: 'fullscreen', controls: { expanded: true } },
};
""", encoding="utf-8")

(lab / "src" / "EditorialHero.jsx").write_text("""import React from 'react';

export function EditorialHero({ eyebrow='WESTSIDE WATCH', title='Watch for the Dawn.', deck='在黑夜仍然守望，在清晨尚未來到以前保存光。' }) {
  return <main style={{minHeight:'100vh',padding:'8vw',background:'#171713',color:'#eee8d7',fontFamily:'Georgia, serif'}}>
    <p style={{letterSpacing:'.18em',fontSize:12}}>{eyebrow}</p>
    <h1 style={{maxWidth:900,fontSize:'clamp(64px,11vw,170px)',lineHeight:.78,fontWeight:400,margin:'12vh 0 6vh'}}>{title}</h1>
    <p style={{maxWidth:620,fontSize:'clamp(18px,2vw,28px)',lineHeight:1.5}}>{deck}</p>
  </main>;
}
""", encoding="utf-8")

(lab / "src" / "EditorialHero.stories.jsx").write_text("""import { EditorialHero } from './EditorialHero.jsx';

export default { title: 'Research/EditorialHero', component: EditorialHero, tags: ['autodocs'] };
export const Dawn = {};
export const LongDeck = { args: { deck: '文章、聖經、教會生活與研究，在同一座城中彼此照亮。這是一個用來測試長文字、比例與編輯節奏的 Storybook 狀態。' } };
""", encoding="utf-8")

print('STORYBOOK9_LESSON_APPLIED')
