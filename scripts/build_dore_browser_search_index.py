#!/usr/bin/env python3
"""Build the public, static Doré Bible Search index from pinned open witnesses.

The browser artifact contains verse-level WEBU/CUV text plus compact original-
language lemma and morphology inverted indexes. It contains no restricted Bible
corpora and preserves source/snapshot metadata for every layer.
"""
from __future__ import annotations
import json, subprocess
from collections import defaultdict
from pathlib import Path
from urllib.request import urlopen

from dore_core.language.base import TextWitness
from dore_core.language.adapters.verse_list_json import VerseListJSONAdapter
from dore_core.language.adapters.midvash_book_json import MidvashBookJSONAdapter
from dore_core.readers.corpus_ingestion import ingest_morphgnt, ingest_oshb, assert_lossless

WEBU_REPO='https://github.com/ringletech/webu-open-bible.git'
WEBU_SHA='44ce9156b77649adf11c0bbcee89c1d80e2c1f1c'
CUV_REPO='https://github.com/midvash/bible-data.git'
CUV_SHA='d9fe1779447717bbfcb578e505b893125cad581c'
OSHB_SHA='3d15126fb1ef74867fc1434be1942e837932691f'
MORPHGNT_SHA='aaed91e57c8e4a8dc9a2383e129ca5e75fe6393d'
OUT=Path('static/dore/search-index.json')
CACHE=Path('.cache')

OT_TARGETS={"GEN":"Gen.xml","EXO":"Exod.xml","LEV":"Lev.xml","NUM":"Num.xml","DEU":"Deut.xml","JOS":"Josh.xml","JDG":"Judg.xml","RUT":"Ruth.xml","1SA":"1Sam.xml","2SA":"2Sam.xml","1KI":"1Kgs.xml","2KI":"2Kgs.xml","1CH":"1Chr.xml","2CH":"2Chr.xml","EZR":"Ezra.xml","NEH":"Neh.xml","EST":"Esth.xml","JOB":"Job.xml","PSA":"Ps.xml","PRO":"Prov.xml","ECC":"Eccl.xml","SNG":"Song.xml","ISA":"Isa.xml","JER":"Jer.xml","LAM":"Lam.xml","EZK":"Ezek.xml","DAN":"Dan.xml","HOS":"Hos.xml","JOL":"Joel.xml","AMO":"Amos.xml","OBA":"Obad.xml","JON":"Jonah.xml","MIC":"Mic.xml","NAM":"Nah.xml","HAB":"Hab.xml","ZEP":"Zeph.xml","HAG":"Hag.xml","ZEC":"Zech.xml","MAL":"Mal.xml"}
NT_TARGETS={"MAT":"61-Mt-morphgnt.txt","MRK":"62-Mk-morphgnt.txt","LUK":"63-Lk-morphgnt.txt","JHN":"64-Jn-morphgnt.txt","ACT":"65-Ac-morphgnt.txt","ROM":"66-Ro-morphgnt.txt","1CO":"67-1Co-morphgnt.txt","2CO":"68-2Co-morphgnt.txt","GAL":"69-Ga-morphgnt.txt","EPH":"70-Eph-morphgnt.txt","PHP":"71-Php-morphgnt.txt","COL":"72-Col-morphgnt.txt","1TH":"73-1Th-morphgnt.txt","2TH":"74-2Th-morphgnt.txt","1TI":"75-1Ti-morphgnt.txt","2TI":"76-2Ti-morphgnt.txt","TIT":"77-Tit-morphgnt.txt","PHM":"78-Phm-morphgnt.txt","HEB":"79-Heb-morphgnt.txt","JAS":"80-Jas-morphgnt.txt","1PE":"81-1Pe-morphgnt.txt","2PE":"82-2Pe-morphgnt.txt","1JN":"83-1Jn-morphgnt.txt","2JN":"84-2Jn-morphgnt.txt","3JN":"85-3Jn-morphgnt.txt","JUD":"86-Jud-morphgnt.txt","REV":"87-Re-morphgnt.txt"}

BOOK_NAMES={
'GEN':['創世記','Genesis'],'EXO':['出埃及記','Exodus'],'LEV':['利未記','Leviticus'],'NUM':['民數記','Numbers'],'DEU':['申命記','Deuteronomy'],'JOS':['約書亞記','Joshua'],'JDG':['士師記','Judges'],'RUT':['路得記','Ruth'],'1SA':['撒母耳記上','1 Samuel'],'2SA':['撒母耳記下','2 Samuel'],'1KI':['列王紀上','1 Kings'],'2KI':['列王紀下','2 Kings'],'1CH':['歷代志上','1 Chronicles'],'2CH':['歷代志下','2 Chronicles'],'EZR':['以斯拉記','Ezra'],'NEH':['尼希米記','Nehemiah'],'EST':['以斯帖記','Esther'],'JOB':['約伯記','Job'],'PSA':['詩篇','Psalms'],'PRO':['箴言','Proverbs'],'ECC':['傳道書','Ecclesiastes'],'SNG':['雅歌','Song of Songs'],'ISA':['以賽亞書','Isaiah'],'JER':['耶利米書','Jeremiah'],'LAM':['耶利米哀歌','Lamentations'],'EZK':['以西結書','Ezekiel'],'DAN':['但以理書','Daniel'],'HOS':['何西阿書','Hosea'],'JOL':['約珥書','Joel'],'AMO':['阿摩司書','Amos'],'OBA':['俄巴底亞書','Obadiah'],'JON':['約拿書','Jonah'],'MIC':['彌迦書','Micah'],'NAM':['那鴻書','Nahum'],'HAB':['哈巴谷書','Habakkuk'],'ZEP':['西番雅書','Zephaniah'],'HAG':['哈該書','Haggai'],'ZEC':['撒迦利亞書','Zechariah'],'MAL':['瑪拉基書','Malachi'],'MAT':['馬太福音','Matthew'],'MRK':['馬可福音','Mark'],'LUK':['路加福音','Luke'],'JHN':['約翰福音','John'],'ACT':['使徒行傳','Acts'],'ROM':['羅馬書','Romans'],'1CO':['哥林多前書','1 Corinthians'],'2CO':['哥林多後書','2 Corinthians'],'GAL':['加拉太書','Galatians'],'EPH':['以弗所書','Ephesians'],'PHP':['腓立比書','Philippians'],'COL':['歌羅西書','Colossians'],'1TH':['帖撒羅尼迦前書','1 Thessalonians'],'2TH':['帖撒羅尼迦後書','2 Thessalonians'],'1TI':['提摩太前書','1 Timothy'],'2TI':['提摩太後書','2 Timothy'],'TIT':['提多書','Titus'],'PHM':['腓利門書','Philemon'],'HEB':['希伯來書','Hebrews'],'JAS':['雅各書','James'],'1PE':['彼得前書','1 Peter'],'2PE':['彼得後書','2 Peter'],'1JN':['約翰一書','1 John'],'2JN':['約翰二書','2 John'],'3JN':['約翰三書','3 John'],'JUD':['猶大書','Jude'],'REV':['啟示錄','Revelation']}

def clone(repo: str, sha: str, dest: Path) -> None:
    if not dest.exists():
        dest.parent.mkdir(parents=True,exist_ok=True)
        subprocess.run(['git','clone','--filter=blob:none',repo,str(dest)],check=True)
    subprocess.run(['git','-C',str(dest),'fetch','--depth','1','origin',sha],check=True)
    subprocess.run(['git','-C',str(dest),'checkout','--detach',sha],check=True)

def fetch(url: str) -> str:
    with urlopen(url,timeout=90) as r:return r.read().decode('utf-8')

def verse_text(units):
    grouped=defaultdict(list); languages={}
    for u in units:
        if u.canonical_ref_id:
            grouped[u.canonical_ref_id].append((u.order,u.surface))
            languages.setdefault(u.canonical_ref_id,u.language)
    out={}
    for ref,parts in grouped.items():
        ordered=[x[1] for x in sorted(parts)]
        out[ref]=(' ' if languages.get(ref,'').startswith('en') else '').join(ordered)
    return out

def compact_refs(refs): return sorted(set(refs))

def main():
    webu_dir=CACHE/'webu-open-bible'; cuv_dir=CACHE/'midvash-bible-data'
    clone(WEBU_REPO,WEBU_SHA,webu_dir); clone(CUV_REPO,CUV_SHA,cuv_dir)
    webu_source=json.loads((webu_dir/'json/complete-bible.json').read_text(encoding='utf-8'))
    webu_w=TextWitness('witness.english.webu','en','WEBU','ringletech/webu-open-bible',WEBU_SHA,'CC0-1.0')
    webu_units=list(VerseListJSONAdapter('en').ingest(webu_source,webu_w)); webu=verse_text(webu_units)
    cuv_w=TextWitness('witness.chinese.cuv.traditional.1919','zh-Hant','CUV Traditional','midvash/bible-data',CUV_SHA,'public-domain')
    cuv_adapter=MidvashBookJSONAdapter(language='zh-Hant'); cuv_units=[]
    for p in sorted((cuv_dir/'versions/zh/cuv/books').glob('*.json')):
        cuv_units.extend(cuv_adapter.ingest_book(json.loads(p.read_text(encoding='utf-8')),cuv_w))
    cuv=verse_text(cuv_units)

    lemma=defaultdict(list); morph=defaultdict(list); original_surface=defaultdict(list)
    for code,filename in OT_TARGETS.items():
        tokens,report=ingest_oshb(fetch(f'https://raw.githubusercontent.com/openscriptures/morphhb/{OSHB_SHA}/wlc/{filename}'),code); assert_lossless(report)
        for t in tokens:
            original_surface[t.surface].append(t.canonical_ref_id)
            for a in t.analyses:
                if a.type=='lemma': lemma[a.value].append(t.canonical_ref_id)
                elif a.type=='morphology': morph[a.value].append(t.canonical_ref_id)
    for code,filename in NT_TARGETS.items():
        tokens,report=ingest_morphgnt(fetch(f'https://raw.githubusercontent.com/morphgnt/sblgnt/{MORPHGNT_SHA}/{filename}').splitlines()); assert_lossless(report)
        for t in tokens:
            original_surface[t.surface].append(t.canonical_ref_id)
            for a in t.analyses:
                if a.type=='lemma': lemma[a.value].append(t.canonical_ref_id)
                elif a.type=='morphology': morph[a.value].append(t.canonical_ref_id)

    refs=sorted(set(webu)|set(cuv)); verses=[]
    for ref in refs:
        parts=ref.split('.'); book,ch,v=parts[2],int(parts[3]),int(parts[4]); names=BOOK_NAMES.get(book,[book,book])
        verses.append({'r':ref,'b':book,'c':ch,'v':v,'z':cuv.get(ref,''),'e':webu.get(ref,''),'n':names})
    payload={
      'schema':'dore.browser-search-index.v0.1',
      'sources':{
        'cuv':{'witness':'CUV Traditional 1919','snapshot':CUV_SHA,'license':'public-domain'},
        'webu':{'witness':'World English Bible Updated','snapshot':WEBU_SHA,'license':'CC0-1.0'},
        'oshb':{'witness':'OSHB/WLC','snapshot':OSHB_SHA},
        'morphgnt':{'witness':'MorphGNT/SBLGNT','snapshot':MORPHGNT_SHA}},
      'verses':verses,
      'lemma':{k:compact_refs(v) for k,v in sorted(lemma.items())},
      'morphology':{k:compact_refs(v) for k,v in sorted(morph.items())},
      'original_surface':{k:compact_refs(v) for k,v in sorted(original_surface.items())}}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(payload,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    print(json.dumps({'status':'PASS','verses':len(verses),'lemmas':len(payload['lemma']),'morphologies':len(payload['morphology']),'surfaces':len(payload['original_surface']),'bytes':OUT.stat().st_size},ensure_ascii=False))
if __name__=='__main__':main()
