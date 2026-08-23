"""BW-6 evidence discipline shared across Biblical World claims."""
from __future__ import annotations
from dataclasses import dataclass

EVIDENCE_CLASSES={
 'SCRIPTURE_EXPLICIT','SCRIPTURE_INFERRED','PRIMARY_EXTRA_BIBLICAL','ARCHAEOLOGICAL',
 'GEOSPATIAL_OBSERVATION','SCHOLARLY_RECONSTRUCTION','TRADITIONAL_IDENTIFICATION','EDITORIAL_NORMALIZATION'
}

@dataclass(frozen=True)
class EvidenceDecision:
    claim:str
    evidence_class:str
    provenance:str
    temporal_scope:str|None=None
    confidence:float|None=None
    controversy:str|None=None

    def valid(self)->bool:
        return self.evidence_class in EVIDENCE_CLASSES and bool(self.provenance) and (self.confidence is None or 0<=self.confidence<=1)

WORDING={
 'SCRIPTURE_EXPLICIT':'Scripture states',
 'SCRIPTURE_INFERRED':'The textual evidence suggests',
 'PRIMARY_EXTRA_BIBLICAL':'An extra-biblical primary source attests',
 'ARCHAEOLOGICAL':'Archaeological evidence indicates',
 'GEOSPATIAL_OBSERVATION':'Geospatial observation gives',
 'SCHOLARLY_RECONSTRUCTION':'A scholarly reconstruction proposes',
 'TRADITIONAL_IDENTIFICATION':'A traditional identification holds',
 'EDITORIAL_NORMALIZATION':'This is an editorial normalization',
}

def permitted_wording(decision:EvidenceDecision)->str:
    if not decision.valid():raise ValueError('invalid evidence decision')
    base=WORDING[decision.evidence_class]
    if decision.controversy:base+=f' (contested: {decision.controversy})'
    return base

def can_say_scripture_says(decision:EvidenceDecision)->bool:
    return decision.evidence_class=='SCRIPTURE_EXPLICIT'
