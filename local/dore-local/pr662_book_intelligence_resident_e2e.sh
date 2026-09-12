#!/bin/bash
set -euo pipefail

TMP="$(mktemp -d "${RUNNER_TEMP:-/tmp}/pr662-e2e.XXXXXX")"
APP_ROOT="$HOME/Library/Application Support/DoreA2A"
NATIVE_MANIFEST="$HOME/Library/Application Support/Mozilla/NativeMessagingHosts/ca.dore.companion.json"
NATIVE_LAUNCHER="$APP_ROOT/dore-native-host"
EXT="$TMP/extension"
RESULT="$TMP/result.json"
MODEL_TRACE="$TMP/model-trace.json"
MODEL_RESPONSE="$TMP/model-response.json"
WEBEXT_LOG="$TMP/web-ext.log"
BACKUP="$TMP/dore-native-host.backup"
CAP_PID=''; PROXY_PID=''; WEBEXT_PID=''

free_port() {
  python3 - <<'PY'
import socket
s=socket.socket(); s.bind(('127.0.0.1',0)); print(s.getsockname()[1]); s.close()
PY
}
CAPTURE_PORT="$(free_port)"
PROXY_PORT="$(free_port)"
while test "$PROXY_PORT" = "$CAPTURE_PORT"; do PROXY_PORT="$(free_port)"; done

echo "E2E_CAPTURE_PORT=$CAPTURE_PORT"
echo "E2E_PROXY_PORT=$PROXY_PORT"

cleanup() {
  set +e
  test -n "$WEBEXT_PID" && kill "$WEBEXT_PID" 2>/dev/null || true
  test -n "$CAP_PID" && kill "$CAP_PID" 2>/dev/null || true
  test -n "$PROXY_PID" && kill "$PROXY_PID" 2>/dev/null || true
  if test -f "$BACKUP"; then cp "$BACKUP" "$NATIVE_LAUNCHER"; chmod 755 "$NATIVE_LAUNCHER"; fi
  rm -rf "$TMP"
}
trap cleanup EXIT

FIREFOX="${FIREFOX:-}"
if test -z "$FIREFOX"; then
  for C in '/Applications/Firefox.app/Contents/MacOS/firefox' "$HOME/Applications/Firefox.app/Contents/MacOS/firefox"; do
    if test -x "$C"; then FIREFOX="$C"; break; fi
  done
fi
test -x "$FIREFOX" || { echo 'E2E_FAIL firefox_missing' >&2; exit 1; }
command -v npx >/dev/null 2>&1 || { echo 'E2E_FAIL npx_missing' >&2; exit 1; }

echo "E2E_SHA=$(git rev-parse HEAD)"
echo "E2E_HOST=$(hostname)"
"$FIREFOX" --version
npx --yes web-ext@8.10.0 --version

test -f "$NATIVE_MANIFEST" || { echo 'E2E_FAIL native_manifest_missing' >&2; exit 1; }
python3 -c 'import json,sys; m=json.load(open(sys.argv[1])); assert m["name"]=="ca.dore.companion"; assert m["allowed_extensions"]==["dore-companion@westsidewatch.ca"]; print("E2E_NATIVE_MANIFEST=PASS")' "$NATIVE_MANIFEST"
test -x "$NATIVE_LAUNCHER" || { echo 'E2E_FAIL native_launcher_missing' >&2; exit 1; }
cp "$NATIVE_LAUNCHER" "$BACKUP"

curl -fsS http://127.0.0.1:11434/api/tags > "$TMP/tags.json"
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); names={m.get("name") for m in d.get("models",[])}; assert "gemma4:e4b" in names, names; print("E2E_MODEL_PRESENT=gemma4:e4b")' "$TMP/tags.json"

cat > "$TMP/ollama_proxy.py" <<'PY'
import json,sys,urllib.request
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
trace=sys.argv[1]; response_path=sys.argv[2]; port=int(sys.argv[3])
class H(BaseHTTPRequestHandler):
    def do_POST(self):
        n=int(self.headers.get('Content-Length','0')); raw=self.rfile.read(n)
        body=json.loads(raw.decode('utf-8'))
        open(trace,'w',encoding='utf-8').write(json.dumps({'path':self.path,'model':body.get('model')},ensure_ascii=False))
        req=urllib.request.Request('http://127.0.0.1:11434'+self.path,data=raw,headers={'Content-Type':'application/json'},method='POST')
        with urllib.request.urlopen(req,timeout=360) as r: out=r.read(); code=r.status
        open(response_path,'wb').write(out)
        self.send_response(code); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(out))); self.end_headers(); self.wfile.write(out)
    def log_message(self,*args): pass
ThreadingHTTPServer(('127.0.0.1',port),H).serve_forever()
PY
python3 "$TMP/ollama_proxy.py" "$MODEL_TRACE" "$MODEL_RESPONSE" "$PROXY_PORT" >"$TMP/proxy.log" 2>&1 & PROXY_PID=$!

cat > "$TMP/capture.py" <<'PY'
import sys
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
out=sys.argv[1]; port=int(sys.argv[2])
class H(BaseHTTPRequestHandler):
    def do_GET(self):
        body=b'<!doctype html><html><body>PR662 Companion E2E probe</body></html>'
        self.send_response(200); self.send_header('Content-Type','text/html; charset=utf-8'); self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)
    def do_POST(self):
        n=int(self.headers.get('Content-Length','0')); raw=self.rfile.read(n); open(out,'wb').write(raw)
        self.send_response(200); self.send_header('Access-Control-Allow-Origin','*'); self.end_headers(); self.wfile.write(b'ok')
    def do_OPTIONS(self):
        self.send_response(204); self.send_header('Access-Control-Allow-Origin','*'); self.send_header('Access-Control-Allow-Methods','POST, OPTIONS'); self.send_header('Access-Control-Allow-Headers','Content-Type'); self.end_headers()
    def log_message(self,*args): pass
ThreadingHTTPServer(('127.0.0.1',port),H).serve_forever()
PY
python3 "$TMP/capture.py" "$RESULT" "$CAPTURE_PORT" >"$TMP/capture.log" 2>&1 & CAP_PID=$!
sleep 1
kill -0 "$CAP_PID" 2>/dev/null || { echo 'E2E_FAIL capture_server_start' >&2; cat "$TMP/capture.log" >&2 || true; exit 1; }
kill -0 "$PROXY_PID" 2>/dev/null || { echo 'E2E_FAIL proxy_server_start' >&2; cat "$TMP/proxy.log" >&2 || true; exit 1; }

cat > "$NATIVE_LAUNCHER" <<EOF
#!/bin/bash
set -euo pipefail
export DORE_REPO_ROOT="$GITHUB_WORKSPACE"
export DORE_LOCAL_MODEL="gemma4:e4b"
export OLLAMA_BASE_URL="http://127.0.0.1:$PROXY_PORT"
exec "$(command -v python3)" "$GITHUB_WORKSPACE/local/dore-local/native_host.py"
EOF
chmod 755 "$NATIVE_LAUNCHER"

mkdir -p "$EXT"
ditto "$GITHUB_WORKSPACE/local/dore-companion-extension" "$EXT"
python3 - "$EXT/native_transport.js" <<'PY'
import sys
p=sys.argv[1]; s=open(p,encoding='utf-8').read(); old='return sendVia4312(payload);'; assert old in s; s=s.replace(old,'throw nativeError;'); open(p,'w',encoding='utf-8').write(s); print('E2E_FALLBACK_DISABLED=PASS')
PY

python3 - "$GITHUB_WORKSPACE/static/multiwrite/books/kingdom-language" "$EXT/e2e_probe.js" "$EXT/manifest.json" "$CAPTURE_PORT" <<'PY'
import json,sys,hashlib
from pathlib import Path
root=Path(sys.argv[1]); probe=Path(sys.argv[2]); mp=Path(sys.argv[3]); port=int(sys.argv[4])
source=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
sections=[]
for i,item in enumerate(source.get('structure') or []):
    if item.get('file'):
        text=(root/item['file']).read_text(encoding='utf-8')
    else:
        text='\n\n'.join((root/f).read_text(encoding='utf-8') for f in (item.get('files') or []))
    sections.append({'id':item.get('id') or f'section-{i+1}','index':i,'role':item.get('role') or 'chapter','title':item.get('title') or '','text':text})
args={'source':source,'sections':sections}
raw=json.dumps(args,ensure_ascii=False,separators=(',',':'))
print('E2E_MANUSCRIPT_TITLE='+source.get('title',''))
print('E2E_MANUSCRIPT_SECTIONS='+str(len(sections)))
print('E2E_MANUSCRIPT_PAYLOAD_SHA256='+hashlib.sha256(raw.encode()).hexdigest())
origin=f'http://127.0.0.1:{port}'
js='const E2E_ARGS='+raw+';\n(async()=>{let payload;try{payload=await browser.runtime.sendMessage({type:"dore.site-capability",capability:"publishing.book-intelligence",args:E2E_ARGS,caller_product:"multiwrite"});}catch(e){payload={ok:false,error:String(e&&e.message||e)}};await fetch("'+origin+'/result",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)});})();\n'
probe.write_text(js,encoding='utf-8')
m=json.loads(mp.read_text(encoding='utf-8'))
m.setdefault('permissions',[]).append('http://127.0.0.1/*')
m.setdefault('content_scripts',[]).append({'matches':['http://127.0.0.1/*'],'js':['e2e_probe.js'],'run_at':'document_idle'})
mp.write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
print('E2E_PROBE_CONTEXT=content-script')
PY

export MOZ_HEADLESS=1
npx --yes web-ext@8.10.0 run --source-dir "$EXT" --firefox "$FIREFOX" --no-reload --start-url "http://127.0.0.1:$CAPTURE_PORT/probe" >"$WEBEXT_LOG" 2>&1 & WEBEXT_PID=$!

for i in $(seq 1 210); do
  test -s "$RESULT" && break
  if ! kill -0 "$WEBEXT_PID" 2>/dev/null; then
    echo 'E2E_FAIL firefox_webext_exited_before_result' >&2
    cat "$WEBEXT_LOG" >&2 || true
    exit 1
  fi
  sleep 2
done

test -s "$RESULT" || { echo 'E2E_FAIL no_companion_result' >&2; cat "$WEBEXT_LOG" >&2 || true; cat "$TMP/capture.log" >&2 || true; exit 1; }
test -s "$MODEL_TRACE" || { echo 'E2E_FAIL no_ollama_model_trace' >&2; cat "$TMP/proxy.log" >&2 || true; cat "$RESULT" >&2 || true; exit 1; }

python3 - "$MODEL_TRACE" "$MODEL_RESPONSE" "$RESULT" <<'PY'
import hashlib,json,sys
trace=json.load(open(sys.argv[1],encoding='utf-8')); assert trace.get('path')=='/api/chat', trace; assert trace.get('model')=='gemma4:e4b', trace
outer=json.load(open(sys.argv[3],encoding='utf-8'))
assert outer.get('ok') is True, outer
assert outer.get('stage')=='site-capability', outer
result=outer.get('result') or {}
assert result.get('ok') is True, result
assert result.get('status')=='completed', result
assert result.get('capability')=='publishing.book-intelligence', result
report=result.get('report') or {}
assert report.get('schema')=='dore.book-intelligence-report.v2', report
runtime=report.get('runtime') or {}
if not (runtime.get('semantic') is True and runtime.get('degraded') is False):
    print('E2E_SEMANTIC_RUNTIME='+json.dumps(runtime,ensure_ascii=False))
    if len(sys.argv)>2:
        try:
            envelope=json.load(open(sys.argv[2],encoding='utf-8')); content=str((envelope.get('message') or {}).get('content') or '')
            print('E2E_MODEL_CONTENT_BYTES='+str(len(content.encode('utf-8'))))
            print('E2E_MODEL_CONTENT_SHA256='+hashlib.sha256(content.encode()).hexdigest())
            print('E2E_MODEL_CONTENT_HEAD='+content[:240].replace('\n','\\n'))
            print('E2E_MODEL_CONTENT_TAIL='+content[-240:].replace('\n','\\n'))
        except Exception as exc:
            print('E2E_MODEL_DIAGNOSTIC_ERROR='+str(exc))
assert runtime.get('semantic') is True and runtime.get('degraded') is False, runtime
authority=report.get('authority') or {}
assert authority.get('mayRewriteThesis') is False, authority
print('E2E_FIREFOX_COMPANION=PASS')
print('E2E_NATIVE_MESSAGING=PASS')
print('E2E_MODEL_BACKED=gemma4:e4b')
print('E2E_REAL_MANUSCRIPT=PASS')
print('E2E_SEMANTIC_DEGRADED=false')
print('E2E_REPORT_CATEGORY='+str(report.get('category') or ''))
print('E2E_REPORT_CONFIDENCE='+str(report.get('confidence')))
print('PR662_RESIDENT_E2E=PASS')
PY
