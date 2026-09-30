#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

from dore_core.language.base import TextWitness
from dore_core.language.materialization import materialize_text
from dore_core.publication_adapters.gutenberg import adapt_gutenberg_work
from dore_core.publication_adapters.gutenberg_loader import load_gutenberg_text
from dore_core.publication_materialization import bind_materialized_text

ROOT=Path(__file__).resolve().parents[1]
INDEX=ROOT/'static/dawn-library/canonical-index.json'

def main()->int:
 data=json.loads(INDEX.read_text(encoding='utf-8'))
 works=data.get('works') or {}
 candidates=[w for w in works.values() if (w.get('authorityIds') or {}).get('projectGutenberg') and str(w.get('readingPointer') or '').startswith('dawn://reading/')]
 if not candidates:raise SystemExit('no canonical Gutenberg reading candidate')
 work=sorted(candidates,key=lambda w:str(w.get('workId')))[0]
 publication=adapt_gutenberg_work(work)
 mapping_source=publication.source
 language=(work.get('languages') or ['en'])[0]
 witness=TextWitness(witness_id=str(mapping_source['witnessId']),language=str(language or 'en'),edition='project-gutenberg',source_id=str((work.get('authorityIds') or {}).get('projectGutenberg')),snapshot='remote-live',license_id='project-gutenberg-license',metadata={'workId':work['workId']})
 from dore_core.language.source_mapping import map_public_domain_source
 mapping=map_public_domain_source(work)
 if mapping is None:raise SystemExit('candidate lost Gutenberg source mapping')
 materialized=materialize_text(witness=witness,policy=mapping.policy,remote_loader=load_gutenberg_text)
 bound,resource=bind_materialized_text(publication,materialized)
 chars=len(resource.body);words=len(resource.body.split())
 if chars<1000:raise SystemExit(f'Gutenberg body too small: {chars}')
 manifest=bound.to_manifest()
 if not manifest.get('readingOrder') or manifest['readingOrder'][0].get('href')!=resource.href:raise SystemExit('publication manifest/resource mismatch')
 print(json.dumps({'status':'PASS','workId':work['workId'],'title':work.get('title'),'gutenbergId':(work.get('authorityIds') or {}).get('projectGutenberg'),'characters':chars,'words':words,'persisted':resource.persisted,'resource':resource.href},ensure_ascii=False))
 return 0
if __name__=='__main__':raise SystemExit(main())
