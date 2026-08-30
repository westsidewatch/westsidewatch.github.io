#!/usr/bin/env python3
from __future__ import annotations
import json,os,subprocess,time
from pathlib import Path
HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser(); OUT=HOME/'evolution'/'design-bakeoff'/'openpencil'; OUT.mkdir(parents=True,exist_ok=True)
def run(a,cwd=OUT,t=600):
 try:
  p=subprocess.run(a,cwd=str(cwd),text=True,capture_output=True,timeout=t)
  return {'ok':p.returncode==0,'code':p.returncode,'stdout':(p.stdout or '')[-10000:],'stderr':(p.stderr or '')[-10000:]}
 except Exception as e:return {'ok':False,'exception':type(e).__name__+': '+str(e)}
def main():
 rid=time.strftime('%Y%m%d-%H%M%S'); d=OUT/rid;d.mkdir()
 html=d/'westside.html';css=d/'westside.css';fig=d/'westside.fig';png=d/'westside.png';png2=d/'westside-v2.png'
 html.write_text('''<main class="page"><header><div><div class="kicker">WESTSIDE WATCH</div><div class="zh">西區守望</div></div><nav>JOURNAL &nbsp;&nbsp; ARCHIVE &nbsp;&nbsp; ONE &nbsp;&nbsp; JOIN</nav></header><section class="hero"><div class="eyebrow">WATCH FOR THE DAWN · A CITY OF LIGHT</div><h1>守望，<br>一座光明的城</h1><p class="lead">在黑夜尚未退去的時候守望，在晨光尚未完全顯明以前等候。不是製造光，而是辨認那已經臨近的黎明。</p><div class="rule"></div><div class="meta">本月專題 · FEATURE &nbsp;&nbsp; / &nbsp;&nbsp; 01</div></section><section class="feature"><div class="number">01</div><div><div class="eyebrow">EDITORIAL / FEATURE</div><h2>Watch for the Dawn</h2><p>我們在城市的邊緣守望，也在日常生活裡學習辨認神的工作。西區守望是一份關於信仰、教會、城市與人的編輯出版物。</p></div><aside>“The night is far spent, the day is at hand.”<br><small>ROMANS 13:12</small></aside></section></main>''')
 css.write_text('''*{box-sizing:border-box}body{margin:0;background:#FAF9F5;color:#252525;font-family:Georgia,serif}.page{width:1440px;min-height:1200px;padding:54px 72px}header{display:flex;justify-content:space-between;align-items:flex-start;border-top:1px solid #252525;padding-top:18px}.kicker{font-size:30px;letter-spacing:.08em}.zh{font-size:18px;margin-top:4px}nav{font:12px Arial,sans-serif;letter-spacing:.18em}.hero{padding:135px 0 105px;width:960px}.eyebrow{font:12px Arial,sans-serif;letter-spacing:.2em;color:#A2872A}h1{font-size:92px;line-height:.98;font-weight:400;margin:26px 0 34px}.lead{font-size:22px;line-height:1.8;width:700px}.rule{height:1px;background:#A2872A;width:100%;margin:48px 0 18px}.meta{font:12px Arial,sans-serif;letter-spacing:.18em}.feature{border-top:1px solid #252525;padding-top:38px;display:grid;grid-template-columns:150px 1fr 320px;gap:55px}.number{font-size:72px;color:#A2872A}h2{font-size:48px;font-weight:400;margin:16px 0}.feature p{font-size:18px;line-height:1.8}.feature aside{border-left:1px solid #D2BC69;padding-left:28px;font-size:22px;line-height:1.6}.feature small{font:11px Arial,sans-serif;letter-spacing:.15em}''')
 steps=[]
 cli=['npx','-y','@open-pencil/cli']
 steps.append({'name':'cli','r':run(cli+['--help'],t=300)})
 steps.append({'name':'import','r':run(cli+['import',str(html),'--css',str(css),'-o',str(fig),'--json'],t=600)})
 if fig.exists():
  steps.append({'name':'tree','r':run(cli+['tree',str(fig),'--json'],t=300)})
  steps.append({'name':'export-v1','r':run(cli+['export',str(fig),'-f','png','-o',str(png),'--json'],t=600)})
  code="const t=figma.currentPage.findOne(n=>n.type==='TEXT'&&n.characters==='Watch for the Dawn'); if(t){t.characters='The Dawn Is Near'}; 'edited'"
  steps.append({'name':'edit','r':run(cli+['eval',str(fig),'-c',code,'-w','--json'],t=300)})
  steps.append({'name':'export-v2','r':run(cli+['export',str(fig),'-f','png','-o',str(png2),'--json'],t=600)})
 ok=fig.exists() and png.exists() and png2.exists() and all(x['r'].get('ok') for x in steps)
 report={'ok':ok,'run_id':rid,'provider':'OpenPencil','artifact':str(fig) if fig.exists() else None,'render_v1':str(png) if png.exists() else None,'render_v2':str(png2) if png2.exists() else None,'structured_editable':fig.exists(),'autonomous_second_edit':png2.exists(),'steps':steps}
 (d/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False));return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
