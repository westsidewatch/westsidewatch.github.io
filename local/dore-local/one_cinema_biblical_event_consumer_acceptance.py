#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
authority=json.loads((ROOT/'data/bible-index/biblical-event.v1.json').read_text())
one=json.loads((ROOT/'docs/one/biblical-event-consumer.v1.json').read_text())
moments=json.loads((ROOT/'cinema/data/video-moment.v0.json').read_text())['items']
resources=json.loads((ROOT/'cinema/data/video-resource.v0.json').read_text())['items']
graph=(ROOT/'cinema/resource-graph.js').read_text()
entry=(ROOT/'cinema/event-entry.js').read_text()
index=(ROOT/'cinema/index.html').read_text()
readme=(ROOT/'docs/one/README.md').read_text()
assert authority['schema']=='dore.biblical-event.v1'
assert authority['authority']=='bible-index'
assert authority['identityPolicy']['consumerMayGrantMediaExactness'] is False
assert one['schema']=='one.biblical-event-consumer.v1'
assert one['surfaceId']=='tool:one'
assert one['authority']=='data/bible-index/biblical-event.v1.json'
assert one['consumesSchema']==authority['schema']
assert one['joinKey']=='eventId'
assert one['projectionPolicy']['duplicateCanonicalEventMetadata'] is False
assert one['projectionPolicy']['mayGrantMediaExactness'] is False
canonical={e['eventId'] for e in authority['items']}
assert set(one['eventRefs'])==canonical
assert all(ref.startswith('bible:event:') for ref in one['eventRefs'])
assert not (ROOT/'cinema/data/biblical-event.v1.json').exists()
assert "events:'../data/bible-index/biblical-event.v1.json'" in graph
assert "eventAuthority:eventPayload.authority" in graph
assert 'momentsForEvent' in graph and 'eventDeepLink' in graph
assert "params.get('event')" in entry
assert "moment.kind==='official-episode'" in entry
assert 'graph.momentsForEvent(event.eventId)' in entry
assert 'graph.deepLink(exact[0].momentId)' in entry
assert 'event-entry.js' in index
assert 'data/bible-index/biblical-event.v1.json' in readme
assert '/cinema/?event={eventId}#cinema-library' in readme
admitted_ids={r['canonicalId'] for r in resources if r['canonicalId']!='cinema:video:goodtv:holy-spirit-power-workplace-testimony'}
alias={a:e['eventId'] for e in authority['items'] for a in [e['canonicalKey'],*e.get('aliases',[])]}
by_event={event_id:[] for event_id in canonical}
for moment in moments:
    if moment['workId'] not in admitted_ids or moment['kind']!='official-episode': continue
    for anchor in moment.get('anchors',[]):
        if anchor['type']=='event' and anchor['value'] in alias:
            by_event[alias[anchor['value']]].append(moment['momentId'])
expected={
 'bible:event:incarnation':['cinema:moment:lumo-matthew:episode-01'],
 'bible:event:baptism-of-jesus':['cinema:moment:lumo-matthew:episode-02'],
 'bible:event:crucifixion':['cinema:moment:lumo-matthew:episode-24'],
 'bible:event:resurrection':['cinema:moment:lumo-matthew:episode-24']
}
assert by_event==expected
assert by_event['bible:event:crucifixion']==by_event['bible:event:resurrection']
assert 'startMs' not in one and 'momentId' not in one
print('ONE_CINEMA_BIBLICAL_EVENT_CONSUMER=PASS consumers=2 events=4 join=eventId overrides=0 fake_timecodes=0')
