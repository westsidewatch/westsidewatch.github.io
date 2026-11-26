#!/usr/bin/env python3
"""Doré Offline: on-demand Westside Watch snapshots."""
import argparse
import contextlib
import fcntl
import functools
import hashlib
import http.server
import json
import mimetypes
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import urllib.parse
import webbrowser

REPO = "https://github.com/westsidewatch/westsidewatch.github.io.git"
ORIGIN = "http://127.0.0.1:8765"
HUGO = "0.167.0"
HOME = Path.home() / "Library/Application Support/Dore Offline"
ROUTES = ("index.html", "one/index.html", "one/one-app.js", "olive/index.html",
          "olive/olive.js", "dore-design/runtime/olive-speaker-compositions.v1.json")
TEXT = {".html", ".css", ".js", ".mjs", ".json", ".svg", ".xml", ".webmanifest"}
CANONICAL = re.compile(r"https?://westsidewatch\.github\.io(?=[/\"'\s?#]|$)")
URL = re.compile(r"https?://[^\s\"'<>\\)]+", re.I)
CSP = ("default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' blob:; "
       "style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; font-src 'self' data:; "
       "connect-src 'self'; media-src 'self' blob: data:; worker-src 'self' blob:; "
       "frame-src 'self' blob:; object-src 'none'; base-uri 'self'")

def run(*args, cwd=None, capture=False):
    return subprocess.run(args, cwd=cwd, check=True, text=True,
                          stdout=subprocess.PIPE if capture else None).stdout

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def files(root):
    for p in sorted(root.rglob("*")):
        if p.is_symlink():
            raise ValueError("Unexpected symlink: " + str(p))
        if p.is_file():
            yield p

def manifest(root):
    return {str(p.relative_to(root)): sha256(p) for p in files(root)}

def check_routes(root):
    for name in ROUTES:
        p = root / name
        if not p.is_file() or not p.stat().st_size:
            raise ValueError("Missing published file: " + name)
    if "one-app.js" not in (root / "one/index.html").read_text(encoding="utf-8"):
        raise ValueError("ONE is not the canonical application")
    if len(json.loads((root / ROUTES[-1]).read_text(encoding="utf-8"))["records"]) != 12:
        raise ValueError("Olive composition count must be 12")

def localize_and_audit(root):
    external = {}
    changed = 0
    for p in files(root):
        if p.suffix.lower() not in TEXT:
            continue
        try:
            original = p.read_text(encoding="utf-8")
        except UnicodeError:
            continue
        local = CANONICAL.sub(ORIGIN, original)
        if local != original:
            p.write_text(local, encoding="utf-8")
            changed += 1
        for match in URL.finditer(local):
            try:
                host = urllib.parse.urlsplit(match.group()).hostname
            except ValueError:
                continue
            if not host or host in ("127.0.0.1", "localhost"):
                continue
            item = external.setdefault(host, {"mentions": 0, "examples": []})
            item["mentions"] += 1
            rel = str(p.relative_to(root))
            if len(item["examples"]) < 5 and rel not in item["examples"]:
                item["examples"].append(rel)
    return {"rewritten_files": changed, "external_url_mentions": external,
            "note": "Text scan includes citations and links; dynamic URLs and relative APIs require browser testing."}

def atomic_text(path, value):
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as f:
        name = f.name
        f.write(value)
    os.replace(name, path)

def atomic_json(path, value):
    atomic_text(path, json.dumps(value, ensure_ascii=False, indent=2))

@contextlib.contextmanager
def update_lock(home):
    home.mkdir(parents=True, exist_ok=True)
    with (home / ".update.lock").open("a") as f:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield

def verify(snapshot):
    meta = json.loads((snapshot / "manifest.json").read_text(encoding="utf-8"))
    check_routes(snapshot / "site")
    if manifest(snapshot / "site") != meta["files"]:
        raise ValueError("Snapshot checksum mismatch")
    return meta

def valid_commit(commit):
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("Use a full commit SHA")
    return commit

def active(home):
    return home / "versions" / valid_commit((home / "current").read_text().strip())

def activate(home, commit):
    verify(home / "versions" / valid_commit(commit))
    atomic_text(home / "current", commit + "\n")

def stage(source, target):
    # Mirror the canonical deployment staging for ONE, Olive and Shupian.
    shutil.copytree(source / "static/one", target / "one", dirs_exist_ok=True)
    shutil.copy2(source / "olive/olive.js", target / "olive/olive.js")
    runtime = Path(ROUTES[-1])
    (target / runtime).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source / "static" / runtime, target / runtime)
    if (source / "static/shupian").is_dir():
        shutil.copytree(source / "static/shupian", target / "shupian", dirs_exist_ok=True)

def update(home, ref):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._/-]*", ref) or ".." in ref:
        raise ValueError("Invalid Git ref")
    with update_lock(home):
        for cmd in ("git", "hugo"):
            if not shutil.which(cmd):
                raise RuntimeError("Missing " + cmd + "; install Git and Hugo Extended before updating.")
        version = run("hugo", "version", capture=True)
        if "v" + HUGO not in version or "extended" not in version.lower():
            raise RuntimeError("Use Hugo Extended " + HUGO + " (production build version). Found: " + version.strip())
        cache = home / "source"
        versions = home / "versions"
        versions.mkdir(exist_ok=True)
        if not cache.exists():
            with tempfile.TemporaryDirectory(prefix=".clone-", dir=home) as d:
                new = Path(d) / "repo"
                run("git", "clone", "--no-checkout", "--single-branch", "--branch", "main", REPO, str(new))
                new.rename(cache)
        run("git", "fetch", "--no-tags", "origin", ref, cwd=cache)
        commit = valid_commit(run("git", "rev-parse", "FETCH_HEAD^{commit}", cwd=cache, capture=True).strip())
        dest = versions / commit
        if dest.exists():
            activate(home, commit)
            print("Already downloaded:", commit)
            return
        with tempfile.TemporaryDirectory(prefix=".stage-", dir=versions) as tmp:
            temp = Path(tmp)
            source = temp / "source"
            out = temp / "snapshot"
            out.mkdir()
            target = out / "site"
            run("git", "worktree", "add", "--detach", str(source), commit, cwd=cache)
            try:
                run("git", "submodule", "update", "--init", "--recursive", cwd=source)
                env = dict(os.environ, HUGO_ENVIRONMENT="production", HUGO_ENV="production")
                subprocess.run(["hugo", "--gc", "--minify", "--baseURL", ORIGIN + "/",
                                "--destination", str(target)], cwd=source, env=env, check=True)
                stage(source, target)
                check_routes(target)
                atomic_json(out / "audit.json", localize_and_audit(target))
                atomic_json(out / "manifest.json", {"commit": commit, "ref": ref,
                            "hugo": version.strip(), "files": manifest(target)})
                verify(out)
                out.rename(dest)
                activate(home, commit)
            finally:
                run("git", "worktree", "remove", "--force", str(source), cwd=cache)
        print("Ready:", commit, "External URL audit:", dest / "audit.json")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, directory, **kwargs):
        self.root = Path(directory).resolve()
        self.remaining = None
        super().__init__(*args, directory=str(self.root), **kwargs)

    def end_headers(self):
        self.send_header("Content-Security-Policy", CSP)
        self.send_header("X-Content-Type-Options", "nosniff")
        super().end_headers()

    def list_directory(self, path):
        self.send_error(404, "No directory index")
        return None

    def send_head(self):
        self.remaining = None
        path = Path(self.translate_path(self.path)).resolve()
        if path != self.root and self.root not in path.parents:
            self.send_error(403)
            return None
        header = self.headers.get("Range")
        if not header or not path.is_file():
            return super().send_head()
        size = path.stat().st_size
        m = re.fullmatch(r"bytes=(\d*)-(\d*)", header.strip())
        if m and size and any(m.groups()):
            a, b = m.groups()
            start = int(a) if a else max(0, size-int(b))
            end = min(size-1, int(b)) if a and b else size-1
            if start <= end and start < size:
                f = path.open("rb")
                f.seek(start)
                self.remaining = end-start+1
                self.send_response(206)
                self.send_header("Content-Type", self.guess_type(str(path)))
                self.send_header("Accept-Ranges", "bytes")
                self.send_header("Content-Range", "bytes %d-%d/%d" % (start, end, size))
                self.send_header("Content-Length", str(self.remaining))
                self.end_headers()
                return f
        self.send_response(416)
        self.send_header("Content-Range", "bytes */" + str(size))
        self.end_headers()
        return None

    def copyfile(self, source, outputfile):
        if self.remaining is None:
            return super().copyfile(source, outputfile)
        while self.remaining:
            chunk = source.read(min(65536, self.remaining))
            if not chunk:
                break
            outputfile.write(chunk)
            self.remaining -= len(chunk)

def serve(home):
    snap = active(home)
    check_routes(snap / "site")
    mimetypes.add_type("application/wasm", ".wasm")
    mimetypes.add_type("model/gltf-binary", ".glb")
    mimetypes.add_type("model/gltf+json", ".gltf")
    handler = functools.partial(Handler, directory=str(snap / "site"))
    with http.server.ThreadingHTTPServer(("127.0.0.1", 8765), handler) as server:
        print("Doré Offline:", ORIGIN, "|", snap.name, "| Ctrl-C to close")
        webbrowser.open(ORIGIN)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass

def build_portable_runtime(tool, out):
    if not shutil.which("go"):
        raise RuntimeError("Install Go 1.26 on the preparation Mac, not the presentation Mac.")
    version = run("go", "version", capture=True)
    if not re.search(r"\bgo1\.26(?:\.\d+)?\b", version):
        raise RuntimeError("Use Go 1.26 to support macOS Monterey and newer.")
    runtime = out / "runtime"
    runtime.mkdir()
    for arch in ("amd64", "arm64"):
        env = dict(os.environ, GOOS="darwin", GOARCH=arch, CGO_ENABLED="0", GOTOOLCHAIN="local")
        subprocess.run(["go", "build", "-trimpath", "-ldflags=-s -w", "-o",
                        str(runtime / ("dore-offline-" + arch)), str(tool / "native" / "main.go")],
                       env=env, check=True)

def export_portable(home, destination):
    """Create a self-contained directory on demand; never overwrite existing data."""
    destination = destination.expanduser().resolve()
    if destination.exists():
        raise ValueError("Export destination already exists")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with update_lock(home):
        snap = active(home)
        verify(snap)
        with tempfile.TemporaryDirectory(prefix=".dore-export-", dir=destination.parent) as d:
            out = Path(d) / "Doré Offline"
            out.mkdir()
            tool = Path(__file__).resolve().parent
            shutil.copy2(tool / "README.md", out / "README.md")
            shutil.copy2(tool / "Present.command", out / "Launch.command")
            (out / "Launch.command").chmod(0o755)
            build_portable_runtime(tool, out)
            store = out / "portable-data"
            (store / "versions").mkdir(parents=True)
            shutil.copytree(snap, store / "versions" / snap.name)
            activate(store, snap.name)
            out.rename(destination)
    print("Portable presentation:", destination)

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--home", type=Path, default=HOME)
    sub = p.add_subparsers(dest="cmd", required=True)
    u = sub.add_parser("update")
    u.add_argument("ref", nargs="?", default="main")
    for name in ("serve", "verify", "versions", "audit"):
        sub.add_parser(name)
    e = sub.add_parser("export")
    e.add_argument("destination", type=Path)
    a = sub.add_parser("select")
    a.add_argument("commit")
    args = p.parse_args()
    home = args.home.expanduser().resolve()
    if args.cmd == "update":
        update(home, args.ref)
    elif args.cmd == "serve":
        serve(home)
    elif args.cmd == "verify":
        meta = verify(active(home))
        print("Verified:", meta["commit"], len(meta["files"]), "files")
    elif args.cmd == "audit":
        print((active(home) / "audit.json").read_text(encoding="utf-8"))
    elif args.cmd == "export":
        export_portable(home, args.destination)
    elif args.cmd == "select":
        with update_lock(home):
            activate(home, args.commit)
        print("Selected:", args.commit)
    elif args.cmd == "versions":
        current = active(home).name if (home / "current").exists() else ""
        for path in sorted((home / "versions").glob("*")):
            if re.fullmatch(r"[0-9a-f]{40}", path.name):
                print("*" if path.name == current else " ", path.name)

if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as e:
        raise SystemExit("Doré Offline: " + str(e))
