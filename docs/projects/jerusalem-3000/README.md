# Jerusalem 3000｜三千年耶路撒冷時空重建

Issue: #832

## Position

This is not a parallel 3D toy. It is the first real consumer of a reusable historical-city temporal reconstruction capability for Westside Watch / Doré Core.

Publication relation:
- 〈建〉: 人在城牆上走。
- Jerusalem 3000: 時間在城市裡走。
- Both share one spatial / evidence authority.

## Prototype 01 — Jaffa Gate fixed-view transform

One stable terrain/camera frame, four temporal states:
1. Today
2. Herodian / Jesus-era reading coordinate
3. Nehemiah / Persian-period reading coordinate
4. David–Solomon reading coordinate

The point is not four unrelated models. The point is one spatial coordinate system with reversible temporal state.

## Hard constraints

- fixed terrain / coordinate authority across eras
- reversible time scrub
- construction, destruction, burial and rebuilding as state changes
- object-level Evidence Architecture
- mobile-first
- publication-embeddable
- no generic black UI surface
- upstream MIT attribution remains explicit

## Evidence Architecture

Every spatial object may carry:
- observed: directly evidenced / extant / excavated
- reconstructed: high-confidence reconstruction from multiple evidence classes
- inferred: plausible but incomplete reconstruction
- disputed: materially contested interpretation

These are display states, not truth scores. Disputed hypotheses may expose A/B alternatives.

## First implementation slice

The first slice deliberately uses abstract architectural masses, not pretend-historical models. It proves:
- stable camera
- timeline interpolation
- reversible assembly/disassembly
- evidence-state rendering
- era deep links
- data contract for replacing abstract masses with researched geometry later

Historical geometry is blocked until evidence authority is attached to the object.


## Continuous Build Mode — hard requirement

Jerusalem 3000 must be able to play the city's urban biography continuously from the earliest settlement landscape to the present. It must not be implemented as four isolated hero-era models.

Canonical runtime phases now live at `preview/jerusalem-3000/data/continuous-build-timeline.json`.

Every phase may emit one or more temporal operations:

- `build` — new fabric appears from terrain/foundation upward
- `expand` — occupied envelope grows
- `transform` — existing fabric is reused/replanned
- `ruin` — destruction is visible as an event and persistent archaeological residue
- `buried` — earlier fabric remains in the stratigraphic stack
- `rebuild` — later fabric reuses or overwrites earlier coordinates

The viewer therefore preserves **urban memory**: moving forward never means deleting the past from the data model. Moving backward must reconstruct prior states from the same object/event ledger.

The four original anchors (Today / Jesus / Nehemiah / David–Solomon) remain editorial shortcuts only. They are not the temporal data model.
