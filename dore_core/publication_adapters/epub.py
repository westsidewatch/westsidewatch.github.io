"""EPUB container -> Readium-shaped DawnPublication.

Uses EPUB's container.xml, OPF spine/manifest, and EPUB3 navigation document.
No provider-specific filenames are assumed.
"""
from __future__ import annotations

from io import BytesIO
from pathlib import PurePosixPath
from zipfile import ZipFile, BadZipFile
import xml.etree.ElementTree as ET

from dore_core.publication import DawnPublication, PublicationLink

CONTAINER_NS="urn:oasis:names:tc:opendocument:xmlns:container"
OPF_NS="http://www.idpf.org/2007/opf"
XHTML_NS="http://www.w3.org/1999/xhtml"
EPUB_NS="http://www.idpf.org/2007/ops"

def _join(base:str,href:str)->str:
 return str(PurePosixPath(base).parent.joinpath(href))

def _package_path(z:ZipFile)->str:
 root=ET.fromstring(z.read('META-INF/container.xml'))
 node=root.find(f'.//{{{CONTAINER_NS}}}rootfile')
 if node is None or not node.get('full-path'):raise ValueError('EPUB container has no package document')
 return node.get('full-path') or ''

def _text(node:ET.Element|None)->str:
 return ''.join(node.itertext()).strip() if node is not None else ''

def publication_from_epub(payload:bytes,*,identifier:str,source:dict|None=None)->DawnPublication:
 try:z=ZipFile(BytesIO(payload))
 except BadZipFile as exc:raise ValueError('invalid EPUB ZIP container') from exc
 with z:
  package_path=_package_path(z);opf=ET.fromstring(z.read(package_path))
  manifest={n.get('id'):{'href':n.get('href') or '','type':n.get('media-type') or 'application/xhtml+xml','properties':n.get('properties') or ''} for n in opf.findall(f'.//{{{OPF_NS}}}manifest/{{{OPF_NS}}}item') if n.get('id')}
  metadata=opf.find(f'{{{OPF_NS}}}metadata')
  title='';authors=[];languages=[]
  if metadata is not None:
   for child in list(metadata):
    tag=child.tag.rsplit('}',1)[-1];value=_text(child)
    if tag=='title' and value and not title:title=value
    elif tag=='creator' and value:authors.append(value)
    elif tag=='language' and value:languages.append(value)
  if not title:title=identifier
  reading=[]
  for itemref in opf.findall(f'.//{{{OPF_NS}}}spine/{{{OPF_NS}}}itemref'):
   item=manifest.get(itemref.get('idref') or '')
   if not item or not item['href']:continue
   reading.append(PublicationLink(href=f"dawn://publication/{identifier}/epub/{_join(package_path,item['href'])}",type=item['type'],language=languages[0] if languages else None))
  if not reading:raise ValueError('EPUB spine has no readable resources')
  toc=[]
  nav_item=next((v for v in manifest.values() if 'nav' in v['properties'].split()),None)
  if nav_item and nav_item['href']:
   nav_path=_join(package_path,nav_item['href'])
   nav=ET.fromstring(z.read(nav_path))
   for section in nav.findall(f'.//{{{XHTML_NS}}}nav'):
    nav_type=section.get(f'{{{EPUB_NS}}}type') or section.get('type') or ''
    if 'toc' not in nav_type.split():continue
    for anchor in section.findall(f'.//{{{XHTML_NS}}}a'):
     href=anchor.get('href') or '';label=_text(anchor)
     if href:toc.append(PublicationLink(href=f"dawn://publication/{identifier}/epub/{_join(nav_path,href)}",type='application/xhtml+xml',title=label or None,language=languages[0] if languages else None))
    break
  resources=[]
  spine_hrefs={link.href.rsplit('/epub/',1)[-1] for link in reading}
  for item in manifest.values():
   if not item['href']:continue
   path=_join(package_path,item['href'])
   if path in spine_hrefs:continue
   resources.append(PublicationLink(href=f"dawn://publication/{identifier}/epub/{path}",type=item['type']))
  return DawnPublication(identifier=identifier,title=title,authors=tuple(dict.fromkeys(authors)),languages=tuple(dict.fromkeys(languages)),reading_order=tuple(reading),resources=tuple(resources),toc=tuple(toc),source=dict(source or {}))
