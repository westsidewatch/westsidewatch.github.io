#!/usr/bin/env python3
"""Doré R2 controlled extraction benchmark. Python stdlib only.
No commands run unless explicitly supplied; never executes page content.
Example:
 python3 dore_benchmark.py --targets targets.txt --output results.jsonl \
   --command 'firecrawl scrape {url}' --label firecrawl
 Repeat with a separately verified Scrapling command. URL is passed as a single
 argv token (no shell), and command templates must contain literal {url}.
"""
import argparse, json, pathlib, shlex, subprocess, time, datetime, statistics, urllib.parse

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--targets",required=True)
 p.add_argument("--output",required=True)
 p.add_argument("--command",required=True,help="quoted executable command containing {url}")
 p.add_argument("--label",required=True)
 p.add_argument("--repeats",type=int,default=3)
 p.add_argument("--timeout",type=int,default=45)
 a=p.parse_args()
 if a.repeats<1 or a.repeats>10 or a.timeout<1: p.error("invalid repeats/timeout")
 args=shlex.split(a.command)
 if sum(part.count("{url}") for part in args)!=1: p.error("command needs exactly one {url}")
 urls=[line.strip() for line in pathlib.Path(a.targets).read_text().splitlines() if line.strip() and not line.lstrip().startswith("#")]
 records=[]
 for url in urls:
  u=urllib.parse.urlsplit(url)
  if u.scheme!="https" or not u.hostname or u.username or u.password: p.error("only public HTTPS URLs accepted")
  for n in range(a.repeats):
   argv=[part.replace("{url}",url) for part in args]
   start=time.perf_counter()
   try:
    proc=subprocess.run(argv,capture_output=True,text=True,timeout=a.timeout,check=False)
    output=proc.stdout
    row={"returncode":proc.returncode,"bytes":len(output.encode()),"chars":len(output),"error":proc.stderr[:300]}
   except subprocess.TimeoutExpired:
    row={"returncode":None,"bytes":0,"chars":0,"error":"timeout"}
   row.update({"url":url,"tool":a.label,"run":n+1,"timestamp_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"duration_ms":round((time.perf_counter()-start)*1000),"license":"unverified","visual":"not-tested"})
   records.append(row)
  vals=[r["duration_ms"] for r in records if r["url"]==url and r["returncode"]==0]
  print(json.dumps({"url":url,"successes":len(vals),"runs":a.repeats,"median_ms":statistics.median(vals) if vals else None},ensure_ascii=False))
 out=pathlib.Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
 with out.open("w") as f:
  for r in records:f.write(json.dumps(r,ensure_ascii=False)+"\n")
 print("Wrote",out,"rows",len(records))
if __name__=="__main__":main()
