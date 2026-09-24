"""Bridge canonical Italian Editorial Atlas evidence into DORÉ grounded vision.

The bridge deliberately consumes evidence identity + real image/source URIs only.
`whatToNotice` and canonical grammar tokens are NOT sent to the observer: they would leak
human/ChatGPT interpretation into what must be an image-grounded observation.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, Mapping
from editorial_visual_observation_capability import HistoricalImageEvidence, observe_historical_editorial_image

def evidence_to_historical_image(item: Mapping[str,Any])->HistoricalImageEvidence:
    return HistoricalImageEvidence(evidence_id=str(item.get("id","")),image_uri=str(item.get("image","")),source_uri=str(item.get("source","")),publication=str(item.get("family","")),era=str(item.get("era","")))

def observe_atlas_evidence(item:Mapping[str,Any],provider:Callable[[Mapping[str,Any]],Mapping[str,Any]],*,provider_id:str,provider_kind:str)->Dict[str,Any]:
    evidence=evidence_to_historical_image(item)
    result=observe_historical_editorial_image(evidence,provider,provider_id=provider_id,provider_kind=provider_kind)
    result["atlasBinding"]={"evidenceId":evidence.evidence_id,"family":item.get("family"),"era":item.get("era"),"historicalAuthority":item.get("authority")}
    result["inputIsolation"]={"whatToNoticeWasNotObserverInput":True,"grammarTokensWereNotObserverInput":True,"handwrittenFingerprintWasNotObserverInput":True}
    return result
