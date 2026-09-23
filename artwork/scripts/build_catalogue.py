#!/usr/bin/env python3
"""Build the design-review catalogue without changing published v0 content."""
import argparse
import json
from pathlib import Path

ARTWORK = Path(__file__).resolve().parents[1]
PHASES = ('morning', 'midday', 'evening', 'night')
SHAPES = ('square', 'wide')
CHARACTERS = {
    'morning': 'sources/characters/namisuke/awake-daylight-v01.png',
    'midday': 'sources/characters/namisuke/awake-daylight-v01.png',
    'evening': 'sources/characters/namisuke/awake-evening-v01.png',
    'night': 'sources/characters/namisuke/sleepy-night-v01.png',
}

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def local(path, root=ARTWORK):
    candidate = (root / path).resolve()
    if not candidate.is_relative_to(root.resolve()):
        raise ValueError(f'Path escapes artwork directory: {path}')
    return candidate

def neighborhood_names(source, existing):
    if source.exists():
        names = {}
        for asset in read(source)['assets']:
            names.setdefault(asset['neighborhood'], {
                'id': asset['neighborhood'],
                'name': {'ja': asset['japanese_label'], 'en': asset['label']},
                'description': asset.get('scene_title', ''),
            })
        return list(names.values())
    if existing.exists():
        return [{key: scene[key] for key in ('id', 'name', 'description')}
                for scene in read(existing)['scenes']]
    raise ValueError('Provide --neighborhood-manifest for the initial catalogue build.')

def build(artwork=ARTWORK, neighborhood_manifest=None):
    original = read(artwork / 'manifest.json')
    assets = list(original['assets'])
    for record in sorted((artwork / 'records').glob('*.json')):
        payload = read(record)
        assets.extend(payload['assets'] if 'assets' in payload else [payload])
    ids, paths, slots = set(), set(), {}
    for asset in assets:
        if asset['id'] in ids or asset['path'] in paths:
            raise ValueError(f"Duplicate asset id or path: {asset['id']}")
        ids.add(asset['id']); paths.add(asset['path'])
        local(asset['path'], artwork)
        parts = Path(asset['path']).parts
        if len(parts) == 5 and parts[:2] == ('sources', 'backgrounds'):
            asset.setdefault('neighborhood', parts[2])
            asset.setdefault('phase', parts[3])
            asset.setdefault('shape', Path(parts[4]).stem.split('-')[0])
            slot = tuple(asset[key] for key in ('neighborhood', 'phase', 'shape'))
            expected = (parts[2], parts[3], Path(parts[4]).stem.split('-')[0])
            if slot != expected:
                raise ValueError(f"Asset slot disagrees with path: {asset['id']}")
            if slot in slots:
                raise ValueError(f'Multiple versions for {slot}; choose one explicitly before building.')
            slots[slot] = asset
    first = read(artwork / 'layouts/first-pass.json')
    source = neighborhood_manifest or artwork.parent.parent / 'namisuke-no-toki/assets/manifest.json'
    scenes = neighborhood_names(source, artwork / 'layouts/collection.json')
    known = {scene['id'] for scene in scenes}
    for area, phase, shape in slots:
        if area not in known or phase not in PHASES or shape not in SHAPES:
            raise ValueError(f'Unknown background slot: {(area, phase, shape)}')
    registered = {a['path'] for a in assets if local(a['path'], artwork).is_file()}
    missing, available = [], 0
    for scene in scenes:
        scene['phases'] = {}
        for phase in PHASES:
            backgrounds = {}
            phase_missing = []
            for shape in SHAPES:
                slot = (scene['id'], phase, shape)
                asset = slots.get(slot)
                path = asset['path'] if asset else None
                backgrounds[shape] = path if path in registered else None
                if backgrounds[shape]:
                    available += 1
                else:
                    entry = {'neighborhood': scene['id'], 'phase': phase, 'shape': shape}
                    missing.append(entry); phase_missing.append(shape)
            desired = CHARACTERS[phase]
            fallback = desired not in registered and CHARACTERS['evening'] in registered
            character = desired if desired in registered else CHARACTERS['evening'] if fallback else None
            scene['phases'][phase] = {
                'backgrounds': backgrounds,
                'character': character,
                'character_requested': desired,
                'character_fallback': fallback,
                'missing_backgrounds': phase_missing,
            }
    summary = {
        'neighborhoods': len(scenes), 'phases': len(PHASES),
        'backgrounds_available': available,
        'backgrounds_expected': len(scenes) * len(PHASES) * len(SHAPES),
        'backgrounds_missing': missing,
        'characters_missing': sorted(set(CHARACTERS.values()) - registered),
    }
    manifest = {'schema_version': 1, 'status': 'design-prototype-not-client-api',
                'assets': assets, 'summary': summary}
    layout = {'schema_version': 1, 'status': 'design-prototype-not-client-api',
              'phase_order': list(PHASES),
              **{key: first[key] for key in ('colors', 'typography', 'surfaces')},
              'summary': summary, 'scenes': scenes}
    return manifest, layout

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--neighborhood-manifest', type=Path)
    args = parser.parse_args()
    manifest, layout = build(neighborhood_manifest=args.neighborhood_manifest)
    for path, payload in ((ARTWORK / 'collection-manifest.json', manifest),
                          (ARTWORK / 'layouts/collection.json', layout)):
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    summary = manifest['summary']
    print(f"{summary['backgrounds_available']}/{summary['backgrounds_expected']} backgrounds; "
          f"{len(summary['characters_missing'])} character variants missing. Published v0 untouched.")

if __name__ == '__main__':
    main()
