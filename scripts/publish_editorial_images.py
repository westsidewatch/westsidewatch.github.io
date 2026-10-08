#!/usr/bin/env python3
"""Publish one or many local editorial images to GitHub without manual web uploads.

Requirements: git, gh (authenticated with 'gh auth login').
Run from a checkout of this repository:
  python3 scripts/publish_editorial_images.py /path/to/david-pawson.png --name david-pawson-editorial
  python3 scripts/publish_editorial_images.py /path/to/image-directory --prefix olive
"""
import argparse
import pathlib
import shutil
import subprocess
import sys

EXTS = {".png", ".jpg", ".jpeg", ".webp", ".avif", ".svg"}

def run(*args):
    subprocess.run(args, check=True)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=pathlib.Path, help="Image file or folder of images")
    parser.add_argument("--name", help="Destination filename stem for a single image")
    parser.add_argument("--prefix", default="olive", help="Destination collection, default olive")
    parser.add_argument("--branch", default="main", help="Target Git branch")
    parser.add_argument("--no-push", action="store_true", help="Stage only, do not commit/push")
    args = parser.parse_args()
    repo = pathlib.Path(__file__).resolve().parents[1]
    if not shutil.which("git") or not shutil.which("gh"):
        parser.error("Requires git and GitHub CLI (gh)")
    run("gh", "auth", "status")
    run("git", "-C", str(repo), "switch", args.branch)
    src = args.source.expanduser().resolve()
    if not src.exists():
        parser.error(f"Missing source: {src}")
    images = sorted(p for p in (src.iterdir() if src.is_dir() else [src]) if p.is_file() and p.suffix.lower() in EXTS)
    if not images:
        parser.error("No supported images found")
    dest_dir = repo / "static" / "images" / args.prefix
    dest_dir.mkdir(parents=True, exist_ok=True)
    for source in images:
        stem = args.name if args.name and len(images) == 1 else source.stem
        dest = dest_dir / (stem + source.suffix.lower())
        if source != dest.resolve():
            shutil.copy2(source, dest)
        run("git", "-C", str(repo), "add", str(dest.relative_to(repo)))
        print(f"STAGED /images/{args.prefix}/{dest.name}")
    if args.no_push:
        return
    run("git", "-C", str(repo), "commit", "-m", f"assets: publish {len(images)} editorial image(s)")
    run("git", "-C", str(repo), "push", "origin", args.branch)
    print("Published. GitHub Pages deployment may take time.")

if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as error:
        sys.exit(error.returncode)
