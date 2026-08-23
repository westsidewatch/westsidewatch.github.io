"""BW-5 institutions/social world: period-aware explanatory routing."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class InstitutionContext:
    concept:str
    period:str
    region:str|None=None
    scripture_refs:tuple[str,...]=()
    comparative_source:str|None=None
    evidence_class:str='SCRIPTURE_INFERRED'
    uncertainty:str|None=None

INSTITUTION_DOMAINS={
 'temple':'cult', 'priesthood':'cult', 'synagogue':'assembly', 'household':'kinship',
 'kingship':'polity', 'court':'law', 'military':'warfare', 'trade':'economy',
 'agriculture':'economy', 'money':'economy', 'weights_measures':'economy',
}

def explain_institution(concept:str,period:str,*,scripture_refs=(),comparative_source=None,region=None,uncertainty=None)->InstitutionContext:
    evidence='SCRIPTURE_EXPLICIT' if scripture_refs and not comparative_source else 'SCHOLARLY_RECONSTRUCTION' if comparative_source else 'SCRIPTURE_INFERRED'
    return InstitutionContext(concept,period,region,tuple(scripture_refs),comparative_source,evidence,uncertainty)

def valid_context(ctx:InstitutionContext)->bool:
    return bool(ctx.concept and ctx.period and ctx.evidence_class)
