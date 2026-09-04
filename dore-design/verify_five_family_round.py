#!/usr/bin/env python3
import hashlib,json,sys,urllib.request
BASE='http://127.0.0.1:4310'
IDS=['new-westside-archive-broadsheet','new-westside-stone-threshold','new-westside-field-notes','new-westside-liturgical-sequence','new-westside-luminous-index']
RKEYS=['hypothesis','why_test','prior_learning_consumed','deliberately_rejected','largest_risk']
def get(url):
 with urllib.request.urlopen(url,timeout=10) as r:return r.status,r.read()
try:
 st,data=get(BASE+'/api/workspace'); w=json.loads(data); pages={p.get('id'):p for p in w.get('pages',[]) if isinstance(p,dict)}; failures=[]; details=[]
 for pid in IDS:
  p=pages.get(pid)
  if not p: failures.append({'gate':'page_present','page':pid}); continue
  rat=p.get('rationale') if isinstance(p.get('rationale'),dict) else {}; miss=[k for k in RKEYS if not str(rat.get(k) or '').strip()]
  nodes=p.get('nodes') if isinstance(p.get('nodes'),list) else []; editable=bool(nodes) and all(isinstance(n,dict) and n.get('id') and n.get('type') for n in nodes)
  ps,pv=get(BASE+'/preview/'+pid); es,ev=get(BASE+'/api/export.html?page='+pid); same=ps==200 and es==200 and hashlib.sha256(pv).hexdigest()==hashlib.sha256(ev).hexdigest()
  semantics=p.get('experimental_only') is True and p.get('product_acceptance') is False and p.get('style_acceptance') is False
  if miss:failures.append({'gate':'rationale','page':pid,'missing':miss})
  if not editable:failures.append({'gate':'editable','page':pid})
  if not same:failures.append({'gate':'preview_export_same_source','page':pid})
  if not semantics:failures.append({'gate':'acceptance_semantics','page':pid})
  details.append({'page':pid,'nodes':len(nodes),'rationale_ok':not miss,'editable':editable,'preview_export_same':same,'acceptance_semantics':semantics})
 out={'ok':not failures,'code':'FIVE_FAMILY_SEMANTIC_PASS' if not failures else 'FIVE_FAMILY_SEMANTIC_FAIL','workspace_revision':w.get('revision'),'workspace_page_count':len(pages),'required_pages':len(IDS),'matched_pages':sum(1 for x in IDS if x in pages),'details':details,'failures':failures}
except Exception as e: out={'ok':False,'code':'FIVE_FAMILY_SEMANTIC_EXCEPTION','error':type(e).__name__+': '+str(e)}
print(json.dumps(out,ensure_ascii=False)); sys.exit(0 if out.get('ok') else 2)
