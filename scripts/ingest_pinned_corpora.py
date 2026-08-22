#!/usr/bin/env python3
"""Run Doré ingestion against the complete pinned Protestant biblical corpora and emit OT/NT canonical inventories."""
from __future__ import annotations
import json
from pathlib import Path
from urllib.request import urlopen
from dore_core.readers.corpus_ingestion import ingest_morphgnt, ingest_oshb, assert_lossless
OSHB_SHA="3d15126fb1ef74867fc1434be1942e837932691f"; MORPHGNT_SHA="aaed91e57c8e4a8dc9a2383e129ca5e75fe6393d"; REPORT_PATH=Path("reports/DORÉ-CORPUS-READING-REPORT.json"); INV_DIR=Path("reports/inventories")
OT_TARGETS={"GEN":"Gen.xml","EXO":"Exod.xml","LEV":"Lev.xml","NUM":"Num.xml","DEU":"Deut.xml","JOS":"Josh.xml","JDG":"Judg.xml","RUT":"Ruth.xml","1SA":"1Sam.xml","2SA":"2Sam.xml","1KI":"1Kgs.xml","2KI":"2Kgs.xml","1CH":"1Chr.xml","2CH":"2Chr.xml","EZR":"Ezra.xml","NEH":"Neh.xml","EST":"Esth.xml","JOB":"Job.xml","PSA":"Ps.xml","PRO":"Prov.xml","ECC":"Eccl.xml","SNG":"Song.xml","ISA":"Isa.xml","JER":"Jer.xml","LAM":"Lam.xml","EZK":"Ezek.xml","DAN":"Dan.xml","HOS":"Hos.xml","JOL":"Joel.xml","AMO":"Amos.xml","OBA":"Obad.xml","JON":"Jonah.xml","MIC":"Mic.xml","NAM":"Nah.xml","HAB":"Hab.xml","ZEP":"Zeph.xml","HAG":"Hag.xml","ZEC":"Zech.xml","MAL":"Mal.xml"}
NT_TARGETS={"MAT":"61-Mt-morphgnt.txt","MRK":"62-Mk-morphgnt.txt","LUK":"63-Lk-morphgnt.txt","JHN":"64-Jn-morphgnt.txt","ACT":"65-Ac-morphgnt.txt","ROM":"66-Ro-morphgnt.txt","1CO":"67-1Co-morphgnt.txt","2CO":"68-2Co-morphgnt.txt","GAL":"69-Ga-morphgnt.txt","EPH":"70-Eph-morphgnt.txt","PHP":"71-Php-morphgnt.txt","COL":"72-Col-morphgnt.txt","1TH":"73-1Th-morphgnt.txt","2TH":"74-2Th-morphgnt.txt","1TI":"75-1Ti-morphgnt.txt","2TI":"76-2Ti-morphgnt.txt","TIT":"77-Tit-morphgnt.txt","PHM":"78-Phm-morphgnt.txt","HEB":"79-Heb-morphgnt.txt","JAS":"80-Jas-morphgnt.txt","1PE":"81-1Pe-morphgnt.txt","2PE":"82-2Pe-morphgnt.txt","1JN":"83-1Jn-morphgnt.txt","2JN":"84-2Jn-morphgnt.txt","3JN":"85-3Jn-morphgnt.txt","JUD":"86-Jud-morphgnt.txt","REV":"87-Re-morphgnt.txt"}
def fetch_text(url):
    with urlopen(url,timeout=60) as response: return response.read().decode("utf-8")
def write_inventory(path,witness_id,language,source_id,snapshot,refs):
    refs=sorted(set(refs)); books=sorted({r.split('.')[2] for r in refs}); payload={"schema":"dore.canonical-inventory.v0.1","witness_id":witness_id,"language":language,"edition":witness_id,"source_id":source_id,"snapshot":snapshot,"book_count":len(books),"book_ids":books,"canonical_ref_count":len(refs),"canonical_refs":refs}; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8"); return payload
def main():
    reports={}; total_tokens=total_warnings=total_failures=0; ot_refs=[]; nt_refs=[]
    try:
        for code,filename in OT_TARGETS.items():
            tokens,report=ingest_oshb(fetch_text(f"https://raw.githubusercontent.com/openscriptures/morphhb/{OSHB_SHA}/wlc/{filename}"),code); assert_lossless(report); ot_refs.extend(t.canonical_ref_id for t in tokens); total_tokens+=report.emitted_tokens; total_warnings+=report.warnings; total_failures+=report.failures; reports[code]={**report.to_dict(),"languages":sorted({t.language for t in tokens})}
        for code,filename in NT_TARGETS.items():
            tokens,report=ingest_morphgnt(fetch_text(f"https://raw.githubusercontent.com/morphgnt/sblgnt/{MORPHGNT_SHA}/{filename}").splitlines()); assert_lossless(report); nt_refs.extend(t.canonical_ref_id for t in tokens); total_tokens+=report.emitted_tokens; total_warnings+=report.warnings; total_failures+=report.failures; reports[code]={**report.to_dict(),"languages":sorted({t.language for t in tokens})}
        if len(reports)!=66: raise AssertionError(f"expected 66 books, read {len(reports)}")
        ot_inv=write_inventory(INV_DIR/"OSHB.json","witness.original.oshb","he+arc","openscriptures/morphhb",OSHB_SHA,ot_refs); nt_inv=write_inventory(INV_DIR/"MORPHGNT-SBLGNT.json","witness.original.morphgnt_sblgnt","grc","morphgnt/sblgnt",MORPHGNT_SHA,nt_refs)
        result={"status":"PASS","books_expected":66,"books_read":len(reports),"tokens_read":total_tokens,"warnings":total_warnings,"failures":total_failures,"silent_token_loss":0,"snapshots":{"oshb":OSHB_SHA,"morphgnt_sblgnt":MORPHGNT_SHA},"inventories":{"oshb":ot_inv["canonical_ref_count"],"morphgnt_sblgnt":nt_inv["canonical_ref_count"]},"reports":reports}
    except Exception as exc:
        result={"status":"FAIL","books_expected":66,"books_read":len(reports),"tokens_read":total_tokens,"warnings":total_warnings,"failures":total_failures+1,"error":f"{type(exc).__name__}: {exc}","snapshots":{"oshb":OSHB_SHA,"morphgnt_sblgnt":MORPHGNT_SHA},"reports":reports}; REPORT_PATH.parent.mkdir(parents=True,exist_ok=True); REPORT_PATH.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True),encoding="utf-8"); print(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)); raise
    REPORT_PATH.parent.mkdir(parents=True,exist_ok=True); REPORT_PATH.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True),encoding="utf-8"); print(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True))
if __name__=="__main__": main()
