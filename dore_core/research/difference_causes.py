"""Conservative cause taxonomy for cross-witness biblical reference differences."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Iterable

NT_BOOKS={"MAT","MRK","LUK","JHN","ACT","ROM","1CO","2CO","GAL","EPH","PHP","COL","1TH","2TH","1TI","2TI","TIT","PHM","HEB","JAS","1PE","2PE","1JN","2JN","3JN","JUD","REV"}
NT_TRADITION_LOCI={"MAT.17.21","MAT.18.11","MAT.23.14","MRK.7.16","MRK.9.44","MRK.9.46","MRK.11.26","MRK.15.28","LUK.17.36","LUK.22.43","LUK.22.44","LUK.23.17","JHN.5.4","JHN.7.53","JHN.8.1","JHN.8.2","JHN.8.3","JHN.8.4","JHN.8.5","JHN.8.6","JHN.8.7","JHN.8.8","JHN.8.9","JHN.8.10","JHN.8.11","ACT.8.37","ACT.15.34","ACT.24.7","ACT.28.29","ROM.16.24","1JN.5.7","1JN.5.8"}

@dataclass(frozen=True)
class Cause:
    code:str; family:str; confidence:str; explanation:str; evidence_basis:tuple[str,...]; correspondence_policy:str; research_status:str="classified_not_textually_adjudicated"
    def to_dict(self): return asdict(self)

def parse_ref(ref:str):
    parts=ref.split(".")
    if len(parts)>=5 and parts[:2]==["bible","ref"]:
        try:return parts[2],int(parts[3]),int(parts[4])
        except ValueError:return None
    return None

def classify(ref:str, category:str, members:Iterable[str]=(), present:Iterable[str]=(), missing:Iterable[str]=()):
    p=parse_ref(ref); members=set(members)
    if not p:
        return Cause("source_specific_identity","canon_or_source_scope","high","The reference remains outside the shared Protestant bible.ref namespace because its source identity cannot be safely collapsed into that namespace.",("source-specific namespace retained","adapter provenance"),"preserve source reference; map only with explicit evidence")
    book,ch,v=p; locus=f"{book}.{ch}.{v}"
    if book=="PSA":
        return Cause("psalm_superscription_or_numbering","versification","high","Psalm traditions differ in counting superscriptions and, in Greek/Latin traditions, sometimes in psalm numbering; the same material can therefore carry shifted references.",("Psalm concentration","terminal/offset reference pattern"),"retain witness numbering and attach offset/range correspondence")
    if book in {"JOL","MAL"}:
        return Cause("chapter_partition_difference","versification","high","The book is partitioned into chapters differently across source traditions, redistributing the same material across chapter boundaries.",("same-book chapter-boundary pattern",),"map contiguous ranges across chapter boundaries")
    if book in {"DAN","EST"} and ("lxx" in members or "vulgate" in members or category!="anchor_only_reference"):
        return Cause("expanded_ancient_text_tradition","textual_tradition_and_versification","high","Greek/Latin forms contain material or numbering structures not represented identically in the Hebrew-based sequence.",("LXX/Vulgate membership","book-specific ancient textual tradition"),"preserve additions/source numbering; map explicit parallels only")
    if book in NT_BOOKS and (locus in NT_TRADITION_LOCI or category in {"multi_witness_extra_reference_candidate","single_witness_extra_reference"}):
        return Cause("new_testament_textual_base_difference","textual_tradition","medium_high","The pattern is consistent with differences among New Testament textual traditions or critical editions, where material may be included, bracketed, relocated, or omitted.",("MorphGNT/SBLGNT critical-text anchor","translation inclusion/omission pattern"),"link at passage/range level; never manufacture missing text")
    if "lxx" in members and len(members)==1:
        return Cause("septuagint_source_versification","versification_or_source_scope","medium_high","The locus is specific to Septuagint numbering or section structure rather than a shared Protestant reference identity.",("LXX-only membership","Rahlfs/CenterBLC identity"),"retain LXX identity; map only demonstrated parallels")
    if "vulgate" in members and len(members)==1:
        return Cause("vulgate_versification","versification","medium_high","The locus reflects Vulgate numbering or section boundaries that do not coincide exactly with the Hebrew/modern-English anchor.",("Vulgate-only membership",),"retain Vulgate reference and attach explicit correspondence")
    if category=="anchor_only_reference":
        return Cause("hebrew_or_critical_versification_boundary","versification","medium_high","The anchor exposes a numbered locus that translations do not expose under the same number; adjacent versification is the first explanation to test before textual omission.",("anchor-only reference",),"seek adjacent-reference correspondence first")
    if category=="translation_reference_divergence":
        return Cause("translation_versification_divergence","versification_or_textual_base","medium","Translations disagree because source versification or textual bases do not expose the passage under one identical reference.",("mixed present/missing translation membership",),"compare adjacent ranges and textual bases")
    if category=="multi_witness_extra_reference_candidate":
        return Cause("shared_non_anchor_reference_tradition","versification_or_textual_tradition","medium_high","Multiple translation witnesses share a numbered locus absent from the anchor, indicating a stable non-anchor reference or textual tradition.",("multiple translation witnesses","anchor absence"),"create shared correspondence node; preserve readings")
    if category=="single_witness_extra_reference":
        return Cause("witness_specific_reference_tradition","versification_or_textual_tradition","medium","A validated single witness exposes a locus absent from the anchor and other loaded witnesses; it is retained as a witness-specific phenomenon pending passage-level evidence.",("single-witness membership","engineering validation clean"),"preserve and require passage-level evidence before equivalence")
    return Cause("structural_reference_difference","versification_or_textual_tradition","low_medium","A validated structural difference remains whose precise historical cause requires passage-level evidence.",("validated inventories",),"preserve all refs and escalate")
