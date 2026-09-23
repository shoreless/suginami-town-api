#!/usr/bin/env python3
"""Validate registered assets and catalogue consistency; allow clearly reported work in progress."""
import argparse
import hashlib
import json
import struct
from pathlib import Path
from build_catalogue import ARTWORK, build, local, read

PNG_MODES = {0: 'L', 2: 'RGB', 3: 'P', 4: 'LA', 6: 'RGBA'}

def validate(artwork=ARTWORK, require_complete=False):
    errors = []
    manifest, layout = build(artwork)
    for asset in manifest['assets']:
        asset_id = asset['id']
        for key in ('width', 'height', 'mode', 'sha256', 'prompt', 'references', 'generator', 'status'):
            if key not in asset:
                errors.append(f'{asset_id}: missing metadata {key}')
        path = local(asset['path'], artwork)
        if not path.is_file():
            errors.append(f'{asset_id}: missing file {path}')
            continue
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != asset.get('sha256'):
            errors.append(f'{asset_id}: hash mismatch')
        if data[:8] != b'\x89PNG\r\n\x1a\n':
            errors.append(f'{asset_id}: expected source PNG')
            continue
        width, height = struct.unpack('>II', data[16:24])
        mode = PNG_MODES.get(data[25])
        if (width, height, mode) != (asset.get('width'), asset.get('height'), asset.get('mode')):
            errors.append(f'{asset_id}: dimension/mode metadata mismatch')
        if asset.get('shape') == 'square' and width != height:
            errors.append(f'{asset_id}: square background is not square')
        if asset.get('shape') == 'wide' and abs(width / height - 2) > .03:
            errors.append(f'{asset_id}: wide background must be approximately 2:1')
        if 'sources/characters/' in asset['path'] and mode != 'RGBA':
            errors.append(f'{asset_id}: character must have an alpha channel')
        if asset.get('prompt') and not local(asset['prompt'], artwork).is_file():
            errors.append(f'{asset_id}: missing prompt')
        for reference in asset.get('references', []):
            if not local(reference, artwork).is_file():
                errors.append(f'{asset_id}: missing reference {reference}')
    for path, expected in ((artwork / 'collection-manifest.json', manifest),
                           (artwork / 'layouts/collection.json', layout)):
        if not path.is_file() or read(path) != expected:
            errors.append(f'{path.name}: stale; run build_catalogue.py')
    summary = manifest['summary']
    if require_complete and (summary['backgrounds_missing'] or summary['characters_missing']):
        errors.append('Collection is incomplete.')
    return errors, summary

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-complete', action='store_true')
    args = parser.parse_args()
    errors, summary = validate(require_complete=args.require_complete)
    for error in errors:
        print(f'ERROR: {error}')
    print(f"{summary['backgrounds_available']}/{summary['backgrounds_expected']} backgrounds available; "
          f"{len(summary['characters_missing'])} missing character variants.")
    print('This verifies files and metadata, not visual quality or native device performance.')
    raise SystemExit(1 if errors else 0)

if __name__ == '__main__':
    main()
