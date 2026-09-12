import base64,importlib.util,tempfile,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def load(path,name):
 spec=importlib.util.spec_from_file_location(name,ROOT/path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

class DawnPublicationSealTests(unittest.TestCase):
 def setUp(self):
  self.action=load(Path('local/dore-local/dawn_publication_action.py'),'dawn_publication_action_test')
  self.builder=load(Path('scripts/build_dawn_canonical_substrate.py'),'dawn_builder_test')
  self.admission={'schema':'dore.dawn-publication-admission.v1','identityAuthority':'Dawn','work':{'workId':'dawn:seal-test','title':'Seal Test','authors':['Author'],'languages':['en']},'edition':{'editionId':'dawn:seal-test:edition-1','workId':'dawn:seal-test','publishedAt':'2026-09-12T00:00:00Z','artifacts':{'cover':'cover.png','web':'book.html','epub':'book.epub','pdf':'book.pdf'}},'surface':{'surfaceId':'dawn-storefront','shelfId':'dore-publications','ref':{'workId':'dawn:seal-test'}},'policy':{'surfaceOwnsIdentity':False,'externalRuntime':False,'wikisource':'forbidden'}}
  raw={'cover':b'PNGDATA','web':b'<html>seal</html>','epub':b'PKepub','pdf':b'%PDF-seal'}
  names={'cover':'cover.png','web':'book.html','epub':'book.epub','pdf':'book.pdf'}
  self.assets=[{'kind':k,'filename':names[k],'bytes':len(v),'mime':'application/octet-stream','base64':base64.b64encode(v).decode()} for k,v in raw.items()]
 def test_action_validation_is_complete_and_idempotent_identity(self):
  w,e,items=self.action._validate(self.admission,self.assets);self.assertEqual(w,'dawn:seal-test');self.assertEqual(e,'dawn:seal-test:edition-1');self.assertEqual(set(items),{'cover','web','epub','pdf'})
 def test_blocked_and_forbidden_inputs_cannot_publish(self):
  bad=dict(self.admission);bad['work']=dict(self.admission['work'],title='https://zh.wikisource.org/test')
  with self.assertRaises(ValueError):self.action._validate(bad,self.assets)
  incomplete=self.assets[:-1]
  with self.assertRaises(ValueError):self.action._validate(self.admission,incomplete)
 def test_canonical_builder_admits_one_work_and_one_surface_ref(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);self.builder.ROOT=root
   paths={'cover':'/static/dawn-library/publications/x/cover.png','web':'/static/dawn-library/publications/x/book.html','epub':'/static/dawn-library/publications/x/book.epub','pdf':'/static/dawn-library/publications/x/book.pdf'}
   for value in paths.values():
    p=root/value.lstrip('/');p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'x')
   admission={**self.admission,'edition':{**self.admission['edition'],'artifacts':paths}}
   queue={'deduplicatedWorks':0,'authorityBackedWorks':0,'items':[]}
   index,dawn,_=self.builder.build(queue,{'shelves':[]},{'items':[]},[admission,admission])
   self.assertEqual(index['workCount'],1);self.assertEqual(index['works']['dawn:seal-test']['readingPointer'],paths['web'])
   shelf=next(s for s in dawn['shelves'] if s['id']=='dore-publications');self.assertEqual(shelf['items'],[{'workId':'dawn:seal-test'}])

if __name__=='__main__':unittest.main()
