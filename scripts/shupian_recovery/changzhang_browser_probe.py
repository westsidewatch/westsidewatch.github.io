#!/usr/bin/env python3
"""Technical HLS playback sampling inside isolated headless Chromium.

Loads only candidate M3U8 in a blank media test page using hls.js; the source
website's JS, ad popups and navigation are never loaded. It does not certify
full-content integrity, ad-free video, or publication rights.
"""
from __future__ import annotations
import argparse
import asyncio
from datetime import datetime,timezone
import json
from pathlib import Path
from urllib.parse import urlsplit

from legacy_engine_core import validate_public_url

HLS_JS="https://cdn.jsdelivr.net/npm/hls.js@1.6.13/dist/hls.min.js"

def sample_candidates(discovery, limit=3):
    samples=discovery.get("media_samples",[])
    selected=[]
    seen=set()
    for sample in samples:
        candidate=sample.get("url","")
        check=sample.get("result",{})
        if check.get("status")!="segment-bytes-sampled": continue
        if check.get("ad_signals",{}).get("suspected"): continue
        try: validate_public_url(candidate)
        except Exception: continue
        title=str(sample.get("title",""))
        if title in seen:continue
        seen.add(title)
        selected.append({"title":title,"episode":sample.get("episode"),
                         "url":candidate})
        if len(selected)>=limit:break
    return selected

async def check_playback(browser, source_url, timeout_ms=20000):
    page=await browser.new_page()
    result={"source_host":urlsplit(source_url).hostname,
            "metadata_loaded":False,"first_frame":False,
            "time_advanced":False,"status":"ERROR"}
    try:
        await page.set_content('<!doctype html><html><body><video id="probe" muted playsinline preload="auto" style="width:640px"></video></body></html>')
        await page.add_script_tag(url=HLS_JS)
        sample=await page.evaluate("""async ({url, timeoutMs}) => {
            const video=document.getElementById("probe");
            const result={metadata_loaded:false,first_frame:false,time_advanced:false,status:"TIMEOUT",error:null};
            let hls=null;
            let initialTime=0;
            return await new Promise(resolve=>{
                let finished=false;
                const done=(status,error)=>{
                    if(finished)return; finished=true;
                    result.status=status;result.error=error||null;
                    result.metadata_loaded=video.readyState>=1;
                    result.first_frame=video.readyState>=2;
                    result.time_advanced=video.currentTime>Math.max(0.6,initialTime+0.6);
                    clearTimeout(timer);
                    if(hls)hls.destroy();
                    video.pause();
                    resolve(result);
                };
                const timer=setTimeout(()=>done("TIMEOUT","No verified playback within window"),timeoutMs);
                video.addEventListener("loadedmetadata",()=>{result.metadata_loaded=true});
                video.addEventListener("loadeddata",()=>{result.first_frame=true;initialTime=video.currentTime});
                video.addEventListener("timeupdate",()=>{
                    if(video.readyState>=2&&video.currentTime>initialTime+0.6){
                        result.first_frame=true;
                        result.time_advanced=true;
                        done("TIME_ADVANCED");
                    }
                });
                video.addEventListener("error",()=>done("MEDIA_ERROR",String(video.error?.code||"unknown")));
                try{
                    if(window.Hls&&Hls.isSupported()){
                        hls=new Hls({enableWorker:true});
                        hls.on(Hls.Events.ERROR,(_,data)=>{
                            if(data.fatal)done("HLS_ERROR",data.details||data.type);
                        });
                        hls.on(Hls.Events.MANIFEST_PARSED,()=>{
                            video.play().catch(e=>done("PLAY_REJECTED",e.message));
                        });
                        hls.loadSource(url);hls.attachMedia(video);
                    }else if(video.canPlayType("application/vnd.apple.mpegurl")){
                        video.src=url;video.play().catch(e=>done("PLAY_REJECTED",e.message));
                    }else{
                        done("UNSUPPORTED_HLS","No supported HLS player");
                    }
                }catch(e){done("EXCEPTION",e.message)}
            });
        }""",{"url":source_url,"timeoutMs":timeout_ms})
        result.update(sample)
        # The browser never certifies an entire media stream from a short sample.
        result["certified_clean"]=False
    except Exception as exc:
        result["error"]=str(exc)[:250]
    finally:
        await page.close()
    return result

async def run(discovery,limit=3,timeout_ms=20000):
    from playwright.async_api import async_playwright
    targets=sample_candidates(discovery,limit)
    report={"schema":1,"at_utc":datetime.now(timezone.utc).isoformat(),
            "method":"isolated-chromium/hls.js/first-frame-and-time-progress",
            "samples_requested":len(targets),"samples":[],
            "warning":"Technical playback sampling is not whole-video or ad-free certification."}
    if not targets:
        report["status"]="NO_QUALIFIED_HLS_SAMPLES"
        return report
    async with async_playwright() as p:
        browser=await p.chromium.launch(headless=True,args=["--autoplay-policy=no-user-gesture-required"])
        try:
            for candidate in targets:
                output=await check_playback(browser,candidate["url"],timeout_ms)
                output["title"]=candidate["title"]
                output["episode"]=candidate["episode"]
                report["samples"].append(output)
        finally:
            await browser.close()
    report["first_frame_pass"]=sum(bool(x["first_frame"]) for x in report["samples"])
    report["time_progress_pass"]=sum(bool(x["time_advanced"]) for x in report["samples"])
    report["status"]="SAMPLED" if report["samples"] else "NO_TEST"
    return report

def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--scan",type=Path,required=True)
    p.add_argument("--output",type=Path,default=Path("shupian-changzhang-playback.json"))
    p.add_argument("--limit",type=int,default=3)
    p.add_argument("--timeout-ms",type=int,default=20000)
    a=p.parse_args(argv)
    if not 1<=a.limit<=10 or not 1000<=a.timeout_ms<=60000:
        p.error("limit must be 1-10, timeout-ms 1000-60000")
    if not a.scan.is_file():p.error("Real discovery file required")
    discovery=json.loads(a.scan.read_text(encoding="utf-8"))
    report=asyncio.run(run(discovery,a.limit,a.timeout_ms))
    a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":report["status"],
                      "first_frames":report.get("first_frame_pass",0),
                      "time_progress":report.get("time_progress_pass",0)},ensure_ascii=False))

if __name__=="__main__":
    main()
