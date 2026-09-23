# Neighborhood collection review

The collection expands the approved two-neighborhood evening study to 23 neighborhoods, four
phases and two background shapes: **184 independently registered backgrounds**, plus shared
transparent Namisuke variants. The round watch and square widget share a square source; the wide
widget uses its own 2:1 composition. This is a source-art and browser-layout collection, not a
published client API or installed widget.

[Open the review](review/) and choose a neighborhood and time of day. Only the selected pair is
loaded, producing round, square and wide previews. A URL such as
`review/?area=kugayama&phase=night` links directly to a composition. Neighborhood names appear in
Japanese first; the approved regular serif and 95% text opacity are inherited from
[the original layout](layouts/first-pass.json).

## Delivery status

All **184 backgrounds and three shared transparent characters** are present and individually
reviewed. Every neighborhood has morning, midday, evening and night in square and wide formats.
The five approved first-pass assets remain unchanged. New assets are collection drafts; the
source PNGs are not optimized runtime downloads.

Preview sheets: [morning](review/collection-morning.png), [midday](review/collection-midday.png),
[evening](review/collection-evening.png), [night](review/collection-night.png), and
[the Kugayama/Nishi-Ogikubo day cycles](review/day-cycles.png).

Small generative differences are recorded in each asset's `visual_review`. Some daytime shop
or street lights retain warm highlights, and a few lamp fixtures vary between phases. These
are discrete illustrations; they are not registered frames for seamless animated transitions.
The shared character variants retain a slight soft edge halo from the approved reference.
Native watch/widget integration, runtime export sizes and physical-device checks remain future work.

## Build and check

From the repository root:

```sh
python3 artwork/scripts/build_catalogue.py
python3 artwork/scripts/validate_catalogue.py
python3 -m http.server 8000
```

Open http://localhost:8000/artwork/review/. Rebuild after adding or correcting records. The build
combines the five approved assets in `artwork/manifest.json` with JSON records in `artwork/records/`.
It writes [the collection manifest](collection-manifest.json) and
[review layouts](layouts/collection.json), without modifying `v0/` or the original five assets.
A record is one asset object (or an object containing an `assets` array), with immutable id/path,
area, phase, shape, dimensions, mode, SHA-256, prompt, references, generator and status.

The initial neighborhood names come from the sibling app's `assets/manifest.json`. Subsequent
builds can use the saved collection names if the sibling checkout is absent. Use
`--neighborhood-manifest /path/to/manifest.json` to explicitly choose that source.

Missing square or wide files produce labelled placeholders, never another neighborhood or time
of day. Missing daytime/night character variants use the approved evening character with a
visible fallback notice. Unregistered files are not silently counted as complete. The generated
manifest's `summary` is the current availability report; it lists every missing background and
character variant. The delivery above passed the complete-collection gate; future additions still use the same missing-slot checks.

Validation checks unique asset IDs/paths/slots, file hashes, PNG dimensions/mode, square/wide
aspect ratios, prompt/reference paths and stale generated metadata. An incomplete collection is
valid work in progress. For a finished delivery gate, run:

```sh
python3 artwork/scripts/validate_catalogue.py --require-complete
```

These checks establish catalogue integrity. They do not establish visual quality, contrast on a
physical device, native widget performance, or an artwork license. Weather remains explicitly
sample data. The device clock can change independently of the chosen scene mood.
