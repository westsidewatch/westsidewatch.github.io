#!/usr/bin/env python3
"""Build one local image-generation job for an M4 16GB Mac mini.
Uses canonical Doré speaker compiler. No paid API, no model downloads, no fake portraits.
Produces prompt + deterministic SVG typography overlay + machine-readable job.
"""
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_dore_speaker_previews import SOURCE,compile_record,svg
def main():
 p=argparse.ArgumentParser()
 p.add_argument('--speaker',default='david-pawson')
 p.add_argument('--out',default='local/dore-speaker-jobs')
 a=p.parse_args()
 records=json.loads(SOURCE.read_text(encoding='utf-8'))['records']
 matches=[(i,r) for i,r in enumerate(records) if r['id']=='speaker:'+a.speaker]
 if not matches:raise SystemExit('Unknown canonical speaker: '+a.speaker)
 i,r=matches[0];spec=compile_record(r,i)
 out=Path(a.out)/a.speaker;out.mkdir(parents=True,exist_ok=True)
 (out/'design-spec.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (out/'image-prompt.txt').write_text(spec['prompt']+'\n',encoding='utf-8')
 (out/'typography-proof.svg').write_text(svg(spec),encoding='utf-8')
 job={'schema':'dore.local-image-job.v0','device':'Mac mini M4 / 16GB unified memory',
      'status':'AWAITING_LOCAL_RENDER','speaker':r['id'],'imagePromptFile':'image-prompt.txt',
      'imageInput':'background-only','expectedOutput':'generated-background.png',
      'finalComposite':'final-cover.png','canvas':[720,960],
      'constraints':{'portraitSynthesis':False,'palette':['#FFFFFF','#174B35'],
                     'noGeneratedText':True,'oneImageAtATime':True},
      'steps':['Render image-prompt.txt in local image model as background-only 3:4 image.',
               'Save output as generated-background.png in this directory.',
               'Run scripts/composite_dore_speaker_cover.py with --job path to this directory.',
               'Review final-cover.png before publication.']}
 (out/'job.json').write_text(json.dumps(job,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('READY:',out,'(render requires installed local image model)')
if __name__=='__main__':main()
