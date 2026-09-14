#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
journey=json.loads((ROOT/'cinema/data/bible-journey.v0.json').read_text())
events=json.loads((ROOT/'data/bible-index/biblical-event.v1.json').read_text())
graph=(ROOT/'cinema/resource-graph.js').read_text()
core={'incarnation':'bible:event:incarnation','baptism':'bible:event:baptism-of-jesus','cross':'bible:event:crucifixion','resurrection':'bible:event:resurrection'}
stations={s['stationId']:s for s in journey['journeys'][0]['stations']}
assert journey['exactMomentOverrides']==[]
assert all(stations[k]['eventId']==v for k,v in core.items())
assert set(core.values()) <= {e['eventId'] for e in events['items']}
assert not (ROOT/'cinema/data/bible-journey-moment.v0.json').exists()
assert not (ROOT/'cinema/data/biblical-event.v1.json').exists()
assert 'journeyMoments' not in graph
assert 'JOURNEY_MOMENT_SCHEMA' not in graph
assert "stationEvent=station=>station.eventId?eventById.get(station.eventId)||null:null" in graph
assert 'journeyPayload.exactMomentOverrides' in graph
assert "dataset.cinemaJourneyDerivation='canonical-event-id-v1'" in graph
assert 'station.world||[]).map(resolveEvent)' not in graph
print('PARADISE_CINEMA_BIBLICAL_EVENT_CLOSURE=PASS authority=bible-index station_identity=eventId override_channel=journey compatibility_files=0')
