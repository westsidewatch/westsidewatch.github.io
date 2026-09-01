#!/usr/bin/env python3
"""Import the current main-site Journal once into an editable Doré Design page.

Hugo is an import source only. Runtime rendering reads the imported design package
and workspace nodes; it does not mirror or fetch the main site.
"""
from html.parser import HTMLParser
from pathlib import Path
import datetime,json,os,shutil,subprocess,tempfile

ROOT=Path(__file__).resolve().parent.parent
DATA=Path(os.environ.get('DORE_DESIGN_DATA',Path.home()/'.dore/design')).expanduser()
WS=DATA/'westside-watch.workspace.json'
HIST=DATA/'workspace-history'
PACKAGE=DATA/'imports/journal-vol-00'
PAGE_ID='journal-vol-00'
RENDERER='journal-imported-dom-v1'
SKIP={'head','title','style','script','svg','noscript','template'}
ELIGIBLE={'div','nav','p','h1','h2','h3','h4','h5','h6','span','em','strong','cite','a','b','i','li','small','label','button','blockquote'}

def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()

def atomic_obj(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix(path.suffix+'.tmp')
    tmp.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
    tmp.replace(path)

class Binder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.out=[];self.stack=[];self.nodes=[];self.body=False;self.counter=0
    def handle_decl(self,decl):self.out.append('<!'+decl+'>')
    def handle_comment(self,data):self.out.append('<!--'+data+'-->')
    def handle_pi(self,data):self.out.append('<?'+data+'>')
    def handle_starttag(self,tag,attrs):
        self.out.append(self.get_starttag_text());self.stack.append(tag)
        if tag=='body':self.body=True
    def handle_startendtag(self,tag,attrs):self.out.append(self.get_starttag_text())
    def handle_endtag(self,tag):
        self.out.append(f'</{tag}>')
        if self.stack:
            if self.stack[-1]==tag:self.stack.pop()
            elif tag in self.stack:self.stack=self.stack[:len(self.stack)-1-self.stack[::-1].index(tag)]
        if tag=='body':self.body=False
    def handle_entityref(self,name):self.out.append('&'+name+';')
    def handle_charref(self,name):self.out.append('&#'+name+';')
    def handle_data(self,data):
        top=self.stack[-1] if self.stack else None
        if not self.body or not data.strip() or any(t in SKIP for t in self.stack) or top not in ELIGIBLE:
            self.out.append(data);return
        self.counter+=1;nid=f'journal-text-{self.counter:04d}'
        self.nodes.append({'id':nid,'type':'text','text':data,'x':0,'y':0,'w':1,'size':1,'role':'dom-text'})
        self.out.append(f'<span class="dore-journal-bound" data-node-id="{nid}" data-field="text">{data}</span>')

def build_import():
    hugo=shutil.which('hugo')
    if not hugo:raise SystemExit('hugo_not_found')
    tmp=Path(tempfile.mkdtemp(prefix='dore-journal-import-'))
    try:
        proc=subprocess.run([hugo,'--destination',str(tmp),'--cleanDestinationDir'],cwd=str(ROOT),capture_output=True,text=True,timeout=120)
        if proc.returncode!=0:raise SystemExit('hugo_build_failed:'+proc.stderr[-4000:])
        source=tmp/'index.html'
        if not source.exists():raise SystemExit('hugo_index_missing')
        html=source.read_text(encoding='utf-8')
        parser=Binder();parser.feed(html);parser.close()
        bound=''.join(parser.out).replace('href="/#','href="/journal/#').replace("href='/#","href='/journal/#")
        if len(parser.nodes)<20:raise SystemExit(f'journal_import_too_small:{len(parser.nodes)}')
        if PACKAGE.exists():shutil.rmtree(PACKAGE)
        shutil.copytree(tmp,PACKAGE)
        (PACKAGE/'index.html').write_text(bound,encoding='utf-8')
        return parser.nodes
    finally:
        shutil.rmtree(tmp,ignore_errors=True)

def main():
    if not WS.exists():raise SystemExit('workspace_not_found')
    w=json.loads(WS.read_text(encoding='utf-8'))
    existing=next((p for p in w.get('pages',[]) if p.get('id')==PAGE_ID),None)
    if existing and (PACKAGE/'index.html').exists():
        print(json.dumps({'ok':True,'code':'EDITABLE_JOURNAL_ALREADY_IMPORTED','page_id':PAGE_ID,'node_count':len(existing.get('nodes',[])),'revision':w.get('revision')},ensure_ascii=False));return
    nodes=build_import()
    if existing:
        old={n.get('id'):n for n in existing.get('nodes',[])}
        for n in nodes:
            if n['id'] in old:n['text']=old[n['id']].get('text',n['text'])
        page=dict(existing);page.update({'id':PAGE_ID,'name':'Journal / Vol.00','renderer':RENDERER,'source_import':'main-site-hugo-root-index','canvas':{'w':1440,'h':12000},'nodes':nodes})
    else:
        page={'id':PAGE_ID,'name':'Journal / Vol.00','renderer':RENDERER,'source_import':'main-site-hugo-root-index','canvas':{'w':1440,'h':12000},'nodes':nodes}
    pages=w.setdefault('pages',[]);idx=next((i for i,p in enumerate(pages) if p.get('id')==PAGE_ID),None)
    if idx is None:
        home_idx=next((i for i,p in enumerate(pages) if p.get('id')=='homepage'),-1);pages.insert(home_idx+1,page)
    else:pages[idx]=page
    HIST.mkdir(parents=True,exist_ok=True);stamp=datetime.datetime.now().strftime('%Y%m%dT%H%M%S');shutil.copy2(WS,HIST/f'westside-watch.before-journal-import-{stamp}.json')
    w['revision']=int(w.get('revision',0))+1;w['updated_at']=now();w['multi_page_wysiwyg']=True
    atomic_obj(WS,w)
    print(json.dumps({'ok':True,'code':'EDITABLE_JOURNAL_IMPORT_PASS','page_id':PAGE_ID,'node_count':len(nodes),'revision':w['revision'],'package':str(PACKAGE)},ensure_ascii=False))

if __name__=='__main__':main()
