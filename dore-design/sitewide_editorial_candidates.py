#!/usr/bin/env python3
"""Read-only sitewide candidate ingestion for the Visual Editorial Director.

Thin adapters normalize existing repository content into ved.Candidate. This is
not a CMS and never writes source content. Missing sources remain visible in
`diagnostics`; they are not replaced with fabricated editorial specimens.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import re
from typing import Iterable

import visual_editorial_director as ved

ROOT = Path(__file__).resolve().parent.parent

@dataclass(frozen=True)
class PoolResult:
    candidates: list[ved.Candidate]
    provenance: dict[str, dict]
    diagnostics: dict[str, dict]


def _read_json(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def _scalar(value: str):
    v=value.strip()
    if len(v)>=2 and v[0]==v[-1] and v[0] in {'"', "'"}:
        return v[1:-1]
    if re.fullmatch(r"-?\d+",v):
        return int(v)
    return v


def _frontmatter(path: Path) -> dict:
    text=path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end=text.find("\n---",4)
    if end<0:
        return {}
    out={}
    for raw in text[4:end].splitlines():
        if not raw or raw[:1].isspace() or ":" not in raw:
            continue
        k,v=raw.split(":",1)
        out[k.strip()]=_scalar(v)
    return out


def _headings(path: Path) -> tuple[str,str]:
    title=subtitle=""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# ") and not title:
            title=line[2:].strip()
        elif line.startswith("### ") and not subtitle:
            subtitle=line[4:].strip()
        if title and subtitle:
            break
    return title,subtitle


def _add(rows, prov, candidate: ved.Candidate, source: str, path: str, **extra):
    rows.append(candidate)
    prov[candidate.id]={"source":source,"path":path,**extra}


def _church(rows,prov) -> dict:
    base=ROOT/"content/church"
    files=sorted(p for p in base.glob("*.md") if p.name!="_index.md") if base.exists() else []
    for path in files:
        fm=_frontmatter(path)
        title=str(fm.get("title") or path.stem.replace("-"," ").title())
        subtitle=str(fm.get("subtitle") or "")
        deck=str(fm.get("description") or subtitle)
        tags=("教會","church",title,subtitle)
        weight=fm.get("weight",4)
        try: order=max(1,int(weight))
        except Exception: order=4
        significance=max(.52,min(.82,.86-order*.055))
        cid=f"site:church:{path.stem}"
        _add(rows,prov,ved.Candidate(cid,title,"Church",deck,"","church",tags,.72,significance,.42,.66),"church",str(path.relative_to(ROOT)),frontmatter=True)
    return {"count":len(files),"path":"content/church","mode":"hugo-frontmatter"}


def _journal(rows,prov) -> dict:
    base=ROOT/"content/journal"
    files=sorted(p for p in base.glob("*.md") if p.name!="_index.md") if base.exists() else []
    for path in files:
        fm=_frontmatter(path)
        title=str(fm.get("title") or path.stem.replace("-"," ").title())
        deck=str(fm.get("description") or fm.get("subtitle") or "")
        cid=f"site:journal:{path.stem}"
        _add(rows,prov,ved.Candidate(cid,title,"Journal",deck,"","journal",("journal",title),.88,.82,.48,.72),"journal",str(path.relative_to(ROOT)),frontmatter=True)
    return {"count":len(files),"path":"content/journal","mode":"hugo-content","note":"_index.md is structural and never promoted as an article"}


def _dawn(rows,prov) -> dict:
    rel="data/resources.json"; data=_read_json(rel); n=0
    theme=data.get("weekly_theme") or {}
    if theme.get("title"):
        cid="site:dawn:weekly-theme"
        deck=str(theme.get("description") or "")
        tags=("黎明書局","dawn","每週主題","經文",str(theme.get("title_en") or ""))
        _add(rows,prov,ved.Candidate(cid,str(theme["title"]),"Dawn Library · Weekly Theme",deck,"","dawn-library",tags,.9,.92,.46,.9),"dawn-library",rel,record="weekly_theme")
        n+=1
    inventory=((data.get("system") or {}).get("recovered_inventory") or [])
    for group in inventory:
        category=str(group.get("category") or "")
        for item in group.get("items") or []:
            rid=str(item.get("id") or "").strip()
            name=str(item.get("name") or "").strip()
            if not rid or not name: continue
            cid=f"site:dawn:{rid.lower()}"
            en=str(item.get("name_en") or "")
            deck=" · ".join(x for x in (category,en) if x)
            tags=("黎明書局","學習","研究",category,en,name)
            history=("History" in category or "Civilization" in category or any(k in name for k in ("史","傳","古卷","宣教")))
            extra=("歷史","見證","人物") if history else ("查經","經文","學習")
            _add(rows,prov,ved.Candidate(cid,name,"Dawn Library",deck,"","dawn-library",tags+extra,.48,.72,.4,.86),"dawn-library",rel,record=rid,category=category)
            n+=1
    return {"count":n,"path":rel,"mode":"resource-master"}


def _one(rows,prov) -> dict:
    rel="static/one/ONE-PRODUCTION-PROGRESS-TEMP.json"; data=_read_json(rel); n=0
    for item in data.get("verifiedPrecedents") or []:
        if item.get("status")!="DONE" or not item.get("verification"): continue
        key=str(item.get("key") or "").strip()
        if not key: continue
        title=f"{item.get('book','ONE')} {item.get('chapter','')}章".strip()
        deck=str(item.get("verification") or "")
        cid=f"site:one:{key}"
        tags=("ONE","查經","經文","study",str(item.get("book") or ""),str(item.get("assignment") or ""))
        _add(rows,prov,ved.Candidate(cid,title,"ONE · verified chapter",deck,"","one",tags,.76,.9,.5,.96),"one",rel,record=key,route=item.get("route"),runtime_isolation=True)
        n+=1
    return {"count":n,"path":rel,"mode":"verified-build-metadata","runtime_isolation":True}


def _folio(rows,prov) -> dict:
    base=ROOT/"static/multiwrite/books"; n=0
    if base.exists():
        for path in sorted(base.glob("*/chapter-*.md")):
            title,subtitle=_headings(path)
            if not title: continue
            book=path.parent.name; slug=path.stem
            cid=f"site:folio:{book}:{slug}"
            deck=subtitle or f"Doré Folio · {book}"
            tags=("Doré Folio","folio","筆記","研究","經文",title,subtitle)
            _add(rows,prov,ved.Candidate(cid,title,"Doré Folio",deck,"","dore-folio",tags,.68,.8,.44,.92),"dore-folio",str(path.relative_to(ROOT)),book=book)
            n+=1
    return {"count":n,"path":"static/multiwrite/books/*/chapter-*.md","mode":"markdown-headings"}


def _visual(rows,prov) -> dict:
    rel="data/visual_graph.json"; data=_read_json(rel); accepted=rejected=0
    for work in data.get("visual_works") or []:
        reps=work.get("representations") or []
        rep=next((r for r in reps if (r.get("rights") or {}).get("branded_derivative_allowed") is True and r.get("image_url")),None)
        if not rep:
            rejected+=1; continue
        wid=str(work.get("id") or "").strip()
        if not wid: continue
        title=str(work.get("canonical_title") or wid)
        scripture=[str(x.get("canonical") or "") for x in work.get("scripture_refs") or []]
        tags=tuple(str(x) for x in (work.get("depicts") or [])+(work.get("persons") or [])+(work.get("places") or [])+(work.get("events") or [])+scripture)
        deck=" · ".join(x for x in (str(work.get("series") or ""),str(work.get("date") or ""),str((work.get("creator") or {}).get("name") or "")) if x)
        cid=f"site:visual:{wid}"
        _add(rows,prov,ved.Candidate(cid,title,"Dawn Library · Visual Graph",deck,str(rep["image_url"]),"dawn-library",tags+("視覺","visual",),.62,.84,.96,.82),"visual-graph",rel,record=wid,representation=rep.get("id"),rights=rep.get("rights"))
        accepted+=1
    return {"count":accepted,"rejected_rights_or_missing_image":rejected,"path":rel,"mode":"rights-gated-visual-graph"}


def load() -> PoolResult:
    rows: list[ved.Candidate]=[]; provenance={}; diagnostics={}
    diagnostics["church"]=_church(rows,provenance)
    diagnostics["journal"]=_journal(rows,provenance)
    diagnostics["dawn-library"]=_dawn(rows,provenance)
    diagnostics["one"]=_one(rows,provenance)
    diagnostics["dore-folio"]=_folio(rows,provenance)
    diagnostics["visual-graph"]=_visual(rows,provenance)
    ids=[c.id for c in rows]
    if len(ids)!=len(set(ids)):
        raise ValueError("duplicate_sitewide_candidate_id")
    diagnostics["total"]={"count":len(rows),"unique":True}
    return PoolResult(rows,provenance,diagnostics)
