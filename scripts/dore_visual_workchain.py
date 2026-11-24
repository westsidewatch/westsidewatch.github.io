#!/usr/bin/env python3
"""Fail-closed evidence gate for isolated Westside visual experiments.
Not a sandbox or an aesthetic judge. No production promotion in v1."""
import argparse, json, re, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
CONTRACT = json.loads((ROOT / "dore-design/visual-workchain/contract.json").read_text())
STAGES = CONTRACT["stages"]
def require(ok, reason):
    if not ok: raise ValueError(reason)
def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()
def scope(paths):
    for p in paths:
        require(p.startswith(CONTRACT["allowed_prefix"]) and ".." not in Path(p).parts, "protected path: "+p)
def authority():
    return {p: git("hash-object", p) for p in CONTRACT["authority"]}
def check(run, hashes, read, human_verified=False):
    events=run.get("events", [])
    require(isinstance(events,list) and len(events)<=len(STAGES), "invalid stages")
    for i,e in enumerate(events):
        require(e.get("stage")==STAGES[i], "stage skipped or reordered")
        require(e.get("status")=="pass", "failed stage cannot advance")
        if i==0:
            require(e.get("authority")==hashes, "missing or stale authority")
        elif i==1:
            refs=e.get("references",[])
            require(len({r.get("url") for r in refs})>=3 and all(re.match(r"https://[^/]+/",r.get("url","")) and all(r.get(k) for k in ("mechanism","application","license_or_rights","decision")) for r in refs), "external exploration evidence incomplete")
        elif i==2:
            candidates=e.get("candidates",[])
            require(len(candidates)>=2, "independent compositions required")
            require(len({c.get("principle") for c in candidates})==len(candidates) and all(c.get("principle") for c in candidates), "distinct composition principles required")
            sources=[]
            for c in candidates:
                p=c.get("html","")
                scope([p]); require(p.endswith(".html"),"HTML required")
                s=read(p).decode()
                require("<html" in s.lower() and "<body" in s.lower(), "renderable HTML required")
                require(not any(x in s for x in CONTRACT["rejected_sources"]),"rejected source reused")
                sources.append(s)
            require(len(set(sources))==len(sources),"duplicate compositions")
        elif i==3:
            proofs=e.get("proofs",[])
            candidates=events[2]["candidates"]
            require({(p.get("candidate"),p.get("width")) for p in proofs}=={(c["html"],w) for c in candidates for w in (1440,390)}, "desktop/mobile proof missing")
            for p in proofs:
                scope([p["png"]]); b=read(p["png"])
                require(b.startswith(b"\x89PNG\r\n\x1a\n") and len(b)>100, "invalid screenshot")
                require(all(p.get(k) is True for k in ("os_colors","os_fonts","no_overflow","readable")), "technical check failed")
        elif i==4:
            require(e.get("winner") in {c["html"] for c in events[2]["candidates"]},"unknown winner")
            require(e.get("comparison") and e.get("blocking_issues")==[], "critique incomplete")
        elif i==5:
            require(human_verified, "human approval must be independently verified; v1 CLI cannot promote")
        elif i==6:
            require(human_verified, "grammar requires human approval")
    return STAGES[len(events)] if len(events)<len(STAGES) else "complete"
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--run",required=True)
    ap.add_argument("--base",required=True,help="trusted starting commit of experiment")
    a=ap.parse_args()
    try:
        scope([a.run])
        changed=git("diff","--name-only",a.base,"HEAD").splitlines()+git("diff","--name-only","HEAD").splitlines()+git("ls-files","--others","--exclude-standard").splitlines()
        scope(changed)
        def read(p):
            scope([p]); target=(ROOT/p).resolve()
            require(target.is_relative_to(ROOT/CONTRACT["allowed_prefix"]),"path escape")
            return target.read_bytes()
        run=json.loads(read(a.run))
        print(json.dumps({"next":check(run,authority(),read),"production_allowed":False}))
    except (ValueError,KeyError,TypeError,OSError,subprocess.CalledProcessError) as e:
        print("REJECT:",e,file=sys.stderr); return 1
    return 0
if __name__=="__main__":sys.exit(main())
