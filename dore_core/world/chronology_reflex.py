"""BW-3 chronology: evidence-bounded relative/absolute time reasoning."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ChronologyClaim:
    label:str
    start_bce:int|None=None
    end_bce:int|None=None
    start_ce:int|None=None
    end_ce:int|None=None
    evidence_class:str='SCHOLARLY_RECONSTRUCTION'
    confidence:float=0.5
    source:str='Doré Foundation period registry'

    @property
    def precise(self)->bool:
        vals=[x for x in (self.start_bce,self.end_bce,self.start_ce,self.end_ce) if x is not None]
        return len(vals)==1 or (len(vals)==2 and vals[0]==vals[1])

def bounded_date(label:str, *, explicit_year:int|None=None, reconstructed_range:tuple[int,int]|None=None, era:str='BCE')->ChronologyClaim:
    if explicit_year is not None:
        kw={'start_bce':explicit_year,'end_bce':explicit_year} if era=='BCE' else {'start_ce':explicit_year,'end_ce':explicit_year}
        return ChronologyClaim(label,evidence_class='SCRIPTURE_EXPLICIT',confidence=1.0,source='canonical text',**kw)
    if reconstructed_range:
        a,b=reconstructed_range;lo,hi=min(a,b),max(a,b)
        kw={'start_bce':hi,'end_bce':lo} if era=='BCE' else {'start_ce':lo,'end_ce':hi}
        return ChronologyClaim(label,evidence_class='SCHOLARLY_RECONSTRUCTION',confidence=.65,**kw)
    return ChronologyClaim(label,evidence_class='SCRIPTURE_INFERRED',confidence=.35)

def compare_sequence(a:str,b:str,relation:str,source:str='canonical sequence')->dict:
    if relation not in {'before','after','overlaps','uncertain'}:raise ValueError(relation)
    return {'a':a,'b':b,'relation':relation,'evidence_class':'SCRIPTURE_INFERRED' if source=='canonical sequence' else 'SCHOLARLY_RECONSTRUCTION','source':source}
