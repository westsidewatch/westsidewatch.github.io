#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json,re,unicodedata
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parents[1]
DEFAULT_QUEUE=ROOT/'data/dawn-10k-work-queue.json';DEFAULT_STOREFRONT=ROOT/'static/dawn-library/storefront.json';DEFAULT_BIBLICAL_WORLD=ROOT/'static/dawn-library/biblical-world/catalog.json';DEFAULT_ADMISSIONS=ROOT/'data/dawn-publication-admissions';DEFAULT_INDEX=ROOT/'static/dawn-library/canonical-index.json';DEFAULT_DAWN_SURFACE=ROOT/'static/dawn-library/surfaces/dawn-storefront.json';DEFAULT_MULTIWRITE_SURFACE=ROOT/'static/dawn-library/surfaces/multiwrite-biblical-world.json'
FORBIDDEN_RUNTIME_TOKENS=('wikisource','zh.wikisource.org','openlibrary.org')
def norm(text:str)->str:
 text=unicodedata.normalize('NFKC',str(text or '')).casefold().strip();text=re.sub(r'[^\w\s-]+',' ',text);return re.sub(r'\s+',' ',text).strip()
def signature(title:str,author:str)->str:return f'{norm(title)}::{norm(author)}'
def normalize_ol_work_id(value:Any)->str:
 value=str(value or '').strip();return value[len('/works/'):] if value.startswith('/works/') else value
def stable_dawn_work_id(seed:str)->str:return f"dawn:{hashlib.sha256(seed.encode('utf-8')).hexdigest()[:20]}"
def local_runtime_pointer(value:Any)->str|None:
 value=str(value or '').strip();lower=value.casefold()
 if not value or lower.startswith(('http://','https://','//')) or any(t in lower for t in FORBIDDEN_RUNTIME_TOKENS):return None
 return value
def read_json(path:Path,fallback:dict|None=None)->dict:return json.loads(path.read_text(encoding='utf-8')) if path.exists() else (fallback or {})
def queue_work_id(item:dict)->str:
 authority=normalize_ol_work_id(item.get('workId'));return authority or stable_dawn_work_id(str(item.get('queueId') or signature(item.get('title',''),item.get('author',''))))
def canonical_from_queue(item:dict)->dict:
 work_id=queue_work_id(item);authority_ids=dict(item.get('authorityIds') or {})
 if authority_ids.get('openLibraryWork'):authority_ids['openLibraryWork']=normalize_ol_work_id(authority_ids['openLibraryWork'])
 return {'workId':work_id,'title':str(item.get('title') or '').strip(),'authors':list(dict.fromkeys(str(v).strip() for v in (item.get('authors') or []) if str(v).strip())),'languages':list(dict.fromkeys(item.get('languages') or [])),'authorityIds':authority_ids,'edition':{'editionId':str(item.get('preferredEdition') or '').strip() or None},'cover':{'pointer':f'dawn://cover/{work_id}','mode':'canonical-fallback'},'readingPointer':None,'firstPublishYear':item.get('firstPublishYear'),'authorityBacked':bool(authority_ids.get('openLibraryWork'))}
def surface_item_work_id(item:dict,by_signature:dict[str,str])->str:
 identity=item.get('identity') or {};identifiers=item.get('identifiers') or {}
 for candidate in (item.get('workId'),identity.get('workId'),identifiers.get('openLibraryWork')):
  normalized=normalize_ol_work_id(candidate)
  if normalized:return normalized
 work=item.get('work') or {};title=item.get('title') or work.get('title') or '';author=item.get('author') or work.get('author') or '';sig=signature(title,author)
 if sig in by_signature:return by_signature[sig]
 seed=sig if sig!='::' else str(item.get('id') or json.dumps(item,ensure_ascii=False,sort_keys=True));return stable_dawn_work_id(seed)
def ensure_surface_work(item:dict,work_id:str,works:dict[str,dict])->None:
 if work_id in works:return
 work=item.get('work') or {};edition=item.get('edition') or {};identity=item.get('identity') or {};identifiers=item.get('identifiers') or {};title=str(item.get('title') or work.get('title') or '').strip();author=str(item.get('author') or work.get('author') or '').strip();language=str(item.get('language') or work.get('language') or '').strip();authority_ids={k:v for k,v in {'openLibraryWork':normalize_ol_work_id(identity.get('workId') or identifiers.get('openLibraryWork')) or None,'isbn':identity.get('isbn') or identifiers.get('isbn')}.items() if v};local_pointer=None
 for key in ('readingPointer','readerUrl','contentUrl'):
  local_pointer=local_runtime_pointer(item.get(key))
  if local_pointer:break
 works[work_id]={'workId':work_id,'title':title,'authors':[author] if author else [],'languages':[language] if language else [],'authorityIds':authority_ids,'edition':{'editionId':str(identity.get('editionId') or identifiers.get('openLibraryEdition') or '').strip() or None,'label':edition.get('label'),'translator':edition.get('translator'),'publicDomain':edition.get('publicDomain')},'cover':{'pointer':f'dawn://cover/{work_id}','mode':'canonical-fallback'},'readingPointer':local_pointer,'firstPublishYear':item.get('firstPublishYear'),'authorityBacked':bool(authority_ids.get('openLibraryWork'))}
def compile_storefront(storefront:dict,works:dict[str,dict],by_signature:dict[str,str])->dict:
 shelves=[]
 for shelf in storefront.get('shelves',[]):
  refs=[]
  for item in shelf.get('items',[]):
   work_id=surface_item_work_id(item,by_signature);ensure_surface_work(item,work_id,works);refs.append({'workId':work_id})
  shelves.append({'id':shelf.get('id'),'title':shelf.get('title'),'kind':shelf.get('kind'),'items':refs})
 return {'schema':'dawn.library.surface.v1','surfaceId':'dawn-storefront','canonicalIndex':'../canonical-index.json','title':storefront.get('title') or '黎明書局','shelves':shelves}
def compile_multiwrite_surface(catalog:dict,works:dict[str,dict],by_signature:dict[str,str])->dict:
 refs=[]
 for item in catalog.get('items',[]):
  work_id=surface_item_work_id(item,by_signature);ensure_surface_work(item,work_id,works);ref={'workId':work_id}
  if item.get('relations'):ref['relations']=list(dict.fromkeys(item.get('relations') or []))
  refs.append(ref)
 return {'schema':'dawn.library.surface.v1','surfaceId':'multiwrite-biblical-world','canonicalIndex':'../canonical-index.json','title':catalog.get('title') or '聖經世界','items':refs}
def load_publication_admissions(directory:Path)->list[dict]:
 if not directory.exists():return []
 result=[]
 for path in sorted(directory.glob('*.json')):
  row=read_json(path)
  if row.get('schema')!='dore.dawn-publication-admission.v1':raise ValueError(f'invalid publication admission: {path.name}')
  result.append(row)
 return result
def apply_publications(works:dict[str,dict],dawn_surface:dict,admissions:list[dict])->None:
 if not admissions:return
 shelf=next((s for s in dawn_surface.get('shelves',[]) if s.get('id')=='dore-publications'),None)
 if shelf is None:
  shelf={'id':'dore-publications','title':'多寫 · 正式出版','kind':'canonical-publications','items':[]};dawn_surface.setdefault('shelves',[]).insert(0,shelf)
 existing={r.get('workId') for r in shelf.get('items',[])}
 for admission in admissions:
  runtime={'work':admission.get('work'),'edition':admission.get('edition'),'surface':admission.get('surface')};serialized=json.dumps(runtime,ensure_ascii=False).casefold()
  if any(t in serialized for t in FORBIDDEN_RUNTIME_TOKENS):raise ValueError('forbidden publication runtime dependency')
  work=admission.get('work') or {};edition=admission.get('edition') or {};policy=admission.get('policy') or {};surface=admission.get('surface') or {};work_id=str(work.get('workId') or '')
  if not work_id or edition.get('workId')!=work_id or (surface.get('ref') or {}).get('workId')!=work_id:raise ValueError('publication identity mismatch')
  if policy.get('surfaceOwnsIdentity') is not False or policy.get('wikisource')!='forbidden':raise ValueError('publication policy mismatch')
  artifacts=edition.get('artifacts') or {}
  for kind in ('cover','web','epub','pdf'):
   ptr=local_runtime_pointer(artifacts.get(kind))
   if not ptr:raise ValueError(f'invalid publication {kind} pointer: {work_id}')
   path=ROOT/ptr.lstrip('/')
   if not path.is_file():raise ValueError(f'missing publication artifact: {ptr}')
  canonical=works.get(work_id) or {'workId':work_id,'authorityIds':{},'firstPublishYear':None,'authorityBacked':False}
  canonical.update({'title':str(work.get('title') or canonical.get('title') or '').strip(),'authors':list(dict.fromkeys(work.get('authors') or canonical.get('authors') or [])),'languages':list(dict.fromkeys(work.get('languages') or canonical.get('languages') or [])),'edition':edition,'editions':[edition],'cover':{'pointer':f'dawn://cover/{work_id}','mode':'published-artifact'},'readingPointer':artifacts.get('web'),'publicationOrigin':'multiwrite'})
  works[work_id]=canonical
  if work_id not in existing:shelf['items'].insert(0,{'workId':work_id});existing.add(work_id)
def assert_runtime_contract(index:dict,surfaces:list[dict])->None:
 serialized=json.dumps({'works':index.get('works',{}),'surfaces':surfaces},ensure_ascii=False).casefold()
 for token in FORBIDDEN_RUNTIME_TOKENS:
  if token in serialized:raise ValueError(f'forbidden runtime dependency: {token}')
 works=index.get('works') or {}
 if len(works)!=index.get('workCount'):raise ValueError('workCount does not match canonical works')
 for work_id,work in works.items():
  if work.get('workId')!=work_id:raise ValueError(f'canonical key mismatch: {work_id}')
  if work.get('readingPointer') and not local_runtime_pointer(work['readingPointer']):raise ValueError(f'external reading pointer: {work_id}')
  if not str((work.get('cover') or {}).get('pointer') or '').startswith('dawn://cover/'):raise ValueError(f'non-canonical cover pointer: {work_id}')
 def refs(surface):
  if 'shelves' in surface:
   for shelf in surface.get('shelves',[]):yield from shelf.get('items',[])
  else:yield from surface.get('items',[])
 for surface in surfaces:
  for ref in refs(surface):
   if set(ref)-{'workId','relations'}:raise ValueError(f'surface contains identity payload: {surface.get("surfaceId")}')
   if ref.get('workId') not in works:raise ValueError(f'unresolved surface Work ID: {ref.get("workId")}')
def build(queue:dict,storefront:dict,biblical_world:dict,admissions:list[dict]|None=None)->tuple[dict,dict,dict]:
 works={};by_signature={}
 for item in queue.get('items',[]):
  record=canonical_from_queue(item);work_id=record['workId'];works[work_id]=record;sig=signature(record['title'],record['authors'][0] if record['authors'] else '')
  if sig!='::':by_signature.setdefault(sig,work_id)
 dawn_surface=compile_storefront(storefront,works,by_signature);multiwrite_surface=compile_multiwrite_surface(biblical_world,works,by_signature);apply_publications(works,dawn_surface,admissions or []);authority_backed=sum(1 for work in works.values() if work.get('authorityBacked'))
 index={'schema':'dawn.library.canonical-index.v1','identityAuthority':'Dawn','runtimePolicy':{'externalSources':'discovery-reconciliation-only','openLibraryRuntime':False,'wikisource':'forbidden','surfaceOwnsIdentity':False},'step6Baseline':{'deduplicatedWorks':queue.get('deduplicatedWorks'),'authorityBackedWorks':queue.get('authorityBackedWorks')},'workCount':len(works),'authorityBackedWorks':authority_backed,'works':dict(sorted(works.items()))}
 assert_runtime_contract(index,[dawn_surface,multiwrite_surface]);return index,dawn_surface,multiwrite_surface
def write_json(path:Path,payload:dict)->None:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(payload,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
def main()->int:
 p=argparse.ArgumentParser();p.add_argument('--queue',type=Path,default=DEFAULT_QUEUE);p.add_argument('--storefront',type=Path,default=DEFAULT_STOREFRONT);p.add_argument('--biblical-world',type=Path,default=DEFAULT_BIBLICAL_WORLD);p.add_argument('--admissions-dir',type=Path,default=DEFAULT_ADMISSIONS);p.add_argument('--index-out',type=Path,default=DEFAULT_INDEX);p.add_argument('--dawn-surface-out',type=Path,default=DEFAULT_DAWN_SURFACE);p.add_argument('--multiwrite-surface-out',type=Path,default=DEFAULT_MULTIWRITE_SURFACE);args=p.parse_args();queue=read_json(args.queue)
 if queue.get('schema')!='dawn.library.10k-work-queue.v2':raise SystemExit('Step 6 queue missing or schema mismatch')
 if queue.get('deduplicatedWorks')!=len(queue.get('items',[])):raise SystemExit('Step 6 queue count mismatch')
 if queue.get('deduplicatedWorks',0)<10000 or queue.get('authorityBackedWorks',0)<9000:raise SystemExit('Step 6 baseline is below accepted threshold')
 admissions=load_publication_admissions(args.admissions_dir);index,dawn_surface,multiwrite_surface=build(queue,read_json(args.storefront,{'shelves':[]}),read_json(args.biblical_world,{'items':[]}),admissions);write_json(args.index_out,index);write_json(args.dawn_surface_out,dawn_surface);write_json(args.multiwrite_surface_out,multiwrite_surface);print(json.dumps({'schema':index['schema'],'workCount':index['workCount'],'authorityBackedWorks':index['authorityBackedWorks'],'publicationAdmissions':len(admissions),'step6Baseline':index['step6Baseline'],'dawnSurfaceRefs':sum(len(s.get('items',[])) for s in dawn_surface.get('shelves',[])),'multiwriteSurfaceRefs':len(multiwrite_surface.get('items',[]))},ensure_ascii=False));return 0
if __name__=='__main__':raise SystemExit(main())
