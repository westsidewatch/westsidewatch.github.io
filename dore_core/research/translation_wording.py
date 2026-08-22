"""Explain wording differences after textual/reference alignment is established."""
from __future__ import annotations
import re
from collections import Counter

ARCHAIC={"thou":"you","thee":"you","thy":"your","thine":"your","ye":"you","hath":"has","doth":"does","saith":"says","unto":"to","art":"are","wast":"were","shalt":"shall","wilt":"will"}
SPELLING={"shew":"show","shewed":"showed","musick":"music","publick":"public","connexion":"connection","throughly":"thoroughly"}
TOKEN=re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?|\d+")

def tokens(text:str):return [x.lower() for x in TOKEN.findall(text)]
def canon_token(t:str):return SPELLING.get(t,ARCHAIC.get(t,t))
def classify_wording(a:str,b:str):
    ta,tb=tokens(a),tokens(b)
    if ta==tb:return ("punctuation_or_formatting","high","Lexical token sequence is identical; the visible difference is punctuation, capitalization, or formatting.")
    ca,cb=[canon_token(x) for x in ta],[canon_token(x) for x in tb]
    if ca==cb:
        archaic=any(x in ARCHAIC for x in ta+tb)
        return (("archaic_language_modernization" if archaic else "spelling_modernization"),"high","The aligned wording differs by recognized archaic/modern English forms or spelling rather than textual content.")
    if Counter(ca)==Counter(cb):return ("word_order_or_syntax","medium_high","The normalized lexical inventory is the same but its order differs, indicating syntax or word-order translation choice.")
    sa,sb=set(ca),set(cb); overlap=len(sa&sb)/max(1,len(sa|sb)); length_ratio=min(len(ca),len(cb))/max(1,max(len(ca),len(cb)))
    if overlap>=0.75 and length_ratio>=0.8:return ("lexical_choice","medium_high","Most aligned vocabulary is shared, with a limited set of substitutions consistent with lexical or idiomatic translation choice.")
    if overlap>=0.55:return ("phrasing_or_expansion_compression","medium","The translations share the passage core but differ in phrase shape or explicitness, consistent with expansion/compression, syntax, or idiom.")
    return ("substantial_rendering_difference","medium","The aligned verse is rendered with substantially different vocabulary; explanation requires lexical/syntactic study rather than a reference-level inference.")
