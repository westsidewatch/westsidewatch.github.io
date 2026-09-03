#!/usr/bin/env python3
"""Free-only RSS/Atom ingestion for provenance-bearing observations."""
from __future__ import annotations
import hashlib,html,re,urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime,timezone
from urllib.parse import urlparse
from free_api_gate import reserve
VERSION="dore.real-signal-connector.v1.0"
DEFAULT_FEED="https://api.io.canada.ca/io-server/gc/news/en/v2?format=atom&sort=publishedDate&orderBy=desc&pick=10"
POLICY={"provider":"canada-news-atom","billing":"free-only","credentials":"none","paid_fallback":False,"daily_request_limit":48,"per_call_result_limit":10}
def _text(node,name):
 child=node.find("{*}"+name);return (child.text or "").strip() if child is not None else ""
def _clean(value):return re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",html.unescape(value or ""))).strip()
def parse_atom(payload,*,publisher,feed_url,limit=10,retrieved_at=None):
 root=ET.fromstring(payload);observed=retrieved_at or datetime.now(timezone.utc).isoformat();rows=[]
 for entry in root.findall("{*}entry")[:limit]:
  link_node=entry.find("{*}link");link=(link_node.attrib.get("href") if link_node is not None else "") or _text(entry,"id")
  external_id=_text(entry,"id") or link;title=_clean(_text(entry,"title"));summary=_clean(_text(entry,"summary") or _text(entry,"content"));occurred=_text(entry,"published") or _text(entry,"updated") or observed
  raw="\n".join((external_id,title,summary,occurred,link))
  rows.append({"schema":"dore.source-observation.v1","source_family":"official-government-feed","external_id":external_id,"title":title,"summary":summary,"occurred_at":occurred,"observed_at":observed,"provenance":[{"publisher":publisher,"url":link,"feed_url":feed_url,"retrieved_at":observed}],"content_hash":hashlib.sha256(raw.encode()).hexdigest()})
 return rows
def fetch_atom(feed_url=DEFAULT_FEED,*,publisher="Government of Canada",limit=10,usage_file=None,timeout=20):
 parsed=urlparse(feed_url)
 if parsed.scheme!="https" or not parsed.netloc:raise ValueError("https_feed_required")
 budget=reserve(POLICY,usage_file);request=urllib.request.Request(feed_url,headers={"User-Agent":"DoreRealSignal/1.0 (+human-editor-gated)"})
 with urllib.request.urlopen(request,timeout=timeout) as response:payload=response.read(2_000_000)
 return {"ok":True,"connector":VERSION,"free_api_budget":budget,"observations":parse_atom(payload,publisher=publisher,feed_url=feed_url,limit=min(limit,POLICY["per_call_result_limit"])),"provenance_preserved":True}
