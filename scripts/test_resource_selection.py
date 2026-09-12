#!/usr/bin/env python3
"""Regression cases for the two independent gates; Python/browser parity."""
import copy,json,subprocess,unittest,tempfile,shutil
from pathlib import Path
from resource_selection import ROOT,book_decision,excluded

class SelectionTests(unittest.TestCase):
    def test_decisions_and_browser_parity(self):
        approved=json.loads((ROOT/'static/dawn-library/biblical-world/catalog.json').read_text())['items']
        cases=[(x,'approved') for x in approved]
        for title in ['巴勒斯坦、阿拉伯人民反击以色列侵略','巴勒斯坦游擊隊不斷襲擊以色列侵略軍']:
            cases.append(({'title':title,'rights':{'status':'public-domain'},'stage':'verified','source':{'url':'https://ws-export.wmcloud.org/?format=epub'},'kind':'book','admission':{'status':'approved'}},'excluded'))
        cases.extend([
            ({'title':'A press release about Bible printing','kind':'book'},'excluded'),
            ({'title':'An Extract out of Josephus’s Discourse','rights':{'status':'public-domain'}},'excluded'),
            ({'title':'A single article','resourceType':'article','admission':{'status':'approved'}},'excluded'),
            ({'title':'Unknown Complete Book','author':'Known Author','isbn':'1234567890','kind':'book','rights':{'status':'public-domain'},'admission':{'status':'approved'}},'hold'),
            ({'title':'Bible geography of ancient Israel and Palestine'},'hold'),
        ])
        flagged=copy.deepcopy(approved[0]);flagged['completeWork']=False;cases.append((flagged,'excluded'))
        flagged=copy.deepcopy(approved[0]);flagged['controversial']=True;cases.append((flagged,'excluded'))
        flagged=copy.deepcopy(approved[0]);flagged['topics']=['political-propaganda'];cases.append((flagged,'excluded'))
        changed=copy.deepcopy(approved[0]);changed['sources'][0]['url']='https://example.com/unreviewed';cases.append((changed,'hold'))
        changed=copy.deepcopy(approved[0]);changed['work']['title']='Unreviewed replacement';cases.append((changed,'hold'))
        for item,want in cases:self.assertEqual(book_decision(item)['status'],want,item)
        self.assertFalse(excluded({'title':'Bible geography of ancient Israel and Palestine'}))
        js="import {bookDecision} from './static/resources/resource-selection.mjs';let s='';for await(const c of process.stdin)s+=c;console.log(JSON.stringify(JSON.parse(s).map(bookDecision)));"
        results=json.loads(subprocess.check_output(['node','--input-type=module','-e',js],input=json.dumps([x for x,_ in cases]),text=True,cwd=ROOT))
        self.assertEqual([x['status'] for x in results],[want for _,want in cases])
    def test_real_promoters_cannot_publish_rights_only_records(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            for directory in ['scripts','data','static/dawn-library/biblical-world','dore-core/review/resource-selection','reports']:
                (root/directory).mkdir(parents=True,exist_ok=True)
            for name in ['resource_selection.py','promote_dawn_library_chinese_catalog.py','promote_dawn_library_english_catalog.py']:
                shutil.copy2(ROOT/'scripts'/name,root/'scripts'/name)
            for name in ['resource_selection_policy.json','resource_book_reviews.json']:
                shutil.copy2(ROOT/'data'/name,root/'data'/name)
            catalog=root/'static/dawn-library/biblical-world/catalog.json'
            catalog.write_text(json.dumps({'items':[]}))
            good={'sourceId':'3296','title':'The Confessions of St. Augustine','sourceUrl':'https://www.gutenberg.org/ebooks/3296','stage':'verified','rights':{'status':'public-domain'},'edition':{'gutenbergId':'3296'}}
            unknown={**good,'sourceId':'999999','title':'A Bible news report','sourceUrl':'https://www.gutenberg.org/ebooks/999999','edition':{'gutenbergId':'999999'}}
            queue=root/'dore-core/review/resource-selection'
            (queue/'english-resolver-results.json').write_text(json.dumps({'items':[unknown,good]}))
            bad={'title':'巴勒斯坦游击队不断袭击以色列侵略军','sourceUrl':'https://zh.wikisource.org/wiki/propaganda','stage':'verified','rights':{'status':'public-domain','provenanceRequired':True}}
            (queue/'chinese-resolver-results.json').write_text(json.dumps({'items':[bad]}))
            for name in ['promote_dawn_library_english_catalog.py','promote_dawn_library_chinese_catalog.py']:
                subprocess.run(['python3',str(root/'scripts'/name)],check=True,capture_output=True,text=True)
            actual=json.loads(catalog.read_text())['items']
            self.assertEqual([i['id'] for i in actual],['gutenberg-3296'])

    def test_private_manuscript_and_catalog_intake(self):
        js="""import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {selectedReferenceAllowed} from './static/resources/resource-selection.mjs';
import {createPersonalReferenceFromDawn,libraryLayers} from './static/multiwrite/library-model.mjs';
const good=JSON.parse(readFileSync('./static/dawn-library/biblical-world/catalog.json')).items[0];
const old={id:'withdrawn',work:{title:'巴勒斯坦、阿拉伯人民反击以色列侵略'},sources:[]};
assert.throws(()=>createPersonalReferenceFromDawn(old));
assert.equal(libraryLayers({dawn:[old,good]}).dawn.length,1);
assert.equal(selectedReferenceAllowed(createPersonalReferenceFromDawn(good)),true);
assert.equal(selectedReferenceAllowed({title:old.work.title,library:{intake:'dawn-reference'},identity:{work:old.work}}),false);
assert.equal(selectedReferenceAllowed({title:'My private draft',nodes:[]}),true);
"""
        subprocess.run(['node','--input-type=module','-e',js],check=True,cwd=ROOT)

if __name__=='__main__':unittest.main()
