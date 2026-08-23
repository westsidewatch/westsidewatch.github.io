"""BW-4 peoples, kingdoms and empires: time-bound political identity."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class PolityContext:
    polity:str
    period:str
    ruler:str|None=None
    territory:str|None=None
    biblical_designation:str|None=None
    modern_label:str|None=None
    evidence_class:str='SCHOLARLY_RECONSTRUCTION'
    source:str='Doré Foundation polity registry'

POLITY_PERIODS={
 'egypt':('patriarchal/exodus narratives','late bronze/iron age contexts'),
 'israel':('united monarchy','northern kingdom'),
 'judah':('united monarchy','southern kingdom','babylonian conquest'),
 'assyria':('neo-assyrian','8th–7th c BCE'),
 'babylon':('neo-babylonian','7th–6th c BCE'),
 'persia':('achaemenid','6th–4th c BCE'),
 'greece':('hellenistic','4th–1st c BCE'),
 'rome':('roman','1st c BCE onward'),
}

def contextualize(polity:str,period:str,**kwargs)->PolityContext:
    return PolityContext(polity=polity,period=period,**kwargs)

def validate_time_bound(ctx:PolityContext)->bool:
    return bool(ctx.polity and ctx.period and ctx.evidence_class)

def naming_boundary(ctx:PolityContext)->dict:
    return {'biblical':ctx.biblical_designation,'modern':ctx.modern_label,'same_label_asserted':False,'evidence_class':ctx.evidence_class}
