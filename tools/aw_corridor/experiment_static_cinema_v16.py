#!/usr/bin/env python3
"""Compatibility launcher for AW-011 strict three-blade V17.

The existing topology-probe workflow watches this path. This bridge also
normalizes camera cadence for the long-take experiment: 30 frames per camera
segment at the workflow's 12 fps, yielding about a 15 second traversal across
six segments. This changes camera motion itself, not merely playback speed.
"""
import sys
from experiment_static_cinema_v17 import main


def force_long_take_cadence(argv):
    out=list(argv)
    flag='--segment-frames'
    if flag in out:
        i=out.index(flag)
        if i+1 < len(out):
            out[i+1]='30'
            return out
    out.extend([flag,'30'])
    return out

if __name__ == '__main__':
    sys.argv=force_long_take_cadence(sys.argv)
    raise SystemExit(main())
