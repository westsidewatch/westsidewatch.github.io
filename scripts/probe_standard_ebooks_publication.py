#!/usr/bin/env python3
from __future__ import annotations
import json

from dore_core.publication_adapters.standard_ebooks_opds import find_standard_ebooks_epub, load_standard_ebooks_epub
from dore_core.publication_adapters.epub import publication_from_epub

# Stable public-domain title used only as an end-to-end transport/parser probe.
IDENTIFIER='jane-austen/pride-and-prejudice'
WORK_ID='probe:standard-ebooks:jane-austen/pride-and-prejudice'

def main()->int:
 acquisition=find_standard_ebooks_epub(IDENTIFIER)
 payload=load_standard_ebooks_epub(acquisition)
 publication=publication_from_epub(payload,identifier=WORK_ID,source={'provider':'standard-ebooks','identifier':IDENTIFIER,'acquisitionUrl':acquisition.epub_url})
 manifest=publication.to_manifest()
 reading=manifest.get('readingOrder') or []
 toc=manifest.get('toc') or []
 resources=manifest.get('resources') or []
 if not reading:raise SystemExit('Standard Ebooks publication has empty readingOrder')
 if not toc:raise SystemExit('Standard Ebooks publication has empty TOC')
 if len(payload)<10000:raise SystemExit(f'EPUB payload unexpectedly small: {len(payload)}')
 print(json.dumps({'status':'PASS','identifier':IDENTIFIER,'title':publication.title,'epubBytes':len(payload),'readingOrder':len(reading),'toc':len(toc),'resources':len(resources),'firstReadingHref':reading[0]['href']},ensure_ascii=False))
 return 0
if __name__=='__main__':raise SystemExit(main())
