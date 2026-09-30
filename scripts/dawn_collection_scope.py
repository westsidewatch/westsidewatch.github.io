#!/usr/bin/env python3
"""Dawn Library collection-scope gate.

Hard policy: public religious holdings are Christian/Biblical. Jewish/Judaism
materials are admissible as research. Other-religion devotional/doctrinal/
scriptural/practice holdings are excluded before public surfaces are built.
"""
from __future__ import annotations
import re
from typing import Any

JEWISH_RESEARCH=re.compile(r"\b(judaism|jewish|jews?|hebrew bible|tanakh|talmud|midrash|rabbinic|rabbinical|second temple|dead sea scrolls?|qمران|qumran|septuagint|masoretic)\b",re.I)
CHRISTIAN=re.compile(r"\b(christian|christianity|bible|biblical|old testament|new testament|gospel|jesus|christ|church|theology|sermon|pastoral|ministry|mission|evangelical|catholic|orthodox|protestant|reformation|patristic|apostl|pentecost|baptis|luther|calvin|anglican|methodist|presbyterian)\b",re.I)
OTHER_RELIGION=re.compile(r"\b(buddh(?:a|ism|ist)|dharma|dalai lama|rinpoche|tibetan buddh|zen buddh|hindu(?:ism)?|vedas?|upanishad|bhagavad\s*gita|krishna|vaishnav|shaiv|islam(?:ic)?|muslim|qur['’]?an|koran|muhammad|sufi(?:sm)?|sikh(?:ism)?|guru granth|jain(?:ism)?|shinto|tao(?:ism|ist)|dao(?:ism|ist)|confucian(?:ism)?|zoroastr|bah[aá][’']?i|scientology|neo[- ]?pagan|wicca)\b",re.I)
RELIGION_MARKER=re.compile(r"\b(religion|religious|faith|spiritual|scripture|sacred|worship|prayer|devotion|doctrine|theology|god|gods|temple|monk|mystic)\b",re.I)


def _flatten(value:Any)->list[str]:
    if value is None:return []
    if isinstance(value,str):return [value]
    if isinstance(value,(list,tuple,set)):
        out=[]
        for v in value:out.extend(_flatten(v))
        return out
    if isinstance(value,dict):
        out=[]
        for k,v in value.items():out.append(str(k));out.extend(_flatten(v))
        return out
    return [str(value)]


def text_blob(item:dict)->str:
    keys=('title','subtitle','authors','author','subjects','subject','description','topics','tags','categories','category','series')
    return ' '.join(x for key in keys for x in _flatten(item.get(key)) if x)


def classify(item:dict)->dict:
    text=text_blob(item)
    if JEWISH_RESEARCH.search(text):
        return {'admit':True,'scope':'jewish-research','reason':'research-exception'}
    if OTHER_RELIGION.search(text):
        return {'admit':False,'scope':'excluded','reason':'other-religion'}
    if CHRISTIAN.search(text):
        return {'admit':True,'scope':'christian-biblical','reason':'christian-biblical'}
    # Secular/reference material is not rejected merely for lacking Christian terms.
    # The hard prohibition is other-religion holdings, not general scholarship.
    if not RELIGION_MARKER.search(text):
        return {'admit':True,'scope':'general-research','reason':'non-religious'}
    return {'admit':False,'scope':'excluded','reason':'religious-scope-unresolved'}


def filter_items(items:list[dict])->tuple[list[dict],list[dict]]:
    admitted=[];excluded=[]
    for item in items:
        verdict=classify(item)
        row=dict(item);row['collectionScope']=verdict['scope']
        if verdict['admit']:admitted.append(row)
        else:excluded.append({'workId':item.get('workId') or item.get('id'),'title':item.get('title'),'reason':verdict['reason']})
    return admitted,excluded
