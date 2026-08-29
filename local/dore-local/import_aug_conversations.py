#!/usr/bin/env python3
import argparse, hashlib, json, sqlite3, zipfile
from datetime import datetime, timezone
from pathlib import Path

def iso(ts):
    if ts is None: return None
    try: return datetime.fromtimestamp(float(ts), timezone.utc).isoformat()
    except Exception: return str(ts)

def text_of(content):
    if not isinstance(content, dict): return ''
    parts=content.get('parts') or []
    out=[]
    for p in parts:
        if isinstance(p,str): out.append(p)
        elif isinstance(p,dict):
            if isinstance(p.get('text'),str): out.append(p['text'])
            else: out.append(json.dumps(p,ensure_ascii=False,separators=(',',':')))
    return '\n'.join(x for x in out if x).strip()

def load_conversations(src):
    p=Path(src)
    if p.is_dir():
        for f in sorted(p.glob('conversations-*.json')):
            for c in json.loads(f.read_text(encoding='utf-8')): yield c, f.name
    else:
        with zipfile.ZipFile(p) as z:
            for name in sorted(n for n in z.namelist() if Path(n).name.startswith('conversations-') and n.endswith('.json')):
                for c in json.loads(z.read(name)): yield c, name

def ensure(c):
    c.executescript('''
    CREATE TABLE IF NOT EXISTS aug_import_runs(id TEXT PRIMARY KEY, source TEXT NOT NULL, started_at TEXT NOT NULL, finished_at TEXT, conversations INTEGER DEFAULT 0, raw_messages INTEGER DEFAULT 0, exchange_messages INTEGER DEFAULT 0);
    CREATE TABLE IF NOT EXISTS aug_conversations(conversation_id TEXT PRIMARY KEY,title TEXT,create_time TEXT,update_time TEXT,current_node TEXT,default_model_slug TEXT,source_file TEXT,raw_json TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS aug_raw_messages(message_id TEXT NOT NULL,conversation_id TEXT NOT NULL,parent_id TEXT,role TEXT,author_name TEXT,content_type TEXT,content_text TEXT,create_time TEXT,raw_json TEXT NOT NULL,PRIMARY KEY(conversation_id,message_id));
    CREATE INDEX IF NOT EXISTS idx_aug_raw_conv_time ON aug_raw_messages(conversation_id,create_time);
    CREATE INDEX IF NOT EXISTS idx_aug_raw_role ON aug_raw_messages(role);
    ''')

def main():
    ap=argparse.ArgumentParser(description='Loss-preserving AUG/ChatGPT conversation import for Doré')
    ap.add_argument('source', help='AUG export zip or extracted directory')
    ap.add_argument('--db', default=str(Path.home()/'.dore/data/dore.sqlite3'))
    ap.add_argument('--archive', default=str(Path.home()/'.dore/archive/aug-conversations'))
    args=ap.parse_args(); dbp=Path(args.db); dbp.parent.mkdir(parents=True,exist_ok=True); arc=Path(args.archive); arc.mkdir(parents=True,exist_ok=True)
    run_id='aug-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'); started=datetime.now(timezone.utc).isoformat()
    con=sqlite3.connect(dbp); ensure(con)
    con.execute('INSERT INTO aug_import_runs(id,source,started_at) VALUES(?,?,?)',(run_id,str(Path(args.source).resolve()),started))
    nc=nr=ne=0
    for conv,source_file in load_conversations(args.source):
        cid=str(conv.get('conversation_id') or conv.get('id')); title=conv.get('title')
        con.execute('''INSERT OR REPLACE INTO aug_conversations(conversation_id,title,create_time,update_time,current_node,default_model_slug,source_file,raw_json) VALUES(?,?,?,?,?,?,?,?)''',(cid,title,iso(conv.get('create_time')),iso(conv.get('update_time')),conv.get('current_node'),conv.get('default_model_slug'),source_file,json.dumps(conv,ensure_ascii=False,separators=(',',':'))))
        for node_id,node in (conv.get('mapping') or {}).items():
            msg=(node or {}).get('message')
            if not msg: continue
            mid=str(msg.get('id') or node_id); author=msg.get('author') or {}; role=author.get('role'); content=msg.get('content') or {}; txt=text_of(content)
            con.execute('''INSERT OR REPLACE INTO aug_raw_messages(message_id,conversation_id,parent_id,role,author_name,content_type,content_text,create_time,raw_json) VALUES(?,?,?,?,?,?,?,?,?)''',(mid,cid,(node or {}).get('parent'),role,author.get('name'),content.get('content_type'),txt,iso(msg.get('create_time')),json.dumps({'node':node,'message':msg},ensure_ascii=False,separators=(',',':'))))
            nr+=1
            if role in {'user','assistant'} and txt:
                created=iso(msg.get('create_time')) or iso(conv.get('create_time')) or started
                h=hashlib.sha256(txt.encode()).hexdigest(); key=f'aug-conversations/{cid}/{mid}.json'
                payload={'schema':'dore.imported-aug-message.v1','id':mid,'conversation_id':cid,'project_id':'aug-history','role':role,'content':txt,'created_at':created,'source':'aug-export','source_message_id':mid,'source_parent_id':(node or {}).get('parent'),'source_conversation_title':title,'source_file':source_file}
                out=arc/cid/f'{mid}.json'; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(payload,ensure_ascii=False),encoding='utf-8')
                try:
                    con.execute('INSERT OR IGNORE INTO dore_conversations(id,project_id,actor_id,mode,title,created_at,updated_at) VALUES(?,?,?,?,?,?,?)',(cid,'aug-history','aug-import','IMPORTED',title,iso(conv.get('create_time')) or started,iso(conv.get('update_time')) or started))
                    con.execute('INSERT OR IGNORE INTO dore_messages(id,conversation_id,project_id,actor_id,role,content,content_sha256,archive_key,created_at) VALUES(?,?,?,?,?,?,?,?,?)',(mid,cid,'aug-history','aug-import',role,txt,h,key,created))
                    ne+=1
                except sqlite3.OperationalError as e:
                    if 'no such table' not in str(e): raise
        nc+=1
        if nc%25==0: con.commit()
    finished=datetime.now(timezone.utc).isoformat(); con.execute('UPDATE aug_import_runs SET finished_at=?,conversations=?,raw_messages=?,exchange_messages=? WHERE id=?',(finished,nc,nr,ne,run_id)); con.commit()
    report={'ok':True,'run_id':run_id,'source':str(Path(args.source).resolve()),'conversations':nc,'raw_messages':nr,'exchange_messages_exposed_to_dore':ne,'archive':str(arc),'db':str(dbp),'finished_at':finished}
    (arc/f'import-report-{run_id}.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8'); print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
