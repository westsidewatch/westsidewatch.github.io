#!/usr/bin/env python3
"""Fixed localhost model adapter. Never accepts a remote URL or SVG fallback."""
import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

BASE = 'http://127.0.0.1:8790'


def generate(prompt_file, output_file):
    prompt_path = Path(prompt_file)
    quality_path = prompt_path.with_name('editorial-quality.json')
    if quality_path.exists():
        quality = json.loads(quality_path.read_text(encoding='utf-8'))
        if quality.get('requiresReferenceConditioning'):
            raise RuntimeError('REFERENCE_CONDITIONING_UNSUPPORTED: the resident /generate adapter only sends text. Refusing to fake an identity-grounded portrait. Install and verify a reference-image capable local adapter before rendering.')
    with urlopen(BASE + '/health', timeout=15) as response:
        health = json.load(response)
    if health.get('model_backed') is not True:
        raise RuntimeError('Local image model is not ready; SVG fallback refused')
    prompt = prompt_path.read_text(encoding='utf-8')
    request = Request(BASE + '/generate', data=json.dumps({'message': 'Generate image: ' + prompt}).encode(),
                      headers={'Content-Type': 'application/json', 'X-Dore-Origin': 'dore-search'})
    with urlopen(request, timeout=1500) as response:
        result = json.load(response)
    if result.get('ok') is not True or result.get('model_backed') is not True:
        raise RuntimeError('Backend did not return model-backed imagery')
    asset = urlparse(result.get('asset_url', ''))
    if asset.scheme != 'http' or asset.hostname != '127.0.0.1' or asset.port != 8790 or asset.path != '/asset':
        raise RuntimeError('Invalid local asset URL')
    with urlopen(asset.geturl(), timeout=30) as response:
        raw = response.read(32 * 1024 * 1024 + 1)
    if len(raw) > 32 * 1024 * 1024 or not raw.startswith(b'\x89PNG\r\n\x1a\n'):
        raise RuntimeError('Backend must return a bounded PNG')
    with Path(output_file).open('xb') as output:
        output.write(raw)
    Path(str(output_file) + '.provenance.json').write_text(json.dumps({
        'modelBacked': True, 'renderer': result.get('renderer'),
        'artifact': result.get('artifact'), 'published': False,
    }, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--prompt-file', required=True)
    parser.add_argument('--output-file', required=True)
    args = parser.parse_args()
    generate(args.prompt_file, args.output_file)
