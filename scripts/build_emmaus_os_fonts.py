#!/usr/bin/env python3
"""Mirror only the approved Emmaus OS faces from pinned official sources.
No new families, no generated design tokens. Official Chiron webfont subsets
are copied byte-for-byte; Noto's full variable font is losslessly WOFF2 packed.
"""
import concurrent.futures, hashlib, json, pathlib, re, time, urllib.request
from urllib.parse import quote
from fontTools.ttLib import TTFont

ROOT = pathlib.Path("static/fonts/os-emmaus")
RAW = "https://raw.githubusercontent.com/"
CHIRON = "chiron-fonts/chiron-hei-hk"
CHIRON_REV = "106b59c99e6164b26a11d46214a98dd68386b31a"
GOOGLE = "google/fonts"
BODONI_REV = "634558fcbd9225a88591dec164f9fdb2716d0bf5"
NOTO_REV = "6d17dab13b85129360f9748f057c7f67c5f484d4"

def fetch(url):
    for i in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent":"Westside-OS-font-mirror"}), timeout=90) as response:
                return response.read()
        except Exception:
            if i == 3: raise
            time.sleep(2**i)

def git_sha(data):
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()

def mirror(repo, revision, path, dest, expected=None):
    raw = fetch(RAW+repo+"/"+revision+"/"+quote(path, safe="/"))
    sha = git_sha(raw)
    if expected and sha != expected:
        raise RuntimeError(f"source hash mismatch: {path}: {sha}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(raw)
    return {"source":repo,"revision":revision,"path":path,"blob":sha,"bytes":len(raw),"local":str(dest)}

def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    # Pin the official tree and verify every webfont against its Git blob.
    shas = json.loads(pathlib.Path("scripts/emmaus-chiron-pinned-blobs.json").read_text())
    if len(shas)!=146: raise RuntimeError("pinned upstream manifest incomplete")
    prefix = "WOFF2_TTF/"
    css_path = prefix+"css/vf.css"
    css_dest = ROOT/"chiron/css/vf.css"
    records = [mirror(CHIRON,CHIRON_REV,css_path,css_dest,shas[css_path])]
    css = css_dest.read_text()
    paths = sorted(set(re.findall(r"url\('\.\./(woff2/[^']+)'\)", css)))
    if len(paths)!=144 or "Chiron Hei HK WS" not in css:
        raise RuntimeError("official Chiron subset inventory changed")
    def one(path):
        return mirror(CHIRON,CHIRON_REV,prefix+path,ROOT/"chiron"/path,shas[prefix+path])
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        records.extend(pool.map(one, paths))
    records.append(mirror(CHIRON,CHIRON_REV,"LICENSE.md",ROOT/"chiron/LICENSE.md",shas["LICENSE.md"]))
    # Roman and italic are distinct real faces, not synthesized SC or italic.
    for name, remote, sha in [
        ("BodoniModa-VF.ttf","ofl/bodonimoda/BodoniModa[opsz,wght].ttf","c5d582f8003ae692761dd8e9ce69de23cb9fea53"),
        ("BodoniModa-Italic-VF.ttf","ofl/bodonimoda/BodoniModa-Italic[opsz,wght].ttf","174375b9265ac430071f6f1f20de8dbe088c61c1")]:
        records.append(mirror(GOOGLE,BODONI_REV,remote,ROOT/name,sha))
    records.append(mirror(GOOGLE,BODONI_REV,"ofl/bodonimoda/OFL.txt",ROOT/"OFL-BodoniModa.txt"))
    tmp=ROOT/"NotoSerifTC-source.ttf"
    record=mirror(GOOGLE,NOTO_REV,"ofl/notoseriftc/NotoSerifTC[wght].ttf",tmp,"f27659681d4141ddc96fe29cccf77e23a3d3b639")
    font=TTFont(tmp)
    cmap=font.getBestCmap()
    font.flavor="woff2"
    packed=ROOT/"NotoSerifTC-VF.woff2"
    font.save(packed)
    font.close()
    check=TTFont(packed)
    if check.getBestCmap()!=cmap: raise RuntimeError("Noto coverage changed")
    check.close()
    tmp.unlink()
    record.update(local=str(packed),localBytes=packed.stat().st_size,localSha256=hashlib.sha256(packed.read_bytes()).hexdigest(),glyphs=len(cmap),encoding="lossless WOFF2")
    records.append(record)
    records.append(mirror(GOOGLE,NOTO_REV,"ofl/notoseriftc/OFL.txt",ROOT/"OFL-NotoSerifTC.txt"))
    for name in ROOT.rglob("*"):
        if name.is_file() and name.stat().st_size>25*1024*1024: raise RuntimeError(f"Pages asset exceeds 25MiB: {name}")
    pathlib.Path("static/css/emmaus-os-fonts.css").write_text('''/* Approved Design OS faces — mirrored from pinned upstream revisions.
   Existing tokens retain all semantic authority; this stylesheet only supplies fonts. */
@import url("/fonts/os-emmaus/chiron/css/vf.css");
@font-face{font-family:"Bodoni Moda SC";src:url("/fonts/scripture-studio/BodoniModaSC-VF.ttf") format("truetype");font-style:normal;font-weight:400 900;font-display:swap}
@font-face{font-family:"Bodoni Moda";src:url("/fonts/os-emmaus/BodoniModa-VF.ttf") format("truetype");font-style:normal;font-weight:400;font-display:swap}
@font-face{font-family:"Bodoni Moda";src:url("/fonts/os-emmaus/BodoniModa-Italic-VF.ttf") format("truetype");font-style:italic;font-weight:400;font-display:swap}
@font-face{font-family:"Noto Serif TC";src:url("/fonts/os-emmaus/NotoSerifTC-VF.woff2") format("woff2");font-style:normal;font-weight:400 600;font-display:swap}
''')
    (ROOT/"manifest.json").write_text(json.dumps({"schema":"westside.os.font-mirror.v1","scope":"emmaus","files":records,"chironSubsets":len(paths)},ensure_ascii=False,indent=2)+"\n")
    print(f"Mirrored {len(paths)} official Chiron subsets; Noto glyphs {len(cmap)}; all assets {sum(x.stat().st_size for x in ROOT.rglob('*') if x.is_file())} bytes")
if __name__=="__main__": main()
