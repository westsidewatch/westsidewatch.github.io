"""Compact Biblical World foundation registry.

This is intentionally macro-level Foundation knowledge. Absolute dates and historical
labels are scholarly reconstructions unless Scripture explicitly supplies them.
Later researcher education may refine/contest these entries without rewriting
canonical attestations.
"""
from __future__ import annotations

MACRO_PERIODS=(
 {'id':'patriarchal_narratives','label':'Patriarchal narratives','scope':'Genesis 12–50','evidence_class':'SCRIPTURE_INFERRED'},
 {'id':'exodus_wilderness','label':'Exodus and wilderness','scope':'Exodus–Deuteronomy','evidence_class':'SCRIPTURE_INFERRED'},
 {'id':'settlement_judges','label':'Settlement and Judges','scope':'Joshua–Judges','evidence_class':'SCRIPTURE_INFERRED'},
 {'id':'united_monarchy','label':'United monarchy','scope':'Saul–David–Solomon','evidence_class':'SCHOLARLY_RECONSTRUCTION'},
 {'id':'divided_monarchies','label':'Israel and Judah','scope':'divided monarchy to Assyrian/Babylonian conquests','evidence_class':'SCHOLARLY_RECONSTRUCTION'},
 {'id':'babylonian_exile','label':'Babylonian exile','scope':'6th century BCE','evidence_class':'SCHOLARLY_RECONSTRUCTION'},
 {'id':'persian_period','label':'Persian period','scope':'Achaemenid imperial context','evidence_class':'SCHOLARLY_RECONSTRUCTION'},
 {'id':'hellenistic_period','label':'Hellenistic period','scope':'post-Alexander eastern Mediterranean','evidence_class':'SCHOLARLY_RECONSTRUCTION'},
 {'id':'roman_nt','label':'Roman New Testament world','scope':'late 1st century BCE–1st century CE','evidence_class':'SCHOLARLY_RECONSTRUCTION'},
)

EMPIRE_SEQUENCE=(
 {'id':'egypt','label':'Egypt','role':'recurring regional power','evidence_class':'SCRIPTURE_EXPLICIT'},
 {'id':'assyria','label':'Assyria','role':'Neo-Assyrian imperial context for Israel/Judah','evidence_class':'SCHOLARLY_RECONSTRUCTION'},
 {'id':'babylon','label':'Babylon','role':'Neo-Babylonian conquest/exile context','evidence_class':'SCHOLARLY_RECONSTRUCTION'},
 {'id':'persia','label':'Persia','role':'Achaemenid return/restoration context','evidence_class':'SCHOLARLY_RECONSTRUCTION'},
 {'id':'hellenistic','label':'Hellenistic kingdoms','role':'intertestamental and later Jewish context','evidence_class':'SCHOLARLY_RECONSTRUCTION'},
 {'id':'rome','label':'Rome','role':'New Testament imperial context','evidence_class':'SCRIPTURE_EXPLICIT'},
)

INSTITUTIONS=(
 {'id':'tabernacle','domain':'cult','periods':('exodus_wilderness','settlement_judges'),'evidence_class':'SCRIPTURE_EXPLICIT'},
 {'id':'temple','domain':'cult','periods':('united_monarchy','divided_monarchies','persian_period','hellenistic_period','roman_nt'),'evidence_class':'SCRIPTURE_EXPLICIT'},
 {'id':'priesthood','domain':'cult','periods':('exodus_wilderness','settlement_judges','united_monarchy','divided_monarchies','persian_period','roman_nt'),'evidence_class':'SCRIPTURE_EXPLICIT'},
 {'id':'synagogue','domain':'assembly','periods':('roman_nt',),'evidence_class':'SCRIPTURE_EXPLICIT'},
 {'id':'kingship','domain':'polity','periods':('united_monarchy','divided_monarchies','roman_nt'),'evidence_class':'SCRIPTURE_EXPLICIT'},
 {'id':'household_kinship','domain':'social','periods':tuple(x['id'] for x in MACRO_PERIODS),'evidence_class':'SCRIPTURE_EXPLICIT'},
 {'id':'agriculture_pastoralism','domain':'economy','periods':tuple(x['id'] for x in MACRO_PERIODS),'evidence_class':'SCRIPTURE_EXPLICIT'},
 {'id':'money_weights_measures','domain':'economy','periods':('divided_monarchies','persian_period','hellenistic_period','roman_nt'),'evidence_class':'SCRIPTURE_EXPLICIT'},
 {'id':'military','domain':'warfare','periods':tuple(x['id'] for x in MACRO_PERIODS),'evidence_class':'SCRIPTURE_EXPLICIT'},
)

def registry_checks()->dict:
    periods={x['id'] for x in MACRO_PERIODS}
    return {
      'macro_periods':len(MACRO_PERIODS)>=9,
      'empire_sequence':len(EMPIRE_SEQUENCE)>=6,
      'institutions':len(INSTITUTIONS)>=8,
      'institution_period_integrity':all(set(x['periods'])<=periods for x in INSTITUTIONS),
      'evidence_classes_present':all(x.get('evidence_class') for x in (*MACRO_PERIODS,*EMPIRE_SEQUENCE,*INSTITUTIONS)),
    }
