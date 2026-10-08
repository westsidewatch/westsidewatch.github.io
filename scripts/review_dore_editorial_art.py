#!/usr/bin/env python3
"""Fail-closed editorial art QA from verifiable evidence and human review.

Does not pretend to measure likeness or image pixels. Machine checks validate
brief contracts; subjective visual checks require explicit reviewer evidence.
"""
import argparse,json
from pathlib import Path

CHECKS={
 'identity':('human','Reference image is authorized and real-person likeness is faithful; if no real portrait, mark not-applicable with rationale.'),
 'crop':('human','Subject is deliberately cropped; essential facial landmarks remain visible where required.'),
 'negative_space':('human','Actual image contains usable continuous negative space in the intended box.'),
 'print_material':('human','Halftone, engraving or cutout is visibly credible at final output size.'),
 'palette':('human','Rendered image uses only section-approved image inks and paper.'),
 'type_collision':('human','Real HTML/CSS type overlays the image correctly without hiding identity.'),
 'mobile_320':('human','At 320 CSS px the focal subject and type remain legible.'),
 'mobile_375':('human','At 375 CSS px the focal subject and type remain legible.'),
 'tablet_768':('human','At 768 CSS px crop and live type remain intentional.'),
 'desktop_1440':('human','At 1440 CSS px image-text composition remains intentional.'),
 'asset_rights':('human','Portrait/reference and source-image rights or permissions have been checked.'),
 'source_truth':('human','No invented person, historical detail, book title or film still is represented as factual.'),
}
ALLOWED={'pass','fail','pending','not-applicable'}
def review(spec,answers):
 failures=[];pending=[];results={}
 for key,(_,description) in CHECKS.items():
  item=answers.get(key,{})
  if isinstance(item,str):item={'status':item}
  status=item.get('status','pending')
  evidence=item.get('evidence','').strip()
  if status not in ALLOWED:
   failures.append(key+': invalid status')
   status='fail'
  if status in ('pass','not-applicable') and not evidence:
   failures.append(key+': evidence required')
   status='fail'
  if status=='not-applicable' and key not in ('identity','type_collision'):
   failures.append(key+': not-applicable not permitted')
   status='fail'
  if status=='fail':failures.append(key+': reviewer failed check')
  if status=='pending':pending.append(key)
  results[key]={'status':status,'evidence':evidence,'question':description}
 if not spec.get('publication_approved') is False:
  failures.append('spec: expected explicit publication_approved=false')
 if spec.get('scenario') in ('speaker','column-author','interview-subject') and not spec.get('verified_reference'):
  failures.append('identity: verified reference absent for named-person scenario')
 return {'schema':'dore.editorial.qa.v1','publication_approved':False,
         'ready_for_editorial_approval':not failures and not pending,
         'failed':failures,'pending':pending,'checks':results}
def main():
 p=argparse.ArgumentParser()
 p.add_argument('--spec',required=True)
 p.add_argument('--review',help='JSON with reviewer statuses and evidence')
 p.add_argument('--out',default='local/dore-editorial-qa.json')
 a=p.parse_args()
 spec=json.loads(Path(a.spec).read_text(encoding='utf-8'))
 answers=json.loads(Path(a.review).read_text(encoding='utf-8')) if a.review else {}
 report=review(spec,answers)
 out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
 out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'ready_for_editorial_approval':report['ready_for_editorial_approval'],'failed':len(report['failed']),'pending':len(report['pending'])}))
if __name__=='__main__':main()
